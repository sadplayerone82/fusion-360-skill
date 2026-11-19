# Tested recipes

Every recipe below was **tested in Fusion** with an automatic check (volume or dimensions equal to the calculation made beforehand). Copy and adapt them instead of
writing the API from memory: misremembered functions were the main cause of errors.

These are the **essential** recipes, written for a real model (constrained, parametric). Everything else that was tested,
with the exact code and the measured result, is in the `ricette-*.md` files (sketches and planes, 21 solid features, surfaces/freeform/
sheet metal, assemblies, editing/importing, manufacturing/views/render) and the screw dimensions in `dati-standard.md`.

Index: 1 header · 2 constrained centred rectangle · 3 L profile on the XZ plane · 4 extrudes · 5 fillets chosen by geometry ·
6 holes in a pattern · 7 countersunk and counterbored · 8 aligned points without over-constraint · 9 engraved text · 10 snap hook · 11 involute
gear · 12 joints · 13 materials and mass · 14 interference · 15 3MF/STEP export and .f3d save · 16 images and render

## 1. Script header
`scripts/mcp_fusion.py` wraps your code in `def run(_context: str):` with this header (function `corpo(codice)`, constant
`TESTA`), so in the examples these names already exist. It is the one used by `scripts/progetto_locale.py` and `scripts/esegui_file.py`: the
file of a step contains **only the code**, without header.
```python
import adsk.core, adsk.fusion, math, json
app = adsk.core.Application.get()
d = adsk.fusion.Design.cast(app.activeProduct)
r = d.rootComponent if d else None; F = r.features if r else None
P = adsk.core.Point3D.create; S = adsk.core.ValueInput.createByString; OP = adsk.fusion.FeatureOperations
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation; V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
def vol(b):     # mm³, high accuracy: b.volume (fast) is off by a few mm³ on intersecting curved surfaces
    return round(b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume * 1000, 4)
def out(**k): print("RIS" + json.dumps(k))            # result readable by the external script (the last out() wins)
def controlla(corpo=None, volume=None, ingombro=None, n_corpi=None, tol_v=0.0001, tol_l=0.01): ...
```
`controlla` compares **in the same call** with the expected value, in mm and mm³: `n_corpi` (bodies of the root component and of all the
occurrences), `volume` of `corpo` (relative tolerance `tol_v`, default 0.01 %), `ingombro` `[x, y, z]` of `corpo` from its
`boundingBox` (tolerance `tol_l`, default 0.01 mm). If something does not match it raises `RuntimeError("CONTROLLO FALLITO: …")` (= check failed): the script
is a transaction, so nothing of the step remains in the document. Example of the end of a step:
`controlla(e.bodies.item(0), volume=7905.309, ingombro=[40, 30, 30], n_corpi=1); out(v=vol(e.bodies.item(0)))`.
On curved bodies the API bounding box can be slightly large (see `sketch.boundingBox` in `connettore-e-api.md`): if `controlla` fails
a bounding box by a few hundredths, measure the true extremes before touching the model.

`progetto_locale.py <cartella> passo <nome> <file.py> --atteso V` runs the file, then measures by itself (total and per-body volume at high
accuracy, timeline elements in error) and compares with the expected volume (0.01 %): if it does not match or there is an element in error the
step is **not** recorded. If it matches, it saves the script in `passi/`, a line in `registro.json`, the copy `progetto.f3d` and makes a
git commit (if the folder is a repository). The other commands: `misura`, `riapri`, `rigioca`, `versione`.

The recipes in the `ricette-*.md` files sometimes use a **simplified** test header (with `vol` from `b.volume`, `rett`,
`blocco`…): for a real model the one above applies.

User parameters: `d.userParameters.add("spessore", S("4 mm"), "mm", "commento")`.

## 2. Fully constrained centred rectangle
The API creates the 4 lines **without constraints**: add them yourself. (Tested: sides 40.0 × 20.0, centre 0,0, `isFullyConstrained` true.)
```python
sk = r.sketches.add(r.xYConstructionPlane); sk.name = "SK_base"
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(2, 1, 0))
g = sk.geometricConstraints; dm = sk.sketchDimensions
g.addHorizontal(l[0]); g.addVertical(l[1]); g.addHorizontal(l[2]); g.addVertical(l[3])
dg = sk.sketchCurves.sketchLines.addByTwoPoints(l[0].startSketchPoint, l[2].startSketchPoint); dg.isConstruction = True
g.addMidPoint(sk.originPoint, dg)                      # centre on the origin
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)).parameter.expression = "base_L"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(2.5, 0, 0)).parameter.expression = "base_W"
```
The lines as construction (`x.isConstruction = True` for each) give 4 constrained points: they are used for holes in a pattern (§6).

