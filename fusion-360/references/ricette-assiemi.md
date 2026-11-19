# Recipes: components, joints, materials, interferences

> Recipes tested on Fusion (Nov. 2026), each with the measured result.

**How to use them**: each recipe shows the API call that **works** (tested, with the measured result). The tests use shortcuts (`rett`, `blocco`: rectangles **without constraints**, dimensions as numbers): in a real model sketches are fully constrained and dimensions are parameters (`ricette.md` §2–§3, `metodo.md`). API coordinates are in **cm**.

The functions `componente`, `faccia`, `angolo_z` and `tras` of the header below create a component with a block and measure the
transforms.

Index: Header · Tested recipes · Does not work this way

## Header

**Simplified** header used by these scripts (names and helper functions already defined; the real one of the skill's scripts is in
`ricette.md` §1):
```python
import adsk.core, adsk.fusion, math, json
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
def vol(b): return round(b.volume * 1000, 4)
def out(**k): print('RIS' + json.dumps(k))
def componente(nome, x0, y0, z0, x1, y1, z1):
    occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    c = occ.component; c.name = nome
    pi = c.constructionPlanes.createInput(); pi.setByOffset(c.xYConstructionPlane, S(f"{z0} mm")); pl = c.constructionPlanes.add(pi)
    sk = c.sketches.add(pl); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(x0/10, y0/10, 0), P(x1/10, y1/10, 0))
    e = c.features.extrudeFeatures.addSimple(sk.profiles.item(0), S(f"{z1 - z0} mm"), OP.NewBodyFeatureOperation)
    return occ, e
def faccia(e, alto):
    return e.endFaces.item(0) if alto else e.startFaces.item(0)
def angolo_z(occ):
    m = occ.transform2; x = adsk.core.Vector3D.create(1, 0, 0); x.transformBy(m)
    return round(math.degrees(math.atan2(x.y, x.x)), 4)
def tras(occ):
    return [round(v * 10, 4) for v in occ.transform2.translation.asArray()]
```

## Tested recipes

### rotante_45_e_limiti
Recorded result: `{"interferenze_base_braccio": 0, "angolo_iniziale": 0.0, "angolo_dopo_45": 45.0, "angolo_dopo_attivazione_limiti": 0.0, "angolo_chiesto_60": 60.0, "valore_chiesto_120_letto": 60.0, "errore_oltre_limite": null, "angolo_reale_dopo_120": 60.0, "tipo": "RevoluteJointMotion"}`
```python
base, eb = componente("Base", 0, 0, 0, 40, 40, 10)
braccio, ea = componente("Braccio", 0, 15, 10, 40, 25, 15)
base.isGrounded = True
g0 = adsk.fusion.JointGeometry.createByPlanarFace(faccia(eb, True).createForAssemblyContext(base), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
g1 = adsk.fusion.JointGeometry.createByPlanarFace(faccia(ea, False).createForAssemblyContext(braccio), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
ji = r.joints.createInput(g1, g0)
ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
ji.isFlipped = True  # without it: the part flips inside the base (verified)
j = r.joints.add(ji); j.name = "GIUNTO_rotante"
mo = j.jointMotion
a0 = angolo_z(braccio)
mo.rotationValue = math.radians(45)
a45 = angolo_z(braccio)
lim = mo.rotationLimits
lim.isMinimumValueEnabled = True; lim.minimumValue = 0
lim.isMaximumValueEnabled = True; lim.maximumValue = math.radians(90)
dopo_limiti = angolo_z(braccio)
mo.rotationValue = math.radians(60); dentro_60 = angolo_z(braccio)
try:
    mo.rotationValue = math.radians(120); oltre = round(math.degrees(mo.rotationValue), 4); errore = None
except Exception as ex:
    oltre = None; errore = str(ex)[-120:]
oc = adsk.core.ObjectCollection.create(); oc.add(base); oc.add(braccio)
out(interferenze_base_braccio=d.analyzeInterference(d.createInterferenceInput(oc)).count, angolo_iniziale=a0, angolo_dopo_45=a45, angolo_dopo_attivazione_limiti=dopo_limiti, angolo_chiesto_60=dentro_60, valore_chiesto_120_letto=oltre, errore_oltre_limite=errore, angolo_reale_dopo_120=angolo_z(braccio), tipo=j.jointMotion.objectType.split("::")[-1])
```

