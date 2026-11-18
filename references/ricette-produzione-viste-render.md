# Ricette: esportazione, analisi, verifica, viste, render, tavole

> Ricette provate su Fusion (nov. 2026), ognuna con il risultato misurato.

**Come usarle**: ogni ricetta mostra la chiamata all'API che **funziona** (provata, col risultato misurato). Le prove usano scorciatoie (`rett`, `blocco`: rettangoli **senza vincoli**, misure a numero): in un modello vero gli schizzi si vincolano completamente e le misure sono parametri (`ricette.md` §2–§3, `metodo.md`). Le coordinate dell'API sono in **cm**.

Intestazione: la stessa, semplificata, di `ricette-solidi.md` (`d`, `r`, `F`, `P`, `S`, `OP`, `rett`, `blocco`, `vol`, `out`, `math`),
più `CARTELLA = os.path.join(os.path.expanduser("~"), "prove-fusion")` (dove scrivere i file: scegline una tua); per un modello vero
vale quella di `ricette.md` §1. Nella ricetta MISURE `blocco` è ridefinita con altri argomenti.

Indice: Esportazione e analisi · Misure, interferenze, difetti (verifica) · Viste · Render e animazione · Tavola 2D (aprire una tavola esistente, leggerla, esportare il PDF)

## Esportazione e analisi

### ESPORTA_STL
```python
import os
os.makedirs(CARTELLA, exist_ok=True)
sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 1)
b = F.extrudeFeatures.addSimple(sk.profiles.item(0), S("10 mm"), OP.NewBodyFeatureOperation).bodies.item(0)
em = d.exportManager; MR = adsk.fusion.MeshRefinementSettings
for nome, imp in (("basso", MR.MeshRefinementLow), ("medio", MR.MeshRefinementMedium), ("alto", MR.MeshRefinementHigh), ("dev001", 0.001), ("dev05", 0.05), ("dev0005", 0.0005)):
    f = os.path.join(CARTELLA, f"cil_{nome}.stl")
    o = em.createSTLExportOptions(b, f)
    if isinstance(imp, float):
        o.meshRefinement = MR.MeshRefinementCustom; o.surfaceDeviation = imp
    else:
        o.meshRefinement = imp
    em.execute(o)
    print("file", nome, os.path.getsize(f) if os.path.exists(f) else 0, "| deviazione impostata cm", round(o.surfaceDeviation, 6), "| normale rad", round(o.normalDeviation, 4))
```

### ESPORTA_STEP_3MF
```python
import os
os.makedirs(CARTELLA, exist_ok=True)
e = blocco(0, 0, 20, 20, 10)
hi = F.holeFeatures.createSimpleInput(S("6 mm")); hi.setPositionByPoint(e.endFaces.item(0), P(1, 1, 1)); hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection); F.holeFeatures.add(hi)
blocco(30, 0, 40, 10, 5)
em = d.exportManager
f1 = os.path.join(CARTELLA, "pezzi.step"); em.execute(em.createSTEPExportOptions(f1, r))
f2 = os.path.join(CARTELLA, "pezzi.3mf"); o = em.createC3MFExportOptions(r, f2); em.execute(o)
print("ok", os.path.getsize(f1), os.path.getsize(f2))
```

### ANALISI
```python
e = blocco(0, 0, 40, 20, 10); b = e.bodies.item(0)
def spigoli_verticali(xmin, xmax):
    c = adsk.core.ObjectCollection.create()
    for ed in b.edges:
        g = ed.geometry
        if isinstance(g, adsk.core.Line3D) and abs(g.startPoint.z - g.endPoint.z) > 0.5 and xmin <= g.startPoint.x <= xmax: c.add(ed)
    return c
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(spigoli_verticali(-0.1, 0.1), S("2 mm"), True); F.filletFeatures.add(fi)
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(spigoli_verticali(3.9, 4.1), S("3 mm"), True); F.filletFeatures.add(fi)
A = d.analyses
mr = A.minimumRadiusAnalyses.add(A.minimumRadiusAnalyses.createInput([b]))
ris = {"raggio_minimo_mm": round(mr.minimumRadius * 10, 4)}
try:
    da = A.draftAnalyses.add(A.draftAnalyses.createInput([b], r.zConstructionAxis)); ris["sformo"] = da.objectType.split("::")[-1]
except Exception as ex: ris["sformo_errore"] = str(ex)[-150:]
try:
    sa = A.sectionAnalyses.add(A.sectionAnalyses.createInput(r.xZConstructionPlane, -1.0)); ris["sezione"] = sa.objectType.split("::")[-1]
except Exception as ex: ris["sezione_errore"] = str(ex)[-150:]
try:
    aa = A.accessibilityAnalyses.add(A.accessibilityAnalyses.createInput([b], r.zConstructionAxis)); ris["accessibilita"] = aa.objectType.split("::")[-1]
except Exception as ex: ris["accessibilita_errore"] = str(ex)[-150:]
ris["analisi_totali"] = A.count
out(**ris)
```

