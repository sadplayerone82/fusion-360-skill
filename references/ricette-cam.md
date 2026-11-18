# CNC (Manufacture) via API

Ricetta provata su Fusion (nov. 2026): piastra in legno, frese reali Onsrud caricate da JSON, contorno 2D, post-processore «Grbl»,
G-code controllato con `scripts/verifica_gcode.py`. Con la licenza Personal (la più comune per uso personale) i rapidi sono rallentati
alla velocità di lavoro (Fusion lo scrive nel G-code).
- **Il contorno a silhouette lavora già anche i fori** (provato su una piastra con 4 fori): un'operazione in più per foro li rifà due
  volte; per un foro solo si usa `createNewChainSelection()` con `inputGeometry = [spigolo]`.
- **In una catena scelta a mano il lato della fresa dipende dal verso dello spigolo** (spigolo sopra o sotto il pezzo danno lati
  opposti), senza errori né avvisi: provato, fori percorsi dalla parte del materiale (di fatto Ø 16 invece di Ø 8) e contorno esterno
  dentro il pezzo (piastra 146 × 96). Si corregge con `isReverted = True` e si controlla sempre con `verifica_gcode.py`, che boccia la
  fresa dentro il pezzo.
- Il CAM funziona anche in un documento non salvato, ma in un documento nuovo va prima attivato l'ambiente:
  `app.userInterface.workspaces.itemById('CAMEnvironment').activate()` (senza: «failed to find product»).
- Misurato sulla piastra (legno 12 mm, fresa Ø 3,97, 10 000 giri/min, 3040 mm/min): percorso valido senza avvisi; 922 mm di taglio in
  21 s (= calcolo a mano: contorno × 3 passate + entrate); G-code di 143 righe, passate −3,9/−7,8/−12,5, ponticelli a −9,5, nessun
  refrigerante; il 98,9 % dei punti dell'ultima passata sta a 1,984 ± 0,05 mm dalla sagoma del pezzo (= raggio della fresa).
- Trappole: la fresa della libreria d'esempio ha 3 taglienti, refrigerante a getto (M8 nel G-code) e velocità generiche → usare frese
  vere; il primo post «grbl» della lista è di un'altra marca → scegliere per nome; `getPointAtParameter` agli estremi di uno spigolo può
  fallire → `getStrokes`.

## Contorno 2D di una piastra con frese reali e post-processore Grbl

Lo script qui sotto si lancia con Python sul PC (la riga `sys.path.insert` punta a `scripts/` della skill installata in
`~/.claude/skills/fusion-360`: cambiala se è altrove), con l'argomento `percorso` e poi `post`. Pezzo dal documento aperto (piastra
distesa sul piano XY, fondo a z = 0). Flusso dall'esempio ufficiale «Wood Routing Workflow Sample» + «Post Toolpaths Sample».
- utensile: fresa piatta Ø 4 mm della libreria ufficiale «Milling Tools (Metric)» (angoli interni R2 → fresa ≤ Ø 4)
- velocità (Onsrud, legno tenero, serie 52-200, Ø 5/32": 0,006–0,008"/tagliente): 10 000 giri/min × 2 taglienti × 0,15 mm = 3000 mm/min,
  entrata 1000 mm/min; passate da 4 mm (1 × D: valore pieno) → IPOTESI da confermare con la macchina dell'utente
- contorno 2D esterno, 3 ponticelli (6 × 3 mm), fondo 0,5 mm sotto il pezzo; grezzo = pezzo + 10 mm per lato

