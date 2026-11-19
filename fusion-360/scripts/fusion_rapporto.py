"""Script to run INSIDE Fusion (via fusion_mcp_execute, readOnly: true): prints a JSON report of the state of the active
model, in user units (mm, mm², mm³, g, degrees). Basis of the automatic verification (area H of the study).

Content: design type and units; user parameters (name, expression, value); timeline (unhealthy items with message);
sketches (fully constrained?, profiles); bodies (solid?, visible?, volume, area, bounding box, number of faces/edges, material,
mass, center of mass); components and occurrences. It changes nothing.
"""
import adsk.core, adsk.fusion, json

def mm(p):
    return [round(p.x * 10, 4), round(p.y * 10, 4), round(p.z * 10, 4)]

def run(_context: str):
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    if not d:
        print(json.dumps({"errore": "the active product is not a design (Design)"}))
        return
    um = d.unitsManager
    sani = adsk.fusion.FeatureHealthStates.HealthyFeatureHealthState
    rap = {
        "documento": app.activeDocument.name if app.activeDocument else None,
        "designIntent": {0: "parte", 1: "assieme", 2: "ibrido"}.get(d.designIntent, d.designIntent),
        "parametrico": d.designType == adsk.fusion.DesignTypes.ParametricDesignType,
        "unita": um.defaultLengthUnits,
        "parametri_utente": [{"nome": p.name, "espressione": p.expression, "valore": round(p.value * 10, 6) if p.unit in ("mm", "cm", "m", "in") else p.value,
                              "unita": p.unit} for p in d.userParameters],
        "timeline": {"elementi": d.timeline.count, "non_sani": [], "sospesi": []},
        "schizzi": [], "corpi": [], "componenti": d.allComponents.count,
        "occorrenze": d.rootComponent.allOccurrences.count,
    }
    elementi, coda = [], [(i, d.timeline.item(i)) for i in range(d.timeline.count)]
    while coda:   # a group (e.g. the one created by importing a DXF) has state 5 and hides its items: those are inspected
        i, it = coda.pop(0)   # inside a group .index raises an error: the group index is kept
        if it.isGroup:
            g = adsk.fusion.TimelineGroup.cast(it)
            coda = [(i, g.item(k)) for k in range(g.count)] + coda
        else:
            elementi.append((i, it))
    for i, it in elementi:
        if it.isSuppressed:     # suppressed on purpose (state 3, no message): not an error, listed separately
            rap["timeline"]["sospesi"].append({"indice": i, "nome": it.name})
        elif it.healthState != sani:
            rap["timeline"]["non_sani"].append({"indice": i, "nome": it.name, "stato": it.healthState,
                                                "messaggio": it.errorOrWarningMessage, "soppresso": it.isSuppressed})
    for comp in d.allComponents:
        for sk in comp.sketches:
            vincolato = sk.isFullyConstrained
            nota = None
            # a text (sketchTexts) keeps the sketch «not constrained» forever, even with the box and all points constrained
            # (tested 09/11). So what counts is whether the box exists and curves and points are all constrained; a text without a box stays free.
            if not vincolato and sk.sketchTexts.count and sk.sketchCurves.count \
                    and all(c.isFullyConstrained for c in sk.sketchCurves) and all(p.isFullyConstrained for p in sk.sketchPoints):
                vincolato, nota = True, "text: Fusion always reports it as free; box and points constrained"
            rap["schizzi"].append({"componente": comp.name, "nome": sk.name, "vincolato": vincolato, "nota": nota,
                                   "profili": sk.profiles.count, "visibile": sk.isVisible})
        for b in comp.bRepBodies:
            bb = b.boundingBox
            # b.volume is the fast calculation: on intersecting curved surfaces it is off by a few mm³ (tested 10/11: 6.85 mm³ out of
            # 88,251, 0.008 %, almost the judge's tolerance). The high-accuracy calculation is used.
            pp = b.getPhysicalProperties(adsk.fusion.CalculationAccuracy.VeryHighCalculationAccuracy)
            voce = {"componente": comp.name, "nome": b.name, "solido": b.isSolid, "visibile": b.isVisible,
                    "volume_mm3": round(pp.volume * 1000, 4), "area_mm2": round(b.area * 100, 4),
                    "ingombro_min_mm": mm(bb.minPoint), "ingombro_max_mm": mm(bb.maxPoint),
                    "dimensioni_mm": [round((bb.maxPoint.x - bb.minPoint.x) * 10, 4), round((bb.maxPoint.y - bb.minPoint.y) * 10, 4),
                                      round((bb.maxPoint.z - bb.minPoint.z) * 10, 4)],
                    "facce": b.faces.count, "spigoli": b.edges.count, "shell": b.shells.count,
                    "materiale": b.material.name if b.material else None}
            voce["massa_g"] = round(pp.mass * 1000, 4)
            voce["baricentro_mm"] = mm(pp.centerOfMass)
            rap["corpi"].append(voce)
    # ASSEMBLIES (11/11/2026): «corpi» above gives each body in the coordinates of ITS component (only once even if the
    # component is used 4 times) and does not know whether the occurrence is hidden. For the true assembly bounding box the occurrences
    # are inspected: their bodies are already in the assembly position. Tested on the drone of exam 10: from the components 154 mm, true 148.
    r = d.rootComponent
    lo = {"visibili": [1e9] * 3, "tutti": [1e9] * 3}; hi = {"visibili": [-1e9] * 3, "tutti": [-1e9] * 3}
    nascosti, n_vis = [], 0
    # TIGHT box along the axes: b.boundingBox on a part rotated by a joint is larger than the true one (16/11: folded drone
    # 150 × 165 × 67 instead of 147.95 × 89.97 × 62). getOrientedBoundingBox with the X and Y axes gives the right one.
    _X = adsk.core.Vector3D.create(1, 0, 0); _Y = adsk.core.Vector3D.create(0, 1, 0)
    for occ, b in [(None, b) for b in r.bRepBodies] + [(o, b) for o in r.allOccurrences for b in o.bRepBodies]:
        ob = app.measureManager.getOrientedBoundingBox(b, _X, _Y); c = ob.centerPoint
        lati = ((c.x - ob.length / 2, c.x + ob.length / 2), (c.y - ob.width / 2, c.y + ob.width / 2), (c.z - ob.height / 2, c.z + ob.height / 2))
        quali = ["tutti"] + (["visibili"] if b.isVisible else [])
        if b.isVisible: n_vis += 1
        else: nascosti.append((occ.fullPathName + "/" if occ else "") + b.name)
        for q in quali:
            for i, (a, z) in enumerate(lati):
                lo[q][i] = min(lo[q][i], a * 10); hi[q][i] = max(hi[q][i], z * 10)
    def _ing(q):
        if lo[q][0] > 1e8: return None
        return {"min_mm": [round(v, 4) for v in lo[q]], "max_mm": [round(v, 4) for v in hi[q]],
                "dimensioni_mm": [round(hi[q][i] - lo[q][i], 4) for i in range(3)]}
    rap["assieme"] = {"corpi_visibili": n_vis, "corpi_nascosti": nascosti, "ingombro_visibili": _ing("visibili"), "ingombro_tutti": _ing("tutti")}
    rap["schizzi_non_vincolati"] = [s["nome"] for s in rap["schizzi"] if not s["vincolato"]]
    print(json.dumps(rap, ensure_ascii=False))
