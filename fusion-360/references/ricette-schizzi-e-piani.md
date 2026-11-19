# Recipes: sketches, constraints, planes and axes, finding entities again

> Recipes tested on Fusion (Nov. 2026), each with the measured result.

**How to use them**: each recipe shows the API call that **works** (tested, with the measured result). The tests use shortcuts (`rett`, `blocco`: rectangles **without constraints**, dimensions as numbers): in a real model sketches are fully constrained and dimensions are parameters (`ricette.md` §2–§3, `metodo.md`). API coordinates are in **cm**.

Every sketch must be fully constrained (`isFullyConstrained`); the API does not add constraints by itself.

Index: Header · Tested recipes · Does not work this way · Finding sketches, features, faces again between one script and the next

## Header

**Simplified** header used by these scripts (names and helper functions already defined; the real one of the skill's scripts is in
`ricette.md` §1):
```python
import adsk.core, adsk.fusion, math, json
app = adsk.core.Application.get()
d = adsk.fusion.Design.cast(app.activeProduct)
r = d.rootComponent
P = adsk.core.Point3D.create
S = adsk.core.ValueInput.createByString
NB = adsk.fusion.FeatureOperations.NewBodyFeatureOperation
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation
V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
def nuovo(nome, piano=None):
    sk = r.sketches.add(piano or r.xYConstructionPlane); sk.name = nome; return sk
```

## Tested recipes

### rettangolo_centrato
Recorded output: `["lines 4 | constrained without dimensions: False", "with 2 dimensions constrained: False | constraints created by Fusion: []"]`
```python
sk = nuovo("SK_rett_centrato")
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(2, 1, 0))
print("lines", l.count, "| constrained without dimensions:", sk.isFullyConstrained)
dm = sk.sketchDimensions
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)).parameter.expression = "40 mm"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(2.5, 0, 0)).parameter.expression = "20 mm"
print("with 2 dimensions constrained:", sk.isFullyConstrained, "| constraints created by Fusion:", [c.objectType.split('::')[-1] for c in sk.geometricConstraints])
```

### ricetta_rettangolo_centrato_vincolato
Recorded output: `["RECIPE constrained: True | sides mm [40.0, 20.0, 40.0, 20.0] | centre mm [0.0, 0.0]"]`
```python
sk = nuovo("SK_rett_ricetta")
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(2, 1, 0))
g = sk.geometricConstraints; dm = sk.sketchDimensions
g.addHorizontal(l[0]); g.addVertical(l[1]); g.addHorizontal(l[2]); g.addVertical(l[3])
dg = sk.sketchCurves.sketchLines.addByTwoPoints(l[0].startSketchPoint, l[2].startSketchPoint); dg.isConstruction = True
g.addMidPoint(sk.originPoint, dg)
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)).parameter.expression = "40 mm"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(2.5, 0, 0)).parameter.expression = "20 mm"
bb = sk.boundingBox
print("RECIPE constrained:", sk.isFullyConstrained, "| sides mm", [round(x.length * 10, 4) for x in l], "| centre mm", [round((l[0].startSketchPoint.geometry.x + l[2].startSketchPoint.geometry.x) * 5, 4), round((l[0].startSketchPoint.geometry.y + l[2].startSketchPoint.geometry.y) * 5, 4)])
```

### asola
Recorded output: `["slot: objects <vector of API objects> | curves 5 | profiles 1 | constrained False"]`
```python
sk = nuovo("SK_asola")
res = sk.addCenterToCenterSlot(P(0, 0, 0), P(3, 0, 0), S("8 mm"))
print("slot: objects", res.count if hasattr(res, 'count') else res, "| curves", sk.sketchCurves.count, "| profiles", sk.profiles.count, "| constrained", sk.isFullyConstrained)
```

### poligono_spline_testo
Recorded output: `["spline: fit points 4 | length mm 46.149", "text: 'Ciao Fusion' | height mm 5.0", "polygon functions in GeometricConstraints: True"]`
```python
sk = nuovo("SK_varie")
g = sk.geometricConstraints
pts = adsk.core.ObjectCollection.create()
for x, y in ((0, 0), (1, 1), (2, 0), (3, 1)): pts.add(P(x, y, 0))
sp = sk.sketchCurves.sketchFittedSplines.add(pts)
print("spline: fit points", sp.fitPoints.count, "| length mm", round(sp.length * 10, 3))
ti = sk.sketchTexts.createInput2("Ciao Fusion", 0.5)
ti.setAsMultiLine(P(0, -2, 0), P(4, -1, 0), adsk.core.HorizontalAlignments.LeftHorizontalAlignment, adsk.core.VerticalAlignments.TopVerticalAlignment, 0)
t = sk.sketchTexts.add(ti)
print("text:", repr(t.text), "| height mm", round(t.height * 10, 3))
print("polygon functions in GeometricConstraints:", hasattr(g, "addPolygon"))
```

