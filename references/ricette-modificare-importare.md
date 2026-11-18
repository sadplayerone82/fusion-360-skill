# Ricette: modificare modelli esistenti, importare STEP/STL, testo, fori, gancio, ingranaggi

> Ricette provate su Fusion (nov. 2026), ognuna con il risultato misurato.

**Come usarle**: ogni ricetta mostra la chiamata all'API che **funziona** (provata, col risultato misurato). Le prove usano scorciatoie (`rett`, `blocco`: rettangoli **senza vincoli**, misure a numero): in un modello vero gli schizzi si vincolano completamente e le misure sono parametri (`ricette.md` §2–§3, `metodo.md`). Le coordinate dell'API sono in **cm**.

La modifica di un modello segue la ricetta ufficiale Autodesk: `rollTo(True)` → modifica → `timeline.moveToEnd()`.

Intestazione: la stessa, semplificata, di `ricette-solidi.md` (`d`, `r`, `F`, `P`, `S`, `OP`, `H`, `V`, `rett`, `blocco`, `vol`, `out`,
`math`); per un modello vero vale quella di `ricette.md` §1. Le ricette di modifica partono dalla staffa a L di `ricette-solidi.md`
(«staffa a L completa»).

**Indice** (file lungo: cerca la sezione, non leggerlo intero)
| Riga | Sezione | Quando |
|---|---|---|
| 20 | Modificare (timeline): leggere, cambiare una definizione, inserire a metà, spostare, riparare | modificare un modello con la storia |
| 124 | Importare: STEP, STL, mesh → solido, modifica diretta | partire da un file scaricato |
| 187 | Testo, fori svasati e lamati, gancio, ingranaggi | dettagli e parti tipiche |

## Modificare (timeline)

### leggi_timeline
Risultato registrato: `{"timeline": [[0, "SK_profilo", "Sketch", 0], [1, "EST_staffa", "ExtrudeFeature", 0], [2, "RAC_interno", "FilletFeature", 0], [3, "SK_fori", "Sketch", 0], [4, "TAGLIO_fori", "ExtrudeFeature", 0]], "volume": 7905.309, "parametri": ["lunghezza_base", "larghezza", "spessore_base", "altezza", "spessore_parete", "raggio", "diametro_foro", "distanza_foro", "interasse"]}`
```python
tl = [(o.index, o.name, o.entity.objectType.split("::")[-1] if o.entity else None, o.healthState) for o in d.timeline]
b = r.bRepBodies.item(0)
out(timeline=tl, volume=round(b.volume * 1000, 3), parametri=[p.name for p in d.userParameters])
```

### modifica_definizione
Risultato registrato: `{"volume_largo": 10564.623, "larghezza_y": 40.0, "volume_ripristinato": 7905.309}`
```python
b = r.bRepBodies.item(0)

e = r.features.itemByName("EST_staffa")
sd = adsk.fusion.SymmetricExtentDefinition.cast(e.extentOne)
e.timelineObject.rollTo(True)
sd.distance.expression = "larghezza + 10 mm"
d.timeline.moveToEnd()
bb = b.boundingBox; v1 = round(b.volume * 1000, 3); y1 = round((bb.maxPoint.y - bb.minPoint.y) * 10, 3)
e.timelineObject.rollTo(True); sd.distance.expression = "larghezza"; d.timeline.moveToEnd()
out(volume_largo=v1, larghezza_y=y1, volume_ripristinato=round(b.volume * 1000, 3))
```

