# Specifica — {{NOME}} ({{DATA}})

{{DESCRIZIONE}}

## 1. A cosa serve e con cosa si accoppia
<!-- funzione del pezzo; parti con cui si monta (viti, schede, altri pezzi) con le loro misure e la fonte -->

## 2. Misure date o lette (con la fonte di ognuna)
| Misura | Valore | Fonte (utente / tavola / norma / produttore / calibro) |
|---|---|---|

## 3. Intento (cosa resta vero se cambiano le misure)
<!-- una frase semplice, proposta all'utente e confermata: es. «i fori restano a 12 mm dal bordo anche se allunghi la staffa» -->

## 3b. Forma e dettaglio (solo per oggetti da riconoscere: `references/forma-e-dettaglio.md`)
Livello concordato: 1 ingombri / 2 riconoscibile / 3 dettagliato — confermato dall'utente: sì / no
Riferimenti (da dove, quali viste, misura usata per la scala): …
| Elemento caratteristico | Dove si vede nel riferimento | Fatto |
|---|---|---|
<!-- togli questa sezione per i pezzi meccanici -->

## 4. Domande per l'utente (prima di modellare) e risposte
| Domanda | Proposta di Claude (con il perché) | Risposta dell'utente |
|---|---|---|
<!-- quote mancanti o ambigue: MAI inventate. Ci si ferma finché non risponde. -->

## 5. Produzione (solo se dichiarata dall'utente; altrimenti scrivi «nessuna»: si consegnano .f3d, STEP, immagini)
Come verrà fatto il pezzo: nessuna / stampa FDM / CNC / lamiera o taglio laser / stampo — `references/produzione-e-stampa.md` §0.
<!-- Solo per la stampa FDM: decisioni con la skill di stampa 3D, se installata (impostazione skill_stampa), o con l'utente -->
| Dato | Valore | Fonte |
|---|---|---|
| macchina / ugello / larghezza linea | | |
| materiale | | |
| orientamento (Z del modello = Z di stampa) | | |
| giochi degli accoppiamenti | | |
| fori | nominali, correzione nello slicer (salvo accoppiamenti critici) | skill di stampa / utente |
| inserti / viti / ganci | | |
<!-- Per CNC, lamiera, stampi: macchina, materiale, utensili o regola di piega, come in produzione-e-stampa.md §0; togli le righe che non servono -->

## 5b. Spessore minimo accettato (per `scripts/spessore_minimo.py --limite`)
Limite: … mm — perché (stampa: 2 linee dell'ugello; CNC/legno: dal materiale; nessuna produzione: 1 mm, dettagli decorativi dichiarati)

## 6. Parametri utente del modello
| Nome | Valore | Commento |
|---|---|---|

## 7. Valori attesi (calcolati PRIMA di modellare)
| Passo | Cosa si fa | Volume atteso (mm³) | Come è calcolato |
|---|---|---|---|
Ingombro finale atteso (x × y × z): …  ·  Posizioni da controllare: …
Tolleranze: quote 0.01 mm · volume del modello 0.01 % · volume della mesh 0.1 %.

## 8. Prova di flessibilità
Parametri da cambiare e valori attesi ricalcolati: …
