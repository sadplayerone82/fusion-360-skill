"""Measurements from a photo with a reference of known size (ruler, coin, dimensioned object on the same plane as the part).

Critical dimensions ALWAYS come from the caliper: the photo serves for the form and for non-critical measurements, with a declared uncertainty.
Flow: 1) `griglia` to see the pixel coordinates; 2) `ingrandisci` the area around a point to read it well; 3) `scala` from the two
ends of the reference; 4) `misura` the distances; 5) `canvas` gives the width/height in cm to place the photo in Fusion at true scale.

Usage (python -X utf8 misura_foto.py …):
  griglia PHOTO OUTPUT.png [--passo 50]                 photo with grid and pixel coordinates
  ingrandisci PHOTO X0 Y0 X1 Y1 OUTPUT.png [--fattore 4] enlarged crop with grid (original coordinates)
  estensione PHOTO X0 Y0 X1 Y1 [--soglia 100]           box of the dark pixels (< threshold, 0–255) in the area: edges of an object
  scala X1 Y1 X2 Y2 MM                                  mm per pixel from the reference (MM = its true length)
  misura X1 Y1 X2 Y2 --scala MM_PER_PX                  distance in mm with uncertainty (±1 px per end)
  canvas PHOTO --scala MM_PER_PX                        size in cm for the canvas matrix in Fusion
Coordinates: image pixels, origin at the top left, y pointing down (in Fusion y points up: y_fusion = height − y).
"""
import json, math, sys
from PIL import Image, ImageDraw

def griglia(foto, uscita, passo=50):
    im = Image.open(foto).convert("RGB"); d = ImageDraw.Draw(im)
    for x in range(0, im.width, passo):
        d.line([(x, 0), (x, im.height)], fill=(255, 0, 0) if x % (passo * 5) == 0 else (255, 160, 160), width=1)
        if x % (passo * 2) == 0: d.text((x + 2, 2), str(x), fill=(255, 0, 0))
    for y in range(0, im.height, passo):
        d.line([(0, y), (im.width, y)], fill=(0, 0, 255) if y % (passo * 5) == 0 else (160, 160, 255), width=1)
        if y % (passo * 2) == 0: d.text((2, y + 2), str(y), fill=(0, 0, 255))
    im.save(uscita); return {"file": uscita, "larghezza_px": im.width, "altezza_px": im.height}

def ingrandisci(foto, x0, y0, x1, y1, uscita, fattore=4):
    im = Image.open(foto).convert("RGB").crop((x0, y0, x1, y1))
    im = im.resize((im.width * fattore, im.height * fattore), Image.LANCZOS); d = ImageDraw.Draw(im)
    passo = max(1, round(20 / fattore)) * fattore
    for i, x in enumerate(range(0, im.width, passo)):
        d.line([(x, 0), (x, im.height)], fill=(255, 120, 120)); d.text((x + 1, 1), str(x0 + x // fattore), fill=(255, 0, 0)) if i % 2 == 0 else None
    for i, y in enumerate(range(0, im.height, passo)):
        d.line([(0, y), (im.width, y)], fill=(120, 120, 255)); d.text((1, y + 1), str(y0 + y // fattore), fill=(0, 0, 255)) if i % 2 == 0 else None
    im.save(uscita); return {"file": uscita, "zona": [x0, y0, x1, y1], "fattore": fattore}

def estensione(foto, x0, y0, x1, y1, soglia=100):
    im = Image.open(foto).convert("L"); px = im.load()
    pts = [(x, y) for y in range(y0, y1) for x in range(x0, x1) if px[x, y] < soglia]
    if not pts:
        return {"trovati": 0}
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return {"trovati": len(pts), "x_min": min(xs), "x_max": max(xs), "y_min": min(ys), "y_max": max(ys),
            "larghezza_px": max(xs) - min(xs) + 1, "altezza_px": max(ys) - min(ys) + 1}

def scala(x1, y1, x2, y2, mm):
    d = math.hypot(x2 - x1, y2 - y1)
    s = mm / d
    return {"mm_per_px": round(s, 6), "distanza_px": round(d, 2), "incertezza_relativa_%": round(200 / d, 3),
            "nota": "uncertainty from ±1 px per end; a longer reference reduces it"}

def misura(x1, y1, x2, y2, s):
    d = math.hypot(x2 - x1, y2 - y1)
    return {"mm": round(d * s, 3), "incertezza_mm": round(2 * s, 3), "distanza_px": round(d, 2)}

def canvas(foto, s):
    im = Image.open(foto)
    return {"larghezza_cm": round(im.width * s / 10, 5), "altezza_cm": round(im.height * s / 10, 5),
            "codice": "m.setWithCoordinateSystem(Point2D(0,0), Vector2D(larghezza_cm, 0), Vector2D(0, altezza_cm))"}

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    opz = lambda k, d: float(a[a.index(k) + 1]) if k in a else d
    if not a:
        print(__doc__); sys.exit(2)
    c = a[0]
    if c == "griglia": r = griglia(a[1], a[2], int(opz("--passo", 50)))
    elif c == "ingrandisci": r = ingrandisci(a[1], *map(int, a[2:6]), a[6], int(opz("--fattore", 4)))
    elif c == "estensione": r = estensione(a[1], *map(int, a[2:6]), int(opz("--soglia", 100)))
    elif c == "scala": r = scala(*map(float, a[1:5]), float(a[5]))
    elif c == "misura": r = misura(*map(float, a[1:5]), opz("--scala", None))
    elif c == "canvas": r = canvas(a[1], opz("--scala", None))
    else:
        print(__doc__); sys.exit(2)
    print(json.dumps(r, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
