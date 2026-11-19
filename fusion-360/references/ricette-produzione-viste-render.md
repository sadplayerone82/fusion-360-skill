# Recipes: export, analysis, verification, views, render, drawings

> Recipes tested on Fusion (Nov. 2026), each with the measured result.

**How to use them**: each recipe shows the API call that **works** (tested, with the measured result). The tests use shortcuts (`rett`, `blocco`: rectangles **without constraints**, dimensions as numbers): in a real model sketches are fully constrained and dimensions are parameters (`ricette.md` §2–§3, `metodo.md`). API coordinates are in **cm**.

Header: the same simplified one as `ricette-solidi.md` (`d`, `r`, `F`, `P`, `S`, `OP`, `rett`, `blocco`, `vol`, `out`, `math`),
plus `CARTELLA = os.path.join(os.path.expanduser("~"), "prove-fusion")` (where to write files: choose your own); for a real model
the one in `ricette.md` §1 applies. In the MISURE recipe `blocco` is redefined with other arguments.

Index: Export and analysis · Measurements, interferences, defects (verification) · Views · Render and animation · 2D drawing (opening an existing drawing, reading it, exporting the PDF)

## Export and analysis

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
    print("file", nome, os.path.getsize(f) if os.path.exists(f) else 0, "| deviation set cm", round(o.surfaceDeviation, 6), "| normal rad", round(o.normalDeviation, 4))
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

Recorded results: `{"I2_step": {"solidi_MANIFOLD_SOLID_BREP": 2, "unita_millimetri": true, "schema": "AUTOMOTIVE_DESIGN { 1 0 10303 214 3 1 1 }"}, "I2_3mf": {"file_model": 1, "oggetti": 2, "elementi_build": 2, "unita": "millimeter"}}`; mesh: 6 quality settings → identical files (404 triangles), options ignored.

## Measurements, interferences, defects (verification)

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
prof = max(sk.profiles, key=lambda p: p.profileLoops.count)   # the profile with the hole (2 loops)
e = r.features.extrudeFeatures.addSimple(prof, S("spessore"), OP.NewBodyFeatureOperation); e.name = "EST_blocco"
e.bodies.item(0).name = "Blocco"
print("constrained", sk.isFullyConstrained)
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
print("minimum_distance_mm", round(res.value * 10, 6))
fa, fb = a.endFaces.item(0), a.sideFaces.item(0)
ang = mm_.measureAngle(fa, fb)
print("angle_degrees", round(math.degrees(ang.value), 6))
c = blocco(4, 6, "I1")   # overlapping M2 by 0.5 cm in X: M2 goes from 2.5 to 4.5, I1 from 4 to 6
coll = adsk.core.ObjectCollection.create()
coll.add(r.bRepBodies.itemByName("M2")); coll.add(r.bRepBodies.itemByName("I1"))
ii = d.createInterferenceInput(coll)
ris = d.analyzeInterference(ii)
print("interferences", ris.count, [round(x.interferenceBody.volume * 1000, 4) for x in ris])
```

## Views

### named views and home view
Named view: `d.namedViews.add(vp.camera, "VISTA_iso")`; home view: `vp.camera` → `setCurrentAsHome` / `goHome`; `vp.fit()` also works in read-only mode.
```python
vp = app.activeViewport
def occhio(c): return [round(x*10, 3) for x in c.eye.asArray()]
```

## Render and animation

### ASPETTO_SCENA
```python
e = blocco(-20, -10, 20, 10, 10); b = e.bodies.item(0)
libs = [l for l in app.materialLibraries if l.appearances.count > 0]
lib = max(libs, key=lambda l: l.appearances.count)
# by CODE (names are localized): «ABS (bianco)» = ABS (white)
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
# 360° turn in 4 frames around the Z axis through the centre of the part
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
# without the Animation workspace active storyboards gives «InternalValidationError : assetRoot»; add() does not accept a name
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

Recorded results (names as shown by the Italian UI): appearance: `{"libreria": "Libreria dei materiali di Fusion", "aspetti": 326, "scelto": "ABS (bianco)", "id": "PrismMaterial-022_physmat_aspects:Prism-374", "applicato": "ABS (bianco)", "sfondo": 1, "terreno": true, "luminosita": 1000.0, "telecamera": 0}`; local renders: the render and the frames of the turn written at 800 × 600.

## 2D drawing (opening an existing drawing, reading it, exporting the PDF)

### LEGGI
The drawing is opened **visible**: hidden it hangs Fusion. Complete script, with its own `run`: send it as it is with the
`fusion_mcp_execute` tool or with `esegui(s, codice, intero=True)` from `mcp_fusion.py`, not with `esegui_file.py` (which adds
the header). Recorded result: 1 sheet, 3 views, 3 dimensions, PDF A3
420.2 × 297.0.
```python
import adsk.core, adsk.drawing, json, os
ID_TAVOLA = "<id of the drawing in the cloud>"                  # dataFile.id of the drawing: replace it
PDF = os.path.join(os.path.expanduser("~"), "tavola.pdf")      # where to export the PDF
def run(_context: str):
    app = adsk.core.Application.get()
    df = app.data.findFileById(ID_TAVOLA)
    doc = app.documents.open(df, True)  # hidden: Fusion hangs
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
