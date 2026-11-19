"""Verifica un programma CNC (G-code) contro il pezzo aperto in Fusion: profondità, fresa che morde il pezzo, contorni non lavorati.

Controlli: unità mm e coordinate assolute (G21, G90), mandrino acceso, avanzamento presente; profondità massima = --z-fine; nessun punto
del percorso sul fondo più vicino al pezzo del raggio della fresa (altrimenti la fresa lo mangia) né DENTRO il pezzo (contorno dal lato
sbagliato: la distanza dal bordo è la stessa dentro e fuori); OGNI contorno del pezzo alla quota
--z-sagoma (esterno, fori, tasche) percorso alla distanza del raggio per almeno --copertura % (i ponticelli lasciano dei tratti alzati);
con --z-cima: nessun rapido G0 sotto la cima del materiale.

Limite: guarda la passata finale in XY e la profondità, non simula l'asportazione né le collisioni del portautensile. Quote in mm.
Uso: python -X utf8 verifica_gcode.py FILE.nc --raggio R --z-fine Z [--dx 0 --dy 0] [--z-sagoma 0] [--z-cima 0] [--copertura 70]
     dx, dy: da aggiungere alle coordinate del MODELLO per ottenere quelle del G-code (dipendono dall'origine scelta nel CAM)
Esce con 1 se un controllo non passa.
"""
import argparse, json, math, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CONTORNI = r'''
d = adsk.fusion.Design.cast(app.activeDocument.products.itemByProductType("DesignProductType")); r = d.rootComponent
corpi = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count)]
for o in r.allOccurrences: corpi += [o.bRepBodies.item(k) for k in range(o.bRepBodies.count)]
spigoli = []
for b in corpi:
    if not b.isSolid: continue
    for i in range(b.edges.count):
        e = b.edges.item(i); bb = e.boundingBox
        if abs(bb.minPoint.z - Z_SAGOMA / 10) > 0.001 or abs(bb.maxPoint.z - Z_SAGOMA / 10) > 0.001: continue
        ev = e.evaluator; ok_, s, t = ev.getParameterExtents(); ok_, pp = ev.getStrokes(s, t, 0.0005)
        spigoli.append([[round(p.x * 10, 4), round(p.y * 10, 4)] for p in pp])
print("RIS" + json.dumps({"n": len(spigoli)}))
for k in range(0, len(spigoli), 20):      # a pezzi: la risposta conserva solo le ultime righe se è una sola riga enorme
    print("SPG" + json.dumps(spigoli[k:k + 20]))
'''

def infittisci(punti, passo=0.2):
    out = []
    for a, b in zip(punti, punti[1:]):
        n = max(1, int(math.hypot(b[0] - a[0], b[1] - a[1]) / passo))
        out += [(a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n) for k in range(n)]
    out.append(tuple(punti[-1]))
    return out

def contorni_collegati(spigoli):
    """Unisce gli spigoli che si toccano: ogni gruppo è un contorno (esterno, un foro, una tasca)."""
    gruppi = []
    for s in spigoli:
        estremi = {(round(s[0][0], 2), round(s[0][1], 2)), (round(s[-1][0], 2), round(s[-1][1], 2))}
        toccati = [g for g in gruppi if g["estremi"] & estremi]
        nuovo = {"estremi": set(estremi), "punti": infittisci(s)}
        for g in toccati:
            nuovo["estremi"] |= g["estremi"]; nuovo["punti"] += g["punti"]; gruppi.remove(g)
        gruppi.append(nuovo)
    return [g["punti"] for g in gruppi]

ASSI = {17: (0, 1, 2, "IJ"), 18: (0, 2, 1, "IK"), 19: (1, 2, 0, "JK")}

