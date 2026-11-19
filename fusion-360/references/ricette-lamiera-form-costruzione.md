# Sheet metal, T-spline forms, joint origins, appearances, scene; construction, surfaces, sketch

**Index** (long file: look up the section, do not read it all)
| Line | Recipe | When |
|---|---|---|
| 16 | Sheet metal (rule, flange, flat pattern), T-spline form, joint origin, component colour, scene | sheet metal parts, free forms, joints, appearance |
| 174 | 13 commands: construction, surfaces (stitch, extend), sketch (offset, fillet, mirror), SVG, pipe, scale, move, split face, interference, unfold and refold | when one of these commands is needed |

Recipes tested in Fusion (Nov. 2026), each with the expected measurements computed beforehand and found again in the model. Each block is a complete
script to run with Python on the PC: it talks to Fusion through `scripts/mcp_fusion.py` (the `sys.path.insert` line points to the
`scripts/` folder of the skill installed in `~/.claude/skills/fusion-360`: change it if you put it elsewhere) and sends Fusion the
code in the upper-case strings (`CODICE`, `CODICI`…). In a real model copy the part you need into the step scripts (`scripts/progetto_locale.py`).
Here: sheet metal flat pattern = bend formula; 13 commands all equal to the expected values (construction planes, axes and points, pipe, scale,
move, split face, interference, surface stitch and extend, unfold and refold, SVG at 96 dpi).

## Sheet metal, T-spline form, joint origin, component colour, scene (new unsaved design)

A sheet metal: active rule, 100 × 60 base flange from a profile, flange on an edge (20 mm), flat pattern; expected: flat pattern
   length = inner legs + neutral length of the bend, BA = π/2 · (R + K·T) (90°), with R, K, T read from the rule.
B form: T-spline body from a primitive (box) inside a FormFeature (startEdit/finishEdit), resulting B-rep body.
C joint origin at the centre of the top face of a 40 × 30 × 10 block: expected (0, 0, 10) mm.
D component colour: appearance from the library assigned to the occurrence, read back.
E scene (Render): environment background and ground set and read back; no rendering in this test (local rendering is free: tavole-e-render.md).
Run one step at a time: `nuovo`, then `lamiera`, `form`, `giunto`, `colore`, `scena`. Measured: sheet metal — base 15,000 mm³ =
expected, flat pattern 80.655 mm = 65 + 20 − 2(R + T) + π/2·(R + K·T) with the rule «Acciaio (mm)» (Steel (mm); T 2.5, R 2.5, K 0.44); form — solid of
18,896.7 mm³ (the T-spline rounds the edges of the 24,000 box); joint origin (0; 0; 10) = expected; appearance «Acrilico (rosso)» (Acrylic (red))
read back and inherited by the body; scene — 14 environments, environment, ground and reflections set and read back. Traps: the sheet metal
component is created with `addNewSheetMetalComponent` and must be **activated** (`occ.activate()`), otherwise the flange ends up in the root
component; the rules collection is called `designSheetMetalRules` and in a design without sheet metal it gives «smDataRoot»; T-spline forms
from a sketch, bridge and repair have no API.

