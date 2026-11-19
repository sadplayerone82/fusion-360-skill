# Testo su faccia curva, zigrinatura, serie lungo un percorso, anelli

Ricette provate su Fusion (nov. 2026), ognuna con le misure attese calcolate prima e ritrovate nel modello. Ogni blocco è uno script
completo da lanciare con Python sul PC: parla con Fusion attraverso `scripts/mcp_fusion.py` (la riga `sys.path.insert` punta alla
cartella `scripts/` della skill installata in `~/.claude/skills/fusion-360`: cambiala se l'hai messa altrove) e manda a Fusion il
codice delle stringhe in maiuscolo (`CODICE`, `CODICI`…). In un modello vero copia la parte che serve negli script dei passi (`scripts/progetto_locale.py`).

**Indice** (file lungo: cerca la sezione, non leggerlo intero)
| Riga | Ricetta | Quando |
|---|---|---|
| 16 | Testo in rilievo e inciso su una faccia cilindrica | scritte su manopole, anelli, oggetti curvi |
| 108 | Zigrinatura dritta e incrociata (IS 3403 / DIN 82) | manopole, prese |
| 247 | Serie lungo un percorso | copie lungo una curva |
| 336 | Anelli dalla misura ISO 8653 | gioielli |

## Testo in rilievo e inciso su una faccia cilindrica (EmbossFeatures + SketchTexts.createInput3)

Due cilindri Ø 40 × 30 mm (asse Z); testo «SKILL» alto 6 mm su un piano tangente; rilievo +1,0 mm sul primo, incisione −0,8 mm sul secondo.
Attesi: lettere a raggio 21,0 (rilievo) e 19,2 (incisione); altezza delle lettere = altezza del testo nello schizzo; larghezza lungo
la circonferenza (angolo × raggio) = larghezza piatta del testo nello schizzo (avvolgimento senza deformazione).
Misurato: rilievo a 21,000 mm dall'asse, fondo dell'incisione a 19,200; larghezza lungo l'arco = larghezza piatta (22,158: nessuna
deformazione); lettere alte 6,205 (Arial da 6 mm); 0 errori. Trappole: il testo è un'espressione (`"'SKILL'"`, tra apici); su un piano
parallelo a XZ, senza `isVerticalFlip = True` la scritta esce capovolta, e solo l'immagine di fronte lo mostra.