def analizza(testo, passo=0.2):
    """Legge il G-code. Restituisce i punti di taglio (x, y, z), i rapidi e cosa c'è nell'intestazione."""
    pos = [0.0, 0.0, 0.0]; modo = None; piano = 17; assoluto = None; mm = None
    taglio, rapidi = [], []; mandrino = avanz = False
    for riga in testo.splitlines():
        l = re.sub(r"\(.*?\)|;.*$", "", riga).strip().upper()
        if not l or l.startswith("G28"):
            continue
        gg = [int(x) for x in re.findall(r"G(\d+)", l)]
        for g in gg:
            if g in (0, 1, 2, 3): modo = g
            elif g in (17, 18, 19): piano = g
            elif g == 90: assoluto = True
            elif g == 91: assoluto = False
            elif g == 21: mm = True
            elif g == 20: mm = False
        if re.search(r"\bM0?3\b", l) and re.search(r"S[1-9]", l): mandrino = True
        if re.search(r"F[0-9.]*[1-9]", l): avanz = True
        v = {k: float(n) for k, n in re.findall(r"([XYZIJK])(-?\d*\.?\d+)", l)}
        if not any(k in v for k in "XYZ"):
            continue
        nuovo = [v.get("X", pos[0]), v.get("Y", pos[1]), v.get("Z", pos[2])]
        if modo == 0:
            rapidi.append((tuple(pos), tuple(nuovo)))
        elif modo == 1:
            n = max(1, int(math.dist(pos, nuovo) / passo))
            taglio += [tuple(pos[i] + (nuovo[i] - pos[i]) * k / n for i in range(3)) for k in range(n + 1)]
        elif modo in (2, 3):
            a, b, c, nomi = ASSI[piano]
            ca, cb = pos[a] + v.get(nomi[0], 0), pos[b] + v.get(nomi[1], 0)
            rg = math.hypot(pos[a] - ca, pos[b] - cb)
            a0, a1 = math.atan2(pos[b] - cb, pos[a] - ca), math.atan2(nuovo[b] - cb, nuovo[a] - ca)
            # G2 è orario guardando il piano dal lato positivo della normale; G18 ha il verso invertito rispetto a X→Z
            orario = (modo == 2) != (piano == 18)
            if orario:
                while a1 >= a0: a1 -= 2 * math.pi
            else:
                while a1 <= a0: a1 += 2 * math.pi
            n = max(2, int(abs(a1 - a0) * rg / passo))
            for k in range(n + 1):
                f = k / n; p = [0.0, 0.0, 0.0]
                p[a] = ca + rg * math.cos(a0 + (a1 - a0) * f); p[b] = cb + rg * math.sin(a0 + (a1 - a0) * f); p[c] = pos[c] + (nuovo[c] - pos[c]) * f
                taglio.append(tuple(p))
        pos = nuovo
    return {"taglio": taglio, "rapidi": rapidi, "assoluto": assoluto, "mm": mm, "mandrino": mandrino, "avanzamento": avanz}

def dentro_materiale(punti, segmenti, blocco=2000):
    """Pari/dispari: quanti segmenti del bordo taglia una semiretta verso +X da ogni punto. Dispari = punto dentro la sezione del pezzo.
    Non serve che i bordi siano ordinati: bastano i segmenti di ogni spigolo."""
    import numpy as np
    s = np.array(segmenti, dtype=float)
    if not len(s) or not len(punti): return np.zeros(len(punti), dtype=bool)
    x1, y1, x2, y2 = s[:, 0], s[:, 1], s[:, 2], s[:, 3]
    esito = []
    for k in range(0, len(punti), blocco):
        p = np.asarray(punti[k:k + blocco])[:, None, :]
        px, py = p[..., 0], p[..., 1]
        attraversa = (y1 > py) != (y2 > py)
        with np.errstate(divide="ignore", invalid="ignore"):
            xi = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
        esito.append(((attraversa & (xi > px)).sum(1) % 2) == 1)
    return np.concatenate(esito)

