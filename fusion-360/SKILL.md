---
name: fusion-360
description: >-
  Designs, models, modifies and verifies in Autodesk Fusion (Fusion 360) through the official Autodesk MCP server,
  like a professional CAD designer: mechanical parts, recognizable products, objects born from an idea, houses and
  rooms, furniture, jewelry, molds, sheet metal, moving assemblies; from a verbal request, a dimensioned drawing,
  photos, a STEP/STL file or an existing project, up to a checked parametric model saved as .f3d on the PC, with
  the outputs needed (STEP, 3MF, DXF, CNC G-code, PDF drawing, images). Use it when asked to model in 3D with
  Fusion, when Fusion is mentioned, and for 3D models, technical drawings, parts to copy or repair, CNC toolpaths
  or sheet metal when no other CAD is named, even without naming the skill (Fusion 360, CAD, sketch, extrude,
  STEP, drawing). Not for Rhino, FreeCAD, Blender, OpenSCAD, SolidWorks or other CAD, nor for slicing,
  electrical schematics or PCBs; 3D printing only if the user declares it (with a printing skill, if installed).
---

# Fusion — design and model like a professional

Answer in the user's language; script outputs and some file names are in Italian.
The person asking is often not a CAD designer: they describe an object, bring a drawing, a photo or a file. Your job is to deliver a
**correct, editable and verified model**, explaining in plain language what you did, with the numbers and their practical meaning
(«the hole is 3.4 mm: an M3 screw goes through it»), and **what you checked and what you did not**.

The risk to keep always in mind: **Fusion can build a wrong part without giving any error** (a hole that cuts away half the part, a rib
that grows on the wrong side, a save that answers «succeeded» and goes nowhere). That is why every step has an expected value
computed *before* and measured *after*.

## How you talk to Fusion
- MCP tools `fusion_mcp_*` of the official server (address in `impostazioni.json`, default `127.0.0.1:27182`); from Python scripts
  the same server through `scripts/mcp_fusion.py`. Every script is **one transaction**; the API works in **cm**. Details, traps and
  the rules learned from Fusion's logs: `references/connettore-e-api.md` — read it before the first script of the session.
- The settings (projects folder, language, printing skill, cloud yes/no, ports to check) are in
  `%USERPROFILE%\.claude\fusion-360\impostazioni.json` (or in the file named by the `FUSION360_SKILL_IMPOSTAZIONI` variable):
  `python -X utf8 scripts/impostazioni.py --mostra`.
- Code is never written inside a shell command: it is written to a file and run with
  `python -X utf8 scripts/esegui_file.py <file.py> [--sola-lettura] [--nuovo-documento]` (images, exports, flexibility tests,
  reopenings); model steps instead go through `scripts/progetto_locale.py` (e.g.
  `python -X utf8 scripts/progetto_locale.py <folder> passo <name> <file.py> --atteso <volume mm³>`). The file contains only the
  code: the header (short names, `vol`, `out`, `controlla`) is added by `mcp_fusion.py` (`references/ricette.md` §1).
- The user's screen is not touched: you work through MCP. Only for what the API cannot do (e.g. closing a Fusion dialog, deleting
  an object in a drawing) is the screen used, **saying so beforehand**, and then you stop.

## The flow (every step has a gate)

**J0 Environment** — `python -X utf8 scripts/ambiente.py` (`--avvia` if Fusion is closed; never a second copy). It must say
`si_puo_lavorare: true` (= work can start). If not, follow the warning: two Fusion instances open, MCP server off (Preferences → General → API), tools changed
after an update (tell the user), port of another program taken by Fusion. **If the server answers but scripts do not
start**, Fusion almost certainly has a dialog open (after a forced close: «Recovered documents») → sentence for the user:
«Fusion has a dialog open that blocks commands: close it (Close), then tell me done».

**J1 Understand the request and choose the branch** — from an idea, from a drawing, from a photo, from a file, modification, architecture, assembly:
branch table in `references/metodo.md` §10, scenarios in `references/scenari.md`. Write the **specification** (`assets/specifica.md`):
what it is for, what it touches, dimensions given or read, the *intent* in one sentence («the holes stay 12 mm from the edge»). Missing
dimensions **are not invented**: question, proposed value with the reason, and you **stop**. A dimension read in pixels is a hypothesis.
From an idea: 4 phases with a stop after each (questions → concepts with images → form → detail).