### inserisci_a_meta
Risultato registrato: `{"volume": 7825.309, "indice_scarico": 3, "indice_raccordo": 4, "timeline": [[0, "SK_profilo", "Sketch", 0], [1, "EST_staffa", "ExtrudeFeature", 0], [2, "SK_scarico", "Sketch", 0], [3, "TAGLIO_scarico", "ExtrudeFeature", 0], [4, "RAC_interno", "FilletFeature", 0], [5, "SK_fori", "Sketch", 0], [6, "TAGLIO_fori", "ExtrudeFeature", 0]]}`
```python
b = r.bRepBodies.item(0)

f = r.features.itemByName("RAC_interno")
f.timelineObject.rollTo(True)
sk = r.sketches.add(r.xYConstructionPlane); sk.name = "SK_scarico"
sk.sketchCurves.sketchLines.addTwoPointRectangle(P(3.6, -1.5, 0), P(4.0, -1.0, 0))
ci = F.extrudeFeatures.createInput(sk.profiles.item(0), OP.CutFeatureOperation)
ci.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
c = F.extrudeFeatures.add(ci); c.name = "TAGLIO_scarico"
d.timeline.moveToEnd()
tl = [(o.index, o.name, o.entity.objectType.split("::")[-1] if o.entity else None, o.healthState) for o in d.timeline]
out(volume=round(b.volume * 1000, 3), indice_scarico=c.timelineObject.index, indice_raccordo=f.timelineObject.index, timeline=tl)
```

### sposta_feature
Risultato registrato: `{"metodi": ["canReorder", "reorder"], "puo": true, "mosso": true, "prima": [6, 4], "dopo": [5, 6], "volume": 7825.309, "timeline": [[0, "SK_profilo", "Sketch", 0], [1, "EST_staffa", "ExtrudeFeature", 0], [2, "SK_scarico", "Sketch", 0], [3, "TAGLIO_scarico", "ExtrudeFeature", 0], [4, "SK_fori", "Sketch", 0], [5, "TAGLIO_fori", "ExtrudeFeature", 0], [6, "RAC_interno", "FilletFeature", 0]]}`
```python
b = r.bRepBodies.item(0)

t = r.features.itemByName("TAGLIO_fori"); f = r.features.itemByName("RAC_interno")
prima = (t.timelineObject.index, f.timelineObject.index)
to = t.timelineObject
metodi = [m for m in dir(to) if "order" in m.lower()]
ok = to.canReorder(f.timelineObject.index) if hasattr(to, "canReorder") else None
mosso = to.reorder(f.timelineObject.index) if ok else None
tl = [(o.index, o.name, o.entity.objectType.split("::")[-1] if o.entity else None, o.healthState) for o in d.timeline]
out(metodi=metodi, puo=ok, mosso=mosso, prima=prima, dopo=(t.timelineObject.index, f.timelineObject.index), volume=round(b.volume * 1000, 3), timeline=tl)
```

### rompi
Risultato registrato: `{"timeline": [[0, "SK_profilo", "Sketch", 0], [1, "EST_staffa", "ExtrudeFeature", 0], [2, "SK_scarico", "Sketch", 0], [3, "TAGLIO_scarico", "ExtrudeFeature", 0], [4, "TAGLIO_fori", "ExtrudeFeature", 1], [5, "RAC_interno", "FilletFeature", 0]]}`
```python
r.sketches.itemByName("SK_fori").deleteMe()
tl = [(o.index, o.name, o.entity.objectType.split("::")[-1] if o.entity else None, o.healthState) for o in d.timeline]
out(timeline=tl)
```

