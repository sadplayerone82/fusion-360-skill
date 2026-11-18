# Ricette: schizzi, vincoli, piani e assi, ritrovare le entità

> Ricette provate su Fusion (nov. 2026), ognuna con il risultato misurato.

**Come usarle**: ogni ricetta mostra la chiamata all'API che **funziona** (provata, col risultato misurato). Le prove usano scorciatoie (`rett`, `blocco`: rettangoli **senza vincoli**, misure a numero): in un modello vero gli schizzi si vincolano completamente e le misure sono parametri (`ricette.md` §2–§3, `metodo.md`). Le coordinate dell'API sono in **cm**.

Ogni schizzo va completamente vincolato (`isFullyConstrained`); l'API non aggiunge vincoli da sola.

Indice: Intestazione · Ricette provate · Non funziona così · Ritrovare schizzi, feature, facce fra uno script e l'altro

## Intestazione

Intestazione **semplificata** usata da questi script (nomi e funzioni d'aiuto già definiti; quella vera degli script della skill è in
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

## Ricette provate

### rettangolo_centrato
Uscita registrata: `["linee 4 | vincolato senza quote: False", "con 2 quote vincolato: False | vincoli creati da Fusion: []"]`
```python
sk = nuovo("SK_rett_centrato")
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(2, 1, 0))
print("linee", l.count, "| vincolato senza quote:", sk.isFullyConstrained)
dm = sk.sketchDimensions
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)).parameter.expression = "40 mm"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(2.5, 0, 0)).parameter.expression = "20 mm"
print("con 2 quote vincolato:", sk.isFullyConstrained, "| vincoli creati da Fusion:", [c.objectType.split('::')[-1] for c in sk.geometricConstraints])
```

### ricetta_rettangolo_centrato_vincolato
Uscita registrata: `["RICETTA vincolato: True | lati mm [40.0, 20.0, 40.0, 20.0] | centro mm [0.0, 0.0]"]`
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
print("RICETTA vincolato:", sk.isFullyConstrained, "| lati mm", [round(x.length * 10, 4) for x in l], "| centro mm", [round((l[0].startSketchPoint.geometry.x + l[2].startSketchPoint.geometry.x) * 5, 4), round((l[0].startSketchPoint.geometry.y + l[2].startSketchPoint.geometry.y) * 5, 4)])
```

### asola
Uscita registrata: `["asola: oggetti <vettore di oggetti dell'API> | curve 5 | profili 1 | vincolato False"]`
```python
sk = nuovo("SK_asola")
res = sk.addCenterToCenterSlot(P(0, 0, 0), P(3, 0, 0), S("8 mm"))
print("asola: oggetti", res.count if hasattr(res, 'count') else res, "| curve", sk.sketchCurves.count, "| profili", sk.profiles.count, "| vincolato", sk.isFullyConstrained)
```

### poligono_spline_testo
Uscita registrata: `["spline: punti di passaggio 4 | lunghezza mm 46.149", "testo: 'Ciao Fusion' | altezza mm 5.0", "funzioni poligono in GeometricConstraints: True"]`
```python
sk = nuovo("SK_varie")
g = sk.geometricConstraints
pts = adsk.core.ObjectCollection.create()
for x, y in ((0, 0), (1, 1), (2, 0), (3, 1)): pts.add(P(x, y, 0))
sp = sk.sketchCurves.sketchFittedSplines.add(pts)
print("spline: punti di passaggio", sp.fitPoints.count, "| lunghezza mm", round(sp.length * 10, 3))
ti = sk.sketchTexts.createInput2("Ciao Fusion", 0.5)
ti.setAsMultiLine(P(0, -2, 0), P(4, -1, 0), adsk.core.HorizontalAlignments.LeftHorizontalAlignment, adsk.core.VerticalAlignments.TopVerticalAlignment, 0)
t = sk.sketchTexts.add(ti)
print("testo:", repr(t.text), "| altezza mm", round(t.height * 10, 3))
print("funzioni poligono in GeometricConstraints:", hasattr(g, "addPolygon"))
```

### serie_nello_schizzo
Uscita registrata: `["serie circolare: cerchi totali 6", "dopo serie rettangolare 3x2: cerchi totali 12 (attesi 6 + 6 = 12)"]`
```python
sk = nuovo("SK_serie")
c = sk.sketchCurves.sketchCircles.addByCenterRadius(P(2, 0, 0), 0.3)
ent = adsk.core.ObjectCollection.create(); ent.add(c)
g = sk.geometricConstraints
ci = g.createCircularPatternInput([c], sk.originPoint)
ci.quantity = S("6")
ci.totalAngle = S("360 deg")
pat = g.addCircularPattern(ci)
print("serie circolare: cerchi totali", sk.sketchCurves.sketchCircles.count)
c2 = sk.sketchCurves.sketchCircles.addByCenterRadius(P(5, 0, 0), 0.2)
ri = g.createRectangularPatternInput([c2], adsk.fusion.PatternDistanceType.SpacingPatternDistanceType)
ri.setDirectionOne(sk.sketchCurves.sketchLines.addByTwoPoints(P(5, -1, 0), P(6, -1, 0)), S("3"), S("10 mm"))
ri.setDirectionTwo(sk.sketchCurves.sketchLines.addByTwoPoints(P(5, -1, 0), P(5, 0, 0)), S("2"), S("10 mm"))
g.addRectangularPattern(ri)
print("dopo serie rettangolare 3x2: cerchi totali", sk.sketchCurves.sketchCircles.count, "(attesi 6 + 6 = 12)")
```

### curva_intersezione
Uscita registrata: `["curve d'intersezione: 2 ['SketchEllipticalArc', 'SketchLine']"]`
```python
sk = nuovo("SK_cil")
sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 1)
e = r.features.extrudeFeatures.addSimple(sk.profiles.item(0), S("30 mm"), NB); e.name = "EST_cil"
pi = r.constructionPlanes.createInput(); pi.setByAngle(r.xAxis if hasattr(r, 'xAxis') else r.xConstructionAxis, S("30 deg"), r.xYConstructionPlane)
pt = r.constructionPlanes.add(pi); pt.name = "PIANO_inclinato"
s2 = nuovo("SK_intersezione", pt)
curve = s2.intersectWithSketchPlane([e.bodies.item(0)])
print("curve d'intersezione:", len(curve), [x.objectType.split('::')[-1] for x in curve])
```

### costruzione
Uscita registrata: `["costruzione True | mezzeria True | profili (la costruzione non crea profili) 2"]`
```python
sk = nuovo("SK_costruzione")
m = sk.sketchCurves.sketchLines.addByTwoPoints(P(-2, 0, 0), P(2, 0, 0)); m.isConstruction = True
c = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, -2, 0), P(0, 2, 0)); c.isCenterLine = True
sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 1)
print("costruzione", m.isConstruction, "| mezzeria", c.isCenterLine, "| profili (la costruzione non crea profili)", sk.profiles.count)
```

### parametri
Uscita registrata: `["quote: d18 = lato_d1 25.0 mm | d19 = lato_d1 * 2 50.0 mm | vincolato False"]`
```python
d.userParameters.add("lato_d1", S("25 mm"), "mm", "lato del quadrato")
sk = nuovo("SK_param")
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(1, 1, 0))
dm = sk.sketchDimensions
a = dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)); a.parameter.expression = "lato_d1"
b = dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(1.5, 0, 0)); b.parameter.expression = "lato_d1 * 2"
print("quote:", a.parameter.name, "=", a.parameter.expression, round(a.parameter.value * 10, 3), "mm |", b.parameter.name, "=", b.parameter.expression, round(b.parameter.value * 10, 3), "mm | vincolato", sk.isFullyConstrained)
```

### vincoli_avanzati
Uscita registrata: `["simmetria + uguale: x estremi mm -10.0 10.0 | lunghezze mm 10.0 10.0", "curvatura (smooth G2) linea-spline: True SmoothConstraint", "tangente arco-linea: ok"]`
```python
sk = nuovo("SK_vincoli")
g = sk.geometricConstraints; L = sk.sketchCurves.sketchLines
asse = L.addByTwoPoints(P(0, -2, 0), P(0, 2, 0)); asse.isCenterLine = True
a = L.addByTwoPoints(P(-1, 0, 0), P(-1, 1, 0)); b = L.addByTwoPoints(P(1.2, 0, 0), P(1.2, 1.1, 0))
g.addSymmetry(a, b, asse)
g.addEqual(a, b)
print("simmetria + uguale: x estremi mm", round(a.startSketchPoint.geometry.x * 10, 3), round(b.startSketchPoint.geometry.x * 10, 3), "| lunghezze mm", round(a.length * 10, 3), round(b.length * 10, 3))
li = L.addByTwoPoints(P(3, 0, 0), P(4, 0, 0))
# la spline PARTE dal punto della linea (con un punto nuovo nella stessa posizione la coincidenza fallisce: «failed to create offset»)
pts = adsk.core.ObjectCollection.create()
pts.add(li.endSketchPoint)
for x, y in ((5, 0.5), (6, 0)): pts.add(P(x, y, 0))
sp = sk.sketchCurves.sketchFittedSplines.add(pts)
sm = g.addSmooth(li, sp)
print("curvatura (smooth G2) linea-spline:", sm is not None, sm.objectType.split('::')[-1] if sm else None)
ar = sk.sketchCurves.sketchArcs.addByCenterStartSweep(P(4, 2, 0), P(5, 2, 0), math.pi / 2)
lt = L.addByTwoPoints(ar.endSketchPoint, P(3, 4, 0))
g.addTangent(ar, lt)
print("tangente arco-linea: ok")
```

### entita_3d
Uscita registrata: `["linea 3D nello schizzo: z fine (mondo) mm 10.0 | lunghezza mm 17.321 (attesa 17.321 ) | isPlanar schizzo? True"]`
```python
sk = nuovo("SK_3D")
l = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, 0, 0), P(1, 1, 1))
s, e = l.startSketchPoint.worldGeometry, l.endSketchPoint.worldGeometry
print("linea 3D nello schizzo: z fine (mondo) mm", round(e.z * 10, 3), "| lunghezza mm", round(l.length * 10, 3), "(attesa", round(3 ** 0.5 * 10, 3), ") | isPlanar schizzo?", getattr(sk, 'isFullyConstrained', None) is not None)
```

### piani_e_assi
Uscita registrata (3 delle 5 righe stampate): `["piano lungo il percorso a metà: x mm 30.0 (atteso 30)", "asse da due piani: direzione [0.0, 0.0, -1.0]", "punto da tre piani: [0.0, 0.0, 0.0]"]`
```python
sk = nuovo("SK_blocco")
sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(4, 2, 0))
e = r.features.extrudeFeatures.addSimple(sk.profiles.item(0), S("10 mm"), NB)
cp = r.constructionPlanes
i = cp.createInput(); i.setByOffset(r.xYConstructionPlane, S("15 mm")); p1 = cp.add(i)
i = cp.createInput(); i.setByTwoPlanes(e.startFaces.item(0), e.endFaces.item(0)); pm = cp.add(i)
print("piano offset z mm", round(p1.geometry.origin.z * 10, 3), "| piano mediano z mm", round(pm.geometry.origin.z * 10, 3), "(atteso 5)")
i = cp.createInput(); i.setByAngle(sk.sketchCurves.sketchLines.item(0), S("45 deg"), r.xYConstructionPlane); pa = cp.add(i)
n = pa.geometry.normal
print("piano a 45°: normale", round(n.x, 4), round(n.y, 4), round(n.z, 4))
sp = nuovo("SK_percorso")
lp = sp.sketchCurves.sketchLines.addByTwoPoints(P(0, 4, 0), P(6, 4, 0))
path = r.features.createPath(lp)
i = cp.createInput(); i.setByDistanceOnPath(path, adsk.core.ValueInput.createByReal(0.5)); pp = cp.add(i)
print("piano lungo il percorso a metà: x mm", round(pp.geometry.origin.x * 10, 3), "(atteso 30)")
ax = r.constructionAxes
ai = ax.createInput(); ai.setByTwoPlanes(r.xZConstructionPlane, r.yZConstructionPlane); a1 = ax.add(ai)
print("asse da due piani: direzione", [round(v, 4) for v in a1.geometry.direction.asArray()])
pt = r.constructionPoints
qi = pt.createInput(); qi.setByThreePlanes(r.xYConstructionPlane, r.xZConstructionPlane, r.yZConstructionPlane); q = pt.add(qi)
print("punto da tre piani:", [round(v * 10, 3) for v in q.geometry.asArray()])
```

### extra_autoconstrain_offset
Uscita registrata: `["autoConstrain ERRORE: 3 : AutoConstrain is not available since user is restricted", "offset con ObjectCollection: ERRORE n::SketchCurve >,std::allocator< adsk::core::Ptr< adsk::fusion::SketchCurve > > > const &'", "offset parametrico 2 mm: curve 8 | profili 2"]`
```python
sk = nuovo("SK_auto")
l = sk.sketchCurves.sketchLines.addTwoPointRectangle(P(0, 0, 0), P(3, 2, 0))
dm = sk.sketchDimensions
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(1.5, -0.5, 0))
try:
    ai = sk.createAutoConstrainInput()
    print("autoConstrain input:", ai.objectType)
    res = sk.autoConstrain(ai)
    print("autoConstrain risultato:", res.objectType if res else None, "| vincolato", sk.isFullyConstrained)
