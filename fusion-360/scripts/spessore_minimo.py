"""MINIMUM THICKNESS check of every part (the user's rule of 02/11/2026: «you must be careful about these things, a rule
would help» — a small tooth of the cradle attached by a 2.2 mm neck had reached delivery).

For each body of the active document: minimum distance between pairs of faces of the same body that do NOT touch (they share no edges or
vertices). It is the thinnest section of material (necks, walls, protrusions). Compared with the chosen limit.
Declared limit: the rounded tip of a sharp edge (two faces separated by a fillet) is not measured: look at it
in the image. Two faces touching at a vertex are not measured against each other. Results (esito, kept in Italian): OK,
FERMARE LA CONSEGNA (= stop the delivery), NON MISURATO (= not measured: a part
without measurable pairs of faces, e.g. a torus: measure it another way, it is not a green light). Solid rounds (pin, rod, sphere):
the thickness is the diameter (since 09/11; before, a Ø 5 × 40 pin came out as 40).
Bodies with more than 200 faces (--max-facce): not measured and declared, check them by calculation or in pieces.
Assemblies (since 11/11): one body per call, bodies repeated in several occurrences only once (key = name, or occurrence/name
if the name is repeated; `occorrenze` = how many times it is used; `secondi_per_pezzo`); parts in moved occurrences are now measured
(before: «NON MISURATO» or the diameter instead of the height). Distant pairs of faces are not tried (509 s -> 1.5 s on 8 bodies).
Read only. Usage: python -X utf8 spessore_minimo.py [--limite 5] [--max-facce 200] [--file model.f3d]
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui, chiudi_documento

CODICE = r'''
# SOLO = index of the body to measure (None = all in this call); ELENCA = True to get only the list of bodies.
# Whoever uses CODICE the old way (only LIMITE and MAX_FACCE in front) measures everything in one call, as before.
try: SOLO
except NameError: SOLO = None
try: ELENCA
except NameError: ELENCA = False
mm = app.measureManager
dz = adsk.fusion.Design.cast(app.activeProduct)
corpi = []                                       # bodies seen from the assembly (proxies): the measurement wants them this way
r0 = dz.rootComponent
for k in range(r0.bRepBodies.count): corpi.append(r0.bRepBodies.item(k))
for i in range(r0.allOccurrences.count):
    occ = r0.allOccurrences.item(i)
    for k in range(occ.bRepBodies.count): corpi.append(occ.bRepBodies.item(k))
def nativo(f, p):
    # On a face seen from the assembly (proxy) of a MOVED occurrence, evaluator.getParameterAtPoint is wrong: it applies the move
    # instead of its inverse (tested 11/11: point surely on the face, round trip 122.7 mm = 2 × the move; with a
    # rotation of exactly 180° the defect does not show). We switch to the component face, with the point brought back into its space.
    occ = f.assemblyContext
    if not occ: return f, p
    m = occ.transform2.copy(); m.invert()
    q = p.copy(); q.transformBy(m)
    return f.nativeObject, q

def su(f, p):
    f, p = nativo(f, p)
    ok_, par = f.evaluator.getParameterAtPoint(p)
    return ok_ and f.evaluator.isParameterOnFace(par)

def sovrapposte(f, g):
    # two parallel planar faces: is there a point of g that, projected onto the plane of f, falls inside f?
    pf = f.geometry; n = pf.normal; o = pf.origin
    rg = g.evaluator.parametricRange(); a2, b2 = rg.minPoint, rg.maxPoint
    for u in range(11):
        for w in range(11):
            par = adsk.core.Point2D.create(a2.x + (b2.x - a2.x) * u / 10, a2.y + (b2.y - a2.y) * w / 10)
            if not g.evaluator.isParameterOnFace(par): continue
            ok_, p = g.evaluator.getPointAtParameter(par)
            d = n.x * (p.x - o.x) + n.y * (p.y - o.y) + n.z * (p.z - o.z)
            if su(f, adsk.core.Point3D.create(p.x - n.x * d, p.y - n.y * d, p.z - n.z * d)): return True
    return False

DENTRO = adsk.fusion.PointContainment.PointInsidePointContainment
FUORI = adsk.fusion.PointContainment.PointOutsidePointContainment
def materiale_fra_piani(f, g):
    # two parallel planes: Fusion measures the infinite planes and its two points can fall in a hole or in the air (tested 05/11).
    # It counts only if there is a point of g, projected onto f, with the midpoint inside the material.
    pf = f.geometry; n = pf.normal; o = pf.origin
    rg = g.evaluator.parametricRange(); a2, b2 = rg.minPoint, rg.maxPoint
    for u in range(21):
        for w in range(21):
            par = adsk.core.Point2D.create(a2.x + (b2.x - a2.x) * u / 20, a2.y + (b2.y - a2.y) * w / 20)
            if not g.evaluator.isParameterOnFace(par): continue
            ok_, p = g.evaluator.getPointAtParameter(par)
            d = n.x * (p.x - o.x) + n.y * (p.y - o.y) + n.z * (p.z - o.z)
            if not su(f, adsk.core.Point3D.create(p.x - n.x * d, p.y - n.y * d, p.z - n.z * d)): continue
            med = adsk.core.Point3D.create(p.x - n.x * d / 2, p.y - n.y * d / 2, p.z - n.z * d / 2)
            if b.pointContainment(med) == DENTRO: return True
    return False

def su_davvero(f, p):
    # su() reprojects the point onto the surface and would say yes even to a detached point (this way a segment on the top face between a
    # slot and a fillet looked like a 2.89 mm wall, 05/11): here the point must lie on the face, within 0.001 mm
    f, p = nativo(f, p)
    ok_, par = f.evaluator.getParameterAtPoint(p)
    if not (ok_ and f.evaluator.isParameterOnFace(par)): return False
    ok_, q = f.evaluator.getPointAtParameter(par)
    return ok_ and q.distanceTo(p) < 1e-4

def tratto_nel_materiale(f, g, a_, b_):
    # does the shortest segment pass through the material? Between two holes Fusion often gives it ON THE EDGE of the part (midpoint «on the surface»):
    # then it is shifted by 0.2 mm staying on the two faces. At the bottom of a pocket it stays on the bottom or goes into the air: it does not count.
    med = adsk.core.Point3D.create((a_.x + b_.x) / 2, (a_.y + b_.y) / 2, (a_.z + b_.z) / 2)
    c = b.pointContainment(med)
    if c == DENTRO: return True
    if c == FUORI: return False
    for dx, dy, dz_ in ((.02,0,0), (-.02,0,0), (0,.02,0), (0,-.02,0), (0,0,.02), (0,0,-.02)):
        pa = adsk.core.Point3D.create(a_.x + dx, a_.y + dy, a_.z + dz_)
        pb = adsk.core.Point3D.create(b_.x + dx, b_.y + dy, b_.z + dz_)
        pm = adsk.core.Point3D.create(med.x + dx, med.y + dy, med.z + dz_)
        if b.pointContainment(pm) == DENTRO and su_davvero(f, pa) and su_davvero(g, pb): return True
    return False

# The thickness belongs to the part, not to where it sits: the same body used in 4 occurrences (4 arms, 38 feet) is measured ONCE.
# Before, the key was the name alone: 4 «Braccio» gave a single result, the last one (11/11). Now a unique name, or occurrence/name.
unici = []; visti = {}
for b in corpi:
    if not b.isSolid: continue
    occ = b.assemblyContext
    tok = (b.nativeObject if occ else b).entityToken
    if tok in visti:
        visti[tok]["occorrenze"].append(occ.fullPathName if occ else "radice"); continue
    visti[tok] = {"corpo": b, "occorrenze": [occ.fullPathName if occ else "radice"]}
    unici.append(visti[tok])
nomi = [u["corpo"].name for u in unici]
for u in unici:
    b = u["corpo"]
    u["chiave"] = b.name if nomi.count(b.name) == 1 else (b.assemblyContext.fullPathName + "/" if b.assemblyContext else "") + b.name
if SOLO is None and ELENCA:
    out(elenco=[{"chiave": u["chiave"], "facce": u["corpo"].faces.count, "occorrenze": u["occorrenze"]} for u in unici])
    return
ris = {}
da_guardare = []
for k_u, u in enumerate(unici):
    if SOLO is not None and k_u != SOLO: continue
    b = u["corpo"]; chiave = u["chiave"]
    # pairs grow with the square of the faces: a wheel with 1,300 faces means almost a million measurements. That body is not measured and this is reported.
    if b.faces.count > MAX_FACCE:
        ris[chiave] = {"spessore_minimo_mm": None, "punto_mm": None, "sotto_limite": False, "motivo": "troppe facce: %d" % b.faces.count,
                       "occorrenze": len(u["occorrenze"])}
        continue
    facce = [b.faces.item(i) for i in range(b.faces.count)]
    vicine = []
    for f in facce:
        s = set()
        for j in range(f.vertices.count): s.add(f.vertices.item(j).tempId)
        vicine.append(s)
    minimo, dove = None, None
    # Pairs are tried from the closest (distance between the bounding boxes of the two faces: it never exceeds the true distance)
    # and we stop when no remaining pair can go below the minimum found nor below the limit. A comb with 19 feet
    # in a single body cost 245 s (11/11): distant pairs are almost all of them.
    riq = [f.boundingBox for f in facce]
    def fra_riquadri(p, q):
        s2 = 0.0
        for lo1, hi1, lo2, hi2 in ((p.minPoint.x, p.maxPoint.x, q.minPoint.x, q.maxPoint.x), (p.minPoint.y, p.maxPoint.y, q.minPoint.y, q.maxPoint.y),
                                   (p.minPoint.z, p.maxPoint.z, q.minPoint.z, q.maxPoint.z)):
            g_ = max(lo1 - hi2, lo2 - hi1, 0.0); s2 += g_ * g_
        return s2 ** 0.5 * 10
    coppie = sorted((fra_riquadri(riq[i], riq[j]), i, j) for i in range(len(facce)) for j in range(i + 1, len(facce)) if not (vicine[i] & vicine[j]))
    for lb, i, j in coppie:
        if minimo is not None and lb >= max(minimo, LIMITE): break
        for _una in (0,):                               # a single pass: the «continue» statements below move on to the next pair
            if vicine[i] & vicine[j]: continue          # they touch: the distance is 0 by construction
            m = mm.measureMinimumDistance(facce[i], facce[j])
            v = m.value * 10
            a_, b_ = m.positionOne, m.positionTwo
            piane = all(x.geometry.objectType == adsk.core.Plane.classType() for x in (facce[i], facce[j]))
            parallele = piane and abs(facce[i].geometry.normal.dotProduct(facce[j].geometry.normal)) > 0.9999
            if v > 1e-6 and parallele:
                # with two parallel planar faces Fusion measures the INFINITE PLANES (tested 02/11: 4.5 mm between two slots
                # 50 mm apart; 05/11: the points fall in a hole): only the real material between the two faces counts
                if not (materiale_fra_piani(facce[i], facce[j]) or materiale_fra_piani(facce[j], facce[i])): continue
            else:
                # it counts only if the shortest segment passes INSIDE the material (near re-entrant corners it passes through the air)
                if v > 1e-6 and not tratto_nel_materiale(facce[i], facce[j], a_, b_): continue
                if v > 1e-6 and not ((su(facce[i], a_) and su(facce[j], b_)) or (su(facce[j], a_) and su(facce[i], b_))):
                    if not piane:
                        if v < LIMITE: da_guardare.append([chiave, round(v, 2), [round(c * 10, 1) for c in m.positionOne.asArray()]])
                        continue
                    if not (sovrapposte(facce[i], facce[j]) or sovrapposte(facce[j], facce[i])): continue
            # a real thickness is perpendicular to at least one of the two faces; the jump across a fillet (chord of the
            # radius, e.g. 3·√2 = 4.24 for R3) is not: there the material is solid
            if v > 1e-6 and not parallele:
                d = a_.vectorTo(b_); d.normalize()
                allineato = False
                for f, pt in ((facce[i], a_), (facce[j], b_)):
                    ok_n, n = f.evaluator.getNormalAtPoint(pt)
                    if ok_n and abs(n.dotProduct(d)) >= 0.9: allineato = True
                if not allineato: continue
            if minimo is None or v < minimo:
                minimo = v; dove = [round(c * 10, 1) for c in m.positionOne.asArray()]
    # solid rounds (pin, rod, sphere): the thickness is the diameter, and a single face has no pairs. A whole cylinder counts
    # (all edges circular: not a fillet) or a whole sphere, if the center of the face is in the material (not a hole).
    for f in facce:
        g = f.geometry
        # the conical tip of a hole has a degenerate edge WITHOUT geometry (geometry = None): before, the script raised an error
        # and the whole part came out «not measured» (found at exam 09b, 11/11)
        intero = all(f.edges.item(k).geometry is not None and f.edges.item(k).geometry.objectType == adsk.core.Circle3D.classType() for k in range(f.edges.count))
        if g.objectType in (adsk.core.Cylinder.classType(), adsk.core.Sphere.classType()) and intero \
                and b.pointContainment(f.centroid) == DENTRO:
            v = 2 * g.radius * 10
            if minimo is None or v < minimo:
                minimo = v; dove = [round(c * 10, 1) for c in f.centroid.asArray()]
    ris[chiave] = {"spessore_minimo_mm": round(minimo, 2) if minimo is not None else None, "punto_mm": dove,
                   "sotto_limite": minimo is not None and minimo < LIMITE, "occorrenze": len(u["occorrenze"])}
# never «OK» without a measurement: a part without measurable pairs of faces (torus, a single shell) or no part at all is not a green light
non_misurati = [k for k, v in ris.items() if v["spessore_minimo_mm"] is None]
esito = "FERMARE LA CONSEGNA" if any(v["sotto_limite"] for v in ris.values()) else ("NON MISURATO" if non_misurati or not ris else "OK")
out(limite_mm=LIMITE, pezzi=ris, da_guardare=da_guardare, non_misurati=non_misurati, esito=esito)
'''

def misura(s, limite=5.0, max_facce=200):
    """Measures the active document of session `s`, ONE body per call: an assembly with many parts does not stay locked in a single
    long call (on 10/11 a single call timed out at 300 s and lost everything) and a part that fails does not erase
    the others. Identical bodies (same component body in several occurrences) are measured once."""
    import time
    testa = f"LIMITE = {limite}\nMAX_FACCE = {max_facce}\n"
    ok, el, righe = esegui(s, testa + "SOLO = None\nELENCA = True\n" + CODICE, sola_lettura=True)
    if not el:
        return None, righe
    pezzi, da_guardare, tempi = {}, [], {}
    for k, u in enumerate(el["elenco"]):
        t0 = time.time()
        ok, r1, righe = esegui(s, testa + f"SOLO = {k}\nELENCA = False\n" + CODICE, sola_lettura=True)
        tempi[u["chiave"]] = round(time.time() - t0, 1)
        if r1:
            pezzi.update(r1["pezzi"]); da_guardare += r1["da_guardare"]
        else:   # timeout or error on this body: it stays written down, it is not a green light
            pezzi[u["chiave"]] = {"spessore_minimo_mm": None, "punto_mm": None, "sotto_limite": False, "occorrenze": len(u["occorrenze"]),
                                  "motivo": "measurement failed: " + str(righe)[-160:]}
    non_misurati = [k for k, v in pezzi.items() if v["spessore_minimo_mm"] is None]
    esito = "FERMARE LA CONSEGNA" if any(v["sotto_limite"] for v in pezzi.values()) else ("NON MISURATO" if non_misurati or not pezzi else "OK")
    return {"limite_mm": limite, "pezzi": pezzi, "da_guardare": da_guardare, "non_misurati": non_misurati, "esito": esito,
            "secondi_per_pezzo": tempi}, None

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    limite = float(a[a.index("--limite") + 1]) if "--limite" in a else 5.0
    max_facce = int(a[a.index("--max-facce") + 1]) if "--max-facce" in a else 200
    s = Sessione()
    aperto = False
    if "--file" in a:
        f = a[a.index("--file") + 1].replace("\\", "/")
        ok, _, righe = esegui(s, f"im = app.importManager\nim.importToNewDocument(im.createFusionArchiveImportOptions({f!r}))\nout(ok=1)")
        if not ok:
            print(righe); sys.exit(1)
        aperto = True
    try:
        ris, righe = misura(s, limite, max_facce)
    finally:
        if aperto:
            chiudi_documento(s)
    print(json.dumps(ris, ensure_ascii=False, indent=1) if ris else righe)

if __name__ == "__main__":
    main()
