# Ricette: superfici, forme libere (T-spline), lamiera

> Ricette provate su Fusion (nov. 2026), ognuna con il risultato misurato.

**Come usarle**: ogni ricetta mostra la chiamata all'API che **funziona** (provata, col risultato misurato). Le prove usano scorciatoie (`rett`, `blocco`: rettangoli **senza vincoli**, misure a numero): in un modello vero gli schizzi si vincolano completamente e le misure sono parametri (`ricette.md` §2–§3, `metodo.md`). Le coordinate dell'API sono in **cm**.

Lamiera: le regole hanno nomi tradotti → sceglile per proprietà; con la licenza Personal (la più comune per uso personale) non ci sono giunzione per piega e chiusure in sovrapposizione.

Indice: Intestazione · Superfici · Forme libere · Lamiera (sviluppo e DXF)

## Intestazione

Intestazione **semplificata** usata da questi script (quella vera degli script della skill è in `ricette.md` §1):
```python
import adsk.core, adsk.fusion, math, json, os
app = adsk.core.Application.get()
d = adsk.fusion.Design.cast(app.activeProduct)
r = d.rootComponent
F = r.features
P = adsk.core.Point3D.create
S = adsk.core.ValueInput.createByString
OP = adsk.fusion.FeatureOperations
def rett(x0, y0, x1, y1, piano=None):
    sk = r.sketches.add(piano or r.xYConstructionPlane)
    sk.sketchCurves.sketchLines.addTwoPointRectangle(P(x0/10, y0/10, 0), P(x1/10, y1/10, 0)); return sk
def blocco(x0, y0, x1, y1, h, op=OP.NewBodyFeatureOperation):
    return F.extrudeFeatures.addSimple(rett(x0, y0, x1, y1).profiles.item(0), S(f'{h} mm'), op)
def vol(b): return round(b.volume * 1000, 4)          # mm³
def area(b): return round(b.area * 100, 4)            # mm², area di tutte le facce del corpo
def out(**k): print('RIS' + json.dumps(k))
CARTELLA = os.path.join(os.path.expanduser("~"), "prove-fusion")   # dove scrivere i file (DXF): scegline una tua
```

## Superfici

### 01_estrusione_superficie
Atteso (calcolato prima): `{"area": 200, "solido": false}`  
Risultato registrato: `{"area": 200.0, "solido": false}`
```python
sk = r.sketches.add(r.xYConstructionPlane); ln = sk.sketchCurves.sketchLines.addByTwoPoints(P(0, 0, 0), P(2, 0, 0))
i = F.extrudeFeatures.createInput(r.createOpenProfile(ln, False), OP.NewBodyFeatureOperation); i.isSolid = False
i.setDistanceExtent(False, S("10 mm")); b = F.extrudeFeatures.add(i).bodies.item(0)
out(area=area(b), solido=b.isSolid)
```

### 02_rivoluzione_superficie
Atteso (calcolato prima): `{"area": 628.3185, "solido": false}`  
Risultato registrato: `{"area": 628.3185, "solido": false}`
```python
sk = r.sketches.add(r.xZConstructionPlane); ln = sk.sketchCurves.sketchLines.addByTwoPoints(P(1, 0, 0), P(1, -1, 0))
i = F.revolveFeatures.createInput(r.createOpenProfile(ln, False), r.zConstructionAxis, OP.NewBodyFeatureOperation); i.isSolid = False
i.setAngleExtent(False, S("360 deg")); b = F.revolveFeatures.add(i).bodies.item(0)
out(area=area(b), solido=b.isSolid)
```

### 03_sweep_superficie
Atteso (calcolato prima): `{"area": 628.3185, "solido": false}`  
Risultato registrato: `{"area": 628.3185, "solido": false}`
```python
sp = r.sketches.add(r.yZConstructionPlane); c = sp.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 0.2)
sl = r.sketches.add(r.xYConstructionPlane); ln = sl.sketchCurves.sketchLines.addByTwoPoints(P(0, 0, 0), P(5, 0, 0))
i = F.sweepFeatures.createInput(r.createOpenProfile(c, False), F.createPath(ln), OP.NewBodyFeatureOperation); i.isSolid = False
b = F.sweepFeatures.add(i).bodies.item(0)
out(area=area(b), solido=b.isSolid)
```