except Exception as ex:
    print("autoConstrain ERRORE:", str(ex)[-150:])
curves = sk.findConnectedCurves(l[0])
try:
    sk.geometricConstraints.createOffsetInput(curves, S("2 mm")); print("offset con ObjectCollection: accettato")
except Exception as ex:
    print("offset con ObjectCollection: ERRORE", str(ex)[-90:])
oi = sk.geometricConstraints.createOffsetInput([c for c in curves], S("2 mm"))
off = sk.geometricConstraints.addOffset2(oi)
print("offset parametrico 2 mm: curve", sk.sketchCurves.count, "| profili", sk.profiles.count)
```

## Non funziona così

(nessuna)

## Ritrovare schizzi, feature, facce fra uno script e l'altro

Intestazione di questi script: `d`, `r`, `P` come sopra.

### dare nomi e attributi (script 1)
Uscita: i token del corpo e della faccia (stringhe lunghe, diverse a ogni prova) e il numero di facce di fine, inizio e laterali.
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

### ritrovare per nome, token, attributo (script 2, separato)
Uscita registrata: `["per token: 1 ['adsk::fusion::BRepBody']", "per token: 1 ['adsk::fusion::BRepFace']", "per attributo: 1 adsk::fusion::BRepFace | area mm2 800.0"]`
```python
b = r.bRepBodies.itemByName("Blocco")
print("corpo per nome:", b is not None, "| volume mm3", round(b.volume * 1000, 3) if b else None)
f = r.features.itemByName("EST_base")
print("feature per nome:", f is not None, f.objectType if f else None)
sk = r.sketches.itemByName("SK_base")
print("schizzo per nome:", sk is not None)
TOKEN = ["<token_corpo>", "<token_alto>"]   # i due token stampati dallo script 1
for t in TOKEN:
    trovati = d.findEntityByToken(t)
    print("per token:", len(trovati), [x.objectType for x in trovati])
