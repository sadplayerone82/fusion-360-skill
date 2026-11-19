"""Simboli e tabelle delle tavole come IMMAGINI calcolate dalla vista (da P13, 04/11/2026; generalizzato il 05/11).

Perché immagini: i comandi nativi di Fusion per riferimenti e tabella fori si bloccano 600 s e il riquadro di tolleranza si associa male.
Le immagini non si cancellano via API: una correzione si fa sovrapponendo un'immagine giusta (sono opache).
Regola delle immagini sul foglio: larghe 58 mm × scala qualunque siano i pixel; posizione = angolo in basso a sinistra, in mm.
I numeri della tabella vengono dalle CURVE della vista, mai scritti a mano. Dopo: PDF guardato ingrandito (`references/tavole-e-render.md`).

Con una tavola attiva in Fusion:
  python -X utf8 tavola_simboli.py tabella CARTELLA --vista 0 --r-max 10 --x 230 --y 140 [--scala 1] [--origine X,Y] [--sigle]
      fori = cerchi della vista con raggio sul foglio < r-max (obbligatorio: a chi lo usa la scelta); origine = coordinate sul foglio,
      predefinita il centro del cerchio più grande; --sigle mette F1, F2… accanto ai fori
  python -X utf8 tavola_simboli.py riferimento CARTELLA --lettera A --x 156.5 --y 63.75
      triangolo in alto (da appoggiare a un bordo orizzontale, dal basso), riquadro sotto
  python -X utf8 tavola_simboli.py riquadro CARTELLA --valore 0,1 [--diametro] --rif A [--testo "Fori F1–F4:"] --x 230 --y 130
      controllo di posizione: simbolo | valore | riferimento
Formato del foglio per il controllo dei bordi: --foglio 420,297 (predefinito A3 orizzontale).
"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PXMM = 12         # pixel per mm sul foglio
LARGHEZZA_BASE = 58.0

def _font(h, grassetto=False):
    from PIL import ImageFont
    return ImageFont.truetype("arialbd.ttf" if grassetto else "arial.ttf", int(h * PXMM / 0.72))

def virgola(x, dec=1):
    return f"{x:.{dec}f}".replace(".", ",").replace("-0,0", "0,0") if abs(x) < 0.05 else f"{x:.{dec}f}".replace(".", ",")

def righe_tabella(cerchi, scala, r_max, origine=None):
    """cerchi: [x, y, r] sul foglio (mm). Restituisce (righe, origine, fori): Ø e posizioni in mm del pezzo (divisi per la scala).
    I doppioni (stesso centro e raggio: un foro visto sopra e sotto) contano una volta."""
    if not cerchi:
        raise ValueError("nessun cerchio nella vista")
    o = origine or max(cerchi, key=lambda c: c[2])[:2]
    visti, fori = set(), []
    for c in cerchi:
        k = (round(c[0], 2), round(c[1], 2), round(c[2], 2))
        if c[2] < r_max and k not in visti:
            visti.add(k); fori.append(c)
    if not fori:
        raise ValueError(f"nessun foro con raggio sul foglio < {r_max}: controlla --r-max")
    fori.sort(key=lambda c: (-(round(c[1] - o[1], 2)), round(c[0] - o[0], 2)))
    righe = [(f"F{i + 1}", virgola((c[0] - o[0]) / scala), virgola((c[1] - o[1]) / scala), "Ø " + virgola(2 * c[2] / scala)) for i, c in enumerate(fori)]
    return righe, list(o), fori

def immagine_tabella(righe, titolo="Tabella fori (mm)"):
    from PIL import Image, ImageDraw
    col, hr, lw = [12, 18, 18, 22], 6, 3
    tab = [("Foro", "X", "Y", "Diametro")] + righe
    W, H = sum(col) * PXMM, (len(tab) + 1) * hr * PXMM
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    d.rectangle([1, 1, W - 2, H - 2], outline="black", width=lw)
    d.text((W / 2, hr * PXMM / 2), titolo, fill="black", font=_font(3.0, True), anchor="mm")
    for i, rg in enumerate(tab):
        y0 = (i + 1) * hr * PXMM; d.line([(0, y0), (W, y0)], fill="black", width=lw); x = 0
        for c, t in zip(col, rg):
            d.text((x + c * PXMM / 2, y0 + hr * PXMM / 2), t, fill="black", font=_font(3.0, i == 0), anchor="mm")
            x += c * PXMM
            if x < W: d.line([(x, hr * PXMM), (x, H)], fill="black", width=lw)
    return im, sum(col), (len(tab) + 1) * hr

def immagine_riferimento(lettera):
    from PIL import Image, ImageDraw
    q = 7 * PXMM; im = Image.new("RGB", (q, q + 4 * PXMM), "white"); d = ImageDraw.Draw(im)
    d.polygon([(q / 2 - 1.5 * PXMM, 0), (q / 2 + 1.5 * PXMM, 0), (q / 2, 2 * PXMM)], fill="black")
    d.line([(q / 2, 2 * PXMM), (q / 2, 4 * PXMM)], fill="black", width=3)
    d.rectangle([1, 4 * PXMM, q - 2, q + 4 * PXMM - 2], outline="black", width=3)
    d.text((q / 2, 4 * PXMM + q / 2), lettera, fill="black", font=_font(3.5), anchor="mm")
    return im, 7.0, 11.0

def immagine_riquadro(valore, rif, diametro=False, testo=None):
    from PIL import Image, ImageDraw
    lw, h = 3, 7; cel = [8, 16, 8]; tx = 26 if testo else 0
    W = (tx + sum(cel)) * PXMM; im = Image.new("RGB", (W, h * PXMM), "white"); d = ImageDraw.Draw(im)
    if testo:
        d.text((tx * PXMM / 2, h * PXMM / 2), testo, fill="black", font=_font(3.0, True), anchor="mm")
    x0 = tx * PXMM; d.rectangle([x0, 1, W - 2, h * PXMM - 2], outline="black", width=lw); x = x0
    for c in cel[:-1]:
        x += c * PXMM; d.line([(x, 0), (x, h * PXMM)], fill="black", width=lw)
    cx, cy, r = x0 + cel[0] * PXMM / 2, h * PXMM / 2, 2.2 * PXMM      # simbolo di posizione: cerchio con la croce
    d.ellipse([cx - r * 0.6, cy - r * 0.6, cx + r * 0.6, cy + r * 0.6], outline="black", width=lw)
    d.line([(cx - r, cy), (cx + r, cy)], fill="black", width=lw); d.line([(cx, cy - r), (cx, cy + r)], fill="black", width=lw)
    d.text((x0 + (cel[0] + cel[1] / 2) * PXMM, cy), ("Ø" if diametro else "") + valore, fill="black", font=_font(3.5), anchor="mm")
    d.text((x0 + (cel[0] + cel[1] + cel[2] / 2) * PXMM, cy), rif, fill="black", font=_font(3.5), anchor="mm")
    return im, tx + sum(cel), h

def immagine_sigla(testo):
    from PIL import Image, ImageDraw
    im = Image.new("RGB", (5 * PXMM, 4 * PXMM), "white")
    ImageDraw.Draw(im).text((2.5 * PXMM, 2 * PXMM), testo, fill="black", font=_font(2.5, True), anchor="mm")
    return im, 5.0, 4.0

def dentro_foglio(x, y, larg, alt, foglio):
    if x < 0 or y < 0 or x + larg > foglio[0] or y + alt > foglio[1]:
        raise ValueError(f"l'immagine ({x}, {y}) {larg} × {alt} mm esce dal foglio {foglio[0]} × {foglio[1]}")

LEGGI = r'''
D = adsk.drawing; sh = D.Drawing.cast(app.activeProduct).activeSheet
v = sh.views.item(VISTA); c_ = []
for j in range(v.viewCurves.count):
    c = v.viewCurves.item(j)
    if c.centerPoint is not None and c.midPoint is None:
        k = c.centerPoint.coordinate; s_ = c.startPoint.coordinate
        c_.append([round(k.x, 3), round(k.y, 3), round(((s_.x - k.x) ** 2 + (s_.y - k.y) ** 2) ** 0.5, 3)])
try: sc_ = v.scaleValue           # su una tavola riaperta dà «failed to read view scale» (05/11): allora serve --scala
except Exception: sc_ = None
out(scala=sc_, cerchi=c_, viste=sh.views.count)
'''
INSERISCI = r'''
D = adsk.drawing; sh = D.Drawing.cast(app.activeProduct).activeSheet; n = 0
for p, x, y, s_ in IMMAGINI:
    ii = sh.images.createInput(); ii.imageFilePath = p; ii.position = adsk.core.Point2D.create(x, y); ii.scale = s_
    if sh.images.insert(ii): n += 1
out(inserite=n, attese=len(IMMAGINI))     # sheet.images ha solo createInput e insert: il totale si conta nel PDF esportato
'''

def leggi_vista(s, vista):
    from mcp_fusion import esegui
    ok, r, righe = esegui(s, f"VISTA = {vista}\n" + LEGGI, sola_lettura=True)
    if not ok or not r:
        raise RuntimeError("vista non letta (è attiva una tavola?): " + " ".join(righe))
    return r

def inserisci(s, immagini):
    """immagini: [(percorso, x, y, larghezza_mm)]"""
    from mcp_fusion import esegui
    voci = [(p.replace("\\", "/"), x, y, round(l / LARGHEZZA_BASE, 5)) for p, x, y, l in immagini]
    righe_ = ",\n    ".join(repr(v) for v in voci)
    ok, r, righe = esegui(s, f"IMMAGINI = [\n    {righe_}\n]\n" + INSERISCI)
    if not ok or not r or r["inserite"] != r["attese"]:
        raise RuntimeError("immagini non inserite: " + str(r or righe))
    return r

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = argparse.ArgumentParser(); a.add_argument("cosa", choices=("tabella", "riferimento", "riquadro")); a.add_argument("cartella")
    a.add_argument("--x", type=float, required=True); a.add_argument("--y", type=float, required=True); a.add_argument("--foglio", default="420,297")
    a.add_argument("--vista", type=int, default=0); a.add_argument("--r-max", type=float); a.add_argument("--origine"); a.add_argument("--sigle", action="store_true"); a.add_argument("--scala", type=float)
    a.add_argument("--lettera", default="A"); a.add_argument("--valore"); a.add_argument("--diametro", action="store_true"); a.add_argument("--rif", default="A"); a.add_argument("--testo")
    o = a.parse_args()
    from mcp_fusion import Sessione
    foglio = [float(v) for v in o.foglio.split(",")]; os.makedirs(o.cartella, exist_ok=True); s = Sessione(); voci = []; info = {}
    def metti(nome, im, x, y, larg, alt):
        dentro_foglio(x, y, larg, alt, foglio)
        p = os.path.join(o.cartella, nome + ".png"); im.save(p); voci.append((p, x, y, larg))
    if o.cosa == "tabella":
        if o.r_max is None:
            a.error("--r-max è obbligatorio: decide quali cerchi sono fori")
        v = leggi_vista(s, o.vista)
        scala = o.scala or v["scala"]
        if not scala:           # mai un valore supposto: una scala sbagliata scriverebbe misure sbagliate in tabella
            a.error("la scala della vista non si legge (tavola riaperta): indicala con --scala (1:2 = 0.5)")
        orig = [float(k) for k in o.origine.split(",")] if o.origine else None
        righe, centro, fori = righe_tabella(v["cerchi"], scala, o.r_max, orig)
        im, l, h = immagine_tabella(righe); metti("tabella_fori", im, o.x, o.y, l, h)
        if o.sigle:
            for (sigla, *_), c in zip(righe, fori):
                im, l, h = immagine_sigla(sigla); metti("sigla_" + sigla, im, round(c[0] + c[2] * 0.8, 3), round(c[1] + c[2] * 0.8, 3), l, h)
        info = {"righe": righe, "origine": centro}
    elif o.cosa == "riferimento":
        im, l, h = immagine_riferimento(o.lettera); metti("riferimento_" + o.lettera, im, o.x, o.y, l, h)
    else:
        if not o.valore:
            a.error("--valore è obbligatorio")
        im, l, h = immagine_riquadro(o.valore, o.rif, o.diametro, o.testo); metti("riquadro", im, o.x, o.y, l, h)
    print(json.dumps({**info, **inserisci(s, voci)}, ensure_ascii=False))

if __name__ == "__main__":
    main()