### 04_patch
Atteso (calcolato prima): `{"area": 314.1593, "solido": false}`  
Risultato registrato: `{"area": 314.1593, "solido": false}`
```python
sk = r.sketches.add(r.xYConstructionPlane); c = sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 1)
b = F.patchFeatures.add(F.patchFeatures.createInput(c, OP.NewBodyFeatureOperation)).bodies.item(0)
out(area=area(b), solido=b.isSolid)
```

### 05_ispessisci
Atteso (calcolato prima): `{"v": 800, "solido": true}`  
Risultato registrato: `{"v": 800.0, "solido": true, "corpi": 2}`
```python
sk = rett(0, 0, 20, 20)
p = F.patchFeatures.add(F.patchFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation))
fc = adsk.core.ObjectCollection.create(); fc.add(p.bodies.item(0).faces.item(0))
t = F.thickenFeatures.add(F.thickenFeatures.createInput(fc, S("2 mm"), False, OP.NewBodyFeatureOperation))
b = t.bodies.item(0)
out(v=vol(b), solido=b.isSolid, corpi=r.bRepBodies.count)
```

### 06_cuci
Atteso (calcolato prima): `{"corpi": 1, "v": 4000, "solido": true}`  
Risultato registrato: `{"corpi": 1, "v": 4000.0, "solido": true}`
```python
sk = rett(0, 0, 20, 20)
curve = adsk.core.ObjectCollection.create()
for l in sk.sketchCurves.sketchLines: curve.add(l)
i = F.extrudeFeatures.createInput(r.createOpenProfile(curve, True), OP.NewBodyFeatureOperation); i.isSolid = False
i.setDistanceExtent(False, S("10 mm")); pareti = F.extrudeFeatures.add(i).bodies.item(0)
fondo = F.patchFeatures.add(F.patchFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation)).bodies.item(0)
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("10 mm")); pl = r.constructionPlanes.add(pi)
coper = F.patchFeatures.add(F.patchFeatures.createInput(rett(0, 0, 20, 20, pl).profiles.item(0), OP.NewBodyFeatureOperation)).bodies.item(0)
print("aree prima", area(pareti), area(fondo), area(coper))
sup = adsk.core.ObjectCollection.create()
for b in (pareti, fondo, coper): sup.add(b)
si = F.stitchFeatures.createInput(sup, S("0.01 mm"), OP.NewBodyFeatureOperation)
st = F.stitchFeatures.add(si)
b = r.bRepBodies.item(0)
out(corpi=r.bRepBodies.count, v=vol(b), solido=b.isSolid)
```

## Forme libere

### Definizioni usate da queste ricette
```python
AX = adsk.core.Vector3D.create(1, 0, 0)
AY = adsk.core.Vector3D.create(0, 1, 0)
def forma():
    ff = F.formFeatures.add(); ff.startEdit(); return ff
def bb_mm(b):
    bb = b.boundingBox; return [round((bb.maxPoint.x-bb.minPoint.x)*10,3), round((bb.maxPoint.y-bb.minPoint.y)*10,3), round((bb.maxPoint.z-bb.minPoint.z)*10,3), round(bb.maxPoint.z*10,3)]
```

### 01_sfera_tspline
Risultato registrato: `{"v": 4182.5805, "v_sfera": 4188.7902, "solido": true, "facce_ts": 64}`
```python
ff = forma(); tb = ff.tSplineBodies
si = tb.createSphereInput(P(0, 0, 0), AX, AY, 1.0); t = tb.addByShapeInput(si); ff.finishEdit()
b = t.bRepBody
out(v=vol(b), v_sfera=round(4/3*math.pi*10**3, 4), solido=b.isSolid, facce_ts=t.faces.count)
```

### 02_quadball
Risultato registrato: `{"v": 4173.5585, "v_sfera": 4188.7902, "solido": true, "facce_ts": 24}`
```python
ff = forma(); tb = ff.tSplineBodies
qi = tb.createQuadballInput(P(0, 0, 0), AX, AY, 1.0); t = tb.addByShapeInput(qi); ff.finishEdit()
b = t.bRepBody
out(v=vol(b), v_sfera=round(4/3*math.pi*10**3, 4), solido=b.isSolid, facce_ts=t.faces.count)
```

