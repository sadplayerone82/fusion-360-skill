"""Reads the Fusion logs: that is where the cause is when Fusion freezes or does strange things (rules of 03/11/2026).

Folder: %LOCALAPPDATA%\\Autodesk\\Autodesk Fusion 360\\<id>\\logs (there can be several <id>: the most recently written one is taken).
- comando_in_corso(): the last drawing command started and not finished (FusionDrawing.log: «cmd will Start» without «cmd Finished»).
  It does not depend on the Fusion language. A command waiting for a click is cancelled by Fusion only after 600 s.
- dialogo(n): the last lines of AcCore*.log, i.e. the command prompts and the answers received.
- salvataggi(): what happened to uploads to the cloud (AppLogFile*.log): a «Queueing» line exists only if the file really leaves.

Usage: python -X utf8 registri.py comando | dialogo [n] | salvataggi [n] | cartella
Exits with 1 if `comando` finds a command in progress.
"""
import datetime, glob, json, os, re, sys

RADICE = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Autodesk", "Autodesk Fusion 360")

def cartella():
    """The logs folder with the most recently written file, or None."""
    file = glob.glob(os.path.join(RADICE, "*", "logs", "*"))
    return os.path.dirname(max(file, key=os.path.getmtime)) if file else None

def _ultimo(modello, cart=None):
    cart = cart or cartella()
    file = glob.glob(os.path.join(cart, modello)) if cart else []
    return max(file, key=os.path.getmtime) if file else None

def _righe(p):
    return open(p, encoding="utf-8", errors="replace").read().splitlines() if p else []

def comando_in_corso(cart=None, adesso=None):
    """{"comando", "iniziato", "secondi"} of the last unfinished drawing command, otherwise None."""
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
