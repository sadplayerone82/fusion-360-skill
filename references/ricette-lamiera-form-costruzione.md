# Lamiera, forme T-spline, origini di giunto, aspetti, scena; costruzione, superfici, schizzo

**Indice** (file lungo: cerca la sezione, non leggerlo intero)
| Riga | Ricetta | Quando |
|---|---|---|
| 16 | Lamiera (regola, flangia, sviluppo), forma T-spline, origine di giunto, colore di un componente, scena | pezzi in lamiera, forme libere, giunti, aspetto |
| 174 | 13 comandi: costruzione, superfici (unione, estensione), schizzo (offset, raccordo, specchio), SVG, tubo, scala, sposta, divisione di faccia, interferenza, sviluppa e ripiega | quando serve uno di questi comandi |

Ricette provate su Fusion (nov. 2026), ognuna con le misure attese calcolate prima e ritrovate nel modello. Ogni blocco è uno script
completo da lanciare con Python sul PC: parla con Fusion attraverso `scripts/mcp_fusion.py` (la riga `sys.path.insert` punta alla
cartella `scripts/` della skill installata in `~/.claude/skills/fusion-360`: cambiala se l'hai messa altrove) e manda a Fusion il
codice delle stringhe in maiuscolo (`CODICE`, `CODICI`…). In un modello vero copia la parte che serve negli script dei passi (`scripts/progetto_locale.py`).
Qui: sviluppo della lamiera = formula della piega; 13 comandi tutti uguali agli attesi (piani, assi e punti di costruzione, tubo, scala,
sposta, divisione di faccia, interferenza, unione ed estensione di superfici, sviluppa e ripiega, SVG a 96 dpi).

## Lamiera, forma T-spline, origine di giunto, colore di un componente, scena (progetto nuovo non salvato)

A lamiera: regola attiva, flangia di base 100 × 60 da profilo, flangia su un bordo (20 mm), sviluppo piano; atteso: lunghezza dello
   sviluppo = gambe interne + tratto neutro della piega, BA = π/2 · (R + K·T) (90°), con R, K, T letti dalla regola.
B form: corpo T-spline da primitiva (box) dentro una FormFeature (startEdit/finishEdit), corpo B-rep risultante.
C origine di giunto al centro della faccia superiore di un blocco 40 × 30 × 10: atteso (0, 0, 10) mm.
D colore di un componente: aspetto dalla libreria assegnato all'occorrenza, riletto.
E scena (Render): sfondo d'ambiente e pavimento impostati e riletti; nessun rendering in questa prova (il render locale è gratuito: tavole-e-render.md).
Si lancia un passo alla volta: `nuovo`, poi `lamiera`, `form`, `giunto`, `colore`, `scena`. Misurato: lamiera — base 15 000 mm³ =
atteso, sviluppo 80,655 mm = 65 + 20 − 2(R + T) + π/2·(R + K·T) con la regola «Acciaio (mm)» (T 2,5, R 2,5, K 0,44); forma — solido di
18 896,7 mm³ (la T-spline arrotonda gli spigoli del box da 24 000); origine di giunto (0; 0; 10) = atteso; aspetto «Acrilico (rosso)»
riletto ed ereditato dal corpo; scena — 14 ambienti, ambiente, pavimento e riflessi impostati e riletti. Trappole: il componente di
lamiera si crea con `addNewSheetMetalComponent` e va **attivato** (`occ.activate()`), altrimenti la flangia finisce nel componente
principale; la raccolta delle regole si chiama `designSheetMetalRules` e in un progetto senza lamiera dà «smDataRoot»; forme T-spline
da schizzo, bridge e riparazione non hanno API.

```python
"""Lamiera, forma T-spline, origine di giunto, colore, scena via API, in un progetto nuovo NON salvato.
A lamiera: regola attiva, flangia di base 100 × 60 da profilo, flangia su un bordo (20 mm), sviluppo piano; atteso: lunghezza dello
   sviluppo = gambe interne + tratto neutro della piega, BA = π/2 · (R + K·T) (90°), con R, K, T letti dalla regola.
B form: corpo T-spline da primitiva (box) dentro una FormFeature (startEdit/finishEdit), corpo B-rep risultante.
C origine di giunto al centro della faccia superiore di un blocco 40 × 30 × 10: atteso (0, 0, 10) mm.
D colore di un componente: aspetto dalla libreria assegnato all'occorrenza, riletto.
E scena (Render): sfondo d'ambiente e pavimento impostati e riletti; nessun rendering in questa prova (il render locale è gratuito: tavole-e-render.md).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
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
    occ = r.occurrences.addNewSheetMetalComponent(adsk.core.Matrix3D.create()); c = occ.component; c.name = "lamiera"   # componente normale: nessuna regola (04/11)
    occ.activate()      # senza, la flangia finisce nel componente principale (04/11)
    # d.designSheetMetalRules (il nome vero, non sheetMetalRules) in un progetto senza lamiera dà «smDataRoot» (04/11): si usa la
    # regola attiva del componente
    reg = c.activeSheetMetalRule
    val = lambda x: x.value if hasattr(x, "value") else x            # alcuni sono parametri, kFactor è un numero (04/11)
    T, R, K = val(reg.thickness), val(reg.bendRadius), val(reg.kFactor)
    ris["regola"] = {"nome": reg.name, "T_mm": round(T * 10, 4), "R_espr": getattr(reg.bendRadius, "expression", None), "R_mm": round(R * 10, 4), "K": round(K, 4)}
    sk = c.sketches.add(c.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(10, 6, 0))
    fi = c.features.flangeFeatures.createBaseFlangeInput([sk.profiles.item(0)])
    ff = c.features.flangeFeatures.add(fi); b = c.bRepBodies.item(0)
    ris["base"] = {"lamiera": b.isSheetMetal, "volume_mm3": round(b.volume * 1000, 2), "atteso_mm3": round(100 * 60 * T * 10, 2)}
    # bordo lungo 100 mm sul lato y = 0, faccia superiore
    top = max([b.faces.item(k) for k in range(b.faces.count)], key=lambda f_: f_.pointOnFace.z)
    ed = [top.edges.item(k) for k in range(top.edges.count) if abs(top.edges.item(k).length - 10) < 1e-6 and abs(top.edges.item(k).pointOnEdge.y) < 1e-6][0]
    ei = c.features.flangeFeatures.createEdgeFlangeInput([ed], VI("20 mm"))
    c.features.flangeFeatures.add(ei)
    b = c.bRepBodies.item(0); bb = b.boundingBox
    ris["piegato"] = {"ingombro_mm": [round((bb.maxPoint.x - bb.minPoint.x) * 10, 3), round((bb.maxPoint.y - bb.minPoint.y) * 10, 3), round((bb.maxPoint.z - bb.minPoint.z) * 10, 3)],
                      "volume_mm3": round(b.volume * 1000, 2)}
    # sviluppo: faccia fissa = la faccia piana più grande del pezzo
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
    ris["nota"] = "box 40 x 30 x 20 = 24000 mm3: la T-spline arrotonda gli spigoli, il volume deve essere minore"
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
    lib = [app.materialLibraries.item(k) for k in range(app.materialLibraries.count) if any(w in app.materialLibraries.item(k).name.lower() for w in ("appearance", "aspetti"))]   # nomi tradotti (04/11)
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
    prima = {"sfondo": str(ss.backgroundType), "ambiente": ss.backgroundEnvironment.name if ss.backgroundType == adsk.fusion.RenderSceneBackgroundTypes.EnvironmentRenderSceneBackgroundType else "(sfondo non d'ambiente: non leggibile)", "pavimento": ss.isGroundDisplayed}
    e = envs.item(envs.count - 1)
    ss.backgroundEnvironment = e      # backgroundType è di sola lettura: lo cambia l'assegnazione dell'ambiente (04/11)
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

## 13 comandi: costruzione, superfici, schizzo, SVG, lamiera (progetto nuovo non salvato)

Ogni voce ha l'atteso calcolato prima; esito ok se |misurato − atteso| ≤ 0,01 (mm, mm², mm³) salvo dove indicato.
 1 ellisse a 20, b 10 → area π·20·10 = 628,319 mm²          2 offset schizzo di un rettangolo 40 × 20 di 5 mm → perimetro 160 (spigoli
 3 raccordo di schizzo R 5 fra due rette a 90° → arco 7,854     vivi) o 151,416 (raccordati): si registra quale
 4 specchio di un cerchio (10, 0) sull'asse Y → (−10, 0)        5 SVG 50 × 30 mm (width/height in mm) importato → ingombro registrato
 6 tubo Ø 10 su retta 100 → 7 853,982 mm³                       7 scala ×2 di un cubo 10 → 8 000 mm³
 8 sposta di (30, 0, 0) → x minimo +30                          9 divisione della faccia superiore con un piano → facce +1
10 costruzione: piano offset 15 → z 15; piano medio fra z 0 e z 10 → z 5; punto al centro di un cerchio (20, 20); punto da 3 piani;
   asse dal cilindro del tubo (voce 6) → direzione X
11 interferenza fra due cubi 10 sovrapposti di 5 → 500 mm³    12 superfici: toppa 20 × 10 + parete 20 × 10 con un bordo in comune, unione → 1 corpo, 400 mm²;
   estensione di 5 di un bordo di una toppa 20 × 10 → 300 mm²
13 lamiera: sviluppo di una piega (Unfold) e ripiegatura (Refold) → stesso volume e stesso ingombro di partenza

Esito: tutte le voci uguali all'atteso; da leggere: 2 offset → 160 (spigoli vivi, non raccordati); 5 SVG da 50 × 30 mm → 13,229 ×
7,937, cioè Fusion legge le unità come pixel a 96 dpi (scala 96/25,4 per avere mm); 12a unione → 1 corpo di 2 facce, superficie (non
solido); 13 lamiera → sviluppato alto 2,5 e largo 80,655, ma dopo «Ripiega» il pezzo può risultare ruotato (alto 65 invece di 20):
ricontrolla l'ingombro. Copiare le facce di un solido con offset 0 dà un SOLIDO, e l'unione lo rifiuta: servono superfici vere.

```python
"""Prova di 13 comandi utili (costruzione, superfici, schizzo, SVG, lamiera), in un progetto nuovo non salvato.
Ogni voce ha l'atteso calcolato prima; esito ok se |misurato − atteso| ≤ 0,01 (mm, mm², mm³) salvo dove indicato.
 1 ellisse a 20, b 10 → area π·20·10 = 628,319 mm²          2 offset schizzo di un rettangolo 40 × 20 di 5 mm → perimetro 160 (spigoli
 3 raccordo di schizzo R 5 fra due rette a 90° → arco 7,854     vivi) o 151,416 (raccordati): si registra quale
 4 specchio di un cerchio (10, 0) sull'asse Y → (−10, 0)        5 SVG 50 × 30 mm (width/height in mm) importato → ingombro registrato
 6 tubo Ø 10 su retta 100 → 7 853,982 mm³                       7 scala ×2 di un cubo 10 → 8 000 mm³
 8 sposta di (30, 0, 0) → x minimo +30                          9 divisione della faccia superiore con un piano → facce +1
10 costruzione: piano offset 15 → z 15; piano medio fra z 0 e z 10 → z 5; punto al centro di un cerchio (20, 20); punto da 3 piani;
   asse dal cilindro del tubo (voce 6) → direzione X
11 interferenza fra due cubi 10 sovrapposti di 5 → 500 mm³    12 superfici: toppa 20 × 10 + parete 20 × 10 con un bordo in comune, unione → 1 corpo, 400 mm²;
   estensione di 5 di un bordo di una toppa 20 × 10 → 300 mm²
13 lamiera: sviluppo di una piega (Unfold) e ripiegatura (Refold) → stesso volume e stesso ingombro di partenza
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
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
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.yZConstructionPlane, adsk.core.ValueInput.createByReal(20.5)); pl = r.constructionPlanes.add(pi)   # il cubo è a x 20–21 cm (04/11)
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
    v = r.constructionAxes.add(ai).geometry.direction; esito("10e_asse_cilindro_dir", [round(abs(v.x), 4), round(abs(v.y), 4), round(abs(v.z), 4)], [1.0, 0.0, 0.0])   # il tubo (prova 6) corre lungo X
def p11():
    a = cubo(70, 0, 0, 1.0, "int A"); b = cubo(70.5, 0, 0, 1.0, "int B")
    oc = adsk.core.ObjectCollection.create(); oc.add(a); oc.add(b)
    res = d.analyzeInterference(d.createInterferenceInput(oc))
    esito("11_interferenza_mm3", mm3(sum(res.item(k).interferenceBody.volume for k in range(res.count))), 500.0)
def p12():
    # unione: pavimento (toppa 20 × 10) + parete (estrusione di superficie 20 × 10) con un bordo in comune → 1 corpo, 2 facce, 400 mm²
    # (04/11: copiare le facce di un solido con offset 0, anche una per volta, dà un SOLIDO e l'unione lo rifiuta)
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
    ui = c.features.unfoldFeatures.createInput(fissa); ui.isUnfoldAllBends = True        # senza: «at least one bend face» (04/11)
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
    solo = sys.argv[1:]          # es. 6 9 10 12 13: rilancia solo quelle voci (la 10e usa il tubo della 6)
    ok, r, righe = esegui(Sessione(), f"SVG = {svg!r}\nSOLO = {solo!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r if r else righe, ensure_ascii=False, indent=1))
    if r and not solo: json.dump(r, open(QUI + "/comandi_provati.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
```

