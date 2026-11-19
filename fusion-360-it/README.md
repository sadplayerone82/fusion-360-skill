🇬🇧 English version: [../README.md](../README.md)

# fusion-360-it — skill per Claude Code (versione italiana)

> **Italian-language version of the `fusion-360` skill for Claude Code, which drives Autodesk Fusion through its official MCP server.
> The English version is in the `fusion-360` folder of this repository: install only one of the two.**
>
> It turns a request (words, a dimensioned drawing, photos, a STEP/STL file or an existing project) into a parametric Fusion model
> that is built step by step, measured after every step against values computed beforehand, and saved as a local `.f3d` file with
> the outputs you need (STEP, 3MF, DXF, CNC G-code, PDF drawing, images) and a written report of what was and was not checked.
> Windows only; works with the Fusion Personal licence. Instructions, messages and reports are in Italian.

Questa skill fa lavorare Claude in **Autodesk Fusion** come un progettista CAD: dalla richiesta al **modello parametrico controllato**,
salvato in un file `.f3d` sul PC, con un resoconto che dice che cosa è stato verificato e che cosa no.

**Provata con Claude Opus. Con modelli più piccoli (Sonnet, Haiku) non è ancora stata provata.**

Il repository contiene due versioni della stessa skill: `fusion-360/` in **inglese** (nome `fusion-360`) e questa cartella,
`fusion-360-it/`, in **italiano** (nome `fusion-360-it`). **Installane una sola**: fanno la stessa cosa e non vanno installate insieme.

La skill **non è affiliata ad Autodesk** né approvata da Autodesk. «Autodesk» e «Fusion» sono marchi dei rispettivi proprietari.

## Che cosa fa
- **Modella** pezzi meccanici, custodie per schede elettroniche, oggetti nati da un'idea, prodotti da riconoscere, mobili e stanze,
  gioielli, stampi, lamiera, **assiemi** che si muovono (giunti).
- **Parte da** una richiesta a parole, una tavola quotata (immagine o PDF), foto, un file STEP, STL o DXF, oppure un progetto esistente
  da modificare.
- **Lavora a passi misurati**: per ogni passo calcola prima il valore atteso (volume, ingombro, posizioni) e lo confronta con quello
  misurato in Fusion. Se un numero non torna cerca la causa invece di andare avanti.
- **Chiede** le misure che mancano invece di inventarle, e si ferma ad aspettare le risposte.
- **Consegna** il `.f3d` (versione nuova, mai sovrascritta), le uscite che servono (STEP, 3MF, DXF, G-code CNC controllato, tavola
  PDF, immagini) e un `resoconto.md`.
- **Rispetta la licenza Personal**: sa quali funzioni sono a pagamento (`references/limiti-personal.md`), non compra niente, non usa
  crediti e salva nel cloud solo con il tuo permesso.

**Per chi è**: per chi usa Fusion e vuole far fare a Claude il modello (o una modifica) con controlli veri; anche per chi non è un
disegnatore CAD e descrive l'oggetto a parole.

**Che cosa NON fa**
- Non funziona senza Fusion aperto sul PC e senza il suo server MCP: non è un CAD a sé.
- Non fa slicing per la stampa 3D, schemi elettrici né circuiti stampati.
- Non è pensata per altri programmi CAD (Rhino, FreeCAD, Blender, OpenSCAD…).
- Non garantisce che un pezzo prodotto funzioni: il resoconto dice fin dove è arrivata la verifica; prove e misure sul pezzo vero
  restano a te.

## Un esempio
Richiesta, in Claude Code con Fusion aperto:

> mi fai in Fusion una piastra 60 × 40 × 5 con due fori da 6 a 8 mm dai bordi corti?

