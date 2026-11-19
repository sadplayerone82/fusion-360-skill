# Recipes: solid features

> Recipes tested in Fusion (Nov. 2026), each with its measured result.

**How to use them**: each recipe shows the API call that **works** (tested, with the measured result). The tests use shortcuts (`rett`, `blocco`: rectangles **without constraints**, numeric dimensions): in a real model sketches are fully constrained and dimensions are parameters (`ricette.md` §2–§3, `metodo.md`). API coordinates are in **cm**.

Each recipe has the expected value computed beforehand and the measured volume: copy, adapt, and recompute the expected value.

**Index** (long file: look up the section, do not read it all)
| Line | Section | When |
|---|---|---|
| 17 | Header | the names already defined in the examples |
| 41 | Tested recipes (21): extrudes, revolve, sweep, loft, holes, thread, shell, fillets, chamfers, draft, patterns, mirror, combine, split, rib | a solid feature |
| 301 | Complete professional example: plate with parameters and constraints; complete L bracket | a real part from start to finish |
| 395 | Does not work this way | — |

## Header

**Simplified** header used by these scripts (names and helper functions already defined; the real one of the skill's scripts, with
high-precision `vol` and `controlla`, is in `ricette.md` §1):
```python
import adsk.core, adsk.fusion, math, json
app = adsk.core.Application.get()
d = adsk.fusion.Design.cast(app.activeProduct)
r = d.rootComponent
F = r.features
P = adsk.core.Point3D.create
S = adsk.core.ValueInput.createByString
OP = adsk.fusion.FeatureOperations
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
def rett(x0, y0, x1, y1, piano=None):
    sk = r.sketches.add(piano or r.xYConstructionPlane)
    sk.sketchCurves.sketchLines.addTwoPointRectangle(P(x0/10, y0/10, 0), P(x1/10, y1/10, 0)); return sk
def blocco(x0, y0, x1, y1, h, op=OP.NewBodyFeatureOperation):
    return F.extrudeFeatures.addSimple(rett(x0, y0, x1, y1).profiles.item(0), S(f'{h} mm'), op)
def vol(b): return round(b.volume * 1000, 4)
def out(**k): print('RIS' + json.dumps(k))
```

## Tested recipes (21)

### 01_estrusione
Expected (computed beforehand): `{"v": 4000}`  
Recorded result: `{"v": 4000.0}`
```python
e = blocco(0, 0, 20, 20, 10); out(v=vol(e.bodies.item(0)))
```

### 02_conicita_5gradi
Expected (computed beforehand): `{"v": 4360.1603}`  
Recorded result: `{"v": 4360.1603, "dx_max": 21.7498}`
```python
sk = rett(0, 0, 20, 20)
i = F.extrudeFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation)
i.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(S("10 mm")), adsk.fusion.ExtentDirections.PositiveExtentDirection, S("5 deg"))
e = F.extrudeFeatures.add(i); b = e.bodies.item(0); bb = b.boundingBox
out(v=vol(b), dx_max=round((bb.maxPoint.x - bb.minPoint.x) * 10, 4))
```

### 02b_conicita_meno_5gradi
Expected (computed beforehand): `{"v": 3660.251}`  
Recorded result: `{"v": 3660.251}`
```python
sk = rett(0, 0, 20, 20)
i = F.extrudeFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation)
i.setOneSideExtent(adsk.fusion.DistanceExtentDefinition.create(S("10 mm")), adsk.fusion.ExtentDirections.PositiveExtentDirection, S("-5 deg"))
out(v=vol(F.extrudeFeatures.add(i).bodies.item(0)))
```

### 03_fino_a_oggetto
Expected (computed beforehand): `{"v": 10000}`  
Recorded result: `{"v": 10000.0}`
```python
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("25 mm")); pl = r.constructionPlanes.add(pi)
i = F.extrudeFeatures.createInput(rett(0, 0, 20, 20).profiles.item(0), OP.NewBodyFeatureOperation)
i.setOneSideExtent(adsk.fusion.ToEntityExtentDefinition.create(pl, False), adsk.fusion.ExtentDirections.PositiveExtentDirection)
out(v=vol(F.extrudeFeatures.add(i).bodies.item(0)))
```