**J1b Manufacturing (only if declared)** — ask how the part will be made; **do not assume 3D printing**. FDM printing → a 3D
printing skill, if installed (`skill_stampa` in the settings), **before** modeling, otherwise the minimum rules of
`references/produzione-e-stampa.md`; CNC, sheet metal/laser, molds → `references/produzione-e-stampa.md` §0.
No manufacturing → deliver `.f3d`, STEP, images (and a drawing if requested).

**J1c Several parts in the same space** (enclosures with electronics, machines, housings): read `references/progetti-a-piu-pezzi.md`
**before drawing**: space budget including cables, clearances, assembly.

**J1d Recognizable objects** (a product that exists, a design object, «make me a model of…»): read
`references/forma-e-dettaglio.md` **before the questions**: agreed level of detail (never lower it on your own: «simplified forms»
is a question), references to scale, list of characteristic features, form before details. Correct numbers are not enough.

**J2 Plan and expected values** — components (before geometry, if there are parts that move or are assembled), **parameters** named
by function, order: references → solid volumes → cuts → modifications → fillets last. Compute the **expected values** by hand: volume after
every step, bounding box, positions. Method: `references/metodo.md`; how to compute: `references/verifica.md`.

**J3 Project** — `python -X utf8 scripts/nuovo_progetto.py "<name>" "<description>"` creates the folder in the projects folder
from the settings and adds it to the list. You work in a new document; **nothing is saved to the cloud** without permission (with the
Personal license, the most common for personal use, there are 10 slots: count them first).

**J4 Modeling in steps** — one step = one sketch or one feature, with `scripts/progetto_locale.py` (runs, measures, saves the step
script, updates the project log and the `.f3d` copy). Every script **checks in the same call** volume/bounding box/bodies against the expected value.
Use the code of the **tested recipes** instead of the API from memory; before a new function, look it up (recipes, `comandi.md`,
`apiDocumentation`): invented calls are the first cause of errors. If a measurement does not match, **look for the cause**; do not bend the
model to the number. An error found is fixed **on its own**, without redoing everything.

**J5 Verification** — `scripts/rapporto_modello.py` (0 elements in error, 0 unconstrained sketches, measurements = expected); **probe points** written from the
specification (`scripts/sonde.py`: volume, bounding box and center of mass do not see a wrong hole circle); assemblies: no interpenetration and
measured clearances (interference 0 only says the parts do not interpenetrate: `scripts/controlla_pezzi.py`);
**minimum thickness** of every body (`scripts/spessore_minimo.py --limite <mm>`, limit chosen according to manufacturing and written in the
specification: below the limit the delivery stops; «NON MISURATO» (= not measured) is not a green light: measure another way); for objects that stand on a surface,
stability (`scripts/analisi_forma.py`); recognizable objects: the poor-form signs (`scripts/segni_forma.py`) and the images next to the
references (`references/forma-e-dettaglio.md` §4); two images (iso and front) actually looked at. `references/verifica.md`.

**J6 Flexibility** — change 2–4 important parameters, also **far** from the initial values, re-check the expected values, restore the values.

**J7 Outputs** — according to the branch: 3MF checked axis by axis (`scripts/controlla_mesh.py`), STEP, DXF of the flat pattern, G-code
checked (`scripts/verifica_gcode.py`), PDF. A «succeeded» answer is not enough: the file must exist and must be measured again.

**J8 Drawing or render (only if requested)** — `references/tavole-e-render.md`: 2 documents in the cloud (permission), one operation per
call, symbols and hole table as images computed from the view (`scripts/tavola_simboli.py`), check of **what is missing** and of
**legibility** on the zoomed-in PDF. If a drawing command stays waiting (`scripts/registri.py comando`): «Fusion is waiting for a click:
press Esc in Fusion, then tell me done».

**J9 Delivery** — `.f3d` (new version, never overwritten), outputs, images, `resoconto.md` (`assets/resoconto.md`): what you did,
the numbers and what they mean, **to what level you verified each thing and what you did not verify**.