### serie_nello_schizzo
Recorded output: `["circular pattern: total circles 6", "after 3x2 rectangular pattern: total circles 12 (expected 6 + 6 = 12)"]`
```python
sk = nuovo("SK_serie")
c = sk.sketchCurves.sketchCircles.addByCenterRadius(P(2, 0, 0), 0.3)
ent = adsk.core.ObjectCollection.create(); ent.add(c)
g = sk.geometricConstraints
ci = g.createCircularPatternInput([c], sk.originPoint)
ci.quantity = S("6")
ci.totalAngle = S("360 deg")
pat = g.addCircularPattern(ci)
print("circular pattern: total circles", sk.sketchCurves.sketchCircles.count)
c2 = sk.sketchCurves.sketchCircles.addByCenterRadius(P(5, 0, 0), 0.2)
ri = g.createRectangularPatternInput([c2], adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
ri.setDirectionOne(sk.sketchCurves.sketchLines.addByTwoPoints(P(5, -1, 0), P(6, -1, 0)), S("3"), S("10 mm"))
ri.setDirectionTwo(sk.sketchCurves.sketchLines.addByTwoPoints(P(5, -1, 0), P(5, 0, 0)), S("2"), S("10 mm"))
g.addRectangularPattern(ri)
print("after 3x2 rectangular pattern: total circles", sk.sketchCurves.sketchCircles.count, "(expected 6 + 6 = 12)")
```

### curva_intersezione
Recorded output: `["intersection curves: 2 ['SketchEllipticalArc', 'SketchLine']"]`
```python
sk = nuovo("SK_cil")
sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 1)
e = r.features.extrudeFeatures.addSimple(sk.profiles.item(0), S("30 mm"), NB); e.name = "EST_cil"
pi = r.constructionPlanes.createInput(); pi.setByAngle(r.xAxis if hasattr(r, 'xAxis') else r.xConstructionAxis, S("30 deg"), r.xYConstructionPlane)
pt = r.constructionPlanes.add(pi); pt.name = "PIANO_inclinato"
s2 = nuovo("SK_intersezione", pt)
curve = s2.intersectWithSketchPlane([e.bodies.item(0)])
print("intersection curves:", len(curve), [x.objectType.split('::')[-1] for x in curve])
```

### costruzione
Recorded output: `["construction True | centerline True | profiles (construction does not create profiles) 2"]`
```python
sk = nuovo("SK_costruzione")
m = sk.sketchCurves.sketchLines.addByTwoPoints(P(-2, 0, 0), P(2, 0, 0)); m.isConstruction = True
c = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, -2, 0), P(0, 2, 0)); c.isCenterLine = True
sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 1)
print("construction", m.isConstruction, "| centerline", c.isCenterLine, "| profiles (construction does not create profiles)", sk.profiles.count)
```

### parametri
Recorded output: `["dimensions: d18 = lato_d1 25.0 mm | d19 = lato_d1 * 2 50.0 mm | constrained False"]`
```python
d.userParameters.add("lato_d1", S("25 mm"), "mm", "side of the square")
sk = nuovo("SK_param")
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(1, 1, 0))
dm = sk.sketchDimensions
a = dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)); a.parameter.expression = "lato_d1"
b = dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(1.5, 0, 0)); b.parameter.expression = "lato_d1 * 2"
print("dimensions:", a.parameter.name, "=", a.parameter.expression, round(a.parameter.value * 10, 3), "mm |", b.parameter.name, "=", b.parameter.expression, round(b.parameter.value * 10, 3), "mm | constrained", sk.isFullyConstrained)
```

