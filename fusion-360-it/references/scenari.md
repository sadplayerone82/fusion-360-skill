# Cosa si fa con Fusion: i 19 scenari e come la skill li copre

Dalle fonti ufficiali Autodesk sugli usi di Fusion, controllati uno per uno (novembre 2026). Per ogni scenario:
il ramo del metodo (`metodo.md` §10), dove stanno le ricette provate, e i limiti da dire all'utente.

| # | Scenario | Ramo | Ricette | Limiti da dire |
|---|---|---|---|---|
| 1 | Pezzi meccanici da tavola (staffe, flange, alberi) | tavola | `ricette.md`, `ricette-solidi.md`, `tavole-e-render.md` | simboli GD&T e tabella fori come immagini |
| 2 | Progetto da un'idea | idea | `metodo.md` §10, `verifica.md` §6c | — |
| 3 | Prodotti di consumo, oggetti di design | idea / oggetto da riconoscere | **`forma-e-dettaglio.md`**, `ricette-superfici-forme-lamiera.md`, `ricette-decori-anelli.md`, `ricette-lamiera-form-costruzione.md` | T-spline: solo primitive via API |
| 4 | Contenitori per elettronica | tavola / idea | `ricette.md` (ganci, gusci, fori) | — |
| 5 | Assiemi e meccanismi | assiemi | `ricette-assiemi.md`, `ricette-stampi-mesh-pezzi.md` (derive) | parametri derivati non si aggiornano; vincoli e contatti d'assieme non provati |
| 6 | Architettura e interni | architettura | `tavole-e-render.md`; schizzi/estrusioni in metri | niente BIM: solo geometria verso Revit e simili |
| 7 | Mobili e falegnameria | idea / CNC | corpi = pannelli; `ricette-cam.md` | distinta dei tagli da script (BOM a pagamento) |
| 8 | Lamiera e taglio 2D | produzione | `ricette-lamiera-form-costruzione.md` | dopo «Ripiega» il pezzo può risultare ruotato: ricontrollare |
| 9 | Lavorazione CNC | produzione | `ricette-cam.md` | rapidi rallentati (licenza Personal) |
| 10 | Stampa 3D | produzione | `produzione-e-stampa.md` + skill di stampa | — |
| 11 | Stampi (silicone, colata) | produzione | `ricette-stampi-mesh-pezzi.md` | — |
| 12 | Gioielli (anelli, ciondoli) | idea | `ricette-decori-anelli.md` (misura ISO 8653: Ø = misura/π) | misure nazionali solo da tabella letta |
| 13 | Cosplay e oggetti scolpiti | idea / file | divisione in pezzi e mesh in `ricette-stampi-mesh-pezzi.md` | Form da schizzo senza API |
| 14 | Ricambi, reverse engineering | foto / file | `ricette-foto-tavole.md` (prospettiva), mesh → solido | serve un riferimento misurato nella foto |
| 15 | Modifica di file altrui (STEP, STL) | file / modifica | `ricette-modificare-importare.md`, `ricette-stampi-mesh-pezzi.md` | STL: solo «a faccette» con la licenza Personal (il «prismatico» è rifiutato) |
| 16 | Presentazione (render, esplosi, video) | — | `tavole-e-render.md` | render solo locale; esploso e video dall'interfaccia |
| 17 | Tavole 2D | tavola | `tavole-e-render.md`, `ricette-foto-tavole.md` | 2 documenti nel cloud; oggetti non cancellabili via API |
| 18 | Elettronica e PCB | — | fuori da questa skill | — |
| 19 | Simulazione, progettazione generativa | — | non disponibili con la licenza Personal (con le altre non provate) | calcoli a mano dichiarati |
