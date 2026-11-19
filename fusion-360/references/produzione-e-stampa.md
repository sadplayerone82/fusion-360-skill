# Manufacturing: 3D printing, CNC, sheet metal and cutting (only if the user declares it)

Manufacturing is **not assumed**: ask how the part will be made (phase 1 of the method). If it will not be manufactured, deliver the `.f3d`
with STEP, images and the drawing if any.

## 0. Which branch
| Declared manufacturing | What to do | Where |
|---|---|---|
| **FDM printing** | printing decisions with a 3D printing skill, if installed (`skill_stampa` in `impostazioni.json`), **before** modeling; §1–5 below | — |
| **CNC** (mill, wood, aluminium) | stock, **real** tools from the manufacturer's data sheets (JSON), 2D/2.5D toolpaths, machine post-processor chosen by name, G-code checked (contour, tool radius, depth) | `ricette-cam.md` |
| **Sheet metal, laser/plasma cutting** | sheet metal component with the rule (thickness, radius, K), flat pattern measured against the formula π/2·(R + K·T) for a 90° bend, DXF of the flat pattern | `ricette-lamiera-form-costruzione.md` |
| **Mold / casting** | two-half mold with draft, keys, sprue and vents | `ricette-stampi-mesh-pezzi.md` |

If the printing skill is not installed: minimum rules (walls ≥ 2 nozzle lines, holes at nominal diameter, clearance 0.2–0.3 mm on the
radius for a sliding fit) and tell the user.

## 3D printing with the printing skill
A 3D printing skill (optional) knows materials, clearances, orientation, slicers; this skill knows how to model. If it is installed you
work together: it decides the printing numbers, you put them in the model as parameters. Printing questions are asked **only once**
(it asks them). If it is not there, the minimum rules above and the tables below apply, and missing numbers are asked of the user.

## 1. The contract (J1b, before modeling)
To ask the printing skill (or the user) and record in the specification, each with its source:
| Data | What it is for in the model |
|---|---|
| machine, nozzle, line width | wall thicknesses = multiples of the line (walls fragile below 2 lines) |
| material (PLA, PETG, ASA…) | clearances, snap hooks (allowed strain), heat resistance |
| **print orientation** | the model is drawn with Z = print Z; overhangs and bridges within limits; where horizontal holes go |
| clearances by fit type (sliding, press, lid) | model parameters `gioco_*` |
| hole rule | holes at **nominal diameter**: the slicer does the correction (`xy_hole_compensation`); only for a critical fit does the clearance become a parameter, saying so |
| heat-set inserts, screws in plastic, snap hooks | dimensions from the tables below (complete in `dati-standard.md`) or from the printing skill |
The snap hook is calculated with the formula in `ricette.md` §10 (thickness from the material's allowed strain).

## 2. Screws and holes (values as in Fusion, ISO standards; mm; complete tables in `dati-standard.md`)
ISO 273 clearance holes (close / **normal** / loose): M2 2.2/2.4/2.6 · M2.5 2.7/2.9/3.1 · **M3 3.2/3.4/3.6** · M4 4.3/4.5/4.8 ·
M5 5.3/5.5/5.8 · M6 6.4/6.6/7.0 · M8 8.4/9.0/10.0.
| Screw | Counterbore for socket head ISO 4762 (Ø × depth) | Countersink for flat head ISO 10642 (Ø, 90°) |
|---|---|---|
| M3 | 6.5 × 3.4 | 7.5 |
| M4 | 8 × 4.6 | 10 |
| M5 | 10 × 5.7 | 12.5 |
| M6 | 11 × 6.8 | 14.5 |
Tapped holes (tap drill, ISO): M2.5 2.05 · **M3 2.5** · M4 3.3 · M5 4.2 · M6 5.0 · M8 6.8 (Fusion: 6.75). In a printed part a metric
screw holds better in a **heat-set insert** than in the plastic.

## 3. Heat-set inserts (manufacturers CNC Kitchen and ruthex, for 3D printing: **straight** hole)
| Insert | Outer Ø | Hole | Hole depth | Length |
|---|---|---|---|---|
| M2 | 3.6 | 3.2 | 4.0–5.0 | 3.0–4.0 |
| M2.5 | 4.6 | 4.0 | 5.0–6.7 | 4.0–5.7 |
| **M3** | 4.6 | **4.0** | **6.7** | 5.7 |
| M4 | 6.3 | 5.7 / 5.6 | 9.1 | 8.1 |
| M5 | 7.1 | 6.5 / 6.4 | 10.5 | 9.5 |
Depth = length + 1; boss around the insert 1.5–1.7 × its outer diameter.

## 4. Export (J7)
- 3MF in mm (`createC3MFExportOptions`), one file even with several bodies; only the bodies to print visible.
- Check: `python -X utf8 scripts/controlla_mesh.py pezzo.3mf --atteso-mm X Y Z --atteso-volume-mm3 V` (measurements axis by axis).
- Then the slicer (or the printing skill, if installed) prepares the file for the printer. The print is always started by the user.
- STEP only if the part goes to someone who uses another CAD.

## 5. After printing (J10)
«It does not fit», «the holes are tight»: first measure with the caliper (3 readings) and go through the printing skill, if installed: often
the correction is in the slicer or in calibration. The model is changed only if it is a design clearance, in a **new version** of the `.f3d`.
