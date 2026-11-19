"""Poor-form signs for recognizable objects (references/forma-e-dettaglio.md §4), read only.
For each visible solid body: number of faces, share of planar area and of free-form surface (NURBS), sharp edges (angle between the
normals of the two faces at mid-edge > 1°) and tangent edges. For each component: how many features and of which type (extrudes, revolves,
lofts, sweeps, forms, fillets, chamfers). Then the WARNINGS:
  S1 sharp edges above 50 % of the total · S2 component with bodies and without any form feature or fillet (extrudes only)
  S3 body with fewer than 12 faces AND planar area at least 50 % (a smooth body with few faces is not poor).
They are warnings, not grades: a boxy mechanical part is right as it is; explain them in the report or fix them. Thresholds tuned on three
models (11/11/2026): the drone failed by the user (warnings), an arm and a shell made with lofts and fillets (no warning). Usage: python -X utf8 segni_forma.py [--file model.f3d] [--soglia-vivi 50] [--facce-min 12]
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
    """Measures on the active document of session `s` and computes the warnings."""
    ok, ris, righe = esegui(s, CODICE, sola_lettura=True)
    if not ris:
        raise RuntimeError("form signs not measured: " + str(righe)[-400:])
    v = sum(c["spigoli_vivi"] for c in ris["corpi"].values()); t = sum(c["spigoli_tangenti"] for c in ris["corpi"].values())
    pct = round(100 * v / (v + t), 1) if v + t else None
    avvisi = []
    if pct is not None and pct > soglia_vivi:
        avvisi.append({"segno": "S1", "testo": f"sharp edges {pct} % (threshold {soglia_vivi} %)"})
    for nome, f in ris["feature"].items():
        if f["corpi"] and f["rivoluzioni"] + f["loft"] + f["sweep"] + f["forme"] + f["raccordi"] + f["smussi"] == 0:
            avvisi.append({"segno": "S2", "testo": f"component «{nome}»: extrudes only ({f['estrusioni']}), no form feature and no fillet"})
    for nome, c in ris["corpi"].items():
        # few faces are a defect only if the body is made of planes: a smooth shell from a loft has 10 faces and is a real
        # form (tested 11/11), a cylindrical motor has 3 and is right as it is; an extruded bar has 7, almost all planar
        if c["facce"] < facce_min and (c["area_piana_pct"] or 0) >= 50:
            avvisi.append({"segno": "S3", "testo": f"body «{nome}»: {c['facce']} faces (minimum {facce_min}), {c['area_piana_pct']} % planar"})
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
    main()
