# Progetti a più pezzi: tutto deve stare, montarsi e funzionare

Leggilo quando più pezzi dividono lo stesso spazio: custodie con elettronica, macchine, veicoli, scocche, mobili con ferramenta.
Non serve per un pezzo singolo.

Il rischio: **ogni pezzo è giusto e l'insieme non funziona**. Il modello è valido, i volumi tornano, nessun errore, e poi la batteria non
esce, la spina non entra, la vite non si raggiunge. Nessun controllo su un pezzo solo lo trova.

## 1. Prima della geometria: il bilancio degli spazi
Elenca **tutto** ciò che deve stare nel volume: pezzo, connettori, cavi, spazio per le dita e per l'attrezzo. Usa misure vere: del
produttore o dell'utente. Se manca una misura, chiedila. Poi somma, direzione per direzione, e scrivi la somma nella specifica:

```
Spazio interno = somma(ingombro dei pezzi in fila) + somma(franchi) + spazio dei cavi
Spazio di un cavo = lunghezza connettore + R + d/2,   con R = k × d
Spazio per estrarre un pezzo = ingombro del pezzo + 2 × franco, lungo tutta la strada di uscita
Ingombro esterno = spazio interno + 2 × parete
```

- **Il cavo è un pezzo.** Una batteria da 60 mm con connettore da 10 mm e filo Ø 1,5 chiede 61 mm senza cavo e circa 81–87 mm con il
  cavo in fila. Se il cavo non è nel modello, nessun controllo lo vede: mettilo come solido, almeno il tratto che esce e il connettore.
- **k** per fasci di cavi: ≥ 10 è il valore prudente citato da una fonte di settore (non universale); vale il dato del produttore se c'è.
- **Spine, attrezzi, connettori volanti**: la misura vera è dell'utente; se non può misurare, assumi un valore prudente e **dichiaralo**.
- **Non ci sta?** Non stringere in silenzio: dì quale pezzo o quale vincolo lo impedisce e proponi cosa spostare.

## 2. L'ordine del lavoro
1. Bilancio degli spazi e disposizione **a numeri**, approvati dall'utente, con immagini degli ingombri come semplici blocchi.
2. **Una** passata di forma attorno alla disposizione. Se la forma non convince, misura le proporzioni e controlla prima la disposizione:
   spesso è lei la causa, e rifare la superficie non la cambia.
3. Sedi, fissaggi, aperture. Dettagli per ultimi.
4. **Rileggi la specifica prima di ogni fase.** Le decisioni prese sono vincoli: se un numero spinge a cambiarne una, dillo e chiedi.

## 3. Franchi: «interferenza 0» non basta
| Risultato | Cosa significa davvero |
|---|---|
| Nessuna interferenza | i pezzi non si compenetrano; può darsi che si **tocchino** (le facce a contatto sono escluse, salvo chiederle) |
| Volume zero, con le facce coincidenti incluse | si toccano |
| Volume positivo | urto vero, oppure sovrapposizione voluta: dichiarala |
| **Distanza minima ≥ franco deciso** | **questo è il criterio** |

- Il franco si **decide** e si scrive nella specifica. Per la stampa FDM 0,5 mm è un punto di partenza per il montaggio, non un valore
  universale (la skill di stampa dà i dettagli).
- Gli appoggi voluti (scheda sulle colonnine, vite nella sede) sono eccezioni **dichiarate una per una**.
- Misura ogni coppia con `app.measureManager.measureMinimumDistance(a, b)`, anche fra corpi: dà la distanza e i due punti, cioè dove guardare.
- `d.createInterferenceInput(corpi)` con `areCoincidentFacesIncluded = True`: i contatti risultano a volume 0, gli urti col loro volume
  (`x.interferenceBody.volume`). Provato in un progetto parametrico. Non usare `createBodies`: secondo l'esempio ufficiale funziona solo in modellazione diretta.