## 3. Constrained closed profile on the XZ plane (e.g. L bracket)
On the XZ plane the sketch Y is the model −Z: give the points in model coordinates and convert them.
```python
sk = r.sketches.add(r.xZConstructionPlane); sk.name = "SK_profilo"
m = lambda x, z: sk.modelToSketchSpace(P(x / 10, 0, z / 10))     # model mm → sketch
pt = [m(0, 0), m(40, 0), m(40, 4), m(4, 4), m(4, 30), m(0, 30)]
L = sk.sketchCurves.sketchLines; li = []
for i in range(6):                                                  # reuse the points: no duplicate points
    a = li[-1].endSketchPoint if li else pt[0]
    b = li[0].startSketchPoint if i == 5 else pt[i + 1]
    li.append(L.addByTwoPoints(a, b))
g = sk.geometricConstraints; dm = sk.sketchDimensions
g.addCoincident(li[0].startSketchPoint, sk.originPoint)
for i in (0, 2, 4): g.addHorizontal(li[i])
for i in (1, 3, 5): g.addVertical(li[i])
for linea, ori, nome in ((li[0], H, "lunghezza_base"), (li[1], V, "spessore_base"), (li[4], H, "spessore_parete"), (li[5], V, "altezza")):
    c = linea.startSketchPoint.geometry
    dm.addDistanceDimension(linea.startSketchPoint, linea.endSketchPoint, ori, P(c.x + 0.3, c.y + 0.3, 0)).parameter.expression = nome
```
Degrees of freedom: 12 (6 points) − 2 origin − 6 horizontal/vertical − 4 dimensions = 0.

## 4. Extrudes
```python
e = F.extrudeFeatures.addSimple(prof, S("base_H"), OP.NewBodyFeatureOperation); e.name = "EST_base"; e.bodies.item(0).name = "Pezzo"
ei = F.extrudeFeatures.createInput(prof, OP.NewBodyFeatureOperation); ei.setSymmetricExtent(S("larghezza"), True)   # symmetric, total
ci = F.extrudeFeatures.createInput(prof, OP.CutFeatureOperation); ci.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
ci = F.extrudeFeatures.createInput(prof, OP.CutFeatureOperation); ci.setDistanceExtent(False, S("incavo_H"))
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("base_H")); piano = r.constructionPlanes.add(pi)
```
Profile: choose it by area (`min(sk.profiles, key=lambda p: abs(p.areaProperties().area - atteso_cm2))`), not by index. Taper and
draft with a **positive** angle **widen** the part. Centred circle: centre coincident with `sk.originPoint` + diameter dimension.

## 5. Fillets on edges chosen by geometry
```python
b = r.bRepBodies.itemByName("Pezzo")
sp = [s for s in b.edges if all(abs(v.geometry.x - 0.4) < 1e-6 and abs(v.geometry.z - 0.4) < 1e-6 for v in (s.startVertex, s.endVertex))]
col = adsk.core.ObjectCollection.create(); [col.add(s) for s in sp]
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(col, S("raggio"), True); F.filletFeatures.add(fi).name = "RAC_interno"
```
Vertical edges: `isinstance(ed.geometry, adsk.core.Line3D) and abs(g.startPoint.z - g.endPoint.z) > 1e-3`. Search **after** the last feature.

## 6. Identical holes in a pattern (a single command)
Never 4 holes on the same face in a loop: after the first one the face no longer exists. Centres as points of a constrained sketch:
```python
sk = r.sketches.add(piano_sopra); sk.name = "SK_fori"
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(5, 3, 0))
for x in l: x.isConstruction = True
# ... constraints and dimensions as in §2 with "fori_X" and "fori_Y"
punti = adsk.core.ObjectCollection.create()
for x in l: punti.add(x.startSketchPoint)
hi = F.holeFeatures.createCounterboreInput(S("foro_D"), S("lamatura_D"), S("lamatura_H"))   # or createSimpleInput(S("foro_D"))
hi.setPositionBySketchPoints(punti)
hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
F.holeFeatures.add(hi).name = "FORI_fissaggio"
```
Tested on a 15 mm base: volume = calculation; careful if the counterbore goes past the edge (the expected calculation must account for it).

## 7. Countersunk and counterbored holes (flat or socket head screws)
```python
hi = F.holeFeatures.createCountersinkInput(S("3.4 mm"), S("6.5 mm"), S("90 deg"))     # M3 countersunk
hi = F.holeFeatures.createCounterboreInput(S("3.4 mm"), S("6.5 mm"), S("3.2 mm"))     # M3 counterbored
hi.setPositionByPoint(faccia, P(x, y, z_faccia)); hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
```
The values above are those of the test (check passed). For a real screw take the dimensions from the standard in
`dati-standard.md`: e.g. M3 flat head ISO 10642 → countersink **Ø7.5**; M3 socket head ISO 4762 → counterbore **Ø6.5 × 3.4**.

