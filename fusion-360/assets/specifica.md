# Specification — {{NOME}} ({{DATA}})

{{DESCRIZIONE}}

## 1. What it is for and what it mates with
<!-- function of the part; parts it is assembled with (screws, boards, other parts) with their dimensions and the source -->

## 2. Dimensions given or read (with the source of each)
| Dimension | Value | Source (user / drawing / standard / manufacturer / caliper) |
|---|---|---|

## 3. Intent (what stays true if the dimensions change)
<!-- one simple sentence, proposed to the user and confirmed: e.g. «the holes stay 12 mm from the edge even if you lengthen the bracket» -->

## 3b. Form and detail (only for recognizable objects: `references/forma-e-dettaglio.md`)
Agreed level: 1 envelope / 2 recognizable / 3 detailed — confirmed by the user: yes / no
References (where from, which views, dimension used for the scale): …
| Characteristic feature | Where it is seen in the reference | Done |
|---|---|---|
<!-- remove this section for mechanical parts -->

## 4. Questions for the user (before modeling) and answers
| Question | Claude's proposal (with the reason) | User's answer |
|---|---|---|
<!-- missing or ambiguous dimensions: NEVER invented. Stop until the user answers. -->

## 5. Manufacturing (only if declared by the user; otherwise write «none»: deliver .f3d, STEP, images)
How the part will be made: none / FDM printing / CNC / sheet metal or laser cutting / mold — `references/produzione-e-stampa.md` §0.
<!-- Only for FDM printing: decisions with the 3D printing skill, if installed (setting skill_stampa), or with the user -->
| Item | Value | Source |
|---|---|---|
| machine / nozzle / line width | | |
| material | | |
| orientation (model Z = print Z) | | |
| clearances of the fits | | |
| holes | nominal, correction in the slicer (except critical fits) | printing skill / user |
| inserts / screws / snap hooks | | |
<!-- For CNC, sheet metal, molds: machine, material, tools or bend rule, as in produzione-e-stampa.md §0; remove the rows not needed -->

## 5b. Accepted minimum thickness (for `scripts/spessore_minimo.py --limite`)
Limit: … mm — why (printing: 2 nozzle lines; CNC/wood: from the material; no manufacturing: 1 mm, decorative details declared)

## 6. User parameters of the model
| Name | Value | Comment |
|---|---|---|

## 7. Expected values (computed BEFORE modeling)
| Step | What is done | Expected volume (mm³) | How it is computed |
|---|---|---|---|
Expected final bounding box (x × y × z): …  ·  Positions to check: …
Tolerances: dimensions 0.01 mm · model volume 0.01 % · mesh volume 0.1 %.

## 8. Flexibility test
Parameters to change and recomputed expected values: …
