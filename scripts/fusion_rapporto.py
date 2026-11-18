"""Script da eseguire DENTRO Fusion (via fusion_mcp_execute, readOnly: true): stampa un rapporto JSON dello stato del modello
attivo, in unità dell'utente (mm, mm², mm³, g, gradi). Base della verifica automatica (area H dello studio).

Contenuto: tipo di progetto e unità; parametri utente (nome, espressione, valore); timeline (elementi non sani con messaggio);
schizzi (completamente vincolati?, profili); corpi (solido?, visibile?, volume, area, ingombro, n. facce/spigoli, materiale,
massa, baricentro); componenti e occorrenze. Non modifica nulla.
"""
import adsk.core, adsk.fusion, json

def mm(p):
    return [round(p.x * 10, 4), round(p.y * 10, 4), round(p.z * 10, 4)]

def run(_context: str):
    app = adsk.core.Application.get()
    d = adsk.fusion.Design.cast(app.activeProduct)
    if not d:
        print(json.dumps({"errore": "il prodotto attivo non è un progetto (Design)"}))
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
    while coda:   # un gruppo (es. quello creato importando un DXF) ha stato 5 e nasconde i suoi elementi: si guardano quelli
        i, it = coda.pop(0)   # dentro un gruppo .index dà errore: si tiene l'indice del gruppo
        if it.isGroup:
            g = adsk.fusion.TimelineGroup.cast(it)
            coda = [(i, g.item(k)) for k in range(g.count)] + coda
        else:
            elementi.append((i, it))
    for i, it in elementi:
        if it.isSuppressed:     # sospesa apposta (stato 3, nessun messaggio): non è un errore, si elenca a parte
            rap["timeline"]["sospesi"].append({"indice": i, "nome": it.name})
        elif it.healthState != sani:
            rap["timeline"]["non_sani"].append({"indice": i, "nome": it.name, "stato": it.healthState,
                                                "messaggio": it.errorOrWarningMessage, "soppresso": it.isSuppressed})
    for comp in d.allComponents:
        for sk in comp.sketches:
            vincolato = sk.isFullyConstrained
            nota = None
            # un testo (sketchTexts) tiene lo schizzo «non vincolato» per sempre, anche col riquadro e tutti i punti vincolati
            # (provato 09/11). Allora conta se il riquadro c'è e curve e punti sono tutti vincolati; un testo senza riquadro resta libero.
            if not vincolato and sk.sketchTexts.count and sk.sketchCurves.count \
                    and all(c.isFullyConstrained for c in sk.sketchCurves) and all(p.isFullyConstrained for p in sk.sketchPoints):
                vincolato, nota = True, "testo: Fusion lo dice sempre libero; riquadro e punti vincolati"
            rap["schizzi"].append({"componente": comp.name, "nome": sk.name, "vincolato": vincolato, "nota": nota,
                                   "profili": sk.profiles.count, "visibile": sk.isVisible})
        for b in comp.bRepBodies:
            bb = b.boundingBox
            # b.volume è il calcolo veloce: su superfici curve che si intersecano sbaglia di qualche mm³ (provato 10/11: 6,85 mm³ su
            # 88 251, lo 0,008 %, quasi la tolleranza del giudice). Si usa il calcolo ad alta precisione.
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
    # ASSIEMI (11/11/2026): «corpi» qui sopra dà ogni corpo nelle coordinate del SUO componente (una volta sola anche se il
    # componente è usato 4 volte) e non sa se l'occorrenza è nascosta. Per l'ingombro vero dell'assieme si guardano le occorrenze:
    # i loro corpi sono già nella posizione dell'assieme. Provato sul drone dell'esame 10: dai componenti 154 mm, vero 148.
    r = d.rootComponent
    lo = {"visibili": [1e9] * 3, "tutti": [1e9] * 3}; hi = {"visibili": [-1e9] * 3, "tutti": [-1e9] * 3}
    nascosti, n_vis = [], 0
    # riquadro STRETTO lungo gli assi: b.boundingBox su un pezzo ruotato da un giunto è più largo del vero (16/11: drone piegato
    # 150 × 165 × 67 invece di 147,95 × 89,97 × 62). getOrientedBoundingBox con gli assi X e Y dà quello giusto.
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