### 04_inizio_sfalsato
Expected (computed beforehand): `{"v": 4000, "z_min": 5, "z_max": 15}`  
Recorded result: `{"v": 4000.0, "z_min": 5.0, "z_max": 15.0}`
```python
i = F.extrudeFeatures.createInput(rett(0, 0, 20, 20).profiles.item(0), OP.NewBodyFeatureOperation)
i.startExtent = adsk.fusion.OffsetStartDefinition.create(S("5 mm"))
i.setDistanceExtent(False, S("10 mm"))
b = F.extrudeFeatures.add(i).bodies.item(0); bb = b.boundingBox
out(v=vol(b), z_min=round(bb.minPoint.z * 10, 4), z_max=round(bb.maxPoint.z * 10, 4))
```

### 05_rivoluzione
Expected (computed beforehand): `{"v": 3926.9908}`  
Recorded result: `{"v": 3926.9908}`
```python
sk = r.sketches.add(r.xZConstructionPlane)
sk.sketchCurves.sketchLines.addTwoPointRectangle(P(1.0, 0, 0), P(1.5, 1.0, 0))
i = F.revolveFeatures.createInput(sk.profiles.item(0), r.zConstructionAxis, OP.NewBodyFeatureOperation)
i.setAngleExtent(False, S("360 deg"))
out(v=vol(F.revolveFeatures.add(i).bodies.item(0)))
```

### 06_sweep
Expected (computed beforehand): `{"v": 628.3185}`  
Recorded result: `{"v": 628.3185}`
```python
sp = r.sketches.add(r.yZConstructionPlane); sp.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 0.2)
sl = r.sketches.add(r.xYConstructionPlane); ln = sl.sketchCurves.sketchLines.addByTwoPoints(P(0, 0, 0), P(5, 0, 0))
i = F.sweepFeatures.createInput(sp.profiles.item(0), F.createPath(ln), OP.NewBodyFeatureOperation)
out(v=vol(F.sweepFeatures.add(i).bodies.item(0)))
```

### 07_loft
Expected (computed beforehand): `{"v": 2333.3333}`  
Recorded result: `{"v": 2333.3333}`
```python
s1 = rett(-10, -10, 10, 10)
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("10 mm")); pl = r.constructionPlanes.add(pi)
s2 = rett(-5, -5, 5, 5, pl)
i = F.loftFeatures.createInput(OP.NewBodyFeatureOperation)
i.loftSections.add(s1.profiles.item(0)); i.loftSections.add(s2.profiles.item(0))
out(v=vol(F.loftFeatures.add(i).bodies.item(0)))
```

### 08_foro_passante
Expected (computed beforehand): `{"v": 3717.2567}`  
Recorded result: `{"v": 3717.2567}`
```python
e = blocco(0, 0, 20, 20, 10)
hi = F.holeFeatures.createSimpleInput(S("6 mm"))
hi.setPositionByPoint(e.endFaces.item(0), P(1, 1, 1))
hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)  # positive = into the part (negative: logicalSelection error)
h = F.holeFeatures.add(hi)
out(v=vol(e.bodies.item(0)))
```

### 09_filettatura_M10
Expected (computed beforehand): `{"v_cilindro": 1570.7963, "intervallo_v_filettato": [1102.0295, 1570.7963]}`  
Recorded result: `{"v_cilindro": 1570.7963, "v_filettato": 1270.4799, "tipo": "ISO Metric profile", "designazione": "M10x1.5", "classi": ["4g6g", "6g"], "modellata": true, "tipi_filettatura": 18}`
```python
sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 0.5)
e = F.extrudeFeatures.addSimple(sk.profiles.item(0), S("20 mm"), OP.NewBodyFeatureOperation)
b = e.bodies.item(0); v0 = vol(b)
cil = [f for f in b.faces if isinstance(f.geometry, adsk.core.Cylinder)][0]
q = adsk.fusion.ThreadDataQuery.create()
tipo = "ISO Metric profile"  # «ISO Metric» alone picks «ISO Metric Trapezoidal Threads» first
des = [x for x in q.allDesignations(tipo, "10.0") if x.startswith("M10x1.5")][0]  # sizes written «10.0»
cl = q.allClasses(False, tipo, des)
ti = adsk.fusion.ThreadInfo.create(False, False, tipo, des, cl[0], True)
fc = adsk.core.ObjectCollection.create(); fc.add(cil)
ii = F.threadFeatures.createInput(fc, ti); ii.isModeled = True; ii.isFullLength = True
th = F.threadFeatures.add(ii)
out(v_cilindro=v0, v_filettato=vol(b), tipo=tipo, designazione=des, classi=list(cl), modellata=th.isModeled, tipi_filettatura=len(q.allThreadTypes))
```

