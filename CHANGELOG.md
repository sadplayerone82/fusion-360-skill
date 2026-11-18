# Novità

Le versioni seguono il versionamento semantico (maggiore.minore.correzione); la più recente sta in cima.

## [1.0.0] — 2026-11-18
Prima versione pubblica.

### Contenuto
- **SKILL.md**: il flusso di lavoro dall'ambiente alla consegna, con un controllo a ogni passo (ambiente, richiesta e specifica,
  produzione se dichiarata, piano e valori attesi, progetto, modellazione a passi misurati, verifica, flessibilità, uscite, tavole e
  render, consegna, ripresa); i punti in cui fermarsi ad aspettare l'utente; le trappole che danno pezzi sbagliati senza errori.
- **Riferimenti** (`references/`): connettore e API con le trappole misurate; metodo e rami di lavoro; 19 scenari d'uso; progetti a
  più pezzi; forma e dettaglio per gli oggetti da riconoscere; verifica; ricette provate per famiglia (schizzi, solidi, superfici,
  lamiera, assiemi, importazione e modifica, viste e render, decori, stampi e mesh, foto e tavole, CNC, forme libere); elenco dei
  comandi di Fusion con API e disponibilità nella licenza Personal; dati standard (filettature, fori di passaggio, viti, inserti,
  cuscinetti); limiti della licenza Personal.
- **Script** (`scripts/`): controllo dell'ambiente e degli strumenti MCP; impostazioni fuori dalla skill; collegamento al server MCP;
  progetti locali a passi misurati con registro e ripresa; rapporto del modello; punti sonda; interferenze e franchi negli assiemi;
  spessore minimo; segni di forma povera; analisi di stabilità; controllo dei file 3MF; controllo del G-code; foto in prospettiva e
  misure da foto; simboli per le tavole; lettura dei registri di Fusion.
- **Modelli** (`assets/`): specifica e resoconto.
- **Casi di prova** (`evals/`): esempi per chi sviluppa la skill, con il loro formato in `evals/LEGGIMI.md`.

### Provato
- Fusion build 2706.1.x, licenza Personal, Windows, modello Opus (novembre 2026). Esiti nella sezione «Validazione» del README.