### 03_scatola_liscia_e_spigoli_vivi
Risultato registrato: `{"v_liscia": 39373.3273, "v_spigoli_vivi": 43750.0, "v_scatola": 43750, "dim_liscia": [50.0, 35.0, 25.0, 25.0], "spigoli": 108}`
```python
ff = forma(); tb = ff.tSplineBodies
bi = tb.createBoxInput(P(0, 0, 0), AX, AY, 5.0, 3.5, 2.5)
bi.xFaceCount = 3; bi.yFaceCount = 3; bi.zFaceCount = 3
t = tb.addByShapeInput(bi); ff.finishEdit()
v_liscia = vol(t.bRepBody); dim_liscia = bb_mm(t.bRepBody)
ff.startEdit()
for e in t.edges:
    e.isCreased = True
ff.finishEdit()
out(v_liscia=v_liscia, v_spigoli_vivi=vol(t.bRepBody), v_scatola=50*35*25, dim_liscia=dim_liscia, spigoli=t.edges.count)
```

### 04_sposta_faccia
Risultato registrato: `{"z_max_prima": 25.0, "z_max_dopo": 34.184}`
```python
ff = forma(); tb = ff.tSplineBodies
bi = tb.createBoxInput(P(0, 0, 0), AX, AY, 5.0, 3.5, 2.5)
bi.xFaceCount = 3; bi.yFaceCount = 3; bi.zFaceCount = 3
t = tb.addByShapeInput(bi); ff.finishEdit(); prima = bb_mm(t.bRepBody)
ff.startEdit()
alto = max(t.faces, key=lambda f: f.boundingBox.maxPoint.z + f.boundingBox.minPoint.z)
m = adsk.core.Matrix3D.create(); m.translation = adsk.core.Vector3D.create(0, 0, 1.0)
alto.transform(m); ff.finishEdit()
out(z_max_prima=prima[3], z_max_dopo=bb_mm(t.bRepBody)[3])
```

### 05_tsm_andata_ritorno
Risultato registrato: `{"caratteri_tsm": 15718, "facce": [64, 64], "volumi": [4182.5805, 4182.5805]}`
```python
ff = forma(); tb = ff.tSplineBodies
t = tb.addByShapeInput(tb.createSphereInput(P(0, 0, 0), AX, AY, 1.0))
desc = t.getTSMDescription()
t2 = tb.addByTSMDescription(desc); ff.finishEdit()
out(caratteri_tsm=len(desc), facce=[t.faces.count, t2.faces.count], volumi=[vol(t.bRepBody), vol(t2.bRepBody)])
```

### 06_foro_su_corpo_tspline
Risultato registrato: `{"v_prima": 34447.1375, "v_dopo": 33740.4301, "corpi": 1}`
```python
ff = forma(); tb = ff.tSplineBodies
bi = tb.createBoxInput(P(-2.5, -1.75, 0), AX, AY, 5.0, 3.5, 2.5)
t = tb.addByShapeInput(bi); ff.finishEdit()
b = t.bRepBody; v0 = vol(b)
sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 0.3)
i = F.extrudeFeatures.createInput(sk.profiles.item(0), OP.CutFeatureOperation); i.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
F.extrudeFeatures.add(i)
corpi = [x for x in r.bRepBodies]
out(v_prima=v0, v_dopo=vol(corpi[0]), corpi=len(corpi))
```

## Lamiera (sviluppo e DXF)

### REGOLE
Risultato registrato: `{"regole": [["Acciaio (mm)", 2.5, "Thickness", 2.5, 0.44], ["Acciaio inossidabile (mm)", 2.5, "Thickness", 2.5, 0.44], ["Alluminio (mm)", 2.0, "Thickness", 2.0, 0.44], ["Acciaio (in)", 2.54, "Thickness", 2.54, 0.44], ["Acciaio inossidabile (in)", 2.54, "Thickness", 2.54, 0.44], ["Alluminio (in)", 2.032, "Thickness", 2.032, 0.44]]}`
```python
lib = d.librarySheetMetalRules
out(regole=[(x.name, round(x.thickness.value*10, 4), x.bendRadius.expression, round(x.bendRadius.value*10, 4), x.kFactor) for x in lib])
```

