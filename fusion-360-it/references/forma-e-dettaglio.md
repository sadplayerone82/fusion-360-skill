# Forma e livello di dettaglio: oggetti da riconoscere

Leggilo **prima delle domande** quando la richiesta è un oggetto che esiste o che deve «sembrare» qualcosa: un prodotto di marca
(un drone, un telefono, un elettrodomestico), un veicolo, un mobile di design, un personaggio, un oggetto da presentare. Non serve
per staffe, flange e pezzi meccanici squadrati: lì gli spigoli vivi sono giusti.

**Perché esiste**: un assieme può avere ingombri, giunti e franchi perfetti ed essere una scatola con quattro barre. Caso reale: un
drone con tutti i numeri giusti, fatto di 22 estrusioni su 25 feature, 81 % di spigoli vivi e nessuna superficie curva libera, non si
riconosceva a colpo d'occhio. I numeri di `verifica.md` non vedono la forma: qui ci sono le regole che la riguardano. Le soglie sono
**avvisi tarati su un solo modello**: il giudizio finale è dell'utente, sulle immagini.

## 1. I tre livelli di dettaglio
| Livello | Cosa si vede | Quando |
|---|---|---|
| **1 Ingombri** | blocchi con le misure giuste | solo se l'utente chiede «solo ingombri» o «un segnaposto» |
| **2 Riconoscibile** | la sagoma segue i riferimenti nelle viste disponibili; superfici curve dove l'oggetto è curvo; spigoli raccordati come nell'oggetto; tutti gli elementi caratteristici | valore normale per un oggetto che esiste |
| **3 Dettagliato** | in più i particolari secondari: feritoie, sensori, viti, linee di giunzione, scritte, pulsanti | l'utente dice «dettagliato», «fedele», «realistico» |

- Il livello si **scrive nella specifica** e si conferma con l'utente nelle domande.
- **Non si scende di livello da soli.** «Forme semplificate» è una domanda, mai una scelta: si scrive cosa si perde («i bracci
  saranno barre dritte, non rastremate») e ci si ferma. Una risposta generica dell'utente («decidi tu») **non** autorizza a scendere.
- Se tempo o strumenti non bastano per il livello chiesto, si dice **prima** di cominciare, non nel resoconto.

## 1b. Prodotti con meccanismi: aspetto o funzionamento?
Un prodotto vero (drone, gimbal, cerniera, pieghevole) non è solo una sagoma: un disegnatore professionista **ingegnerizza** le
parti che si muovono. Esempio: un drone pieghevole con la forma giusta non basta se ha bracci su semplici supporti, senza nulla che
regoli apertura, verso, blocco aperto e chiuso; nessun esploso; scocca piena invece di gusci con la batteria e l'interno come pezzi a
parte; gimbal senza motori; attacchi diversi dall'originale (lì i motori del gimbal stanno nelle estensioni della scocca ai suoi lati).
Quindi, nelle domande, chiedi **anche il livello funzionale**, oltre a quello di dettaglio:
| Livello funzionale | Cosa si modella |
|---|---|
| **A Aspetto** | gusci e parti esterne, giunti solo per muovere la vista |
| **B Funzionante** | ogni meccanismo progettato: cerniera con perno, battute di fine corsa, scatto o fermo nelle posizioni d'uso, verso di apertura; gusci con spessore e giunzioni; parti interne principali come pezzi a parte (batteria, motori, schede); motori dove servono (gimbal); un **esploso** dell'assieme |
Per un prodotto con parti mobili proponi **B** e, se l'utente sceglie A, scrivilo nel resoconto come limite. Gli attacchi si
copiano dall'originale guardando i riferimenti (dove sono i motori, come gira la cerniera), non si inventano.

## 2. Prima di modellare
1. **Riferimenti**: immagini ufficiali del produttore in almeno 2 viste (fianco e alto, o fianco e fronte) e le misure pubblicate.
   Se non puoi averle, **chiedile**: senza riferimenti il livello 2 non si promette. Foto di terzi: solo come integrazione dichiarata.
