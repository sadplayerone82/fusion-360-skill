# Text on a curved face, knurling, pattern along a path, rings

Recipes tested in Fusion (Nov. 2026), each with the expected measurements computed beforehand and found again in the model. Each block is a complete
script to run with Python on the PC: it talks to Fusion through `scripts/mcp_fusion.py` (the `sys.path.insert` line points to the
`scripts/` folder of the skill installed in `~/.claude/skills/fusion-360`: change it if you put it elsewhere) and sends Fusion the
code in the upper-case strings (`CODICE`, `CODICI`…). In a real model copy the part you need into the step scripts (`scripts/progetto_locale.py`).

**Index** (long file: look up the section, do not read it all)
| Line | Recipe | When |
|---|---|---|
| 16 | Embossed and engraved text on a cylindrical face | lettering on knobs, rings, curved objects |
| 108 | Straight and diamond knurling (IS 3403 / DIN 82) | knobs, grips |
| 247 | Pattern along a path | copies along a curve |
| 336 | Rings from the ISO 8653 size | jewellery |

## Embossed and engraved text on a cylindrical face (EmbossFeatures + SketchTexts.createInput3)

Two cylinders Ø 40 × 30 mm (Z axis); text «SKILL» 6 mm high on a tangent plane; emboss +1.0 mm on the first, engrave −0.8 mm on the second.
Expected: letters at radius 21.0 (emboss) and 19.2 (engrave); letter height = text height in the sketch; width along
the circumference (angle × radius) = flat width of the text in the sketch (wrapping without distortion).
Measured: emboss at 21.000 mm from the axis, bottom of the engraving at 19.200; width along the arc = flat width (22.158: no
distortion); letters 6.205 high (Arial at 6 mm); 0 errors. Traps: the text is an expression (`"'SKILL'"`, in quotes); on a plane
parallel to XZ, without `isVerticalFlip = True` the lettering comes out upside down, and only the front image shows it.