### ripara
Risultato registrato: `{"volume": 7825.309, "profili": 2, "vincolato": true, "tentativi": {"ObjectCollection": "2 : InternalValidationError : curProfile", "lista": "ment 2 of type 'adsk::core::Ptr< adsk::core::Base > const &'", "un_profilo": "2 : InternalValidationError : curProfile", "rifatta": "ok"}, "timeline": [[0, "SK_profilo", "Sketch", 0], [1, "EST_staffa", "ExtrudeFeature", 0], [2, "SK_scarico", "Sketch", 0], [3 …`
```python
b = r.bRepBodies.item(0)

t = r.features.itemByName("TAGLIO_fori")
t.timelineObject.rollTo(True)
sf = r.sketches.add(r.xYConstructionPlane); sf.name = "SK_fori_nuovo"
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation; V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
o = sf.originPoint; dm = sf.sketchDimensions
c1 = sf.sketchCurves.sketchCircles.addByCenterRadius(P(2.8, 0.8, 0), 0.17)
c2 = sf.sketchCurves.sketchCircles.addByCenterRadius(P(2.8, -0.8, 0), 0.17)
lc = sf.sketchCurves.sketchLines.addByTwoPoints(c1.centerSketchPoint, c2.centerSketchPoint); lc.isConstruction = True
sf.geometricConstraints.addVertical(lc)
dm.addDiameterDimension(c1, P(3.3, 1.3, 0)).parameter.expression = "diametro_foro"
dm.addDiameterDimension(c2, P(3.3, -1.3, 0)).parameter.expression = "diametro_foro"
dm.addDistanceDimension(o, c1.centerSketchPoint, H, P(1.4, 1.4, 0)).parameter.expression = "lunghezza_base - distanza_foro"
dm.addDistanceDimension(o, c1.centerSketchPoint, V, P(3.5, 0.4, 0)).parameter.expression = "interasse / 2"
dm.addDistanceDimension(c1.centerSketchPoint, c2.centerSketchPoint, V, P(3.8, 0, 0)).parameter.expression = "interasse"
pr = adsk.core.ObjectCollection.create()
for p in sf.profiles:
    if abs(p.areaProperties().area - math.pi * 0.17 ** 2) < 1e-4: pr.add(p)
tentativi = {}
for nome, val in (("ObjectCollection", pr), ("lista", [x for x in pr]), ("un_profilo", pr.item(0))):
    try:
        t.profile = val; tentativi[nome] = "ok"; break
    except Exception as ex:
        tentativi[nome] = str(ex)[-60:]
if "ok" not in tentativi.values():
    # strada sicura: cancellare la feature rotta e rifarla dal nuovo schizzo (stesso nome)
    t.deleteMe()
    ci = F.extrudeFeatures.createInput(pr, OP.CutFeatureOperation)
    ci.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
    t = F.extrudeFeatures.add(ci); t.name = "TAGLIO_fori"; tentativi["rifatta"] = "ok"
d.timeline.moveToEnd()
tl = [(o.index, o.name, o.entity.objectType.split("::")[-1] if o.entity else None, o.healthState) for o in d.timeline]
out(volume=round(b.volume * 1000, 3), profili=pr.count, vincolato=sf.isFullyConstrained, tentativi=tentativi, timeline=tl)
```

## Importare

### step
Risultato registrato: `{"corpi": [["Corpo2", true, 500.0], ["Corpo1", true, 3717.257]], "componenti": 2, "timeline": 1}`
```python
im = app.importManager
FILE_STEP = "pezzi.step"   # percorso completo del file da importare (qui: due blocchi, 500 e 3 717,257 mm³)
o = im.createSTEPImportOptions(FILE_STEP); o.isViewFit = False
im.importToTarget(o, r)
corpi = [(b.name, b.isSolid, round(b.volume * 1000, 3)) for c in d.allComponents for b in c.bRepBodies]
out(corpi=sorted(corpi, key=lambda x: x[2]), componenti=d.allComponents.count, timeline=d.timeline.count)
```

### stl
Risultato registrato: `{"tipo": "MeshBody", "triangoli": 12, "ingombro": [20.0, 20.0, 10.0]}`
```python
FILE_STL = "cubo.stl"   # percorso completo del file da importare (qui: blocco 20 × 20 × 10)
mb = r.meshBodies.add(FILE_STL, adsk.fusion.MeshUnits.MillimeterMeshUnit)
m = mb.item(0) if hasattr(mb, "item") else mb
bb = m.boundingBox
out(tipo=m.objectType.split("::")[-1], triangoli=m.displayMesh.triangleCount if hasattr(m, "displayMesh") else None,
    ingombro=[round((bb.maxPoint.x - bb.minPoint.x) * 10, 3), round((bb.maxPoint.y - bb.minPoint.y) * 10, 3), round((bb.maxPoint.z - bb.minPoint.z) * 10, 3)])
```