## 8. Aligned points without a wrongful «over-constraint»
A 2nd horizontal dimension from the origin to a point vertically aligned with one already dimensioned is refused. Tie the second to the first:
```python
c1 = sk.sketchCurves.sketchCircles.addByCenterRadius(P(2.8, 0.8, 0), 0.17)
c2 = sk.sketchCurves.sketchCircles.addByCenterRadius(P(2.8, -0.8, 0), 0.17)
lc = sk.sketchCurves.sketchLines.addByTwoPoints(c1.centerSketchPoint, c2.centerSketchPoint); lc.isConstruction = True
sk.geometricConstraints.addVertical(lc)
dm.addDiameterDimension(c1, P(3.3, 1.3, 0)).parameter.expression = "foro_D"; dm.addDiameterDimension(c2, P(3.3, -1.3, 0)).parameter.expression = "foro_D"
dm.addDistanceDimension(sk.originPoint, c1.centerSketchPoint, H, P(1.4, 1.4, 0)).parameter.expression = "lunghezza - distanza_foro"
dm.addDistanceDimension(sk.originPoint, c1.centerSketchPoint, V, P(3.5, 0.4, 0)).parameter.expression = "interasse / 2"
dm.addDistanceDimension(c1.centerSketchPoint, c2.centerSketchPoint, V, P(3.8, 0, 0)).parameter.expression = "interasse"
```
To centre a figure on an axis use an «L / 2» dimension from the origin: a centreline with a free end leaves one degree of freedom.

## 9. Engraved or embossed text
```python
ti = sk.sketchTexts.createInput2("TESTO", 0.6)            # height 6 mm
ti.setAsMultiLine(P(0.5, 0.4, 0), P(5.5, 1.6, 0), adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                  adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
t = sk.sketchTexts.add(ti)
ci = F.extrudeFeatures.createInput(t, OP.CutFeatureOperation); ci.setDistanceExtent(False, S("-1 mm")); F.extrudeFeatures.add(ci)
```
The text itself is the profile. Minimum height and depth for production: from the 3D printing skill, if installed (setting
`skill_stampa`), or from the chosen process. Text on curved faces: `ricette-decori-anelli.md`.

## 10. Parametric snap hook
Arm thickness (constant-section cantilever, Bayer guide «Snap-Fit Joints for Plastics»): **h = 0.67 · ε · l² / y**, with l arm
length, y undercut, ε allowed strain of the material (for a 3D-printed part that of the printed part, lower
for repeated assembly: from the manufacturer or from a test piece). Tested example: l 12, y 0.8, width 8, thickness 1.86 (ε ≈ 1.5 %). If a
3D printing skill is installed (setting `skill_stampa`), it gives ε and the thickness. Profile on the XZ plane as in §3 with 6
parameters and expression dimensions:
`gancio_sottosquadro * tan(gancio_ritorno)` and `gancio_sottosquadro / tan(gancio_invito)` for the two faces of the tooth; symmetric
extrude `gancio_larghezza`. Tested: (1.86·12 + ½·0.8·2.186)·8 = 185.554 mm³, sketch constrained.

## 11. Involute gear
Compute the profile in Python (outside Fusion) and pass it as a polyline:
```python
def ingranaggio(z, m=1.0, alfa=20.0, gioco=0.05, fase=0.0, cx=0.0, cy=0.0, n=8):
    a = math.radians(alfa); r = m*z/2; rb = r*math.cos(a); ra = r + m; rf = r - 1.25*m
    inv = lambda t: math.tan(t) - t
    beta = (math.pi*m/2 - gioco) / (2*r)                               # tooth half-angle on the pitch circle
    th = lambda rho: beta + inv(a) - inv(math.acos(min(1.0, rb/rho)))
    r0 = max(rf, rb); fianco = [r0 + (ra - r0)*i/n for i in range(n + 1)]
    pts = []
    for k in range(z):
        c = 2*math.pi*k/z + fase
        pts += ([(rf, c - th(r0))] if rf < rb else []) + [(rho, c - th(rho)) for rho in fianco] + [(ra, c)] + \
               [(rho, c + th(rho)) for rho in reversed(fianco)] + ([(rf, c + th(r0))] if rf < rb else [])
    return [(cx + rr*math.cos(t), cy + rr*math.sin(t)) for rr, t in pts]   # mm
```
Closed polyline in the sketch (reusing the points), profile with maximum area, extrude. Tested m 1, z 20: tip Ø 22.0, root Ø 17.5,
area = Gauss formula; pair at centre distance m·z with backlash 0.1: 0 interferences in 3 positions; with thicker teeth the interference
appears. For large modules increase `n`. Helical and bevel gears not studied.