def verifica(g, contorni, raggio, z_fine, z_cima=None, copertura=70.0, toll=0.05, segmenti=None):
    import numpy as np
    from scipy.spatial import cKDTree
    e = {}; problemi = []
    if g["mm"] is not True: problemi.append("il programma non dichiara i millimetri (G21)")
    if g["assoluto"] is not True: problemi.append("il programma non è in coordinate assolute (G90)")
    if not g["mandrino"]: problemi.append("il mandrino non viene acceso (M3 con S)")
    if not g["avanzamento"]: problemi.append("nessun avanzamento F")
    t = np.array(g["taglio"]) if g["taglio"] else np.zeros((0, 3))
    if not len(t):
        problemi.append("nessun movimento di taglio")
        return {"problemi": problemi, "esito": "BOCCIATO"}
    zmin = float(t[:, 2].min()); e["z_min"] = round(zmin, 3); e["z_fine_attesa"] = z_fine
    if abs(zmin - z_fine) > 0.01:
        problemi.append(f"profondità {zmin:.3f}, attesa {z_fine:.3f}: " + ("non arriva in fondo" if zmin > z_fine else "scende troppo"))
    fondo = t[np.abs(t[:, 2] - zmin) < 1e-3][:, :2]
    tutti = np.array([p for c in contorni for p in c]) if contorni else np.zeros((0, 2))
    if len(tutti):
        dist, _ = cKDTree(tutti).query(fondo)
        e["distanza_min"] = round(float(dist.min()), 3); e["distanza_mediana"] = round(float(np.median(dist)), 3); e["raggio"] = raggio
        if dist.min() < raggio - toll:
            problemi.append(f"la fresa morde il pezzo: distanza minima {dist.min():.3f} con raggio {raggio:.3f}")
    if segmenti is not None:
        # la distanza dal bordo è uguale dentro e fuori: una fresa che gira DENTRO il contorno esterno passa il controllo sopra
        # (09/11: piastra 146 × 96 invece di 150 × 100). Il centro della fresa sul fondo non deve mai stare nel materiale del pezzo.
        dentro = dentro_materiale(fondo, segmenti)
        e["punti_dentro_il_pezzo"] = int(dentro.sum())
        if dentro.any():
            px, py = fondo[dentro][0]
            problemi.append(f"la fresa passa DENTRO il pezzo in {int(dentro.sum())} punti (es. {px:.2f}, {py:.2f}): contorno dal lato sbagliato?")
    albero = cKDTree(fondo); e["contorni"] = []
    for i, c in enumerate(contorni):
        c_ = np.array(c); d_, _ = albero.query(c_)
        cop = float((np.abs(d_ - raggio) < toll + 0.05).mean() * 100)
        cx, cy = c_.mean(0)
        e["contorni"].append({"contorno": i + 1, "centro": [round(float(cx), 2), round(float(cy), 2)], "copertura_%": round(cop, 1)})
        if cop < copertura:
            problemi.append(f"contorno {i + 1} (centro {cx:.1f}, {cy:.1f}) percorso solo per il {cop:.0f} %: non lavorato?")
    if z_cima is not None:
        sotto = sum(1 for a, b in g["rapidi"] if (a[0], a[1]) != (b[0], b[1]) and min(a[2], b[2]) < z_cima - 1e-3)
        e["rapidi_sotto_la_cima"] = sotto
        if sotto: problemi.append(f"{sotto} rapidi G0 sotto la cima del materiale")
    e["problemi"] = problemi; e["esito"] = "OK" if not problemi else "BOCCIATO"
    return e

def contorni_dal_modello(z_sagoma, dx, dy, con_segmenti=False):
    from mcp_fusion import Sessione, corpo, testi
    s = Sessione()
    script = corpo(f"Z_SAGOMA = {z_sagoma}\n" + CONTORNI)
    r, _ = s.strumento("fusion_mcp_execute", {"featureType": "script", "object": {"script": script, "readOnly": True}})
    j = json.loads(testi(r)[0])
    if not j.get("success"):
        raise RuntimeError((j.get("error") or j.get("message") or "")[-400:])
    spigoli = []
    for l in (j.get("message") or "").splitlines():
        if l.startswith("SPG"): spigoli += json.loads(l[3:])
    sp_ = [[(x + dx, y + dy) for x, y in sp] for sp in spigoli]
    if con_segmenti:   # i segmenti di ogni spigolo, per sapere da che parte del bordo sta il materiale
        return contorni_collegati(sp_), [(a[0], a[1], b[0], b[1]) for sp in sp_ for a, b in zip(sp, sp[1:])]
    return contorni_collegati(sp_)

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(); a.add_argument("file"); a.add_argument("--raggio", type=float, required=True); a.add_argument("--z-fine", type=float, required=True)
    a.add_argument("--dx", type=float, default=0); a.add_argument("--dy", type=float, default=0); a.add_argument("--z-sagoma", type=float, default=0)
    a.add_argument("--z-cima", type=float); a.add_argument("--copertura", type=float, default=70.0)
    o = a.parse_args()
    g = analizza(open(o.file, encoding="utf-8", errors="replace").read())
    contorni, segmenti = contorni_dal_modello(o.z_sagoma, o.dx, o.dy, con_segmenti=True)
    r = verifica(g, contorni, o.raggio, o.z_fine, o.z_cima, o.copertura, segmenti=segmenti)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    sys.exit(0 if r["esito"] == "OK" else 1)

if __name__ == "__main__":
    main()
