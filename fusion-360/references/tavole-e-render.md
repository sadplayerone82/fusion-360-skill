# 2D drawings, realistic images, animations (only if the user asks for them)

## 2D technical drawing — what works via API (tested)
- **Cloud**: the drawing is created from the design file **in the cloud** and the drawing itself is a cloud document → it takes **2 slots** (with
  the Personal license, the most common for personal use, there are 10 editable slots). Ask permission; better to reuse two test documents as **new versions** than to create more.
- **Creation**: `DrawingManager.createDrawingInput(dataFile, modo)`; the manual mode wants an `.f2t` template, the automatic one
  sometimes comes out **without views** (happened with a design made of a single imported component) → views are added with
  `sheet.views.createBaseViewInput()` + `views.add` (base views only; scale and style **after** creation). Sheet coordinates in
  **mm** (the help says cm: measured, they are mm).
- **Native dimensions**: `drawingDimensions.addLinearDimension(p1, p2, posizione)` and `addDiameterDimension(curva, posizione)` work;
  the view curves are found by geometry (`viewCurves`: `centerPoint` for circles and arcs — even a circle seen edge-on —,
  `midPoint` for lines). Units, decimals, comma and zeros are set in `documentSettings`.
- **Cannot be deleted or moved via API**: views, dimensions, symbols, images (`DrawingDimension` only has `type`). A mistake is removed
  **by hand** on screen (tell the user first), then put back correctly via API.
- **Native GD&T symbols and hole table**: unreliable (preview). The datum and the hole table hang for 600 s; the tolerance
  frame sometimes works, sometimes attaches wrongly. They are made as **images** (`sheet.images`, opaque, 58 mm wide × scale, positioned
  from the bottom-left corner) with values **computed from the view curves**, never written by hand: `scripts/tavola_simboli.py`
  (table, datum, frame; `--r-max` decides which circles are holes). Corrections are made by overlaying a correct image.
  `sheet.images` has no `count`: images are counted in the exported PDF (`page.get_images`). On a **reopened** drawing
  `view.scaleValue` gives an error: the scale must be passed (`--scala`), never assumed.
- Sheet sketch lines with close endpoints get joined in a zig-zag: for hatching and small marks, use images.
- Native custom tables do not show text; the title block accepts only name and position of the attributes.

## Drawing check (before saying «done»)
1. **What is missing**: list of what the drawing must have — overall sizes, diameters, thicknesses, holes (table or dimensions), datums and
   tolerances if requested, title block — ticked item by item.
2. **Readability**: no text under a line or over a border; two concentric diameters on different diagonals with text outside the
   part; text no smaller than the dimension text; tables scaled to the sheet.
3. **PDF looked at zoomed in**, zone by zone (`exportManager.createPDFExportOptions`): «pdf: true» is not enough.
4. Drawings are opened **visible** (opened hidden, a drawing hangs Fusion).

## Realistic images (render)
- **Local only** (cloud render is paid): `startLocalRender(file, camera)`, quality 25 for tests, 75 for the user;
  asynchronous → wait for the file to exist and check the resolution.
- Scene: `design.renderManager.sceneSettings` — the environment is chosen by assigning `backgroundEnvironment` (the background type is
  read-only and changes by itself; the environment can be read only with an environment background); ground and reflections with `isGroundDisplayed`,
  `isGroundReflections`.
- Appearance by **code** or by searching the «appearances» library (names are localized); assignable to the **occurrence** (bodies inherit it).

## Animations and exploded views
`d.animationManager.activateAnimationWorkspace()` → `storyboards.add()`; then go back to the design workspace. Exploded view and AVI video
work (also with the Personal license) but **from the UI** (tested on screen); they are not in the API: tell the user.