### 10_guscio_2mm
Expected (computed beforehand): `{"v": 1952}`  
Recorded result: `{"v": 1952.0}`
```python
e = blocco(0, 0, 20, 20, 10)
c = adsk.core.ObjectCollection.create(); c.add(e.endFaces.item(0))
si = F.shellFeatures.createInput(c, False); si.insideThickness = S("2 mm")
F.shellFeatures.add(si)
out(v=vol(e.bodies.item(0)))
```

### 11_raccordo_spigoli_verticali
Expected (computed beforehand): `{"v": 3965.6637, "spigoli": 4}`  
Recorded result: `{"v": 3965.6637, "spigoli": 4}`
```python
e = blocco(0, 0, 20, 20, 10); b = e.bodies.item(0)
sp = adsk.core.ObjectCollection.create()
for ed in b.edges:
    g = ed.geometry
    if isinstance(g, adsk.core.Line3D) and abs(g.startPoint.z - g.endPoint.z) > 0.5: sp.add(ed)
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(sp, S("2 mm"), True)
F.filletFeatures.add(fi)
out(v=vol(b), spigoli=sp.count)
```

### 12_smusso_1mm
Expected (computed beforehand): `{"v": 3980.0}`  
Recorded result: `{"v": 3980.0}`
```python
e = blocco(0, 0, 20, 20, 10); b = e.bodies.item(0)
sp = adsk.core.ObjectCollection.create()
for ed in b.edges:
    g = ed.geometry
    if isinstance(g, adsk.core.Line3D) and abs(g.startPoint.z - g.endPoint.z) > 0.5: sp.add(ed)
ci = F.chamferFeatures.createInput2(); ci.chamferEdgeSets.addEqualDistanceChamferEdgeSet(sp, S("1 mm"), True)
F.chamferFeatures.add(ci)
out(v=vol(b))
```

### 13_sformo_5gradi
Expected (computed beforehand): `{"v": 4360.1603}`  
Recorded result: `{"v": 4360.1603, "dx_max": 21.7498}`
```python
e = blocco(0, 0, 20, 20, 10); b = e.bodies.item(0)
lat = [f for f in e.sideFaces]
di = F.draftFeatures.createInput(lat, e.startFaces.item(0), True)
di.setSingleAngle(False, S("5 deg"))
F.draftFeatures.add(di)
bb = b.boundingBox
out(v=vol(b), dx_max=round((bb.maxPoint.x - bb.minPoint.x) * 10, 4))
```

### 14_serie_rettangolare_fori
Expected (computed beforehand): `{"v": 5811.5044}`  
Recorded result: `{"v": 5811.5044}`
```python
e = blocco(0, 0, 60, 20, 5)
hi = F.holeFeatures.createSimpleInput(S("4 mm")); hi.setPositionByPoint(e.endFaces.item(0), P(1, 1, 0.5))
hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection); h = F.holeFeatures.add(hi)
c = adsk.core.ObjectCollection.create(); c.add(h)
pi = F.rectangularPatternFeatures.createInput(c, r.xConstructionAxis, S("3"), S("20 mm"), adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
F.rectangularPatternFeatures.add(pi)
out(v=vol(e.bodies.item(0)))
```

### 15_serie_circolare_fori
Expected (computed beforehand): `{"v": 5906.1942}`  
Recorded result: `{"v": 5906.1942}`
```python
sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 2)
e = F.extrudeFeatures.addSimple(sk.profiles.item(0), S("5 mm"), OP.NewBodyFeatureOperation)
hi = F.holeFeatures.createSimpleInput(S("4 mm")); hi.setPositionByPoint(e.endFaces.item(0), P(1.5, 0, 0.5))
hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection); h = F.holeFeatures.add(hi)
c = adsk.core.ObjectCollection.create(); c.add(h)
ci = F.circularPatternFeatures.createInput(c, r.zConstructionAxis); ci.quantity = S("6"); ci.totalAngle = S("360 deg")
F.circularPatternFeatures.add(ci)
out(v=vol(e.bodies.item(0)))
```

### 16_specchio_corpo
Expected (computed beforehand): `{"corpi": 2, "v": 4000, "x_min": -25, "x_max": -5}`  
Recorded result: `{"corpi": 2, "v": 4000.0, "x_min": -25.0, "x_max": -5.0}`
```python
e = blocco(5, 0, 25, 20, 10)
c = adsk.core.ObjectCollection.create(); c.add(e.bodies.item(0))
m = F.mirrorFeatures.add(F.mirrorFeatures.createInput(c, r.yZConstructionPlane))
b2 = m.bodies.item(0); bb = b2.boundingBox
out(corpi=r.bRepBodies.count, v=vol(b2), x_min=round(bb.minPoint.x * 10, 4), x_max=round(bb.maxPoint.x * 10, 4))
```

