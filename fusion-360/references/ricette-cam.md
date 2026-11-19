# CNC (Manufacture) via API

Recipe tested on Fusion (Nov. 2026): wooden plate, real Onsrud cutters loaded from JSON, 2D contour, «Grbl» post-processor,
G-code checked with `scripts/verifica_gcode.py`. With the Personal license (the most common for personal use) rapids are slowed
to the feed rate (Fusion writes it in the G-code).
- **The silhouette contour already machines the holes too** (tested on a plate with 4 holes): an extra operation per hole machines them
  twice; for a single hole use `createNewChainSelection()` with `inputGeometry = [spigolo]`.
- **In a hand-picked chain the cutter side depends on the direction of the edge** (edge on the top or bottom of the part give opposite
  sides), without errors or warnings: tested, holes machined from the material side (in effect Ø 16 instead of Ø 8) and outer contour
  inside the part (plate 146 × 96). It is corrected with `isReverted = True` and always checked with `verifica_gcode.py`, which fails a
  cutter inside the part.
- CAM also works in an unsaved document, but in a new document the workspace must be activated first:
  `app.userInterface.workspaces.itemById('CAMEnvironment').activate()` (without it: «failed to find product»).
- Measured on the plate (wood 12 mm, cutter Ø 3.97, 10 000 rpm, 3040 mm/min): valid toolpath without warnings; 922 mm of cutting in
  21 s (= hand calculation: contour × 3 passes + entries); G-code of 143 lines, passes −3.9/−7.8/−12.5, tabs at −9.5, no
  coolant; 98.9 % of the points of the last pass lie at 1.984 ± 0.05 mm from the part outline (= cutter radius).
- Traps: the sample library cutter has 3 flutes, flood coolant (M8 in the G-code) and generic speeds → use real
  cutters; the first «grbl» post in the list is from another brand → choose by name; `getPointAtParameter` at the ends of an edge can
  fail → `getStrokes`.

## 2D contour of a plate with real cutters and the Grbl post-processor

The script below is run with Python on the PC (the `sys.path.insert` line points to `scripts/` of the skill installed in
`~/.claude/skills/fusion-360`: change it if it is elsewhere), with the argument `percorso` and then `post`. Part from the open document (plate
lying on the XY plane, bottom at z = 0). Flow from the official samples «Wood Routing Workflow Sample» + «Post Toolpaths Sample».
- tool: Ø 4 mm flat end mill from the official library «Milling Tools (Metric)» (inner corners R2 → cutter ≤ Ø 4)
- speeds (Onsrud, soft wood, series 52-200, Ø 5/32": 0.006–0.008"/flute): 10 000 rpm × 2 flutes × 0.15 mm = 3000 mm/min,
  plunge 1000 mm/min; 4 mm passes (1 × D: full value) → HYPOTHESIS to be confirmed with the user's machine
- outer 2D contour, 3 tabs (6 × 3 mm), bottom 0.5 mm below the part; stock = part + 10 mm per side

