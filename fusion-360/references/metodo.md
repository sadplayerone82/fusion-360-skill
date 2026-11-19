# The professional's method

## Why a method is needed
A part «with the right shape» is not enough: when the user asks «make it 10 mm longer» or «holes farther apart», a badly built
model **breaks without errors**. Test done: the same plate built as a beginner (fixed coordinates) and as a professional
(parameters, constraints, names), then length 60 → 90 and thickness 5 → 8. The beginner has 0 Fusion errors but 2 violations of the intent
(a hole 38 mm from the edge instead of 8, the pin off-centre); the professional 0. In research (Camba et al. 2016, CAD 74) the ordered
«resilient» method (RMS) halved or quartered the editing times (115 s against 630 s unstructured, experiment 1).

## 1. The intent, first of all
Write in one sentence what must stay true if the dimensions change: «the holes stay 12 mm from the free end and symmetric», «the pin
stays in the centre». Propose it yourself to the user in simple words and ask for confirmation: they do not know the term, but they know what they need.
Parameters and constraints follow from it.

## 2. User parameters
- One parameter for each design dimension, with a **function name** (`spessore_parete`, `gioco_coperchio`, `interasse_fori`) and a
  comment on its origin («from the drawing», «from the printing skill: PETG clearance»). Names without spaces, never unit symbols.
- Secondary dimensions as **formulas** of the main parameters (`lunghezza_base - distanza_foro`, `interasse / 2`): a dimension is
  changed in one place only. Do not mix fixed numbers and parameters in the same logic, and avoid circular references.

## 3. Timeline order (resilient method)
1. **References**: construction planes at parametric distance, layout sketches.
2. **Solid volumes** that give the shape (extrudes, revolves: they are the base of 90 % of parts).
3. **Details that remove material**: holes, pockets, slots — children of the references and volumes, never used as a reference by anything else.
4. **Modifiers**: patterns, mirrors, drafts.
5. **Fillets and chamfers last**: a fillet made early breaks when the downstream geometry changes.
A trick from Autodesk instructors: «work backwards» — imagine the part without fillets and without cuts, model that, then add.

## 4. Sketches
- On origin planes or parametric construction planes, **not on faces** that may change (a sketch on a face projects its
  edges by itself: in the test the «pin» was born on the circle of a projected hole).
- **Fully constrained** and anchored to the origin: constraints first (horizontal, vertical, coincident, symmetry, midpoint), then
  dimensions; dimensions are parameters. A constrained sketch is predictable, a free one deforms at the first change.
- Many small sketches, one per function (profile, holes, reliefs), instead of a big one: they are easier to edit and repair.
- Construction geometry for axes, symmetries, alignments; «real» geometry only for the contours that become features. Careful:
  a **centerline** (`isCenterLine`) splits profiles, a **construction** line does not.
- Projections sparingly, never of filleted or changing edges.

## 5. Names
Sketches, features, bodies, components and planes with names by function (`SK_profilo`, `EST_base`, `TAGLIO_fori`, `RAC_interno`,
`PIANO_sopra`). They help you find them in later scripts and the user understand the timeline.

## 6. Components
If there are parts that move, fit together or must be printed separately, create the **components before the geometry** and work
inside the right component. The first component of an assembly is fixed (a rigid joint to the origin is better than «ground»).

## 7. Patterns and symmetries
The pattern seed fully constrained; distances and counts as parameters; **feature** patterns hold up better than sketch
patterns. Identical holes: a single hole command on several sketch points (see recipes).

## 8. Corrections in the timeline
A small correction that does not change the upstream logic can be made **at the end** (move a face, delete a face and redo the hole);
a correction that changes the logic must be made **in the original feature** (roll back in the timeline, edit, go back to the end).

## 9. Flexibility test (at the end of every part)
Change 2–4 key parameters to realistic values, recompute the expected values, measure; then restore the values. A Fusion error during the
test is a **useful signal** (it tells you what to fix); a wrong part without errors is the worst case, and it is exactly what the
test uncovers.

## 10. The work branches (where the request starts from)
| Branch | How to proceed | Recipes and tests |
|---|---|---|
| **From an idea** («can you make me a pen holder?») | 4 phases with a **stop** after each: (1) questions — what it is for, what it touches, what it endures, how it is made (printing only if they say so), overall size and style; (2) 2–3 quick concepts with images; (3) form: parameters, skeleton sketch, bodies, flexibility; (4) detail, minimum thickness, form analysis (fillets, stability) | `verifica.md` |
| **Recognizable object** (a product that exists, «make me a model of…») | agreed level of detail (envelope / recognizable / detailed; never lower it on your own), official images to scale, list of characteristic features shown with the questions, form before details, poor-form signs in the report. Applies **together** with the Assemblies branch if there are several parts | `forma-e-dettaglio.md` |
| **From a drawing** | read it zooming into the views; every dimension in a «used by» log (an unused dimension = missing element); ambiguous ones become questions | `ricette.md`, `ricette-solidi.md` |
| **From a photo** | a reference of known size is needed **on the same plane** (measured A4 sheet, credit card, ruler); skewed photo → straighten it first (`scripts/foto_prospettiva.py`), then canvas at true scale; error declared; critical dimensions from the caliper; without caliper, a test sample | `ricette-foto-tavole.md` |
| **From a file** STEP/STL/mesh | STEP: direct modeling; STL: with the Personal license (the most common for personal use) it converts only «faceted» (the «prismatic» method is refused) → **rebuild** from computed sections and fitted curves | `ricette-modificare-importare.md`, `ricette-stampi-mesh-pezzi.md` |
| **Editing** an existing project | find it in the projects list, reopen the latest version, change **one** parameter or feature at a time, save a new version | `modificare-importare-copiare.md` |
| **Architecture** (house, room) | metres, walls from sketch with thicknesses as parameters, openings as cuts, floor plan from DXF (DXF has no units: scale factor) or from an image as canvas; dimensioned drawing | `tavole-e-render.md`, `modificare-importare-copiare.md` (canvas to scale) |
| **Assemblies** and multi-file projects | several parts in the same space → first `progetti-a-piu-pezzi.md`; components before geometry, joints with limits, no interpenetration and clearances measured; skeleton in one file and **derived** parts: **geometry** propagates, derived parameters do not (re-check after every change) | `ricette-assiemi.md`, `ricette-stampi-mesh-pezzi.md` |
| **Production** (only if declared) | FDM printing → printing skill (`skill_stampa` in `impostazioni.json`); CNC → `ricette-cam.md`; sheet metal/laser → flat pattern and DXF; none → `.f3d` + STEP/images/drawing | `produzione-e-stampa.md` |
