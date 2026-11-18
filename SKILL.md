---
name: fusion-360
description: >-
  Progetta, modella, modifica e verifica in Autodesk Fusion (Fusion 360) attraverso il server MCP ufficiale Autodesk,
  come un progettista CAD professionista: pezzi meccanici, prodotti da riconoscere, oggetti nati da un'idea, case e
  stanze, mobili, gioielli, stampi, lamiera, assiemi che si muovono; da una richiesta a parole, una tavola quotata,
  foto, un file STEP/STL o un progetto esistente, fino al modello parametrico controllato, salvato in .f3d sul PC, con
  le uscite che servono (STEP, 3MF, DXF, G-code CNC, tavola PDF, immagini). Va usata quando si chiede di modellare in
  3D con Fusion, quando si parla di Fusion, e per modelli 3D, tavole tecniche, pezzi da copiare o riparare, percorsi
  CNC o lamiera quando non è indicato un altro CAD, anche senza nominare la skill (Fusion 360, CAD, sketch, extrude,
  STEP, drawing). Non per Rhino, FreeCAD, Blender, OpenSCAD, SolidWorks o altri CAD, né per
  slicing, schemi elettrici o PCB; la stampa 3D solo se l'utente la dichiara (con una skill di stampa, se installata).
---

# Fusion — progettare e modellare come un professionista

Chi chiede spesso non è un disegnatore CAD: descrive un oggetto, porta una tavola, una foto o un file. Il tuo lavoro è consegnare un
**modello giusto, modificabile e verificato**, spiegando in italiano semplice cosa hai fatto, con i numeri e il loro significato pratico
(«il foro è 3,4 mm: ci passa una vite M3»), e **cosa hai controllato e cosa no**.

Il rischio da avere sempre in mente: **Fusion può costruire un pezzo sbagliato senza dare nessun errore** (un foro che taglia via mezzo
pezzo, una nervatura che cresce dalla parte sbagliata, un salvataggio che risponde «riuscito» e non va da nessuna parte). Per questo ogni
passo ha un valore atteso calcolato *prima* e misurato *dopo*.

## Come parli con Fusion
- Strumenti MCP `fusion_mcp_*` del server ufficiale (indirizzo in `impostazioni.json`, predefinito `127.0.0.1:27182`); dagli script
  Python lo stesso server con `scripts/mcp_fusion.py`. Ogni script è **una transazione**; l'API lavora in **cm**. Dettagli, trappole e
  le regole imparate dai registri di Fusion: `references/connettore-e-api.md` — leggilo prima del primo script della sessione.
- Le impostazioni (cartella dei progetti, lingua, skill di stampa, cloud sì/no, porte da controllare) stanno in
  `%USERPROFILE%\.claude\fusion-360\impostazioni.json` (o nel file indicato dalla variabile `FUSION360_SKILL_IMPOSTAZIONI`):
  `python -X utf8 scripts/impostazioni.py --mostra`.
- Il codice non si scrive mai dentro un comando della shell: si scrive in un file e si lancia con
  `python -X utf8 scripts/esegui_file.py <file.py> [--sola-lettura] [--nuovo-documento]` (immagini, esportazioni, prove di
  flessibilità, riaperture); i passi del modello invece vanno con `scripts/progetto_locale.py` (es.
  `python -X utf8 scripts/progetto_locale.py <cartella> passo <nome> <file.py> --atteso <volume mm³>`). Il file contiene solo il
  codice: l'intestazione (nomi corti, `vol`, `out`, `controlla`) la aggiunge `mcp_fusion.py` (`references/ricette.md` §1).
- Lo schermo dell'utente non si tocca: si lavora via MCP. Solo per ciò che l'API non fa (es. chiudere una finestra di Fusion, cancellare
  un oggetto di una tavola) si usa lo schermo, **dicendolo prima**, e poi si smette.

## Il flusso (ogni passo ha un cancello)

