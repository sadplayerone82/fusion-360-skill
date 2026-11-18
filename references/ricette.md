# Ricette provate

Ogni ricetta qui sotto è stata **provata in Fusion** con un controllo automatico (volume o misure uguali al calcolo fatto prima). Copiale e adattale invece di
scrivere l'API a memoria: le funzioni ricordate male sono state la causa principale degli errori.

Queste sono le ricette **essenziali**, scritte per un modello vero (vincolato, parametrico). Tutto il resto di quello che è stato provato,
con il codice esatto e il risultato misurato, è nei file `ricette-*.md` (schizzi e piani, 21 feature solide, superfici/forme
libere/lamiera, assiemi, modificare/importare, produzione/viste/render) e le misure delle viti in `dati-standard.md`.

Indice: 1 intestazione · 2 rettangolo centrato vincolato · 3 profilo a L sul piano XZ · 4 estrusioni · 5 raccordi scelti per geometria ·
6 fori in serie · 7 svasati e lamati · 8 punti allineati senza ipervincolo · 9 testo inciso · 10 gancio a scatto · 11 ingranaggio a
evolvente · 12 giunti · 13 materiali e massa · 14 interferenza · 15 esportazione 3MF/STEP e salvataggio .f3d · 16 immagini e render

## 1. Intestazione degli script
`scripts/mcp_fusion.py` avvolge il tuo codice in `def run(_context: str):` con questa intestazione (funzione `corpo(codice)`, costante
`TESTA`), quindi negli esempi questi nomi esistono già. È quella che usano `scripts/progetto_locale.py` e `scripts/esegui_file.py`: il
file di un passo contiene **solo il codice**, senza intestazione.
```python
import adsk.core, adsk.fusion, math, json
app = adsk.core.Application.get()
d = adsk.fusion.Design.cast(app.activeProduct)
r = d.rootComponent if d else None; F = r.features if r else None
P = adsk.core.Point3D.create; S = adsk.core.ValueInput.createByString; OP = adsk.fusion.FeatureOperations
H = adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation; V = adsk.fusion.DimensionOrientations.VerticalDimensionOrientation
def vol(b):     # mm³, ad alta precisione: b.volume (veloce) sbaglia di qualche mm³ sulle superfici curve che si intersecano
    return round(b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy).volume * 1000, 4)
def out(**k): print("RIS" + json.dumps(k))            # risultato leggibile dallo script esterno (l'ultimo out() vince)
def controlla(corpo=None, volume=None, ingombro=None, n_corpi=None, tol_v=0.0001, tol_l=0.01): ...
```
`controlla` confronta **nella stessa chiamata** con l'atteso, in mm e mm³: `n_corpi` (corpi del componente principale e di tutte le
occorrenze), `volume` di `corpo` (tolleranza relativa `tol_v`, predefinita 0,01 %), `ingombro` `[x, y, z]` di `corpo` dal suo
`boundingBox` (tolleranza `tol_l`, predefinita 0,01 mm). Se qualcosa non torna solleva `RuntimeError("CONTROLLO FALLITO: …")`: lo script
è una transazione, quindi nel documento non resta nulla del passo. Esempio di fine passo:
`controlla(e.bodies.item(0), volume=7905.309, ingombro=[40, 30, 30], n_corpi=1); out(v=vol(e.bodies.item(0)))`.
Sui corpi curvi l'ingombro dell'API può essere un po' largo (vedi `sketch.boundingBox` in `connettore-e-api.md`): se `controlla` boccia
un ingombro di pochi centesimi, misura gli estremi veri prima di toccare il modello.

`progetto_locale.py <cartella> passo <nome> <file.py> --atteso V` esegue il file, poi misura da solo (volume totale e per corpo ad alta
precisione, elementi della timeline in errore) e confronta col volume atteso (0,01 %): se non torna o c'è un elemento in errore il
passo **non** viene registrato. Se torna, salva lo script in `passi/`, una riga in `registro.json`, la copia `progetto.f3d` e fa un
commit git (se la cartella è un repository). Gli altri comandi: `misura`, `riapri`, `rigioca`, `versione`.