## 12. Joints between components
```python
occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create()); occ.component.name = "Braccio"
g0 = adsk.fusion.JointGeometry.createByPlanarFace(faccia_fissa.createForAssemblyContext(occ_fisso), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
g1 = adsk.fusion.JointGeometry.createByPlanarFace(faccia_mobile.createForAssemblyContext(occ), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
ji = r.joints.createInput(g1, g0); ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
ji.isFlipped = True        # without it, with bottom→top faces the part flips INSIDE the other (full interference, no error)
j = r.joints.add(ji); j.jointMotion.rotationValue = math.radians(45)
```
After every joint: no interpenetration, clearance measured and body position as expected (`occ.transform2.translation`). Limits: set them **before** the
values (enabling them resets the joint to 0); an out-of-range value is silently ignored → read the value back. `occurrence.boundingBox`
gives zeros: measure the bodies. Slider: `setAsSliderJointMotion(XAxisJointDirection)`, `slideValue` in cm.

## 13. Materials and mass (by code, names are localized)
```python
lib = max(app.materialLibraries, key=lambda l: l.materials.count)
b.material = lib.materials.itemById("PrismMaterial-022")      # ABS plastic 1 060 kg/m³; steel = PrismMaterial-018 (7 850)
massa_g = b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.HighCalculationAccuracy).mass * 1000
```

## 14. Interference between bodies or components
```python
oc = adsk.core.ObjectCollection.create(); oc.add(a); oc.add(b)
ris = d.analyzeInterference(d.createInterferenceInput(oc)); volumi = [x.interferenceBody.volume * 1000 for x in ris]
```

## 15. Export and save on the PC
```python
em = d.exportManager
em.execute(em.createC3MFExportOptions(r, file_3mf))                 # 3MF in mm (visible bodies!)
em.execute(em.createSTEPExportOptions(file_step, r))
em.execute(em.createFusionArchiveExportOptions(file_f3d, r))        # .f3d design: reopened it stays parametric
im = app.importManager; im.importToNewDocument(im.createFusionArchiveImportOptions(file_f3d))   # reopening
```
After every export check that the file exists; the 3MF goes through `scripts/controlla_mesh.py` with the expected dimensions axis by axis.
Mesh quality: for **STL** the options are ignored (tested: 6 settings → identical files); for **3MF they work** and are needed
(tested: with the default settings an R33 arc came out 0.04 mm shorter and the 0.01 mm check failed; with
custom refinement at 0.01 mm deviation it passes — heavier file, 1.7 MB for a flange):
```python
o = em.createC3MFExportOptions(r, file_3mf)
o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom; o.surfaceDeviation = 0.001   # cm = 0.01 mm
em.execute(o)
```

### Threads: careful
- **Cosmetic threads change the diameters** of the model to the standard's dimensions without errors (tested: hub Ø45 → Ø44.822, hole
  Ø10.106 → Ø10.2735; the volume dropped by 444 mm³ and only the expected-value check found it). If the dimensions of the drawing or of the user
  must stay as they are: if the user wants **only the dimensions**, no thread and data in the parameter comment; if they want **the cosmetic thread too**,
  put it and restore the diameter with «Move Face» right after (tested: exact volume, `.f3d` reopened without errors). That step has a fixed value:
  if the diameter changes it must be updated, and it must be said in the report. Do not remove something requested without saying so.
- **Internal** thread (nut thread, class 6H): `q.allClasses(True, tipo, designazione)` and `adsk.fusion.ThreadInfo.create(False, True, tipo,
  designazione, classe, True)` (the second argument `True` = internal). External: `allClasses(False, …)`, `ThreadInfo.create(False, False, …)`.

## 16. Images and render
- Images of the part: set the **camera by hand** and save with the view — the default directions (`viewOrientation`, or the
  screenshot with `direction`) have several times given images **all identical** (tested on two occasions):
  ```python
  vp = app.activeViewport; cam = vp.camera
  cam.eye = P(30, -30, 25); cam.target = P(0, 0, 2.5); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); cam.isSmoothTransition = False
  vp.camera = cam; vp.fit(); vp.saveAsImageFile(file_png, 1200, 900)
  ```
  Look at every image: they must be different and show the part as in the drawing.
- **Local** render (free): `rd = d.renderManager.rendering; rd.resolution = adsk.fusion.RenderResolutions.Web800x600RenderResolution;
  rd.renderQuality = 25; rd.startLocalRender(file_png, app.activeViewport.camera)` (asynchronous: wait for the file to exist).
  Cloud render is paid.