### vincoli_avanzati
Recorded output: `["symmetry + equal: x ends mm -10.0 10.0 | lengths mm 10.0 10.0", "curvature (smooth G2) line-spline: True SmoothConstraint", "tangent arc-line: ok"]`
```python
sk = nuovo("SK_vincoli")
g = sk.geometricConstraints; L = sk.sketchCurves.sketchLines
asse = L.addByTwoPoints(P(0, -2, 0), P(0, 2, 0)); asse.isCenterLine = True
a = L.addByTwoPoints(P(-1, 0, 0), P(-1, 1, 0)); b = L.addByTwoPoints(P(1.2, 0, 0), P(1.2, 1.1, 0))
g.addSymmetry(a, b, asse)
g.addEqual(a, b)
print("symmetry + equal: x ends mm", round(a.startSketchPoint.geometry.x * 10, 3), round(b.startSketchPoint.geometry.x * 10, 3), "| lengths mm", round(a.length * 10, 3), round(b.length * 10, 3))
li = L.addByTwoPoints(P(3, 0, 0), P(4, 0, 0))
# the spline STARTS from the line's point (with a new point in the same position the coincidence fails: «failed to create offset»)
pts = adsk.core.ObjectCollection.create()
pts.add(li.endSketchPoint)
for x, y in ((5, 0.5), (6, 0)): pts.add(P(x, y, 0))
sp = sk.sketchCurves.sketchFittedSplines.add(pts)
sm = g.addSmooth(li, sp)
print("curvature (smooth G2) line-spline:", sm is not None, sm.objectType.split('::')[-1] if sm else None)
ar = sk.sketchCurves.sketchArcs.addByCenterStartSweep(P(4, 2, 0), P(5, 2, 0), math.pi / 2)
lt = L.addByTwoPoints(ar.endSketchPoint, P(3, 4, 0))
g.addTangent(ar, lt)
print("tangent arc-line: ok")
```

### entita_3d
Recorded output: `["3D line in the sketch: end z (world) mm 10.0 | length mm 17.321 (expected 17.321 ) | isPlanar sketch? True"]`
```python
sk = nuovo("SK_3D")
l = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, 0, 0), P(1, 1, 1))
s, e = l.startSketchPoint.worldGeometry, l.endSketchPoint.worldGeometry
print("3D line in the sketch: end z (world) mm", round(e.z * 10, 3), "| length mm", round(l.length * 10, 3), "(expected", round(3 ** 0.5 * 10, 3), ") | isPlanar sketch?", getattr(sk, 'isFullyConstrained', None) is not None)
```

### piani_e_assi
Recorded output (3 of the 5 printed lines): `["plane along the path at midpoint: x mm 30.0 (expected 30)", "axis from two planes: direction [0.0, 0.0, -1.0]", "point from three planes: [0.0, 0.0, 0.0]"]`
```python
sk = nuovo("SK_blocco")
sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(4, 2, 0))
e = r.features.extrudeFeatures.addSimple(sk.profiles.item(0), S("10 mm"), NB)
cp = r.constructionPlanes
i = cp.createInput(); i.setByOffset(r.xYConstructionPlane, S("15 mm")); p1 = cp.add(i)
i = cp.createInput(); i.setByTwoPlanes(e.startFaces.item(0), e.endFaces.item(0)); pm = cp.add(i)
print("offset plane z mm", round(p1.geometry.origin.z * 10, 3), "| midplane z mm", round(pm.geometry.origin.z * 10, 3), "(expected 5)")
i = cp.createInput(); i.setByAngle(sk.sketchCurves.sketchLines.item(0), S("45 deg"), r.xYConstructionPlane); pa = cp.add(i)
n = pa.geometry.normal
print("plane at 45°: normal", round(n.x, 4), round(n.y, 4), round(n.z, 4))
sp = nuovo("SK_percorso")
lp = sp.sketchCurves.sketchLines.addByTwoPoints(P(0, 4, 0), P(6, 4, 0))
path = r.features.createPath(lp)
i = cp.createInput(); i.setByDistanceOnPath(path, adsk.core.ValueInput.createByReal(0.5)); pp = cp.add(i)
print("plane along the path at midpoint: x mm", round(pp.geometry.origin.x * 10, 3), "(expected 30)")
ax = r.constructionAxes
ai = ax.createInput(); ai.setByTwoPlanes(r.xZConstructionPlane, r.yZConstructionPlane); a1 = ax.add(ai)
print("axis from two planes: direction", [round(v, 4) for v in a1.geometry.direction.asArray()])
pt = r.constructionPoints
qi = pt.createInput(); qi.setByThreePlanes(r.xYConstructionPlane, r.xZConstructionPlane, r.yZConstructionPlane); q = pt.add(qi)
print("point from three planes:", [round(v * 10, 3) for v in q.geometry.asArray()])
```

