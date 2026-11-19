# What Fusion is used for: the 19 scenarios and how the skill covers them

From the official Autodesk sources on the uses of Fusion, checked one by one (November 2026). For each scenario:
the branch of the method (`metodo.md` §10), where the tested recipes are, and the limits to tell the user.

| # | Scenario | Branch | Recipes | Limits to tell |
|---|---|---|---|---|
| 1 | Mechanical parts from a drawing (brackets, flanges, shafts) | drawing | `ricette.md`, `ricette-solidi.md`, `tavole-e-render.md` | GD&T symbols and hole table as images |
| 2 | Design from an idea | idea | `metodo.md` §10, `verifica.md` §6c | — |
| 3 | Consumer products, design objects | idea / recognizable object | **`forma-e-dettaglio.md`**, `ricette-superfici-forme-lamiera.md`, `ricette-decori-anelli.md`, `ricette-lamiera-form-costruzione.md` | T-spline: only primitives via API |
| 4 | Enclosures for electronics | drawing / idea | `ricette.md` (snap hooks, shells, holes) | — |
| 5 | Assemblies and mechanisms | assemblies | `ricette-assiemi.md`, `ricette-stampi-mesh-pezzi.md` (derive) | derived parameters do not update; assembly constraints and contacts not tested |
| 6 | Architecture and interiors | architecture | `tavole-e-render.md`; sketches/extrudes in metres | no BIM: only geometry towards Revit and similar |
| 7 | Furniture and woodworking | idea / CNC | bodies = panels; `ricette-cam.md` | cut list from a script (BOM is paid) |
| 8 | Sheet metal and 2D cutting | manufacturing | `ricette-lamiera-form-costruzione.md` | after «Refold» the part may end up rotated: re-check |
| 9 | CNC machining | manufacturing | `ricette-cam.md` | slowed rapids (Personal license) |
| 10 | 3D printing | manufacturing | `produzione-e-stampa.md` + printing skill | — |
| 11 | Molds (silicone, casting) | manufacturing | `ricette-stampi-mesh-pezzi.md` | — |
| 12 | Jewelry (rings, pendants) | idea | `ricette-decori-anelli.md` (ISO 8653 size: Ø = size/π) | national sizes only from a table actually read |
| 13 | Cosplay and sculpted objects | idea / file | splitting into parts and mesh in `ricette-stampi-mesh-pezzi.md` | Form from sketch has no API |
| 14 | Spare parts, reverse engineering | photo / file | `ricette-foto-tavole.md` (perspective), mesh → solid | a measured reference is needed in the photo |
| 15 | Editing other people's files (STEP, STL) | file / edit | `ricette-modificare-importare.md`, `ricette-stampi-mesh-pezzi.md` | STL: only «faceted» with the Personal license («prismatic» is refused) |
| 16 | Presentation (renders, exploded views, videos) | — | `tavole-e-render.md` | local render only; exploded view and video from the UI |
| 17 | 2D drawings | drawing | `tavole-e-render.md`, `ricette-foto-tavole.md` | 2 documents in the cloud; objects cannot be deleted via API |
| 18 | Electronics and PCB | — | outside this skill | — |
| 19 | Simulation, generative design | — | not available with the Personal license (not tested with the others) | hand calculations, declared |