```python
"""Sheet metal, T-spline form, joint origin, colour, scene via API, in a new UNSAVED design.
A sheet metal: active rule, 100 × 60 base flange from a profile, flange on an edge (20 mm), flat pattern; expected: flat pattern
   length = inner legs + neutral length of the bend, BA = π/2 · (R + K·T) (90°), with R, K, T read from the rule.
B form: T-spline body from a primitive (box) inside a FormFeature (startEdit/finishEdit), resulting B-rep body.
C joint origin at the centre of the top face of a 40 × 30 × 10 block: expected (0, 0, 10) mm.
D component colour: appearance from the library assigned to the occurrence, read back.
E scene (Render): environment background and ground set and read back; no rendering in this test (local rendering is free: tavole-e-render.md).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui

TESTA = r'''
import math, traceback
d = adsk.fusion.Design.cast(app.activeProduct); r = d.rootComponent; F = r.features
P = adsk.core.Point3D.create; V = adsk.core.Vector3D.create; VI = adsk.core.ValueInput.createByString
def errori():
    t = d.timeline
    return [t.item(k).name for k in range(t.count) if t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
'''
CODICI = {
"nuovo": r'''
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
out(doc=app.activeDocument.name)''',
"lamiera": r'''
ris = {}
try:
    occ = r.occurrences.addNewSheetMetalComponent(adsk.core.Matrix3D.create()); c = occ.component; c.name = "lamiera"   # normal component: no rule (04/11)
    occ.activate()      # without it, the flange ends up in the root component (04/11)
    # d.designSheetMetalRules (the real name, not sheetMetalRules) in a design without sheet metal gives «smDataRoot» (04/11): use the
    # component's active rule
    reg = c.activeSheetMetalRule
    val = lambda x: x.value if hasattr(x, "value") else x            # some are parameters, kFactor is a number (04/11)
    T, R, K = val(reg.thickness), val(reg.bendRadius), val(reg.kFactor)
    ris["regola"] = {"nome": reg.name, "T_mm": round(T * 10, 4), "R_espr": getattr(reg.bendRadius, "expression", None), "R_mm": round(R * 10, 4), "K": round(K, 4)}
    sk = c.sketches.add(c.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(10, 6, 0))
    fi = c.features.flangeFeatures.createBaseFlangeInput([sk.profiles.item(0)])
    ff = c.features.flangeFeatures.add(fi); b = c.bRepBodies.item(0)
    ris["base"] = {"lamiera": b.isSheetMetal, "volume_mm3": round(b.volume * 1000, 2), "atteso_mm3": round(100 * 60 * T * 10, 2)}
    # 100 mm long edge on the y = 0 side, top face
    top = max([b.faces.item(k) for k in range(b.faces.count)], key=lambda f_: f_.pointOnFace.z)
    ed = [top.edges.item(k) for k in range(top.edges.count) if abs(top.edges.item(k).length - 10) < 1e-6 and abs(top.edges.item(k).pointOnEdge.y) < 1e-6][0]
    ei = c.features.flangeFeatures.createEdgeFlangeInput([ed], VI("20 mm"))
    c.features.flangeFeatures.add(ei)
    b = c.bRepBodies.item(0); bb = b.boundingBox
    ris["piegato"] = {"ingombro_mm": [round((bb.maxPoint.x - bb.minPoint.x) * 10, 3), round((bb.maxPoint.y - bb.minPoint.y) * 10, 3), round((bb.maxPoint.z - bb.minPoint.z) * 10, 3)],
                      "volume_mm3": round(b.volume * 1000, 2)}
    # flat pattern: stationary face = the largest planar face of the part
    fissa = max([b.faces.item(k) for k in range(b.faces.count) if b.faces.item(k).geometry.objectType == adsk.core.Plane.classType()], key=lambda f_: f_.area)
    fp = c.createFlatPattern(fissa)
    fb = fp.flatBody if hasattr(fp, "flatBody") else fp.bodies.item(0)
    fbb = fb.boundingBox
    dims = sorted([round((fbb.maxPoint.x - fbb.minPoint.x) * 10, 3), round((fbb.maxPoint.y - fbb.minPoint.y) * 10, 3), round((fbb.maxPoint.z - fbb.minPoint.z) * 10, 3)])
    ris["sviluppo_mm"] = dims
    ris["sviluppo_volume_mm3"] = round(fb.volume * 1000, 2)
    d.activateRootComponent()
except Exception:
    ris["errore"] = traceback.format_exc()[-700:]
ris["errori"] = errori()
out(**ris)''',
"form": r'''
ris = {}
try:
    occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create()); c = occ.component; c.name = "forma"
    fo = c.features.formFeatures.add()
    fo.startEdit()
    bi = fo.tSplineBodies.createBoxInput(P(10, 0, 0), V(1, 0, 0), V(0, 1, 0), 4.0, 3.0, 2.0)
    tb = fo.tSplineBodies.addByShapeInput(bi)
    ris["tspline"] = {"facce": tb.faces.count if tb else None, "vertici": tb.vertices.count if tb else None}
    fo.finishEdit()
    bs = [c.bRepBodies.item(k) for k in range(c.bRepBodies.count)]
    ris["corpi"] = [{"nome": x.name, "solido": x.isSolid, "volume_mm3": round(x.volume * 1000, 1)} for x in bs]
    ris["nota"] = "box 40 x 30 x 20 = 24000 mm3: the T-spline rounds the edges, the volume must be smaller"
except Exception:
    ris["errore"] = traceback.format_exc()[-700:]
ris["errori"] = errori()
out(**ris)''',
"giunto": r'''
ris = {}
try:
    occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create()); c = occ.component; c.name = "blocco"
    sk = c.sketches.add(c.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(-2, -1.5, 0), P(2, 1.5, 0))
    b = c.features.extrudeFeatures.addSimple(sk.profiles.item(0), VI("10 mm"), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    top = max([b.faces.item(k) for k in range(b.faces.count)], key=lambda f_: f_.pointOnFace.z)
    g = adsk.fusion.JointGeometry.createByPlanarFace(top, None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
    jo = c.jointOrigins.add(c.jointOrigins.createInput(g)); jo.name = "presa"
    o = jo.geometry.origin
    ris["origine_mm"] = [round(o.x * 10, 4), round(o.y * 10, 4), round(o.z * 10, 4)]
    ris["asse_z"] = [round(v, 4) for v in jo.geometry.primaryAxisVector.asArray()]
except Exception:
    ris["errore"] = traceback.format_exc()[-700:]
ris["errori"] = errori()
out(**ris)''',
"colore": r'''
ris = {}
try:
    occ = [r.occurrences.item(k) for k in range(r.occurrences.count) if r.occurrences.item(k).component.name == "blocco"][0]
    lib = [app.materialLibraries.item(k) for k in range(app.materialLibraries.count) if any(w in app.materialLibraries.item(k).name.lower() for w in ("appearance", "aspetti"))]   # translated names (04/11)
    ris["librerie"] = [app.materialLibraries.item(k).name for k in range(app.materialLibraries.count)]
    ap = None
    for L_ in lib:
        for k in range(L_.appearances.count):
            a = L_.appearances.item(k)
            if any(w in a.name.lower() for w in ("red", "rosso")): ap = a; break
        if ap: break
    if ap is None: ap = lib[0].appearances.item(0)
    occ.appearance = ap
    ris["assegnato"] = ap.name; ris["riletto"] = occ.appearance.name if occ.appearance else None
    ris["corpo_eredita"] = occ.bRepBodies.item(0).appearance.name
except Exception:
    ris["errore"] = traceback.format_exc()[-700:]
out(**ris)''',
"scena": r'''
ris = {}
try:
    rm = d.renderManager; ss = rm.sceneSettings; envs = rm.renderEnvironments
    ris["ambienti"] = [envs.item(k).name for k in range(envs.count)]
    prima = {"sfondo": str(ss.backgroundType), "ambiente": ss.backgroundEnvironment.name if ss.backgroundType == adsk.fusion.RenderSceneBackgroundTypes.EnvironmentRenderSceneBackgroundType else "(background is not an environment: not readable)", "pavimento": ss.isGroundDisplayed}
    e = envs.item(envs.count - 1)
    ss.backgroundEnvironment = e      # backgroundType is read-only: assigning the environment changes it (04/11)
    ss.isGroundDisplayed = True; ss.isGroundReflections = True
    ris["prima"] = prima
    ris["dopo"] = {"sfondo": str(ss.backgroundType), "ambiente": ss.backgroundEnvironment.name, "pavimento": ss.isGroundDisplayed, "riflessi": ss.isGroundReflections}
except Exception:
    ris["errore"] = traceback.format_exc()[-700:]
out(**ris)''',
}

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    passo = sys.argv[1]
    codice = CODICI[passo] if passo == "nuovo" else TESTA + CODICI[passo]
    ok, r, righe = esegui(Sessione(), codice, sola_lettura=False)
    print(json.dumps(r if r else righe, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
```

