# Assiemi: parti che si montano o si muovono

## Quando servono i componenti
Se ci sono parti che si muovono (cerniere, bracci, slitte), che si montano insieme (scatola e coperchio, supporto e scheda) o che si
stampano separate, ogni parte è un **componente**, creato **prima** della sua geometria e con un nome. I corpi bastano solo per un
pezzo unico. Il documento deve essere ibrido o assieme (un documento «parte» rifiuta i componenti).

## Creare e lavorare dentro un componente
`occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create()); occ.component.name = "Coperchio"`; la geometria si crea con gli
oggetti del **componente** (`occ.component.sketches`, `occ.component.features`); nel contesto dell'assieme si usano i proxy
(`entita.createForAssemblyContext(occ)`).

## Giunti (ricetta in `ricette.md` §12)
- Tipi provati: **rotante** (cerniere), **scorrevole** (slitte), **rigido**, gruppi rigidi, giunti «come costruito» (pezzi già in
  posizione). Cilindrico, pin-slot, planare, sferico: firme note, non provati.
- Il primo componente si fissa con un giunto rigido all'origine (o «fisso»).
- **Dopo ogni giunto**: posizione dei corpi = attesa e nessuna compenetrazione. Con le impostazioni predefinite un giunto fra la faccia di
  sotto di un pezzo e quella di sopra dell'altro ha **capovolto** il pezzo dentro l'altro senza errori → `isFlipped = True`.
- Movimento: imposta angolo o corsa e misura la trasformazione. **I limiti si impostano prima** (attivarli riporta il giunto a 0); un
  valore fuori dai limiti è ignorato in silenzio: rileggi sempre il valore.
- Verifica il movimento in più posizioni (es. un braccio ripiegato e aperto): nessuna compenetrazione in ognuna, e il gioco misurato.

## Collegare il moto di due giunti (ingranaggi, trasmissioni)
Una coppia di ruote non si trascina da sola: il rapporto si impone con un collegamento di moto.
```python
i_ = r.motionLinks.createInput(giunto_pignone, giunto_ruota)
i_.valueOne = S("54 deg"); i_.valueTwo = S("18 deg")   # per una coppia 18/54: 54° del primo = 18° del secondo
i_.isReversed = True                                   # ruote esterne: versi opposti
m = r.motionLinks.add(i_)                              # poi controlla m.healthState == 0
```
Provato con la licenza Personal: pignone a 30° → ruota a −10°; i collegamenti in catena si sommano (rapporto 12:1 esatto) e restano nel `.f3d`.
Il contatto fra i denti **non** viene calcolato: sei tu a imporre il rapporto e la fase. Controlla in più posizioni, senza `computeAll`, rileggendo gli
angoli (`connettore-e-api.md`). Prova che il controllo veda i denti: sospendi il collegamento (`m.isSuppressed = True`) e porta il pignone a mezzo passo:
deve urtare; rimetti poi tutto. Per una ruota con z pari di fronte a un pignone con un dente sull'asse, sfasa la ruota di mezzo passo (`fase = pi / z`).

## Parti comprate o di riferimento (schede, viti, motori)
- Schede elettroniche: il modello 3D ufficiale del produttore se esiste (STEP), altrimenti un blocco semplificato con le quote della
  tavola ufficiale (ingombro, fori, connettori con le loro altezze). Serve per controllare che la scatola non tocchi niente.
- Anche il modello di una parte comprata **non deve avere corpi uno dentro l'altro**: se fai scheda e piedini come corpi separati,
  la scheda ha i fori (o i piedini partono dalla sua faccia), oppure la parte è un corpo solo. Il controllo delle compenetrazioni
  va fatto su **tutti** i corpi, anche fra quelli dello stesso componente (caso reale: 19 piedini 0,64 × 0,64 attraverso una
  scheda da 1,6 senza fori = 12,452 mm³ di compenetrazione, trovata da un controllo automatico e non da chi aveva modellato).
- Viti, dadi, rondelle: misure dalle norme (`dati-standard.md`); filettature cosmetiche (non modellate in 3D) bastano per i controlli.
- Un file esterno si inserisce come componente collegato (`occurrences.addByInsert(dataFile, Matrix3D, True)`): richiede un file nel
  cloud, quindi preferisci importare lo STEP.

## Materiali, masse, visibilità
Materiali per codice (`ricette.md` §13); massa = volume × densità, controllala. Visibilità: `isLightBulbOn`, isolamento `isIsolated`.

## Misurare un assieme
Ingombro dai **corpi delle occorrenze** (l'ingombro dell'occorrenza dà zeri; i corpi letti dai componenti sono nelle coordinate del
componente, non dell'assieme): `scripts/rapporto_modello.py` lo dà in `assieme` (`ingombro_visibili`, `ingombro_tutti`,
`corpi_nascosti`; provato: 148 vero, 154 dai componenti, 196 contando i corpi nascosti). `scripts/spessore_minimo.py` misura
una volta i corpi ripetuti e dice quante occorrenze hanno. Interferenze e distanza minima fra **tutte** le coppie; nel resoconto la massa
totale e le interferenze volute (es. inserti a pressione) dichiarate. Più pezzi nello stesso spazio: `progetti-a-piu-pezzi.md`.