### 17_combina_taglio
Expected (computed beforehand): `{"corpi": 1, "v": 3000}`  
Recorded result: `{"corpi": 1, "v": 3000.0}`
```python
a = blocco(0, 0, 20, 20, 10).bodies.item(0)
t = blocco(5, 5, 15, 15, 20).bodies.item(0)
c = adsk.core.ObjectCollection.create(); c.add(t)
ci = F.combineFeatures.createInput(a, c); ci.operation = OP.CutFeatureOperation; ci.isKeepToolBodies = False
F.combineFeatures.add(ci)
out(corpi=r.bRepBodies.count, v=vol(a))
```

### 18_dividi_corpo
Expected (computed beforehand): `{"corpi": 2, "volumi": [1600, 2400]}`  
Recorded result: `{"corpi": 2, "volumi": [1600.0, 2400.0]}`
```python
a = blocco(0, 0, 20, 20, 10).bodies.item(0)
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("4 mm")); pl = r.constructionPlanes.add(pi)
F.splitBodyFeatures.add(F.splitBodyFeatures.createInput(a, pl, True))
out(corpi=r.bRepBodies.count, volumi=sorted(vol(b) for b in r.bRepBodies))
```

### 19_nervatura
Expected (computed beforehand): `{"v_squadretta": 7500, "v_con_nervatura": 9300.0}`  
Recorded result: `{"v_squadretta": 7500.0, "v_con_nervatura": 9300.0}`
```python
base = blocco(0, 0, 40, 20, 5); b = base.bodies.item(0)
sk = r.sketches.add(r.yZConstructionPlane)
w = F.extrudeFeatures.createInput(rett(0, 0, 5, 20).profiles.item(0), OP.JoinFeatureOperation)
w.setDistanceExtent(False, S("40 mm")); F.extrudeFeatures.add(w)
v0 = vol(b)
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xZConstructionPlane, S("10 mm")); pl = r.constructionPlanes.add(pi)
sr = r.sketches.add(pl)
ln = sr.sketchCurves.sketchLines.addByTwoPoints(sr.modelToSketchSpace(P(0.5, 1, 3.5)), sr.modelToSketchSpace(P(3.5, 1, 0.5)))
ri = F.ribFeatures.createInput([ln], S("4 mm"), b)
ri.isFlipped = True  # with the default direction the rib went outside the part (11,272 mm³) without errors
rb = F.ribFeatures.add(ri)
out(v_squadretta=v0, v_con_nervatura=vol(b))
```

### 19b_nervatura_direzione_predefinita
Expected (computed beforehand): `{"fuori_dal_pezzo": 1}`  
Recorded result: `{"v": 11272.0, "x_min": -2.0, "x_max": 42.0, "fuori_dal_pezzo": 1}`
```python
base = blocco(0, 0, 40, 20, 5); b = base.bodies.item(0)
w = F.extrudeFeatures.createInput(rett(0, 0, 5, 20).profiles.item(0), OP.JoinFeatureOperation)
w.setDistanceExtent(False, S("40 mm")); F.extrudeFeatures.add(w)
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xZConstructionPlane, S("10 mm")); pl = r.constructionPlanes.add(pi)
sr = r.sketches.add(pl)
ln = sr.sketchCurves.sketchLines.addByTwoPoints(sr.modelToSketchSpace(P(0.5, 1, 3.5)), sr.modelToSketchSpace(P(3.5, 1, 0.5)))
F.ribFeatures.add(F.ribFeatures.createInput([ln], S("4 mm"), b))
bb = b.boundingBox
out(v=vol(b), x_min=round(bb.minPoint.x * 10, 3), x_max=round(bb.maxPoint.x * 10, 3), fuori_dal_pezzo=int(bb.minPoint.x < -1e-6 or bb.maxPoint.x > 4 + 1e-6))
```

## Complete professional example