## 4. Il controllo di tutte le coppie
Dopo ogni feature che tocca un pezzo, e alla fine: **tutte le coppie**, non solo quelle che pensi si tocchino (n pezzi = n(n−1)/2 coppie;
7 pezzi = 21). Il difetto più comune è in una coppia a cui non avevi pensato.

```
python -X utf8 scripts/controlla_pezzi.py --franco 1 --appoggi "*/albero*:*/ruota*,cuscinetto*:guscio*" [--giunto NOME --angoli 0,30,90]
```
Dà urti (con volume e punto), contatti e franchi sotto il limite (con i due punti); OK solo se ogni contatto o franco piccolo è dichiarato.
Dichiara solo ciò che è voluto: albero nel foro, cuscinetto nella sede, vite sulla flangia, **ruote in presa** (il gioco fra i denti è ~0,1 mm).
Con `--giunto` prova il meccanismo in più posizioni. Su un riduttore di 31 corpi: circa 1 minuto per posizione.

## 5. Il montaggio, scritto
Scrivi la sequenza nella specifica, passo per passo, e per ogni passo controlla:
- **Entra ed esce**: il pezzo ha una strada in linea retta, con il franco per tutta la corsa, senza dover smontare ciò che non deve
  essere smontato? Provalo con copie temporanee, senza toccare il modello: `t = adsk.fusion.TemporaryBRepManager.get()`, `cb = t.copy(pezzo)`,
  `cs = t.copy(altro)`, `t.transform(cb, M)`, `t.booleanOperation(cb, cs, adsk.fusion.BooleanTypes.IntersectionBooleanType)`; un volume maggiore
  di 0 è un urto (`cb.volume` solo se `cb.faces.count` non è 0). Ripeti a passi lungo tutta la corsa.
- **Attrezzo**: per ogni vite, lungo il suo asse, c'è spazio per l'attrezzo con la mano e per la testa della vite? Una sede si progetta
  insieme all'accesso, non solo al foro.
- **Uso**: porte e pulsanti si raggiungono a oggetto chiuso, con la spina vera e non solo con il connettore della scheda? Cosa si cambia
  spesso si raggiunge senza attrezzi o con poche viti?
- **Regole di comodità** (da letteratura sul montaggio, fonte secondaria): montare lungo un asse, in genere dall'alto; una parte si
  posiziona prima di essere lasciata; evitare di girare l'insieme a metà; pochi tipi di vite; dove si può, incastri al posto delle viti.

## 6. Stampabilità pezzo per pezzo
Se si stampa, ogni pezzo ha il suo orientamento, deciso **mentre lo disegni**: sporgenze, ponti, fondi sospesi, fori sul bordo di una
colonnina, e cosa tocca il piatto. Le regole sono della skill di stampa. Ciò che scende sotto il piano d'appoggio di un pezzo spesso va staccato.

## 7. Guardare da vicino
I numeri confermano, non sostituiscono: un foro che sbuca fuori dal suo bordo è geometria valida, e passa volume, interferenza e sonde.
- Dopo ogni dettaglio, un'immagine **ravvicinata di quel dettaglio**: nella vista d'insieme un difetto di 1 mm non si vede.
- **Viste in sezione** per le cavità: nascondi i corpi che coprono.
- **Copie uguali** (4 bracci, 4 piedi): confronta 2 immagini fra loro, la differenza salta all'occhio.
- Mostra le immagini all'utente **insieme** ai numeri: la forma si giudica solo lì.

## 8. Se una zona è intrecciata nella timeline
Una modifica che rompe feature lontane non si insiste a rattoppare, e non si rifà tutto il progetto:
misura la geometria esistente, concorda cosa si rifà, ricostruisci **solo quella zona**. Poi ripeti §3 e §4.

## 9. Cosa dire alla consegna
Oltre al resoconto normale: il bilancio degli spazi, la tabella delle coppie con la distanza minima e le eccezioni dichiarate, la
sequenza di montaggio con cosa è stato controllato a calcolo. **Niente di tutto questo sostituisce il montaggio vero**: dillo.
Curvatura dei cavi, forze sui fissaggi e resistenza non sono coperti da questi controlli.