a = d.findAttributes("skill-fusion", "faccia")
print("per attributo:", len(a), a[0].parent.objectType if a and a[0].parent else None, "| area mm2", round(a[0].parent.area * 100, 3) if a and a[0].parent else None)
```

### scegliere facce e spigoli per geometria e raccordarli
Uscita registrata: `["faccia in alto trovata per geometria: True | z mm 10.0", "spigoli raccordati: 4 | volume mm3 7900.059"]`
```python
b = r.bRepBodies.itemByName("Blocco")
alto = None
for f in b.faces:
    ok, n = f.evaluator.getNormalAtPoint(f.pointOnFace)
    if isinstance(f.geometry, adsk.core.Plane) and n.isParallelTo(adsk.core.Vector3D.create(0, 0, 1)) and n.z > 0:
        alto = f
print("faccia in alto trovata per geometria:", alto is not None, "| z mm", round(alto.pointOnFace.z * 10, 3) if alto else None)
spigoli = adsk.core.ObjectCollection.create()
for e in alto.edges:
    spigoli.add(e)
inp = r.features.filletFeatures.createInput()
inp.edgeSetInputs.addConstantRadiusEdgeSet(spigoli, adsk.core.ValueInput.createByString("2 mm"), True)
fil = r.features.filletFeatures.add(inp)
fil.name = "RAC_alto"
v = b.volume * 1000
print("spigoli raccordati:", spigoli.count, "| volume mm3", round(v, 3))
```

### attributo su uno spigolo consumato: parent None
Uscita registrata: `["attributi spigolo: 1 | parent: None"]`
```python
a = d.findAttributes("skill-fusion", "spigolo")
print("attributi spigolo:", len(a), "| parent:", (a[0].parent.objectType if a and a[0].parent else None))
```

⚠️ `findEntityByToken` (script 2) crea un passo di annullamento fantasma: preferisci nomi e attributi.