```python
"""Testo in rilievo e inciso su faccia cilindrica, via API (EmbossFeatures + SketchTexts.createInput3).
Due cilindri Ø 40 × 30 mm (asse Z); testo «SKILL» alto 6 mm su un piano tangente; rilievo +1,0 mm sul primo, incisione −0,8 mm sul secondo.
Attesi: lettere a raggio 21,0 (rilievo) e 19,2 (incisione); altezza delle lettere = altezza del testo nello schizzo; larghezza lungo
la circonferenza (angolo × raggio) = larghezza piatta del testo nello schizzo (avvolgimento senza deformazione).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:                                                         # chiude solo un documento di questa prova rimasto aperto
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("cilindro ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VI = adsk.core.ValueInput.createByString
ris = {"casi": {}}
for nome, x0, prof in (("rilievo", 0, "1.0 mm"), ("incisione", 6, "-0.8 mm")):
    sk = r.sketches.add(r.xYConstructionPlane)
    sk.sketchCurves.sketchCircles.addByCenterRadius(P(x0, 0, 0), 2.0)
    cil = F.extrudeFeatures.addSimple(sk.profiles.item(0), VI("30 mm"), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    cil.name = "cilindro " + nome
    # piano tangente al cilindro sul lato −Y (parallelo a XZ, a distanza 20 mm dall'asse)
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xZConstructionPlane, VI("-20 mm")); pt = r.constructionPlanes.add(pi)
    skt = r.sketches.add(pt)
    ti = skt.sketchTexts.createInput3("'SKILL'", VI("6 mm"))       # il testo è un'ESPRESSIONE: va tra apici
    c0 = skt.modelToSketchSpace(P(x0 - 1.2, -2.0, 1.2)); c1 = skt.modelToSketchSpace(P(x0 + 1.2, -2.0, 1.8))
    ti.setAsMultiLine(c0, c1, adsk.core.HorizontalAlignments.CenterHorizontalAlignment, adsk.core.VerticalAlignments.MiddleVerticalAlignment, 0)
    ti.fontName = "Arial"
    ti.isVerticalFlip = True       # piano parallelo a XZ: y dello schizzo = −Z del modello → senza ribaltare il testo esce capovolto
    st = skt.sketchTexts.add(ti)
    xs, zs = [], []
    for cv in st.asCurves():                                 # geometrie del contorno delle lettere (spazio dello schizzo)
        ev = cv.evaluator; ok_, s, t = ev.getParameterExtents(); ok_, punti = ev.getStrokes(s, t, 0.0005)
        for q in punti:
            m = skt.sketchToModelSpace(q); xs.append(m.x); zs.append(m.z)
    piatto = {"larghezza_mm": round((max(xs) - min(xs)) * 10, 3), "altezza_mm": round((max(zs) - min(zs)) * 10, 3)}
    facce_cil = [f for f in [cil.faces.item(k) for k in range(cil.faces.count)] if f.geometry.objectType == adsk.core.Cylinder.classType()]
    ei = F.embossFeatures.createInput([st], facce_cil, VI(prof))     # (profili o testi, facce, profondità: + rilievo, − incisione)
    em = F.embossFeatures.add(ei)
    # misure sulle facce create: distanza dall'asse (x0, 0) in pianta, quote z, angolo
    rs, zz, ang = [], [], []
    for k in range(em.faces.count):
        f = em.faces.item(k)
        ok_, a, b = f.evaluator.parametricRange().minPoint, None, None
        rg = f.evaluator.parametricRange()
        for i in range(7):
            for j in range(7):
                par = adsk.core.Point2D.create(rg.minPoint.x + (rg.maxPoint.x - rg.minPoint.x) * i / 6, rg.minPoint.y + (rg.maxPoint.y - rg.minPoint.y) * j / 6)
                if not f.evaluator.isParameterOnFace(par): continue
                ok_, q = f.evaluator.getPointAtParameter(par)
                rr = math.hypot(q.x - x0, q.y); rs.append(rr); zz.append(q.z); ang.append(math.atan2(q.x - x0, -q.y))
    raggio_lettere = max(rs) if prof.startswith("1") else min(rs)
    ris["casi"][nome] = {"profondita": prof, "testo_piatto": piatto,
                         "raggio_esterno_o_fondo_mm": round(raggio_lettere * 10, 3),
                         "altezza_lettere_mm": round((max(zz) - min(zz)) * 10, 3),
                         "larghezza_su_arco_mm": round((max(ang) - min(ang)) * 20.0 if True else 0, 3),
                         "facce_create": em.faces.count, "stato": str(em.healthState), "volume_cm3": round(cil.volume, 4)}
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
vp = app.activeViewport; cam = vp.camera; cam.isSmoothTransition = False
cam.cameraType = adsk.core.CameraTypes.OrthographicCameraType
cam.target = P(0.3, 0, 1.5); cam.eye = P(0.3, -30, 1.5); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); vp.camera = cam; vp.fit()
vp.saveAsImageFile(IMG, 1000, 500)        # vista DI FRONTE (dal lato del testo): serve a vedere se si legge dritto
ris["documento"] = app.activeDocument.name
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("testo_curvo.png")   # immagine di controllo, nella cartella da cui lanci
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Zigrinatura secondo IS 3403:1981 (da DIN 82): profilo 90°, passi 0,5–1,6 mm, elica 30°

Modello: solco a V di 90° profondo P/2; n = round(π·d/P) solchi; elica con passo L = π·d / tan(30°).
Caso A — RAA (dritta, parallela all'asse), Ø 20 × 15, P 1,0 → n 63, fondi a r = 9,5.
Caso B — RGE (sinistra + destra, punte in rilievo), Ø 20 × 15, P 1,6 → n 39, fondi a r = 9,2; solchi = triangolo nel piano assiale
spazzato lungo un'elica disegnata per punti (l'API non crea elicoidi: CoilFeatures senza add/createInput).
Misurato: RAA 63 solchi, fondi a 9,501 (= atteso), 191 facce; RGE 39 solchi per verso, elica con passo 108,8 mm, fondi a 9,244
(= atteso con la cresta piatta di 0,1 mm), 0 schegge, 0 errori. Trappole: senza la seconda elica come rotaia il profilo ruota lungo lo
sweep (creste mangiate, 39 schegge staccate); la serie circolare vuole un asse di costruzione, non una linea di schizzo; dopo un taglio
che stacca pezzi si riprende il corpo più grande; creste a spessore zero non esistono (né in stampa né al CNC): cresta piatta.

```python
"""Zigrinatura via API secondo IS 3403:1981 (da DIN 82): profilo 90°, passi 0,5–1,6 mm, elica 30°.
Modello: solco a V di 90° profondo P/2; n = round(π·d/P) solchi; elica con passo L = π·d / tan(30°).
Caso A — RAA (dritta, parallela all'asse), Ø 20 × 15, P 1,0 → n 63, fondi a r = 9,5.
Caso B — RGE (sinistra + destra, punte in rilievo), Ø 20 × 15, P 1,6 → n 39, fondi a r = 9,2; solchi = triangolo nel piano assiale
spazzato lungo un'elica disegnata per punti (l'API non crea elicoidi: CoilFeatures senza add/createInput).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math, time
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("manopola ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VI = adsk.core.ValueInput.createByString; VR = adsk.core.ValueInput.createByReal
ris = {"coil_api": [m for m in ("add", "createInput") if hasattr(F.coilFeatures, m)], "casi": {}}
R, H = 1.0, 1.5                                                 # cm: Ø 20, alto 15
def cilindro(nome, x0):
    sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchCircles.addByCenterRadius(P(x0, 0, 0), R)
    b = F.extrudeFeatures.addSimple(sk.profiles.item(0), VR(H), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    b.name = nome; return b
def asse(x0):
    sk = r.sketches.add(r.xZConstructionPlane); l = sk.sketchCurves.sketchLines.addByTwoPoints(P(x0, 0, 0), P(x0, -1, 0))  # XZ: y schizzo = −Z
    l.isConstruction = True
    ai = r.constructionAxes.createInput(); ai.setByTwoPoints(l.startSketchPoint, l.endSketchPoint)   # asse di costruzione vero
    return r.constructionAxes.add(ai)
def serie(feat, ax, n, corpo):
    oc = adsk.core.ObjectCollection.create(); oc.add(feat)
    pi = F.circularPatternFeatures.createInput(oc, ax); pi.quantity = VR(n); pi.totalAngle = VI("360 deg"); pi.isSymmetric = False
    try: return F.circularPatternFeatures.add(pi)
    except Exception as e: ris.setdefault("errori_serie", []).append(str(e)[:150]); return None
def misura(b, x0):
    rs = []
    for k in range(b.faces.count):
        f = b.faces.item(k); rg = f.evaluator.parametricRange()
        for i in range(5):
            for j in range(5):
                par = adsk.core.Point2D.create(rg.minPoint.x + (rg.maxPoint.x - rg.minPoint.x) * i / 4, rg.minPoint.y + (rg.maxPoint.y - rg.minPoint.y) * j / 4)
                if not f.evaluator.isParameterOnFace(par): continue
                ok_, q = f.evaluator.getPointAtParameter(par)
                if 0.05 < q.z < H - 0.05: rs.append(math.hypot(q.x - x0, q.y))
    return round(min(rs) * 10, 3), round(max(rs) * 10, 3), b.faces.count, round(b.volume * 1000, 1)
def errori():
    t = d.timeline
    return [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
# ---- caso A: RAA, P 1,0
p, x0 = 0.10, 0.0
n = round(math.pi * 2 * R / p); pr = math.pi * 2 * R / n
b = cilindro("manopola RAA", x0)
sk = r.sketches.add(r.xYConstructionPlane)                     # solco a V 90°: punta a r = R − P/2, lati a 45° oltre il bordo
L = sk.sketchCurves.sketchLines
a = P(x0, -(R - pr / 2), 0); s = P(x0 - pr * 0.75, -(R + pr / 4), 0); t_ = P(x0 + pr * 0.75, -(R + pr / 4), 0)
L.addByTwoPoints(a, s); L.addByTwoPoints(s, t_); L.addByTwoPoints(t_, a)
prof = min([sk.profiles.item(k) for k in range(sk.profiles.count)], key=lambda q: q.areaProperties().area)
ei = F.extrudeFeatures.createInput(prof, adsk.fusion.FeatureOperations.CutFeatureOperation); ei.setDistanceExtent(False, VR(H)); ei.participantBodies = [b]
taglio = F.extrudeFeatures.add(ei)
t0 = time.time(); serie(taglio, asse(x0), n, b)
ris["casi"]["RAA"] = {"P": 1.0, "n": n, "passo_reale_mm": round(pr * 10, 4), "atteso_fondi_creste_mm": [round((R - pr / 2) * 10, 3), R * 10],
                      "misurato_min_max_facce_volume": misura(b, x0), "serie_s": round(time.time() - t0, 1)}
# ---- caso B: RGE, P 1,6, elica 30° (sinistra e destra)
p, x0 = 0.16, 3.0
n = round(math.pi * 2 * R / p); pr = math.pi * 2 * R / n
Lead = math.pi * 2 * R / math.tan(math.radians(30))          # cm
b = cilindro("manopola RGE", x0)
ax = asse(x0)
for verso in (1, -1):
    # elica per punti sul raggio R (3D), da z −0,1 a H + 0,1 (esce dal pezzo)
    sk = r.sketches.add(r.xYConstructionPlane)
    pts = adsk.core.ObjectCollection.create()
    for k in range(61):          # 3 mm oltre ogni faccia: i capi della spline si scostano dall'elica vera (schegge sul bordo, 03/11)
        z = -0.3 + (H + 0.6) * k / 60; th = verso * 2 * math.pi * z / Lead - math.pi / 2
        pts.add(P(x0 + R * math.cos(th), R * math.sin(th), z))
    elica = sk.sketchCurves.sketchFittedSplines.add(pts)
    guida = adsk.core.ObjectCollection.create()             # seconda elica, stessa forma, raggio R + P: tiene il profilo rivolto all'asse
    for k in range(61):
        z = -0.3 + (H + 0.6) * k / 60; th = verso * 2 * math.pi * z / Lead - math.pi / 2
        guida.add(P(x0 + (R + pr) * math.cos(th), (R + pr) * math.sin(th), z))
    rotaia = sk.sketchCurves.sketchFittedSplines.add(guida)
    # profilo: triangolo nel piano normale all'elica all'inizio (piano per il primo punto, normale = tangente)
    p0 = pts.item(0); p1 = pts.item(1)
    tg = p0.vectorTo(p1); tg.normalize()
    pl = r.constructionPlanes.createInput(); pl.setByDistanceOnPath(elica, VR(0)); piano = r.constructionPlanes.add(pl)
    sp = r.sketches.add(piano)
    rad = adsk.core.Vector3D.create(p0.x - x0, p0.y, 0); rad.normalize()
    lat = tg.crossProduct(rad); lat.normalize()
    def pp(u, v): return sp.modelToSketchSpace(P(p0.x + rad.x * u + lat.x * v, p0.y + rad.y * u + lat.y * v, p0.z + rad.z * u + lat.z * v))
    Ls = sp.sketchCurves.sketchLines
    # cresta piatta di 0,1 mm (03/11): con solchi a V larghi quanto il passo le creste hanno spessore zero e Fusion stacca schegge
    piatto = 0.01; dd = (pr - piatto) / 2
    A_ = pp(-dd, 0); B_ = pp(pr / 4, -(dd + pr / 4)); C_ = pp(pr / 4, dd + pr / 4)
    Ls.addByTwoPoints(A_, B_); Ls.addByTwoPoints(B_, C_); Ls.addByTwoPoints(C_, A_)
    prof = min([sp.profiles.item(k) for k in range(sp.profiles.count)], key=lambda q: q.areaProperties().area)
    path = F.createPath(elica)
    swi = F.sweepFeatures.createInput(prof, path, adsk.fusion.FeatureOperations.CutFeatureOperation); swi.participantBodies = [b]
    swi.guideRail = F.createPath(rotaia); swi.profileScaling = adsk.fusion.SweepProfileScalingOptions.SweepProfileNoScalingOption
    sw = F.sweepFeatures.add(swi)
    t0 = time.time(); serie(sw, ax, n, b)
    lato = "destra" if verso > 0 else "sinistra"
    ris["casi"].setdefault("RGE", {})["serie_%s_s" % lato] = round(time.time() - t0, 1)
    corpi = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count) if r.bRepBodies.item(k).name != "manopola RAA"]
    b = max(corpi, key=lambda c: c.volume); b.name = "manopola RGE"           # il pezzo vero = il corpo più grande
    ris["casi"]["RGE"]["schegge_dopo_" + lato] = sum(1 for c in corpi if c != b)
ris["casi"]["RGE"].update({"P": 1.6, "n": n, "passo_reale_mm": round(pr * 10, 4), "passo_elica_mm": round(Lead * 10, 1),
                           "atteso_fondi_creste_mm": [round((R - (pr - 0.01) / 2) * 10, 3), R * 10], "misurato_min_max_facce_volume": misura(b, x0)})
ris["errori"] = errori()
vp = app.activeViewport; cam = vp.camera; cam.isSmoothTransition = False
cam.target = P(1.5, 0, 0.75); cam.eye = P(1.5, -12, 4); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); vp.camera = cam; vp.fit()
vp.saveAsImageFile(IMG, 1000, 600)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("zigrinatura.png")   # immagine di controllo, nella cartella da cui lanci
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Serie lungo un percorso (PathPatternFeatures)

Percorso: arco R 50 mm, 180° (lunghezza 157,08 mm) nel piano XY, da (50, 0) a (−50, 0) passando per (0, 50).
Caso 1 «Extent»: 7 cilindretti Ø 6 su tutta la lunghezza → centri a raggio 50,000 e angoli 0, 30, …, 180°.
Caso 2 «Spacing»: 5 copie ogni 20 mm lungo l'arco → angoli 0; 22,92; 45,84; 68,75; 91,67°.
Caso 3 orientamento: blocchetto 10 × 4 (lato lungo tangente all'inizio): la copia a 90° deve misurare 10 (X) × 4 (Y) se segue il
percorso, 4 × 10 se identica. Ogni caso in un piano Z diverso (0, 20, 40 mm) per non sovrapporre i corpi.
Misurato: «Extent» → raggio 50,000 e angoli 0/30/…/180; «Spacing» → angoli = attesi (s / R); orientamento identico 4 × 10 ovunque,
lungo il percorso 10 × 4 a 90°; 0 errori. Con «Extent» la distanza è la lunghezza su cui si distribuiscono le copie (per tutto il
percorso: `SketchCurve.length`); la posizione si misura col baricentro dei corpi.

```python
"""Serie lungo un percorso via API (PathPatternFeatures).
Percorso: arco R 50 mm, 180° (lunghezza 157,08 mm) nel piano XY, da (50, 0) a (−50, 0) passando per (0, 50).
Caso 1 «Extent»: 7 cilindretti Ø 6 su tutta la lunghezza → centri a raggio 50,000 e angoli 0, 30, …, 180°.
Caso 2 «Spacing»: 5 copie ogni 20 mm lungo l'arco → angoli 0; 22,92; 45,84; 68,75; 91,67°.
Caso 3 orientamento: blocchetto 10 × 4 (lato lungo tangente all'inizio): la copia a 90° deve misurare 10 (X) × 4 (Y) se segue il
percorso, 4 × 10 se identica. Ogni caso in un piano Z diverso (0, 20, 40 mm) per non sovrapporre i corpi.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("seme ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VR = adsk.core.ValueInput.createByReal; VI = adsk.core.ValueInput.createByString
ris = {"tipi_distanza": [x for x in dir(adsk.fusion.PatternDistanceType) if x.endswith("Type")] if hasattr(adsk.fusion, "PatternDistanceType") else "?", "casi": {}}
R = 5.0
def piano_z(z):
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, VR(z)); return r.constructionPlanes.add(pi)
def arco(z):
    sk = r.sketches.add(piano_z(z)); a = sk.sketchCurves.sketchArcs.addByThreePoints(P(R, 0, 0), P(0, R, 0), P(-R, 0, 0))
    return F.createPath(a), a.length
def seme(nome, z, forma):
    sk = r.sketches.add(piano_z(z))
    if forma == "cilindro": sk.sketchCurves.sketchCircles.addByCenterRadius(P(R, 0, 0), 0.3)
    else: sk.sketchCurves.sketchLines.addTwoPointRectangle(P(R - 0.2, -0.5, 0), P(R + 0.2, 0.5, 0))     # 4 (X) × 10 (Y): lato lungo tangente
    b = F.extrudeFeatures.addSimple(sk.profiles.item(0), VR(0.5), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
    b.name = "seme " + nome; return b
def serie(b, path, n, dist, tipo, lungo):
    oc = adsk.core.ObjectCollection.create(); oc.add(b)
    pi = F.pathPatternFeatures.createInput(oc, path, VR(n), VR(dist), tipo)
    pi.isOrientationAlongPath = lungo
    return F.pathPatternFeatures.add(pi)
def posizioni(feat):
    out_ = []
    for k in range(feat.bodies.count):
        bb = feat.bodies.item(k); c = bb.physicalProperties.centerOfMass; box = bb.boundingBox
        out_.append({"raggio_mm": round(math.hypot(c.x, c.y) * 10, 3), "angolo_gradi": round(math.degrees(math.atan2(c.y, c.x)), 2),
                     "ingombro_xy_mm": [round((box.maxPoint.x - box.minPoint.x) * 10, 2), round((box.maxPoint.y - box.minPoint.y) * 10, 2)]})
    return sorted(out_, key=lambda q: q["angolo_gradi"])
T = adsk.fusion.PatternDistanceType
# caso 1: Extent
path, lung = arco(0.0); ris["lunghezza_arco_mm"] = round(lung * 10, 3)
f1 = serie(seme("extent", 0.0, "cilindro"), path, 7, lung, T.ExtentPatternDistanceType, False)
ris["casi"]["extent"] = [(q["raggio_mm"], q["angolo_gradi"]) for q in posizioni(f1)]
# caso 2: Spacing 20 mm
path, lung = arco(2.0)
f2 = serie(seme("spacing", 2.0, "cilindro"), path, 5, 2.0, T.SpacingPatternDistanceType, False)
ris["casi"]["spacing"] = [(q["raggio_mm"], q["angolo_gradi"]) for q in posizioni(f2)]
# caso 3: orientamento (identico e lungo il percorso), 3 copie a 0, 90, 180°
for nome, z, lungo in (("identico", 4.0, False), ("lungo_percorso", 6.0, True)):
    path, lung = arco(z)
    f = serie(seme(nome, z, "blocco"), path, 3, lung, T.ExtentPatternDistanceType, lungo)
    ris["casi"]["orientamento_" + nome] = [(q["angolo_gradi"], q["ingombro_xy_mm"]) for q in posizioni(f)]
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
vp = app.activeViewport; vp.fit(); vp.saveAsImageFile(IMG, 1000, 700)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("serie_percorso.png")   # immagine di controllo, nella cartella da cui lanci
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Anelli dalla misura ISO 8653

Fonte: ISO 8653:2016 §2.1 (anteprima pubblica su iso.org, letta): «ring-size: circumference of the bigger cylinder that could be
inserted in the ring» → diametro interno utile d = misura / π (misura in mm di circonferenza).
Casi (misura 52 → d = 16,5521 mm): (A) fascia piatta 4 × 2 mm; (B) fascia «comoda» (interno bombato, freccia 0,4 mm): il cilindro
più grande che entra tocca il punto PIÙ STRETTO, quindi il raggio minimo interno = d/2 (non il raggio al bordo).
Misura in Fusion: distanza minima fra l'asse Z e il corpo (= raggio del cilindro più grande che entra), circonferenza = 2π·r.
Argomento facoltativo: la misura (predefinita 52). Misurato: diametro utile 16,5521 per tutti e due gli anelli (= atteso), misura
ricavata 52,000; 0 errori. Gli anelli si fanno sempre dal parametro `misura_ISO`; le misure di altri paesi (italiana, USA, UK) solo con
una tabella di fonte letta.

```python
"""Anelli dalla misura ISO 8653.
Fonte: ISO 8653:2016 §2.1 (anteprima pubblica su iso.org, letta): «ring-size: circumference of the bigger cylinder that could be
inserted in the ring» → diametro interno utile d = misura / π (misura in mm di circonferenza).
Casi (misura 52 → d = 16,5521 mm): (A) fascia piatta 4 × 2 mm; (B) fascia «comoda» (interno bombato, freccia 0,4 mm): il cilindro
più grande che entra tocca il punto PIÙ STRETTO, quindi il raggio minimo interno = d/2 (non il raggio al bordo).
Misura in Fusion: distanza minima fra l'asse Z e il corpo (= raggio del cilindro più grande che entra), circonferenza = 2π·r.
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("anello ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VI = adsk.core.ValueInput.createByString
d.userParameters.add("misura_ISO", VI(str(MISURA)), "", "ISO 8653: circonferenza interna in mm")
d.userParameters.add("d_int", VI("misura_ISO * 1 mm / PI"), "mm", "diametro del cilindro più grande che entra")
ri = d.userParameters.itemByName("d_int").value / 2                       # cm
w, t, e = 0.4, 0.2, 0.04                                                  # larghezza 4, spessore 2, freccia 0,4 (mm → cm)
ris = {"d_int_mm": round(ri * 20, 4), "casi": {}}
def anello(nome, z0, bombato):
    sk = r.sketches.add(r.xZConstructionPlane); L = sk.sketchCurves.sketchLines; S = lambda x, z: sk.modelToSketchSpace(P(x, 0, z))
    ro = ri + t
    if bombato:   # interno: arco dal bordo (ri + e) al centro (ri), esterno dritto
        a = S(ri + e, z0 - w / 2); b = S(ri + e, z0 + w / 2)
        sk.sketchCurves.sketchArcs.addByThreePoints(a, S(ri, z0), b)
        L.addByTwoPoints(b, S(ro, z0 + w / 2)); L.addByTwoPoints(S(ro, z0 + w / 2), S(ro, z0 - w / 2)); L.addByTwoPoints(S(ro, z0 - w / 2), a)
    else:
        L.addTwoPointRectangle(S(ri, z0 - w / 2), S(ro, z0 + w / 2))
    ri_ = F.revolveFeatures.createInput(sk.profiles.item(0), r.zConstructionAxis, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    ri_.setAngleExtent(False, VI("360 deg"))
    b = F.revolveFeatures.add(ri_).bodies.item(0); b.name = nome
    rmin = app.measureManager.measureMinimumDistance(r.zConstructionAxis, b).value
    ris["casi"][nome] = {"raggio_minimo_mm": round(rmin * 10, 4), "diametro_utile_mm": round(rmin * 20, 4),
                         "misura_ISO_ricavata": round(2 * math.pi * rmin * 10, 3), "volume_mm3": round(b.volume * 1000, 2)}
anello("anello piatto", 0.0, False)
anello("anello comodo", 1.0, True)
t_ = d.timeline
ris["errori"] = [t_.item(k).name for k in range(t_.count) if t_.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
vp = app.activeViewport; vp.fit(); vp.saveAsImageFile(IMG, 900, 600)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    misura = float(sys.argv[1]) if len(sys.argv) > 1 else 52
    atteso = {"misura_ISO": misura, "d_int_mm": round(misura / math.pi, 4)}
    img = os.path.abspath("anelli.png")   # immagine di controllo, nella cartella da cui lanci
    ok, r, righe = esegui(Sessione(), f"MISURA = {misura!r}\nIMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps({"atteso": atteso, "misurato": r if r else righe}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
```

