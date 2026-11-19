# Ricette di forma: pezzi curvi e raccordati via script (provate a novembre 2026)

Per gli oggetti da riconoscere (`forma-e-dettaglio.md`). Dicono **come si passa dall'estrusione alla forma** restando parametrici:
sezioni vincolate su piani paralleli → loft → tondi e tagli → raccordi → guscio. Stesse definizioni delle altre ricette (`r`, `d`,
`F`, `P`, `S`, `OP`, `vol`, `out`, `controlla`: l'intestazione di `ricette.md` §1). Lunghezze dell'API in cm.

Misurato sui due pezzi qui sotto: braccio 18 facce e 5,9 % di spigoli vivi (una barra estrusa: 8 facce, 100 %); guscio 0 % di spigoli
vivi, parete 1,5 mm costante. Nessun avviso di `scripts/segni_forma.py`, 0 errori, schizzi tutti vincolati, modifiche dei parametri rette.

## 1. Una sezione ellittica vincolata su un piano parallelo a YZ
```python
def piano_x(espr, nome):
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.yZConstructionPlane, S(espr)); pl = r.constructionPlanes.add(pi); pl.name = nome
    return pl
def sezione(pl, x_cm, z_cm, ea, eb, ez, nome):      # ea, eb, ez = nomi dei parametri: semiassi e altezza del centro (ez None = sull'asse)
    sk = r.sketches.add(pl); sk.name = nome
    c = sk.modelToSketchSpace(P(x_cm, 0, z_cm)); pa = sk.modelToSketchSpace(P(x_cm, 1.0, z_cm)); pb = sk.modelToSketchSpace(P(x_cm, 0, z_cm + 0.5))
    el = sk.sketchCurves.sketchEllipses.add(c, pa, pb)
    o = sk.project(r.originConstructionPoint).item(0)
    g = sk.geometricConstraints; dm = sk.sketchDimensions
    orizz = abs(pa.x - c.x) > abs(pa.y - c.y)        # l'asse Y del modello è orizzontale o verticale in QUESTO schizzo? non darlo per scontato
    (g.addHorizontal if orizz else g.addVertical)(el.majorAxisLine)
    if ez is None: g.addCoincident(el.centerSketchPoint, o)
    else:
        asse = sk.sketchCurves.sketchLines.addByTwoPoints(o, el.centerSketchPoint); asse.isConstruction = True
        (g.addVertical if orizz else g.addHorizontal)(asse)
        dm.addDistanceDimension(o, el.centerSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, P(c.x + 0.5, c.y + 0.5, 0)).parameter.expression = ez
    dm.addEllipseMajorRadiusDimension(el, P(c.x + 0.3, c.y + 0.3, 0)).parameter.expression = ea
    dm.addEllipseMinorRadiusDimension(el, P(c.x - 0.3, c.y - 0.3, 0)).parameter.expression = eb
    return sk                                        # sk.isFullyConstrained == True (provato su 7 sezioni)
```

## 2. Loft fra le sezioni
```python
i = F.loftFeatures.createInput(OP.NewBodyFeatureOperation)
for sk in (s0, s1, s2): i.loftSections.add(sk.profiles.item(0))
lo = F.loftFeatures.add(i); lo.name = "LOFT_braccio"; b = lo.bodies.item(0)
```
- **Attesi**: se i semiassi calano in linea retta, il volume è la somma dei tronchi fra sezioni vicine,
  `V = π·h/6·(2·a1·b1 + 2·a2·b2 + a1·b2 + a2·b1)` (braccio: 3 701,84 mm³ calcolati e misurati). Con sezioni che non calano in linea
  retta il loft è una superficie liscia senza formula chiusa: dichiara un intervallo.
- **Il loft liscio sporge oltre la sezione più grande**: guscio con sezione massima 52 × 48 → ingombro misurato 54,8 × 50,6. Se un
  ingombro è un vincolo (misure del produttore), controllalo dopo il loft e correggi le sezioni, non il numero.
- Controlla `lo.healthState == 0`, il volume e un'immagine: un loft può autointersecarsi senza errori.

## 3. Unire tondi (nocca, sede) e non lasciare cuspidi
Un tondo = cerchio vincolato su un piano spostato di metà altezza + estrusione `JoinFeatureOperation`; il foro con `CutFeatureOperation`.
Due difetti che **i numeri non vedono** e l'immagine sì (trovati guardandola, con 10/10 nei controlli):
- sezione **alta quanto il tondo** → il loft esce dalla faccia superiore con una piega a cuneo: tieni la sezione 1 mm sotto;
- sezione **larga quanto il tondo** → cuspide dove i fianchi toccano il cilindro: tienila più stretta (13 su Ø 16).

## 4. Raccordi scelti per geometria (mai per indice)
```python
b = r.bRepBodies.item(0); tipo = lambda f: f.geometry.objectType.split("::")[-1]
unione = adsk.core.ObjectCollection.create(); orli = adsk.core.ObjectCollection.create()
rf = d.userParameters.itemByName("D_foro").value / 2
for e in b.edges:
    if e.faces.count != 2: continue
    t = sorted(tipo(f) for f in e.faces)
    if any(tipo(f) == "Cylinder" and abs(f.geometry.radius - rf) < 1e-6 for f in e.faces): continue     # gli spigoli del foro restano vivi
    if "NurbsSurface" in t: unione.add(e)             # fra la superficie del loft e un tondo
    elif t == ["Cylinder", "Plane"]: orli.add(e)      # orli dei tondi
fi = F.filletFeatures.createInput()
fi.edgeSetInputs.addConstantRadiusEdgeSet(unione, S("R_unione"), True); fi.edgeSetInputs.addConstantRadiusEdgeSet(orli, S("R_bordo"), True)
fe = F.filletFeatures.add(fi)                          # poi fe.healthState == 0 e volume
```
Raccordi grandi (unione) e piccoli (orli) nella stessa feature: provato con R2 e R1.

## 5. Guscio cavo di spessore costante
```python
col = adsk.core.ObjectCollection.create(); col.add(r.bRepBodies.item(0))
si = F.shellFeatures.createInput(col, False); si.insideThickness = S("spessore_guscio")
sh = F.shellFeatures.add(si)                           # corpo con 2 superfici chiuse (b.shells.count == 2)
```
Prima del guscio raccorda gli orli dei tappi piani (R6 provato). Attesi: volume fra l'85 e il 100 % di «area esterna × spessore»
(misurato 26 975 mm³ su 28 188, il 95,7 %); `scripts/spessore_minimo.py` deve dare lo spessore del guscio (1,5 misurato).

## 6. Limiti dichiarati
- Provati **due pezzi**, con sezioni ellittiche. Sezioni di forma libera (spline ricalcate su un'immagine), loft con guide o linea
  centrale, superfici cucite e T-spline modificate **non sono provati qui**: per le T-spline vedi `ricette-superfici-forme-lamiera.md`.
- Un guscio liscio è una forma, non ancora un prodotto riconoscibile: mancano i dettagli (tagli, sedi, feritoie) e il confronto con i
  riferimenti, che restano compito di `forma-e-dettaglio.md`.
- Il codice qui sopra è quello delle due prove, riunito: la funzione `sezione` unisce le due varianti (centro sull'asse o rialzato)
  e la scelta degli spigoli d'unione è scritta nella forma più corta.
- Esito delle prove: braccio 10 controlli su 10, guscio 9 su 9; la stessa barra fatta come semplice estrusione prende tutti e tre gli
  avvisi S1, S2, S3 di `scripts/segni_forma.py`.