Risultati registrati: `{"I2_step": {"solidi_MANIFOLD_SOLID_BREP": 2, "unita_millimetri": true, "schema": "AUTOMOTIVE_DESIGN { 1 0 10303 214 3 1 1 }"}, "I2_3mf": {"file_model": 1, "oggetti": 2, "elementi_build": 2, "unita": "millimeter"}}`; mesh: 6 impostazioni di qualità → file identici (404 triangoli), opzioni ignorate.

## Misure, interferenze, difetti (verifica)

### SANO
```python
d.userParameters.add("lunghezza", S("40 mm"), "mm", "")
d.userParameters.add("larghezza", S("20 mm"), "mm", "")
d.userParameters.add("spessore", S("10 mm"), "mm", "")
d.userParameters.add("diametro_foro", S("8 mm"), "mm", "")
sk = r.sketches.add(r.xYConstructionPlane); sk.name = "SK_base"
l = sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(4, 2, 0))
g = sk.geometricConstraints
g.addCoincident(l[0].startSketchPoint, sk.originPoint)
g.addHorizontal(l[0]); g.addVertical(l[1]); g.addHorizontal(l[2]); g.addVertical(l[3])
dm = sk.sketchDimensions
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, P(2, -0.5, 0)).parameter.expression = "lunghezza"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, P(4.5, 1, 0)).parameter.expression = "larghezza"
c = sk.sketchCurves.sketchCircles.addByCenterRadius(P(2, 1, 0), 0.4)
dm.addDiameterDimension(c, P(2.6, 1.6, 0)).parameter.expression = "diametro_foro"
dm.addDistanceDimension(sk.originPoint, c.centerSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, P(1, -1, 0)).parameter.expression = "lunghezza / 2"
dm.addDistanceDimension(sk.originPoint, c.centerSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, P(-1, 0.5, 0)).parameter.expression = "larghezza / 2"
prof = max(sk.profiles, key=lambda p: p.profileLoops.count)   # il profilo con il foro (2 anelli)
e = r.features.extrudeFeatures.addSimple(prof, S("spessore"), OP.NewBodyFeatureOperation); e.name = "EST_blocco"
e.bodies.item(0).name = "Blocco"
print("vincolato", sk.isFullyConstrained)
```

### MISURE
```python
def blocco(x0, x1, nome):
    sk = r.sketches.add(r.xYConstructionPlane)
    sk.sketchCurves.sketchLines.addTwoPointRectangle(P(x0, 10, 0), P(x1, 12, 0))
    e = r.features.extrudeFeatures.addSimple(sk.profiles.item(0), S("10 mm"), OP.NewBodyFeatureOperation)
    e.bodies.item(0).name = nome
    return e
a = blocco(0, 2, "M1"); b = blocco(2.5, 4.5, "M2")
mm_ = app.measureManager
res = mm_.measureMinimumDistance(a.bodies.item(0), b.bodies.item(0))
print("distanza_minima_mm", round(res.value * 10, 6))
fa, fb = a.endFaces.item(0), a.sideFaces.item(0)
ang = mm_.measureAngle(fa, fb)
print("angolo_gradi", round(math.degrees(ang.value), 6))
c = blocco(4, 6, "I1")   # sovrapposto a M2 per 0.5 cm in X: M2 va da 2.5 a 4.5, I1 da 4 a 6
coll = adsk.core.ObjectCollection.create()
coll.add(r.bRepBodies.itemByName("M2")); coll.add(r.bRepBodies.itemByName("I1"))
ii = d.createInterferenceInput(coll)
ris = d.analyzeInterference(ii)
print("interferenze", ris.count, [round(x.interferenceBody.volume * 1000, 4) for x in ris])
```

## Viste

### viste con nome e vista iniziale
Vista con nome: `d.namedViews.add(vp.camera, "VISTA_iso")`; vista iniziale: `vp.camera` → `setCurrentAsHome` / `goHome`; `vp.fit()` funziona anche in sola lettura.
```python
vp = app.activeViewport
def occhio(c): return [round(x*10, 3) for x in c.eye.asArray()]
```

## Render e animazione

### ASPETTO_SCENA
```python
e = blocco(-20, -10, 20, 10, 10); b = e.bodies.item(0)
libs = [l for l in app.materialLibraries if l.appearances.count > 0]
lib = max(libs, key=lambda l: l.appearances.count)
# per CODICE (i nomi sono tradotti): «ABS (bianco)»
a = lib.appearances.itemById("PrismMaterial-022_physmat_aspects:Prism-374")
copia = d.appearances.addByCopy(a, a.name)
b.appearance = copia
sc = d.renderManager.sceneSettings
out(libreria=lib.name, aspetti=lib.appearances.count, scelto=a.name, id=a.id, applicato=b.appearance.name,
    sfondo=sc.backgroundType, terreno=sc.isGroundDisplayed, luminosita=sc.brightness, telecamera=sc.cameraType)
```

