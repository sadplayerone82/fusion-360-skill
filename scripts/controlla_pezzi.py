"""Controllo di TUTTE le coppie di corpi di un progetto a più pezzi (references/progetti-a-piu-pezzi.md §3–4). Sola lettura, salvo la rotazione
del giunto chiesta (rimessa a 0 alla fine).

Per ogni coppia: URTO (si compenetrano, volume > 0,001 mm³), CONTATTO (si toccano: volume 0), FRANCO SOTTO il limite (distanza minima < --franco,
con i due punti). «Interferenza 0» da sola non basta: dice solo che non si compenetrano.
Gli appoggi voluti (albero nel foro della ruota, cuscinetto nella sede, vite sulla flangia) si dichiarano con --appoggi: coppie di nomi con * e ?.
Esito: OK solo se non ci sono urti e ogni contatto o franco sotto il limite è dichiarato.

Uso: python -X utf8 controlla_pezzi.py [--franco 1] [--appoggi "albero*:ruota*,cuscinetto*:guscio*"] [--giunto NOME --angoli 0,30,90] [--file m.f3d]
I nomi sono «componente/corpo». Con --giunto: si ruota quel giunto e si ricontrolla a ogni angolo, senza computeAll (lo riporterebbe a 0) e rileggendo l'angolo.
"""
import fnmatch, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui

CODICE = r"""
def nome(b):
    # «componente/corpo»: i risultati dell'interferenza restituiscono corpi diversi dagli originali, il nome va ricostruito dal contesto
    # (i corpi dei risultati arrivano senza contesto: allora vale il componente che li contiene)
    ctx = b.assemblyContext
    return (ctx.component.name if ctx else b.parentComponent.name) + "/" + b.name
def corpi():
    v = [r.bRepBodies.item(i) for i in range(r.bRepBodies.count)]
    for o in r.allOccurrences:
        v += [o.bRepBodies.item(k) for k in range(o.bRepBodies.count)]
    return [(nome(b), b) for b in v if b.isSolid and b.isVisible]
tt = corpi()
col = adsk.core.ObjectCollection.create()
for _, b in tt: col.add(b)
def bbd(a_, b_):
    # distanza fra gli ingombri: se supera il franco la coppia non va misurata
    A, B = a_.boundingBox, b_.boundingBox; s_ = 0.0
    for lo1, hi1, lo2, hi2 in ((A.minPoint.x, A.maxPoint.x, B.minPoint.x, B.maxPoint.x), (A.minPoint.y, A.maxPoint.y, B.minPoint.y, B.maxPoint.y), (A.minPoint.z, A.maxPoint.z, B.minPoint.z, B.maxPoint.z)):
        g = max(lo2 - hi1, lo1 - hi2, 0); s_ += g * g
    return math.sqrt(s_) * 10
J_ = {}
if GIUNTO:
    for j in list(r.allJoints) + list(r.allAsBuiltJoints):
        if j.name == GIUNTO and hasattr(j.jointMotion, "rotationValue"): J_ = j
    if not J_: raise RuntimeError("giunto di rotazione non trovato: " + GIUNTO)
ris = {"corpi": len(tt), "coppie": len(tt) * (len(tt) - 1) // 2, "angoli": {}}
mm = app.measureManager
for a_ in ANGOLI:
    if J_:
        J_.jointMotion.rotationValue = math.radians(a_)
        if abs(math.degrees(J_.jointMotion.rotationValue) - a_) > 0.01: raise RuntimeError("angolo non raggiunto: %s" % a_)
    i_ = d.createInterferenceInput(col); i_.areCoincidentFacesIncluded = True
    urti, contatti = [], []
    for x in d.analyzeInterference(i_):
        v = x.interferenceBody.volume * 1000 if x.interferenceBody else 0.0
        bb = x.interferenceBody.boundingBox if x.interferenceBody else None
        dove = [round((bb.minPoint.x + bb.maxPoint.x) * 5, 2), round((bb.minPoint.y + bb.maxPoint.y) * 5, 2), round((bb.minPoint.z + bb.maxPoint.z) * 5, 2)] if bb else None
        cp = sorted([nome(x.entityOne), nome(x.entityTwo)])
        (urti if v > 0.001 else contatti).append(cp + [round(v, 3), dove])
    sotto = []
    tocca = {tuple(c[:2]) for c in contatti} | {tuple(u[:2]) for u in urti}
    for i in range(len(tt)):
        for k in range(i + 1, len(tt)):
            (na, a), (nb, b) = tt[i], tt[k]
            if tuple(sorted([na, nb])) in tocca or bbd(a, b) >= FRANCO: continue
            m = mm.measureMinimumDistance(a, b); dist = m.value * 10
            if dist < FRANCO:
                sotto.append(sorted([na, nb]) + [round(dist, 3), [round(c * 10, 2) for c in m.positionOne.asArray()]])
    ris["angoli"][str(a_)] = {"urti": urti, "contatti": contatti, "franco_sotto": sotto}
if J_: J_.jointMotion.rotationValue = 0
out(**ris)
"""

def dichiarato(a, b, appoggi):
    return any((fnmatch.fnmatch(a, p) and fnmatch.fnmatch(b, q)) or (fnmatch.fnmatch(a, q) and fnmatch.fnmatch(b, p)) for p, q in appoggi)

def controlla(s=None, franco=1.0, appoggi=(), giunto=None, angoli=(0,), file=None):
    s = s or Sessione(timeout=900)
    pre = ""
    if file:
        f = file.replace("\\", "/")
        pre = f"im = app.importManager\nim.importToNewDocument(im.createFusionArchiveImportOptions({f!r}))\n"
        ok, _, rr = esegui(s, pre + "out(ok=1)")
        if not ok: raise RuntimeError(rr)
    ok, ris, rr = esegui(s, f"FRANCO = {float(franco)}\nGIUNTO = {giunto!r}\nANGOLI = {list(angoli)!r}\n" + CODICE, sola_lettura=not giunto)
    if not ok or not ris: raise RuntimeError(rr)
    da_vedere = 0
    for a, x in ris["angoli"].items():
        x["non_dichiarati"] = [c for c in x["contatti"] + x["franco_sotto"] if not dichiarato(c[0], c[1], appoggi)]
        da_vedere += len(x["urti"]) + len(x["non_dichiarati"])
    ris["esito"] = "OK" if da_vedere == 0 else ("URTI" if any(x["urti"] for x in ris["angoli"].values()) else "DA DICHIARARE O CORREGGERE")
    ris["franco_mm"] = franco
    return ris

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    def opz(n, d=None): return a[a.index(n) + 1] if n in a else d
    app_ = [tuple(x.split(":", 1)) for x in (opz("--appoggi", "") or "").split(",") if ":" in x]
    ris = controlla(franco=float(opz("--franco", 1.0)), appoggi=app_, giunto=opz("--giunto"),
                    angoli=[float(x) for x in opz("--angoli", "0").split(",")], file=opz("--file"))
    print(json.dumps(ris, ensure_ascii=False, indent=1))
    sys.exit(0 if ris["esito"] == "OK" else 1)

if __name__ == "__main__":
    main()
