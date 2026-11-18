# Foto in prospettiva raddrizzata; tavole con quote, riferimento, tolleranza e tabella fori

**Indice** (file lungo: cerca la sezione, non leggerlo intero)
| Riga | Ricetta | Quando |
|---|---|---|
| 19 | Misure da una foto di sbieco, raddrizzata dal riferimento | copiare un pezzo da una foto |
| 164 | Tavola con viste, quote, riferimento A, controllo di posizione e tabella fori | tavole 2D da consegnare |
| 363 | Correzioni dei singoli pezzi della tavola dopo il controllo del PDF | quando la tavola ha un difetto da correggere |

Ricette provate su Fusion (nov. 2026), ognuna con le misure attese calcolate prima e ritrovate nel modello. Ogni blocco è uno script
completo da lanciare con Python sul PC: parla con Fusion attraverso `scripts/mcp_fusion.py` (la riga `sys.path.insert` punta alla
cartella `scripts/` della skill installata in `~/.claude/skills/fusion-360`: cambiala se l'hai messa altrove) e manda a Fusion il
codice delle stringhe in maiuscolo (`CODICE`, `CODICI`…; lo script della foto invece lavora solo sul PC). In un modello vero copia la parte che serve negli script dei passi (`scripts/progetto_locale.py`).
Qui: foto raddrizzata con l'omografia dai 4 angoli di un riferimento (la tela di Fusion non toglie la prospettiva); tavola con quote
native una per chiamata, simboli GD&T e tabella fori come IMMAGINI calcolate dalle curve della vista (i comandi nativi si bloccano
600 s o si associano male), controllo sul PDF ingrandito. Gli script della tavola si lanciano un passo alla volta, con il nome del
passo come argomento.

## Misure da una foto di sbieco, raddrizzata con l'omografia dal riferimento (`scripts/foto_prospettiva.py`)

La foto è generata qui con un modello di fotocamera da telefono (provata solo con una foto generata, non ancora con una foto vera), poi misurata SENZA usare
la geometria vera: fori e bordi riconosciuti dall'immagine raddrizzata.
Scena (mm, piano del tavolo z = 0): foglio A4 210 × 297 (riferimento) con la flangia disegnata sopra (Ø 80, foro centrale Ø 30,
4 fori Ø 9 a ±30 dal centro (105, 150)), e un blocchetto 30 × 30 alto h = 10 con un bollino nero Ø 20 sopra, centro (105, 250).
Fotocamera: 4000 × 3000 px, f = 3000 px (circa 26 mm equivalenti), alta 450 mm, spostata di 250 mm → inclinata 29°; supercampionata 2×,
rumore σ = 2 livelli. Angoli del foglio «cliccati» con errore σ = 1 px. Casi: obiettivo senza distorsione (k1 = 0) e a botte k1 = −0,03.
Attesi: diametri e interassi veri; bollino spostato della parallasse e = d·h/(H − h) (calcolata prima).

Misurato (foto generata, obiettivo senza distorsione / a botte k1 = −0,03): flangia Ø 79,94 / 80,17 (vero 80); foro centrale
30,03 / 30,13; fori 9,02–9,04 / 9,04–9,06; posizioni dei fori entro 0,055 / 0,10; spostamento del bollino 3,413 (formula 3,409);
bordo dritto 0,0 px «ok» / 1,21 px «distorsione». Errore dei clic (±1 px) su 60 mm: ±0,10 mm (95 %). Regole: riferimento misurato
col calibro sullo stesso piano dei pezzi (un pezzo spesso 10 mm fotografato da 45 cm sposta i punti alti di ~3 mm); almeno ~5 px/mm;
pezzo al centro della foto; controllo `dritto` prima di fidarsi; quote critiche sempre dal calibro.

```python
"""Misure da una foto presa DI SBIECO, raddrizzata con l'omografia dal riferimento (foto_prospettiva.py, in scripts/ della skill).
La foto è generata qui con un modello di fotocamera da telefono (provata solo con una foto generata, non ancora con una foto vera), poi misurata SENZA usare
la geometria vera: fori e bordi riconosciuti dall'immagine raddrizzata.
Scena (mm, piano del tavolo z = 0): foglio A4 210 × 297 (riferimento) con la flangia disegnata sopra (Ø 80, foro centrale Ø 30,
4 fori Ø 9 a ±30 dal centro (105, 150)), e un blocchetto 30 × 30 alto h = 10 con un bollino nero Ø 20 sopra, centro (105, 250).
Fotocamera: 4000 × 3000 px, f = 3000 px (circa 26 mm equivalenti), alta 450 mm, spostata di 250 mm → inclinata 29°; supercampionata 2×,
rumore σ = 2 livelli. Angoli del foglio «cliccati» con errore σ = 1 px. Casi: obiettivo senza distorsione (k1 = 0) e a botte k1 = −0,03.
Attesi: diametri e interassi veri; bollino spostato della parallasse e = d·h/(H − h) (calcolata prima).
"""
import json, os, sys
import numpy as np
from PIL import Image
from scipy import ndimage
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # foto_prospettiva.py è in scripts/ della skill
import foto_prospettiva as FP

W, H_, F = 4000, 3000, 3000.0
C = np.array([105.0, 150.0 + 250.0, 450.0])            # fotocamera (x, y, z) in mm; y del foglio verso il «basso» dell'immagine raddrizzata
BERSAGLIO = np.array([105.0, 150.0, 0.0])
CX0, CY0, R_FL, R_C, R_F, DF = 105.0, 150.0, 40.0, 15.0, 4.5, 30.0
BLK = (90.0, 235.0, 120.0, 265.0); HB = 10.0; BOLL = (105.0, 250.0, 10.0)
COL = {"tavolo": 80, "foglio": 235, "flangia": 140, "lato": 60, "cima": 200, "bollino": 20}

def rotazione():
    z = BERSAGLIO - C; z /= np.linalg.norm(z)                  # asse ottico
    x = np.cross(z, [0, 0, 1.0]); x /= np.linalg.norm(x)        # destra dell'immagine
    y = np.cross(z, x)                                          # basso dell'immagine
    return np.vstack([x, y, z])                                 # mondo → camera

def colore_piano(X, Y):
    g = np.full(X.shape, COL["tavolo"], float)
    fog = (X >= 0) & (X <= 210) & (Y >= 0) & (Y <= 297); g[fog] = COL["foglio"]
    r = np.hypot(X - CX0, Y - CY0)
    fl = fog & (r <= R_FL) & (r > R_C)
    for dx, dy in ((DF, 0), (-DF, 0), (0, DF), (0, -DF)):
        fl &= np.hypot(X - CX0 - dx, Y - CY0 - dy) > R_F
    g[fl] = COL["flangia"]
    return g

def rendi(k1, seme=0):
    R = rotazione(); s = 2
    v, u = np.mgrid[0:H_ * s, 0:W * s].astype(float)
    xd, yd = ((u + 0.5) / s - W / 2) / F, ((v + 0.5) / s - H_ / 2) / F
    x, y = xd.copy(), yd.copy()
    for _ in range(8):                                          # togli la distorsione (iterazione)
        f = 1 + k1 * (x * x + y * y); x, y = xd / f, yd / f
    d = np.stack([x, y, np.ones_like(x)], -1) @ R               # direzione nel mondo
    t0 = -C[2] / d[..., 2]; X0, Y0 = C[0] + t0 * d[..., 0], C[1] + t0 * d[..., 1]
    g = colore_piano(X0, Y0)
    # blocchetto: cima a z = HB, lati scuri (intersezione raggio–scatola)
    tc = (HB - C[2]) / d[..., 2]; Xc, Yc = C[0] + tc * d[..., 0], C[1] + tc * d[..., 1]
    cima = (Xc >= BLK[0]) & (Xc <= BLK[2]) & (Yc >= BLK[1]) & (Yc <= BLK[3])
    tmin = np.zeros_like(t0); tmax = np.full_like(t0, np.inf)
    for k, (lo, hi) in enumerate(((BLK[0], BLK[2]), (BLK[1], BLK[3]), (0.0, HB))):
        a = (lo - C[k]) / d[..., k]; b = (hi - C[k]) / d[..., k]
        tmin = np.maximum(tmin, np.minimum(a, b)); tmax = np.minimum(tmax, np.maximum(a, b))
    scatola = tmin <= tmax
    g[scatola] = COL["lato"]
    g[cima] = COL["cima"]; g[cima & (np.hypot(Xc - BOLL[0], Yc - BOLL[1]) <= BOLL[2])] = COL["bollino"]
    g = g.reshape(H_, s, W, s).mean((1, 3)) + np.random.default_rng(seme).normal(0, 2, (H_, W))
    return g.clip(0, 255).astype(np.uint8), R

def proietta(P, R, k1):
    q = (np.asarray(P, float) - C) @ R.T; x, y = q[:, 0] / q[:, 2], q[:, 1] / q[:, 2]
    f = 1 + k1 * (x * x + y * y)
    return np.c_[x * f * F + W / 2, y * f * F + H_ / 2]

def misura(img, pxmm, margine):
    g = np.asarray(Image.open(img).convert("L"), float)
    mm = lambda p: (np.asarray(p, float) + 0.5) / pxmm - margine        # pixel → mm nel sistema del foglio
    fl = (g > 110) & (g < 180)                                           # flangia
    lab, n = ndimage.label(fl); grande = 1 + np.argmax(ndimage.sum(fl, lab, range(1, n + 1)))
    pieno = ndimage.binary_fill_holes(lab == grande)
    cy, cx = ndimage.center_of_mass(pieno); c = mm([cx, cy])
    ris = {"flangia": {"centro_mm": c.round(3).tolist(), "diametro_mm": round(2 * np.sqrt(pieno.sum() / np.pi) / pxmm, 3)}}
    buchi = pieno & ~(lab == grande)
    lb, nb = ndimage.label(buchi); fori = []
    for k in range(1, nb + 1):
        a = (lb == k).sum()
        if a < 20: continue
        yy, xx = ndimage.center_of_mass(lb == k); p = mm([xx, yy])
        fori.append({"centro_rel_mm": (p - c).round(3).tolist(), "diametro_mm": round(2 * np.sqrt(a / np.pi) / pxmm, 3)})
    ris["fori"] = sorted(fori, key=lambda f: -f["diametro_mm"])
    bo = g < 45; lb2, n2 = ndimage.label(bo)
    if n2:
        k = 1 + np.argmax(ndimage.sum(bo, lb2, range(1, n2 + 1))); yy, xx = ndimage.center_of_mass(lb2 == k)
        ris["bollino_centro_mm"] = mm([xx, yy]).round(3).tolist()
    return ris

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pxmm, marg = 5.0, 40.0
    # parallasse attesa del bollino (alto HB): proiezione dal centro della fotocamera sul piano z = 0
    P = np.array(BOLL[:2]); s = C[2] / (C[2] - HB); app = C[:2] + (P - C[:2]) * s
    attesi = {"flangia_d": 80.0, "foro_centrale_d": 30.0, "fori_d": 9.0, "interasse_fori": 30.0,
              "bollino_vero": P.tolist(), "bollino_apparente_atteso": app.round(3).tolist(),
              "parallasse_mm": round(float(np.linalg.norm(app - P)), 3),
              "formula_d_h_su_H_meno_h": round(float(np.linalg.norm(P - C[:2]) * HB / (C[2] - HB)), 3)}
    out = {"attesi": attesi, "casi": {}}
    for k1 in (0.0, -0.03):
        img, R = rendi(k1)
        nome = os.path.join(QUI, "foto_k%s.png" % ("0" if k1 == 0 else "m003"))
        Image.fromarray(img).save(nome)
        veri = proietta([[0, 0, 0], [210, 0, 0], [210, 297, 0], [0, 297, 0]], R, k1)
        clic = veri + np.random.default_rng(7).normal(0, 1.0, (4, 2))        # angoli presi a mano: ±1 px
        rad = nome.replace(".png", "_raddrizzata.png")
        info = FP.raddrizza(nome, rad, clic, 210, 297, pxmm, marg)
        m = misura(rad, pxmm, marg)
        # rettilineità del bordo lungo del foglio nella foto (11 punti veri proiettati): segnale della distorsione
        bordo = proietta([[0, y, 0] for y in np.linspace(0, 297, 11)], R, k1)
        inc = FP.incertezza(clic, 210, 297, proietta([[CX0 - DF, CY0, 0], [CX0 + DF, CY0, 0]], R, k1), 1.0, 1000)
        fori4 = [f for f in m["fori"] if f["diametro_mm"] < 20]
        out["casi"]["k1=%g" % k1] = {
            "flangia_d": m["flangia"]["diametro_mm"], "flangia_centro": m["flangia"]["centro_mm"],
            "foro_centrale_d": m["fori"][0]["diametro_mm"] if m["fori"] else None,
            "fori_d": [f["diametro_mm"] for f in fori4], "fori_pos": [f["centro_rel_mm"] for f in fori4],
            "bollino_apparente": m.get("bollino_centro_mm"),
            "bordo_dritto": FP.dritto(bordo), "incertezza_interasse_60mm_1px": inc,
            "scala_foto_px_per_mm_vicino_lontano": [round(float(np.linalg.norm(veri[1] - veri[0]) / 210), 2),
                                                     round(float(np.linalg.norm(veri[2] - veri[3]) / 210), 2)]}
    print(json.dumps(out, ensure_ascii=False, indent=1))
    json.dump(out, open(os.path.join(QUI, "prospettiva.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    main()
```

## Tavola della flangia con quote, riferimento A, controllo di posizione e tabella fori

Flangia salvata nel cloud (la tavola parte da lì): disco Ø 80 × 10, foro centrale Ø 30, 4 fori Ø 9 a ±30 mm.
Regole: un'operazione per chiamata, subito una lettura che fa uscire l'errore,
poi la coda di AcCore*.log: se l'ultima domanda del motore dei disegni è senza risposta, il comando è in attesa (non insistere).
Passi (argomento): `apri`, `viste`, `rif`, `fcf`, `fori`, `piano_b`, `pdf`, `stato`; i nomi del cloud si scrivono in cima ad `apri`.
Esito: il riferimento A nativo (`addDatumIdentifier`) resta appeso 600 s anche nella forma della guida → non usabile; il riquadro nativo
(`addFeatureControlFrame`) è inaffidabile (3 prove, 3 dialoghi diversi); la tabella fori nativa rifiuta un punto semplice e con il
centro di un cerchio resta appesa 600 s. Per questo riferimento, riquadro e tabella fori si fanno come **immagini** calcolate dalle
curve della vista (passo `piano_b`; tabella: F1 (0; 30), F2 (−30; 0), F3 (30; 0), F4 (0; −30), tutti Ø 9,0 = atteso). Le quote
native funzionano, una per chiamata (blocco seguente).

```python
"""Tavola della flangia con riferimento A, controllo di posizione e tabella fori, via API.
Flangia salvata nel cloud (la tavola parte da lì): disco Ø 80 × 10, foro centrale Ø 30, 4 fori Ø 9 a ±30 mm.
Regole: un'operazione per chiamata, subito una lettura che fa uscire l'errore,
poi la coda di AcCore*.log: se l'ultima domanda del motore dei disegni è senza risposta, il comando è in attesa (non insistere).
"""
import glob, json, os, sys, time
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

LOG = os.path.expandvars(r"%LOCALAPPDATA%\Autodesk\Autodesk Fusion 360")
PDF = os.path.abspath("tavola.pdf")   # dove esportare il PDF della tavola

TESTA = r'''
D = adsk.drawing; P2 = adsk.core.Point2D.create; DP = lambda x, y: D.DrawingPoint.create(P2(x, y))
dr = D.Drawing.cast(app.activeProduct); sh = dr.activeSheet if dr else None
def curva(v, cond):
    for j in range(v.viewCurves.count):
        c = v.viewCurves.item(j)
        if cond(c): return c
def vicino(p, x, y): return p is not None and abs(p.coordinate.x - x) < 0.01 and abs(p.coordinate.y - y) < 0.01
def stato():
    return {"documento": app.activeDocument.name, "viste": sh.views.count if sh else None,
            "simboli": sh.drawingSymbols.count if sh else None, "tabelle_fori": sh.holeTables.count if sh else None}
'''
CODICI = {
"apri": r'''
PROGETTO_CLOUD, CARTELLA_CLOUD, TAVOLA = "<progetto del cloud>", "<cartella del cloud>", "<nome della tavola>"   # sostituisci con i nomi del tuo cloud
prog = [app.data.dataProjects.item(k) for k in range(app.data.dataProjects.count) if app.data.dataProjects.item(k).name == PROGETTO_CLOUD][0]
cart = [prog.rootFolder.dataFolders.item(i) for i in range(prog.rootFolder.dataFolders.count) if prog.rootFolder.dataFolders.item(i).name == CARTELLA_CLOUD][0]
# se nel cloud ci sono due disegni con lo stesso nome si prende il più recente
for i in range(app.documents.count - 1, -1, -1):
    d_ = app.documents.item(i)
    if d_.name.startswith(TAVOLA): d_.close(False)
dfs = [cart.dataFiles.item(i) for i in range(cart.dataFiles.count) if cart.dataFiles.item(i).name == TAVOLA]
df = max(dfs, key=lambda f: f.dateCreated)
app.documents.open(df, True)
dr = D.Drawing.cast(app.activeProduct); sh = dr.activeSheet
out(file=[(cart.dataFiles.item(i).name, cart.dataFiles.item(i).latestVersionNumber) for i in range(cart.dataFiles.count)], **stato())''',
"viste": r'''
# vista dall'alto (pianta) e di fronte, scala 1:1, sul foglio A3 (coordinate in mm, misurate: la guida dice cm ma il foglio è in mm)
for nome, ori, x, y in (("alto", D.ViewOrientationTypes.TopViewOrientationType, 140, 180), ("fronte", D.ViewOrientationTypes.FrontViewOrientationType, 140, 80)):
    vi = sh.views.createBaseViewInput(); vp = vi.viewParameters; vp.orientation = ori; vp.scaleValue = 1.0
    vi.placementPoint = DP(x, y)
    v = sh.views.add(vi); v.scaleValue = 1.0; v.style = D.DrawingViewStyleTypes.VisibleAndHiddenEdgesDrawingViewStyleType
out(**stato())''',
"rif": r'''
fronte = sh.views.item(1)
# la linea di base nella vista di fronte è il cerchio Ø 80 visto di taglio: ha centerPoint (140, 75), non midPoint (03/11)
fondo = curva(fronte, lambda c: vicino(c.centerPoint, 140, 75))
di = sh.drawingSymbols.createDatumIdentifierInput(); di.viewCurve = fondo; di.identifier = "A"
# guida API: «solo posizione, senza piega» = stessi punti per leaderPoints e placementPoint
di.leaderPoints = [DP(165, 62), DP(165, 62)]; di.placementPoint = DP(165, 62)
sh.drawingSymbols.addDatumIdentifier(di)
out(**stato())''',
"fcf": r'''
alto = sh.views.item(0)
foro = curva(alto, lambda c: vicino(c.centerPoint, 170, 180) and abs(c.startPoint.coordinate.x - 165.5) < 0.01)
fi = sh.drawingSymbols.createFeatureControlFrameInput(); fi.viewCurve = foro
fr = fi.firstFrame
fr.geometricCharacteristic = D.GeometricCharacteristicTypes.PositionGeometricCharacteristicType
tol = fr.primaryTolerance; tol.appendText("0,1"); fr.primaryTolerance = tol
da = fr.primaryDatum; da.appendText("A"); fr.primaryDatum = da      # firstFrame è di sola lettura: si modifica sul posto (04/11)
fi.leaderPoints = [DP(195, 200), DP(195, 200)]; fi.placementPoint = DP(195, 200)
sh.drawingSymbols.addFeatureControlFrame(fi)
out(**stato())''',
"fori": r'''
alto = sh.views.item(0)
centro = curva(alto, lambda c: vicino(c.centerPoint, 140, 180) and abs(c.startPoint.coordinate.x - 125) < 0.01)
hi = sh.holeTables.createInput(); hi.view = alto; hi.originPoint = DP(140, 180); hi.title = "Tabella fori"
sh.holeTables.add(hi)
out(**stato())''',
"pdf": r'''
o = dr.exportManager.createPDFExportOptions(PDF); o.openPDF = False
out(pdf=dr.exportManager.execute(o), **stato())''',
"stato": r'''out(**stato())''',
"misura_fori": r'''
alto = sh.views.item(0)
cerchi = []
for j in range(alto.viewCurves.count):
    c = alto.viewCurves.item(j)
    if c.centerPoint is not None and c.midPoint is None:
        k = c.centerPoint.coordinate; s = c.startPoint.coordinate
        cerchi.append([round(k.x, 3), round(k.y, 3), round(((s.x - k.x) ** 2 + (s.y - k.y) ** 2) ** 0.5, 3)])
out(scala=alto.scaleValue, cerchi=cerchi, **stato())''',
"piano_b": r'''
# simboli come immagini (larghezza = 58 mm × scala, angolo in basso a sinistra) + linee di richiamo nello schizzo del foglio
n = 0
for p, x, y, s in IMMAGINI:
    ii = sh.images.createInput(); ii.imageFilePath = p; ii.position = P2(x, y); ii.scale = s
    if sh.images.insert(ii): n += 1
sk = sh.sketches.add()
for a, b in RICHIAMI: sk.lines.add([P2(*a), P2(*b)])
out(immagini=n, richiami=len(RICHIAMI), **stato())''',
}

# ---- piano B (04/11): riferimento A, riquadro di posizione e tabella fori come immagini (l'API dei simboli resta appesa)
PXMM = 12                      # pixel per mm sul foglio
def _font(h, bold=False):
    from PIL import ImageFont
    return ImageFont.truetype("arialbd.ttf" if bold else "arial.ttf", int(h * PXMM / 0.72))

def immagini_gdt(cerchi, scala):
    """cerchi: [x, y, r] in mm sul foglio (dalla vista dall'alto); origine = centro del cerchio più grande."""
    from PIL import Image, ImageDraw
    qui = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/tavola_img/"
    os.makedirs(qui, exist_ok=True)
    out_ = []
    def salva(im, nome, x, y, larg_mm):
        p = qui + nome + ".png"; im.save(p); out_.append((p, x, y, round(larg_mm / 58.0, 5))); return p
    lw = 3
    # riferimento A: quadrato 7 mm con la lettera, triangolo pieno sotto (verso la linea di base)
    q = 7 * PXMM; im = Image.new("RGB", (q, q + 4 * PXMM), "white"); d = ImageDraw.Draw(im)
    d.rectangle([1, 1, q - 2, q - 2], outline="black", width=lw)
    d.text((q / 2, q / 2), "A", fill="black", font=_font(3.5), anchor="mm")
    d.line([(q / 2, q), (q / 2, q + 2 * PXMM)], fill="black", width=lw)
    d.polygon([(q / 2 - 1.5 * PXMM, q + 4 * PXMM - 1), (q / 2 + 1.5 * PXMM, q + 4 * PXMM - 1), (q / 2, q + 2 * PXMM)], fill="black")
    salva(im, "rif_A", 156.5, 75.0, 7.0)                    # triangolo appoggiato sulla linea di base (y = 75) a x = 160
    # riquadro di posizione: | ⌖ | ⌀0,1 | A |
    cel = [8, 16, 8]; h = 7; W = sum(cel) * PXMM; im = Image.new("RGB", (W, h * PXMM), "white"); d = ImageDraw.Draw(im)
    d.rectangle([1, 1, W - 2, h * PXMM - 2], outline="black", width=lw)
    x = 0
    for k, c in enumerate(cel[:-1]):
        x += c * PXMM; d.line([(x, 0), (x, h * PXMM)], fill="black", width=lw)
    cx, cy, r = cel[0] * PXMM / 2, h * PXMM / 2, 2.2 * PXMM                       # simbolo di posizione
    d.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], outline="black", width=lw)
    d.line([(cx - r, cy), (cx + r, cy)], fill="black", width=lw); d.line([(cx, cy - r), (cx, cy + r)], fill="black", width=lw)
    d.text(((cel[0] + cel[1] / 2) * PXMM, cy), "⌀ 0,1", fill="black", font=_font(3.5), anchor="mm")
    d.text(((cel[0] + cel[1] + cel[2] / 2) * PXMM, cy), "A", fill="black", font=_font(3.5), anchor="mm")
    salva(im, "fcf_posizione", 185.0, 205.0, sum(cel))
    # tabella fori dalla vista: origine = centro del cerchio più grande, fori = cerchi con r < 10 mm
    o = max(cerchi, key=lambda c: c[2]); fori = sorted([c for c in cerchi if c[2] < 10], key=lambda c: (-(c[1] - o[1]), c[0] - o[0]))
    v = lambda x: ("%.1f" % x).replace(".", ",")                     # virgola decimale, come le quote della tavola (04/11)
    righe = [("F%d" % (i + 1), v((c[0] - o[0]) / scala), v((c[1] - o[1]) / scala), "Ø " + v(2 * c[2] / scala))     # Ø: «⌀» (U+2300) non c'è in Arial (04/11)
             for i, c in enumerate(fori)]
    col = [12, 18, 18, 22]; hr = 6; righe_tab = [("Foro", "X", "Y", "Diametro")] + righe
    W = sum(col) * PXMM; H = (len(righe_tab) + 1) * hr * PXMM
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    d.rectangle([1, 1, W - 2, H - 2], outline="black", width=lw)
    d.text((W / 2, hr * PXMM / 2), "Tabella fori (origine: centro, mm)", fill="black", font=_font(3.0, True), anchor="mm")
    for i, rg in enumerate(righe_tab):
        y0 = (i + 1) * hr * PXMM; d.line([(0, y0), (W, y0)], fill="black", width=lw)
        x = 0
        for c, t in zip(col, rg):
            d.text((x + c * PXMM / 2, y0 + hr * PXMM / 2), t, fill="black", font=_font(3.0, i == 0), anchor="mm")
            x += c * PXMM
            if x < W: d.line([(x, hr * PXMM), (x, H)], fill="black", width=lw)
    salva(im, "tabella_fori", 230.0, 140.0, sum(col))
    # sigle dei fori nella vista: 5 × 4 mm, angolo a 3,6 mm in diagonale dal centro (5,1 mm > raggio 4,5); verso il basso a destra
    # se in alto a destra passa il richiamo del riquadro (foro a x 170, y 180)
    for i, c in enumerate(fori):
        im = Image.new("RGB", (5 * PXMM, 4 * PXMM), "white"); d = ImageDraw.Draw(im)
        d.text((2.5 * PXMM, 2 * PXMM), "F%d" % (i + 1), fill="black", font=_font(2.5, True), anchor="mm")
        giu = abs(c[0] - 170) < 0.01 and abs(c[1] - 180) < 0.01
        salva(im, "sigla_F%d" % (i + 1), c[0] + 3.6, c[1] - 7.6 if giu else c[1] + 3.6, 5.0)
    richiami = [((170.0 + 4.5 * 0.7071, 180.0 + 4.5 * 0.7071), (185.0, 208.5))]   # dal bordo del foro F (170, 180) al riquadro
    return out_, richiami, righe

def coda_accore(n=12):
    f = sorted(glob.glob(os.path.join(LOG, "*", "logs", "AcCore*.log")), key=os.path.getmtime)[-1]
    righe = [r for r in open(f, encoding="utf-8", errors="replace").read().splitlines() if r.strip()]
    return righe[-n:]

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    passo = sys.argv[1]
    t = time.time()
    extra = ""
    if passo == "piano_b":
        ok, m, _ = esegui(Sessione(), TESTA + CODICI["misura_fori"], sola_lettura=True)
        imm, rich, tab = immagini_gdt(m["cerchi"], m["scala"])
        imm = [i for i in imm if "fcf_" not in i[0]]; rich = []      # il riquadro nativo funziona (04/11): niente immagine
        if len(sys.argv) > 2: imm = [i for i in imm if sys.argv[2] in i[0]]   # solo un'immagine (correzione del singolo pezzo)
        print("tabella fori calcolata:", tab)
        extra = f"IMMAGINI = {imm!r}\nRICHIAMI = {rich!r}\n"
    ok, r, righe = esegui(Sessione(), f"PDF = {PDF!r}\n" + extra + TESTA + CODICI[passo], sola_lettura=passo in ("stato", "misura_fori"))
    print(json.dumps({"passo": passo, "secondi": round(time.time() - t, 1), "risultato": r if r else righe}, ensure_ascii=False, indent=1))
    coda = coda_accore()
    print("--- AcCore (ultime righe)"); print("\n".join(coda))
    domanda = coda[-1].rstrip()
    if domanda.endswith(("INVIO", "origine", "punto", ":")) and "Comando:" not in domanda:
        print("!!! ATTENZIONE: il motore dei disegni sembra in attesa di una risposta (comando bloccato)")

if __name__ == "__main__":
    main()
```

## Correzioni dei singoli pezzi della tavola dopo il controllo del PDF (simboli e immagini non si cancellano via API)

1. tabella: «⌀» (U+2300) assente in Arial → quadratino; nuova tabella con «Ø» sovrapposta (le immagini sono opache).
2. riferimento A: era dentro la vista e copriva il bordo superiore (y 85) e un tratto di quello inferiore (y 75) → «cerotto» bianco
   con le due linee ridisegnate (0,5 mm, come i bordi visibili) + nuovo riferimento SOTTO la vista, triangolo appoggiato al bordo.
3. riquadro di posizione: senza ⌀ e sopra il bordo del disco → nuovo riquadro nativo con ⌀ (DiameterSymbolPaletteType) fuori dal
   disco; quello vecchio va cancellato a mano (l'API non ha delete per i simboli).
Usa le funzioni del blocco precedente: salvalo nella stessa cartella come modulo `tavola_flangia` (è il nome che si importa qui).
Passi (argomento): `tabella`, `rif`, `rif_nuovo`, `fcf`, `nota_fcf`, e le quote native `d80`, `d30`, `s10`. Errori corretti così, uno
alla volta, con un'immagine opaca sovrapposta: «⌀» (U+2300) assente in Arial → «Ø»; punto decimale → virgola; riferimento dentro la
vista → «cerotto» con i bordi ridisegnati e riferimento nuovo sotto; la quota Ø 30 col testo sotto la linea della Ø 80 → rifatta sulla
diagonale libera. Quote e simboli sbagliati si cancellano solo a mano sullo schermo (dirlo prima all'utente).

```python
"""Correzioni dei singoli pezzi della tavola dopo il controllo del PDF; simboli e immagini non si cancellano via API.
1. tabella: «⌀» (U+2300) assente in Arial → quadratino; nuova tabella con «Ø» sovrapposta (le immagini sono opache).
2. riferimento A: era dentro la vista e copriva il bordo superiore (y 85) e un tratto di quello inferiore (y 75) → «cerotto» bianco
   con le due linee ridisegnate (0,5 mm, come i bordi visibili) + nuovo riferimento SOTTO la vista, triangolo appoggiato al bordo.
3. riquadro di posizione: senza ⌀ e sopra il bordo del disco → nuovo riquadro nativo con ⌀ (DiameterSymbolPaletteType) fuori dal
   disco; quello vecchio va cancellato a mano (l'API non ha delete per i simboli).
"""
import json, os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))   # qui c'è il blocco precedente, salvato come tavola_flangia
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
import tavola_flangia as T
from mcp_fusion import Sessione, esegui

PX = T.PXMM; QUI = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/") + "/tavola_img/"

def immagine(nome, im, x, y, larg_mm):
    p = QUI + nome + ".png"; im.save(p); return (p, x, y, round(larg_mm / 58.0, 5))

def tabella():
    ok, m, _ = esegui(Sessione(), T.TESTA + T.CODICI["misura_fori"], sola_lettura=True)
    imm, _, righe = T.immagini_gdt(m["cerchi"], m["scala"])
    return [i for i in imm if "tabella_fori" in i[0]], righe

def rif():
    lw = int(0.5 * PX)
    # cerotto: copre x 156,5–163,5, y 74,5–86,5 e ridisegna i bordi a y 75 e y 85
    w, h = 7.0, 12.0; y0 = 74.5
    im = Image.new("RGB", (int(w * PX), int(h * PX)), "white"); d = ImageDraw.Draw(im)
    for yl in (75.0, 85.0):
        yp = (y0 + h - yl) * PX; d.line([(0, yp), (w * PX, yp)], fill="black", width=lw)
    cer = immagine("cerotto_rif", im, 156.5, y0, w)
    # nuovo riferimento sotto la vista: triangolo pieno con la base sul bordo (y 75), gambo, riquadro 7 × 7 con «A»
    q = 7 * PX; im = Image.new("RGB", (q, q + 4 * PX), "white"); d = ImageDraw.Draw(im)
    d.polygon([(q / 2 - 1.5 * PX, 0), (q / 2 + 1.5 * PX, 0), (q / 2, 2 * PX)], fill="black")
    d.line([(q / 2, 2 * PX), (q / 2, 4 * PX)], fill="black", width=3)
    d.rectangle([1, 4 * PX, q - 2, q + 4 * PX - 2], outline="black", width=3)
    d.text((q / 2, 4 * PX + q / 2), "A", fill="black", font=T._font(3.5), anchor="mm")
    # il bordo y 75 (0,5 mm) è disegnato dentro l'immagine, in alto: senza, il fondo bianco lo tagliava (04/11)
    im2 = Image.new("RGB", (q, q + 4 * PX + int(0.5 * PX)), "white"); im2.paste(im, (0, int(0.5 * PX)))
    ImageDraw.Draw(im2).line([(0, int(0.25 * PX)), (q, int(0.25 * PX))], fill="black", width=int(0.5 * PX))
    nuovo = immagine("rif_A_sotto", im2, 156.5, 75.0 + 0.25 - 11.5, 7.0)
    return [cer, nuovo]

FCF = r'''
alto = sh.views.item(0)
foro = curva(alto, lambda c: vicino(c.centerPoint, 140, 210) and abs(c.startPoint.coordinate.x - 135.5) < 0.01)   # foro F1
fi = sh.drawingSymbols.createFeatureControlFrameInput(); fi.viewCurve = foro
fr = fi.firstFrame
fr.geometricCharacteristic = D.GeometricCharacteristicTypes.PositionGeometricCharacteristicType
tol = fr.primaryTolerance; tol.append(D.SymbolPaletteTypes.DiameterSymbolPaletteType); tol.appendText("0,1"); fr.primaryTolerance = tol
da = fr.primaryDatum; da.appendText("A"); fr.primaryDatum = da
# 1° punto SUL foro (il motore lo chiede come «punto iniziale»: se è lontano il simbolo non si associa, 04/11), 2° = posizione
fi.leaderPoints = [DP(143.182, 213.182), DP(168, 230)]; fi.placementPoint = DP(168, 230)
sh.drawingSymbols.addFeatureControlFrame(fi)
out(**stato())'''


QUOTE = {   # quote principali native: una tavola senza ingombri e diametri è incompleta
"d80": "alto = sh.views.item(0); c = curva(alto, lambda c: vicino(c.centerPoint, 140, 180) and abs(c.startPoint.coordinate.x - 180) < 0.01)\n"
       "sh.drawingDimensions.addDiameterDimension(c, DP(98, 224))",
"d30": "alto = sh.views.item(0); c = curva(alto, lambda c: vicino(c.centerPoint, 140, 180) and abs(c.startPoint.coordinate.x - 125) < 0.01)\n"
       "sh.drawingDimensions.addDiameterDimension(c, DP(96, 136))   # 04/11: a (118, 198) «creation failed»; a (140, 186) il testo stava sotto la linea della Ø80: fuori, sulla diagonale libera",
"s10": "fr = sh.views.item(1); c = curva(fr, lambda c: c.midPoint is not None and vicino(c.startPoint, 180, 75) and vicino(c.endPoint, 180, 85))\n"
       "sh.drawingDimensions.addLinearDimension(c.startPoint, c.endPoint, DP(192, 80))",
}

def nota_fcf():
    """Riquadro come nota sotto la tabella fori (04/11): il riquadro nativo è inaffidabile (3 prove, 3 dialoghi diversi)."""
    lw = 3; h = 7; testo = 26; cel = [8, 16, 8]          # 26: a 22 la scritta toccava il riquadro (04/11)
    W = (testo + sum(cel)) * PX; im = Image.new("RGB", (W, h * PX), "white"); d = ImageDraw.Draw(im)
    d.text((testo * PX / 2, h * PX / 2), "Fori F1–F4:", fill="black", font=T._font(3.0, True), anchor="mm")
    x0 = testo * PX; d.rectangle([x0, 1, W - 2, h * PX - 2], outline="black", width=lw)
    x = x0
    for c in cel[:-1]:
        x += c * PX; d.line([(x, 0), (x, h * PX)], fill="black", width=lw)
    cx, cy, r = x0 + cel[0] * PX / 2, h * PX / 2, 2.2 * PX
    d.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], outline="black", width=lw)
    d.line([(cx - r, cy), (cx + r, cy)], fill="black", width=lw); d.line([(cx, cy - r), (cx, cy + r)], fill="black", width=lw)
    d.text((x0 + (cel[0] + cel[1] / 2) * PX, cy), "Ø0,1", fill="black", font=T._font(3.5), anchor="mm")
    d.text((x0 + (cel[0] + cel[1] + cel[2] / 2) * PX, cy), "A", fill="black", font=T._font(3.5), anchor="mm")
    return [immagine("nota_fcf", im, 230.0, 130.0, testo + sum(cel))]          # 3 mm sotto la tabella (fondo a y 140)

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    passo = sys.argv[1]
    if passo in QUOTE:
        codice = QUOTE[passo] + "\nout(quote=sh.drawingDimensions.count, **stato())"
    elif passo == "nota_fcf":
        codice = f"IMMAGINI = {nota_fcf()!r}\nRICHIAMI = []\n" + T.CODICI["piano_b"]
    elif passo == "fcf":
        codice = FCF
    else:
        imm = tabella()[0] if passo == "tabella" else (rif()[1:] if passo == "rif_nuovo" else rif())
        codice = f"IMMAGINI = {imm!r}\nRICHIAMI = []\n" + T.CODICI["piano_b"]
    ok, r, righe = esegui(Sessione(), T.TESTA + codice, sola_lettura=False)
    print(json.dumps(r if r else righe, ensure_ascii=False, indent=1))
    print("--- AcCore"); print("\n".join(T.coda_accore(6)))

if __name__ == "__main__":
    main()
```

