# Il metodo del professionista

## Perché serve un metodo
Un pezzo «della forma giusta» non basta: quando l'utente chiederà «allungalo di 10 mm» o «i fori più distanti», un modello costruito
male **si rompe senza errori**. Prova fatta: stessa piastra costruita da principiante (coordinate fisse) e da professionista
(parametri, vincoli, nomi), poi lunghezza 60 → 90 e spessore 5 → 8. Il principiante ha 0 errori di Fusion ma 2 violazioni dell'intento
(un foro a 38 mm dal bordo invece di 8, il perno fuori centro); il professionista 0. Nella ricerca (Camba et al. 2016, CAD 74) il metodo
ordinato «resiliente» (RMS) ha dimezzato o ridotto a un quarto i tempi di modifica (115 s contro 630 s non strutturato, esperimento 1).

## 1. L'intento, prima di tutto
Scrivi in una frase cosa deve restare vero se cambiano le misure: «i fori restano a 12 mm dall'estremo libero e simmetrici», «il perno
resta al centro». Proponila tu all'utente in parole semplici e chiedigli conferma: lui non conosce il termine, ma sa cosa gli serve.
Da lì discendono parametri e vincoli.

## 2. Parametri utente
- Un parametro per ogni misura di progetto, con **nome di funzione** (`spessore_parete`, `gioco_coperchio`, `interasse_fori`) e un
  commento sull'origine («da tavola», «dalla skill di stampa: gioco PETG»). Nomi senza spazi, mai simboli di unità.
- Le quote secondarie come **formule** dei parametri principali (`lunghezza_base - distanza_foro`, `interasse / 2`): una misura si
  cambia in un posto solo. Non mescolare numeri fissi e parametri nella stessa logica, ed evita riferimenti circolari.

## 3. Ordine della timeline (metodo resiliente)
1. **Riferimenti**: piani di costruzione a distanza parametrica, schizzi di layout.
2. **Volumi pieni** che danno la forma (estrusioni, rivoluzioni: sono la base del 90 % dei pezzi).
3. **Dettagli che tolgono materiale**: fori, tasche, asole — figli dei riferimenti e dei volumi, mai usati come riferimento da altro.
4. **Modifiche**: serie, specchi, sformi.
5. **Raccordi e smussi per ultimi**: un raccordo fatto presto si rompe quando cambia la geometria a valle.
Un trucco degli istruttori Autodesk: «lavora all'indietro» — immagina il pezzo senza raccordi e senza tagli, modella quello, poi aggiungi.

## 4. Schizzi
- Su piani d'origine o piani di costruzione parametrici, **non su facce** che possono cambiare (uno schizzo su una faccia proietta da solo
  i suoi bordi: nella prova il «perno» è nato sul cerchio di un foro proiettato).
- **Completamente vincolati** e ancorati all'origine: prima i vincoli (orizzontale, verticale, coincidente, simmetria, punto medio), poi
  le quote; le quote sono parametri. Uno schizzo vincolato è prevedibile, uno libero si deforma alla prima modifica.
- Molti schizzi piccoli, uno per funzione (profilo, fori, scarichi), invece di uno grande: si modificano e si riparano meglio.
- Geometria di costruzione per assi, simmetrie, allineamenti; la geometria «vera» solo per i contorni che diventano feature. Attento:
  una **mezzeria** (`isCenterLine`) divide i profili, una linea di **costruzione** no.
- Proiezioni con parsimonia, mai di spigoli raccordati o che cambiano.

## 5. Nomi
Schizzi, feature, corpi, componenti e piani con nomi per funzione (`SK_profilo`, `EST_base`, `TAGLIO_fori`, `RAC_interno`,
`PIANO_sopra`). Servono a te per ritrovarli negli script successivi e all'utente per capire la timeline.

