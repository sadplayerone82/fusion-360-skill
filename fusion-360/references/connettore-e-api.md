# Talking to Fusion: MCP connector and API

Everything below was measured on Fusion (build 2706.1.14, November 2026, Personal license) with the official Autodesk MCP server,
with the user interface in Italian; where something looks strange,
it is exactly what made the tests go wrong.

## The tools
| Tool | What it is for |
|---|---|
| `fusion_mcp_execute` `featureType: "script"` | **all the modeling**: a Python script with `def run(_context: str):` run inside Fusion |
| `fusion_mcp_execute` `document` | open/close documents. `close` with `userConfirmedCloseWithoutSave: true` for test documents |
| `fusion_mcp_read` `screenshot` | image of the model (views: `current`, `iso-top-right`, `front`, `top`…) — to really look at the part |
| `fusion_mcp_read` `apiDocumentation` | documentation of a class or function (`searchPattern`, `className`) |
| `fusion_mcp_update` | `undo` / `redo` |
| `purchase`, `editImage`, `generatePowerpoint` | **do not use them** without an explicit request: they buy or consume credits |

From Python scripts (also from the shell) the same server is reached with `scripts/mcp_fusion.py` (HTTP client, `Sessione().strumento(nome,
argomenti)`); it is what `progetto_locale.py`, `rapporto_modello.py` and the other check scripts use. The «native» MCP tools exist in the
session only if Fusion was already open when the session started: if they are missing, the HTTP client works anyway.

## How a script behaves
- It is a **transaction**: if it fails, nothing of what it had created remains; a single `undo` cancels the whole script. That is why you
  work in small scripts (one step = one sketch or one feature): an error costs little and an undo is precise.
- The error comes back **inside the text** of the response (`"success": false` plus the traceback), not in the `isError` field: always check
  `success`.
- What the script prints with `print()` comes back to you: print one JSON line with the measurements you need (the project scripts use
  `print("RIS" + json.dumps(...))`). Do not catch exceptions in the script: you would hide where it failed.
- `readOnly: true` for scripts that only read: Fusion really checks it, and it works even if the user has a command open
  (a normal script instead does not start until the user closes the command: ask them to).
- Python variables do not survive from one script to the next: give a **name** to sketches, features, bodies, components and find them again with
  `sketches.itemByName`, `features.itemByName`, `bRepBodies.itemByName`. Avoid `findEntityByToken` (it creates a ghost undo
  step).
- Times: read 0.01–0.05 s, script 0.05–0.3 s. Verifying after every step costs nothing.
- If another third-party MCP add-in runs inside Fusion, the first response may contain one of its lines («Server listening on
  localhost:…»): ignore it and, if the port is among the `porte_da_controllare` of `impostazioni.json`, warn the user (`ambiente.py` does it).

## Units (the most important rule)
The API **always works in centimetres and radians**, even if the document is in mm: 2.0 in the API = 20 mm. Use:
- strings with units: `adsk.core.ValueInput.createByString("12 mm")`, `"30 deg"`;
- user parameter names (`"spessore_base"`, `"lunghezza / 2"`): the model stays readable and parametric;
- `createByReal` only for computed values, and in cm. Measurements read from the API must be multiplied by 10 (mm) or 1000 (mm³).
Parameter names **without spaces** and that are not unit symbols (`W`, `H`, `A`, `m`, `g`, `l`, `mm`, `in` are refused).

## Document types
A new document created by script (`app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)`) is **hybrid** (fine for
parts and assemblies). One created from the UI may be a **part** (a single component: no assemblies). Check
`design.designIntent` (0 part, 1 assembly, 2 hybrid) before creating components.

