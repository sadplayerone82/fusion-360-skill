# Editing, importing, copying, resuming

## 1. Finding and reopening a project
Projects live in the projects folder of `impostazioni.json` (`cartella_progetti`), with the list `elenco-progetti.md` (date,
name, description, folder), written by `scripts/nuovo_progetto.py`. «Yesterday's bracket» is searched there (`nuovo_progetto.py --cerca
<parola>`); the latest version is the file with the highest number in `consegna/` (or `progetto.f3d`, the copy after the last step). Reopen the latest version:
`im = app.importManager; im.importToNewDocument(im.createFusionArchiveImportOptions(file_f3d))` (reopened it stays parametric: parameters,
timeline and constraints intact, tested). Changes are saved in a **new version** (`-v2`, `-v3`…), never over the previous one.

## 2. Editing a model with history (timeline)
- Read the timeline first: `[(o.index, o.name, o.entity.objectType, o.healthState) for o in d.timeline]`.
- Changing a parameter: `d.userParameters.itemByName("x").expression = "30 mm"`.
- Changing the definition of a feature (official Autodesk recipe): `feat.timelineObject.rollTo(True)` → edit (e.g.
  `adsk.fusion.SymmetricExtentDefinition.cast(feat.extentOne).distance.expression = "larghezza + 10 mm"`) → `d.timeline.moveToEnd()`.
- Inserting a feature in the middle: `rollTo(True)` on the feature in front of which it goes, create the new one, `moveToEnd()`.
- Moving a feature: `to.canReorder(indice)` then `to.reorder(indice)`.
- **Repairing** a feature with a lost reference (e.g. deleted sketch): changing its profile is refused
  («InternalValidationError : curProfile»); go back before the feature, redo the constrained sketch, delete and **redo** the feature with the
  same name, `moveToEnd()`, report. Tested: volume correct again, 0 elements in error.
After every change: report and measurements against the **recomputed** expected values.

## 3. Importing downloaded STEP and STL
- STEP: `o = im.createSTEPImportOptions(file); o.isViewFit = False; im.importToTarget(o, r)`. Each body ends up in **its own component**:
  look for the bodies in `d.allComponents`. Measure volume and bounding box right away (they are the starting point of the expected values).
- **STEP plus drawing of the same part** (rebuilding a «dumb» model as parametric): the two sources may not match, because
  the drawing rounds. Measure **every** dimension on the imported 3D and put it next to the drawing's; even a difference of a few
  thousandths changes the volume beyond the tolerance (tested: floor 1.93 on the drawing and 1.925 in the STEP → volume +0.14 %).
  List the differences and **ask which source counts** before modeling, even if the request says «take the dimensions from the drawing»;
  at the end compare volume, bounding box and number of faces with the STEP and write the differences in the report.
- STL/3MF: first `scripts/controlla_mesh.py` (closed? dimensions?), then `r.meshBodies.add(file, adsk.fusion.MeshUnits.MillimeterMeshUnit)`.
- Mesh → solid: `F.meshConvertFeatures.createInput([mesh])` (wants a **list**) and `add`. Tested on a cube (exactly 4 000 mm³).
  On large organic meshes the faceted solid is heavy and hard to edit: to lengthen or shorten it is better to cut with
  a plane, move and rejoin, or tell the user the limit. The «prismatic» method (recognizes cylinders and planes) with the Personal
  license is **refused** («No rights for mesh conversion», tested): a spare part is rebuilt from computed sections
  (`ricette-stampi-mesh-pezzi.md`). Mesh reduction: not tested, check first that it is not paid.
- Direct edits on an imported body (no history): move/offset faces with the features of **its** component
  (`b.parentComponent.features.offsetFacesFeatures.createInput([faccia], S("2 mm"))`). Tested: +2 mm = computed volume.

## 4. Copying a real part (broken, to be replaced)
Ask the user for:
1. the **dimensions that matter, with the caliper** (holes, fits, thicknesses, bounding box), **3 readings** per dimension, and which caliper they use;
2. **photos** only for the shape: part lying flat, phone straight above and a bit far (zoom), **ruler or object of known size
   on the same plane**, uniform background, one photo per side; saved in the project's `foto/` folder (photos pasted in the chat are not
   files).
3. where the part is broken, the intact part or the part it fits into.
Then `scripts/misura_foto.py` (scale from the reference, pixel measurements → mm with uncertainty ≈ 1–2 px × scale) and image as a **canvas**
at true scale: `ci = r.canvases.createInput(file, r.xYConstructionPlane)`, `m = adsk.core.Matrix2D.create();
m.setWithCoordinateSystem(adsk.core.Point2D.create(0, 0), adsk.core.Vector2D.create(larghezza_cm, 0), adsk.core.Vector2D.create(0, altezza_cm))`,
`ci.transform = m; r.canvases.add(ci)` (the size is the length of the vectors). Trace over it, but critical dimensions **always** come from the
caliper. On real photos perspective and distortion have not been tested: declare it. Knurling and grips: not tested.

## 5. Resuming after Fusion closes
Every project has: `progetto.f3d` updated after each verified step, `passi/NN-nome.py`, `registro.json`. After a close:
`Progetto(...).riapri()` (from the copy, compare with the last line of the log) or `rigioca()` (replays the steps from the scripts, new
document). Both tested: same volume as the log. Never start over from memory.
