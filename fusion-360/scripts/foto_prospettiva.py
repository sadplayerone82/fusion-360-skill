"""Photo taken at an angle → «top view» image at true scale (area P8, 04/11/2026).

Why it is needed: the Fusion canvas accepts only transforms with perpendicular axes (move, rotate, scale: API manual
`CanvasInput.transform`), so it does not remove perspective. The photo is rectified FIRST, with a homography computed from 4 points of a
flat reference of known size [OpenCV, «Geometric Transformations»: 3×3 matrix, 4 points of which 3 not collinear; straight lines stay
straight], then it is placed as a canvas with the scale of the rectified image (known px/mm).

Limits (model in P-studi-mancanti §P8):
- valid only for points ON THE PLANE of the reference; a point at height h, at distance d from the foot of a camera at height H, moves by
  e = d·h/(H − h) (parallax): put the reference at the same height as the part to be measured;
- lens distortion bends straight lines [OpenCV, «Camera Calibration»: x_d = x(1 + k1 r² + k2 r⁴ + k3 r⁶)], it grows towards the edges:
  object in the center of the photo, check with `dritto` on an edge known to be straight;
- the reference must be measured with a caliper (an A4 sheet can deviate by ±2 mm over 297 [ISO 216, secondary source]).

Usage (python -X utf8 foto_prospettiva.py …):
  raddrizza PHOTO OUTPUT.png "x1,y1 x2,y2 x3,y3 x4,y4" WIDTH_MM HEIGHT_MM [--pxmm 4] [--margine 60]
      reference corners in order: top-left, top-right, bottom-right, bottom-left (as seen in the photo); the output has the
      top-left corner of the reference at (margin, margin) mm; prints the matrix and the data for the canvas
  incertezza "x1,y1 …" WIDTH_MM HEIGHT_MM "u1,v1 u2,v2" [--sigma 1] [--prove 2000]
      error on the distance between two photo points if the corners are picked with ±sigma px (Monte Carlo)
  dritto "x1,y1 x2,y2 …"      maximum deviation (px) of the points from the line through the first and the last: > 1 px = distortion to correct
"""
import json, sys
import numpy as np

def omografia(src, dst):
    """Normalized DLT (Hartley): src, dst = N×2 (N ≥ 4) → 3×3 H with dst ~ H·src."""
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
    return np.array([[m, m], [m + larg, m], [m + larg, m + alt], [m, m + alt]])   # image: y pointing down

def raddrizza(foto, uscita, angoli_px, larg, alt, pxmm=4.0, margine=60.0):
    from PIL import Image
    im = np.asarray(Image.open(foto).convert("RGB"), float)
    H = omografia(angoli_px, angoli_mm(larg, alt, margine))          # photo → mm
    W, Hh = int(round((larg + 2 * margine) * pxmm)), int(round((alt + 2 * margine) * pxmm))
    jj, ii = np.meshgrid(np.arange(W), np.arange(Hh))
    mm = np.c_[(jj.ravel() + 0.5) / pxmm, (ii.ravel() + 0.5) / pxmm]
    p = applica(np.linalg.inv(H), mm) - 0.5                            # pixel center
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
                     "nota": "top-left corner of the reference at (margin, margin) mm from the top-left corner of the image"}}

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
    return {"scostamento_max_px": round(float(dev.max()), 2), "giudizio": "ok" if dev.max() <= 1.0 else "distortion: correct it or stay in the center"}

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
