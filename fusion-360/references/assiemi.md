# Assemblies: parts that fit together or move

## When components are needed
If there are parts that move (hinges, arms, slides), that fit together (box and lid, support and board) or that are
printed separately, each part is a **component**, created **before** its geometry and with a name. Bodies are enough only for a
single part. The document must be hybrid or assembly (a «part» document refuses components).

## Creating and working inside a component
`occ = r.occurrences.addNewComponent(adsk.core.Matrix3D.create()); occ.component.name = "Coperchio"`; geometry is created with the
objects of the **component** (`occ.component.sketches`, `occ.component.features`); in the assembly context proxies are used
(`entita.createForAssemblyContext(occ)`).

## Joints (recipe in `ricette.md` §12)
- Types tested: **revolute** (hinges), **slider** (slides), **rigid**, rigid groups, «as-built» joints (parts already in
  position). Cylindrical, pin-slot, planar, ball: signatures known, not tested.
- The first component is fixed with a rigid joint to the origin (or «ground»).
- **After every joint**: body position = expected and no interpenetration. With the default settings a joint between the bottom face
  of one part and the top face of the other **flipped** the part inside the other without errors → `isFlipped = True`.
- Motion: set angle or travel and measure the transform. **Limits are set first** (enabling them resets the joint to 0); a
  value outside the limits is silently ignored: always read the value back.
- Check the motion in several positions (e.g. an arm folded and open): no interpenetration in each one, and the clearance measured.

## Linking the motion of two joints (gears, transmissions)
A pair of gears does not drive itself: the ratio is imposed with a motion link.
```python
i_ = r.motionLinks.createInput(giunto_pignone, giunto_ruota)
i_.valueOne = S("54 deg"); i_.valueTwo = S("18 deg")   # for an 18/54 pair: 54° of the first = 18° of the second
i_.isReversed = True                                   # external gears: opposite directions
m = r.motionLinks.add(i_)                              # then check m.healthState == 0
```
Tested with the Personal license: pinion at 30° → gear at −10°; chained links add up (exact 12:1 ratio) and stay in the `.f3d`.
Contact between teeth is **not** computed: you impose ratio and phase. Check in several positions, without `computeAll`, reading the
angles back (`connettore-e-api.md`). Prove that the check sees the teeth: suppress the link (`m.isSuppressed = True`) and move the pinion by half a pitch:
it must collide; then restore everything. For a gear with even z facing a pinion with a tooth on the axis, offset the gear by half a pitch (`fase = pi / z`).

## Purchased or reference parts (boards, screws, motors)
- Electronic boards: the manufacturer's official 3D model if it exists (STEP), otherwise a simplified block with the dimensions of the
  official drawing (bounding box, holes, connectors with their heights). It serves to check that the box does not touch anything.
- Even the model of a purchased part **must not have bodies one inside the other**: if you make board and pins as separate bodies,
  the board has the holes (or the pins start from its face), or the part is a single body. The interpenetration check
  is done on **all** bodies, including those of the same component (real case: 19 pins 0.64 × 0.64 through a
  1.6 board without holes = 12.452 mm³ of interpenetration, found by an automatic check and not by whoever had modeled it).
- Screws, nuts, washers: dimensions from the standards (`dati-standard.md`); cosmetic threads (not modeled in 3D) are enough for the checks.
- An external file is inserted as a linked component (`occurrences.addByInsert(dataFile, Matrix3D, True)`): it requires a file in the
  cloud, so prefer importing the STEP.

## Materials, masses, visibility
Materials by code (`ricette.md` §13); mass = volume × density, check it. Visibility: `isLightBulbOn`, isolation `isIsolated`.

## Measuring an assembly
Bounding box from the **bodies of the occurrences** (the occurrence bounding box gives zeros; bodies read from components are in the
component's coordinates, not the assembly's): `scripts/rapporto_modello.py` gives it in `assieme` (`ingombro_visibili`, `ingombro_tutti`,
`corpi_nascosti`; tested: 148 true, 154 from the components, 196 counting the hidden bodies). `scripts/spessore_minimo.py` measures
repeated bodies once and says how many occurrences they have. Interferences and minimum distance between **all** pairs; in the report the total
mass and the intended interferences (e.g. press-fit inserts) declared. Several parts in the same space: `progetti-a-piu-pezzi.md`.
