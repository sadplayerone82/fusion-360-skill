# Casi di prova (evals)

Questa cartella serve a **chi sviluppa o modifica la skill**: ogni sottocartella è un caso di prova, cioè una richiesta realistica
con le risposte da dare alle domande di Claude e i valori che il modello consegnato deve avere. Si usano per controllare che una
modifica alla skill non peggiori i risultati.

A Claude, durante l'uso normale, non servono: **non copiarla** nella cartella delle skill (il README dice come escluderla).

## Com'è fatta una cartella
| File | Che cosa contiene |
|---|---|
| `prompt.md` | La richiesta dell'utente, così come la scriverebbe. In cima, fra due righe `---`, alcune indicazioni per l'esecuzione (numero massimo di turni, tempo massimo in secondi, strumenti permessi). In fondo, `Input files:` elenca i file d'ingresso. |
| `risposte.md` | Le risposte dell'**utente simulato**. Si danno **solo dopo** che Claude ha fatto le sue domande, mai insieme alla richiesta: il caso controlla anche che Claude chieda le misure che mancano invece di inventarle. Coprono le domande prevedibili; per le altre di solito c'è una riga «per il resto decidi tu e dichiaralo». |
| `attesi.json` | I valori controllati sul modello consegnato, per esempio volume e ingombro in mm³ e mm, interassi, numero minimo di componenti, file da consegnare. Le chiavi cambiano da caso a caso. |
| `case.yaml` | Nome del caso e `expected_outcome`, cioè il risultato atteso descritto a parole: che cosa deve esserci e che cosa si valuta. |
| `place-files.sh` | Copia il contenuto di `files/` nella cartella di lavoro prima dell'esecuzione (script bash; su Windows si lancia da Git Bash, oppure si copiano i file a mano). |
| `files/` | I file d'ingresso: tavole, STEP, STL, DXF, PDF. Può essere vuota (richiesta solo a parole) o da riempire a mano (vedi «Fonti dei file d'ingresso»). |
| `graders/` | Solo in alcuni casi: criteri da valutare leggendo la consegna e il resoconto, uno per file (per esempio «ha chiesto il quarto foro», «le colonnine formano un rettangolo 58 × 49»). |

## Come si esegue un caso
**Non ci sono strumenti automatici inclusi** per eseguire i casi e valutarli: si fanno a mano.

1. Installa la skill (vedi il README) e apri Fusion.
2. Crea una cartella di lavoro vuota e copiaci il contenuto di `files/` del caso (o lancia `place-files.sh` da quella cartella).
3. Apri Claude Code nella cartella di lavoro e incolla il testo di `prompt.md`, senza l'intestazione fra le righe `---`.
4. Quando Claude fa le domande, rispondi con il contenuto di `risposte.md`. Se chiede qualcosa che lì non c'è, rispondi come direbbe
   l'utente del caso e annotalo.
5. Alla consegna confronta il modello con `attesi.json` (misure nel resoconto di Claude, ricontrollate in Fusion), rileggi
   `expected_outcome` di `case.yaml` e, se ci sono, i criteri di `graders/`.
6. Annota l'esito controllo per controllo, con il numero misurato; per gli oggetti da riconoscere il giudizio sulla forma lo dà una
   persona guardando le immagini.

Alcune richieste contengono segnaposti come `<stampante dell'utente>`: sostituiscili con una stampante vera prima di usarle. I casi che
dichiarano la stampa 3D funzionano meglio con una skill di stampa installata (facoltativa, non inclusa). I casi di oggetti da
riconoscere chiedono immagini ufficiali del prodotto in una cartella `riferimenti/`: non sono incluse, vanno scaricate dal sito del
produttore.

## Fonti dei file d'ingresso
I file di terzi qui sotto **non sono coperti dalla licenza MIT** della skill.

### NIST — inclusi
Casi `esame-09-nist-ftc11` (FTC 11) e `esame-09b-nist-ctc01` (CTC 01): modelli STEP e tavole PDF dei casi di prova del NIST
(National Institute of Standards and Technology), progetto «MBE PMI Validation and Conformance Testing».
- Pagina ufficiale: https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/mbe-pmi-0
- Opera del governo degli Stati Uniti: pubblico dominio negli USA. La pagina dice che casi di prova, modelli CAD e file STEP si
  possono usare senza restrizioni, chiede di citare il NIST quando si usano e precisa che l'uso non implica un'approvazione del NIST
  (il logo del NIST non va usato).

### Raspberry Pi 4 Model B — non incluso
Caso `scatola-raspberry-pi-4`: disegno meccanico ufficiale della Raspberry Pi 4 Model B.
- Pagina ufficiale (Raspberry Pi Product Information Portal): https://pip.raspberrypi.com/categories/545
- File: https://pip-assets.raspberrypi.com/categories/545-raspberry-pi-4-model-b/documents/RP-008343-DS-1-raspberry-pi-4-mechanical-drawing.pdf
- Salvalo in `files/` con il nome `raspberry-pi-4-meccanico.pdf`.

### Arduino Uno R3 — non incluso
Caso `supporto-arduino-uno`: scheda tecnica ufficiale (datasheet) dell'Arduino UNO R3, codice A000066.
- Pagina ufficiale: https://docs.arduino.cc/hardware/uno-rev3/
- File: https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf
- Salvalo in `files/` con il nome `arduino-uno-r3-datasheet.pdf`. Il disegno è nella sezione «Board Outline & Mounting Holes»; nelle
  versioni più recenti del PDF può stare a una pagina diversa da quella citata nella richiesta.

### Espressif ESP32-DevKitC V4 — non incluso
Caso `esame-11-esp32`: dimensioni ufficiali della scheda ESP32-DevKitC V4, in PDF e DXF.
- Pagina ufficiale (guida della scheda, sezione dei documenti collegati):
  https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- File: https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.pdf e
  https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.dxf (circa 4 MB)
- Salvali in `files/` con gli stessi nomi: `esp32_devkitc_v4_dimensions.pdf` e `esp32_devkitc_v4_dimensions.dxf`.

**Prima di usare uno di questi tre casi**, scarica i file dalle pagine ufficiali e mettili nella cartella `files/` del caso con i nomi
indicati: la richiesta in `prompt.md` li cita con quei nomi.

Gli altri file d'ingresso presenti nella cartella (per esempio lo STL, il DXF della pianta, il modello `.f3d`) sono stati creati per
questi casi e ricadono nella licenza della skill.
