"""Segni di «forma povera» per gli oggetti da riconoscere (references/forma-e-dettaglio.md §4), sola lettura.
Per ogni corpo solido visibile: numero di facce, quota di area piana e di superficie libera (NURBS), spigoli vivi (angolo fra le
normali delle due facce a metà spigolo > 1°) e tangenti. Per ogni componente: quante feature e di che tipo (estrusioni, rivoluzioni,
loft, sweep, forme, raccordi, smussi). Poi gli AVVISI:
  S1 spigoli vivi sopra il 50 % del totale · S2 componente con corpi e senza nessuna feature di forma né raccordi (solo estrusioni)
  S3 corpo con meno di 12 facce E area piana almeno il 50 % (un corpo liscio con poche facce non è povero).
Sono avvisi, non voti: un pezzo meccanico squadrato è giusto così; si spiegano nel resoconto o si corregge. Soglie tarate su tre
modelli (11/11/2026): il drone bocciato dall'utente (avvisi), un braccio e un guscio fatti con loft e raccordi (nessun avviso). Uso: python -X utf8 segni_forma.py [--file modello.f3d] [--soglia-vivi 50] [--facce-min 12]
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mcp_fusion import Sessione, esegui, chiudi_documento

CODICE = r'''
import math
TIPI = {0: "piana", 1: "cilindrica", 2: "conica", 3: "sferica", 4: "torica", 5: "ellittica_cil", 6: "ellittica_con", 7: "nurbs"}
dz = adsk.fusion.Design.cast(app.activeProduct); r0 = dz.rootComponent
corpi = {}
for o, b in [(None, b) for b in r0.bRepBodies] + [(o, b) for o in r0.allOccurrences for b in o.bRepBodies]:
    if not (b.isSolid and b.isVisible):
        continue
    nome = (o.fullPathName + "/" if o else "") + b.name
    tipi_n = {}; tipi_a = {}; area = 0.0
    for f in b.faces:
        t = TIPI.get(f.geometry.surfaceType, str(f.geometry.surfaceType))
        tipi_n[t] = tipi_n.get(t, 0) + 1; tipi_a[t] = tipi_a.get(t, 0.0) + f.area; area += f.area
    vivi = tang = 0
    for e in b.edges:
        if e.faces.count != 2:
            continue
        ev = e.evaluator
        _, a, z = ev.getParameterExtents()
        _, p = ev.getPointAtParameter((a + z) / 2)
        nn = [f.evaluator.getNormalAtPoint(p)[1] for f in e.faces]
        if math.degrees(nn[0].angleTo(nn[1])) > 1.0: vivi += 1
        else: tang += 1
    corpi[nome] = {"componente": (o.component.name if o else r0.name), "facce": b.faces.count, "tipi_numero": tipi_n,
                   "area_piana_pct": round(100 * tipi_a.get("piana", 0.0) / area, 1) if area else None,
                   "area_nurbs_pct": round(100 * tipi_a.get("nurbs", 0.0) / area, 1) if area else None,
                   "spigoli_vivi": vivi, "spigoli_tangenti": tang}
feat = {}
for c in dz.allComponents:
    fe = c.features
    feat[c.name] = {"feature": fe.count, "estrusioni": fe.extrudeFeatures.count, "rivoluzioni": fe.revolveFeatures.count,
                    "loft": fe.loftFeatures.count, "sweep": fe.sweepFeatures.count, "forme": fe.formFeatures.count,
                    "raccordi": fe.filletFeatures.count, "smussi": fe.chamferFeatures.count, "corpi": c.bRepBodies.count}
out(corpi=corpi, feature=feat)
'''

def segni(s, soglia_vivi=50.0, facce_min=12):
    """Misura sul documento attivo della sessione `s` e calcola gli avvisi."""
    ok, ris, righe = esegui(s, CODICE, sola_lettura=True)
    if not ris:
        raise RuntimeError("segni di forma non misurati: " + str(righe)[-400:])
    v = sum(c["spigoli_vivi"] for c in ris["corpi"].values()); t = sum(c["spigoli_tangenti"] for c in ris["corpi"].values())
    pct = round(100 * v / (v + t), 1) if v + t else None
    avvisi = []
    if pct is not None and pct > soglia_vivi:
        avvisi.append({"segno": "S1", "testo": f"spigoli vivi {pct} % (soglia {soglia_vivi} %)"})
    for nome, f in ris["feature"].items():
        if f["corpi"] and f["rivoluzioni"] + f["loft"] + f["sweep"] + f["forme"] + f["raccordi"] + f["smussi"] == 0:
            avvisi.append({"segno": "S2", "testo": f"componente «{nome}»: solo estrusioni ({f['estrusioni']}), nessuna forma né raccordo"})
    for nome, c in ris["corpi"].items():
        # poche facce sono un difetto solo se il corpo è fatto di piani: un guscio liscio da loft ha 10 facce ed è una forma
        # vera (provato 11/11), un motore cilindrico ne ha 3 ed è giusto così; una barra estrusa ne ha 7, quasi tutte piane
        if c["facce"] < facce_min and (c["area_piana_pct"] or 0) >= 50:
            avvisi.append({"segno": "S3", "testo": f"corpo «{nome}»: {c['facce']} facce (minimo {facce_min}), piane per il {c['area_piana_pct']} %"})
    ris["totale"] = {"corpi": len(ris["corpi"]), "facce": sum(c["facce"] for c in ris["corpi"].values()),
                     "spigoli_vivi": v, "spigoli_tangenti": t, "vivi_pct": pct}
    ris["avvisi"] = avvisi
    return ris

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    sv = float(a[a.index("--soglia-vivi") + 1]) if "--soglia-vivi" in a else 50.0
    fm = int(a[a.index("--facce-min") + 1]) if "--facce-min" in a else 12
    s = Sessione(timeout=600)
    aperto = False
    if "--file" in a:
        f = a[a.index("--file") + 1].replace("\\", "/")
        ok, _, righe = esegui(s, f"im = app.importManager\nim.importToNewDocument(im.createFusionArchiveImportOptions({f!r}))\nout(ok=1)")
        if not ok:
            print(righe); sys.exit(1)
        aperto = True
    try:
        ris = segni(s, sv, fm)
    finally:
        if aperto:
            chiudi_documento(s)
    print(json.dumps({"totale": ris["totale"], "avvisi": ris["avvisi"], "feature": ris["feature"], "corpi": ris["corpi"]}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    if sys.argv[1:2] in (["-h"], ["--help"]):  # aiuto senza Fusion
        sys.stdout.reconfigure(encoding="utf-8"); print(__doc__); sys.exit(0)
    main()