### FLANGIA
Risultato registrato: `{"t": 2.5, "r": 2.5, "K": 0.44, "lamiera": true, "z_spessore": 2.5, "v_base": 6000.0, "dim_piegato": [60.0, 40.0, 20.0], "sviluppo": [55.6549, 60.0], "pieghe": [90.0, 90.0], "dxf_execute": true, "dxf_byte": 2806}`
```python
# i nomi delle regole sono TRADOTTI (Fusion in italiano: «Acciaio (mm)»): qui si prende la prima regola il cui nome finisce con «(mm)»
# (provato in italiano); per una regola precisa scegli per proprietà (thickness, kFactor), non per il nome intero
regola = [x for x in d.librarySheetMetalRules if x.name.endswith("(mm)")][0]
r.activeSheetMetalRule = regola
t, rb, K = regola.thickness.value * 10, regola.bendRadius.value * 10, regola.kFactor
sk = rett(0, 0, 60, 40)
fl = F.flangeFeatures
bf = fl.add(fl.createBaseFlangeInput([sk.profiles.item(0)]))
b = bf.bodies.item(0)
v_base = vol(b); lamiera = b.isSheetMetal
bb = b.boundingBox; z_spessore = round((bb.maxPoint.z - bb.minPoint.z) * 10, 4)
# flangia sul bordo lungo a y = 40 (spigolo della faccia sopra)
alto = max((f for f in b.faces if isinstance(f.geometry, adsk.core.Plane)), key=lambda f: f.pointOnFace.z)
spig = max((e for e in alto.edges), key=lambda e: (e.boundingBox.minPoint.y + e.boundingBox.maxPoint.y))
ei = fl.createEdgeFlangeInput([spig], S("20 mm"))
ei.bendPositionType = adsk.fusion.BendPositionTypes.InsideBendPositionType
ei.angle = S("90 deg")
ef = fl.add(ei)
bb = b.boundingBox
dim = [round((bb.maxPoint.x-bb.minPoint.x)*10, 4), round((bb.maxPoint.y-bb.minPoint.y)*10, 4), round((bb.maxPoint.z-bb.minPoint.z)*10, 4)]
fp = r.createFlatPattern(min((f for f in b.faces if isinstance(f.geometry, adsk.core.Plane)), key=lambda f: f.pointOnFace.z))
fb = fp.flatBody.boundingBox
sv = sorted([round((fb.maxPoint.x-fb.minPoint.x)*10, 4), round((fb.maxPoint.y-fb.minPoint.y)*10, 4)])
pieghe = []
for e in fp.bendLinesBody.edges:
    ok, su, ang = fp.getBendInfo(e)
    if ok: pieghe.append(round(math.degrees(ang), 3))
f = os.path.join(CARTELLA, "sviluppo.dxf")
os.makedirs(CARTELLA, exist_ok=True)
o = d.exportManager.createDXFFlatPatternExportOptions(f, fp)
esito = d.exportManager.execute(o)
out(t=t, r=rb, K=K, lamiera=lamiera, z_spessore=z_spessore, v_base=v_base, dim_piegato=dim, sviluppo=sv, pieghe=pieghe,
    dxf_execute=esito, dxf_byte=os.path.getsize(f) if os.path.exists(f) else 0)
```

### CONVERTI
Risultato registrato: `{"lamiera": true, "v": 3750.0}`
```python
# i nomi delle regole sono TRADOTTI: qui la prima regola il cui nome finisce con «(mm)» (provato in italiano; vedi sopra)
regola = [x for x in d.librarySheetMetalRules if x.name.endswith("(mm)")][0]
e = blocco(0, 0, 50, 30, regola.thickness.value * 10)
b = e.bodies.item(0)
b.convertToSheetMetal(e.endFaces.item(0), regola)
out(lamiera=b.isSheetMetal, v=vol(b))
```

Controllo registrato dello sviluppo: `{"v_base_atteso": 6000.0, "sviluppo_atteso": [55.6549, 60], "dim_piegato_atteso": [60, 40, 20]}` (lunghezza sviluppata = (L − (r + t)) + (h − (r + t)) + π/2 (r + K·t)).

