# Parlare con Fusion: connettore MCP e API

Tutto quello che segue è stato misurato su Fusion (build 2706.1.14, novembre 2026, licenza Personal) con il server MCP ufficiale
Autodesk, con l'interfaccia in italiano; dove una cosa sembra strana,
è proprio quella che ha fatto sbagliare le prove.

## Gli strumenti
| Strumento | A cosa serve |
|---|---|
| `fusion_mcp_execute` `featureType: "script"` | **tutta la modellazione**: uno script Python con `def run(_context: str):` eseguito dentro Fusion |
| `fusion_mcp_execute` `document` | aprire/chiudere documenti. `close` con `userConfirmedCloseWithoutSave: true` per i documenti di prova |
| `fusion_mcp_read` `screenshot` | immagine del modello (viste: `current`, `iso-top-right`, `front`, `top`…) — per guardare davvero il pezzo |
| `fusion_mcp_read` `apiDocumentation` | documentazione di una classe o funzione (`searchPattern`, `className`) |
| `fusion_mcp_update` | `undo` / `redo` |
| `purchase`, `editImage`, `generatePowerpoint` | **non usarli** senza richiesta esplicita: comprano o consumano crediti |

Dagli script Python (anche dalla shell) lo stesso server si raggiunge con `scripts/mcp_fusion.py` (client HTTP, `Sessione().strumento(nome,
argomenti)`); è quello che usano `progetto_locale.py`, `rapporto_modello.py` e gli altri script di controllo. Gli strumenti MCP «nativi» esistono nella
sessione solo se Fusion era già aperto quando la sessione è partita: se mancano, il client HTTP funziona comunque.

## Come si comporta uno script
- È una **transazione**: se fallisce, non resta nulla di quello che aveva creato; un solo `undo` annulla l'intero script. Per questo si
  lavora a script piccoli (un passo = uno schizzo o una feature): un errore costa poco e un annulla è preciso.
- L'errore torna **dentro il testo** della risposta (`"success": false` più il traceback), non nel campo `isError`: controlla sempre
  `success`.
- Quello che lo script stampa con `print()` torna a te: stampa una riga JSON con le misure che servono (gli script del progetto usano
  `print("RIS" + json.dumps(...))`). Non catturare le eccezioni nello script: nasconderesti dove è fallito.