## 13 commands: construction, surfaces, sketch, SVG, sheet metal (new unsaved design)

Each item has its expected value computed beforehand; outcome ok if |measured − expected| ≤ 0.01 (mm, mm², mm³) unless stated otherwise.
 1 ellipse a 20, b 10 → area π·20·10 = 628.319 mm²          2 sketch offset of a 40 × 20 rectangle by 5 mm → perimeter 160 (sharp
 3 sketch fillet R 5 between two lines at 90° → arc 7.854       corners) or 151.416 (filleted): record which
 4 mirror of a circle (10, 0) about the Y axis → (−10, 0)       5 SVG 50 × 30 mm (width/height in mm) imported → bounding box recorded
 6 pipe Ø 10 on a 100 line → 7,853.982 mm³                      7 scale ×2 of a 10 cube → 8,000 mm³
 8 move by (30, 0, 0) → minimum x +30                           9 split of the top face with a plane → faces +1
10 construction: offset plane 15 → z 15; midplane between z 0 and z 10 → z 5; point at the centre of a circle (20, 20); point from 3 planes;
   axis from the pipe cylinder (item 6) → X direction
11 interference between two 10 cubes overlapping by 5 → 500 mm³    12 surfaces: patch 20 × 10 + wall 20 × 10 sharing an edge, stitch → 1 body, 400 mm²;
   extend by 5 of an edge of a 20 × 10 patch → 300 mm²