**J10 Resuming and corrections** — the state of the work lives in the **project log** (phase, step, expected values, open questions): tomorrow, on
another PC or after the conversation has been summarized, you restart from there (`nuovo_progetto.py --cerca <word>` to find it).
A correction = one parameter or one feature at a time, new version. A manufactured part that «does not fit»: first measure it (3 readings),
and for printing go through the printing skill, if installed.

## Where you stop and wait for the user
After the questions · after each phase of the «from an idea» branch · after the manufacturing decisions · before overwriting, deleting or saving
to the cloud · when the screen is needed · at delivery. Between these points work on your own, measuring every step.

## The traps that give wrong parts without errors (the others are in the references)
- **Units**: API in cm; dimensions as strings with units (`"12 mm"`) or parameters.
- **Faces and edges** by geometry, never by index, and **looked up again** after every feature.
- **Sketches**: the API does not constrain them by itself; on XZ the sketch y is −Z (`modelToSketchSpace`).
- **Saving**: with a drawing open Fusion keeps a hidden copy of the project with the same name; saving it «succeeds» but does not go
  to the cloud → after every cloud save check that the version went up.
- **Drawings**: symbol commands hang for 600 s; errors come out at the next call; nothing can be deleted via API.
- **Derive**: derived geometry updates (with `computeAll`), **derived parameters do not**.
- **Exports**: a hidden body is not exported but the API says «succeeded».
- **SVG**: Fusion reads the units as pixels at 96 dpi (scale 96/25.4 to get mm).
- **License**: never `purchase`, credit-consuming features or cloud renders without a request; with the Personal license (the most common for personal
  use) many features are missing or reduced: `references/limiti-personal.md`.

## References (open them when needed)
| File | When |
|---|---|
| `references/connettore-e-api.md` | before the first script: tools, units, transactions, traps, rules from the logs |
| `references/ricette.md` §1 | the script header (`vol`, `out`, `controlla`) and how `progetto_locale.py` measures and logs a step |
| `references/metodo.md` | J1–J2: intent, parameters, order, names, **the branches** (§10) |
| `references/scenari.md` | J1: the 19 uses of Fusion, branch, recipes and limits of each |
| `references/progetti-a-piu-pezzi.md` | several parts in the same space: space budget, clearances, all the pairs, assembly, close-up images |
| `references/forma-e-dettaglio.md` · `ricette-forma.md` | recognizable objects: levels of detail, references to scale, characteristic features, poor-form signs; tested form recipes (sections → loft → fillets → shell) |
| `references/verifica.md` | J2, J5: expected values, checks in the same call, minimum thickness, form, scale of the checks |
| `references/ricette.md` | essential recipes (constrained sketches, holes, countersinks, text, snap hooks, gears, joints, exports) |
| `references/ricette-schizzi-e-piani.md` · `ricette-solidi.md` · `ricette-superfici-forme-lamiera.md` · `ricette-assiemi.md` · `ricette-modificare-importare.md` · `ricette-produzione-viste-render.md` | tested recipes, by family |
| `references/ricette-decori-anelli.md` | text on a curved face, knurling, pattern along a path, rings |
| `references/ricette-stampi-mesh-pezzi.md` | molds, mesh → solid, splitting into parts, skeleton with Derive |
| `references/ricette-lamiera-form-costruzione.md` | sheet metal with flat pattern, T-spline, joint origins, appearances, scene, construction, surfaces, SVG |
| `references/ricette-foto-tavole.md` | photos with rectified perspective; drawings with dimensions, datum, tolerance, hole table |
| `references/ricette-cam.md` | CNC: real tools, contour, post-processor, checked G-code |
| `references/comandi.md` | Fusion's 1 665 commands: name, identifier, API, Personal, tested — **search it, do not read it whole** |
| `references/dati-standard.md` | threads, clearance holes, screws, nuts, inserts, bearings (search) |
| `references/assiemi.md` · `produzione-e-stampa.md` · `modificare-importare-copiare.md` · `tavole-e-render.md` · `limiti-personal.md` | assemblies; manufacturing; existing files, photos, resuming; drawings and renders; license |

Scripts are run with `python -X utf8 <script>` (without UTF-8, on Windows accented characters break the output).
