"""Foto presa di sbieco → immagine «vista dall'alto» in scala vera (area P8, 04/11/2026).

Perché serve: la tela (canvas) di Fusion accetta solo trasformazioni con assi perpendicolari (sposta, ruota, scala: manuale API
`CanvasInput.transform`), quindi non toglie la prospettiva. La foto si raddrizza PRIMA, con un'omografia calcolata da 4 punti di un
riferimento piano di misura nota [OpenCV, «Geometric Transformations»: matrice 3×3, 4 punti di cui 3 non allineati; le rette restano
rette], poi si mette come tela con la scala dell'immagine raddrizzata (px/mm noto).

Limiti (modello in P-studi-mancanti §P8):
- vale solo per i punti SUL PIANO del riferimento; un punto alto h, a distanza d dal piede della fotocamera alta H, si sposta di
  e = d·h/(H − h) (parallasse): mettere il riferimento alla stessa altezza della parte da misurare;
- la distorsione dell'obiettivo piega le rette [OpenCV, «Camera Calibration»: x_d = x(1 + k1 r² + k2 r⁴ + k3 r⁶)], cresce verso i bordi:
  oggetto al centro della foto, controllo con `dritto` su un bordo che si sa dritto;
- il riferimento va misurato col calibro (un foglio A4 può scostarsi di ±2 mm su 297 [ISO 216, fonte secondaria]).

Uso (python -X utf8 foto_prospettiva.py …):
  raddrizza FOTO USCITA.png "x1,y1 x2,y2 x3,y3 x4,y4" LARG_MM ALT_MM [--pxmm 4] [--margine 60]
      angoli del riferimento in ordine: alto-sx, alto-dx, basso-dx, basso-sx (come si vedono nella foto); l'uscita ha l'angolo
      alto-sx del riferimento a (margine, margine) mm; stampa la matrice e i dati per la tela
  incertezza "x1,y1 …" LARG_MM ALT_MM "u1,v1 u2,v2" [--sigma 1] [--prove 2000]
      errore sulla distanza fra due punti della foto se gli angoli sono presi con ±sigma px (Monte Carlo)
  dritto "x1,y1 x2,y2 …"      scostamento massimo (px) dei punti dalla retta per il primo e l'ultimo: > 1 px = distorsione da correggere
"""
import json, sys
import numpy as np

def omografia(src, dst):
    """DLT normalizzata (Hartley): src, dst = N×2 (N ≥ 4) → H 3×3 con dst ~ H·src."""
    src, dst = np.asarray(src, float), np.asarray(dst, float)
    def norm(p):
        c = p.mean(0); s = np.sqrt(2) / np.mean(np.linalg.norm(p - c, axis=1))
        return np.array([[s, 0, -s * c[0]], [0, s, -s * c[1]], [0, 0, 1]])
    Ts, Td = norm(src), norm(dst)
    a = (Ts @ np.c_[src, np.ones(len(src))].T).T; b = (Td @ np.c_[dst, np.ones(len(dst))].T).T
    A = []
    for (x, y, _), (u, v, _) in zip(a, b):
        A.append([-x, -y, -1, 0, 0, 0, u * x, u * y, u]); A.append([0, 0, 0, -x, -y, -1, v * x, v * y, v])
    H = np.linalg.svd(np.asarray(A))[2][-1].reshape(3, 3)
    H = np.linalg.inv(Td) @ H @ Ts
    return H / H[2, 2]

def applica(H, p):
    p = np.atleast_2d(np.asarray(p, float)); q = (H @ np.c_[p, np.ones(len(p))].T).T
    return q[:, :2] / q[:, 2:3]

def angoli_mm(larg, alt, margine=0.0):
    m = margine
    return np.array([[m, m], [m + larg, m], [m + larg, m + alt], [m, m + alt]])   # immagine: y verso il basso

def raddrizza(foto, uscita, angoli_px, larg, alt, pxmm=4.0, margine=60.0):
    from PIL import Image
    im = np.asarray(Image.open(foto).convert("RGB"), float)
    H = omografia(angoli_px, angoli_mm(larg, alt, margine))          # foto → mm
    W, Hh = int(round((larg + 2 * margine) * pxmm)), int(round((alt + 2 * margine) * pxmm))
    jj, ii = np.meshgrid(np.arange(W), np.arange(Hh))
    mm = np.c_[(jj.ravel() + 0.5) / pxmm, (ii.ravel() + 0.5) / pxmm]
    p = applica(np.linalg.inv(H), mm) - 0.5                            # centro del pixel
    x, y = p[:, 0], p[:, 1]
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int); fx, fy = (x - x0)[:, None], (y - y0)[:, None]
    h, w = im.shape[:2]
    ok = (x0 >= 0) & (y0 >= 0) & (x0 < w - 1) & (y0 < h - 1)
    x0c, y0c = np.clip(x0, 0, w - 2), np.clip(y0, 0, h - 2)
    v = (im[y0c, x0c] * (1 - fx) * (1 - fy) + im[y0c, x0c + 1] * fx * (1 - fy)
         + im[y0c + 1, x0c] * (1 - fx) * fy + im[y0c + 1, x0c + 1] * fx * fy)
    v[~ok] = 0
    Image.fromarray(v.reshape(Hh, W, 3).clip(0, 255).astype(np.uint8)).save(uscita)
    return {"matrice_foto_a_mm": H.round(8).tolist(), "pixel_per_mm": pxmm, "uscita_px": [W, Hh],
            "tela": {"larghezza_mm": W / pxmm, "altezza_mm": Hh / pxmm,
                     "nota": "angolo alto-sx del riferimento a (margine, margine) mm dall'angolo alto-sx dell'immagine"}}

def incertezza(angoli_px, larg, alt, coppia, sigma=1.0, prove=2000, seme=1):
    rng = np.random.default_rng(seme); dst = angoli_mm(larg, alt)
    H = omografia(angoli_px, dst); a, b = applica(H, coppia); d0 = float(np.linalg.norm(a - b))
    ds = []
    for _ in range(prove):
        Hn = omografia(np.asarray(angoli_px, float) + rng.normal(0, sigma, (4, 2)), dst)
        a, b = applica(Hn, coppia); ds.append(np.linalg.norm(a - b))
    ds = np.asarray(ds)
    return {"distanza_mm": round(d0, 3), "dev_std_mm": round(float(ds.std()), 3), "errore_95_mm": round(float(1.96 * ds.std()), 3)}

def dritto(punti):
    p = np.asarray(punti, float); a, b = p[0], p[-1]; t = (b - a) / np.linalg.norm(b - a)
    dev = np.abs((p[:, 0] - a[0]) * t[1] - (p[:, 1] - a[1]) * t[0])
    return {"scostamento_max_px": round(float(dev.max()), 2), "giudizio": "ok" if dev.max() <= 1.0 else "distorsione: correggere o stare al centro"}

def _punti(s): return [tuple(float(v) for v in q.split(",")) for q in s.split()]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    def opz(nome, d):
        return float(a[a.index(nome) + 1]) if nome in a else d
    if a[0] == "raddrizza":
        r = raddrizza(a[1], a[2], _punti(a[3]), float(a[4]), float(a[5]), opz("--pxmm", 4.0), opz("--margine", 60.0))
    elif a[0] == "incertezza":
        r = incertezza(_punti(a[1]), float(a[2]), float(a[3]), _punti(a[4]), opz("--sigma", 1.0), int(opz("--prove", 2000)))
    elif a[0] == "dritto":
        r = dritto(_punti(a[1]))
    else:
        print(__doc__); return
    print(json.dumps(r, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