## 6. Componenti
Se ci sono parti che si muovono, si montano insieme o vanno stampate separate, crea i **componenti prima della geometria** e lavora
dentro il componente giusto. Il primo componente di un assieme si fissa (meglio un giunto rigido all'origine che «fisso»).

## 7. Serie e simmetrie
Il seme della serie completamente vincolato; distanze e numeri come parametri; le serie di **feature** reggono meglio di quelle di
schizzo. Fori uguali: un solo comando foro su più punti di schizzo (vedi ricette).

## 8. Correzioni nella timeline
Una piccola correzione che non cambia la logica a monte si può fare **in fondo** (sposta una faccia, cancella una faccia e rifai il foro);
una correzione che cambia la logica va fatta **nella feature d'origine** (torna indietro nella timeline, modifica, torna in fondo).

## 9. Prova di flessibilità (alla fine di ogni pezzo)
Cambia 2–4 parametri chiave fino a valori realistici, ricalcola gli attesi, misura; poi rimetti i valori. Un errore di Fusion durante la
prova è un **segnale utile** (ti dice cosa sistemare); un pezzo sbagliato senza errori è il caso peggiore, ed è proprio quello che la
prova scopre.

## 10. I rami del lavoro (da dove parte la richiesta)
| Ramo | Come si procede | Ricette e prove |
|---|---|---|
| **Da un'idea** («mi fai un portapenne?») | 4 fasi con una **fermata** dopo ognuna: (1) domande — a cosa serve, con cosa si tocca, cosa subisce, come si fa (stampa solo se lo dice), ingombro e stile; (2) 2–3 concetti veloci con immagini; (3) forma: parametri, schizzo-scheletro, corpi, flessibilità; (4) dettaglio, spessore minimo, analisi della forma (raccordi, stabilità) | `verifica.md` |
| **Oggetto da riconoscere** (un prodotto che esiste, «fammi un modello di…») | livello di dettaglio concordato (ingombri / riconoscibile / dettagliato; mai scendere da soli), immagini ufficiali in scala, elenco degli elementi caratteristici mostrato con le domande, forma prima dei dettagli, segni di forma povera nel resoconto. Vale **insieme** al ramo Assiemi se ci sono più pezzi | `forma-e-dettaglio.md` |
| **Da una tavola** | si legge ingrandendo le viste; ogni quota in un registro «usata da» (una quota non usata = elemento mancante); le ambigue diventano domande | `ricette.md`, `ricette-solidi.md` |
| **Da una foto** | serve un riferimento di misura nota **sullo stesso piano** (foglio A4 misurato, carta di credito, righello); foto storta → raddrizzarla prima (`scripts/foto_prospettiva.py`), poi tela in scala vera; errore dichiarato; quote critiche dal calibro; senza calibro, un campione di prova | `ricette-foto-tavole.md` |
| **Da un file** STEP/STL/mesh | STEP: modellazione diretta; STL: con la licenza Personal (la più comune per uso personale) si converte solo «a faccette» (il metodo «prismatico» è rifiutato) → si **ricostruisce** da sezioni calcolate e curve adattate | `ricette-modificare-importare.md`, `ricette-stampi-mesh-pezzi.md` |
| **Modifica** di un progetto esistente | ritrovarlo nell'elenco dei progetti, riaprire l'ultima versione, cambiare **un** parametro o una feature alla volta, salvare una versione nuova | `modificare-importare-copiare.md` |
| **Architettura** (casa, stanza) | metri, muri da schizzo con spessori come parametri, aperture come tagli, pianta da DXF (il DXF non ha unità: fattore di scala) o da immagine come tela; tavola quotata | `tavole-e-render.md`, `modificare-importare-copiare.md` (tela in scala) |
| **Assiemi** e progetti su più file | più pezzi nello stesso spazio → prima `progetti-a-piu-pezzi.md`; componenti prima della geometria, giunti con limiti, nessuna compenetrazione e franchi misurati; scheletro in un file e pezzi **derivati**: si propaga la **geometria**, i parametri derivati no (ricontrollare dopo ogni modifica) | `ricette-assiemi.md`, `ricette-stampi-mesh-pezzi.md` |
| **Produzione** (solo se dichiarata) | stampa FDM → skill di stampa (`skill_stampa` in `impostazioni.json`); CNC → `ricette-cam.md`; lamiera/laser → sviluppo e DXF; nessuna → `.f3d` + STEP/immagini/tavola | `produzione-e-stampa.md` |