### «professional» plate (parameters, constraints, construction plane, names) — survives edits
Tested: after length 60 → 90 and thickness 5 → 8 the design intent is respected (0 violations); the same plate made with fixed coordinates has 2.
```python
up = d.userParameters
up.add("lunghezza", S("60 mm"), "mm", ""); up.add("larghezza", S("40 mm"), "mm", ""); up.add("spessore", S("5 mm"), "mm", "")
up.add("diametro_foro", S("6 mm"), "mm", ""); up.add("distanza_foro", S("8 mm"), "mm", "")
up.add("diametro_perno", S("16 mm"), "mm", ""); up.add("altezza_perno", S("10 mm"), "mm", "")
sk = r.sketches.add(r.xYConstructionPlane); sk.name = "SK_piastra"
l = sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(6, 4, 0))
g = sk.geometricConstraints; dm = sk.sketchDimensions
g.addCoincident(l[0].startSketchPoint, sk.originPoint)
g.addHorizontal(l[0]); g.addVertical(l[1]); g.addHorizontal(l[2]); g.addVertical(l[3])
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(3, -0.5, 0)).parameter.expression = "lunghezza"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(6.5, 2, 0)).parameter.expression = "larghezza"
# holes in the same sketch, constrained to the edges and the centre line
mez = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, 2, 0), P(6, 2, 0)); mez.isConstruction = True
g.addMidPoint(mez.startSketchPoint, l[3]); g.addMidPoint(mez.endSketchPoint, l[1])
for x, bordo in ((0.8, l[3]), (5.2, l[1])):
    c = sk.sketchCurves.sketchCircles.addByCenterRadius(P(x, 2, 0), 0.3)
    g.addCoincident(c.centerSketchPoint, mez)
    dm.addDiameterDimension(c, P(x + 0.5, 2.6, 0)).parameter.expression = "diametro_foro"
    dm.addOffsetDimension(bordo, c.centerSketchPoint, P(x, 1, 0)).parameter.expression = "distanza_foro"
prof = max(sk.profiles, key=lambda p: p.profileLoops.count)
e = r.features.extrudeFeatures.addSimple(prof, S("spessore"), OP.NewBodyFeatureOperation); e.name = "EST_piastra"; e.bodies.item(0).name = "Piastra"
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("spessore"))
piano = r.constructionPlanes.add(pi); piano.name = "PIANO_sopra"
skp = r.sketches.add(piano); skp.name = "SK_perno"
c = skp.sketchCurves.sketchCircles.addByCenterRadius(P(3, 2, 0), 0.8)
o = skp.project(sk.originPoint).item(0)
skp.sketchDimensions.addDiameterDimension(c, P(4, 3, 0)).parameter.expression = "diametro_perno"
skp.sketchDimensions.addDistanceDimension(o, c.centerSketchPoint, H, P(1.5, -1, 0)).parameter.expression = "lunghezza / 2"
skp.sketchDimensions.addDistanceDimension(o, c.centerSketchPoint, V, P(-1, 1, 0)).parameter.expression = "larghezza / 2"
p = r.features.extrudeFeatures.addSimple(skp.profiles.item(0), S("altezza_perno"), OP.JoinFeatureOperation); p.name = "EST_perno"
print("professional plate built; constrained sketches:", [(s.name, s.isFullyConstrained) for s in r.sketches])
```