```python
"""CAM via API: cutting toolpath of a 12 mm wooden plate from the open document
(plate lying on the XY plane, bottom at z = 0). Flow from the official samples «Wood Routing Workflow Sample» + «Post Toolpaths Sample».
- tool: Ø 4 mm flat end mill from the official library «Milling Tools (Metric)» (inner corners R2 → cutter ≤ Ø 4)
- speeds (Onsrud, soft wood, series 52-200, Ø 5/32": 0.006–0.008"/flute): 10 000 rpm × 2 flutes × 0.15 mm = 3000 mm/min,
  plunge 1000 mm/min; 4 mm passes (1 × D: full value) → HYPOTHESIS to be confirmed with the user's machine
- outer 2D contour, 3 tabs (6 × 3 mm), bottom 0.5 mm below the part; stock = part + 10 mm per side
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # the skill's scripts/
from mcp_fusion import Sessione, esegui

USCITA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "consegna", "cnc")).replace("\\", "/")
# Real cutters: Onsrud series 52-200 «Double Flute Solid Carbide Upcut Spiral Wood Rout», data from the official
# LMT shop (lmt-tools.com, items 2600626 and 2600627); feed per flute: Onsrud table «Soft Wood Cutting Data», row
# 52-200, 5/32" and 3/16": 0.006–0.008" = 0.152–0.203 mm (the minimum is used); passes ≤ 1 × D (full value).
# Machine: HYPOTHESIS hobby CNC, maximum feed 3000 mm/min → rpm = 3000 / (2 × 0.152) ≈ 9900 → 10 000 rpm.
LMT = "https://www.lmt-tools.com/en/shop/products/CXt0g1z44FcvW3LLqWdl0"
FRESE = [
    {"codice": "52-250", "descrizione": "Onsrud 52-250 — upcut spiral 2 flutes Ø 5/32\" (3.97 mm)", "produttore": "LMT Onsrud", "link": LMT,
     "DC": 3.9675, "LCF": 15.875, "OAL": 50.8, "SFDM": 6.35, "NOF": 2, "numero": 1, "guid": "6e0c2f52-0250-4a6e-9f52-000000000250",
     "giri": 10000, "fz": 0.152, "entrata": 1000, "profilo": "Soft wood — Onsrud", "nota_profilo": "Onsrud Soft Wood, 52-200, 0.006\"/flute; machine 3000 mm/min (hypothesis)"},
    {"codice": "52-260", "descrizione": "Onsrud 52-260 — upcut spiral 2 flutes Ø 3/16\" (4.76 mm)", "produttore": "LMT Onsrud", "link": LMT,
     "DC": 4.7625, "LCF": 19.05, "OAL": 50.8, "SFDM": 6.35, "NOF": 2, "numero": 2, "guid": "6e0c2f52-0260-4a6e-9f52-000000000260",
     "giri": 10000, "fz": 0.152, "entrata": 1000, "profilo": "Soft wood — Onsrud", "nota_profilo": "Onsrud Soft Wood, 52-200, 0.006\"/flute; machine 3000 mm/min (hypothesis)"},
]
PARAMETRI_OP = {"tool_spindleSpeed": "10000 rpm", "tool_feedCutting": "3040 mm/min", "tool_feedPlunge": "1000 mm/min",
                "tool_feedEntry": "1000 mm/min", "tool_feedRamp": "1000 mm/min", "tool_coolant": "'disabled'",
                "doMultipleDepths": "true", "maximumStepdown": "3.9 mm", "tolerance": "0.02 mm",
                "group_tabs": "true", "tabWidth": "6 mm", "tabHeight": "3 mm", "tabPositioning": "'distance'", "tabDistance": "60 mm",
                "bottomHeight_offset": "-0.5 mm"}

TESTA = r'''
cam = adsk.cam.CAM.cast(app.activeDocument.products.itemByProductType("CAMProductType"))
ris = {"errori": []}
def imposta(params, nome, espr):
    p = params.itemByName(nome)
    if not p: ris["errori"].append("missing " + nome); return
    try: p.expression = espr
    except Exception as e: ris["errori"].append(nome + ": " + str(e)[:100])
'''
PERCORSO = r'''
import time
while cam.setups.count: cam.setups.item(0).deleteMe()          # start from scratch every time
import json as _j, math as _m
tl = adsk.cam.CAMManager.get().libraryManager.toolLibraries.toolLibraryAtURL(adsk.core.URL.create("systemlibraryroot://Samples/Milling Tools (Metric).json"))
modello = [t for t in tl if t.parameters.itemByName("tool_type").value.value == "flat end mill" and abs(t.parameters.itemByName("tool_diameter").value.value - 0.4) < 1e-6][0]
def fresa_vera(f):
    """real cutter from the manufacturer's data on the JSON template of a flat end mill from the library"""
    j = _j.loads(modello.toJson())
    g = j["geometry"]
    g.update({"DC": f["DC"], "LCF": f["LCF"], "OAL": f["OAL"], "SFDM": f["SFDM"], "NOF": f["NOF"], "LB": f["LCF"] + 2, "HAND": True,
              "shoulder-diameter": f["DC"], "shoulder-length": f["LCF"], "tip-diameter": f["DC"], "RE": 0})
    j.update({"description": f["descrizione"], "vendor": f["produttore"], "product-id": f["codice"], "product-link": f["link"],
              "BMC": "carbide", "guid": f["guid"]})
    j.pop("holder", None)
    j["post-process"]["number"] = f["numero"]
    n, fz = f["giri"], f["fz"]
    vf = round(n * f["NOF"] * fz)
    p = j["start-values"]["presets"][0]
    p.update({"name": f["profilo"], "description": f["nota_profilo"], "n": n, "n_ramp": n, "f_z": fz, "f_n": fz * f["NOF"],
              "v_f": vf, "v_f_leadIn": vf, "v_f_leadOut": vf, "v_f_transition": vf, "v_f_plunge": f["entrata"], "v_f_ramp": f["entrata"],
              "v_c": _m.pi * f["DC"] * n / 1000, "tool-coolant": "disabled"})
    j["start-values"]["presets"] = [p]
    t = adsk.cam.Tool.createFromJson(_j.dumps(j))
    cam.documentToolLibrary.add(t)
    return [cam.documentToolLibrary.item(k) for k in range(cam.documentToolLibrary.count) if cam.documentToolLibrary.item(k).parameters.itemByName("tool_productId").value.value == f["codice"]][-1], vf
ris["frese"] = {}
frese = {}
for f in FRESE:
    t, vf = fresa_vera(f); frese[f["codice"]] = t
    ris["frese"][f["codice"]] = {k: t.parameters.itemByName(k).expression for k in ("tool_diameter", "tool_fluteLength", "tool_numberOfFlutes", "tool_shaftDiameter", "tool_overallLength", "tool_vendor", "tool_spindleSpeed", "tool_feedCutting", "tool_coolant") if t.parameters.itemByName(k)}
fresa = frese["52-250"]
si = cam.setups.createInput(adsk.cam.OperationTypes.MillingOperation)
si.models = [cam.designRootOccurrence.bRepBodies.item(0)]
setup = cam.setups.add(si); setup.name = "plate — wood 12 mm"
setup.stockMode = adsk.cam.SetupStockModes.RelativeBoxStock
for n, e in (("job_stockOffsetMode", "'simple'"), ("job_stockOffsetSides", "10 mm"), ("job_stockOffsetTop", "0 mm"), ("job_stockOffsetBottom", "0 mm"), ("wcs_origin_boxPoint", "'top 1'")):
    imposta(setup.parameters, n, e)
oi = setup.operations.createInput("contour2d"); oi.tool = fresa; oi.displayName = "Outer contour with tabs"
for n, e in PARAMETRI_OP.items(): imposta(oi.parameters, n, e)
op = setup.operations.add(oi)
cc = op.parameters.itemByName("contours").value; ch = cc.getCurveSelections(); ch.createNewSilhouetteSelection(); cc.applyCurveSelections(ch)
fut = cam.generateToolpath(op)
t0 = time.time()
while not fut.isGenerationCompleted and time.time() - t0 < 200:
    adsk.doEvents(); time.sleep(0.5)
ris["calcolato_in_s"] = round(time.time() - t0, 1)
ris["percorso"] = {"ha_percorso": op.hasToolpath, "valido": op.isToolpathValid, "avvisi": op.hasWarning, "errori": op.hasError,
                   "messaggio": (op.error or op.warning or "")[:300] if hasattr(op, "error") else ""}
mt = cam.getMachiningTime(op, 1.0, 300.0, 0.0)          # feedScale, rapids (cm/min) , tool change (s)
ris["tempo"] = {k: round(getattr(mt, k), 2) for k in dir(mt) if not k.startswith("_") and isinstance(getattr(mt, k, None), (int, float))}
lett = {n: op.parameters.itemByName(n).expression for n in ("tool_spindleSpeed", "tool_feedCutting", "tool_feedPlunge", "maximumStepdown", "tabDistance", "tabHeight") if op.parameters.itemByName(n)}
ris["parametri_letti"] = lett
ris["grezzo_mm"] = [round(setup.parameters.itemByName(n).value.value * 10, 2) for n in ("stockXLow", "stockXHigh", "stockYLow", "stockYHigh", "stockZLow", "stockZHigh") if setup.parameters.itemByName(n)]
'''
POST = r'''
import os
op = cam.setups.item(0).allOperations.item(0)
pl = adsk.cam.CAMManager.get().libraryManager.postLibrary
q = pl.createQuery(adsk.cam.LibraryLocations.Fusion360LibraryLocation); q.capability = adsk.cam.PostCapabilities.Milling
tutti = q.execute()
ris["post_disponibili"] = len(tutti)
scelto = sorted([c for c in tutti if "grbl" in c.description.lower()], key=lambda c: c.description != "Grbl")   # the generic Grbl first
ris["post_grbl"] = [(c.vendor, c.description) for c in scelto][:5]
cfg = scelto[0]
url = pl.importPostConfiguration(cfg, adsk.core.URL.create("user://"), "skill-grbl.cps")
post = pl.postConfigurationAtURL(url)
ni = cam.ncPrograms.createInput(); ni.displayName = "piastra"
ni.parameters.itemByName("nc_program_filename").value.value = "piastra"
ni.parameters.itemByName("nc_program_openInEditor").value.value = False
ni.parameters.itemByName("nc_program_output_folder").value.value = USCITA
ni.operations = [op]
prog = cam.ncPrograms.add(ni); prog.postConfiguration = post
ris["post_eseguito"] = prog.postProcess(adsk.cam.NCProgramPostProcessOptions.create())
ris["file"] = [f for f in os.listdir(USCITA)] if os.path.isdir(USCITA) else []
'''

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    fase = sys.argv[1]
    os.makedirs(USCITA, exist_ok=True)
    pre = f"USCITA = {USCITA!r}\nPARAMETRI_OP = {PARAMETRI_OP!r}\nFRESE = {FRESE!r}\n"
    ok, ris, righe = esegui(Sessione(), pre + TESTA + {"percorso": PERCORSO, "post": POST}[fase] + "out(**ris)\n", sola_lettura=False)
    print(ok, json.dumps(ris, ensure_ascii=False, indent=1) if ris else righe)

if __name__ == "__main__":
    main()
```