**J0 Ambiente** — `python -X utf8 scripts/ambiente.py` (`--avvia` se Fusion è chiuso; mai una seconda copia). Deve dire
`si_puo_lavorare: true`. Se no, segui l'avviso: due Fusion aperti, server MCP spento (Preferenze → Generale → API), strumenti cambiati
dopo un aggiornamento (dillo all'utente), porta di un altro programma occupata da Fusion. **Se il server risponde ma gli script non
partono**, Fusion ha quasi certamente una finestra aperta (dopo una chiusura forzata: «Documenti recuperati») → frase per l'utente:
«Fusion ha una finestra aperta che blocca i comandi: chiudila (Chiudi), poi dimmi fatto».

**J1 Capire la richiesta e scegliere il ramo** — da un'idea, da una tavola, da una foto, da un file, modifica, architettura, assieme:
tabella dei rami in `references/metodo.md` §10, scenari in `references/scenari.md`. Scrivi la **specifica** (`assets/specifica.md`):
a cosa serve, con cosa si tocca, misure date o lette, l'*intento* in una frase («i fori restano a 12 mm dal bordo»). Le quote che
mancano **non si inventano**: domanda, valore proposto col perché, e ti **fermi**. Una misura letta in pixel è un'ipotesi.
Da un'idea: 4 fasi con una fermata dopo ognuna (domande → concetti con immagini → forma → dettaglio).

**J1b Produzione (solo se dichiarata)** — chiedi come verrà fatto il pezzo; **non presumere la stampa**. Stampa FDM → una skill di
stampa 3D, se installata (`skill_stampa` nelle impostazioni), **prima** di modellare, altrimenti le regole minime di
`references/produzione-e-stampa.md`; CNC, lamiera/laser, stampi → `references/produzione-e-stampa.md` §0.
Nessuna produzione → si consegnano `.f3d`, STEP, immagini (e tavola se chiesta).

**J1c Più pezzi nello stesso spazio** (custodie con elettronica, macchine, scocche): leggi `references/progetti-a-piu-pezzi.md`
**prima di disegnare**: bilancio degli spazi con i cavi, franchi, montaggio.

**J1d Oggetti da riconoscere** (un prodotto che esiste, un oggetto di design, «fammi un modello di…»): leggi
`references/forma-e-dettaglio.md` **prima delle domande**: livello di dettaglio concordato (mai scendere da soli: «forme semplificate»
è una domanda), riferimenti in scala, elenco degli elementi caratteristici, forma prima dei dettagli. Numeri giusti non bastano.

**J2 Piano e valori attesi** — componenti (prima della geometria, se ci sono parti che si muovono o si montano), **parametri** con nomi
di funzione, ordine: riferimenti → volumi pieni → tagli → modifiche → raccordi per ultimi. Calcola a mano gli **attesi**: volume dopo
ogni passo, ingombro, posizioni. Metodo: `references/metodo.md`; come calcolare: `references/verifica.md`.

**J3 Progetto** — `python -X utf8 scripts/nuovo_progetto.py "<nome>" "<descrizione>"` crea la cartella nella cartella dei progetti
delle impostazioni e la aggiunge all'elenco. Si lavora in un documento nuovo; **nel cloud non si salva** senza permesso (con la
licenza Personal, la più comune per uso personale, i posti sono 10: contali prima).

**J4 Modellazione a passi** — un passo = uno schizzo o una feature, con `scripts/progetto_locale.py` (esegue, misura, salva lo script
del passo, aggiorna registro e copia `.f3d`). Ogni script **controlla nella stessa chiamata** volume/ingombro/corpi contro l'atteso.
Usa il codice delle **ricette provate** invece dell'API a memoria; prima di una funzione nuova, cercala (ricette, `comandi.md`,
`apiDocumentation`): le chiamate inventate sono la prima causa di errore. Se una misura non torna, **cerca la causa**; non piegare il
modello al numero. Un errore trovato si corregge **da solo**, senza rifare tutto.

**J5 Verifica** — `scripts/rapporto_modello.py` (0 elementi in errore, 0 schizzi liberi, misure = attesi); **punti sonda** scritti dalla
specifica (`scripts/sonde.py`: volume, ingombro e baricentro non vedono un cerchio di fori sbagliato); assiemi: nessuna compenetrazione e
franchi misurati (interferenza 0 dice solo che i pezzi non si compenetrano: `scripts/controlla_pezzi.py`);
**spessore minimo** di ogni corpo (`scripts/spessore_minimo.py --limite <mm>`, limite scelto secondo la produzione e scritto nella
specifica: sotto il limite si ferma la consegna; «NON MISURATO» non è un via libera: misura in altro modo); per oggetti da appoggiare,
stabilità (`scripts/analisi_forma.py`); oggetti da riconoscere: i segni di forma povera (`scripts/segni_forma.py`) e le immagini accanto ai
riferimenti (`references/forma-e-dettaglio.md` §4); due immagini (iso e fronte) guardate davvero. `references/verifica.md`.

**J6 Flessibilità** — cambia 2–4 parametri importanti anche **lontano** dai valori iniziali, ricontrolla gli attesi, rimetti i valori.

**J7 Uscite** — secondo il ramo: 3MF controllato asse per asse (`scripts/controlla_mesh.py`), STEP, DXF dello sviluppo, G-code
controllato (`scripts/verifica_gcode.py`), PDF. Una risposta «riuscito» non basta: il file deve esistere e va rimisurato.

**J8 Tavola o render (solo se chiesti)** — `references/tavole-e-render.md`: 2 documenti nel cloud (permesso), un'operazione per
chiamata, simboli e tabella fori come immagini calcolate dalla vista (`scripts/tavola_simboli.py`), controllo di **cosa manca** e della
**leggibilità** sul PDF ingrandito. Se un comando delle tavole resta in attesa (`scripts/registri.py comando`): «Fusion aspetta un clic:
premi Esc in Fusion, poi dimmi fatto».

**J9 Consegna** — `.f3d` (versione nuova, mai sovrascritta), uscite, immagini, `resoconto.md` (`assets/resoconto.md`): cosa hai fatto,
i numeri e cosa significano, **fino a che livello hai verificato ogni cosa e cosa non hai verificato**.