### RENDER
```python
import os
os.makedirs(CARTELLA, exist_ok=True)
vp = app.activeViewport; vp.fit()
rd = d.renderManager.rendering
rd.resolution = adsk.fusion.RenderResolutions.Web800x600RenderResolution
rd.renderQuality = 25
cam = vp.camera
f = rd.startLocalRender(os.path.join(CARTELLA, "K-render.png"), cam)
stati = [f.renderState]
# giro a 360° in 4 fotogrammi attorno all'asse Z passante per il centro del pezzo
bb = r.boundingBox
c = adsk.core.Point3D.create((bb.minPoint.x + bb.maxPoint.x) / 2, (bb.minPoint.y + bb.maxPoint.y) / 2, (bb.minPoint.z + bb.maxPoint.z) / 2)
occhio = cam.eye
for i in range(4):
    m = adsk.core.Matrix3D.create(); m.setToRotation(math.pi / 2 * i, adsk.core.Vector3D.create(0, 0, 1), c)
    e2 = occhio.copy(); e2.transformBy(m)
    c2 = vp.camera; c2.eye = e2; c2.target = c; c2.upVector = adsk.core.Vector3D.create(0, 0, 1)
    rd.startLocalRender(os.path.join(CARTELLA, f"K-giro-{i}.png"), c2)
out(stato_iniziale=str(stati[0]), qualita=rd.renderQuality, risoluzione=[rd.resolutionWidth, rd.resolutionHeight])
```

### STORYBOARD
```python
# senza l'ambiente Animazione attivo storyboards dà «InternalValidationError : assetRoot»; add() non accetta un nome
am = d.animationManager
ris = {"attivata": am.activateAnimationWorkspace()}
try:
    sbs = am.storyboards; ris["storyboard_prima"] = sbs.count
    sb = sbs.add()
    ris["storyboard_creata"] = sb.objectType.split("::")[-1]; ris["storyboard_dopo"] = sbs.count
except Exception as ex:
    ris["storyboard_errore"] = str(ex)[-200:]
app.userInterface.workspaces.itemById("FusionSolidEnvironment").activate()
out(**ris)
```

Risultati registrati: aspetto: `{"libreria": "Libreria dei materiali di Fusion", "aspetti": 326, "scelto": "ABS (bianco)", "id": "PrismMaterial-022_physmat_aspects:Prism-374", "applicato": "ABS (bianco)", "sfondo": 1, "terreno": true, "luminosita": 1000.0, "telecamera": 0}`; render locali: il render e i fotogrammi del giro scritti a 800 × 600.

## Tavola 2D (aprire una tavola esistente, leggerla, esportare il PDF)

### LEGGI
La tavola si apre **visibile**: nascosta blocca Fusion. Script completo, con la sua `run`: si manda così com'è con lo
strumento `fusion_mcp_execute` o con `esegui(s, codice, intero=True)` di `mcp_fusion.py`, non con `esegui_file.py` (che aggiunge
l'intestazione). Risultato registrato: 1 foglio, 3 viste, 3 quote, PDF A3
420.2 × 297.0.
```python
import adsk.core, adsk.drawing, json, os
ID_TAVOLA = "<id della tavola nel cloud>"                       # dataFile.id della tavola: sostituiscilo
PDF = os.path.join(os.path.expanduser("~"), "tavola.pdf")      # dove esportare il PDF
def run(_context: str):
    app = adsk.core.Application.get()
    df = app.data.findFileById(ID_TAVOLA)
    doc = app.documents.open(df, True)  # nascosta: Fusion si blocca
    ris = {"documento": doc.name, "tipo": doc.objectType.split("::")[-1]}
    try:
        dw = adsk.drawing.Drawing.cast(doc.products.item(0))
        fogli = []
        for sh in dw.sheets:
            v = sh.views
            fogli.append({"nome": sh.name, "viste": v.count,
                           "quote": sh.drawingDimensions.count if hasattr(sh, "drawingDimensions") else None})
        ris["fogli"] = fogli
        tb = dw.titleBlocks
        ris["cartigli"] = tb.count
        if tb.count:
            ris["campi_cartiglio"] = [a.attributeName for a in tb.item(0).getAttributes()]
        os.makedirs(os.path.dirname(PDF), exist_ok=True)
        em = dw.exportManager
        o = em.createPDFExportOptions(PDF)
        ris["pdf_execute"] = em.execute(o)
        ris["pdf_byte"] = os.path.getsize(PDF) if os.path.exists(PDF) else 0
    except Exception as ex:
        ris["errore"] = str(ex)[-300:]
    doc.close(False)
    ris["documenti_aperti_dopo"] = app.documents.count
    print("RIS" + json.dumps(ris))
```

