"""Runs in Fusion the code written in a FILE (images, flexibility tests, exports, reopenings, checks outside the
project steps). It exists because code must never be written inside a shell command: write the file (Write), then
run it with this script. The code already has the same definitions as the steps (`app`, `d`, `r`, `F`, `P`, `S`, `OP`, `vol`,
`out`, `controlla`): the last `out(...)` becomes the printed result.
Usage: python -X utf8 esegui_file.py <file.py> [--sola-lettura] [--nuovo-documento] [--timeout 600]
  --nuovo-documento  first opens a new, empty design document (for work that must not be done in the open project)
Output: one JSON line {"riuscito": ..., "risultato": ..., "righe": [...]}; exit code 1 if the script failed."""
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
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