## Verified traps
| Trap | What happens | What to do |
|---|---|---|
| Sketch on the XZ plane | sketch point (x, y) goes to (x, 0, **−y**) in the model; on YZ the sketch X is −Z | give the points in model coordinates and convert them with `sketch.modelToSketchSpace(P(x, y, z))` |
| Profiles | the order of profiles is not reliable (the circle may come before the ring) | choose by area (`areaProperties().area`), number of loops or position |
| Faces and edges | after every feature the old faces **no longer exist**: reusing them gives «InternalValidationError : face» | search them again after every feature, by geometry (planar, normal, height, radius) |
| Constraints | the API does not add constraints by itself; AutoConstrain is not available (Personal) | constrained recipes in `ricette.md`; check `sketch.isFullyConstrained` |
| `sketch.boundingBox` | it is slightly large (40.02 for 40) | measure the lines, not the sketch bounding box |
| `occurrence.boundingBox` | gives all zeros | use the bounding box of the bodies |
| Localized names | libraries and materials have Italian names («Plastica ABS» = ABS Plastic) | choose them by **code** (`itemById("PrismMaterial-022")`) |
| Exporting a hidden body | no file, but `execute` says «success» | body visible, then check that the file exists and measure it |
| Wrong functions from memory | e.g. 3MF is exported with `createC3MFExportOptions` (not `create3MF…`) | copy from the recipes or ask `apiDocumentation`; if the documentation answers empty, the name does not exist |
| Lists | some functions want a Python list (`createOffsetInput`, `meshConvertFeatures.createInput([mesh])`), others an `ObjectCollection` | read the signature in `apiDocumentation` |
| Drawing opened hidden | `documents.open(df, False)` on a drawing **hangs Fusion** | open drawings visible |
| Long lines | the official server's adapter corrupts script lines beyond ~4 000 characters (figure from the open source project cadclamp, github.com/ChristianNHill/cadclamp) | short lines; long data in files read by the script |
| Invented calls | in the cadclamp project tests 39 % of the errors in Fusion were API calls that do not exist | before using a new function: recipes, then `apiDocumentation` or the installed stubs (`…\Api\Python\packages\adsk\*.py`) |
| Names that look right | `d.sheetMetalRules` does not exist (it is `designSheetMetalRules`); `FeatureControlFrameInput.firstFrame` cannot be reassigned; the scene's `backgroundType` is read-only | same rules: check the signature |
| Solid primitives | box, cylinder, sphere, torus: the classes (`BoxFeatures`…) **have no creation methods** | sketch + extrude/revolve |
| Bend radius in a sheet metal rule | `bendRadius.expression = "2.5 mm"` is **ignored without error if the number does not change**: it stays `Thickness`, and with a new thickness the radius changes too | to fix it go through another value (`"4 mm"`, then `"2.5 mm"`) and read the expression back; same round trip to go back to `Thickness` |
| Sheet metal DXF units | **reading** `DXFFlatPatternExportOptions.units` makes the script fail: «Distance unit is not supported by DXF» | do not read it; the default DXF is already in mm, or assign it without reading it (`MillimeterDistanceUnits`) |
| Moving a component via API | `occ.transform2 = M` works, but without fixing it **`computeAll` puts the part back where it was, without errors** | right after: `if d.snapshots.hasPendingSnapshot: d.snapshots.add()`; then remeasure the body position |
| Rotating a joint to test a mechanism | `computeAll` resets the joint to 0 without errors: the interference checks the starting position and the test passes **for nothing** | no `computeAll` between `rotationValue` and the measurement; read the angle back; also test a case that must collide |
| Rotated joint that must **stay** (assembly delivered folded, several joints one after another) | without capture position, **any new or edited feature resets it to 0 without errors**: another joint, a component, a changed extrude (tested: 30° → 0°). Only setting other `rotationValue`s, saving and exporting do **not** reset it | after every `rotationValue` that must stay: `if d.snapshots.hasPendingSnapshot: d.snapshots.add()` (tested: it stays at 30°); at the end read all the angles back. Parts carried by a joint (a propeller on the arm) must be constrained **before** moving it |
| Three-point arcs chained in a profile | `sketchArcs.addByThreePoints(p1, p2, p3)` keeps the arc counter-clockwise: if the three points are given clockwise, `startSketchPoint` is **p3**, not p1 (tested). Joining the curves «end to start» closes the profile wrongly (7 profiles instead of 2 in a real case) | after every arc read where `startSketchPoint` and `endSketchPoint` really are; count `sk.profiles.count` before extruding |
| A call that never ends | on a rich model (hundreds of sketches or faces: raised ribs, lettering, textures) a script that touches **everything at once** (constraining all sketches, probes or thickness on every face) keeps Fusion «Non risponde» (= Not responding) for tens of minutes, with memory climbing to several GB (measured: 28 minutes and 8 GB, work lost since the last saved step) | **before** launching it count how many elements it touches; above ~30, in chunks (one component or 20–30 elements per call) with the step saved between one chunk and the next; decorative details (textures, knurling, lettering) are made **last**, after the checks, and excluded from the heavy checks; if a call exceeds 5 minutes, next round halve the work per call. **Cause** (measured on 58 sketches, 210 elements): every change to a sketch recomputes the whole timeline after it; to constrain old sketches first move the marker right after the sketch (`schizzo.timelineObject.rollTo(False)`), edit (0.4 s), then `d.timeline.moveToEnd()` once per group of 10: 2.5 minutes for 58 sketches instead of a hang at 8 GB |
| Many heavy calls in a row | interferences between all pairs, high-accuracy physical properties, minimum thickness, images: they run in the window thread, Fusion shows «Non risponde» (= Not responding) for minutes and looks hung | one call at a time, never parallel sessions; heavy checks **only once, at the end**; if a call times out, check the state before repeating it |
| Diameter of a gear read from the bounding box | if no tooth lies on the axis the bounding box is smaller (83.913 for Ø 84) | maximum radius of the vertices from the hole centre; teeth are counted by entering the material along a circle |
| Dimensions on aligned points or concentric circles | a second dimension from the origin to an already aligned point, or a second centre, is refused as over-constraining | tie the points with vertical or horizontal construction lines; the second circle uses the `centerSketchPoint` of the first |
| Importing an `.f3d` into an assembly | `importToTarget2` creates a component that contains the file's one; in `allOccurrences` **the first one is the nested one** | to move use `r.occurrences`; search the bodies by name in `allOccurrences` |
| Choosing the profile by area | «the smallest» is the ring if the inner rectangle is large (936 mm² against 264): the wrong thing is cut without errors | check the expected volume in the same call |
| Through cut from a sketch at mid-part | `setAllExtent(SymmetricExtentDirection)` cuts **only one side**, without errors (tested: 2 000 mm³ removed instead of 4 000); `setOneSideExtent(ThroughAll, Symmetric)` gives an error | `ei.setTwoSidesExtent(ThroughAllExtentDefinition.create(), ThroughAllExtentDefinition.create())` and expected volume in the same call |
| Sketch with a text (`sketchTexts`) | it stays «not constrained» for Fusion even with the frame (`definition.rectangleLines`) and all points constrained (tested) | constrain the frame (one horizontal, midpoint of the diagonal on the origin, width and height); `rapporto_modello.py` counts it as constrained only if curves and points are |
| DXF for cutting | the default DXF also contains the bend lines (layers `BEND`, `BEND_EXTENT`): a laser could cut them | for the contour only `isCenterLinesExported = False` and `isExtentLinesExported = False`; read the file back and count the entities |