### complete L bracket: parameters, constrained profile on the XZ plane, symmetric extrude, fillet chosen by geometry, aligned constrained holes (whole J flow)
Tested: volume `{"volume": 7905.309, "ingombro": [40.0, 30.0, 30.0], "minimo": [0.0, -15.0, 0.0], "fori": [[28.0, -8.0], [28.0, 8.0]], "corpi": 1}`, after changing 4 parameters `{"volume": 14967.15, "ingombro": [60.0, 30.0, 45.0], "minimo": [0.0, -15.0, 0.0], "fori": [[48.0, -8.0], [48.0, 8.0]], "corpi": 1}` = recomputed expected values; report `{"non_sani": [], "schizzi_non_vincolati": [], "parametri_utente": 9, "timeline": 5}`.
```python
up = d.userParameters
for nome, val, nota in [('lunghezza_base', 40, ''), ('larghezza', 30, ''), ('spessore_base', 4, ''), ('altezza', 30, ''), ('spessore_parete', 4, ''), ('raggio', 3, ''), ('diametro_foro', 3.4, ''), ('distanza_foro', 12, ''), ('interasse', 16, '')]:
    up.add(nome, S(f"{val} mm"), "mm", nota)
# J2 L profile on the XZ plane, points given in MODEL coordinates and converted (on the XZ plane the sketch Y is −Z)
sk = r.sketches.add(r.xZConstructionPlane); sk.name = "SK_profilo"
m = lambda x, z: sk.modelToSketchSpace(P(x / 10, 0, z / 10))
pt = [m(0, 0), m(40, 0), m(40, 4), m(4, 4), m(4, 30), m(0, 30)]
L = sk.sketchCurves.sketchLines; li = []
for i in range(6):
    a = li[-1].endSketchPoint if li else pt[0]
    b = li[0].startSketchPoint if i == 5 else pt[i + 1]
    li.append(L.addByTwoPoints(a, b))
g = sk.geometricConstraints; dm = sk.sketchDimensions
g.addCoincident(li[0].startSketchPoint, sk.originPoint)
for i in (0, 2, 4): g.addHorizontal(li[i])
for i in (1, 3, 5): g.addVertical(li[i])
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation; V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
for linea, ori, nome in ((li[0], H, "lunghezza_base"), (li[1], V, "spessore_base"), (li[4], H, "spessore_parete"), (li[5], V, "altezza")):
    c = linea.startSketchPoint.geometry
    dm.addDistanceDimension(linea.startSketchPoint, linea.endSketchPoint, ori, P(c.x + 0.3, c.y + 0.3, 0)).parameter.expression = nome
# J3 symmetric extrude over the width
ei = F.extrudeFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation)
ei.setSymmetricExtent(S("larghezza"), True)
e = F.extrudeFeatures.add(ei); e.name = "EST_staffa"; b = e.bodies.item(0); b.name = "Staffa"
# J4 fillet: the straight edge of the inner corner (x = spessore_parete, z = spessore_base), chosen by geometry
sp = [s for s in b.edges if all(abs(v.geometry.x - 0.4) < 1e-6 and abs(v.geometry.z - 0.4) < 1e-6 for v in (s.startVertex, s.endVertex))]
col = adsk.core.ObjectCollection.create(); [col.add(s) for s in sp]
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(col, S("raggio"), True)
f = F.filletFeatures.add(fi); f.name = "RAC_interno"
# J5 holes on the XY plane, dimensioned from the origin with design-intent expressions, cut towards +Z
sf = r.sketches.add(r.xYConstructionPlane); sf.name = "SK_fori"
# a 2nd horizontal dimension from the origin to a point vertically aligned with one already dimensioned gives «over-constrained» (tested):
# the 2nd hole is tied to the 1st with a vertical construction line and the centre-distance dimension
o = sf.originPoint; dmf = sf.sketchDimensions
c1 = sf.sketchCurves.sketchCircles.addByCenterRadius(sf.modelToSketchSpace(P(2.8, 0.8, 0)), 0.17)
c2 = sf.sketchCurves.sketchCircles.addByCenterRadius(sf.modelToSketchSpace(P(2.8, -0.8, 0)), 0.17)
lc = sf.sketchCurves.sketchLines.addByTwoPoints(c1.centerSketchPoint, c2.centerSketchPoint); lc.isConstruction = True
sf.geometricConstraints.addVertical(lc)
q1, q2 = c1.centerSketchPoint.geometry, c2.centerSketchPoint.geometry
dmf.addDiameterDimension(c1, P(q1.x + 0.5, q1.y + 0.5, 0)).parameter.expression = "diametro_foro"
dmf.addDiameterDimension(c2, P(q2.x + 0.5, q2.y - 0.5, 0)).parameter.expression = "diametro_foro"
dmf.addDistanceDimension(o, c1.centerSketchPoint, H, P(q1.x / 2, q1.y + 0.6, 0)).parameter.expression = "lunghezza_base - distanza_foro"
dmf.addDistanceDimension(o, c1.centerSketchPoint, V, P(q1.x + 0.7, q1.y / 2, 0)).parameter.expression = "interasse / 2"
dmf.addDistanceDimension(c1.centerSketchPoint, c2.centerSketchPoint, V, P(q1.x + 1.0, 0, 0)).parameter.expression = "interasse"
pr = adsk.core.ObjectCollection.create()
for p in sf.profiles:
    if abs(p.areaProperties().area - math.pi * 0.17 ** 2) < 1e-4: pr.add(p)
ci = F.extrudeFeatures.createInput(pr, OP.CutFeatureOperation)
ci.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
t = F.extrudeFeatures.add(ci); t.name = "TAGLIO_fori"
out(fori_profili=pr.count, spigoli_raccordo=len(sp), schizzi=[(s.name, s.isFullyConstrained) for s in r.sketches])
```

## Does not work this way

(none)

