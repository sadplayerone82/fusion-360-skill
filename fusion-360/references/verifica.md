# Verification: how a wrong part is uncovered

## Why
Fusion builds wrong parts **without errors**. Cases seen in the tests:
- Ø25 hole in a block 20 wide: the circle splits the profile in two and the extrude keeps **half** (1 801.1 mm³ instead of 3 602.2);
- fillet larger than the thickness: built anyway, faces eaten away;
- rib with the default direction: it grows **outside** the part (11 272 mm³ instead of 9 300);
- joint with the default settings: the part flips **inside** the other (interference 4 000 mm³).
None of these gives a message. Only the comparison with a value computed beforehand reveals them.

## 1. Expected values, before modeling
- **Volume after every step**, with simple formulas: blocks, cylinders (π r² h), rings, fillets (area (1 − π/4)·r² times length;
  around a cylinder with Pappus's theorem), chamfers (triangles), cones (π h/3 (R² + Rr + r²)), envelopes of circles (sectors +
  tangents). When a shape is complicated, compute in **two different ways** (formula and dense polygon) and compare them.
- **Bounding box** (x, y, z), **positions** of the holes and of the features that matter, number of bodies.
- Write them in the specification (`assets/specifica.md`): they are the yardstick you check every step against.

## 2. After every step (`progetto_locale.Progetto.passo`)
Measure volume, bodies, timeline elements, elements in error; compare with the expected value. Tolerances: dimensions **0.01 mm**, model
volume **0.01 %**, exported mesh volume **0.1 %**.
If it does not match: **find the cause by measuring** the geometry (radii and dimensions of cylindrical faces, bounding boxes). In the tests once
the calculation was wrong (the counterbore went past the edge of the base), another time the reading of the drawing (a chamfer that would have pierced the
wall). Fix what is really wrong; do not bend the model to the number.

## 3. Model report (`scripts/rapporto_modello.py`)
It gives: document type and units; parameters; timeline elements in error (with the message); sketches not fully constrained;
for each body: solid, visible, volume, bounding box (`dimensioni_mm`), faces, material, mass. The gate: **0 elements in error,
0 free sketches**, all bodies solid and visible, measurements = expected values. The report really finds an element in error (tested: base
sketch deleted → the extrude shows as in error with Fusion's message).

## 4. Assemblies
After every joint and at the end: interference between pairs of components (`analyzeInterference`) = 0, except the intended and declared ones;
position of the bodies against the expected. **It is not enough**: 0 only says the parts do not interpenetrate, they may touch. Where space is needed,
measure the clearance of each pair (`references/progetti-a-piu-pezzi.md` §3).

## 5. Looking at the part
`viewport.fit()` and then two images (`iso-top-right` and `front`) with `fusion_mcp_read screenshot`. Really look at them and compare them with
the drawing or the request: the right number with the wrong shape happens (e.g. a mirrored part).

## 6. Files for printing
`python -X utf8 scripts/controlla_mesh.py pezzo.3mf --atteso-mm X Y Z --atteso-volume-mm3 V`: file exists, units, mesh closed and with
consistent normals, dimensions **axis by axis** (a rotated part does not pass, unless `--qualsiasi-orientamento`), volume. It applies the
3MF transforms. Exits with 1 if something is wrong.

## 6b. Checks in the same call
Every step script measures and compares **before finishing**: the script header (`mcp_fusion.corpo`) has
`controlla(corpo, volume=…, ingombro=[x, y, z], n_corpi=…)` in mm and mm³, tolerances 0.01 % and 0.01 mm (details in `ricette.md` §1).
The bounding box comes from the API `boundingBox`: on curved bodies it can be slightly large, so a bounding box failed by a few hundredths
is re-checked by measuring the true extremes before changing the model. If it does not match the script fails with
«CONTROLLO FALLITO: …» (= check failed) and **nothing of the step remains in the document** (tested: 0 bodies, 0 sketches, empty timeline; a document
created by the script itself instead stays open). The error shows in the same call: fewer calls = less time (in an external
project, 5 calls instead of 30 for the same part).

## 6b-bis. Probe points (`scripts/sonde.py`)
Volume, bounding box and centre of mass **do not see everything**. Tested on a flange with 4 holes: hole circle R 32 instead of R 30, or holes
rotated by 45°: volume, bounding box and centre of mass **identical** to the right ones; the probes fail them (8 mutants out of 8 caught, real flange
57 probes out of 57). Write the probes **before modeling**, from the specification: for each hole `{"nome", "centro", "diametro"}` (9 points, at mid
thickness), for each edge one point inside and one outside. Sensitivity is the margin: with 0.5 mm a Ø 9.4 hole instead of Ø 9 passes, with 0.1
it fails; tight dimensions are measured. A probe on a face comes out as «bordo» (= edge): that is the probe to move.

## 6b-ter. CNC programs (`scripts/verifica_gcode.py`)
It checks G21/G90, spindle, feed rate, **depth**, that the cutter does not bite the part and **does not pass inside the part** (contour on the
wrong side: the distance from the edge is the same inside and outside, so only this check sees it), that **every contour** (outer,
each hole) is machined, rapids below the top. Tested: 9 ruined programs out of 9 failed, each with the right reason, plus 2 real programs
with the wrong side (Ø 8 holes machined from outside, plate 146 × 96), failed. `dx`, `dy` = CAM origin
(stock +10 per side with origin on the corner: 10, 10). It does not simulate material removal or tool-holder collisions: say so.

## 6c. Minimum thickness and form (before every delivery)
- `python -X utf8 scripts/spessore_minimo.py --limite <mm>` measures for every body the minimum distance between opposite faces; below the
  limit it says «FERMARE LA CONSEGNA» (= stop the delivery). The limit is **always chosen** according to production and passed with `--limite` (do not rely on the
  script's default value): 3D printing: 2 nozzle lines (e.g. 0.8 with a 0.4 nozzle); wood/CNC:
  from the material; without production, only for viewing or rendering: `--limite 1`, and decorative details below the limit are declared.
  It is mandatory: in a real project the most serious defect (a part too thin) had been seen by the user, not by the other checks. Limit: it does not measure rounded sharp tips. In assemblies it measures one body per
  call and repeated bodies only once (`occorrenze`, `secondi_per_pezzo`); a thin purchased part (a 0.64 pin)
  triggers the limit: it is explained in the report, not hidden.
- `python -X utf8 scripts/analisi_forma.py [--carico m,x,y,z]`: edge continuity (G0/G1/G2), fillet radii, **stability**
  (centre of mass, support base, tipping margin and angle). For objects that rest on a surface or carry a load (supports, holders).
  For **recognizable objects** the share of sharp edges (G0 over the total) is one of the poor-form signs: `forma-e-dettaglio.md` §4.

## 6d. Verification ladder (what to say in the report)
For each check, the highest level reached: **call returned** → **exists** (body, file) → **geometry** (measurements = expected) →
**round trip** (file reopened/reimported and remeasured). And the list of **what was not verified**, with why. An «ok»
answer from Fusion is not proof: it is the first rung.

## 7. Flexibility and report
Flexibility test (`metodo.md` §9) and final report: what you checked, **with which number**, where; what you did not check.
Never «everything is fine» without this list.
