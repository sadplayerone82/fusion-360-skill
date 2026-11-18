"""Esegue in Fusion il codice scritto in un FILE (immagini, prove di flessibilità, esportazioni, riaperture, controlli fuori dai
passi del progetto). Serve perché il codice non va mai scritto dentro un comando della shell: si scrive il file (Write), poi lo si
lancia con questo script. Nel codice ci sono già le stesse definizioni dei passi (`app`, `d`, `r`, `F`, `P`, `S`, `OP`, `vol`,
`out`, `controlla`): l'ultimo `out(...)` diventa il risultato stampato.
Uso: python -X utf8 esegui_file.py <file.py> [--sola-lettura] [--nuovo-documento] [--timeout 600]
  --nuovo-documento  apre prima un documento di progetto nuovo e vuoto (per lavori che non vanno fatti nel progetto aperto)
Uscita: una riga JSON {"riuscito": ..., "risultato": ..., "righe": [...]}; codice d'uscita 1 se lo script è fallito."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if not a or a[0].startswith("--"):
        print(__doc__); sys.exit(2)
    codice = open(a[0], encoding="utf-8").read()
    t = int(a[a.index("--timeout") + 1]) if "--timeout" in a else 600
    s = Sessione(timeout=t)
    if "--nuovo-documento" in a:
        ok, _, righe = esegui(s, "app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)\nout(ok=1)")
        if not ok:
            print(json.dumps({"riuscito": False, "risultato": None, "righe": righe}, ensure_ascii=False)); sys.exit(1)
    ok, ris, righe = esegui(s, codice, sola_lettura="--sola-lettura" in a)
    print(json.dumps({"riuscito": bool(ok), "risultato": ris, "righe": righe[-8:] if righe else []}, ensure_ascii=False))
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