Le ricette dei file `ricette-*.md` usano a volte un'intestazione **semplificata** delle prove (con `vol` da `b.volume`, `rett`,
`blocco`…): per un modello vero vale quella qui sopra.

Parametri utente: `d.userParameters.add("spessore", S("4 mm"), "mm", "commento")`.

## 2. Rettangolo centrato completamente vincolato
L'API crea le 4 linee **senza vincoli**: aggiungili tu. (Provato: lati 40.0 × 20.0, centro 0,0, `isFullyConstrained` vero.)
```python
sk = r.sketches.add(r.xYConstructionPlane); sk.name = "SK_base"
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(2, 1, 0))
g = sk.geometricConstraints; dm = sk.sketchDimensions
g.addHorizontal(l[0]); g.addVertical(l[1]); g.addHorizontal(l[2]); g.addVertical(l[3])
dg = sk.sketchCurves.sketchLines.addByTwoPoints(l[0].startSketchPoint, l[2].startSketchPoint); dg.isConstruction = True
g.addMidPoint(sk.originPoint, dg)                      # centro sull'origine
dm.addDistanceDimension(l[0].startSketchPoint, l[0].endSketchPoint, H, P(0, -1.5, 0)).parameter.expression = "base_L"
dm.addDistanceDimension(l[1].startSketchPoint, l[1].endSketchPoint, V, P(2.5, 0, 0)).parameter.expression = "base_W"
```
Le linee come costruzione (`x.isConstruction = True` per ciascuna) danno 4 punti vincolati: servono per i fori in serie (§6).