Che cosa succede:
1. Claude controlla che Fusion e il server MCP rispondano.
2. Fa le domande che servono (per esempio: fori passanti? centrati sull'altezza? il pezzo come verrà prodotto?) e **aspetta**.
3. Scrive la specifica e i valori attesi: volume pieno 60 × 40 × 5 = 12 000 mm³; ogni foro Ø 6 passante toglie π × 3² × 5 ≈ 141,4 mm³,
   quindi il pezzo finito misura ≈ 11 717,3 mm³.
4. Crea la cartella del progetto e modella a passi (schizzo, estrusione, fori), misurando dopo ogni passo.
5. Verifica: schizzi vincolati, nessun elemento in errore, posizioni dei fori, spessore minimo; poi cambia i parametri principali per
   vedere che il modello resta giusto, e li rimette com'erano.
6. Consegna, nella cartella del progetto: `consegna\AAAA-MM-GG-piastra-v1.f3d` (il nome della cartella del progetto, con la data del giorno) e lo STEP accanto, due immagini (iso e fronte), `resoconto.md` con la tabella
   «atteso / misurato / esito» e l'elenco di ciò che non è stato controllato.

Altre richieste tipiche:
- «ti allego la tavola (PDF): rifammi il pezzo in Fusion» → legge le quote, chiede quelle che mancano, confronta il volume.
- «ho questo STEP, rifallo parametrico» → ricostruisce il pezzo e confronta la forma con lo STEP.
- «fammi un modello del mouse X, che si riconosca» → concorda prima il livello di dettaglio e vuole immagini di riferimento in scala.
- «mi serve un supporto per questa scheda, con la scheda dentro» → assieme con la scheda come componente, giochi misurati, nessuna
  compenetrazione.

## Requisiti
| Cosa | Versione | Note |
|---|---|---|
| Windows | 10 o 11 | Avvio di Fusion, finestre e registri sono scritti per Windows. Su macOS non è provata. |
| Autodesk Fusion | recente, con il **server MCP ufficiale** | Provata con le build 2706.1.x (ottobre–novembre 2026). Il server si accende in Preferenze → Generale → API. Fusion si aggiorna da solo: vedi «Risoluzione dei problemi». |
| Licenza di Fusion | Personal va bene | La skill evita le funzioni a pagamento. Con la Personal il cloud ha 10 posti: la skill salva i progetti come file `.f3d` sul PC; solo le tavole 2D usano 2 documenti nel cloud, e solo con il tuo permesso. |
| Python | **3.11 o più recente** | Lo richiede scipy 1.16. Pacchetti in `scripts/requirements.txt` (numpy, Pillow, scipy). |
| Claude Code | recente | Provata con il modello Opus; con modelli più piccoli non è stata provata. |
| git | facoltativo | Se c'è, ogni progetto ha il suo storico locale (niente invii in rete). |
| Una skill di stampa 3D | facoltativa | Usata solo se dichiari che il pezzo va stampato in FDM. Non è inclusa: senza, la skill applica le regole minime di `references/produzione-e-stampa.md`. |

## Installazione
I comandi sono scritti in due versioni: **PowerShell** (`$env:USERPROFILE`) e **Prompt dei comandi, cmd** (`%USERPROFILE%`).
Usa quella della finestra che hai aperto.

**1. Scarica il repository** (pulsante «Code» → «Download ZIP» ed estrai, oppure `git clone`).

**2. Copia la cartella `fusion-360-it` nella cartella delle skill di Claude Code**, **senza** la sua cartella `evals/` (contiene i
casi di prova per chi sviluppa la skill: a Claude non servono). Lancia il comando **dalla cartella del repository scaricato, quella
che contiene `README.md`, `fusion-360` e `fusion-360-it`**:

PowerShell:
```powershell
robocopy fusion-360-it "$env:USERPROFILE\.claude\skills\fusion-360-it" /E /XD evals __pycache__
```
cmd:
```bat
robocopy fusion-360-it "%USERPROFILE%\.claude\skills\fusion-360-it" /E /XD evals __pycache__
```
**Non** copiare anche `fusion-360`: si installa una sola delle due versioni. Se avevi installato l'altra (o una versione precedente
di questa skill in `.claude\skills\fusion-360`), cancella prima quella cartella.
robocopy finisce con un riepilogo; i codici d'uscita da 0 a 7 vogliono dire «riuscito».

**3. Accendi il server MCP in Fusion**: Preferenze → Generale → API → attiva il server MCP di Fusion. Gira solo sul tuo PC, sulla
porta 27182.

**4. Collega Claude Code al server** (comando uguale in PowerShell e in cmd):
```
claude mcp add --transport http --scope user autodesk-fusion http://127.0.0.1:27182/mcp
```
Poi riavvia Claude Code. `claude mcp list` deve mostrare `autodesk-fusion`.

**5. Entra nella cartella della skill installata** (i passi seguenti si lanciano tutti da qui):

PowerShell:
```powershell
cd "$env:USERPROFILE\.claude\skills\fusion-360-it"
```
cmd:
```bat
cd /d "%USERPROFILE%\.claude\skills\fusion-360-it"
```

