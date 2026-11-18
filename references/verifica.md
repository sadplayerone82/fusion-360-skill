# Verifica: come si scopre un pezzo sbagliato

## Perché
Fusion costruisce pezzi sbagliati **senza errori**. Casi visti nelle prove:
- foro Ø25 in un blocco largo 20: il cerchio divide il profilo in due e l'estrusione ne tiene **metà** (1 801.1 mm³ invece di 3 602.2);
- raccordo più grande dello spessore: costruito lo stesso, facce mangiate;
- nervatura con la direzione predefinita: cresce **fuori** dal pezzo (11 272 mm³ invece di 9 300);
- giunto con le impostazioni predefinite: il pezzo si capovolge **dentro** l'altro (interferenza 4 000 mm³).
Nessuno di questi dà un messaggio. Solo il confronto con un valore calcolato prima li fa vedere.

## 1. Valori attesi, prima di modellare
- **Volume dopo ogni passo**, con formule semplici: blocchi, cilindri (π r² h), corone, raccordi (area (1 − π/4)·r² per lunghezza;
  attorno a un cilindro con il teorema di Pappo), smussi (triangoli), coni (π h/3 (R² + Rr + r²)), inviluppi di cerchi (settori +
  tangenti). Quando una forma è complicata, calcola in **due modi diversi** (formula e poligono fitto) e confrontali.
- **Ingombro** (x, y, z), **posizioni** dei fori e degli elementi che contano, numero di corpi.
- Scrivili nella specifica (`assets/specifica.md`): sono il metro con cui controlli ogni passo.

## 2. Dopo ogni passo (`progetto_locale.Progetto.passo`)
Misura volume, corpi, elementi della timeline, elementi in errore; confronta con l'atteso. Tolleranze: quote **0.01 mm**, volume del
modello **0.01 %**, volume della mesh esportata **0.1 %**.
Se non torna: **cerca la causa misurando** la geometria (raggi e quote delle facce cilindriche, ingombri). Nelle prove una volta
era sbagliato il calcolo (la lamatura usciva dal bordo della base), un'altra la lettura della tavola (uno smusso che avrebbe bucato la
parete). Correggi ciò che è sbagliato davvero; non piegare il modello al numero.

## 3. Rapporto del modello (`scripts/rapporto_modello.py`)
Dice: tipo di documento e unità; parametri; elementi della timeline in errore (con il messaggio); schizzi non completamente vincolati;
per ogni corpo: solido, visibile, volume, ingombro (`dimensioni_mm`), facce, materiale, massa. Il cancello: **0 elementi in errore,
0 schizzi liberi**, corpi tutti solidi e visibili, misure = attesi. Il rapporto trova davvero un elemento in errore (provato: schizzo
di base cancellato → l'estrusione risulta in errore con il messaggio di Fusion).

## 4. Assiemi
Dopo ogni giunto e alla fine: interferenza fra le coppie di componenti (`analyzeInterference`) = 0, salvo quelle volute e dichiarate;
posizione dei corpi rispetto all'atteso. **Non basta**: 0 dice solo che i pezzi non si compenetrano, possono toccarsi. Dove serve spazio,
misura il franco di ogni coppia (`references/progetti-a-piu-pezzi.md` §3).

## 5. Guardare il pezzo
`viewport.fit()` e poi due immagini (`iso-top-right` e `front`) con `fusion_mcp_read screenshot`. Guardale davvero e confrontale con
la tavola o con la richiesta: il numero giusto con la forma sbagliata succede (es. un pezzo specchiato).

## 6. File per la stampa
`python -X utf8 scripts/controlla_mesh.py pezzo.3mf --atteso-mm X Y Z --atteso-volume-mm3 V`: file esistente, unità, mesh chiusa e con
normali coerenti, misure **asse per asse** (un pezzo ruotato non passa, salvo `--qualsiasi-orientamento`), volume. Applica le
trasformazioni del 3MF. Esce con 1 se qualcosa non va.

## 6b. Controlli nella stessa chiamata
Ogni script di un passo misura e confronta **prima di finire**: l'intestazione degli script (`mcp_fusion.corpo`) ha
`controlla(corpo, volume=…, ingombro=[x, y, z], n_corpi=…)` in mm e mm³, tolleranze 0,01 % e 0,01 mm (dettagli in `ricette.md` §1).
L'ingombro viene dal `boundingBox` dell'API: su corpi curvi può essere un po' largo, quindi un ingombro bocciato di pochi centesimi
si ricontrolla misurando gli estremi veri prima di cambiare il modello. Se non torna lo script fallisce con
«CONTROLLO FALLITO: …» e **nel documento non resta nulla** del passo (provato: 0 corpi, 0 schizzi, timeline vuota; un documento
creato dallo script stesso invece resta aperto). L'errore si vede nella stessa chiamata: meno chiamate = meno tempo (in un progetto
esterno, 5 chiamate invece di 30 per lo stesso pezzo).