13 sheet metal: unfold of a bend (Unfold) and refold (Refold) → same volume and same bounding box as at the start

Outcome: all items equal to the expected values; to note: 2 offset → 160 (sharp corners, not filleted); 5 SVG of 50 × 30 mm → 13.229 ×
7.937, i.e. Fusion reads the units as pixels at 96 dpi (scale 96/25.4 to get mm); 12a stitch → 1 body with 2 faces, a surface (not a
solid); 13 sheet metal → unfolded 2.5 high and 80.655 wide, but after «Refold» the part may end up rotated (65 high instead of 20):
re-check the bounding box. Copying the faces of a solid with offset 0 gives a SOLID, and stitch rejects it: real surfaces are needed.

```python
"""Test of 13 useful commands (construction, surfaces, sketch, SVG, sheet metal), in a new unsaved design.
Each item has its expected value computed beforehand; outcome ok if |measured − expected| ≤ 0.01 (mm, mm², mm³) unless stated otherwise.
 1 ellipse a 20, b 10 → area π·20·10 = 628.319 mm²          2 sketch offset of a 40 × 20 rectangle by 5 mm → perimeter 160 (sharp
 3 sketch fillet R 5 between two lines at 90° → arc 7.854       corners) or 151.416 (filleted): record which
 4 mirror of a circle (10, 0) about the Y axis → (−10, 0)       5 SVG 50 × 30 mm (width/height in mm) imported → bounding box recorded
 6 pipe Ø 10 on a 100 line → 7,853.982 mm³                      7 scale ×2 of a 10 cube → 8,000 mm³
 8 move by (30, 0, 0) → minimum x +30                           9 split of the top face with a plane → faces +1
10 construction: offset plane 15 → z 15; midplane between z 0 and z 10 → z 5; point at the centre of a circle (20, 20); point from 3 planes;
   axis from the pipe cylinder (item 6) → X direction
11 interference between two 10 cubes overlapping by 5 → 500 mm³    12 surfaces: patch 20 × 10 + wall 20 × 10 sharing an edge, stitch → 1 body, 400 mm²;
   extend by 5 of an edge of a 20 × 10 patch → 300 mm²
13 sheet metal: unfold of a bend (Unfold) and refold (Refold) → same volume and same bounding box as at the start
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui
QUI = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")

CODICE = r'''
import math, traceback
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; V = adsk.core.Vector3D.create; VI = adsk.core.ValueInput.createByString
OP = adsk.fusion.FeatureOperations
ris = {}
def esito(k, mis, att, tol=0.01):
    ok = None if att is None else (abs(mis - att) <= tol if isinstance(att, (int, float)) else mis == att)
    ris[k] = {"misurato": mis, "atteso": att, "ok": ok}
def prova(k, f):
    try: f()
    except Exception: ris[k] = {"errore": traceback.format_exc()[-400:]}
def cubo(x, y, z, l=1.0, nome=None):
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, adsk.core.ValueInput.createByReal(z)); pl = r.constructionPlanes.add(pi)
    sk = r.sketches.add(pl); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(x, y, 0), P(x + l, y + l, 0))
    b = F.extrudeFeatures.addSimple(sk.profiles.item(0), adsk.core.ValueInput.createByReal(l), OP.NewBodyFeatureOperation).bodies.item(0)
    if nome: b.name = nome
    return b
mm2 = lambda a: round(a * 100, 3); mm3 = lambda v: round(v * 1000, 3); mm = lambda x: round(x * 10, 3)

def p1():
    sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchEllipses.add(P(0, 0, 0), P(2, 0, 0), P(0, 1, 0))
    esito("1_ellisse_area_mm2", mm2(sk.profiles.item(0).areaProperties().area), round(math.pi * 200, 3))
def p2():
    sk = r.sketches.add(r.xYConstructionPlane); L = sk.sketchCurves.sketchLines.addTwoPointRectangle(P(10, 10, 0), P(14, 12, 0))
    oc = adsk.core.ObjectCollection.create(); [oc.add(L.item(k)) for k in range(L.count)]
    nuove = sk.offset(oc, P(20, 20, 0), 0.5)
    lung = sum(nuove.item(k).length for k in range(nuove.count))
    tipi = sorted(set(nuove.item(k).objectType.split("::")[-1] for k in range(nuove.count)))
    ris["2_offset"] = {"perimetro_mm": mm(lung), "tipi": tipi, "spigoli_vivi_160": abs(mm(lung) - 160) < 0.01, "raccordati_151_416": abs(mm(lung) - 151.416) < 0.01}
def p3():
    sk = r.sketches.add(r.xYConstructionPlane); A = sk.sketchCurves.sketchLines
    a = A.addByTwoPoints(P(30, 0, 0), P(34, 0, 0)); b = A.addByTwoPoints(a.endSketchPoint, P(34, 4, 0))
    arc = sk.sketchCurves.sketchArcs.addFillet(a, P(33, 0, 0), b, P(34, 1, 0), 0.5)
    esito("3_raccordo_arco_mm", mm(arc.length), round(math.pi * 5 / 2, 3)); ris["3_raccordo_arco_mm"]["raggio"] = mm(arc.radius)
def p4():
    sk = r.sketches.add(r.xYConstructionPlane)
    c = sk.sketchCurves.sketchCircles.addByCenterRadius(P(1, 5, 0), 0.3)
    asse = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, 4, 0), P(0, 6, 0)); asse.isConstruction = True
    m = sk.mirror([c], asse)
    cc = [e for e in m if e.objectType == adsk.fusion.SketchCircle.classType()][0].centerSketchPoint.geometry
    esito("4_specchio_x_mm", mm(cc.x), -10.0)
def p5():
    sk = r.sketches.add(r.xYConstructionPlane)
    ok = sk.importSVG(SVG, 0, 0, 1)
    xs, ys = [], []
    for k in range(sk.sketchCurves.count):
        bb = sk.sketchCurves.item(k).boundingBox; xs += [bb.minPoint.x, bb.maxPoint.x]; ys += [bb.minPoint.y, bb.maxPoint.y]
    ris["5_svg"] = {"importato": ok, "ingombro_mm": [mm(max(xs) - min(xs)), mm(max(ys) - min(ys))] if xs else None, "atteso_se_mm": [50, 30]}
def p6():
    sk = r.sketches.add(r.xZConstructionPlane); ln = sk.sketchCurves.sketchLines.addByTwoPoints(P(50, 0, 0), P(60, 0, 0))
    pi = F.pipeFeatures.createInput(F.createPath(ln), OP.NewBodyFeatureOperation); pi.sectionSize = adsk.core.ValueInput.createByReal(1.0)
    b = F.pipeFeatures.add(pi).bodies.item(0)
    esito("6_tubo_mm3", mm3(b.volume), round(math.pi * 25 * 100, 3), 0.05)
def p7():
    b = cubo(-10, -10, 0, 1.0, "da scalare")
    oc = adsk.core.ObjectCollection.create(); oc.add(b)
    si = F.scaleFeatures.createInput(oc, r.originConstructionPoint, adsk.core.ValueInput.createByReal(2)); F.scaleFeatures.add(si)
    esito("7_scala_mm3", mm3(r.bRepBodies.itemByName("da scalare").volume), 8000.0)
def p8():
    b = cubo(-10, 20, 0, 1.0, "da spostare"); x0 = b.boundingBox.minPoint.x
    oc = adsk.core.ObjectCollection.create(); oc.add(b)
    m = adsk.core.Matrix3D.create(); m.translation = V(3, 0, 0)
    F.moveFeatures.add(F.moveFeatures.createInput(oc, m))
    esito("8_sposta_dx_mm", mm(r.bRepBodies.itemByName("da spostare").boundingBox.minPoint.x - x0), 30.0)
def p9():
    b = cubo(20, 20, 0, 1.0, "da dividere"); n0 = b.faces.count
    top = max([b.faces.item(k) for k in range(b.faces.count)], key=lambda f_: f_.pointOnFace.z)
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.yZConstructionPlane, adsk.core.ValueInput.createByReal(20.5)); pl = r.constructionPlanes.add(pi)   # the cube is at x 20–21 cm (04/11)
    oc = adsk.core.ObjectCollection.create(); oc.add(top)
    F.splitFaceFeatures.add(F.splitFaceFeatures.createInput(oc, pl, True))
    esito("9_divisione_facce", r.bRepBodies.itemByName("da dividere").faces.count, n0 + 1, 0)
def p10():
    b = cubo(40, 0, 0, 1.0, "per costruzione")
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, adsk.core.ValueInput.createByReal(1.5))
    esito("10a_piano_offset_z_mm", mm(r.constructionPlanes.add(pi).geometry.origin.z), 15.0)
    fs = sorted([b.faces.item(k) for k in range(b.faces.count) if abs(b.faces.item(k).geometry.normal.z) > 0.99] if hasattr(b.faces.item(0).geometry, "normal") else [], key=lambda f_: f_.pointOnFace.z)
    fz = [f_ for f_ in [b.faces.item(k) for k in range(b.faces.count)] if f_.geometry.objectType == adsk.core.Plane.classType() and abs(f_.geometry.normal.z) > 0.99]
    fz.sort(key=lambda f_: f_.pointOnFace.z)
    pi = r.constructionPlanes.createInput(); pi.setByTwoPlanes(fz[0], fz[-1])
    esito("10b_piano_medio_z_mm", mm(r.constructionPlanes.add(pi).geometry.origin.z), 5.0)
    sk = r.sketches.add(r.xYConstructionPlane); ci = sk.sketchCurves.sketchCircles.addByCenterRadius(P(2, 2, 0), 0.5)
    pp = r.constructionPoints.createInput(); pp.setByCenter(ci)
    g = r.constructionPoints.add(pp).geometry; esito("10c_punto_centro_mm", [mm(g.x), mm(g.y)], [20.0, 20.0])
    pa = r.constructionPlanes.createInput(); pa.setByOffset(r.yZConstructionPlane, adsk.core.ValueInput.createByReal(0.7)); A_ = r.constructionPlanes.add(pa)
    pp = r.constructionPoints.createInput(); pp.setByThreePlanes(A_, r.xZConstructionPlane, r.xYConstructionPlane)
    g = r.constructionPoints.add(pp).geometry; esito("10d_punto_3_piani_mm", [mm(g.x), mm(g.y), mm(g.z)], [7.0, 0.0, 0.0])
    cyl = r.bRepBodies.item(r.bRepBodies.count - 1)
    tubo = [x for x in [r.bRepBodies.item(k) for k in range(r.bRepBodies.count)] if any(x.faces.item(j).geometry.objectType == adsk.core.Cylinder.classType() for j in range(x.faces.count))][0]
    cf = [tubo.faces.item(j) for j in range(tubo.faces.count) if tubo.faces.item(j).geometry.objectType == adsk.core.Cylinder.classType()][0]
    ai = r.constructionAxes.createInput(); ai.setByCircularFace(cf)
    v = r.constructionAxes.add(ai).geometry.direction; esito("10e_asse_cilindro_dir", [round(abs(v.x), 4), round(abs(v.y), 4), round(abs(v.z), 4)], [1.0, 0.0, 0.0])   # the pipe (test 6) runs along X
def p11():
    a = cubo(70, 0, 0, 1.0, "int A"); b = cubo(70.5, 0, 0, 1.0, "int B")
    oc = adsk.core.ObjectCollection.create(); oc.add(a); oc.add(b)
    res = d.analyzeInterference(d.createInterferenceInput(oc))
    esito("11_interferenza_mm3", mm3(sum(res.item(k).interferenceBody.volume for k in range(res.count))), 500.0)
def p12():
    # stitch: floor (20 × 10 patch) + wall (20 × 10 surface extrude) sharing an edge → 1 body, 2 faces, 400 mm²
    # (04/11: copying the faces of a solid with offset 0, even one at a time, gives a SOLID and stitch rejects it)
    sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, -50, 0), P(2, -49, 0))
    pav = F.patchFeatures.add(F.patchFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation)).bodies.item(0)
    sk2 = r.sketches.add(r.xYConstructionPlane); ln = sk2.sketchCurves.sketchLines.addByTwoPoints(P(0, -50, 0), P(2, -50, 0))
    ei = F.extrudeFeatures.createInput(F.createPath(ln), OP.NewBodyFeatureOperation); ei.isSolid = False
    ei.setDistanceExtent(False, adsk.core.ValueInput.createByReal(1.0)); par = F.extrudeFeatures.add(ei).bodies.item(0)
    sup = adsk.core.ObjectCollection.create(); sup.add(pav); sup.add(par)
    st = F.stitchFeatures.add(F.stitchFeatures.createInput(sup, adsk.core.ValueInput.createByReal(0.001), OP.NewBodyFeatureOperation))
    sb = st.bodies.item(0)
    esito("12a_unione_area_mm2", mm2(sum(sb.faces.item(k).area for k in range(sb.faces.count))), 400.0)
    ris["12a_unione_area_mm2"].update({"corpi": st.bodies.count, "facce": sb.faces.count, "solido": sb.isSolid})
    sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(-10, -40, 0), P(-8, -39, 0))
    pt = F.patchFeatures.add(F.patchFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation)).bodies.item(0)
    ed = [pt.edges.item(k) for k in range(pt.edges.count) if abs(pt.edges.item(k).length - 2) < 1e-6 and pt.edges.item(k).pointOnEdge.y > -39.5][0]
    oe = adsk.core.ObjectCollection.create(); oe.add(ed)
    ex = F.extendFeatures.add(F.extendFeatures.createInput(oe, adsk.core.ValueInput.createByReal(0.5), adsk.fusion.SurfaceExtendTypes.NaturalSurfaceExtendType, False))
    area = sum(f_.area for f_ in [ex.bodies.item(0).faces.item(k) for k in range(ex.bodies.item(0).faces.count)]) if ex.bodies.count else sum(pt.faces.item(k).area for k in range(pt.faces.count))
    esito("12b_estendi_mm2", mm2(area), 300.0)
def p13():
    occ = r.occurrences.addNewSheetMetalComponent(adsk.core.Matrix3D.create()); occ.activate(); c = occ.component
    sk = c.sketches.add(c.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 10, 0), P(10, 16, 0))
    c.features.flangeFeatures.add(c.features.flangeFeatures.createBaseFlangeInput([sk.profiles.item(0)]))
    b = c.bRepBodies.item(0)
    top = max([b.faces.item(k) for k in range(b.faces.count)], key=lambda f_: f_.pointOnFace.z)
    ed = [top.edges.item(k) for k in range(top.edges.count) if abs(top.edges.item(k).length - 10) < 1e-6 and abs(top.edges.item(k).pointOnEdge.y - 10) < 1e-6][0]
    c.features.flangeFeatures.add(c.features.flangeFeatures.createEdgeFlangeInput([ed], VI("20 mm")))
    b = c.bRepBodies.item(0); v0 = mm3(b.volume); bb = b.boundingBox; i0 = [mm(bb.maxPoint.z - bb.minPoint.z), mm(bb.maxPoint.y - bb.minPoint.y)]
    fissa = max([b.faces.item(k) for k in range(b.faces.count) if b.faces.item(k).geometry.objectType == adsk.core.Plane.classType()], key=lambda f_: f_.area)
    ui = c.features.unfoldFeatures.createInput(fissa); ui.isUnfoldAllBends = True        # without it: «at least one bend face» (04/11)
    un = c.features.unfoldFeatures.add(ui)
    b = c.bRepBodies.item(0); bb = b.boundingBox; iu = [mm(bb.maxPoint.z - bb.minPoint.z), mm(bb.maxPoint.y - bb.minPoint.y)]
    c.features.refoldFeatures.add(c.features.refoldFeatures.createInput(un))
    b = c.bRepBodies.item(0); bb = b.boundingBox; ir = [mm(bb.maxPoint.z - bb.minPoint.z), mm(bb.maxPoint.y - bb.minPoint.y)]
    ris["13_lamiera"] = {"piegato_alto_largo": i0, "sviluppato_alto_largo": iu, "ripiegato_alto_largo": ir, "volume_prima": v0, "volume_dopo": mm3(b.volume),
                         "ok": ir == i0 and abs(mm3(b.volume) - v0) < 0.01 and iu[0] < i0[0]}
    d.activateRootComponent()

for k, f in [(k_, f_) for k_, f_ in (("1", p1), ("2", p2), ("3", p3), ("4", p4), ("5", p5), ("6", p6), ("7", p7), ("8", p8), ("9", p9), ("10", p10), ("11", p11), ("12", p12), ("13", p13)) if not SOLO or k_ in SOLO]:
    prova(k, f)
t = d.timeline
ris["errori_timeline"] = [t.item(k).name for k in range(t.count) if t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    svg = QUI + "/rettangolo_50x30mm.svg"
    open(svg, "w", encoding="utf-8").write('<svg xmlns="http://www.w3.org/2000/svg" width="50mm" height="30mm" viewBox="0 0 50 30">'
                                          '<rect x="0" y="0" width="50" height="30" fill="none" stroke="black" stroke-width="0.2"/></svg>')
    solo = sys.argv[1:]          # e.g. 6 9 10 12 13: rerun only those items (10e uses the pipe from 6)
    ok, r, righe = esegui(Sessione(), f"SVG = {svg!r}\nSOLO = {solo!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r if r else righe, ensure_ascii=False, indent=1))
    if r and not solo: json.dump(r, open(QUI + "/comandi_provati.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
```

