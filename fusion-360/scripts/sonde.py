"""Probe points: for each feature of the part, points where there MUST be material and points where there must NOT be.

Why: volume, bounding box and center of mass do not see everything. A bolt circle enlarged or rotated leaves all three unchanged (tested with
parts damaged on purpose: 8 out of 8 caught); the probes see it. Compute the probes BEFORE modeling, from the specification, like the other expected values.

The sensitivity is the margin: a probe at `margine` mm from the wall only sees errors larger than the margin (tested: hole Ø 9.4 instead
of Ø 9 passes with margin 0.5, fails with margin 0.1). Tight dimensions are checked by measuring them.

Probe file (JSON, dimensions in mm in the model coordinate system; "pieno" = solid, "vuoto" = empty, "bordo" = on a face):
  {"sonde": [{"nome": "centro", "punto": [x, y, z], "atteso": "pieno"}],
   "fori":  [{"nome": "F1", "centro": [x, y, z], "diametro": 9, "asse": "z", "margine": 0.5}]}
A hole becomes 5 empty probes (axis and 4 points at radius − margin) and 4 solid ones (at radius + margin). `centro` = a point on the axis INSIDE the
part (for a through hole: at mid thickness). A probe that falls exactly on a face is a probe error: move it.

Usage: python -X utf8 sonde.py sonde.json   → checks all bodies of the active document; exits with 1 if a probe is wrong
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

def sonde_foro(nome, centro, diametro, asse="z", margine=0.5):
    """The 9 probes of a cylindrical hole."""
    i = "xyz".index(asse); assi = [k for k in range(3) if k != i]
    def punto(raggio, gradi):
        p = list(centro); a = math.radians(gradi)
        p[assi[0]] += raggio * math.cos(a); p[assi[1]] += raggio * math.sin(a)
        return p
    r = diametro / 2
    s = [{"nome": f"{nome} axis", "punto": list(centro), "atteso": "vuoto"}]
    for g in (45, 135, 225, 315):       # not on the x/y axes: edges of other features are more often there
        s.append({"nome": f"{nome} inside {g}°", "punto": punto(r - margine, g), "atteso": "vuoto"})
        s.append({"nome": f"{nome} outside {g}°", "punto": punto(r + margine, g), "atteso": "pieno"})
    return s

def espandi(dati):
    s = list(dati.get("sonde", []))
    for f in dati.get("fori", []):
        s += sonde_foro(f["nome"], f["centro"], f["diametro"], f.get("asse", "z"), f.get("margine", 0.5))
    return s

CODICE = r'''
PC = adsk.fusion.PointContainment
corpi = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count)]
for o in r.allOccurrences:
    corpi += [o.bRepBodies.item(k) for k in range(o.bRepBodies.count)]
corpi = [c for c in corpi if c.isSolid]
esiti = []
for x, y, z in PUNTI:
    p = P(x / 10, y / 10, z / 10); e = "vuoto"
    for c in corpi:
        v = c.pointContainment(p)
        if v == PC.PointOnPointContainment: e = "bordo"; break
        if v == PC.PointInsidePointContainment: e = "pieno"
    esiti.append(e)
out(esiti=esiti, corpi=len(corpi))
'''

def controlla(sonde, sessione=None):
    """Returns {"totali", "giuste", "sbagliate": [...], "corpi"}."""
    righe = ",\n    ".join(json.dumps(s["punto"]) for s in sonde)      # one line per point: lines over ~4,000 characters get corrupted
    ok, r, testo = esegui(sessione or Sessione(), f"PUNTI = [\n    {righe}\n]\n" + CODICE, sola_lettura=True)
    if not ok or not r:
        raise RuntimeError("probes not run: " + " ".join(testo))
    sb = [{"nome": s["nome"], "punto": s["punto"], "atteso": s["atteso"], "trovato": e} for s, e in zip(sonde, r["esiti"]) if e != s["atteso"]]
    return {"totali": len(sonde), "giuste": len(sonde) - len(sb), "sbagliate": sb, "corpi": r["corpi"]}

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(0)  # senza argomenti: l'uso, come --help
    r = controlla(espandi(json.load(open(sys.argv[1], encoding="utf-8"))))
    print(json.dumps(r, ensure_ascii=False, indent=1))
    sys.exit(1 if r["sbagliate"] else 0)

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