### mesh_a_solido
Risultato registrato: `{"funzioni": ["meshCombineFaceGroupsFeatures", "meshCombineFeatures", "meshConvertFeatures", "meshGenerateFaceGroupsFeatures", "meshPlaneCutFeatures", "meshReduceFeatures", "meshRemeshFeatures", "meshRemoveFeatures", "meshRepairFeatures", "meshReverseNormalFeatures", "meshSeparateFeatures", "meshShellFeatures", "meshSmoothFeatures", "volumetricModelToMeshFeatures"], "input_firma": "createInput([m] …`
```python
m = r.meshBodies.item(r.meshBodies.count - 1)
nomi = [n for n in dir(F) if not n.startswith("_") and ("mesh" in n.lower() or "convert" in n.lower())]
ris = {"funzioni": nomi}
for n in nomi:
    if n == "meshConvertFeatures":
        coll = getattr(F, n)
        try:
            inp = coll.createInput([m])  # vuole una LISTA di MeshBody
            ris["input_firma"] = "createInput([m])"
            for k in dir(inp):
                if "method" in k.lower() or "resolution" in k.lower() or "operation" in k.lower(): ris.setdefault("opzioni", []).append(k)
            f = coll.add(inp)
            ris["corpi_creati"] = [(b.isSolid, round(b.volume * 1000, 3)) for b in f.bodies]
        except Exception as ex:
            ris["errore"] = str(ex)[-200:]
        break
out(**ris)
```

### modifica_diretta
Risultato registrato: `{"volume_prima": 3717.257, "faccia_z": 10.0, "parametrico": true, "volume_dopo": 4460.708}`
```python
# lo STEP mette ogni corpo in un suo componente: cercare in tutti i componenti
b = next(b for c in d.allComponents for b in c.bRepBodies if abs(b.volume * 1000 - 3717.257) < 0.01)
alto = max([f for f in b.faces if isinstance(f.geometry, adsk.core.Plane)], key=lambda f: f.centroid.z)
ris = {"volume_prima": round(b.volume * 1000, 3), "faccia_z": round(alto.centroid.z * 10, 3), "parametrico": d.designType == adsk.fusion.DesignTypes.ParametricDesignType}
try:
    FF = b.parentComponent.features
    oi = FF.offsetFacesFeatures.createInput([alto], S("2 mm"))
    FF.offsetFacesFeatures.add(oi)
    ris["volume_dopo"] = round(b.volume * 1000, 3)
except Exception as ex:
    ris["errore"] = str(ex)[-200:]
out(**ris)
```

## Testo, fori svasati e lamati, gancio, ingranaggi

### TESTO
```python
e = blocco(0, 0, 60, 20, 5); b = e.bodies.item(0); v0 = vol(b)
def testo(sk):
    ti = sk.sketchTexts.createInput2("TESTO", 0.6)
    ti.setAsMultiLine(P(0.5, 0.4, 0), P(5.5, 1.6, 0), adsk.core.HorizontalAlignments.LeftHorizontalAlignment, adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    return sk.sketchTexts.add(ti)
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("5 mm")); pl = r.constructionPlanes.add(pi)
t1 = testo(r.sketches.add(pl))
ci = F.extrudeFeatures.createInput(t1, OP.CutFeatureOperation); ci.setDistanceExtent(False, S("-1 mm"))
F.extrudeFeatures.add(ci); tolto = round(v0 - vol(b), 4)
pi2 = r.constructionPlanes.createInput(); pi2.setByOffset(r.xYConstructionPlane, S("20 mm")); pl2 = r.constructionPlanes.add(pi2)
t2 = testo(r.sketches.add(pl2))
nb = F.extrudeFeatures.addSimple(t2, S("1 mm"), OP.NewBodyFeatureOperation)
vt = round(sum(x.volume for x in nb.bodies) * 1000, 4)
bb = b.boundingBox
out(volume_tolto=tolto, volume_testo=vt, corpi_testo=nb.bodies.count, z_max=round(bb.maxPoint.z * 10, 3))
```