### extra_autoconstrain_offset
Recorded output: `["autoConstrain ERROR: 3 : AutoConstrain is not available since user is restricted", "offset with ObjectCollection: ERROR n::SketchCurve >,std::allocator< adsk::core::Ptr< adsk::fusion::SketchCurve > > > const &'", "parametric offset 2 mm: curves 8 | profiles 2"]`
```python
sk = nuovo("SK_auto")
l = sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(3, 2, 0))
dm = sk.sketchDimensions
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(1.5, -0.5, 0))
try:
    ai = sk.createAutoConstrainInput()
    print("autoConstrain input:", ai.objectType)
    res = sk.autoConstrain(ai)
    print("autoConstrain result:", res.objectType if res else None, "| constrained", sk.isFullyConstrained)
except Exception as ex:
    print("autoConstrain ERROR:", str(ex)[-150:])
curves = sk.findConnectedCurves(l[0])
try:
    sk.geometricConstraints.createOffsetInput(curves, S("2 mm")); print("offset with ObjectCollection: accepted")
except Exception as ex:
    print("offset with ObjectCollection: ERROR", str(ex)[-90:])
oi = sk.geometricConstraints.createOffsetInput([c for c in curves], S("2 mm"))
off = sk.geometricConstraints.addOffset2(oi)
print("parametric offset 2 mm: curves", sk.sketchCurves.count, "| profiles", sk.profiles.count)
```

## Does not work this way

(none)

## Finding sketches, features, faces again between one script and the next

Header of these scripts: `d`, `r`, `P` as above.

### giving names and attributes (script 1)
Output: the tokens of the body and of the face (long strings, different at every test) and the number of end, start and side faces.
```python
sk = r.sketches.add(r.xYConstructionPlane)
sk.name = "SK_base"
sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(4, 2, 0))
ext = r.features.extrudeFeatures.addSimple(sk.profiles.item(0), adsk.core.ValueInput.createByString("10 mm"), adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
ext.name = "EST_base"
b = ext.bodies.item(0)
b.name = "Blocco"
alto = ext.endFaces.item(0)
alto.attributes.add("skill-fusion", "faccia", "alto")
spigolo = alto.edges.item(0)
spigolo.attributes.add("skill-fusion", "spigolo", "alto0")
print("token_corpo", b.entityToken)
print("token_alto", alto.entityToken)
print("endFaces", ext.endFaces.count, "startFaces", ext.startFaces.count, "sideFaces", ext.sideFaces.count)
```

### finding by name, token, attribute (script 2, separate)
Recorded output: `["by token: 1 ['adsk::fusion::BRepBody']", "by token: 1 ['adsk::fusion::BRepFace']", "by attribute: 1 adsk::fusion::BRepFace | area mm2 800.0"]`
```python
b = r.bRepBodies.itemByName("Blocco")
print("body by name:", b is not None, "| volume mm3", round(b.volume * 1000, 3) if b else None)
f = r.features.itemByName("EST_base")
print("feature by name:", f is not None, f.objectType if f else None)
sk = r.sketches.itemByName("SK_base")
print("sketch by name:", sk is not None)
TOKEN = ["<token_corpo>", "<token_alto>"]   # the two tokens printed by script 1
for t in TOKEN:
    trovati = d.findEntityByToken(t)
    print("by token:", len(trovati), [x.objectType for x in trovati])
a = d.findAttributes("skill-fusion", "faccia")
print("by attribute:", len(a), a[0].parent.objectType if a and a[0].parent else None, "| area mm2", round(a[0].parent.area * 100, 3) if a and a[0].parent else None)
```

### choosing faces and edges by geometry and filleting them
Recorded output: `["top face found by geometry: True | z mm 10.0", "edges filleted: 4 | volume mm3 7900.059"]`
```python
b = r.bRepBodies.itemByName("Blocco")
alto = None
for f in b.faces:
    ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
    if isinstance(f.geometry, adsk.core.Plane) and n.isParallelTo(adsk.core.Vector3D.create(0, 0, 1)) and n.z > 0:
        alto = f
print("top face found by geometry:", alto is not None, "| z mm", round(alto.pointOnFace.z * 10, 3) if alto else None)
spigoli = adsk.core.ObjectCollection.create()
for e in alto.edges:
    spigoli.add(e)
inp = r.features.filletFeatures.createInput()
inp.edgeSetInputs.addConstantRadiusEdgeSet(spigoli, adsk.core.ValueInput.createByString("2 mm"), True)
fil = r.features.filletFeatures.add(inp)
fil.name = "RAC_alto"
v = b.volume * 1000
print("edges filleted:", spigoli.count, "| volume mm3", round(v, 3))
```

### attribute on a consumed edge: parent None
Recorded output: `["edge attributes: 1 | parent: None"]`
```python
a = d.findAttributes("skill-fusion", "spigolo")
print("edge attributes:", len(a), "| parent:", (a[0].parent.objectType if a and a[0].parent else None))
```

⚠️ `findEntityByToken` (script 2) creates a ghost undo step: prefer names and attributes.