- `readOnly: true` per gli script che leggono soltanto: Fusion lo controlla davvero, e funziona anche se l'utente ha un comando aperto
  (uno script normale invece non parte finché l'utente non chiude il comando: chiediglielo).
- Le variabili Python non sopravvivono fra uno script e l'altro: dai un **nome** a schizzi, feature, corpi, componenti e ritrovali con
  `sketches.itemByName`, `features.itemByName`, `bRepBodies.itemByName`. Evita `findEntityByToken` (crea un passo di annullamento
  fantasma).
- Tempi: lettura 0.01–0.05 s, script 0.05–0.3 s. Verificare dopo ogni passo non costa nulla.
- Se un altro add-in MCP di terzi gira dentro Fusion, la prima risposta può contenere una sua riga («Server listening on
  localhost:…»): ignorala e, se la porta è fra le `porte_da_controllare` di `impostazioni.json`, avvisa l'utente (`ambiente.py` lo fa).

## Le unità (la regola più importante)
L'API lavora **sempre in centimetri e radianti**, anche se il documento è in mm: 2.0 nell'API = 20 mm. Usa:
- stringhe con unità: `adsk.core.ValueInput.createByString("12 mm")`, `"30 deg"`;
- nomi di parametri utente (`"spessore_base"`, `"lunghezza / 2"`): il modello resta leggibile e parametrico;
- `createByReal` solo per valori calcolati, e in cm. Le misure lette dall'API vanno moltiplicate per 10 (mm) o 1000 (mm³).
Nomi di parametri **senza spazi** e che non siano simboli di unità (`W`, `H`, `A`, `m`, `g`, `l`, `mm`, `in` vengono rifiutati).

## Tipi di documento
Un documento nuovo creato da script (`app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)`) è **ibrido** (va bene per
pezzi e assiemi). Uno creato dall'interfaccia può essere una **parte** (un solo componente: niente assiemi). Controlla
`design.designIntent` (0 parte, 1 assieme, 2 ibrido) prima di creare componenti.

## Trappole verificate
| Trappola | Cosa succede | Cosa fare |
|---|---|---|
| Schizzo sul piano XZ | il punto (x, y) dello schizzo va in (x, 0, **−y**) nel modello; su YZ la X dello schizzo è la −Z | dai i punti in coordinate del modello e convertili con `sketch.modelToSketchSpace(P(x, y, z))` |
| Profili | l'ordine dei profili non è affidabile (il cerchio può venire prima dell'anello) | scegli per area (`areaProperties().area`), numero di anelli o posizione |
| Facce e spigoli | dopo ogni feature le facce vecchie **non esistono più**: riusarle dà «InternalValidationError : face» | ricercale dopo ogni feature, per geometria (piana, normale, quota, raggio) |
| Vincoli | l'API non aggiunge vincoli da sola; AutoConstrain non è disponibile (Personal) | ricette vincolate in `ricette.md`; controlla `sketch.isFullyConstrained` |
| `sketch.boundingBox` | è un po' largo (40.02 per 40) | misura le linee, non l'ingombro dello schizzo |
| `occurrence.boundingBox` | dà tutti zeri | usa l'ingombro dei corpi |
| Nomi tradotti | librerie e materiali hanno nomi in italiano («Plastica ABS») | sceglili per **codice** (`itemById("PrismMaterial-022")`) |
| Esportare un corpo nascosto | nessun file, ma `execute` dice «riuscito» | corpo visibile, poi controlla che il file esista e misuralo |
| Funzioni sbagliate a memoria | es. il 3MF si esporta con `createC3MFExportOptions` (non `create3MF…`) | copia dalle ricette o chiedi `apiDocumentation`; se la documentazione risponde vuota, il nome non esiste |
| Liste | alcune funzioni vogliono una lista Python (`createOffsetInput`, `meshConvertFeatures.createInput([mesh])`), altre un `ObjectCollection` | leggi la firma in `apiDocumentation` |
| Tavola aperta nascosta | `documents.open(df, False)` su una tavola **blocca Fusion** | apri le tavole visibili |
| Righe lunghe | l'adattatore del server ufficiale rovina le righe di uno script oltre ~4 000 caratteri (dato del progetto open source cadclamp, github.com/ChristianNHill/cadclamp) | righe corte; dati lunghi in file letti dallo script |
| Chiamate inventate | nelle prove del progetto cadclamp il 39 % degli errori in Fusion erano chiamate API che non esistono | prima di usare una funzione nuova: ricette, poi `apiDocumentation` o gli stub installati (`…\Api\Python\packages\adsk\*.py`) |
| Nomi che sembrano giusti | `d.sheetMetalRules` non esiste (è `designSheetMetalRules`); `FeatureControlFrameInput.firstFrame` non si riassegna; `backgroundType` della scena è di sola lettura | stesse regole: controllare la firma |
| Primitive del Solido | parallelepipedo, cilindro, sfera, toro: le classi (`BoxFeatures`…) **non hanno metodi di creazione** | schizzo + estrusione/rivoluzione |
| Raggio di piega in una regola di lamiera | `bendRadius.expression = "2.5 mm"` è **ignorata senza errore se il numero non cambia**: resta `Thickness`, e con uno spessore nuovo cambia anche il raggio | per fissarlo passa da un altro valore (`"4 mm"`, poi `"2.5 mm"`) e rileggi l'espressione; stesso giro per tornare a `Thickness` |
| Unità del DXF di lamiera | **leggere** `DXFFlatPatternExportOptions.units` fa fallire lo script: «Distance unit is not supported by DXF» | non leggerla; il DXF predefinito è già in mm, oppure assegnala senza leggerla (`MillimeterDistanceUnits`) |
| Spostare un componente via API | `occ.transform2 = M` funziona, ma senza fissarla **`computeAll` riporta il pezzo dov'era, senza errori** | subito dopo: `if d.snapshots.hasPendingSnapshot: d.snapshots.add()`; poi rimisura la posizione del corpo |
| Ruotare un giunto per provare un meccanismo | `computeAll` riporta il giunto a 0 senza errori: l'interferenza controlla la posizione di partenza e la prova passa **a vuoto** | niente `computeAll` fra `rotationValue` e la misura; rileggi l'angolo; prova anche un caso che deve urtare |
| Giunto ruotato che deve **restare** (assieme consegnato piegato, più giunti uno dopo l'altro) | senza cattura della posizione, **qualunque feature nuova o modificata lo riporta a 0 senza errori**: un altro giunto, un componente, un'estrusione cambiata (provato: 30° → 0°). Impostare solo altri `rotationValue`, salvare ed esportare **non** lo azzerano | dopo ogni `rotationValue` che deve restare: `if d.snapshots.hasPendingSnapshot: d.snapshots.add()` (provato: resta a 30°); alla fine rileggi tutti gli angoli. I pezzi portati da un giunto (un'elica sul braccio) vanno vincolati **prima** di muoverlo |
| Archi per tre punti concatenati in un profilo | `sketchArcs.addByThreePoints(p1, p2, p3)` tiene l'arco in senso antiorario: se i tre punti sono dati in senso orario, `startSketchPoint` è **p3**, non p1 (provato). Unendo le curve «fine con inizio» il profilo si chiude male (7 profili invece di 2 in un caso vero) | dopo ogni arco leggi dove sono davvero `startSketchPoint` ed `endSketchPoint`; conta `sk.profiles.count` prima di estrudere |
| Una chiamata che non finisce più | su un modello ricco (centinaia di schizzi o di facce: righe in rilievo, scritte, trame) uno script che tocca **tutto in una volta** (vincolare tutti gli schizzi, sonde o spessore su ogni faccia) tiene Fusion «Non risponde» per decine di minuti, con la memoria che sale a più GB (misurato: 28 minuti e 8 GB, lavoro perso dall'ultimo passo salvato) | **prima** di lanciarla conta quanti elementi tocca; sopra ~30, a pezzi (un componente o 20–30 elementi per chiamata) con il passo salvato fra un pezzo e l'altro; i dettagli decorativi (trame, zigrinature, scritte) si fanno **per ultimi**, dopo le verifiche, e si escludono dai controlli pesanti; se una chiamata supera 5 minuti, al giro dopo si dimezza il lavoro per chiamata. **Causa** (misurata su 58 schizzi, 210 elementi): ogni modifica a uno schizzo ricalcola tutta la timeline che lo segue; per vincolare schizzi vecchi porta prima il marcatore subito dopo lo schizzo (`schizzo.timelineObject.rollTo(False)`), modifica (0,4 s), poi `d.timeline.moveToEnd()` una volta per gruppo di 10: 2,5 minuti per 58 schizzi invece di un blocco a 8 GB |
| Tante chiamate pesanti di fila | interferenze fra tutte le coppie, proprietà fisiche ad alta precisione, spessore minimo, immagini: girano nel filo della finestra, Fusion risulta «Non risponde» per minuti e sembra bloccato | una chiamata alla volta, mai sessioni in parallelo; i controlli pesanti **una volta sola, alla fine**; se una chiamata va in timeout, controlla lo stato prima di ripeterla |
| Diametro di una ruota dentata letto dall'ingombro | se nessun dente sta sull'asse l'ingombro è più piccolo (83,913 per Ø 84) | raggio massimo dei vertici dal centro del foro; i denti si contano entrando nel materiale lungo un cerchio |
| Quote su punti allineati o cerchi concentrici | una seconda quota dall'origine verso un punto già allineato, o un secondo centro, viene rifiutata come ipervincolo | lega i punti con linee di costruzione verticali o orizzontali; il secondo cerchio usa `centerSketchPoint` del primo |
| Importare un `.f3d` in un assieme | `importToTarget2` crea un componente che contiene quello del file; in `allOccurrences` **il primo è quello annidato** | per spostare usa `r.occurrences`; i corpi cercali per nome in `allOccurrences` |
| Scegliere il profilo per area | «il più piccolo» è la corona se il rettangolo interno è grande (936 mm² contro 264): si taglia la cosa sbagliata senza errori | controlla il volume atteso nella stessa chiamata |
| Taglio passante da uno schizzo a metà del pezzo | `setAllExtent(SymmetricExtentDirection)` taglia **un lato solo**, senza errori (provato: 2 000 mm³ tolti invece di 4 000); `setOneSideExtent(ThroughAll, Symmetric)` dà errore | `ei.setTwoSidesExtent(ThroughAllExtentDefinition.create(), ThroughAllExtentDefinition.create())` e volume atteso nella stessa chiamata |
| Schizzo con un testo (`sketchTexts`) | resta «non vincolato» per Fusion anche con il riquadro (`definition.rectangleLines`) e tutti i punti vincolati (provato) | vincola il riquadro (un orizzontale, punto medio della diagonale sull'origine, larghezza e altezza); `rapporto_modello.py` lo conta vincolato solo se curve e punti lo sono |
| DXF per il taglio | il DXF predefinito contiene anche le linee di piega (strati `BEND`, `BEND_EXTENT`): un laser potrebbe tagliarle | per il solo contorno `isCenterLinesExported = False` e `isExtentLinesExported = False`; rileggi il file e conta le entità |

## Regole imparate dai registri di Fusion
Quando Fusion fa una cosa strana, la causa si trova nei suoi registri, non a tentativi:
`%LOCALAPPDATA%\Autodesk\Autodesk Fusion 360\<id>\logs\` (la cartella `<id>` scritta più di recente): `AppLogFile*.log` (cloud,
salvataggi, script MCP), `AcCore*.log` (il dialogo riga per riga dei comandi delle tavole), `FusionDrawing.log`.
- **Copia nascosta**: quando un disegno è aperto, Fusion carica una copia nascosta del progetto che usa, con lo **stesso nome**, in
  `app.documents`. Si riconosce perché `documentReferences` dà errore («non-top-level»). Salvarla risponde «riuscito» ma **non va mai nel
  cloud**. Regola: salvare solo documenti di primo livello e **dopo il salvataggio controllare che `dataFile.latestVersionNumber` sia salito
  di 1** (attendere qualche secondo); se no, fermarsi.
- **«Documenti recuperati»**: dopo una chiusura forzata Fusion riparte con questa finestra aperta; il server risponde a `initialize` ma
  **nessuno script parte**. Si chiude con un clic (non cancella nulla: resta in File → Recupera documenti). `ambiente.py` lo segnala.
- **Tavole**: i comandi dei simboli e della tabella fori **dettano risposte** a un comando del motore dei disegni; se una non è quella
  attesa il comando aspetta un clic e Fusion lo annulla dopo **600 s** (bloccato nel frattempo). Gli errori delle funzioni delle tavole
  **escono alla chiamata dopo**, non sulla riga sbagliata. Regole: un'operazione per chiamata, subito dopo una lettura (es.
  `drawingSymbols.count`), poi la coda di `AcCore*.log`: se l'ultima riga è una domanda senza risposta, dire all'utente la frase
  «Fusion aspetta un clic: premi Esc in Fusion, poi dimmi fatto» invece di aspettare 10 minuti.
- **Uscita persa dopo troppi script**: ogni script aggiunge uno strato a `sys.stdout` e nessuno lo toglie; dopo circa **368 script** nella stessa
  sessione di Fusion la risposta è `success: true` con messaggio **vuoto**, per qualunque script (misurato). `mcp_fusion.py` lo previene
  da solo e, se succede lo stesso, `esegui` lo dice invece di restituire «niente». Chi usa gli strumenti MCP nativi non ha questa protezione:
  se uno script che stampa torna vuoto, si usa `mcp_fusion.py` o si riavvia Fusion. In una sessione mai fidarsi di una risposta vuota.
- **Due documenti con lo stesso nome nel cloud**: scegliere per data (`dateCreated`) o identificativo, mai il primo della lista.
- **Lettura dei registri**: `scripts/registri.py comando` dice se un comando delle tavole è ancora in corso (`FusionDrawing.log`: inizio senza
  fine, non dipende dalla lingua); `dialogo` mostra domande e risposte; `salvataggi` gli invii al cloud. La riga «show recovery document»
  è in tutti i registri e non indica niente; la finestra «Documenti recuperati» non compare fra le finestre del sistema: si riconosce dal
  comportamento (`ambiente.py`: uno script di una riga non torna entro 25 s).

## Dopo un aggiornamento di Fusion
Fusion si aggiorna e si chiude da solo. Al riavvio `scripts/ambiente.py` confronta l'elenco degli strumenti con quello salvato: se è
cambiato, dillo all'utente prima di continuare, perché ricette e trappole potrebbero non valere più.