```python
"""Embossed and engraved text on a cylindrical face, via API (EmbossFeatures + SketchTexts.createInput3).
Two cylinders Ø 40 × 30 mm (Z axis); text «SKILL» 6 mm high on a tangent plane; emboss +1.0 mm on the first, engrave −0.8 mm on the second.
Expected: letters at radius 21.0 (emboss) and 19.2 (engrave); letter height = text height in the sketch; width along
the circumference (angle × radius) = flat width of the text in the sketch (wrapping without distortion).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:                                                         # closes only a document of this test left open
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("cilindro ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VI = adsk.core.ValueInput.createByString
ris = {"casi": {}}
for nome, x0, prof in (("rilievo", 0, "1.0 mm"), ("incisione", 6, "-0.8 mm")):
    sk = r.sketches.add(r.xYConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(P(x0, 0, 0), 2.0)
    cil = F.extrudeFeatures.addSimple(sk.profiles.item(0), VI("30 mm"), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    cil.name = "cilindro " + nome
    # plane tangent to the cylinder on the −Y side (parallel to XZ, 20 mm from the axis)
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xZConstructionPlane, VI("-20 mm")); pt = r.constructionPlanes.add(pi)
    skt = r.sketches.add(pt)
    ti = skt.sketchTexts.createInput3("'SKILL'", VI("6 mm"))       # the text is an EXPRESSION: it goes in quotes
    c0 = skt.modelToSketchSpace(P(x0 - 1.2, -2.0, 1.2)); c1 = skt.modelToSketchSpace(P(x0 + 1.2, -2.0, 1.8))
    ti.setAsMultiLine(c0, c1, adsk.core.HorizontalAlignments.CenterHorizontalAlignment, adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    ti.fontName = "Arial"
    ti.isVerticalFlip = True       # plane parallel to XZ: sketch y = model −Z → without flipping, the text comes out upside down
    st = skt.sketchTexts.add(ti)
    xs, zs = [], []
    for cv in st.asCurves():                                 # outline geometry of the letters (sketch space)
        ev = cv.evaluator; ok_, s, t = ev.getParameterExtents(); ok_, punti = ev.getStrokes(s, t, 0.0005)
        for q in punti:
            m = skt.sketchToModelSpace(q); xs.append(m.x); zs.append(m.z)
    piatto = {"larghezza_mm": round((max(xs) - min(xs)) * 10, 3), "altezza_mm": round((max(zs) - min(zs)) * 10, 3)}
    facce_cil = [f for f in [cil.faces.item(k) for k in range(cil.faces.count)] if f.geometry.objectType == adsk.core.Cylinder.classType()]
    ei = F.embossFeatures.createInput([st], facce_cil, VI(prof))     # (profiles or texts, faces, depth: + emboss, − engrave)
    em = F.embossFeatures.add(ei)
    # measurements on the created faces: distance from the axis (x0, 0) in plan, z coordinates, angle
    rs, zz, ang = [], [], []
    for k in range(em.faces.count):
        f = em.faces.item(k)
        ok_, a, b = f.evaluator.parametricRange().minPoint, None, None
        rg = f.evaluator.parametricRange()
        for i in range(7):
            for j in range(7):
                par = adsk.core.Point2D.create(rg.minPoint.x + (rg.maxPoint.x - rg.minPoint.x) * i / 6, rg.minPoint.y + (rg.maxPoint.y - rg.minPoint.y) * j / 6)
                if not f.evaluator.isParameterOnFace(par): continue
                ok_, q = f.evaluator.getPointAtParameter(par)
                rr = math.hypot(q.x - x0, q.y); rs.append(rr); zz.append(q.z); ang.append(math.atan2(q.x - x0, -q.y))
    raggio_lettere = max(rs) if prof.startswith("1") else min(rs)
    ris["casi"][nome] = {"profondita": prof, "testo_piatto": piatto,
                         "raggio_esterno_o_fondo_mm": round(raggio_lettere * 10, 3),
                         "altezza_lettere_mm": round((max(zz) - min(zz)) * 10, 3),
                         "larghezza_su_arco_mm": round((max(ang) - min(ang)) * 20.0 if True else 0, 3),
                         "facce_create": em.faces.count, "stato": str(em.healthState), "volume_cm3": round(cil.volume, 4)}
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
vp = app.activeViewport; cam = vp.camera; cam.isSmoothTransition = False
cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
cam.target = P(0.3, 0, 1.5); cam.eye = P(0.3, -30, 1.5); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); vp.camera = cam; vp.fit()
vp.saveAsImageFile(IMG, 1000, 500)        # FRONT view (from the text side): shows whether it reads the right way up
ris["documento"] = app.activeDocument.name
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("testo_curvo.png")   # check image, in the folder you run from
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Knurling to IS 3403:1981 (from DIN 82): 90° profile, pitches 0.5–1.6 mm, 30° helix

Model: 90° V groove P/2 deep; n = round(π·d/P) grooves; helix with lead L = π·d / tan(30°).
Case A — RAA (straight, parallel to the axis), Ø 20 × 15, P 1.0 → n 63, groove bottoms at r = 9.5.
Case B — RGE (left + right, raised points), Ø 20 × 15, P 1.6 → n 39, groove bottoms at r = 9.2; grooves = triangle in the axial plane
swept along a helix drawn through points (the API does not create helices: CoilFeatures has no add/createInput).
Measured: RAA 63 grooves, bottoms at 9.501 (= expected), 191 faces; RGE 39 grooves per direction, helix with lead 108.8 mm, bottoms at 9.244
(= expected with the 0.1 mm flat crest), 0 slivers, 0 errors. Traps: without the second helix as a guide rail the profile rotates along the
sweep (crests eaten away, 39 detached slivers); the circular pattern wants a construction axis, not a sketch line; after a cut
that detaches pieces, take the largest body again; zero-thickness crests do not exist (neither in printing nor on CNC): flat crest.

```python
"""Knurling via API to IS 3403:1981 (from DIN 82): 90° profile, pitches 0.5–1.6 mm, 30° helix.
Model: 90° V groove P/2 deep; n = round(π·d/P) grooves; helix with lead L = π·d / tan(30°).
Case A — RAA (straight, parallel to the axis), Ø 20 × 15, P 1.0 → n 63, groove bottoms at r = 9.5.
Case B — RGE (left + right, raised points), Ø 20 × 15, P 1.6 → n 39, groove bottoms at r = 9.2; grooves = triangle in the axial plane
swept along a helix drawn through points (the API does not create helices: CoilFeatures has no add/createInput).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math, time
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("manopola ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VI = adsk.core.ValueInput.createByString; VR = adsk.core.ValueInput.createByReal
ris = {"coil_api": [m for m in ("add", "createInput") if hasattr(F.coilFeatures, m)], "casi": {}}
R, H = 1.0, 1.5                                                 # cm: Ø 20, 15 high
def cilindro(nome, x0):
    sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchCircles.addByCenterRadius(P(x0, 0, 0), R)
    b = F.extrudeFeatures.addSimple(sk.profiles.item(0), VR(H), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    b.name = nome; return b
def asse(x0):
    sk = r.sketches.add(r.xZConstructionPlane); l = sk.sketchCurves.sketchLines.addByTwoPoints(P(x0, 0, 0), P(x0, -1, 0))  # XZ: sketch y = −Z
    l.isConstruction = True
    ai = r.constructionAxes.createInput(); ai.setByTwoPoints(l.startSketchPoint, l.endSketchPoint)   # a real construction axis
    return r.constructionAxes.add(ai)
def serie(feat, ax, n, corpo):
    oc = adsk.core.ObjectCollection.create(); oc.add(feat)
    pi = F.circularPatternFeatures.createInput(oc, ax); pi.quantity = VR(n); pi.totalAngle = VI("360 deg"); pi.isSymmetric = False
    try: return F.circularPatternFeatures.add(pi)
    except Exception as e: ris.setdefault("errori_serie", []).append(str(e)[:150]); return None
def misura(b, x0):
    rs = []
    for k in range(b.faces.count):
        f = b.faces.item(k); rg = f.evaluator.parametricRange()
        for i in range(5):
            for j in range(5):
                par = adsk.core.Point2D.create(rg.minPoint.x + (rg.maxPoint.x - rg.minPoint.x) * i / 4, rg.minPoint.y + (rg.maxPoint.y - rg.minPoint.y) * j / 4)
                if not f.evaluator.isParameterOnFace(par): continue
                ok_, q = f.evaluator.getPointAtParameter(par)
                if 0.05 < q.z < H - 0.05: rs.append(math.hypot(q.x - x0, q.y))
    return round(min(rs) * 10, 3), round(max(rs) * 10, 3), b.faces.count, round(b.volume * 1000, 1)
def errori():
    t = d.timeline
    return [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
# ---- case A: RAA, P 1.0
p, x0 = 0.10, 0.0
n = round(math.pi * 2 * R / p); pr = math.pi * 2 * R / n
b = cilindro("manopola RAA", x0)
sk = r.sketches.add(r.xYConstructionPlane)                     # 90° V groove: tip at r = R − P/2, sides at 45° beyond the edge
L = sk.sketchCurves.sketchLines
a = P(x0, -(R - pr / 2), 0); s = P(x0 - pr * 0.75, -(R + pr / 4), 0); t_ = P(x0 + pr * 0.75, -(R + pr / 4), 0)
L.addByTwoPoints(a, s); L.addByTwoPoints(s, t_); L.addByTwoPoints(t_, a)
prof = min([sk.profiles.item(k) for k in range(sk.profiles.count)], key=lambda q: q.areaProperties().area)
ei = F.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation); ei.setDistanceExtent(False, VR(H)); ei.participantBodies = [b]
taglio = F.extrudeFeatures.add(ei)
t0 = time.time(); serie(taglio, asse(x0), n, b)
ris["casi"]["RAA"] = {"P": 1.0, "n": n, "passo_reale_mm": round(pr * 10, 4), "atteso_fondi_creste_mm": [round((R - pr / 2) * 10, 3), R * 10],
                      "misurato_min_max_facce_volume": misura(b, x0), "serie_s": round(time.time() - t0, 1)}
# ---- case B: RGE, P 1.6, 30° helix (left and right)
p, x0 = 0.16, 3.0
n = round(math.pi * 2 * R / p); pr = math.pi * 2 * R / n
Lead = math.pi * 2 * R / math.tan(math.radians(30))          # cm
b = cilindro("manopola RGE", x0)
ax = asse(x0)
for verso in (1, -1):
    # helix through points on radius R (3D), from z −0.1 to H + 0.1 (it runs out of the part)
    sk = r.sketches.add(r.xYConstructionPlane)
    pts = adsk.core.ObjectCollection.create()
    for k in range(61):          # 3 mm beyond each face: the spline ends drift away from the true helix (slivers on the edge, 03/11)
        z = -0.3 + (H + 0.6) * k / 60; th = verso * 2 * math.pi * z / Lead - math.pi / 2
        pts.add(P(x0 + R * math.cos(th), R * math.sin(th), z))
    elica = sk.sketchCurves.sketchFittedSplines.add(pts)
    guida = adsk.core.ObjectCollection.create()             # second helix, same shape, radius R + P: keeps the profile facing the axis
    for k in range(61):
        z = -0.3 + (H + 0.6) * k / 60; th = verso * 2 * math.pi * z / Lead - math.pi / 2
        guida.add(P(x0 + (R + pr) * math.cos(th), (R + pr) * math.sin(th), z))
    rotaia = sk.sketchCurves.sketchFittedSplines.add(guida)
    # profile: triangle in the plane normal to the helix at its start (plane through the first point, normal = tangent)
    p0 = pts.item(0); p1 = pts.item(1)
    tg = p0.vectorTo(p1); tg.normalize()
    pl = r.constructionPlanes.createInput(); pl.setByDistanceOnPath(elica, VR(0)); piano = r.constructionPlanes.add(pl)
    sp = r.sketches.add(piano)
    rad = adsk.core.Vector3D.create(p0.x - x0, p0.y, 0); rad.normalize()
    lat = tg.crossProduct(rad); lat.normalize()
    def pp(u, v): return sp.modelToSketchSpace(P(p0.x + rad.x * u + lat.x * v, p0.y + rad.y * u + lat.y * v, p0.z + rad.z * u + lat.z * v))
    Ls = sp.sketchCurves.sketchLines
    # 0.1 mm flat crest (03/11): with V grooves as wide as the pitch the crests have zero thickness and Fusion detaches slivers
    piatto = 0.01; dd = (pr - piatto) / 2
    A_ = pp(-dd, 0); B_ = pp(pr / 4, -(dd + pr / 4)); C_ = pp(pr / 4, dd + pr / 4)
    Ls.addByTwoPoints(A_, B_); Ls.addByTwoPoints(B_, C_); Ls.addByTwoPoints(C_, A_)
    prof = min([sp.profiles.item(k) for k in range(sp.profiles.count)], key=lambda q: q.areaProperties().area)
    path = F.createPath(elica)
    swi = F.sweepFeatures.createInput(prof, path, adsk.fusion.FeatureOperations.CutFeatureOperation); swi.participantBodies = [b]
    swi.guideRail = F.createPath(rotaia); swi.profileScaling = adsk.fusion.SweepProfileScalingOptions.SweepProfileNoScalingOption
    sw = F.sweepFeatures.add(swi)
    t0 = time.time(); serie(sw, ax, n, b)
    lato = "destra" if verso > 0 else "sinistra"
    ris["casi"].setdefault("RGE", {})["serie_%s_s" % lato] = round(time.time() - t0, 1)
    corpi = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count) if r.bRepBodies.item(k).name != "manopola RAA"]
    b = max(corpi, key=lambda c: c.volume); b.name = "manopola RGE"           # the real part = the largest body
    ris["casi"]["RGE"]["schegge_dopo_" + lato] = sum(1 for c in corpi if c != b)
ris["casi"]["RGE"].update({"P": 1.6, "n": n, "passo_reale_mm": round(pr * 10, 4), "passo_elica_mm": round(Lead * 10, 1),
                           "atteso_fondi_creste_mm": [round((R - (pr - 0.01) / 2) * 10, 3), R * 10], "misurato_min_max_facce_volume": misura(b, x0)})
ris["errori"] = errori()
vp = app.activeViewport; cam = vp.camera; cam.isSmoothTransition = False
cam.target = P(1.5, 0, 0.75); cam.eye = P(1.5, -12, 4); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); vp.camera = cam; vp.fit()
vp.saveAsImageFile(IMG, 1000, 600)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("zigrinatura.png")   # check image, in the folder you run from
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Pattern along a path (PathPatternFeatures)

Path: arc R 50 mm, 180° (length 157.08 mm) in the XY plane, from (50, 0) to (−50, 0) through (0, 50).
Case 1 «Extent»: 7 small cylinders Ø 6 over the whole length → centres at radius 50.000 and angles 0, 30, …, 180°.
Case 2 «Spacing»: 5 copies every 20 mm along the arc → angles 0; 22.92; 45.84; 68.75; 91.67°.
Case 3 orientation: small 10 × 4 block (long side tangent at the start): the copy at 90° must measure 10 (X) × 4 (Y) if it follows the
path, 4 × 10 if identical. Each case on a different Z plane (0, 20, 40 mm) so the bodies do not overlap.
Measured: «Extent» → radius 50.000 and angles 0/30/…/180; «Spacing» → angles = expected (s / R); identical orientation 4 × 10 everywhere,
along the path 10 × 4 at 90°; 0 errors. With «Extent» the distance is the length over which the copies are distributed (for the whole
path: `SketchCurve.length`); the position is measured with the bodies' centre of mass.

```python
"""Pattern along a path via API (PathPatternFeatures).
Path: arc R 50 mm, 180° (length 157.08 mm) in the XY plane, from (50, 0) to (−50, 0) through (0, 50).
Case 1 «Extent»: 7 small cylinders Ø 6 over the whole length → centres at radius 50.000 and angles 0, 30, …, 180°.
Case 2 «Spacing»: 5 copies every 20 mm along the arc → angles 0; 22.92; 45.84; 68.75; 91.67°.
Case 3 orientation: small 10 × 4 block (long side tangent at the start): the copy at 90° must measure 10 (X) × 4 (Y) if it follows the
path, 4 × 10 if identical. Each case on a different Z plane (0, 20, 40 mm) so the bodies do not overlap.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("seme ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VR = adsk.core.ValueInput.createByReal; VI = adsk.core.ValueInput.createByString
ris = {"tipi_distanza": [x for x in dir(adsk.fusion.PatternDistanceType) if x.endswith("Type")] if hasattr(adsk.fusion, "PatternDistanceType") else "?", "casi": {}}
R = 5.0
def piano_z(z):
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, VR(z)); return r.constructionPlanes.add(pi)
def arco(z):
    sk = r.sketches.add(piano_z(z)); a = sk.sketchCurves.sketchArcs.addByThreePoints(P(R, 0, 0), P(0, R, 0), P(-R, 0, 0))
    return F.createPath(a), a.length
