"""J3 — creates (or finds again) the folder of a Fusion project on the PC and keeps the list of projects.

Root: `cartella_progetti` from impostazioni.json (outside any repository: the .f3d files stay on the PC).
Each project: <root>\\YYYY-MM-DD-<name>\\ with passi\\, foto\\, consegna\\, specifica.md (from the template in assets\\), registro.json
(written by progetto_locale.py) and a local git repository (the user's rule «always git»; never push).
The list <root>\\elenco-progetti.md (date, name, description, folder) is used to find «yesterday's part» again.

Usage: python -X utf8 nuovo_progetto.py "<short name>" "<one-line description>"   → creates and prints the folder
       python -X utf8 nuovo_progetto.py --cerca <word>                             → lines of the list that contain it
       python -X utf8 nuovo_progetto.py --radice <folder> ...                      → another root (e.g. for tests)
"""
import datetime, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import impostazioni

IMP = impostazioni.carica()
RADICE = IMP["cartella_progetti"]
QUI = os.path.dirname(os.path.abspath(__file__))
MODELLO = os.path.join(QUI, "..", "assets", "specifica.md")

def slug(nome):
    s = re.sub(r"[^a-z0-9]+", "-", nome.lower().replace("à", "a").replace("è", "e").replace("é", "e").replace("ì", "i")
               .replace("ò", "o").replace("ù", "u")).strip("-")
    return s[:40] or "pezzo"

def elenco(radice):
    return os.path.join(radice, "elenco-progetti.md")

def crea(nome, descrizione, radice=RADICE):
    os.makedirs(radice, exist_ok=True)
    cart = os.path.join(radice, f"{datetime.date.today().isoformat()}-{slug(nome)}")
    nuova = not os.path.exists(cart)
    for sotto in ("passi", "foto", "consegna"):
        os.makedirs(os.path.join(cart, sotto), exist_ok=True)
    spec = os.path.join(cart, "specifica.md")
    if not os.path.exists(spec) and os.path.exists(MODELLO):
        t = open(MODELLO, encoding="utf-8").read().replace("{{NOME}}", nome).replace("{{DATA}}", datetime.date.today().isoformat())
        open(spec, "w", encoding="utf-8").write(t.replace("{{DESCRIZIONE}}", descrizione))
    if nuova:
        el = elenco(radice)
        if not os.path.exists(el):
            open(el, "w", encoding="utf-8").write("# Fusion projects\n\n| Date | Name | Description | Folder |\n|---|---|---|---|\n")
        with open(el, "a", encoding="utf-8") as f:
            f.write(f"| {datetime.date.today().isoformat()} | {nome} | {descrizione} | `{os.path.basename(cart)}` |\n")
        if IMP["git_progetti"] and shutil.which("git"):          # git optional: without it, the project is created anyway
            subprocess.run(["git", "-C", cart, "init", "-q"], capture_output=True)
            open(os.path.join(cart, ".gitignore"), "w", encoding="utf-8").write("*.f3d.tmp\n")
            subprocess.run(["git", "-C", cart, "add", "-A"], capture_output=True)
            subprocess.run(["git", "-C", cart, "commit", "-q", "-m", f"project created: {nome}"], capture_output=True)
    return cart, nuova

def cerca(parola, radice=RADICE):
    el = elenco(radice)
    if not os.path.exists(el):
        return []
    return [l.rstrip() for l in open(el, encoding="utf-8") if l.startswith("| 2") and parola.lower() in l.lower()]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]; radice = RADICE
    if "--radice" in a:
        i = a.index("--radice"); radice = a[i + 1]; del a[i:i + 2]
    if not a or a[0] in ("-h", "--help", "--aiuto"):
        print(__doc__); sys.exit(0 if a else 2)
    if a[0] == "--cerca":
        for r in cerca(a[1], radice):
            print(r)
        return
    if a[0].startswith("-"):      # real case: «--help» taken as a name created a fake project in the real folder
        print(f"unknown option {a[0]!r}: no project created\n\n" + __doc__); sys.exit(2)
    cart, nuova = crea(a[0], a[1] if len(a) > 1 else "", radice)
    print(("created: " if nuova else "already exists: ") + cart)

if __name__ == "__main__":
    main()
