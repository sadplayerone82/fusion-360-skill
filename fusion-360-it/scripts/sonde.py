"""Punti sonda: per ogni elemento del pezzo, punti dove DEVE esserci materiale e punti dove NON deve esserci.

Perché: volume, ingombro e baricentro non vedono tutto. Un cerchio di fori ingrandito o ruotato lascia uguali tutti e tre (provato con
pezzi rovinati apposta: 8 su 8 presi); le sonde lo vedono. Calcola le sonde PRIMA di modellare, dalla specifica, come gli altri attesi.

La sensibilità è il margine: una sonda a `margine` mm dalla parete vede solo errori più grandi del margine (provato: foro Ø 9,4 invece
di Ø 9 passa con margine 0,5, è bocciato con margine 0,1). Le quote strette si controllano misurandole.

File delle sonde (JSON, misure in mm nel sistema del modello):
  {"sonde": [{"nome": "centro", "punto": [x, y, z], "atteso": "pieno"}],
   "fori":  [{"nome": "F1", "centro": [x, y, z], "diametro": 9, "asse": "z", "margine": 0.5}]}
Un foro diventa 5 sonde vuote (asse e 4 punti a raggio − margine) e 4 piene (a raggio + margine). `centro` = un punto sull'asse DENTRO il
pezzo (per un foro passante: a metà spessore). Una sonda che cade esattamente su una faccia è un errore della sonda: va spostata.

Uso: python -X utf8 sonde.py sonde.json   → controlla tutti i corpi del documento attivo; esce con 1 se una sonda è sbagliata
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

def sonde_foro(nome, centro, diametro, asse="z", margine=0.5):
    """Le 9 sonde di un foro cilindrico."""
    i = "xyz".index(asse); assi = [k for k in range(3) if k != i]
    def punto(raggio, gradi):
        p = list(centro); a = math.radians(gradi)
        p[assi[0]] += raggio * math.cos(a); p[assi[1]] += raggio * math.sin(a)
        return p
    r = diametro / 2
    s = [{"nome": f"{nome} asse", "punto": list(centro), "atteso": "vuoto"}]
    for g in (45, 135, 225, 315):       # non sugli assi x/y: lì stanno più spesso i bordi di altri elementi
        s.append({"nome": f"{nome} dentro {g}°", "punto": punto(r - margine, g), "atteso": "vuoto"})
        s.append({"nome": f"{nome} fuori {g}°", "punto": punto(r + margine, g), "atteso": "pieno"})
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
    """Restituisce {"totali", "giuste", "sbagliate": [...], "corpi"}."""
    righe = ",\n    ".join(json.dumps(s["punto"]) for s in sonde)      # una riga per punto: le righe oltre ~4 000 caratteri si rovinano
    ok, r, testo = esegui(sessione or Sessione(), f"PUNTI = [\n    {righe}\n]\n" + CODICE, sola_lettura=True)
    if not ok or not r:
        raise RuntimeError("sonde non eseguite: " + " ".join(testo))
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
