"""J3 — crea (o ritrova) la cartella di un progetto Fusion sul PC e tiene l'elenco dei progetti.

Radice: `cartella_progetti` di impostazioni.json (fuori da qualunque repository: i .f3d restano sul PC).
Ogni progetto: <radice>\\AAAA-MM-GG-<nome>\\ con passi\\, foto\\, consegna\\, specifica.md (dal modello in assets\\), registro.json
(lo scrive progetto_locale.py) e un repository git locale (regola dell'utente «git sempre»; mai push).
L'elenco <radice>\\elenco-progetti.md (data, nome, descrizione, cartella) serve a ritrovare «il pezzo di ieri».

Uso: python -X utf8 nuovo_progetto.py "<nome breve>" "<descrizione in una riga>"   → crea e stampa la cartella
     python -X utf8 nuovo_progetto.py --cerca <parola>                             → righe dell'elenco che la contengono
     python -X utf8 nuovo_progetto.py --radice <cartella> ...                      → altra radice (es. per i test)
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
            open(el, "w", encoding="utf-8").write("# Progetti Fusion\n\n| Data | Nome | Descrizione | Cartella |\n|---|---|---|---|\n")
        with open(el, "a", encoding="utf-8") as f:
            f.write(f"| {datetime.date.today().isoformat()} | {nome} | {descrizione} | `{os.path.basename(cart)}` |\n")
        if IMP["git_progetti"] and shutil.which("git"):          # git facoltativo: senza, il progetto si crea lo stesso
            subprocess.run(["git", "-C", cart, "init", "-q"], capture_output=True)
            open(os.path.join(cart, ".gitignore"), "w", encoding="utf-8").write("*.f3d.tmp\n")
            subprocess.run(["git", "-C", cart, "add", "-A"], capture_output=True)
            subprocess.run(["git", "-C", cart, "commit", "-q", "-m", f"progetto creato: {nome}"], capture_output=True)
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
    if a[0].startswith("-"):      # caso reale: «--help» preso come nome creava un progetto fasullo nella cartella vera
        print(f"opzione sconosciuta {a[0]!r}: nessun progetto creato\n\n" + __doc__); sys.exit(2)
    cart, nuova = crea(a[0], a[1] if len(a) > 1 else "", radice)
    print(("creato: " if nuova else "già esistente: ") + cart)

if __name__ == "__main__":
    main()