def seme(nome, z, forma):
    sk = r.sketches.add(piano_z(z))
    if forma == "cilindro": sk.sketchCurves.sketchCircles.addByCenterRadius(P(R, 0, 0), 0.3)
    else: sk.sketchCurves.sketchLines.addTwoPointRectangle(P(R - 0.2, -0.5, 0), P(R + 0.2, 0.5, 0))     # 4 (X) × 10 (Y): long side tangent
    b = F.extrudeFeatures.addSimple(sk.profiles.item(0), VR(0.5), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    b.name = "seme " + nome; return b
def serie(b, path, n, dist, tipo, lungo):
    oc = adsk.core.ObjectCollection.create(); oc.add(b)
    pi = F.pathPatternFeatures.createInput(oc, path, VR(n), VR(dist), tipo)
    pi.isOrientationAlongPath = lungo
    return F.pathPatternFeatures.add(pi)
def posizioni(feat):
    out_ = []
    for k in range(feat.bodies.count):
        bb = feat.bodies.item(k); c = bb.physicalProperties.centerOfMass; box = bb.boundingBox
        out_.append({"raggio_mm": round(math.hypot(c.x, c.y) * 10, 3), "angolo_gradi": round(math.degrees(math.atan2(c.y, c.x)), 2),
                     "ingombro_xy_mm": [round((box.maxPoint.x - box.minPoint.x) * 10, 2), round((box.maxPoint.y - box.minPoint.y) * 10, 2)]})
    return sorted(out_, key=lambda q: q["angolo_gradi"])
T = adsk.fusion.PatternDistanceType
# case 1: Extent
path, lung = arco(0.0); ris["lunghezza_arco_mm"] = round(lung * 10, 3)
f1 = serie(seme("extent", 0.0, "cilindro"), path, 7, lung, T.ExtentPatternDistanceType, False)
ris["casi"]["extent"] = [(q["raggio_mm"], q["angolo_gradi"]) for q in posizioni(f1)]
# case 2: Spacing 20 mm
path, lung = arco(2.0)
f2 = serie(seme("spacing", 2.0, "cilindro"), path, 5, 2.0, T.SpacingPatternDistanceType, False)
ris["casi"]["spacing"] = [(q["raggio_mm"], q["angolo_gradi"]) for q in posizioni(f2)]
# case 3: orientation (identical and along the path), 3 copies at 0, 90, 180°
for nome, z, lungo in (("identico", 4.0, False), ("lungo_percorso", 6.0, True)):
    path, lung = arco(z)
    f = serie(seme(nome, z, "blocco"), path, 3, lung, T.ExtentPatternDistanceType, lungo)
    ris["casi"]["orientamento_" + nome] = [(q["angolo_gradi"], q["ingombro_xy_mm"]) for q in posizioni(f)]
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
vp = app.activeViewport; vp.fit(); vp.saveAsImageFile(IMG, 1000, 700)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("serie_percorso.png")   # check image, in the folder you run from
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Rings from the ISO 8653 size

Source: ISO 8653:2016 §2.1 (public preview on iso.org, read): «ring-size: circumference of the bigger cylinder that could be
inserted in the ring» → usable inner diameter d = size / π (size in mm of circumference).
Cases (size 52 → d = 16.5521 mm): (A) flat band 4 × 2 mm; (B) «comfort fit» band (domed inside, 0.4 mm rise): the largest
cylinder that fits touches the NARROWEST point, so the minimum inner radius = d/2 (not the radius at the edge).
Measurement in Fusion: minimum distance between the Z axis and the body (= radius of the largest cylinder that fits), circumference = 2π·r.
Optional argument: the size (default 52). Measured: usable diameter 16.5521 for both rings (= expected), size
derived 52.000; 0 errors. Rings are always made from the `misura_ISO` parameter; sizes of other countries (Italian, US, UK) only with
a table from a source that has been read.

```python
"""Rings from the ISO 8653 size.
Source: ISO 8653:2016 §2.1 (public preview on iso.org, read): «ring-size: circumference of the bigger cylinder that could be
inserted in the ring» → usable inner diameter d = size / π (size in mm of circumference).
Cases (size 52 → d = 16.5521 mm): (A) flat band 4 × 2 mm; (B) «comfort fit» band (domed inside, 0.4 mm rise): the largest
cylinder that fits touches the NARROWEST point, so the minimum inner radius = d/2 (not the radius at the edge).
Measurement in Fusion: minimum distance between the Z axis and the body (= radius of the largest cylinder that fits), circumference = 2π·r.
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("anello ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VI = adsk.core.ValueInput.createByString
d.userParameters.add("misura_ISO", VI(str(MISURA)), "", "ISO 8653: inner circumference in mm")
d.userParameters.add("d_int", VI("misura_ISO * 1 mm / PI"), "mm", "diameter of the largest cylinder that fits")
ri = d.userParameters.itemByName("d_int").value / 2                       # cm
w, t, e = 0.4, 0.2, 0.04                                                  # width 4, thickness 2, rise 0.4 (mm → cm)
ris = {"d_int_mm": round(ri * 20, 4), "casi": {}}
def anello(nome, z0, bombato):
    sk = r.sketches.add(r.xZConstructionPlane); L = sk.sketchCurves.sketchLines; S = lambda x, z: sk.modelToSketchSpace(P(x, 0, z))
    ro = ri + t
    if bombato:   # inside: arc from the edge (ri + e) to the centre (ri), straight outside
        a = S(ri + e, z0 - w / 2); b = S(ri + e, z0 + w / 2)
        sk.sketchCurves.sketchArcs.addByThreePoints(a, S(ri, z0), b)
        L.addByTwoPoints(b, S(ro, z0 + w / 2)); L.addByTwoPoints(S(ro, z0 + w / 2), S(ro, z0 - w / 2)); L.addByTwoPoints(S(ro, z0 - w / 2), a)
    else:
        L.addTwoPointRectangle(S(ri, z0 - w / 2), S(ro, z0 + w / 2))
    ri_ = F.revolveFeatures.createInput(sk.profiles.item(0), r.zConstructionAxis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ri_.setAngleExtent(False, VI("360 deg"))
    b = F.revolveFeatures.add(ri_).bodies.item(0); b.name = nome
    rmin = app.measureManager.measureMinimumDistance(r.zConstructionAxis, b).value
    ris["casi"][nome] = {"raggio_minimo_mm": round(rmin * 10, 4), "diametro_utile_mm": round(rmin * 20, 4),
                         "misura_ISO_ricavata": round(2 * math.pi * rmin * 10, 3), "volume_mm3": round(b.volume * 1000, 2)}
anello("anello piatto", 0.0, False)
anello("anello comodo", 1.0, True)
t_ = d.timeline
ris["errori"] = [t_.item(k).name for k in range(t_.count) if t_.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
vp = app.activeViewport; vp.fit(); vp.saveAsImageFile(IMG, 900, 600)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    misura = float(sys.argv[1]) if len(sys.argv) > 1 else 52
    atteso = {"misura_ISO": misura, "d_int_mm": round(misura / math.pi, 4)}
    img = os.path.abspath("anelli.png")   # check image, in the folder you run from
    ok, r, righe = esegui(Sessione(), f"MISURA = {misura!r}\nIMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps({"atteso": atteso, "misurato": r if r else righe}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
```

