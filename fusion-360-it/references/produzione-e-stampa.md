# Produzione: stampa 3D, CNC, lamiera e taglio (solo se l'utente la dichiara)

La produzione **non si presume**: si chiede come verrà fatto il pezzo (fase 1 del metodo). Se non verrà prodotto, si consegna il `.f3d`
con STEP, immagini ed eventuale tavola.

## 0. Quale ramo
| Produzione dichiarata | Cosa fare | Dove |
|---|---|---|
| **Stampa FDM** | decisioni di stampa con una skill di stampa 3D, se installata (`skill_stampa` in `impostazioni.json`), **prima** di modellare; §1–5 qui sotto | — |
| **CNC** (fresa, legno, alluminio) | grezzo, utensili **reali** dalle schede del produttore (JSON), percorsi 2D/2,5D, post-processore della macchina scelto per nome, G-code controllato (contorno, raggio utensile, profondità) | `ricette-cam.md` |
| **Lamiera, taglio laser/plasma** | componente di lamiera con la regola (spessore, raggio, K), sviluppo misurato contro la formula π/2·(R + K·T) per piega a 90°, DXF dello sviluppo | `ricette-lamiera-form-costruzione.md` |
| **Stampo / colata** | stampo in due metà con sformo, chiavi, colata e sfiati | `ricette-stampi-mesh-pezzi.md` |

Se la skill di stampa non è installata: regole minime (pareti ≥ 2 linee dell'ugello, fori al diametro nominale, gioco 0,2–0,3 mm sul
raggio per un accoppiamento scorrevole) e lo si dice all'utente.

## Stampa 3D con la skill di stampa
Una skill di stampa 3D (facoltativa) sa di materiali, giochi, orientamento, slicer; questa skill sa disegnare. Se è installata si
lavora insieme: lei decide i numeri di stampa, tu li metti nel modello come parametri. Le domande di stampa si fanno **una volta sola**
(le fa lei). Se non c'è, valgono le regole minime qui sopra e le tabelle qui sotto, e i numeri che mancano si chiedono all'utente.

## 1. Il contratto (J1b, prima di modellare)
Da chiedere alla skill di stampa (o all'utente) e riportare nella specifica, ognuno con la sua fonte:
| Dato | Per cosa serve nel modello |
|---|---|
| macchina, ugello, larghezza della linea | spessori delle pareti = multipli della linea (pareti fragili sotto 2 linee) |
| materiale (PLA, PETG, ASA…) | giochi, ganci (deformazione ammessa), resistenza al calore |
| **orientamento di stampa** | il modello si disegna con Z = Z di stampa; sporgenze e ponti nei limiti; dove vanno i fori orizzontali |
| giochi per tipo di accoppiamento (scorrevole, a pressione, coperchio) | parametri `gioco_*` del modello |
| regola dei fori | fori al **diametro nominale**: la correzione la fa lo slicer (`xy_hole_compensation`); solo per un accoppiamento critico il gioco diventa parametro, dicendolo |
| inserti a caldo, viti nella plastica, ganci | misure dalle tabelle sotto (complete in `dati-standard.md`) o dalla skill di stampa |
Il gancio a scatto si calcola con la formula di `ricette.md` §10 (spessore dalla deformazione ammessa del materiale).

## 2. Viti e fori (valori come in Fusion, norme ISO; mm; tabelle complete in `dati-standard.md`)
Fori di passaggio ISO 273 (stretto / **normale** / largo): M2 2.2/2.4/2.6 · M2.5 2.7/2.9/3.1 · **M3 3.2/3.4/3.6** · M4 4.3/4.5/4.8 ·
M5 5.3/5.5/5.8 · M6 6.4/6.6/7.0 · M8 8.4/9.0/10.0.
| Vite | Lamatura testa cilindrica ISO 4762 (Ø × profondità) | Svasatura testa piana ISO 10642 (Ø, 90°) |
|---|---|---|
| M3 | 6.5 × 3.4 | 7.5 |
| M4 | 8 × 4.6 | 10 |
| M5 | 10 × 5.7 | 12.5 |
| M6 | 11 × 6.8 | 14.5 |
Fori filettati (punta per filettare, ISO): M2.5 2.05 · **M3 2.5** · M4 3.3 · M5 4.2 · M6 5.0 · M8 6.8 (Fusion: 6.75). In un pezzo stampato una vite
metrica si avvita meglio in un **inserto a caldo** che nella plastica.

## 3. Inserti a caldo (produttori CNC Kitchen e ruthex, per stampa 3D: foro **dritto**)
| Inserto | Ø esterno | Foro | Profondità del foro | Lunghezza |
|---|---|---|---|---|
| M2 | 3.6 | 3.2 | 4.0–5.0 | 3.0–4.0 |
| M2.5 | 4.6 | 4.0 | 5.0–6.7 | 4.0–5.7 |
| **M3** | 4.6 | **4.0** | **6.7** | 5.7 |
| M4 | 6.3 | 5.7 / 5.6 | 9.1 | 8.1 |
| M5 | 7.1 | 6.5 / 6.4 | 10.5 | 9.5 |
Profondità = lunghezza + 1; bossolo attorno all'inserto 1.5–1.7 × il suo diametro esterno.

## 4. Esportazione (J7)
- 3MF in mm (`createC3MFExportOptions`), un file anche con più corpi; solo i corpi da stampare visibili.
- Controllo: `python -X utf8 scripts/controlla_mesh.py pezzo.3mf --atteso-mm X Y Z --atteso-volume-mm3 V` (misure asse per asse).
- Poi lo slicer (o la skill di stampa, se installata) prepara il file per la stampante. La stampa la avvia sempre l'utente.
- STEP solo se il pezzo va a qualcuno che usa un altro CAD.

## 5. Dopo la stampa (J10)
«Non entra», «i fori sono stretti»: prima si misura col calibro (3 letture) e si passa dalla skill di stampa, se installata: spesso
la correzione è nello slicer o nella calibrazione. Si cambia il modello solo se è un gioco di progetto, in una **nuova versione** del `.f3d`.