## 3. Profilo chiuso sul piano XZ (es. staffa a L) vincolato
Sul piano XZ la Y dello schizzo è la −Z del modello: dai i punti in coordinate del modello e convertili.
```python
sk = r.sketches.add(r.xZConstructionPlane); sk.name = "SK_profilo"
m = lambda x, z: sk.modelToSketchSpace(P(x / 10, 0, z / 10))     # mm del modello → schizzo
pt = [m(0, 0), m(40, 0), m(40, 4), m(4, 4), m(4, 30), m(0, 30)]
L = sk.sketchCurves.sketchLines; li = []
for i in range(6):                                                  # riusa i punti: niente punti doppi
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
Gradi di libertà: 12 (6 punti) − 2 origine − 6 orizzontali/verticali − 4 quote = 0.

## 4. Estrusioni
```python
e = F.extrudeFeatures.addSimple(prof, S("base_H"), OP.NewBodyFeatureOperation); e.name = "EST_base"; e.bodies.item(0).name = "Pezzo"
ei = F.extrudeFeatures.createInput(prof, OP.NewBodyFeatureOperation); ei.setSymmetricExtent(S("larghezza"), True)   # simmetrica, totale
ci = F.extrudeFeatures.createInput(prof, OP.CutFeatureOperation); ci.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
ci = F.extrudeFeatures.createInput(prof, OP.CutFeatureOperation); ci.setDistanceExtent(False, S("incavo_H"))
pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, S("base_H")); piano = r.constructionPlanes.add(pi)
```
Profilo: sceglilo per area (`min(sk.profiles, key=lambda p: abs(p.areaProperties().area - atteso_cm2))`), non per indice. Conicità e
sformo con angolo **positivo allargano** il pezzo. Cerchio centrato: centro coincidente con `sk.originPoint` + quota di diametro.

## 5. Raccordi su spigoli scelti per geometria
```python
b = r.bRepBodies.itemByName("Pezzo")
sp = [s for s in b.edges if all(abs(v.geometry.x - 0.4) < 1e-6 and abs(v.geometry.z - 0.4) < 1e-6 for v in (s.startVertex, s.endVertex))]
col = adsk.core.ObjectCollection.create(); [col.add(s) for s in sp]
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(col, S("raggio"), True); F.filletFeatures.add(fi).name = "RAC_interno"
```
Spigoli verticali: `isinstance(ed.geometry, adsk.core.Line3D) and abs(g.startPoint.z - g.endPoint.z) > 1e-3`. Ricerca **dopo** l'ultima feature.

## 6. Fori uguali in serie (un solo comando)
Mai 4 fori sulla stessa faccia in un ciclo: dopo il primo la faccia non esiste più. Centri come punti di uno schizzo vincolato:
```python
sk = r.sketches.add(piano_sopra); sk.name = "SK_fori"
l = sk.sketchCurves.sketchLines.addCenterPointRectangle(P(0, 0, 0), P(5, 3, 0))
for x in l: x.isConstruction = True
# ... vincoli e quote come §2 con "fori_X" e "fori_Y"
punti = adsk.core.ObjectCollection.create()
for x in l: punti.add(x.startSketchPoint)
hi = F.holeFeatures.createCounterboreInput(S("foro_D"), S("lamatura_D"), S("lamatura_H"))   # o createSimpleInput(S("foro_D"))
hi.setPositionBySketchPoints(punti)
hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
F.holeFeatures.add(hi).name = "FORI_fissaggio"
```
Provato su una base 15 mm: volume = calcolo; attenzione se la lamatura esce dal bordo (il calcolo atteso deve tenerne conto).

## 7. Fori svasati e lamati (viti a testa piana o cilindrica)
```python
hi = F.holeFeatures.createCountersinkInput(S("3.4 mm"), S("6.5 mm"), S("90 deg"))     # svasato M3
hi = F.holeFeatures.createCounterboreInput(S("3.4 mm"), S("6.5 mm"), S("3.2 mm"))     # lamato M3
hi.setPositionByPoint(faccia, P(x, y, z_faccia)); hi.setAllExtent(adsk.fusion.ExtentDirections.PositiveExtentDirection)
```
I valori qui sopra sono quelli della prova (controllo superato). Per una vite vera prendi le misure dalla norma in
`dati-standard.md`: es. testa piana M3 ISO 10642 → svasatura **Ø7.5**; testa cilindrica M3 ISO 4762 → lamatura **Ø6.5 × 3.4**.

## 8. Punti allineati senza «ipervincolo» a torto
Una 2ª quota orizzontale dall'origine verso un punto allineato in verticale con uno già quotato viene rifiutata. Lega il secondo al primo:
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
Per centrare una figura su un asse usa una quota «L / 2» dall'origine: una linea d'asse con un estremo libero lascia un grado di libertà.

## 9. Testo inciso o in rilievo
```python
ti = sk.sketchTexts.createInput2("TESTO", 0.6)            # altezza 6 mm
ti.setAsMultiLine(P(0.5, 0.4, 0), P(5.5, 1.6, 0), adsk.core.HorizontalAlignments.LeftHorizontalAlignment,
                  adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
t = sk.sketchTexts.add(ti)
ci = F.extrudeFeatures.createInput(t, OP.CutFeatureOperation); ci.setDistanceExtent(False, S("-1 mm")); F.extrudeFeatures.add(ci)
```
Il testo stesso è il profilo. Altezza e spessore minimi per la produzione: dalla skill di stampa 3D, se installata (impostazione
`skill_stampa`), o dal processo scelto. Testo su facce curve: `ricette-decori-anelli.md`.

## 10. Gancio a scatto parametrico
Spessore del braccio (sbalzo a sezione costante, guida Bayer «Snap-Fit Joints for Plastics»): **h = 0,67 · ε · l² / y**, con l lunghezza
del braccio, y sottosquadro, ε deformazione ammessa del materiale (per un pezzo stampato in 3D quella del pezzo stampato, più bassa
per montaggi ripetuti: dal produttore o da un provino). Esempio provato: l 12, y 0.8, larghezza 8, spessore 1.86 (ε ≈ 1,5 %). Se è
installata una skill di stampa 3D (impostazione `skill_stampa`), ε e lo spessore li dà lei. Profilo sul piano XZ come §3 con 6
parametri e quote a espressione:
`gancio_sottosquadro * tan(gancio_ritorno)` e `gancio_sottosquadro / tan(gancio_invito)` per le due facce del dente; estrusione
simmetrica `gancio_larghezza`. Provato: (1.86·12 + ½·0.8·2.186)·8 = 185.554 mm³, schizzo vincolato.

## 11. Ingranaggio a evolvente
Calcola il profilo in Python (fuori da Fusion) e passalo come polilinea:
```python
def ingranaggio(z, m=1.0, alfa=20.0, gioco=0.05, fase=0.0, cx=0.0, cy=0.0, n=8):
    a = math.radians(alfa); r = m*z/2; rb = r*math.cos(a); ra = r + m; rf = r - 1.25*m
    inv = lambda t: math.tan(t) - t
    beta = (math.pi*m/2 - gioco) / (2*r)                               # semi-angolo del dente sul primitivo
    th = lambda rho: beta + inv(a) - inv(math.acos(min(1.0, rb/rho)))
    r0 = max(rf, rb); fianco = [r0 + (ra - r0)*i/n for i in range(n + 1)]
    pts = []
    for k in range(z):
        c = 2*math.pi*k/z + fase
        pts += ([(rf, c - th(r0))] if rf < rb else []) + [(rho, c - th(rho)) for rho in fianco] + [(ra, c)] + \
               [(rho, c + th(rho)) for rho in reversed(fianco)] + ([(rf, c + th(r0))] if rf < rb else [])
    return [(cx + rr*math.cos(t), cy + rr*math.sin(t)) for rr, t in pts]   # mm
```
Polilinea chiusa nello schizzo (riusando i punti), profilo di area massima, estrusione. Provato m 1, z 20: Ø testa 22.0, Ø piede 17.5,
area = formula di Gauss; coppia a interasse m·z con gioco 0.1: 0 interferenze in 3 posizioni; con denti più grossi l'interferenza
compare. Per moduli grandi aumenta `n`. Dentature elicoidali e coniche non studiate.

## 12. Giunti fra componenti
```python
occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create()); occ.component.name = "Braccio"
g0 = adsk.fusion.JointGeometry.createByPlanarFace(faccia_fissa.createForAssemblyContext(occ_fisso), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
g1 = adsk.fusion.JointGeometry.createByPlanarFace(faccia_mobile.createForAssemblyContext(occ), None, adsk.fusion.JointKeyPointTypes.CenterKeyPoint)
ji = r.joints.createInput(g1, g0); ji.setAsRevoluteJointMotion(adsk.fusion.JointDirections.ZAxisJointDirection)
ji.isFlipped = True        # senza, con facce sotto→sopra il pezzo si capovolge DENTRO l'altro (interferenza piena, nessun errore)
j = r.joints.add(ji); j.jointMotion.rotationValue = math.radians(45)
```
Dopo ogni giunto: nessuna compenetrazione, gioco misurato e posizione dei corpi attesa (`occ.transform2.translation`). Limiti: impostali **prima** dei
valori (attivarli riporta il giunto a 0); un valore fuori campo viene ignorato in silenzio → rileggi il valore. `occurrence.boundingBox`
dà zeri: misura i corpi. Scorrevole: `setAsSliderJointMotion(XAxisJointDirection)`, `slideValue` in cm.

## 13. Materiali e massa (per codice, i nomi sono tradotti)
```python
lib = max(app.materialLibraries, key=lambda l: l.materials.count)
b.material = lib.materials.itemById("PrismMaterial-022")      # Plastica ABS 1 060 kg/m³; acciaio = PrismMaterial-018 (7 850)
massa_g = b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.HighCalculationAccuracy).mass * 1000
```

## 14. Interferenza fra corpi o componenti
```python
oc = adsk.core.ObjectCollection.create(); oc.add(a); oc.add(b)
ris = d.analyzeInterference(d.createInterferenceInput(oc)); volumi = [x.interferenceBody.volume * 1000 for x in ris]
```

## 15. Esportazione e salvataggio sul PC
```python
em = d.exportManager
em.execute(em.createC3MFExportOptions(r, file_3mf))                 # 3MF in mm (corpi visibili!)
em.execute(em.createSTEPExportOptions(file_step, r))
em.execute(em.createFusionArchiveExportOptions(file_f3d, r))        # progetto .f3d: riaperto resta parametrico
im = app.importManager; im.importToNewDocument(im.createFusionArchiveImportOptions(file_f3d))   # riapertura
```
Dopo ogni esportazione controlla che il file esista; il 3MF passa da `scripts/controlla_mesh.py` con le misure attese asse per asse.
Qualità della mesh: per l'**STL** le opzioni sono ignorate (provato: 6 impostazioni → file identici); per il **3MF funzionano** e servono
(provato: con le impostazioni di serie un arco R33 usciva 0.04 mm più corto e il controllo a 0.01 mm falliva; con
raffinamento personalizzato a scarto 0.01 mm passa — file più pesante, 1.7 MB per una flangia):
```python
o = em.createC3MFExportOptions(r, file_3mf)
o.meshRefinement = adsk.fusion.MeshRefinementSettings.MeshRefinementCustom; o.surfaceDeviation = 0.001   # cm = 0.01 mm
em.execute(o)
```

### Filetti: attenzione
- I **filetti cosmetici cambiano i diametri** del modello alle misure della norma senza errori (provato: mozzo Ø45 → Ø44.822, foro
  Ø10.106 → Ø10.2735; il volume è sceso di 444 mm³ e solo il controllo dell'atteso l'ha scoperto). Se le quote della tavola o dell'utente
  devono restare quelle: se l'utente vuole **solo le misure**, niente filetto e dati nel commento del parametro; se vuole **anche il filetto cosmetico**,
  mettilo e riporta il diametro con «Sposta faccia» subito dopo (provato: volume esatto, `.f3d` riaperto senza errori). Quel passo ha un valore fisso:
  se cambia il diametro va aggiornato, e va detto nel resoconto. Non togliere una cosa chiesta senza dirlo.
- Filetto **interno** (madrevite, classe 6H): `q.allClasses(True, tipo, designazione)` e `adsk.fusion.ThreadInfo.create(False, True, tipo,
  designazione, classe, True)` (il secondo argomento `True` = interno). Esterno: `allClasses(False, …)`, `ThreadInfo.create(False, False, …)`.

## 16. Immagini e render
- Immagini del pezzo: imposta la **telecamera a mano** e salva con la vista — le direzioni predefinite (`viewOrientation`, o lo
  screenshot con `direction`) hanno dato più volte immagini **tutte uguali** (provato in due occasioni):
  ```python
  vp = app.activeViewport; cam = vp.camera
  cam.eye = P(30, -30, 25); cam.target = P(0, 0, 2.5); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); cam.isSmoothTransition = False
  vp.camera = cam; vp.fit(); vp.saveAsImageFile(file_png, 1200, 900)
  ```
  Guarda ogni immagine: devono essere diverse e mostrare il pezzo come nella tavola.
- Render **locale** (gratis): `rd = d.renderManager.rendering; rd.resolution = adsk.fusion.RenderResolutions.Web800x600RenderResolution;
  rd.renderQuality = 25; rd.startLocalRender(file_png, app.activeViewport.camera)` (asincrono: aspetta che il file esista).
  Il render nel cloud è a pagamento.
