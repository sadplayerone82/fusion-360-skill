"""Impostazioni della skill, lette da tutti gli script al posto dei percorsi fissi (PIANO v4 §11.6, C5 del 04/11/2026).

Dove sta il file (FUORI dalla cartella della skill, così una reinstallazione non lo cancella):
  1. la variabile d'ambiente FUSION360_SKILL_IMPOSTAZIONI, se c'è;
  2. altrimenti %USERPROFILE%\\.claude\\fusion-360\\impostazioni.json.
Se il file non c'è valgono i VALORI PREDEFINITI qui sotto (e `--crea` lo scrive, da modificare a mano).
Le chiavi mancanti nel file prendono il valore predefinito; le chiavi sconosciute sono segnalate (errore di battitura?).

Uso: python -X utf8 impostazioni.py --mostra | --crea [--cartella-progetti "<cartella>"] | --dove
"""
import json, os, sys

PREDEFINITE = {
    "versione": 1,
    "cartella_progetti": os.path.join(os.path.expanduser("~"), "Documents", "Progetti-Fusion"),
    "lingua": "it",                                   # lingua dei messaggi e dell'interfaccia di Fusion (nomi dei comandi)
    "unita": "mm",                                    # unità mostrate nei progetti nuovi (l'API lavora sempre in cm)
    "mcp_url": "http://127.0.0.1:27182/mcp",          # server MCP ufficiale di Fusion
    "skill_stampa": "stampa-3d",                      # skill da usare se l'utente dichiara la stampa FDM; null se non installata
    "cloud_consentito": False,                        # salvare nel cloud solo con permesso esplicito (Personal: 10 documenti)
    "porte_da_controllare": {},                       # {"porta": "chi deve occuparla"}: avviso se la tiene Fusion
    "git_progetti": True,                             # repository git locale in ogni progetto (se git è installato)
}

def percorso():
    p = os.environ.get("FUSION360_SKILL_IMPOSTAZIONI")
    return p or os.path.join(os.path.expanduser("~"), ".claude", "fusion-360", "impostazioni.json")

def carica(avvisa=True):
    imp = dict(PREDEFINITE)
    p = percorso()
    if os.path.exists(p):
        letto = json.load(open(p, encoding="utf-8"))
        ignote = sorted(set(letto) - set(PREDEFINITE))
        if ignote and avvisa:
            print(f"[impostazioni] chiavi sconosciute in {p}: {ignote}", file=sys.stderr)
        imp.update({k: v for k, v in letto.items() if k in PREDEFINITE})
    imp["_file"] = p if os.path.exists(p) else None
    return imp

def porta_mcp(imp=None):
    from urllib.parse import urlparse
    return urlparse((imp or carica())["mcp_url"]).port or 27182

def crea(cartella_progetti=None):
    p = percorso()
    if os.path.exists(p):
        return f"esiste già: {p} (non lo sovrascrivo)"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    imp = dict(PREDEFINITE)
    if cartella_progetti:
        imp["cartella_progetti"] = cartella_progetti
    json.dump(imp, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return f"creato: {p}"

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if "--crea" in a:
        cp = a[a.index("--cartella-progetti") + 1] if "--cartella-progetti" in a else None
        print(crea(cp))
    elif "--dove" in a:
        print(percorso())
    else:
        print(json.dumps(carica(), ensure_ascii=False, indent=2))

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