## Rules learned from Fusion's logs
When Fusion does something strange, the cause is found in its logs, not by trial and error:
`%LOCALAPPDATA%\Autodesk\Autodesk Fusion 360\<id>\logs\` (the most recently written `<id>` folder): `AppLogFile*.log` (cloud,
saves, MCP scripts), `AcCore*.log` (the line-by-line dialogue of the drawing commands), `FusionDrawing.log`.
- **Hidden copy**: when a drawing is open, Fusion loads a hidden copy of the design it uses, with the **same name**, in
  `app.documents`. It is recognized because `documentReferences` gives an error («non-top-level»). Saving it answers «success» but it **never goes to the
  cloud**. Rule: save only top-level documents and **after saving check that `dataFile.latestVersionNumber` went up
  by 1** (wait a few seconds); if not, stop.
- **«Documenti recuperati»** (= Recovered documents): after a forced close Fusion restarts with this window open; the server answers `initialize` but
  **no script starts**. It is closed with a click (it deletes nothing: it stays in File → Recover documents). `ambiente.py` reports it.
- **Drawings**: the symbol and hole table commands **dictate answers** to a command of the drawing engine; if one is not the
  expected one the command waits for a click and Fusion cancels it after **600 s** (hung in the meantime). Errors of the drawing functions
  **come out at the next call**, not on the wrong line. Rules: one operation per call, right after a read (e.g.
  `drawingSymbols.count`), then the tail of `AcCore*.log`: if the last line is a question without an answer, tell the user
  «Fusion is waiting for a click: press Esc in Fusion, then tell me done» instead of waiting 10 minutes.
- **Output lost after too many scripts**: every script adds a layer to `sys.stdout` and nobody removes it; after about **368 scripts** in the same
  Fusion session the response is `success: true` with an **empty** message, for any script (measured). `mcp_fusion.py` prevents it
  by itself and, if it happens anyway, `esegui` says so instead of returning «nothing». Whoever uses the native MCP tools does not have this protection:
  if a script that prints comes back empty, use `mcp_fusion.py` or restart Fusion. Within a session never trust an empty response.
- **Two documents with the same name in the cloud**: choose by date (`dateCreated`) or identifier, never the first in the list.
- **Reading the logs**: `scripts/registri.py comando` says whether a drawing command is still running (`FusionDrawing.log`: start without
  end, does not depend on the language); `dialogo` shows questions and answers; `salvataggi` the uploads to the cloud. The line «show recovery document»
  is in all the logs and means nothing; the «Documenti recuperati» window does not appear among the system windows: it is recognized from its
  behaviour (`ambiente.py`: a one-line script does not return within 25 s).

## After a Fusion update
Fusion updates and closes by itself. On restart `scripts/ambiente.py` compares the list of tools with the saved one: if it has
changed, tell the user before continuing, because recipes and traps might no longer apply.