### FORI
```python
def foro(tipo):
    e = blocco(0, 0, 20, 20, 10); b = e.bodies.item(0)
    H = F.holeFeatures
    hi = H.createCountersinkInput(S("3.4 mm"), S("6.5 mm"), S("90 deg")) if tipo == "svasato" else H.createCounterboreInput(S("3.4 mm"), S("6.5 mm"), S("3.2 mm"))
    hi.setPositionByPoint(e.endFaces.item(0), P(1, 1, 1))
    hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
    H.add(hi)
    return vol(b)
out(svasato=foro("svasato"), lamato=foro("lamato"))
```

### GANCIO
```python
up = d.userParameters
for n, v, u in (("gancio_spessore", "1.86 mm", "mm"), ("gancio_lunghezza", "12 mm", "mm"), ("gancio_sottosquadro", "0.8 mm", "mm"),
                ("gancio_larghezza", "8 mm", "mm"), ("gancio_ritorno", "45 deg", "deg"), ("gancio_invito", "30 deg", "deg")):
    up.add(n, S(v), u, "gancio PETG l 12, b 8, y 0,8, montaggio ripetuto (formula in ricette.md §10)")
sk = r.sketches.add(r.xZConstructionPlane); sk.name = "SK_gancio"
m = lambda x, z: sk.modelToSketchSpace(P(x / 10, 0, z / 10))
z0 = 12 - 0.8 - 0.8 / math.tan(math.radians(30))
pt = [m(0, 0), m(1.86, 0), m(1.86, z0), m(2.66, z0 + 0.8), m(1.86, 12), m(0, 12)]
L = sk.sketchCurves.sketchLines; li = []
for i in range(6):
    a = li[-1].endSketchPoint if li else pt[0]
    b_ = li[0].startSketchPoint if i == 5 else pt[i + 1]
    li.append(L.addByTwoPoints(a, b_))
g = sk.geometricConstraints; dm = sk.sketchDimensions
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation; V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
g.addCoincident(li[0].startSketchPoint, sk.originPoint)
g.addHorizontal(li[0]); g.addVertical(li[1]); g.addHorizontal(li[4]); g.addVertical(li[5])
def q(p1, p2, ori, espr):
    c = p1.geometry; dm.addDistanceDimension(p1, p2, ori, P(c.x + 0.3, c.y + 0.3, 0)).parameter.expression = espr
q(li[0].startSketchPoint, li[0].endSketchPoint, H, "gancio_spessore")
q(li[5].startSketchPoint, li[5].endSketchPoint, V, "gancio_lunghezza")
q(li[4].startSketchPoint, li[4].endSketchPoint, H, "gancio_spessore")
q(li[2].startSketchPoint, li[2].endSketchPoint, H, "gancio_sottosquadro")
q(li[2].startSketchPoint, li[2].endSketchPoint, V, "gancio_sottosquadro * tan(gancio_ritorno)")
q(li[3].startSketchPoint, li[3].endSketchPoint, V, "gancio_sottosquadro / tan(gancio_invito)")
ei = F.extrudeFeatures.createInput(sk.profiles.item(0), OP.NewBodyFeatureOperation); ei.setSymmetricExtent(S("gancio_larghezza"), True)
e = F.extrudeFeatures.add(ei); e.name = "EST_gancio"; b = e.bodies.item(0)
bb = b.boundingBox
out(vincolato=sk.isFullyConstrained, volume=vol(b), ingombro=[round((bb.maxPoint.x - bb.minPoint.x) * 10, 3), round((bb.maxPoint.y - bb.minPoint.y) * 10, 3), round((bb.maxPoint.z - bb.minPoint.z) * 10, 3)])
```

