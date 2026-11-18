"""Legge i registri di Fusion: è lì la causa quando Fusion si blocca o fa cose strane (regole del 03/11/2026).

Cartella: %LOCALAPPDATA%\\Autodesk\\Autodesk Fusion 360\\<id>\\logs (ci possono essere più <id>: si prende quella scritta più di recente).
- comando_in_corso(): l'ultimo comando delle tavole iniziato e non finito (FusionDrawing.log: «cmd will Start» senza «cmd Finished»).
  Non dipende dalla lingua di Fusion. Un comando che aspetta un clic viene annullato da Fusion solo dopo 600 s.
- dialogo(n): le ultime righe di AcCore*.log, cioè le domande del comando e le risposte ricevute.
- salvataggi(): cosa è successo agli invii verso il cloud (AppLogFile*.log): una riga «Queueing» c'è solo se il file parte davvero.

Uso: python -X utf8 registri.py comando | dialogo [n] | salvataggi [n] | cartella
Esce con 1 se `comando` trova un comando in corso.
"""
import datetime, glob, json, os, re, sys

RADICE = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Autodesk", "Autodesk Fusion 360")

def cartella():
    """La cartella logs con il file scritto più di recente, o None."""
    file = glob.glob(os.path.join(RADICE, "*", "logs", "*"))
    return os.path.dirname(max(file, key=os.path.getmtime)) if file else None

def _ultimo(modello, cart=None):
    cart = cart or cartella()
    file = glob.glob(os.path.join(cart, modello)) if cart else []
    return max(file, key=os.path.getmtime) if file else None

def _righe(p):
    return open(p, encoding="utf-8", errors="replace").read().splitlines() if p else []

def comando_in_corso(cart=None, adesso=None):
    """{"comando", "iniziato", "secondi"} dell'ultimo comando delle tavole non finito, altrimenti None."""
    aperti = []
    for l in _righe(_ultimo("FusionDrawing.log", cart)):
        m = re.match(r"(\d{8}T\d{6}) \S+ \S+ cmd will Start: (\S+)", l)
        if m:
            aperti.append((m.group(2), m.group(1))); continue
        m = re.match(r"\d{8}T\d{6} \S+ \S+ cmd Finished: (\S+)", l)
        if m:
            for i in range(len(aperti) - 1, -1, -1):
                if aperti[i][0] == m.group(1):
                    del aperti[i]; break
    if not aperti:
        return None
    nome, quando = aperti[-1]
    t = datetime.datetime.strptime(quando, "%Y%m%dT%H%M%S")
    return {"comando": nome, "iniziato": quando, "secondi": round(((adesso or datetime.datetime.now()) - t).total_seconds())}

def dialogo(n=12, cart=None):
    return [l for l in _righe(_ultimo("AcCore*.log", cart)) if l.strip()][-n:]

def salvataggi(n=8, cart=None):
    chiavi = ("[CFS] Queueing file", "[CFSUploader] Uploaded document", "Upload failed", "version created for file")
    return [l[:220] for l in _righe(_ultimo("AppLogFile*.log", cart)) if any(k in l for k in chiavi)][-n:]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:] or ["comando"]
    n = int(a[1]) if len(a) > 1 else None
    if a[0] == "cartella":
        print(cartella())
    elif a[0] == "dialogo":
        print("\n".join(dialogo(n or 12)))
    elif a[0] == "salvataggi":
        print("\n".join(salvataggi(n or 8)))
    else:
        c = comando_in_corso()
        print(json.dumps({"in_corso": c}, ensure_ascii=False))
        sys.exit(1 if c else 0)

if __name__ == "__main__":
    main()