## 6b-bis. Punti sonda (`scripts/sonde.py`)
Volume, ingombro e baricentro **non vedono tutto**. Provato su una flangia con 4 fori: cerchio dei fori R 32 invece di R 30, oppure fori
ruotati di 45°: volume, ingombro e baricentro **identici** a quelli giusti; le sonde li bocciano (8 mutanti su 8 presi, flangia vera
57 sonde su 57). Scrivi le sonde **prima di modellare**, dalla specifica: per ogni foro `{"nome", "centro", "diametro"}` (9 punti, a metà
spessore), per ogni bordo un punto dentro e uno fuori. La sensibilità è il margine: con 0,5 mm un foro Ø 9,4 invece di Ø 9 passa, con 0,1
è bocciato; le quote strette si misurano. Una sonda su una faccia esce come «bordo»: è la sonda da spostare.

## 6b-ter. Programmi CNC (`scripts/verifica_gcode.py`)
Controlla G21/G90, mandrino, avanzamento, **profondità**, che la fresa non morda il pezzo e **non passi dentro il pezzo** (contorno dal
lato sbagliato: la distanza dal bordo è la stessa dentro e fuori, quindi solo questo controllo lo vede), che **ogni contorno** (esterno,
ogni foro) sia percorso, rapidi sotto la cima. Provato: 9 programmi rovinati su 9 bocciati, ognuno col motivo giusto, più 2 programmi veri
col lato sbagliato (fori Ø 8 lavorati da fuori, piastra 146 × 96), bocciati. `dx`, `dy` = origine del CAM
(grezzo +10 per lato con origine sull'angolo: 10, 10). Non simula l'asportazione né le collisioni del portautensile: dillo.

## 6c. Spessore minimo e forma (prima di ogni consegna)
- `python -X utf8 scripts/spessore_minimo.py --limite <mm>` misura per ogni corpo la distanza minima fra facce opposte; sotto il
  limite dice «FERMARE LA CONSEGNA». Il limite si **sceglie sempre** secondo la produzione e si passa con `--limite` (non affidarti al
  valore predefinito dello script): stampa 3D: 2 linee dell'ugello (es. 0,8 con ugello 0,4); legno/CNC:
  dal materiale; senza produzione, solo per vedere o per render: `--limite 1`, e i dettagli decorativi sotto il limite si dichiarano.
  È obbligatorio: in un progetto vero il difetto più grave (una parte troppo sottile) l'aveva visto l'utente, non le altre verifiche. Limite: le punte acute arrotondate non le misura. Negli assiemi misura un corpo per
  chiamata e i corpi ripetuti una volta sola (`occorrenze`, `secondi_per_pezzo`); una parte comprata sottile (un piedino da 0,64)
  fa scattare il limite: si spiega nel resoconto, non si nasconde.
- `python -X utf8 scripts/analisi_forma.py [--carico m,x,y,z]`: continuità degli spigoli (G0/G1/G2), raggi dei raccordi, **stabilità**
  (baricentro, base d'appoggio, margine e angolo di ribaltamento). Per oggetti da appoggiare o con un carico (supporti, porta-oggetti).
  Per gli **oggetti da riconoscere** la quota di spigoli vivi (G0 sul totale) è uno dei segni di forma povera: `forma-e-dettaglio.md` §4.

## 6d. Scala delle verifiche (cosa dire nel resoconto)
Per ogni controllo, il livello più alto raggiunto: **chiamata tornata** → **esiste** (corpo, file) → **geometria** (misure = attesi) →
**andata e ritorno** (file riaperto/reimportato e rimisurato). E l'elenco di **cosa non è stato verificato**, col perché. Una risposta
«ok» di Fusion non è una prova: è il primo gradino.

## 7. Flessibilità e resoconto
Prova di flessibilità (`metodo.md` §9) e resoconto finale: cosa hai controllato, **con quale numero**, dove; cosa non hai controllato.
Mai «è tutto a posto» senza questo elenco.