**J10 Ripresa e correzioni** — lo stato del lavoro sta nel **registro del progetto** (fase, passo, attesi, domande aperte): domani, su
un altro PC o dopo che la conversazione è stata riassunta, si riparte da lì (`nuovo_progetto.py --cerca <parola>` per ritrovarlo).
Una correzione = un parametro o una feature alla volta, versione nuova. Un pezzo prodotto che «non entra»: prima si misura (3 letture),
e per la stampa si passa dalla skill di stampa, se installata.

## Dove ti fermi ad aspettare l'utente
Dopo le domande · dopo ogni fase del ramo «da un'idea» · dopo le decisioni di produzione · prima di sovrascrivere, cancellare o salvare
nel cloud · quando serve lo schermo · alla consegna. Fra questi punti lavora da solo, misurando ogni passo.

## Le trappole che danno pezzi sbagliati senza errori (le altre nei riferimenti)
- **Unità**: API in cm; quote come stringhe con unità (`"12 mm"`) o parametri.
- **Facce e spigoli** per geometria, mai per indice, e **cercati di nuovo** dopo ogni feature.
- **Schizzi**: l'API non li vincola da sola; su XZ la y dello schizzo è −Z (`modelToSketchSpace`).
- **Salvataggio**: con un disegno aperto Fusion tiene una copia nascosta del progetto con lo stesso nome; salvarla «riesce» ma non va
  nel cloud → dopo ogni salvataggio nel cloud controlla che la versione sia salita.
- **Tavole**: i comandi dei simboli si bloccano 600 s; gli errori escono alla chiamata dopo; niente si cancella via API.
- **Derive**: la geometria derivata si aggiorna (con `computeAll`), i **parametri derivati no**.
- **Esportazioni**: un corpo nascosto non viene esportato ma l'API dice «riuscito».
- **SVG**: Fusion legge le unità come pixel a 96 dpi (scala 96/25,4 per avere mm).
- **Licenza**: mai `purchase`, funzioni a credito o render nel cloud senza richiesta; con la licenza Personal (la più comune per uso
  personale) molte funzioni mancano o sono ridotte: `references/limiti-personal.md`.

## Riferimenti (aprili quando servono)
| File | Quando |
|---|---|
| `references/connettore-e-api.md` | prima del primo script: strumenti, unità, transazioni, trappole, regole dai registri |
| `references/ricette.md` §1 | l'intestazione degli script (`vol`, `out`, `controlla`) e come `progetto_locale.py` misura e registra un passo |
| `references/metodo.md` | J1–J2: intento, parametri, ordine, nomi, **i rami** (§10) |
| `references/scenari.md` | J1: i 19 usi di Fusion, ramo, ricette e limiti di ciascuno |
| `references/progetti-a-piu-pezzi.md` | più pezzi nello stesso spazio: bilancio degli spazi, franchi, tutte le coppie, montaggio, immagini ravvicinate |
| `references/forma-e-dettaglio.md` · `ricette-forma.md` | oggetti da riconoscere: livelli di dettaglio, riferimenti in scala, elementi caratteristici, segni di forma povera; ricette provate di forma (sezioni → loft → raccordi → guscio) |
| `references/verifica.md` | J2, J5: attesi, controlli nella stessa chiamata, spessore minimo, forma, scala delle verifiche |
| `references/ricette.md` | ricette essenziali (schizzi vincolati, fori, svasati, testo, ganci, ingranaggi, giunti, esportazioni) |
| `references/ricette-schizzi-e-piani.md` · `ricette-solidi.md` · `ricette-superfici-forme-lamiera.md` · `ricette-assiemi.md` · `ricette-modificare-importare.md` · `ricette-produzione-viste-render.md` | ricette provate, per famiglia |
| `references/ricette-decori-anelli.md` | testo su faccia curva, zigrinatura, serie su percorso, anelli |
| `references/ricette-stampi-mesh-pezzi.md` | stampi, mesh → solido, divisione in pezzi, scheletro con Derive |
| `references/ricette-lamiera-form-costruzione.md` | lamiera con sviluppo, T-spline, origini di giunto, aspetti, scena, costruzione, superfici, SVG |
| `references/ricette-foto-tavole.md` | foto in prospettiva raddrizzata; tavole con quote, riferimento, tolleranza, tabella fori |
| `references/ricette-cam.md` | CNC: utensili reali, contorno, post-processore, G-code controllato |
| `references/comandi.md` | i 1 665 comandi di Fusion: nome, identificativo, API, Personal, provato — **cerca, non leggere intero** |
| `references/dati-standard.md` | filettature, fori di passaggio, viti, dadi, inserti, cuscinetti (cerca) |
| `references/assiemi.md` · `produzione-e-stampa.md` · `modificare-importare-copiare.md` · `tavole-e-render.md` · `limiti-personal.md` | assiemi; produzione; file esistenti, foto, ripresa; tavole e render; licenza |

Gli script si lanciano con `python -X utf8 <script>` (senza UTF-8, su Windows i caratteri accentati rompono l'uscita).
