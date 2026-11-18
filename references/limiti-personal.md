# Licenza Fusion «Personal»: cosa c'è e cosa no

Questo file vale per la licenza **Personal** (uso personale, non commerciale: la più comune per uso personale). Se non sai che
licenza ha l'utente, chiediglielo o leggila con `fusion_mcp_read` (`{"queryType": "licensing"}`). Con la licenza Personal, prima di
proporre una funzione controlla qui: proporre una cosa che poi non funziona, o che costa, fa perdere fiducia e tempo. Con una licenza
commerciale molti limiti qui sotto non valgono (non provato con questa skill): dillo all'utente quando conta.

## Dalla pagina ufficiale Autodesk (confronto Personal / commerciale, letta a ottobre 2026)
Nella Personal sono **limitati**: CAM, elettronica e PCB, **documentazione 2D e tavole**, **tipi di file in importazione ed esportazione**;
la gestione dei dati è per un solo utente. Sono **solo nella versione a pagamento**: tavole e modellazione **automatizzate**,
**configurazioni**, **distinta base (BOM)**, **render nel cloud**, simulazioni nel cloud.

## Cosa è stato verificato dal vero
| Funzione | Esito con la Personal |
|---|---|
| Modellazione solida, superfici, forme libere, lamiera (anche sviluppo e DXF), assiemi e giunti | funziona |
| AutoConstrain (vincoli automatici) | **non disponibile** («user is restricted») → i vincoli li scrive lo script |
| Lamiera: giunzione per piega, chiusure d'angolo in sovrapposizione | non disponibili |
| Esportazione 3MF, STEP, STL, archivio `.f3d`; importazione STEP, STL, `.f3d` | funziona |
| Render **locale** | funziona (gratis); quello nel cloud è a pagamento |
| Tavola automatica | funziona ma in versione ridotta: solo 3 quote d'ingombro; le altre quote vanno aggiunte o messe dall'utente |
| Documenti nel cloud | **solo 10** modificabili (i file nel cestino contano finché non si svuota) → i progetti si salvano come `.f3d` sul PC |
| Mesh → solido «Prismatic» (cilindri e piani riconosciuti) | **negato** («No rights for mesh conversion», provato); solo «a faccette» → ricostruire da sezioni (`ricette-stampi-mesh-pezzi.md`) |
| CAM | funziona per 2–3 assi; i **rapidi sono rallentati** alla velocità di lavoro (scritto nel G-code) |
| Simulazione, progettazione generativa | **non disponibili** («aggiorna ad abbonamento», provato) → calcoli a mano dichiarati |
| Esploso e video AVI (animazione) | funzionano dall'interfaccia, non dall'API |
| Distinta e palloncini nelle tavole | palloncini senza API; distinta solo nella tavola automatica di un assieme |

## Cosa non ha API (si fa a mano o in altro modo)
Forme T-spline da schizzo, bridge e riparazione (ci sono solo le primitive, l'inserimento di spigoli e i file TSM); primitive del Solido
(si usano schizzo + estrusione); ciclo colori dei componenti della vista; cancellare o spostare oggetti delle tavole.

## Regole che ne derivano
- **Mai** `purchase`; **mai** `editImage` o `generatePowerpoint` (consumano crediti) senza una richiesta esplicita dell'utente.
- **Mai salvare nel cloud** senza permesso: un documento nel cloud occupa uno dei 10 posti. Una tavola 2D occupa **2 posti** (il
  progetto da cui nasce e la tavola stessa, `tavole-e-render.md`): chiedi il permesso, riusa se puoi due documenti di prova come
  versioni nuove, esporta il PDF; le cancellazioni nel cloud le fa l'utente.
- Se una richiesta richiede una funzione a pagamento (distinta automatica, configurazioni, render nel cloud), dillo subito e proponi
  l'alternativa gratuita (tabella scritta nel resoconto, varianti come parametri, render locale).
