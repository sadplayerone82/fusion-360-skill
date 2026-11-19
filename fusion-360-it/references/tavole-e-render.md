# Tavole 2D, immagini realistiche, animazioni (solo se l'utente le chiede)

## Tavola tecnica 2D — cosa funziona via API (provato)
- **Cloud**: la tavola si crea dal file del progetto **nel cloud** e la tavola stessa è un documento nel cloud → occupa **2 posti** (con
  la licenza Personal, la più comune per uso personale, i posti modificabili sono 10). Chiedi il permesso; meglio riusare due documenti di prova come **versioni nuove** che crearne altri.
- **Creazione**: `DrawingManager.createDrawingInput(dataFile, modo)`; la modalità manuale vuole un modello `.f2t`, quella automatica a
  volte esce **senza viste** (successo con un progetto fatto di un solo componente importato) → le viste si aggiungono con
  `sheet.views.createBaseViewInput()` + `views.add` (solo viste di base; scala e stile **dopo** la creazione). Coordinate del foglio in
  **mm** (la guida dice cm: misurato, sono mm).
- **Quote native**: `drawingDimensions.addLinearDimension(p1, p2, posizione)` e `addDiameterDimension(curva, posizione)` funzionano;
  le curve della vista si trovano per geometria (`viewCurves`: `centerPoint` per cerchi e archi — anche un cerchio visto di taglio —,
  `midPoint` per le rette). Unità, decimali, virgola e zeri si impostano in `documentSettings`.
- **Non si cancellano né si spostano via API**: viste, quote, simboli, immagini (`DrawingDimension` ha solo `type`). Un errore si toglie
  **a mano** sullo schermo (dirlo prima all'utente), poi si rimette giusto via API.
- **Simboli GD&T e tabella fori nativi**: inaffidabili (anteprima). Il riferimento e la tabella fori si bloccano 600 s; il riquadro di
  tolleranza a volte va, a volte si associa male. Si fanno come **immagini** (`sheet.images`, opache, larghe 58 mm × scala, posizionate
  dall'angolo in basso a sinistra) con i valori **calcolati dalle curve della vista**, mai scritti a mano: `scripts/tavola_simboli.py`
  (tabella, riferimento, riquadro; `--r-max` decide quali cerchi sono fori). Le correzioni si fanno sovrapponendo un'immagine giusta.
  `sheet.images` non ha `count`: le immagini si contano nel PDF esportato (`page.get_images`). Su una tavola **riaperta**
  `view.scaleValue` dà errore: la scala va passata (`--scala`), mai supposta.
- Linee dello schizzo del foglio con estremi vicini vengono unite a zig-zag: per tratteggi e segni piccoli, immagini.
- Le tabelle personalizzate native non mostrano il testo; il cartiglio accetta solo nome e posizione degli attributi.

## Controllo della tavola (prima di dire «fatto»)
1. **Cosa manca**: elenco di ciò che la tavola deve avere — ingombri, diametri, spessori, fori (tabella o quote), riferimenti e
   tolleranze se richiesti, cartiglio — spuntato voce per voce.
2. **Leggibilità**: nessun testo sotto una linea o sopra un bordo; due diametri concentrici su diagonali diverse con il testo fuori dal
   pezzo; testo non più piccolo di quello delle quote; tabelle in scala con il foglio.
3. **PDF guardato ingrandito**, zona per zona (`exportManager.createPDFExportOptions`): non basta «pdf: true».
4. Le tavole si aprono **visibili** (aperta nascosta, una tavola blocca Fusion).

## Immagini realistiche (render)
- **Solo locale** (il render nel cloud è a pagamento): `startLocalRender(file, camera)`, qualità 25 per le prove, 75 per l'utente;
  asincrono → aspetta che il file esista e controlla la risoluzione.
- Scena: `design.renderManager.sceneSettings` — l'ambiente si sceglie assegnando `backgroundEnvironment` (il tipo di sfondo è di sola
  lettura e cambia da solo; l'ambiente si legge solo con sfondo d'ambiente); pavimento e riflessi con `isGroundDisplayed`,
  `isGroundReflections`.
- Aspetto per **codice** o cercando nella libreria «aspetti» (nomi tradotti); assegnabile all'**occorrenza** (lo ereditano i corpi).

## Animazioni ed esplosi
`d.animationManager.activateAnimationWorkspace()` → `storyboards.add()`; poi torna all'ambiente di progettazione. Esploso e video AVI
funzionano (anche con la licenza Personal) ma **dall'interfaccia** (provato a schermo); nell'API non ci sono: dirlo all'utente.