### INGRANAGGI
`PUNTI` (nome → punti del profilo in mm) e `COPPIE` (coppie di nomi da controllare) si calcolano fuori da Fusion con `ingranaggio()`
(blocco qui sotto) e si passano allo script, per esempio una coppia m 1, z 20 a interasse m·z, la seconda sfasata di mezzo passo:
`PUNTI = {"A0": ingranaggio(20, gioco=0.1)[0], "B0": ingranaggio(20, gioco=0.1, cx=20.0, fase=math.pi / 20)[0]}; COPPIE = [("A0", "B0")]`.
```python
def ruota(pts, nome):
    sk = r.sketches.add(r.xYConstructionPlane); sk.name = nome
    L = sk.sketchCurves.sketchLines; prima = None; primo = None
    for i, (x, y) in enumerate(pts):
        x2, y2 = pts[(i + 1) % len(pts)]
        a = prima.endSketchPoint if prima else P(x / 10, y / 10, 0)
        bpt = primo.startSketchPoint if i == len(pts) - 1 else P(x2 / 10, y2 / 10, 0)
        prima = L.addByTwoPoints(a, bpt); primo = primo or prima
    prof = max(sk.profiles, key=lambda p: p.areaProperties().area)
    e = F.extrudeFeatures.addSimple(prof, S("5 mm"), OP.NewBodyFeatureOperation); e.bodies.item(0).name = nome
    return e.bodies.item(0), prof.areaProperties().area * 100
ris = {}
b1, area = ruota(PUNTI["A0"], "A0")
bb = b1.boundingBox
ris["area_mm2"] = round(area, 3); ris["volume"] = vol(b1)
ris["diametro_x"] = round((bb.maxPoint.x - bb.minPoint.x) * 10, 3)
ris["piede_min"] = round(2 * min(math.hypot(x, y) for x, y in PUNTI["A0"]), 3)
ris["interferenze"] = {}
for coppia in COPPIE:
    oc = adsk.core.ObjectCollection.create()
    for nome in coppia:
        if r.bRepBodies.itemByName(nome) is None: ruota(PUNTI[nome], nome)
        oc.add(r.bRepBodies.itemByName(nome))
    res = d.analyzeInterference(d.createInterferenceInput(oc))
    ris["interferenze"]["-".join(coppia)] = [round(x.interferenceBody.volume * 1000, 4) for x in res]
out(**ris)
```

Esito registrato: `{"R1_testo_tolto_uguale_al_testo": true, "R2_svasato": true, "R3_lamato": true, "R4_gancio_vincolato": true, "R4_gancio_volume": true, "R5_area": true, "R5_testa_22": true, "R5_piede_17.5": true, "R5_coppie_senza_interferenze": true, "R5_rottura_apposta_interferisce": true}`

```python
def ingranaggio(z, m=1.0, alfa=20.0, gioco=0.0, fase=0.0, cx=0.0, cy=0.0, n=8):
    a = math.radians(alfa); r = m * z / 2; rb = r * math.cos(a); ra = r + m; rf = r - 1.25 * m
    inv = lambda t: math.tan(t) - t
    beta = (math.pi * m / 2 - gioco) / (2 * r)                      # semi-angolo del dente sul primitivo
    th = lambda rho: beta + inv(a) - inv(math.acos(min(1.0, rb / rho)))  # semi-angolo del dente al raggio rho
    r0 = max(rf, rb)
    fianco = [r0 + (ra - r0) * i / n for i in range(n + 1)]
    pts = []
    for k in range(z):
        c = 2 * math.pi * k / z + fase
        dente = ([(rf, c - th(r0))] if rf < rb else []) + [(rho, c - th(rho)) for rho in fianco] + [(ra, c)] + \
                [(rho, c + th(rho)) for rho in reversed(fianco)] + ([(rf, c + th(r0))] if rf < rb else [])
        pts += dente
    xy = [(cx + rr * math.cos(t), cy + rr * math.sin(t)) for rr, t in pts]
    area = 0.5 * abs(sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(xy, xy[1:] + xy[:1])))
    return xy, area, ra, rf
```

