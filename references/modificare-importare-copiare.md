# Modificare, importare, copiare, riprendere

## 1. Ritrovare e riaprire un progetto
I progetti stanno nella cartella dei progetti di `impostazioni.json` (`cartella_progetti`), con l'elenco `elenco-progetti.md` (data,
nome, descrizione, cartella), scritto da `scripts/nuovo_progetto.py`. «Il supporto di ieri» si cerca lì (`nuovo_progetto.py --cerca
<parola>`); l'ultima versione è il file con il numero più alto in `consegna/` (o `progetto.f3d`, la copia dopo l'ultimo passo). Si riapre l'ultima versione:
`im = app.importManager; im.importToNewDocument(im.createFusionArchiveImportOptions(file_f3d))` (riaperto resta parametrico: parametri,
timeline e vincoli intatti, provato). Le modifiche si salvano in una **nuova versione** (`-v2`, `-v3`…), mai sopra la precedente.

## 2. Modificare un modello con la storia (timeline)
- Leggi prima la timeline: `[(o.index, o.name, o.entity.objectType, o.healthState) for o in d.timeline]`.
- Cambiare un parametro: `d.userParameters.itemByName("x").expression = "30 mm"`.
- Cambiare la definizione di una feature (ricetta ufficiale Autodesk): `feat.timelineObject.rollTo(True)` → modifica (es.
  `adsk.fusion.SymmetricExtentDefinition.cast(feat.extentOne).distance.expression = "larghezza + 10 mm"`) → `d.timeline.moveToEnd()`.
- Inserire una feature a metà: `rollTo(True)` sulla feature davanti alla quale va, crea la nuova, `moveToEnd()`.
- Spostare una feature: `to.canReorder(indice)` poi `to.reorder(indice)`.
- **Riparare** una feature con un riferimento perso (es. schizzo cancellato): cambiarle il profilo viene rifiutato
  («InternalValidationError : curProfile»); torna prima della feature, rifai lo schizzo vincolato, cancella e **rifai** la feature con lo
  stesso nome, `moveToEnd()`, rapporto. Provato: volume di nuovo giusto, 0 elementi in errore.
Dopo ogni modifica: rapporto e misure contro gli attesi **ricalcolati**.

## 3. Importare STEP e STL scaricati
- STEP: `o = im.createSTEPImportOptions(file); o.isViewFit = False; im.importToTarget(o, r)`. Ogni corpo finisce in un **suo componente**:
  cerca i corpi in `d.allComponents`. Misura subito volume e ingombro (sono il punto di partenza degli attesi).
- **STEP più tavola dello stesso pezzo** (ricostruire un modello «muto» come parametrico): le due fonti possono non coincidere, perché
  la tavola arrotonda. Misura **ogni** quota sul 3D importato e mettila accanto a quella della tavola; anche una differenza di pochi
  millesimi cambia il volume oltre la tolleranza (provato: fondo 1,93 sulla tavola e 1,925 nello STEP → volume +0,14 %).
  Elenca le differenze e **chiedi quale fonte vale** prima di modellare, anche se la richiesta dice «prendi le quote dalla tavola»;
  alla fine confronta volume, ingombro e numero di facce con lo STEP e scrivi le differenze nel resoconto.
- STL/3MF: prima `scripts/controlla_mesh.py` (chiusa? misure?), poi `r.meshBodies.add(file, adsk.fusion.MeshUnits.MillimeterMeshUnit)`.
- Mesh → solido: `F.meshConvertFeatures.createInput([mesh])` (vuole una **lista**) e `add`. Provato su un cubo (4 000 mm³ esatti).
  Su mesh grandi e organiche il solido sfaccettato è pesante e difficile da modificare: per allungare o accorciare conviene tagliare con
  un piano, spostare e riunire, oppure dire all'utente il limite. Il metodo «prismatico» (riconosce cilindri e piani) con la licenza
  Personal è **rifiutato** («No rights for mesh conversion», provato): un ricambio si ricostruisce da sezioni calcolate
  (`ricette-stampi-mesh-pezzi.md`). Riduzione della mesh: non provata, controllare prima che non sia a pagamento.
- Modifiche dirette su un corpo importato (senza storia): spostare/sfalsare facce con le feature del **suo** componente
  (`b.parentComponent.features.offsetFacesFeatures.createInput([faccia], S("2 mm"))`). Provato: +2 mm = volume calcolato.

## 4. Copiare un pezzo reale (rotto, da sostituire)
Chiedi all'utente:
1. le **misure che contano col calibro** (fori, incastri, spessori, ingombro), **3 letture** per misura, e quale calibro usa;
2. **foto** solo per la forma: pezzo appoggiato piatto, telefono dritto sopra e un po' lontano (zoom), **righello o oggetto di misura nota
   sullo stesso piano**, sfondo uniforme, una foto per lato; salvate nella cartella `foto/` del progetto (le foto incollate in chat non
   sono file).
3. dove il pezzo è rotto, la parte intera o il pezzo in cui si monta.
Poi `scripts/misura_foto.py` (scala dal riferimento, misure in pixel → mm con incertezza ≈ 1–2 px × scala) e immagine come **canvas**
in scala vera: `ci = r.canvases.createInput(file, r.xYConstructionPlane)`, `m = adsk.core.Matrix2D.create();
m.setWithCoordinateSystem(adsk.core.Point2D.create(0, 0), adsk.core.Vector2D.create(larghezza_cm, 0), adsk.core.Vector2D.create(0, altezza_cm))`,
`ci.transform = m; r.canvases.add(ci)` (la grandezza è la lunghezza dei vettori). Ricalca, ma le quote critiche vengono **sempre** dal
calibro. Su foto vere prospettiva e distorsione non sono state provate: dichiaralo. Zigrinature e prese: non provate.

## 5. Riprendere dopo una chiusura di Fusion
Ogni progetto ha: `progetto.f3d` aggiornato dopo ogni passo verificato, `passi/NN-nome.py`, `registro.json`. Dopo una chiusura:
`Progetto(...).riapri()` (dalla copia, confronta con l'ultima riga del registro) oppure `rigioca()` (rifà i passi dagli script, documento
nuovo). Provato entrambi: stesso volume del registro. Mai ricominciare a memoria.