2. **In scala**: ogni immagine come tela calibrata su una misura vera (`modificare-importare-copiare.md`, righe sulla tela;
   foto storte: `ricette-foto-tavole.md`). Una misura letta dall'immagine resta un'ipotesi, con il suo errore.
3. **Elenco degli elementi caratteristici**: guardando i riferimenti, scrivi nella specifica ciò che fa riconoscere l'oggetto
   (esempio per un drone pieghevole: muso inclinato, bracci che si assottigliano, piedini, sensori, prese d'aria, vano batteria,
   gimbal con i suoi assi). Di solito 6–12 voci al livello 2, di più al 3. L'elenco va **mostrato all'utente con le domande**.
4. **Proporzioni**: dalle tele ricava i rapporti principali (lunghezza/altezza della scocca, posizione dei perni, rastremazioni) e
   mettili nei parametri; se una stima è tua, dichiarala.

## 3. Ordine di lavoro (dal grosso al fine)
riferimenti in scala → volumi con le misure pubblicate → **forma** → dettagli → raccordi piccoli per ultimi.
- **Forma** vuol dire: profili ricalcati sulle tele e uniti con loft o sweep, rivoluzioni, raccordi grandi, rastremazioni: codice
  provato in **`ricette-forma.md`** (sezioni vincolate → loft → tondi → raccordi → guscio; via script riesce). Per le
  superfici organiche le T-spline (`ricette-superfici-forme-lamiera.md`, `ricette-lamiera-form-costruzione.md`). Via API le
  T-spline si guidano con numeri (primitive, spigoli inseriti, descrizione TSM), non con il «tira e spingi» a mano: poche facce,
  simmetria attiva, modifiche piccole.
- **Prova prima su un pezzo solo** (il più caratteristico): se loft o forma non riescono, lo scopri subito. I loft possono
  autointersecarsi e l'ingombro può mentire: controlla volume e immagine a ogni passo.
- **Un'estrusione da sola non è una forma**: va bene come volume di partenza, non come pezzo finito di un oggetto curvo.
- A ogni fase un'immagine **dalla stessa vista del riferimento**, guardata accanto al riferimento. Dove ci si può fermare
  (`SKILL.md`, «Dove ti fermi»), la si mostra all'utente prima dei dettagli.

## 4. Segni di forma povera (avvisi, da mettere nel resoconto)
I primi tre li misura `python -X utf8 scripts/segni_forma.py [--file modello.f3d]` (avvisi S1, S2, S3; provato su un cubo, un cubo
raccordato e il drone a blocchi estrusi descritto sopra).
| Segno | Come si misura | Avviso |
|---|---|---|
| S1 Spigoli vivi | spigoli con le due facce a più di 1° / tutti gli spigoli | sopra il 50 % |
| S2 Solo estrusioni | feature di forma (loft, sweep, rivoluzioni, forme) + raccordi e smussi, per componente | 0 in un componente che nell'oggetto vero è curvo |
| S3 Poche facce piane | facce di ogni corpo e quota di area piana | sotto 12 facce **e** almeno il 50 % di area piana (un guscio liscio con 10 facce va bene) |
| Elementi caratteristici | presenti / elencati (§2.3) | sotto il 100 % |
| Sagoma | immagine del modello accanto al riferimento, stessa vista | differenze visibili a colpo d'occhio |

Un avviso non è una bocciatura: si **spiega** («il motore è un cilindro anche nella realtà») oppure si corregge. Tacerlo no.

## 5. Nel resoconto
Livello concordato · riferimenti usati (da dove, quali viste) · elenco degli elementi caratteristici con fatto/non fatto ·
i segni del §4 con i numeri · immagini del modello accanto ai riferimenti · cosa è stima tua · cosa manca per il livello sopra.