```python
"""CAM via API: percorso di taglio di una piastra in legno da 12 mm dal documento aperto
(piastra distesa sul piano XY, fondo a z = 0). Flusso dall'esempio ufficiale «Wood Routing Workflow Sample» + «Post Toolpaths Sample».
- utensile: fresa piatta Ø 4 mm della libreria ufficiale «Milling Tools (Metric)» (angoli interni R2 → fresa ≤ Ø 4)
- velocità (Onsrud, legno tenero, serie 52-200, Ø 5/32": 0,006–0,008"/tagliente): 10 000 giri/min × 2 taglienti × 0,15 mm = 3000 mm/min,
  entrata 1000 mm/min; passate da 4 mm (1 × D: valore pieno) → IPOTESI da confermare con la macchina dell'utente
- contorno 2D esterno, 3 ponticelli (6 × 3 mm), fondo 0,5 mm sotto il pezzo; grezzo = pezzo + 10 mm per lato
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.expanduser("~"), ".claude", "skills", "fusion-360", "scripts"))   # scripts/ della skill
from mcp_fusion import Sessione, esegui

USCITA = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "consegna", "cnc")).replace("\\", "/")
# Frese reali: Onsrud serie 52-200 «Double Flute Solid Carbide Upcut Spiral Wood Rout», dati dallo shop
# ufficiale LMT (lmt-tools.com, articoli 2600626 e 2600627); avanzamento per tagliente: tabella Onsrud «Soft Wood Cutting Data», riga
# 52-200, 5/32" e 3/16": 0,006–0,008" = 0,152–0,203 mm (si usa il minimo); passate ≤ 1 × D (valore pieno).
# Macchina: IPOTESI CNC hobbistica, avanzamento massimo 3000 mm/min → giri = 3000 / (2 × 0,152) ≈ 9900 → 10 000 giri/min.
LMT = "https://www.lmt-tools.com/en/shop/products/CXt0g1z44FcvW3LLqWdl0"
FRESE = [
    {"codice": "52-250", "descrizione": "Onsrud 52-250 — spirale upcut 2 taglienti Ø 5/32\" (3,97 mm)", "produttore": "LMT Onsrud", "link": LMT,
     "DC": 3.9675, "LCF": 15.875, "OAL": 50.8, "SFDM": 6.35, "NOF": 2, "numero": 1, "guid": "6e0c2f52-0250-4a6e-9f52-000000000250",
     "giri": 10000, "fz": 0.152, "entrata": 1000, "profilo": "Legno tenero — Onsrud", "nota_profilo": "Onsrud Soft Wood, 52-200, 0,006\"/tagliente; macchina 3000 mm/min (ipotesi)"},
    {"codice": "52-260", "descrizione": "Onsrud 52-260 — spirale upcut 2 taglienti Ø 3/16\" (4,76 mm)", "produttore": "LMT Onsrud", "link": LMT,
     "DC": 4.7625, "LCF": 19.05, "OAL": 50.8, "SFDM": 6.35, "NOF": 2, "numero": 2, "guid": "6e0c2f52-0260-4a6e-9f52-000000000260",
     "giri": 10000, "fz": 0.152, "entrata": 1000, "profilo": "Legno tenero — Onsrud", "nota_profilo": "Onsrud Soft Wood, 52-200, 0,006\"/tagliente; macchina 3000 mm/min (ipotesi)"},
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
    if not p: ris["errori"].append("manca " + nome); return
    try: p.expression = espr
    except Exception as e: ris["errori"].append(nome + ": " + str(e)[:100])
'''
PERCORSO = r'''
import time
while cam.setups.count: cam.setups.item(0).deleteMe()          # si riparte da zero ogni volta
import json as _j, math as _m
tl = adsk.cam.CAMManager.get().libraryManager.toolLibraries.toolLibraryAtURL(adsk.core.URL.create("systemlibraryroot://Samples/Milling Tools (Metric).json"))
modello = [t for t in tl if t.parameters.itemByName("tool_type").value.value == "flat end mill" and abs(t.parameters.itemByName("tool_diameter").value.value - 0.4) < 1e-6][0]
def fresa_vera(f):
    """fresa reale dai dati del produttore sul modello JSON di una fresa piatta della libreria"""
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
setup = cam.setups.add(si); setup.name = "piastra — legno 12 mm"
setup.stockMode = adsk.cam.SetupStockModes.RelativeBoxStock
for n, e in (("job_stockOffsetMode", "'simple'"), ("job_stockOffsetSides", "10 mm"), ("job_stockOffsetTop", "0 mm"), ("job_stockOffsetBottom", "0 mm"), ("wcs_origin_boxPoint", "'top 1'")):
    imposta(setup.parameters, n, e)
oi = setup.operations.createInput("contour2d"); oi.tool = fresa; oi.displayName = "Contorno esterno con ponticelli"
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
mt = cam.getMachiningTime(op, 1.0, 300.0, 0.0)          # feedScale, rapidi (cm/min) , cambio utensile (s)
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
scelto = sorted([c for c in tutti if "grbl" in c.description.lower()], key=lambda c: c.description != "Grbl")   # prima il Grbl generico
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