### scorrevole_10_e_limiti
Recorded result: `{"interferenze_guida_carrello": 0, "posizione_dopo_unione": [20.0, 0.0, 0.0], "posizione_dopo_10mm": [30.0, 0.0, 0.0], "spostamento_x": 10.0, "valore_chiesto_30_letto": 0.0, "errore_oltre_limite": null, "posizione_dopo_30": [20.0, 0.0, 0.0]}`
```python
base, eb = componente("Guida", 0, 0, 0, 60, 20, 10)
carro, ec = componente("Carrello", 0, 0, 10, 20, 20, 20)
base.isGrounded = True
g0 = adsk.fusion.JointGeometry.createByPlanarFace(faccia(eb, True).createForAssemblyContext(base), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
g1 = adsk.fusion.JointGeometry.createByPlanarFace(faccia(ec, False).createForAssemblyContext(carro), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
ji = r.joints.createInput(g1, g0)
ji.setAsSliderJointMotion(adsk.fusion.JointDirections.XAxisJointDirection)
ji.isFlipped = True  # without it: carriage inside the rail, interference 4000 mm3 (verified)
j = r.joints.add(ji)
mo = j.jointMotion
t0 = tras(carro)
mo.slideValue = 1.0
t10 = tras(carro)
lim = mo.slideLimits
lim.isMinimumValueEnabled = True; lim.minimumValue = 0
lim.isMaximumValueEnabled = True; lim.maximumValue = 2.0
try:
    mo.slideValue = 3.0; oltre = round(mo.slideValue * 10, 4); errore = None
except Exception as ex:
    oltre = None; errore = str(ex)[-120:]
oc = adsk.core.ObjectCollection.create(); oc.add(base); oc.add(carro)
out(interferenze_guida_carrello=d.analyzeInterference(d.createInterferenceInput(oc)).count, posizione_dopo_unione=t0, posizione_dopo_10mm=t10, spostamento_x=round(t10[0] - t0[0], 4), valore_chiesto_30_letto=oltre, errore_oltre_limite=errore, posizione_dopo_30=tras(carro))
```

### gruppo_rigido_e_come_costruito
Recorded result: `{"gruppo_rigido": 2, "giunto_come_costruito": "RigidJointMotion", "giunti_come_costruiti": 1}`
```python
a, ea = componente("A", 0, 0, 0, 10, 10, 10)
b, eb2 = componente("B", 20, 0, 0, 30, 10, 10)
c, ec = componente("C", 40, 0, 0, 50, 10, 10)
oc = adsk.core.ObjectCollection.create(); oc.add(a); oc.add(b)
rg = r.rigidGroups.add(oc, True)
abj = r.asBuiltJoints.add(r.asBuiltJoints.createInput(b, c, None))
out(gruppo_rigido=rg.occurrences.count, giunto_come_costruito=abj.jointMotion.objectType.split("::")[-1], giunti_come_costruiti=r.asBuiltJoints.count)
```

### interferenza_fra_componenti
Recorded result: `{"interferenze": 1, "volumi": [1000.0]}`
```python
a, ea = componente("P1", 0, 0, 0, 20, 20, 10)
b, eb2 = componente("P2", 15, 0, 0, 35, 20, 10)
oc = adsk.core.ObjectCollection.create(); oc.add(a); oc.add(b)
ris = d.analyzeInterference(d.createInterferenceInput(oc))
out(interferenze=ris.count, volumi=[round(x.interferenceBody.volume * 1000, 4) for x in ris])
```

