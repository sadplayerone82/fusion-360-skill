"""Skill settings, read by all scripts instead of fixed paths (PIANO v4 §11.6, C5 of 04/11/2026).

Where the file lives (OUTSIDE the skill folder, so a reinstallation does not delete it):
  1. the environment variable FUSION360_SKILL_IMPOSTAZIONI, if set;
  2. otherwise %USERPROFILE%\\.claude\\fusion-360\\impostazioni.json.
If the file does not exist the DEFAULT VALUES below apply (and `--crea` writes it, to be edited by hand).
Keys missing from the file take the default value; unknown keys are reported (typo?).

Usage: python -X utf8 impostazioni.py --mostra | --crea [--cartella-progetti "<folder>"] | --dove
"""
import json, os, sys

PREDEFINITE = {
    "versione": 1,
    "cartella_progetti": os.path.join(os.path.expanduser("~"), "Documents", "Progetti-Fusion"),
    "lingua": "it",                                   # language of the messages and of the Fusion interface (command names)
    "unita": "mm",                                    # units shown in new projects (the API always works in cm)
    "mcp_url": "http://127.0.0.1:27182/mcp",          # official Fusion MCP server
    "skill_stampa": "stampa-3d",                      # skill to use if the user declares FDM printing; null if not installed
    "cloud_consentito": False,                        # save to the cloud only with explicit permission (Personal: 10 documents)
    "porte_da_controllare": {},                       # {"port": "who should hold it"}: warning if Fusion holds it
    "git_progetti": True,                             # local git repository in every project (if git is installed)
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
            print(f"[impostazioni] unknown keys in {p}: {ignote}", file=sys.stderr)
        imp.update({k: v for k, v in letto.items() if k in PREDEFINITE})
    imp["_file"] = p if os.path.exists(p) else None
    return imp

def porta_mcp(imp=None):
    from urllib.parse import urlparse
    return urlparse((imp or carica())["mcp_url"]).port or 27182

def crea(cartella_progetti=None):
    p = percorso()
    if os.path.exists(p):
        return f"already exists: {p} (not overwritten)"
    os.makedirs(os.path.dirname(p), exist_ok=True)
    imp = dict(PREDEFINITE)
    if cartella_progetti:
        imp["cartella_progetti"] = cartella_progetti
    json.dump(imp, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return f"created: {p}"

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
    main()
