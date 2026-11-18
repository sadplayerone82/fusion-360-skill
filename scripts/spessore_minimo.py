"""Controllo dello SPESSORE MINIMO di ogni pezzo (regola dell'utente del 02/11/2026: «devi stare attento a queste cose, servirebbe
una regola» — un dentino della culla attaccato con un collo di 2,2 mm era passato in consegna).

Per ogni corpo del documento attivo: distanza minima fra coppie di facce dello stesso corpo che NON si toccano (non hanno spigoli o
vertici in comune). È lo spessore più sottile del materiale (colli, pareti, sporgenze). Confronto con il limite scelto.
Limite dichiarato: la punta arrotondata di uno spigolo acuto (due facce separate da un raccordo) non viene misurata: guardarla
nell'immagine. Due facce che si toccano in un vertice non vengono misurate fra loro. Esiti: OK, FERMARE LA CONSEGNA, NON MISURATO (un pezzo
senza coppie di facce misurabili, es. un toro: si misura in altro modo, non è un via libera). Tondi pieni (perno, tondino, sfera):
lo spessore è il diametro (dal 09/11; prima un perno Ø 5 × 40 risultava 40).
Corpi con più di 200 facce (--max-facce): non misurati e dichiarati, si controllano per calcolo o a pezzi.
Assiemi (dall'11/11): un corpo per chiamata, i corpi ripetuti in più occorrenze una volta sola (chiave = nome, oppure occorrenza/nome
se il nome è ripetuto; `occorrenze` = quante volte è usato; `secondi_per_pezzo`); i pezzi in occorrenze spostate ora sono misurati
(prima: «NON MISURATO» o il diametro al posto dell'altezza). Le coppie di facce lontane non si provano (509 s -> 1,5 s su 8 corpi).
Sola lettura. Uso: python -X utf8 spessore_minimo.py [--limite 5] [--max-facce 200] [--file modello.f3d]
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui, chiudi_documento

CODICE = r'''
# SOLO = indice del corpo da misurare (None = tutti in questa chiamata); ELENCA = True per avere solo l'elenco dei corpi.
# Chi usa CODICE alla vecchia maniera (solo LIMITE e MAX_FACCE davanti) misura tutto in una chiamata, come prima.
try: SOLO
except NameError: SOLO = None
try: ELENCA
except NameError: ELENCA = False
mm = app.measureManager
dz = adsk.fusion.Design.cast(app.activeProduct)
corpi = []                                       # corpi visti dall'assieme (proxy): la misura li vuole così
r0 = dz.rootComponent
for k in range(r0.bRepBodies.count): corpi.append(r0.bRepBodies.item(k))
for i in range(r0.allOccurrences.count):
    occ = r0.allOccurrences.item(i)
    for k in range(occ.bRepBodies.count): corpi.append(occ.bRepBodies.item(k))
def nativo(f, p):
    # Su una faccia vista dall'assieme (proxy) di un'occorrenza SPOSTATA, evaluator.getParameterAtPoint sbaglia: applica lo spostamento
    # al posto del suo inverso (provato 11/11: punto certo sulla faccia, andata e ritorno 122,7 mm = 2 × lo spostamento; con una
    # rotazione di 180° esatti il difetto non si vede). Si passa alla faccia del componente, con il punto riportato nel suo spazio.
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
    # due facce piane parallele: esiste un punto di g che, proiettato sul piano di f, cade dentro f?
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
    # due piani paralleli: Fusion misura i piani infiniti e i suoi due punti possono cadere in un foro o nell'aria (provato 05/11).
    # Conta solo se esiste un punto di g, proiettato su f, con il punto medio dentro il materiale.
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
    # su() riproietta il punto sulla superficie e direbbe sì anche a un punto staccato (così un tratto sulla faccia superiore fra una
    # scanalatura e un raccordo sembrava una parete da 2,89 mm, 05/11): qui il punto deve stare sulla faccia, entro 0,001 mm
    f, p = nativo(f, p)
    ok_, par = f.evaluator.getParameterAtPoint(p)
    if not (ok_ and f.evaluator.isParameterOnFace(par)): return False
    ok_, q = f.evaluator.getPointAtParameter(par)
    return ok_ and q.distanceTo(p) < 1e-4

def tratto_nel_materiale(f, g, a_, b_):
    # il tratto più corto passa nel materiale? Fra due fori Fusion lo dà spesso SUL BORDO del pezzo (punto medio «sulla superficie»):
    # allora lo si sposta di 0,2 mm restando sulle due facce. Sul fondo di uno scasso resta sul fondo o va nell'aria: non conta.
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

# Lo spessore è del pezzo, non di dove sta: lo stesso corpo usato in 4 occorrenze (4 bracci, 38 piedini) si misura UNA volta.
# Prima la chiave era il solo nome: 4 «Braccio» davano un risultato solo, l'ultimo (11/11). Ora nome unico, o occorrenza/nome.
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
    # le coppie crescono col quadrato delle facce: una ruota da 1 300 facce sono quasi un milione di misure. Quel corpo non si misura e lo si dice.
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
    # Le coppie si provano dalla più vicina (distanza fra i riquadri d'ingombro delle due facce: non supera mai la distanza vera)
    # e ci si ferma quando nessuna coppia rimasta può scendere sotto il minimo trovato né sotto il limite. Un pettine da 19 piedini
    # in un corpo solo costava 245 s (11/11): le coppie lontane sono quasi tutte.
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
        for _una in (0,):                               # un giro solo: i «continue» qui sotto passano alla coppia dopo
            if vicine[i] & vicine[j]: continue          # si toccano: la distanza è 0 per costruzione
            m = mm.measureMinimumDistance(facce[i], facce[j])
            v = m.value * 10
            a_, b_ = m.positionOne, m.positionTwo
            piane = all(x.geometry.objectType == adsk.core.Plane.classType() for x in (facce[i], facce[j]))
            parallele = piane and abs(facce[i].geometry.normal.dotProduct(facce[j].geometry.normal)) > 0.9999
            if v > 1e-6 and parallele:
                # con due facce piane parallele Fusion misura i PIANI INFINITI (provato 02/11: 4,5 mm fra due scanalature lontane
                # 50 mm; 05/11: i punti cadono in un foro): conta solo il materiale vero fra le due facce
                if not (materiale_fra_piani(facce[i], facce[j]) or materiale_fra_piani(facce[j], facce[i])): continue
            else:
                # conta solo se il tratto più corto passa DENTRO il materiale (vicino agli angoli rientranti passa nell'aria)
                if v > 1e-6 and not tratto_nel_materiale(facce[i], facce[j], a_, b_): continue
                if v > 1e-6 and not ((su(facce[i], a_) and su(facce[j], b_)) or (su(facce[j], a_) and su(facce[i], b_))):
                    if not piane:
                        if v < LIMITE: da_guardare.append([chiave, round(v, 2), [round(c * 10, 1) for c in m.positionOne.asArray()]])
                        continue
                    if not (sovrapposte(facce[i], facce[j]) or sovrapposte(facce[j], facce[i])): continue
            # uno spessore vero è perpendicolare ad almeno una delle due facce; il salto attraverso un raccordo (corda del
            # raggio, es. 3·√2 = 4,24 per R3) no: lì il materiale è pieno
            if v > 1e-6 and not parallele:
                d = a_.vectorTo(b_); d.normalize()
                allineato = False
                for f, pt in ((facce[i], a_), (facce[j], b_)):
                    ok_n, n = f.evaluator.getNormalAtPoint(pt)
                    if ok_n and abs(n.dotProduct(d)) >= 0.9: allineato = True
                if not allineato: continue
            if minimo is None or v < minimo:
                minimo = v; dove = [round(c * 10, 1) for c in m.positionOne.asArray()]
    # tondi pieni (perno, tondino, sfera): lo spessore è il diametro, e una faccia sola non ha coppie. Si conta un cilindro intero
    # (bordi tutti circolari: non un raccordo) o una sfera intera, se il centro della faccia è nel materiale (non un foro).
    for f in facce:
        g = f.geometry
        # la punta conica di un foro ha uno spigolo degenere SENZA geometria (geometry = None): prima lo script andava in errore
        # e tutto il pezzo risultava «non misurato» (trovato all'esame 09b, 11/11)
        intero = all(f.edges.item(k).geometry is not None and f.edges.item(k).geometry.objectType == adsk.core.Circle3D.classType() for k in range(f.edges.count))
        if g.objectType in (adsk.core.Cylinder.classType(), adsk.core.Sphere.classType()) and intero \
                and b.pointContainment(f.centroid) == DENTRO:
            v = 2 * g.radius * 10
            if minimo is None or v < minimo:
                minimo = v; dove = [round(c * 10, 1) for c in f.centroid.asArray()]
    ris[chiave] = {"spessore_minimo_mm": round(minimo, 2) if minimo is not None else None, "punto_mm": dove,
                   "sotto_limite": minimo is not None and minimo < LIMITE, "occorrenze": len(u["occorrenze"])}
# mai «OK» senza una misura: un pezzo senza coppie di facce misurabili (toro, un solo guscio) o nessun pezzo non è un via libera
non_misurati = [k for k, v in ris.items() if v["spessore_minimo_mm"] is None]
esito = "FERMARE LA CONSEGNA" if any(v["sotto_limite"] for v in ris.values()) else ("NON MISURATO" if non_misurati or not ris else "OK")
out(limite_mm=LIMITE, pezzi=ris, da_guardare=da_guardare, non_misurati=non_misurati, esito=esito)
'''

def misura(s, limite=5.0, max_facce=200):
    """Misura il documento attivo della sessione `s`, UN corpo per chiamata: un assieme con molti pezzi non resta chiuso in una sola
    chiamata lunga (il 10/11 una chiamata unica è andata in timeout a 300 s e ha perso tutto) e un pezzo che fallisce non cancella
    gli altri. I corpi uguali (stesso corpo del componente in più occorrenze) si misurano una volta."""
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
        else:   # timeout o errore su questo corpo: resta scritto, non è un via libera
            pezzi[u["chiave"]] = {"spessore_minimo_mm": None, "punto_mm": None, "sotto_limite": False, "occorrenze": len(u["occorrenze"]),
                                  "motivo": "misura non riuscita: " + str(righe)[-160:]}
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
