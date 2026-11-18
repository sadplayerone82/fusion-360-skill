# Stampi, mesh → solido, divisione in pezzi, scheletro con Derive

**Indice** (file lungo: cerca la sezione, non leggerlo intero)
| Riga | Ricetta | Quando |
|---|---|---|
| 18 | Stampo rigido in due metà: sformo, blocco con cavità, chiavi, colata e sfiati | stampi per silicone o colata |
| 160 | Da mesh (STL) a solido: a faccette, prismatico, ricostruzione da sezioni e cerchi adattati | file STL da modificare |
| 296 | Divisione di un oggetto troppo grande, con fori e perni di allineamento | pezzi più grandi del piatto o della macchina |
| 396 | Modellazione a scheletro con «Derive» su due file | progetti su più file con parametri comuni |

Ricette provate su Fusion (nov. 2026), ognuna con le misure attese calcolate prima e ritrovate nel modello. Ogni blocco è uno script
completo da lanciare con Python sul PC: parla con Fusion attraverso `scripts/mcp_fusion.py` (la riga `sys.path.insert` punta alla
cartella `scripts/` della skill installata in `~/.claude/skills/fusion-360`: cambiala se l'hai messa altrove) e manda a Fusion il
codice delle stringhe in maiuscolo (`CODICE`, `CODICI`…). In un modello vero copia la parte che serve negli script dei passi (`scripts/progetto_locale.py`).
Qui: stampo in due metà, da STL a solido, oggetto più grande del piano diviso con perni, scheletro in un file e pezzo derivato in un
altro (la geometria si propaga, i parametri derivati NO).

## Stampo rigido in due metà

Pezzo 40 × 25 × 16 (z 0–16), sformo 2° simmetrico dalla linea di divisione z = 8 (Alias: > ~1° per staccare il pezzo), raccordi R2.
Stampo = pezzo + 10 mm per lato (Smooth-On: ≥ 1 cm) → blocco 60 × 45 × 36 (z −10…26), cavità = taglio col pezzo conservato,
divisione a z = 8; chiavi di centraggio: 4 semisfere R4 maschio sulla metà inferiore, R4,2 femmina sulla superiore (gioco 0,2);
colata Ø 6 al centro, 2 sfiati Ø 2 alle estremità (dal pezzo alla faccia superiore).
Attesi: fianchi a 2,000° dalla verticale; distanza minima pezzo–esterno 10,000; gioco chiavi 0,200; volume comune fra le metà 0.
Misurato = atteso: fianchi a 2,000° (8 facce), parete minima 10,000 mm su tutte e due le metà, chiavi 4 + 4 con gioco 0,200, volume
comune fra le metà e fra pezzo e stampo 0; 0 errori. Prima di modellare chiedi il materiale dello stampo: **silicone** (flessibile: lo
sformo non serve; almeno 10 mm di silicone attorno) o **rigido** (stampato o fresato: sformo ≥ 1°, linea di divisione dove il pezzo è
più largo, nessun sottosquadro). Trappole di misura: gli angoli dei raccordi sono sfere (filtra per raggio); la faccia di divisione
tocca i bordi del blocco (filtra per direzione).

```python
"""Stampo rigido in due metà via API.
Pezzo 40 × 25 × 16 (z 0–16), sformo 2° simmetrico dalla linea di divisione z = 8 (Alias: > ~1° per staccare il pezzo), raccordi R2.
Stampo = pezzo + 10 mm per lato (Smooth-On: ≥ 1 cm) → blocco 60 × 45 × 36 (z −10…26), cavità = taglio col pezzo conservato,
divisione a z = 8; chiavi di centraggio: 4 semisfere R4 maschio sulla metà inferiore, R4,2 femmina sulla superiore (gioco 0,2);
colata Ø 6 al centro, 2 sfiati Ø 2 alle estremità (dal pezzo alla faccia superiore).
Attesi: fianchi a 2,000° dalla verticale; distanza minima pezzo–esterno 10,000; gioco chiavi 0,200; volume comune fra le metà 0.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name in ("pezzo", "stampo sotto") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VR = adsk.core.ValueInput.createByReal; VI = adsk.core.ValueInput.createByString
OP = adsk.fusion.FeatureOperations
ris = {}
def piano_z(z):
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.xYConstructionPlane, VR(z)); return r.constructionPlanes.add(pi)
def blocco(nome, x0, y0, x1, y1, z0, h):
    sk = r.sketches.add(piano_z(z0)); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(x0, y0, 0), P(x1, y1, 0))
    b = F.extrudeFeatures.addSimple(sk.profiles.item(0), VR(h), OP.NewBodyFeatureOperation).bodies.item(0); b.name = nome; return b
# pezzo, sformo simmetrico dalla linea di divisione, raccordi
pezzo = blocco("pezzo", -2.0, -1.25, 2.0, 1.25, 0.0, 1.6)
pd = piano_z(0.8)
fianchi = [f for f in [pezzo.faces.item(k) for k in range(pezzo.faces.count)] if abs(f.geometry.normal.z) < 1e-6]
di = F.draftFeatures.createInput(fianchi, pd, False); di.setSingleAngle(True, VI("2 deg"))
F.draftFeatures.add(di)
pezzo = r.bRepBodies.itemByName("pezzo")
ang = []
for k in range(pezzo.faces.count):
    f = pezzo.faces.item(k)
    if f.geometry.objectType == adsk.core.Plane.classType() and abs(f.geometry.normal.z) < 0.5:
        ang.append(round(math.degrees(math.asin(abs(f.geometry.normal.z))), 3))
ris["sformo_fianchi_gradi"] = sorted(set(ang)); ris["fianchi_piani"] = len(ang)
ec = adsk.core.ObjectCollection.create()
for k in range(pezzo.edges.count): ec.add(pezzo.edges.item(k))
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(ec, VI("2 mm"), True); F.filletFeatures.add(fi)
pezzo = r.bRepBodies.itemByName("pezzo"); ris["volume_pezzo_mm3"] = round(pezzo.volume * 1000, 2)
# blocco dello stampo (+10 mm per lato) e cavità
st = blocco("stampo", -3.0, -2.25, 3.0, 2.25, -1.0, 3.6)
ci = F.combineFeatures.createInput(st, adsk.core.ObjectCollection.create()); ci.toolBodies.add(pezzo)
ci = F.combineFeatures.createInput(st, ci.toolBodies); ci.operation = OP.CutFeatureOperation; ci.isKeepToolBodies = True
F.combineFeatures.add(ci)
st = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count) if r.bRepBodies.item(k).name != "pezzo"][0]
si = F.splitBodyFeatures.createInput(st, pd, True); F.splitBodyFeatures.add(si)
meta = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count) if r.bRepBodies.item(k).name != "pezzo"]
sotto = min(meta, key=lambda b: b.boundingBox.minPoint.z); sopra = max(meta, key=lambda b: b.boundingBox.minPoint.z)
sotto.name = "stampo sotto"; sopra.name = "stampo sopra"
# chiavi: semisfere (rivoluzione di un semicerchio) ai 4 angoli, centro sulla linea di divisione
def sfera(nome, x, y, rr):
    pp = r.constructionPlanes.createInput(); pp.setByOffset(r.xZConstructionPlane, VR(y)); pl = r.constructionPlanes.add(pp)
    sk = r.sketches.add(pl)
    c = sk.modelToSketchSpace(P(x, y, 0.8)); a = sk.modelToSketchSpace(P(x, y, 0.8 + rr)); b_ = sk.modelToSketchSpace(P(x, y, 0.8 - rr)); m = sk.modelToSketchSpace(P(x + rr, y, 0.8))
    arc = sk.sketchCurves.sketchArcs.addByThreePoints(a, m, b_); ln = sk.sketchCurves.sketchLines.addByTwoPoints(arc.startSketchPoint, arc.endSketchPoint)
    ri = F.revolveFeatures.createInput(sk.profiles.item(0), ln, OP.NewBodyFeatureOperation); ri.setAngleExtent(False, VI("360 deg"))
    b = F.revolveFeatures.add(ri).bodies.item(0); b.name = nome; return b
def combina(target, tool, op):
    tc = adsk.core.ObjectCollection.create(); tc.add(tool)
    ci = F.combineFeatures.createInput(target, tc); ci.operation = op; ci.isKeepToolBodies = False; return F.combineFeatures.add(ci)
centri = [(sx * 2.3, sy * 1.55) for sx in (-1, 1) for sy in (-1, 1)]
for i, (x, y) in enumerate(centri):
    m_ = sfera("chiave M%d" % i, x, y, 0.4)                    # maschio: sfera intera unita alla metà sotto (la metà inferiore è già nel materiale)
    combina(r.bRepBodies.itemByName("stampo sotto"), m_, OP.JoinFeatureOperation)
    f_ = sfera("chiave F%d" % i, x, y, 0.42)                   # femmina: sfera più grande tolta dalla metà sopra
    combina(r.bRepBodies.itemByName("stampo sopra"), f_, OP.CutFeatureOperation)
sotto = r.bRepBodies.itemByName("stampo sotto"); sopra = r.bRepBodies.itemByName("stampo sopra")
# colata e sfiati: dalla sommità del pezzo (z 16) alla faccia superiore dello stampo (z 26)
sk = r.sketches.add(piano_z(1.5))
sk.sketchCurves.sketchCircles.addByCenterRadius(P(0, 0, 0), 0.3)
for x in (-1.6, 1.6): sk.sketchCurves.sketchCircles.addByCenterRadius(P(x, 0, 0), 0.1)
prof = adsk.core.ObjectCollection.create()
for k in range(sk.profiles.count): prof.add(sk.profiles.item(k))
ei = F.extrudeFeatures.createInput(prof, OP.CutFeatureOperation); ei.setDistanceExtent(False, VR(1.2)); ei.participantBodies = [sopra]
F.extrudeFeatures.add(ei)
sotto = r.bRepBodies.itemByName("stampo sotto"); sopra = r.bRepBodies.itemByName("stampo sopra"); pezzo = r.bRepBodies.itemByName("pezzo")
mm = app.measureManager
# misure
def dist_min_esterno(metà):
    # facce ESTERNE = piane che stanno su un bordo dell'ingombro del blocco (−30/+30, −22,5/+22,5, −10/+26 mm), non la cavità
    bb = metà.boundingBox
    def sul_bordo(f):
        fb = f.boundingBox; n = f.geometry.normal      # (la faccia di divisione tocca i bordi ma è orizzontale a z 8: esclusa)
        return (abs(abs(n.x) - 1) < 1e-6 and (abs(fb.minPoint.x + 3.0) < 1e-4 or abs(fb.maxPoint.x - 3.0) < 1e-4)) \
            or (abs(abs(n.y) - 1) < 1e-6 and (abs(fb.minPoint.y + 2.25) < 1e-4 or abs(fb.maxPoint.y - 2.25) < 1e-4)) \
            or (abs(abs(n.z) - 1) < 1e-6 and (abs(fb.minPoint.z + 1.0) < 1e-4 or abs(fb.minPoint.z - 2.6) < 1e-4))
    est = [f for f in [metà.faces.item(k) for k in range(metà.faces.count)] if f.geometry.objectType == adsk.core.Plane.classType() and sul_bordo(f)]
    return round(min(mm.measureMinimumDistance(pezzo, f).value for f in est) * 10, 3)
ris["distanza_minima_pezzo_esterno_mm"] = {"sotto": dist_min_esterno(sotto), "sopra": dist_min_esterno(sopra)}
sfere = lambda b, rr: [f for f in [b.faces.item(k) for k in range(b.faces.count)] if f.geometry.objectType == adsk.core.Sphere.classType()
                       and abs(f.geometry.radius - rr) < 1e-4]        # solo le chiavi (gli angoli dei raccordi R2 sono sfere R2)
sf_m = sfere(sotto, 0.4); sf_f = sfere(sopra, 0.42)
ris["chiavi"] = {"maschi": len(sf_m), "femmine": len(sf_f), "raggi_mm": sorted({round(f.geometry.radius * 10, 3) for f in sf_m + sf_f}),
                 "gioco_min_mm": round(min(mm.measureMinimumDistance(a, b).value for a in sf_m for b in sf_f) * 10, 3)}
T = adsk.fusion.TemporaryBRepManager.get()
a_ = T.copy(sotto); T.booleanOperation(a_, T.copy(sopra), adsk.fusion.BooleanTypes.IntersectionBooleanType)
ris["volume_comune_metà_mm3"] = round(a_.volume * 1000, 4) if a_ else 0
b_ = T.copy(pezzo); T.booleanOperation(b_, T.copy(sotto), adsk.fusion.BooleanTypes.IntersectionBooleanType)
c_ = T.copy(pezzo); T.booleanOperation(c_, T.copy(sopra), adsk.fusion.BooleanTypes.IntersectionBooleanType)
ris["volume_comune_pezzo_stampo_mm3"] = [round(b_.volume * 1000, 4), round(c_.volume * 1000, 4)]
ris["metà_volume_mm3"] = {"sotto": round(sotto.volume * 1000, 1), "sopra": round(sopra.volume * 1000, 1)}
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
ris["corpi"] = [r.bRepBodies.item(k).name for k in range(r.bRepBodies.count)]
sopra.opacity = 0.35
vp = app.activeViewport; cam = vp.camera; cam.isSmoothTransition = False
cam.target = P(0, 0, 0.8); cam.eye = P(8, -10, 8); cam.upVector = adsk.core.Vector3D.create(0, 0, 1); vp.camera = cam; vp.fit()
vp.saveAsImageFile(IMG, 1000, 700)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("stampo.png")   # immagine di controllo, nella cartella da cui lanci
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Da mesh (STL) a solido

STL generato qui con misure note: anello Ø 30 / Ø 10 × 20 mm, lati a N = 128 segmenti (vertici sui cerchi).
Attesi calcolati prima: volume del poligono = (A(15) − A(5)) × 20, con A(R) = (N/2)·R²·sin(2π/N).
Strade provate: (1) conversione «Faceted» → volume = mesh; (2) «Prismatic» (dopo i gruppi di facce), atteso: cilindri riconosciuti R 15 e R 5;
(3) reverse engineering: sezione a z = 10 calcolata dai triangoli (l'API non ha la «sezione di mesh»), cerchi adattati ai punti
(minimi quadrati), estrusione 20 mm → raggi entro R·(1 − cos(π/N)) = 0,0045 mm dal vero.
Misurato: mesh chiusa, 1 024 triangoli, volume 12 561,325 = atteso; «Faceted» → solido di 1 024 facce, stesso volume; «Prismatic» →
**rifiutato con la licenza Personal** («No rights for mesh conversion»; con le altre licenze non provato); ricostruzione → R 14,9977 e
4,9992 (entro lo 0,0045 teorico), cilindri veri. Quindi con la Personal un ricambio da STL si **ricostruisce**: sezioni calcolate dalla
mesh, curve adattate (rette, cerchi; spline per le forme libere), poi estrusioni e rivoluzioni con misure arrotondate dopo il confronto
con la mesh. Trappole: `MeshConvertFeatures.createInput` vuole una lista Python, `MeshGenerateFaceGroupsFeatures.createInput` un
corpo solo; volume 0 se la mesh non è chiusa (`isClosed`). L'API non ha la «sezione di mesh»: la sezione si calcola dai triangoli.

```python
"""Da mesh (STL) a solido, via API.
STL generato qui con misure note: anello Ø 30 / Ø 10 × 20 mm, lati a N = 128 segmenti (vertici sui cerchi).
Attesi calcolati prima: volume del poligono = (A(15) − A(5)) × 20, con A(R) = (N/2)·R²·sin(2π/N).
Strade provate: (1) conversione «Faceted» → volume = mesh; (2) «Prismatic» (dopo i gruppi di facce), atteso: cilindri riconosciuti R 15 e R 5;
(3) reverse engineering: sezione a z = 10 calcolata dai triangoli (l'API non ha la «sezione di mesh»), cerchi adattati ai punti
(minimi quadrati), estrusione 20 mm → raggi entro R·(1 − cos(π/N)) = 0,0045 mm dal vero.
"""
import json, math, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

QUI = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
N, RE, RI, H = 128, 15.0, 5.0, 20.0

def scrivi_stl(p):
    def tri(a, b, c): return f"facet normal 0 0 0\n outer loop\n  vertex {a[0]:.6f} {a[1]:.6f} {a[2]:.6f}\n  vertex {b[0]:.6f} {b[1]:.6f} {b[2]:.6f}\n  vertex {c[0]:.6f} {c[1]:.6f} {c[2]:.6f}\n endloop\nendfacet\n"
    pt = lambda R, k, z: (R * math.cos(2 * math.pi * k / N), R * math.sin(2 * math.pi * k / N), z)
    s = ["solid anello\n"]
    for k in range(N):
        k1 = (k + 1) % N
        oa, ob, ia, ib = pt(RE, k, 0), pt(RE, k1, 0), pt(RI, k, 0), pt(RI, k1, 0)
        oA, oB, iA, iB = pt(RE, k, H), pt(RE, k1, H), pt(RI, k, H), pt(RI, k1, H)
        s += [tri(oa, ob, oB), tri(oa, oB, oA)]            # parete esterna (normale verso fuori)
        s += [tri(ia, iB, ib), tri(ia, iA, iB)]            # parete del foro (normale verso l'asse)
        s += [tri(oA, oB, iB), tri(oA, iB, iA)]            # sopra
        s += [tri(oa, ib, ob), tri(oa, ia, ib)]            # sotto
    s.append("endsolid anello\n")
    open(p, "w", encoding="ascii").write("".join(s))

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and _d.rootComponent.meshBodies.count and _d.rootComponent.meshBodies.item(0).name.startswith("anello"):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VR = adsk.core.ValueInput.createByReal
ris = {}
def importa(nome):
    ml = r.meshBodies.add(STL, adsk.fusion.MeshUnits.MillimeterMeshUnit)
    m = ml.item(0); m.name = nome; return m
def tipi_facce(b):
    t = {}
    for k in range(b.faces.count):
        g = b.faces.item(k).geometry; n = g.objectType.split("::")[-1]
        if n == "Cylinder": n += " R%.3f" % (g.radius * 10)
        t[n] = t.get(n, 0) + 1
    return t
# (1) Faceted
m1 = importa("anello faceted")
ris["mesh"] = {"chiusa": m1.isClosed, "volume_mm3": round(m1.volume * 1000, 3), "triangoli": m1.displayMesh.triangleCount}
try:
    ci = F.meshConvertFeatures.createInput([m1])
    ci.meshConvertMethodType = adsk.fusion.MeshConvertMethodTypes.FacetedMeshConvertMethodType
    f1 = F.meshConvertFeatures.add(ci); b1 = f1.bodies.item(0)
    ris["faceted"] = {"volume_mm3": round(b1.volume * 1000, 3), "facce": b1.faces.count, "solido": b1.isSolid}
except Exception as e: ris["faceted"] = "ERR " + str(e)[:300]
# (2) Prismatic: gruppi di facce, poi conversione
m2 = importa("anello prismatic")
try:
    gi = F.meshGenerateFaceGroupsFeatures.createInput(m2)      # qui un corpo solo (la conversione invece vuole una lista)
    F.meshGenerateFaceGroupsFeatures.add(gi)
    m2 = [r.meshBodies.item(k) for k in range(r.meshBodies.count) if r.meshBodies.item(k).name == "anello prismatic"][0]
    ris["gruppi_di_facce"] = m2.faceGroups.count
    ci = F.meshConvertFeatures.createInput([m2])
    ci.meshConvertMethodType = adsk.fusion.MeshConvertMethodTypes.PrismaticMeshConvertMethodType
    f2 = F.meshConvertFeatures.add(ci); b2 = f2.bodies.item(0)
    ris["prismatic"] = {"volume_mm3": round(b2.volume * 1000, 3), "facce": b2.faces.count, "tipi": tipi_facce(b2)}
except Exception as e: ris["prismatic"] = "ERR " + str(e)[:300]
# (3) sezione a z = 10 dai triangoli della mesh + cerchi adattati
tm = m1.displayMesh; c = tm.nodeCoordinatesAsDouble; idx = tm.nodeIndices
pts = []
zc = 1.0
for t in range(0, len(idx), 3):
    v = [(c[3 * idx[t + j]], c[3 * idx[t + j] + 1], c[3 * idx[t + j] + 2]) for j in range(3)]
    for a, b in ((v[0], v[1]), (v[1], v[2]), (v[2], v[0])):
        if (a[2] - zc) * (b[2] - zc) < 0:
            s = (zc - a[2]) / (b[2] - a[2]); pts.append((a[0] + (b[0] - a[0]) * s, a[1] + (b[1] - a[1]) * s))
def cerchio(ps):           # minimi quadrati (Kasa): x² + y² + D x + E y + F = 0
    import itertools
    sx = sy = sxx = syy = sxy = sz = szx = szy = 0.0; n = len(ps)
    for x, y in ps:
        z = x * x + y * y; sx += x; sy += y; sxx += x * x; syy += y * y; sxy += x * y; sz += z; szx += z * x; szy += z * y
    A = [[sxx, sxy, sx], [sxy, syy, sy], [sx, sy, n]]; B = [-szx, -szy, -sz]
    def det(m): return m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    D0 = det(A); sol = []
    for i in range(3):
        Mi = [row[:] for row in A]
        for k in range(3): Mi[k][i] = B[k]
        sol.append(det(Mi) / D0)
    Dd, Ee, Ff = sol; cx, cy = -Dd / 2, -Ee / 2
    return cx, cy, math.sqrt(cx * cx + cy * cy - Ff)
est = [q for q in pts if math.hypot(*q) > 1.0]; inn = [q for q in pts if math.hypot(*q) <= 1.0]
ce, ci_ = cerchio(est), cerchio(inn)
ris["sezione"] = {"punti": len(pts), "esterno": [round(v * 10, 4) for v in ce], "foro": [round(v * 10, 4) for v in ci_]}
sk = r.sketches.add(r.xYConstructionPlane)
sk.sketchCurves.sketchCircles.addByCenterRadius(P(ce[0], ce[1], 0), ce[2]); sk.sketchCurves.sketchCircles.addByCenterRadius(P(ci_[0], ci_[1], 0), ci_[2])
prof = min([sk.profiles.item(k) for k in range(sk.profiles.count)], key=lambda q: abs(q.areaProperties().area - math.pi * (ce[2] ** 2 - ci_[2] ** 2)))
b3 = F.extrudeFeatures.addSimple(prof, VR(2.0), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0); b3.name = "anello ricostruito"
ris["ricostruito"] = {"volume_mm3": round(b3.volume * 1000, 3), "tipi": tipi_facce(b3)}
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    stl = QUI + "/anello-128.stl"; scrivi_stl(stl)
    A = lambda R: (N / 2) * R * R * math.sin(2 * math.pi / N)
    attesi = {"volume_poligono_mm3": round((A(RE) - A(RI)) * H, 3), "volume_cilindri_veri_mm3": round(math.pi * (RE ** 2 - RI ** 2) * H, 3),
              "tolleranza_raggio_mm": round(RE * (1 - math.cos(math.pi / N)), 4)}
    ok, r, righe = esegui(Sessione(), f"STL = {stl!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps({"attesi": attesi, "misurati": r if r else righe}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
```

## Dividere un oggetto più grande del piano di stampa o della macchina, con perni di allineamento

Oggetto 400 × 120 × 80 (x −200…200), raccordi R10; piano di stampa 256 × 256 × 256 (esempio) con 10 mm di margine →
pezzi = ceil(400 / 246) = 2, taglio a x = 0; perni Ø 8 × 24 a (y ±30, z 40); fori Ø 8,4 (gioco 0,2 sul raggio: perno infilato,
0,15–0,25 secondo un produttore di stampanti, PETG +0–0,05) profondi 12,5 per parte (0,5 di gioco in fondo).
Attesi: pezzi 200 × 120 × 80 (≤ 256); volume pezzi = originale − 4 fori; assi dei fori coincidenti fra i pezzi; gioco radiale 0,200;
perno dentro i fori senza toccare (distanza minima 0,200).
Misurato: 2 pezzi 200 × 120 × 80; volume dei pezzi = originale − 4 fori (3 787 063,91 = atteso); assi dei fori coincidenti fra i pezzi
(y ±30, z 40); distanza perno–foro 0,200 = gioco; 0 errori. Trappola trovata dal bilancio dei volumi: `setSymmetricExtent(d, True)` =
lunghezza **totale** (metà per lato); per la distanza per lato serve `False`. Tagli lontani dalle zone sottili.

```python
"""Dividere un oggetto più grande del piano di stampa, con perni di allineamento.
Oggetto 400 × 120 × 80 (x −200…200), raccordi R10; piano di stampa 256 × 256 × 256 (esempio) con 10 mm di margine →
pezzi = ceil(400 / 246) = 2, taglio a x = 0; perni Ø 8 × 24 a (y ±30, z 40); fori Ø 8,4 (gioco 0,2 sul raggio: perno infilato,
0,15–0,25 secondo un produttore di stampanti, PETG +0–0,05) profondi 12,5 per parte (0,5 di gioco in fondo).
Attesi: pezzi 200 × 120 × 80 (≤ 256); volume pezzi = originale − 4 fori; assi dei fori coincidenti fra i pezzi; gioco radiale 0,200;
perno dentro i fori senza toccare (distanza minima 0,200).
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

CODICE = r'''
import math
try:
    _d = adsk.fusion.Design.cast(app.activeProduct)
    if _d and any(_d.rootComponent.bRepBodies.item(k).name.startswith("pezzo ") for k in range(_d.rootComponent.bRepBodies.count)):
        app.activeDocument.close(False)
except Exception: pass
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
d.fusionUnitsManager.distanceDisplayUnits = adsk.fusion.DistanceUnits.MillimeterDistanceUnits
r = d.rootComponent; F = r.features; P = adsk.core.Point3D.create; VR = adsk.core.ValueInput.createByReal; VI = adsk.core.ValueInput.createByString
OP = adsk.fusion.FeatureOperations
LIM, MARG = 25.6, 1.0
ris = {}
sk = r.sketches.add(r.xYConstructionPlane); sk.sketchCurves.sketchLines.addTwoPointRectangle(P(-20, -6, 0), P(20, 6, 0))
b = F.extrudeFeatures.addSimple(sk.profiles.item(0), VR(8), OP.NewBodyFeatureOperation).bodies.item(0); b.name = "oggetto"
ec = adsk.core.ObjectCollection.create()
for k in range(b.edges.count): ec.add(b.edges.item(k))
fi = F.filletFeatures.createInput(); fi.edgeSetInputs.addConstantRadiusEdgeSet(ec, VI("10 mm"), True); F.filletFeatures.add(fi)
b = r.bRepBodies.itemByName("oggetto"); v0 = b.volume
bb = b.boundingBox; L = bb.maxPoint.x - bb.minPoint.x
n = math.ceil(L / (LIM - MARG)); ris["pezzi_calcolati"] = n
# taglio a x = 0 (piano YZ)
si = F.splitBodyFeatures.createInput(b, r.yZConstructionPlane, True); F.splitBodyFeatures.add(si)
pz = [r.bRepBodies.item(k) for k in range(r.bRepBodies.count)]
pz.sort(key=lambda q: q.boundingBox.minPoint.x)
for i, q in enumerate(pz): q.name = "pezzo %d" % (i + 1)
# fori Ø 8,4 profondi 12,5 per parte (estrusione simmetrica 25 dal piano di taglio) e perni Ø 8 × 24
sk2 = r.sketches.add(r.yZConstructionPlane)
for y in (-3.0, 3.0): sk2.sketchCurves.sketchCircles.addByCenterRadius(sk2.modelToSketchSpace(P(0, y, 4.0)), 0.42)
pr = adsk.core.ObjectCollection.create()
for k in range(sk2.profiles.count): pr.add(sk2.profiles.item(k))
ei = F.extrudeFeatures.createInput(pr, OP.CutFeatureOperation); ei.setSymmetricExtent(VR(1.25), False)      # False = distanza PER LATO (True = lunghezza totale)
ei.participantBodies = pz
F.extrudeFeatures.add(ei)
sk3 = r.sketches.add(r.yZConstructionPlane)
for y in (-3.0, 3.0): sk3.sketchCurves.sketchCircles.addByCenterRadius(sk3.modelToSketchSpace(P(0, y, 4.0)), 0.40)
pr = adsk.core.ObjectCollection.create()
for k in range(sk3.profiles.count): pr.add(sk3.profiles.item(k))
ei = F.extrudeFeatures.createInput(pr, OP.NewBodyFeatureOperation); ei.setSymmetricExtent(VR(1.2), False)
perni = F.extrudeFeatures.add(ei).bodies
for k in range(perni.count): perni.item(k).name = "perno %d" % (k + 1)
pz = [r.bRepBodies.itemByName("pezzo 1"), r.bRepBodies.itemByName("pezzo 2")]
# misure
ris["pezzi"] = {}
for q in pz:
    qb = q.boundingBox
    dim = [round((qb.maxPoint.x - qb.minPoint.x) * 10, 2), round((qb.maxPoint.y - qb.minPoint.y) * 10, 2), round((qb.maxPoint.z - qb.minPoint.z) * 10, 2)]
    ris["pezzi"][q.name] = {"ingombro_mm": dim, "sta_nel_piano": all(x <= LIM * 10 for x in dim), "volume_mm3": round(q.volume * 1000, 2)}
fori = math.pi * 0.42 ** 2 * 1.25 * 4
ris["volumi"] = {"originale_mm3": round(v0 * 1000, 2), "pezzi_mm3": round(sum(q.volume for q in pz) * 1000, 2), "atteso_mm3": round((v0 - fori) * 1000, 2)}
assi = {}
for q in pz:
    for k in range(q.faces.count):
        g = q.faces.item(k).geometry
        if g.objectType == adsk.core.Cylinder.classType() and abs(g.radius - 0.42) < 1e-6:
            assi.setdefault(q.name, []).append([round(g.origin.y * 10, 3), round(g.origin.z * 10, 3), round(g.axis.x, 3)])
ris["assi_dei_fori"] = assi
mm = app.measureManager
ris["distanza_minima_perni_pezzi_mm"] = [round(mm.measureMinimumDistance(r.bRepBodies.itemByName("perno %d" % (k + 1)), q).value * 10, 3) for k in range(2) for q in pz]
t = d.timeline
ris["errori"] = [t.item(k).name for k in range(t.count) if not t.item(k).isGroup and t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState]
pz[1].opacity = 0.3
vp = app.activeViewport; vp.fit(); vp.saveAsImageFile(IMG, 1000, 600)
out(**ris)
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    img = os.path.abspath("divisione.png")   # immagine di controllo, nella cartella da cui lanci
    ok, r, righe = esegui(Sessione(), f"IMG = {img!r}\n" + CODICE, sola_lettura=False)
    print(json.dumps(r, ensure_ascii=False, indent=1) if r else righe)

if __name__ == "__main__":
    main()
```

## Modellazione a scheletro con «Derive» (Inserisci derivata) su due file

Fonti: guida Fusion «Derive design features from one design into another» (letta: corpi, schizzi, parametri «preferiti» e dei
componenti; la derivata compare nella timeline, i parametri derivati nella finestra Parametri); manuale API installato
(DeriveFeatures.createInput(sourceDesign), DeriveFeatureInput.sourceEntities / isIncludeFavoriteParameters,
DeriveFeature.documentReference.isOutOfDate / getLatestVersion()).
Sorgente = un progetto già salvato nel cloud (gli si aggiunge un parametro preferito
`scheletro_L` e lo schizzo «scheletro» L × 40), destinazione = progetto NUOVO NON SALVATO (non occupa un posto nel cloud).
Passi: sorgente (L = 80, salva, versione +1 verificata) → derivato (estrusione 5 mm dello schizzo derivato: atteso 80 × 40 × 5 = 16 000 mm³)
→ sorgente L = 100 (salva, +1) → aggiorna la derivata (atteso 20 000 mm³, parametro derivato 100).
Si lancia a passi, con gli argomenti `sorgente 80`, `derivato`, `sorgente 100`, `aggiorna`; i nomi del cloud si scrivono in cima a
`TROVA`. Misurato: la derivata funziona anche in un progetto non salvato (schizzo e parametro `scheletro_L_Ref` = 80, estrusione
16 000 mm³ = atteso); dopo L = 100 nella sorgente il pezzo resta 16 000 finché non si chiama `design.computeAll()`, poi 20 000: la
**geometria** si propaga. Il **parametro derivato resta 80**, e togliere e rimettere `isIncludeFavoriteParameters` crea un doppione
(`scheletro_L_Ref1`) senza avvisi. Regola: con lo scheletro si guida la geometria, non i parametri derivati; dopo ogni modifica della
sorgente la si salva (versione +1 verificata), nel derivato `getLatestVersion()` + `computeAll()`, poi si confrontano misure e
parametri con la sorgente. Ogni file derivato salvato occupa un documento nel cloud (con la licenza Personal sono 10).

```python
"""Modellazione a scheletro con «Derive» (Inserisci derivata) su due file.
Fonti: guida Fusion «Derive design features from one design into another» (letta: corpi, schizzi, parametri «preferiti» e dei
componenti; la derivata compare nella timeline, i parametri derivati nella finestra Parametri); manuale API installato
(DeriveFeatures.createInput(sourceDesign), DeriveFeatureInput.sourceEntities / isIncludeFavoriteParameters,
DeriveFeature.documentReference.isOutOfDate / getLatestVersion()).
Sorgente = un progetto già salvato nel cloud (gli si aggiunge un parametro preferito
`scheletro_L` e lo schizzo «scheletro» L × 40), destinazione = progetto NUOVO NON SALVATO (non occupa un posto nel cloud).
Passi: sorgente (L = 80, salva, versione +1 verificata) → derivato (estrusione 5 mm dello schizzo derivato: atteso 80 × 40 × 5 = 16 000 mm³)
→ sorgente L = 100 (salva, +1) → aggiorna la derivata (atteso 20 000 mm³, parametro derivato 100).
"""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

TROVA = r'''
PROGETTO_CLOUD, CARTELLA_CLOUD, SORGENTE = "<progetto del cloud>", "<cartella del cloud>", "<progetto sorgente>"   # sostituisci con i nomi del tuo cloud
prog = [app.data.dataProjects.item(k) for k in range(app.data.dataProjects.count) if app.data.dataProjects.item(k).name == PROGETTO_CLOUD][0]
cart = [prog.rootFolder.dataFolders.item(i) for i in range(prog.rootFolder.dataFolders.count) if prog.rootFolder.dataFolders.item(i).name == CARTELLA_CLOUD][0]
DF = [cart.dataFiles.item(i) for i in range(cart.dataFiles.count) if cart.dataFiles.item(i).name == SORGENTE and cart.dataFiles.item(i).fileExtension == "f3d"][0]
def primo_livello(doc):
    try: doc.documentReferences; return True
    except Exception: return False
def sorgente_aperta():
    for i in range(app.documents.count):
        d_ = app.documents.item(i)
        if d_.name.startswith(SORGENTE + " v") and primo_livello(d_): return d_
    return app.documents.open(DF, True)
'''
CODICI = {
"sorgente": r'''
doc = sorgente_aperta(); doc.activate()
d = adsk.fusion.Design.cast(doc.products.itemByProductType("DesignProductType")); r = d.rootComponent; P = adsk.core.Point3D.create
p = d.userParameters.itemByName("scheletro_L")
if p is None:
    p = d.userParameters.add("scheletro_L", adsk.core.ValueInput.createByString("%g mm" % L), "mm", "scheletro: lunghezza")
    p.isFavorite = True
    sk = r.sketches.add(r.xYConstructionPlane); sk.name = "scheletro"
    ln = sk.sketchCurves.sketchLines.addTwoPointRectangle(P(-20, -2, 0), P(-12, 2, 0))       # provvisorio, poi quotato
    dims = sk.sketchDimensions
    dims.addDistanceDimension(ln.item(0).startSketchPoint, ln.item(0).endSketchPoint, adsk.fusion.DimensionOrientations.HorizontalDimensionOrientation, P(-16, -3, 0)).parameter.expression = "scheletro_L"
    dims.addDistanceDimension(ln.item(1).startSketchPoint, ln.item(1).endSketchPoint, adsk.fusion.DimensionOrientations.VerticalDimensionOrientation, P(-10, 0, 0)).parameter.expression = "40 mm"
else:
    p.expression = "%g mm" % L
v0 = doc.dataFile.latestVersionNumber
ok = doc.save("scheletro_L = %g mm" % L)
out(doc=doc.name, primo_livello=primo_livello(doc), parametro=p.expression, preferito=p.isFavorite, versione_prima=v0, salva=ok)''',
"derivato": r'''
src = sorgente_aperta()
sd = adsk.fusion.Design.cast(src.products.itemByProductType("DesignProductType"))
app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
d = adsk.fusion.Design.cast(app.activeProduct); d.designType = adsk.fusion.DesignTypes.ParametricDesignType
r = d.rootComponent
di = r.features.deriveFeatures.createInput(sd)
di.sourceEntities = [sd.rootComponent.sketches.itemByName("scheletro")]
di.isIncludeFavoriteParameters = True
df = r.features.deriveFeatures.add(di)
sk = [r.sketches.item(k) for k in range(r.sketches.count)][-1]
pr = max([sk.profiles.item(k) for k in range(sk.profiles.count)], key=lambda q: q.areaProperties().area)
b = r.features.extrudeFeatures.addSimple(pr, adsk.core.ValueInput.createByString("5 mm"), adsk.fusion.FeatureOperations.NewBodyFeatureOperation).bodies.item(0)
b.name = "pezzo derivato"
ref = df.documentReference
out(volume_mm3=round(b.volume * 1000, 3), parametri=[(d.allParameters.item(k).name, d.allParameters.item(k).expression) for k in range(d.allParameters.count) if "scheletro" in d.allParameters.item(k).name],
    versione_rif=ref.version, superata=ref.isOutOfDate, salvato=app.activeDocument.isSaved)''',
"aggiorna": r'''
def con_derivata(doc_):                 # i disegni non hanno il prodotto «Design»: itemByProductType dà errore (04/11)
    if doc_.objectType != adsk.fusion.FusionDocument.classType(): return False
    d_ = adsk.fusion.Design.cast(doc_.products.itemByProductType("DesignProductType"))
    return bool(d_ and d_.rootComponent.features.deriveFeatures.count)
doc = [app.documents.item(i) for i in range(app.documents.count) if app.documents.item(i).isVisible and con_derivata(app.documents.item(i))][-1]
doc.activate(); d = adsk.fusion.Design.cast(app.activeProduct); r = d.rootComponent
df = r.features.deriveFeatures.item(0); ref = df.documentReference
prima = {"versione_rif": ref.version, "superata": ref.isOutOfDate}
ok = ref.getLatestVersion()
b = r.bRepBodies.itemByName("pezzo derivato")
t = d.timeline
out(prima=prima, aggiornata=ok, versione_rif=ref.version, superata=ref.isOutOfDate, volume_mm3=round(b.volume * 1000, 3),
    parametri=[(d.allParameters.item(k).name, d.allParameters.item(k).expression) for k in range(d.allParameters.count) if "scheletro" in d.allParameters.item(k).name],
    errori=[t.item(k).name for k in range(t.count) if t.item(k).healthState != adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState])''',
}

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    passo = sys.argv[1]; L = float(sys.argv[2]) if len(sys.argv) > 2 else 80
    s = Sessione()
    ok, r, righe = esegui(s, f"L = {L!r}\n" + TROVA + CODICI[passo], sola_lettura=False)
    print(json.dumps(r if r else righe, ensure_ascii=False, indent=1))
    if passo == "sorgente" and r:                      # regola del salvataggio: la versione nel cloud deve salire di 1
        for _ in range(12):
            time.sleep(6)
            ok, r2, _ = esegui(s, TROVA + "out(versione=DF.latestVersionNumber)", sola_lettura=True)
            if r2 and r2["versione"] > r["versione_prima"]: print("SALVATAGGIO VERIFICATO", r2); break
        else: print("!!! la versione nel cloud non è salita:", r2)

if __name__ == "__main__":
    main()
```