### materiale_e_massa
Recorded result: `{"acciaio": "Acciaio", "acciaio_id": "PrismMaterial-018", "densita_kg_m3": 7850.0, "massa_g": 31.4, "volume_mm3": 4000.0, "abs_nome": "Plastica ABS", "abs_id": "PrismMaterial-022", "abs_densita": 1060.0, "abs_massa_g": 4.24}`
```python
lib = max(app.materialLibraries, key=lambda l: l.materials.count)
acc = lib.materials.itemById("PrismMaterial-018")
abs_ = [lib.materials.itemById("PrismMaterial-022")]  # «Plastica ABS» (localized name = ABS Plastic): by code
occ, e = componente("Pezzo", 0, 0, 0, 20, 20, 10)
b = e.bodies.item(0)
def rho(m):
    for p in m.materialProperties:
        if p.id == "structural_Density": return p.value
b.material = acc
pp = b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.HighCalculationAccuracy)
uscita = {"acciaio": acc.name, "acciaio_id": acc.id, "densita_kg_m3": rho(acc), "massa_g": round(pp.mass * 1000, 4), "volume_mm3": round(b.volume * 1000, 4)}
if abs_:
    b.material = abs_[0]
    uscita.update(abs_nome=abs_[0].name, abs_id=abs_[0].id, abs_densita=rho(abs_[0]), abs_massa_g=round(b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.HighCalculationAccuracy).mass * 1000, 4))
out(**uscita)
```

### visibilita_e_isolamento
Recorded result: `{"nascosto_isVisible": false, "isolato_b": true, "a_visibile_mentre_b_isolato": false, "dopo": true, "opacita": 1.0}`
```python
a, ea = componente("V1", 0, 0, 0, 10, 10, 10)
b, eb2 = componente("V2", 20, 0, 0, 30, 10, 10)
a.isLightBulbOn = False
vis_a = a.isVisible
a.isLightBulbOn = True
b.isIsolated = True
iso = (b.isIsolated, a.isVisible)
b.isIsolated = False
out(nascosto_isVisible=vis_a, isolato_b=iso[0], a_visibile_mentre_b_isolato=iso[1], dopo=a.isVisible, opacita=round(a.visibleOpacity, 3))
```

### scorrevole_senza_isFlipped
Recorded result: `{"carrello_z_mm": [0.0, 10.0], "interferenza_mm3": [4000.0]}`
```python
base, eb = componente("Guida", 0, 0, 0, 60, 20, 10)
carro, ec = componente("Carrello", 0, 0, 10, 20, 20, 20)
base.isGrounded = True
g0 = adsk.fusion.JointGeometry.createByPlanarFace(faccia(eb, True).createForAssemblyContext(base), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
g1 = adsk.fusion.JointGeometry.createByPlanarFace(faccia(ec, False).createForAssemblyContext(carro), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
ji = r.joints.createInput(g1, g0); ji.setAsSliderJointMotion(adsk.fusion.JointDirections.XAxisJointDirection)
r.joints.add(ji)
bc = carro.bRepBodies.item(0).boundingBox
oc = adsk.core.ObjectCollection.create(); oc.add(base); oc.add(carro)
ris = d.analyzeInterference(d.createInterferenceInput(oc))
out(carrello_z_mm=[round(bc.minPoint.z * 10, 4), round(bc.maxPoint.z * 10, 4)], interferenza_mm3=[round(x.interferenceBody.volume * 1000, 4) for x in ris])
```

### ingombro_occorrenza
Recorded result: `{"occorrenza": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "corpo": [0.0, 0.0, 0.0, 20.0, 10.0, 5.0]}`
```python
occ, e = componente("Q", 0, 0, 0, 20, 10, 5)
bo, bb = occ.boundingBox, occ.bRepBodies.item(0).boundingBox
out(occorrenza=[round(v * 10, 4) for v in bo.minPoint.asArray() + bo.maxPoint.asArray()], corpo=[round(v * 10, 4) for v in bb.minPoint.asArray() + bb.maxPoint.asArray()])
```

### componente_esterno_dal_cloud
Requires a file in the cloud (with the Personal license there are 10 slots): ask permission. Recorded result: `{"nome": "<file name> v1", "referenziato": true, "volume_mm3": 13727.876}`
```python
ID_FILE = "<id of the file in the cloud>"   # dataFile.id of the design to insert: replace it
df = app.data.findFileById(ID_FILE)
occ = r.occurrences.addByInsert(df, adsk.core.Matrix3D.create(), True)
out(nome=occ.component.name, referenziato=occ.isReferencedComponent, volume_mm3=round(sum(b.volume for b in occ.bRepBodies) * 1000, 3))
```

## Does not work this way

(none)

