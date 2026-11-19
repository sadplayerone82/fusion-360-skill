# Form and level of detail: recognizable objects

Read it **before the questions** when the request is an object that exists or that must «look like» something: a branded product
(a drone, a phone, a home appliance), a vehicle, a design furniture piece, a character, an object to present. It is not needed
for brackets, flanges and boxy mechanical parts: there sharp edges are right.

**Why it exists**: an assembly can have perfect bounding boxes, joints and clearances and be a box with four bars. Real case: a
drone with all the right numbers, made of 22 extrudes out of 25 features, 81 % sharp edges and no freeform curved surface, could not
be recognized at a glance. The numbers in `verifica.md` do not see the form: the rules about it are here. The thresholds are
**warnings tuned on a single model**: the final judgement is the user's, on the images.

## 1. The three levels of detail
| Level | What you see | When |
|---|---|---|
| **1 Envelope** | blocks with the right dimensions | only if the user asks for «only the envelope» or «a placeholder» |
| **2 Recognizable** | the outline follows the references in the available views; curved surfaces where the object is curved; edges filleted as on the object; all the characteristic features | normal value for an object that exists |
| **3 Detailed** | in addition the secondary details: vents, sensors, screws, parting lines, lettering, buttons | the user says «detailed», «faithful», «realistic» |

- The level is **written in the specification** and confirmed with the user in the questions.
- **You do not lower the level on your own.** «Simplified shapes» is a question, never a choice: write what is lost («the arms
  will be straight bars, not tapered») and stop. A generic answer from the user («you decide») does **not** authorize lowering it.
- If time or tools are not enough for the requested level, say so **before** starting, not in the report.

## 1b. Products with mechanisms: appearance or function?
A real product (drone, gimbal, hinge, foldable) is not just an outline: a professional designer **engineers** the
moving parts. Example: a foldable drone with the right shape is not enough if it has arms on simple supports, with nothing that
governs opening, direction, locking open and closed; no exploded view; a solid shell instead of shells with the battery and the interior as separate
parts; gimbal without motors; mounts different from the original (there the gimbal motors sit in the shell extensions at its sides).
So, in the questions, ask **also for the functional level**, besides the level of detail:
| Functional level | What is modeled |
|---|---|
| **A Appearance** | shells and outer parts, joints only to move the view |
| **B Working** | every mechanism designed: hinge with pin, end stops, snap or detent in the use positions, opening direction; shells with thickness and junctions; main internal parts as separate parts (battery, motors, boards); motors where needed (gimbal); an **exploded view** of the assembly |
For a product with moving parts propose **B** and, if the user chooses A, write it in the report as a limit. Mounts are
copied from the original by looking at the references (where the motors are, how the hinge turns), not invented.

## 2. Before modeling
1. **References**: official manufacturer images in at least 2 views (side and top, or side and front) and the published dimensions.
   If you cannot get them, **ask for them**: without references level 2 is not promised. Third-party photos: only as a declared supplement.
2. **To scale**: every image as a canvas calibrated on a true dimension (`modificare-importare-copiare.md`, lines on the canvas;
   skewed photos: `ricette-foto-tavole.md`). A dimension read from the image remains a hypothesis, with its error.
3. **List of the characteristic features**: looking at the references, write in the specification what makes the object recognizable
   (example for a foldable drone: sloped nose, tapering arms, feet, sensors, air vents, battery bay,
   gimbal with its axes). Usually 6–12 items at level 2, more at 3. The list must be **shown to the user with the questions**.
4. **Proportions**: from the canvases derive the main ratios (length/height of the shell, position of the pins, tapers) and
   put them in the parameters; if an estimate is yours, declare it.

## 3. Order of work (from coarse to fine)
references to scale → volumes with the published dimensions → **form** → details → small fillets last.
- **Form** means: profiles traced on the canvases and joined with loft or sweep, revolves, large fillets, tapers: code
  tested in **`ricette-forma.md`** (constrained sections → loft → round bosses → fillets → shell; via script it works). For
  organic surfaces T-splines (`ricette-superfici-forme-lamiera.md`, `ricette-lamiera-form-costruzione.md`). Via API
  T-splines are driven with numbers (primitives, inserted edges, TSM description), not with manual «push and pull»: few faces,
  symmetry on, small changes.
- **Test first on a single part** (the most characteristic one): if loft or form fail, you find out right away. Lofts can
  self-intersect and the bounding box can lie: check volume and image at every step.
- **An extrude alone is not a form**: it is fine as a starting volume, not as a finished part of a curved object.
- At every phase an image **from the same view as the reference**, looked at next to the reference. Where you may stop
  (`SKILL.md`, «Where you stop and wait for the user»), show it to the user before the details.

## 4. Poor-form signs (warnings, to put in the report)
The first three are measured by `python -X utf8 scripts/segni_forma.py [--file modello.f3d]` (warnings S1, S2, S3; tested on a cube, a filleted
cube and the extruded-block drone described above).
| Sign | How it is measured | Warning |
|---|---|---|
| S1 Sharp edges | edges with the two faces at more than 1° / all edges | above 50 % |
| S2 Only extrudes | form features (loft, sweep, revolves, forms) + fillets and chamfers, per component | 0 in a component that is curved in the real object |
| S3 Few flat faces | faces of each body and share of flat area | below 12 faces **and** at least 50 % flat area (a smooth shell with 10 faces is fine) |
| Characteristic features | present / listed (§2.3) | below 100 % |
| Outline | image of the model next to the reference, same view | differences visible at a glance |

A warning is not a failure: it is **explained** («the motor is a cylinder in reality too») or corrected. Keeping quiet about it is not allowed.

## 5. In the report
Agreed level · references used (from where, which views) · list of characteristic features with done/not done ·
the signs of §4 with the numbers · images of the model next to the references · what is your estimate · what is missing for the level above.