**6. Installa i pacchetti Python** (controlla prima con `python --version` che sia 3.11 o più recente; se `python` non c'è, prova `py`):
```
python -m pip install -r scripts\requirements.txt
```

**7. Crea le impostazioni**, cioè la cartella dove finiranno i progetti:

PowerShell:
```powershell
python -X utf8 scripts\impostazioni.py --crea --cartella-progetti "$env:USERPROFILE\Documents\Progetti-Fusion"
```
cmd:
```bat
python -X utf8 scripts\impostazioni.py --crea --cartella-progetti "%USERPROFILE%\Documents\Progetti-Fusion"
```
Il file si chiama `impostazioni.json` e sta in `.claude\fusion-360\` dentro la tua cartella utente, **fuori** dalla skill: una
reinstallazione non lo cancella. `python -X utf8 scripts\impostazioni.py --mostra` lo mostra. Se non hai una skill di stampa 3D,
aprilo con un editor di testo e metti `"skill_stampa": null`.

**8. Controlla l'ambiente**, con Fusion aperto:
```
python -X utf8 scripts\ambiente.py
```
Deve rispondere `"si_puo_lavorare": true`. Alla prima volta avvisa che manca l'elenco degli strumenti: è normale, vedi il passo 9.

**9. Una volta sola, con Fusion aperto**, salva l'elenco degli strumenti del server MCP. Serve ad accorgersi, dopo un aggiornamento di
Fusion, se gli strumenti sono cambiati:
```
python -X utf8 scripts\ambiente.py --salva-strumenti
```

`-X utf8` serve: senza, su Windows le lettere accentate rompono l'uscita degli script.

## Prima prova
Apri Fusion e, in Claude Code, scrivi:

> mi fai in Fusion una piastra 60 × 40 × 5 con due fori da 6 a 8 mm dai bordi corti?

Che cosa aspettarsi: Claude fa le domande che servono e si ferma; dopo le tue risposte crea la cartella del progetto nella cartella
delle impostazioni, modella a passi misurando ogni passo e consegna `.f3d`, immagini e `resoconto.md` (vedi «Un esempio» qui sopra).
Se il volume finale è vicino a 11 717 mm³ (con fori Ø 6 passanti) e il resoconto elenca i controlli fatti, l'installazione funziona.

## Risoluzione dei problemi
| Che cosa vedi | Che cosa fare |
|---|---|
| `ambiente.py` dice che il server MCP non risponde | Fusion deve essere aperto, una copia sola. Controlla Preferenze → Generale → API (server MCP acceso, porta 27182). Controlla `claude mcp list`. Dopo aver aggiunto il server, riavvia Claude Code. |
| Il server risponde ma gli script non partono | Quasi sempre Fusion ha una finestra aperta che blocca i comandi. Dopo una chiusura forzata Fusion riparte con la finestra **«Documenti recuperati»**: chiudila (Chiudi) e riprova. |
| Fusion «Non risponde» durante un calcolo lungo | Su modelli ricchi (centinaia di schizzi, scritte, trame) un'operazione fatta su tutto in una volta può bloccare Fusion per decine di minuti. Aspetta: chiuderlo a forza fa perdere il lavoro dall'ultimo passo salvato. La skill sa che va lavorato a gruppi: `references/connettore-e-api.md`, tabella delle trappole, riga «Una chiamata che non finisce più». |
| Un comando delle tavole 2D resta in attesa | Fusion aspetta un clic: premi Esc in Fusion e riprova. |
| `ambiente.py` avvisa che gli strumenti MCP sono cambiati | Fusion si è aggiornato da solo e il server potrebbe essersi comportato diversamente: alcune ricette potrebbero non valere più. Prova un pezzo semplice (la piastra); se va, rilancia `ambiente.py --salva-strumenti`. Se qualcosa si rompe, apri una segnalazione (vedi «Contribuire»). |
| Lettere accentate sbagliate o errori di codifica | Lancia gli script con `python -X utf8`. |

## Validazione
La skill è stata provata in Fusion (licenza Personal, novembre 2026, modello Opus), su casi veri:
- **pezzi da tavole quotate**, cioè disegni tecnici con le quote, anche con quote mancanti da chiedere;
- **pezzi da file STEP** dei casi di prova pubblici del NIST (l'ente statunitense degli standard), confrontando la forma con lo STEP;
- **assiemi** con giunti (cerniera, riduttore a due stadi) e **custodie** per schede elettroniche (Raspberry Pi 4, Arduino Uno,
  ESP32), con la scheda inserita come componente;
- lamiera, CNC con G-code, una stanza da una pianta DXF, la modifica di un STL, un oggetto da un'idea;
- **oggetti da riconoscere** (un mouse, un drone), giudicati da una persona guardando le immagini accanto a quelle ufficiali.

Ogni caso aveva valori da controllare decisi prima (volumi, ingombri, posizioni, numero di componenti, nessuna compenetrazione,
schizzi vincolati, file d'uscita validi), misurati sul modello consegnato.

Esiti, senza abbellimenti:
- Casi usati durante lo sviluppo: 11 superati su 11, con una sola esecuzione per caso. Messa a confronto con Claude senza la skill:
  alla pari su 4 casi semplici; sul riduttore a due stadi 18 controlli su 18 con la skill e 12 su 18 senza (senza la skill il modello
  non aveva giunti e non si muoveva). Una sola esecuzione per condizione: un indizio, non una prova statistica.
- Prima serie di 11 pezzi nuovi, al primo tentativo: **8 superati su 11**. Non superati: un anello da STEP (una quota presa dalla
  tavola invece che dal 3D), un supporto per scheda (piedini dentro la scheda) e un drone giusto nei numeri ma respinto sulla forma
  («una scatola con barre»).
- Dopo le correzioni, seconda serie:

  | Caso | Esito |
  |---|---|
  | Pezzo complesso da STEP (139 facce), al primo tentativo | 11 controlli su 11, forma identica allo STEP |
  | Anello da STEP + tavola, rifatto | 11 su 11 (ora chiede quale fonte vale) |
  | Supporto per scheda ESP32, rifatto | 9 su 9 |
  | Mouse ergonomico, oggetto mai visto | 10 su 10, **approvato** dalla persona sulle immagini |
  | Drone pieghevole, rifatto | 12 su 14, **non superato**: molto meglio del primo, ma meccanismi non progettati (cerniere senza fine corsa né scatti, gusci senza interno, gimbal senza motori, niente vista esplosa) |

- Dopo il drone la skill chiede anche il **livello funzionale** (solo aspetto o funzionante: `references/forma-e-dettaglio.md`).
  Questa regola non è ancora stata provata con un nuovo drone.

## Limiti
- I numeri giusti non garantiscono la forma: per gli oggetti da riconoscere il giudizio finale è di chi guarda le immagini.
- Meccanismi realistici (cerniere con scatti, interni, motori) in oggetti complessi: sono il punto più debole (vedi il drone).
- Tavole 2D: servono 2 documenti nel cloud (con il tuo permesso) e alcuni comandi possono bloccare Fusion (la skill dice come uscirne).
- Forme libere via script: provate con sezioni ellittiche e contorni ricalcati, loft, raccordi e guscio; T-spline solo da primitive.
- Modelli molto ricchi: alcune operazioni fatte tutte insieme bloccano Fusion per minuti; la skill lavora a gruppi.
- Fusion in una lingua diversa dall'italiano è stato provato poco o per niente: alcuni controlli leggono i nomi dei comandi.
- Provata solo su Windows e solo con il modello Opus.
- Fusion cambia con gli aggiornamenti automatici: ricette e trappole sono state misurate su una versione precisa.
- Lingua: istruzioni, messaggi e resoconti in italiano.

## Licenza
MIT, testo completo nel file [`LICENSE`](../LICENSE) alla radice del repository.

Copyright (c) 2026 sadplayerone82

I file d'ingresso di terzi usati negli esempi di `evals/` non sono coperti da questa licenza: le fonti e le condizioni sono in
`evals/LEGGIMI.md`.

## Contribuire
Segnalazioni e proposte sono benvenute, come «issue» del repository. Per un problema allega, se puoi:
- un file `.f3d` o STEP d'esempio che lo mostra (senza dati riservati);
- il `resoconto.md` della skill e, se c'è, il `registro.json` della cartella del progetto;
- l'uscita di `python -X utf8 scripts\ambiente.py` e, se Fusion si è bloccato, di `python -X utf8 scripts\registri.py dialogo`
  (le ultime righe dei registri di Fusion);
- la versione di Fusion (Guida → Informazioni) e il tipo di licenza (Personal o commerciale).

Chi modifica la skill trova i casi di prova in `evals/` (vedi `evals/LEGGIMI.md`). Una modifica va fatta in tutte e due le versioni. Le novità di ogni versione sono in [`CHANGELOG.md`](../CHANGELOG.md)
alla radice del repository.
