"""Analisi della FORMA di un progetto (area P2, 03/11/2026): controlli misurabili di qualità della forma, sola lettura.
1) continuità a ogni spigolo fra due facce (definizioni della guida Fusion «Analyze surface continuity»): G0 = spigolo vivo (angolo fra
   le normali > 1°), G1 = tangente (normali uguali, curvature diverse), G2 = curvatura continua (anche le curvature uguali);
2) gerarchia dei raggi: raggi dei raccordi (facce cilindriche e toriche) per corpo, distinti e contati;
3) stabilità: baricentro del progetto + carichi (massa e posizione), poligono d'appoggio = inviluppo del fondo del corpo più basso,
   margine minimo dal bordo e angolo di ribaltamento = atan(margine / altezza del baricentro);
4) impugnature (se indicate): diametro fra 25 e 40 mm (Drury e Pizatella, Human Factors 1983).
Uso: python -X utf8 analisi_forma.py [--file modello.f3d] [--densita 1.27] [--carico massa_kg,x_mm,y_mm,z_mm ...]
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

CODICE = r'''
dz = adsk.fusion.Design.cast(app.activeProduct); r0 = dz.rootComponent
corpi = [r0.bRepBodies.item(k) for k in range(r0.bRepBodies.count)]
for i in range(r0.allOccurrences.count):
    occ = r0.allOccurrences.item(i)
    corpi += [occ.bRepBodies.item(k) for k in range(occ.bRepBodies.count)]
corpi = [b for b in corpi if b.isSolid and b.isVisible]
ris = {"corpi": {}}
def curv(f, p):
    ok_, par = f.evaluator.getParameterAtPoint(p)
    ok_, d, kmax, kmin = f.evaluator.getCurvature(par)
    return kmax, kmin
for b in corpi:
    g = {"G0": 0, "G1": 0, "G2": 0, "non_misurati": 0}
    for i in range(b.edges.count):
        e = b.edges.item(i)
        if e.faces.count != 2: g["non_misurati"] += 1; continue
        ev = e.evaluator; ok_, s, t = ev.getParameterExtents()
        ok_, p = ev.getPointAtParameter(s + (t - s) * 0.5)
        f1, f2 = e.faces.item(0), e.faces.item(1)
        try:
            ok1, n1 = f1.evaluator.getNormalAtPoint(p); ok2, n2 = f2.evaluator.getNormalAtPoint(p)
            ang = math.degrees(math.acos(max(-1, min(1, n1.dotProduct(n2)))))
            if ang > 1.0: g["G0"] += 1; continue
            a1, b1 = curv(f1, p); a2, b2 = curv(f2, p)
            k = max(abs(a1), abs(b1), abs(a2), abs(b2), 1e-9)
            if abs(a1 - a2) + abs(b1 - b2) < 0.05 * k + 1e-4: g["G2"] += 1
            else: g["G1"] += 1
        except Exception: g["non_misurati"] += 1
    raggi = {}
    for i in range(b.faces.count):
        geo = b.faces.item(i).geometry
        if geo.objectType == adsk.core.Cylinder.classType(): rr = round(geo.radius * 10, 2)
        elif geo.objectType == adsk.core.Torus.classType(): rr = round(geo.minorRadius * 10, 2)
        else: continue
        raggi[str(rr)] = raggi.get(str(rr), 0) + 1
    pp = b.physicalProperties; c = pp.centerOfMass
    bb = b.boundingBox
    ris["corpi"][b.name] = {"spigoli": g, "raggi_mm": dict(sorted(raggi.items(), key=lambda x: float(x[0]))),
                            "volume_cm3": round(b.volume, 3), "baricentro_mm": [round(c.x * 10, 2), round(c.y * 10, 2), round(c.z * 10, 2)],
                            "z_min_mm": round(bb.minPoint.z * 10, 2)}
# fondo del corpo più basso: punti degli spigoli che stanno alla sua quota minima
basso = min(corpi, key=lambda b: b.boundingBox.minPoint.z); zmin = basso.boundingBox.minPoint.z
pts = []
for i in range(basso.edges.count):
    e = basso.edges.item(i); bb = e.boundingBox
    if abs(bb.minPoint.z - zmin) < 1e-4 and abs(bb.maxPoint.z - zmin) < 1e-4:
        ok_, s, t = e.evaluator.getParameterExtents(); ok_, st = e.evaluator.getStrokes(s, t, 0.001)
        pts += [[round(q.x * 10, 3), round(q.y * 10, 3)] for q in st]
ris["appoggio"] = {"corpo": basso.name, "punti": pts}
out(**ris)
'''

def inviluppo(p):
    p = sorted(set(map(tuple, p)))
    if len(p) < 3: return p
    croce = lambda o, a, b: (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    basso, alto = [], []
    for q in p:
        while len(basso) >= 2 and croce(basso[-2], basso[-1], q) <= 0: basso.pop()
        basso.append(q)
    for q in reversed(p):
        while len(alto) >= 2 and croce(alto[-2], alto[-1], q) <= 0: alto.pop()
        alto.append(q)
    return basso[:-1] + alto[:-1]

def dist_bordo(pt, poli):
    """distanza (positiva dentro) dal punto al bordo del poligono convesso antiorario"""
    m = float("inf")
    for a, b in zip(poli, poli[1:] + poli[:1]):
        ex, ey = b[0] - a[0], b[1] - a[1]; L = math.hypot(ex, ey)
        if L == 0: continue
        m = min(m, (ex * (pt[1] - a[1]) - ey * (pt[0] - a[0])) / L)
    return m

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    dens = float(a[a.index("--densita") + 1]) if "--densita" in a else 1.27          # g/cm³ (PETG pieno)
    carichi = [list(map(float, a[i + 1].split(","))) for i, v in enumerate(a) if v == "--carico"]
    pre = ""
    if "--file" in a:
        f = a[a.index("--file") + 1].replace("\\", "/")
        pre = f"im = app.importManager\nim.importToNewDocument(im.createFusionArchiveImportOptions({f!r}))\n"
    ok, r, righe = esegui(Sessione(), pre + CODICE, sola_lettura=not pre)
    if not r: print(righe); return
    masse = [(v["volume_cm3"] * dens / 1000, v["baricentro_mm"]) for v in r["corpi"].values()] + [(c[0], c[1:]) for c in carichi]
    M = sum(m for m, _ in masse)
    G = [sum(m * p[k] for m, p in masse) / M for k in range(3)]
    poli = inviluppo(r["appoggio"]["punti"])
    marg = dist_bordo(G, poli)
    tot = {"G0": 0, "G1": 0, "G2": 0}
    for v in r["corpi"].values():
        for k in tot: tot[k] += v["spigoli"][k]
    raggi = sorted({float(x) for v in r["corpi"].values() for x in v["raggi_mm"]})
    print(json.dumps({"corpi": {n: {k: v[k] for k in ("spigoli", "raggi_mm", "baricentro_mm")} for n, v in r["corpi"].items()},
                      "spigoli_totali": tot, "raggi_distinti_mm": raggi,
                      "stabilita": {"massa_totale_kg": round(M, 3), "densita": dens, "carichi": carichi,
                                    "baricentro_mm": [round(x, 1) for x in G], "appoggio": r["appoggio"]["corpo"], "vertici_appoggio": len(poli),
                                    "margine_mm": round(marg, 1), "dentro": marg > 0,
                                    "angolo_ribaltamento_gradi": round(math.degrees(math.atan2(marg, G[2])), 1) if G[2] > 0 else None}},
                     ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
