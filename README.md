🇮🇹 Versione italiana: [fusion-360-it/README.md](fusion-360-it/README.md)

# fusion-360 — skill for Claude Code

This skill makes Claude work in **Autodesk Fusion** like a CAD designer: from the request to a **checked parametric model**,
saved as an `.f3d` file on the PC, with a report that says what was verified and what was not.

The repository contains two versions of the same skill:
- `fusion-360/` — **English** (skill name `fusion-360`);
- `fusion-360-it/` — **Italian** (skill name `fusion-360-it`, instructions in [fusion-360-it/README.md](fusion-360-it/README.md)).

**Install only one of the two**: they do the same thing and must not be installed together.
File names, script names and script outputs are kept in Italian so both versions stay in sync.

The skill is **not affiliated with Autodesk** nor endorsed by Autodesk. «Autodesk» and «Fusion» are trademarks of their respective owners.

## What it does
- **Models** mechanical parts, enclosures for electronic boards, objects born from an idea, recognizable products, furniture and rooms,
  jewelry, molds, sheet metal, moving **assemblies** (joints).
- **Starts from** a verbal request, a dimensioned drawing (image or PDF), photos, a STEP, STL or DXF file, or an existing project
  to modify.
- **Works in measured steps**: for every step it first computes the expected value (volume, bounding box, positions) and compares it with the one
  measured in Fusion. If a number does not match it looks for the cause instead of going on.
- **Asks** for the missing dimensions instead of inventing them, and stops to wait for the answers.
- **Delivers** the `.f3d` (new version, never overwritten), the outputs needed (STEP, 3MF, DXF, checked CNC G-code, PDF
  drawing, images) and a `resoconto.md` (report).
- **Respects the Personal license**: it knows which features are paid (`fusion-360/references/limiti-personal.md`), buys nothing, uses no
  credits and saves to the cloud only with your permission.

**Who it is for**: people who use Fusion and want Claude to build the model (or a modification) with real checks; also for people who are not
CAD designers and describe the object in words.

**What it does NOT do**
- It does not work without Fusion open on the PC and without its MCP server: it is not a CAD program of its own.
- It does no slicing for 3D printing, no electrical schematics and no printed circuit boards.
- It is not meant for other CAD programs (Rhino, FreeCAD, Blender, OpenSCAD…).
- It does not guarantee that a manufactured part works: the report says how far verification went; tests and measurements on the real part
  are up to you.

## An example
Request, in Claude Code with Fusion open:

> can you make me a 60 × 40 × 5 plate in Fusion with two 6 mm holes 8 mm from the short edges?

What happens:
1. Claude checks that Fusion and the MCP server respond.
2. It asks the questions it needs (for example: through holes? centered on the 40 mm side? how will the part be made?) and **waits**.
3. It writes the specification and the expected values: solid volume 60 × 40 × 5 = 12 000 mm³; each Ø 6 through hole removes π × 3² × 5 ≈ 141.4 mm³,
   so the finished part measures ≈ 11 717.3 mm³.
4. It creates the project folder and models in steps (sketch, extrude, holes), measuring after every step.
5. Verification: constrained sketches, no elements in error, hole positions, minimum thickness; then it changes the main parameters to
   see that the model stays correct, and puts them back as they were.
6. Delivery, in the project folder: `consegna\piastra-v1.f3d`, STEP, two images (iso and front), `resoconto.md` with the table
   «expected / measured / result» and the list of what was not checked.

Other typical requests:
- «here is the drawing (PDF): rebuild the part in Fusion» → reads the dimensions, asks for the missing ones, compares the volume.
- «I have this STEP, make it parametric» → rebuilds the part and compares the form with the STEP.
- «make me a model of mouse X, recognizable» → first agrees on the level of detail and wants reference images to scale.
- «I need a holder for this board, with the board inside» → assembly with the board as a component, measured clearances, no
  interpenetration.

## Requirements
| What | Version | Notes |
|---|---|---|
| Windows | 10 or 11 | Fusion startup, dialogs and logs are written for Windows. Not tested on macOS. |
| Autodesk Fusion | recent, with the **official MCP server** | Tested with builds 2706.1.x (October–November 2026). The server is turned on in Preferences → General → API. Fusion updates itself: see «Troubleshooting». |
| Fusion license | Personal is fine | The skill avoids paid features. With Personal the cloud has 10 slots: the skill saves projects as `.f3d` files on the PC; only 2D drawings use 2 cloud documents, and only with your permission. |
| Python | **3.11 or newer** | Required by scipy 1.16. Packages in `fusion-360/scripts/requirements.txt` (numpy, Pillow, scipy). |
| Claude Code | recent | Tested with the Opus model; not tested with smaller models. |
| git | optional | If present, every project has its own local history (nothing is sent over the network). |
| A 3D printing skill | optional | Used only if you declare that the part will be FDM printed. Not included: without it, the skill applies the minimum rules of `fusion-360/references/produzione-e-stampa.md`. |

## Installation
Commands are written in two versions: **PowerShell** (`$env:USERPROFILE`) and **Command Prompt, cmd** (`%USERPROFILE%`).
Use the one that matches the window you opened.

**1. Download the repository** («Code» button → «Download ZIP» and extract, or `git clone`).

**2. Copy the skill folder `fusion-360` into the Claude Code skills folder**, **without** its `evals/` folder (it contains test
cases for people who develop the skill: Claude does not need them). Run the command **from the downloaded repository folder, the one
that contains `README.md`, `fusion-360` and `fusion-360-it`**:

PowerShell:
```powershell
robocopy fusion-360 "$env:USERPROFILE\.claude\skills\fusion-360" /E /XD evals __pycache__
```
cmd:
```bat
robocopy fusion-360 "%USERPROFILE%\.claude\skills\fusion-360" /E /XD evals __pycache__
```
Do **not** also copy `fusion-360-it`: install only one of the two versions (for the Italian one follow
[fusion-360-it/README.md](fusion-360-it/README.md)). If you previously installed the other version, delete its folder
(`.claude\skills\fusion-360-it`) first.
robocopy ends with a summary; exit codes from 0 to 7 mean «succeeded».

**3. Turn on the MCP server in Fusion**: Preferences → General → API → enable the Fusion MCP server. It runs only on your PC, on
port 27182.

**4. Connect Claude Code to the server** (same command in PowerShell and in cmd):
```
claude mcp add --transport http --scope user autodesk-fusion http://127.0.0.1:27182/mcp
```
Then restart Claude Code. `claude mcp list` must show `autodesk-fusion`.

**5. Go into the installed skill folder** (the following steps are all run from here):

PowerShell:
```powershell
cd "$env:USERPROFILE\.claude\skills\fusion-360"
```
cmd:
```bat
cd /d "%USERPROFILE%\.claude\skills\fusion-360"
```

**6. Install the Python packages** (first check with `python --version` that it is 3.11 or newer; if `python` is missing, try `py`):
```
python -m pip install -r scripts\requirements.txt
```

**7. Create the settings**, that is the folder where the projects will go:

PowerShell:
```powershell
python -X utf8 scripts\impostazioni.py --crea --cartella-progetti "$env:USERPROFILE\Documents\Progetti-Fusion"
```
cmd:
```bat
python -X utf8 scripts\impostazioni.py --crea --cartella-progetti "%USERPROFILE%\Documents\Progetti-Fusion"
```
The file is called `impostazioni.json` and lives in `.claude\fusion-360\` inside your user folder, **outside** the skill: a
reinstall does not delete it. `python -X utf8 scripts\impostazioni.py --mostra` shows it. If you do not have a 3D printing skill,
open it with a text editor and set `"skill_stampa": null`.

**8. Check the environment**, with Fusion open:
```
python -X utf8 scripts\ambiente.py
```
It must answer `"si_puo_lavorare": true` (= work can start). The first time it warns that the tool list is missing: this is normal, see step 9.

**9. Once only, with Fusion open**, save the MCP server's tool list. It is used to notice, after a Fusion update,
whether the tools have changed:
```
python -X utf8 scripts\ambiente.py --salva-strumenti
```

`-X utf8` is needed: without it, on Windows accented letters break the scripts' output.

## First test
Open Fusion and, in Claude Code, write:

> can you make me a 60 × 40 × 5 plate in Fusion with two 6 mm holes 8 mm from the short edges?

What to expect: Claude asks the questions it needs and stops; after your answers it creates the project folder in the settings'
projects folder, models in steps measuring every step and delivers `.f3d`, images and `resoconto.md` (see «An example» above).
If the final volume is close to 11 717 mm³ (with Ø 6 through holes) and the report lists the checks made, the installation works.

## Troubleshooting
| What you see | What to do |
|---|---|
| `ambiente.py` says the MCP server does not respond | Fusion must be open, a single copy. Check Preferences → General → API (MCP server on, port 27182). Check `claude mcp list`. After adding the server, restart Claude Code. |
| The server responds but scripts do not start | Almost always Fusion has a dialog open that blocks commands. After a forced close Fusion restarts with the **«Recovered documents»** dialog: close it (Close) and try again. |
| Fusion «Not responding» during a long computation | On rich models (hundreds of sketches, texts, textures) an operation done on everything at once can freeze Fusion for tens of minutes. Wait: force-closing it loses the work since the last saved step. The skill knows it must work in groups: `fusion-360/references/connettore-e-api.md`, traps table, row «A call that never ends». |
| A 2D drawing command stays waiting | Fusion is waiting for a click: press Esc in Fusion and try again. |
| `ambiente.py` warns that the MCP tools have changed | Fusion updated itself and the server may behave differently: some recipes may no longer hold. Try a simple part (the plate); if it works, run `ambiente.py --salva-strumenti` again. If something breaks, open an issue (see «Contributing»). |
| Wrong accented letters or encoding errors | Run the scripts with `python -X utf8`. |

## Validation
The skill was tested in Fusion (Personal license, November 2026, Opus model), on real cases:
- **parts from dimensioned drawings**, that is technical drawings with dimensions, including missing dimensions to ask for;
- **parts from STEP files** from the public test cases of NIST (the US standards agency), comparing the form with the STEP;
- **assemblies** with joints (hinge, two-stage gear reducer) and **enclosures** for electronic boards (Raspberry Pi 4, Arduino Uno,
  ESP32), with the board inserted as a component;
- sheet metal, CNC with G-code, a room from a DXF floor plan, the modification of an STL, an object from an idea;
- **recognizable objects** (a mouse, a drone), judged by a person looking at the images next to the official ones.

Every case had values to check decided beforehand (volumes, bounding boxes, positions, number of components, no interpenetration,
constrained sketches, valid output files), measured on the delivered model.

Results, without embellishment:
- Cases used during development: 11 passed out of 11, with a single run per case. Compared with Claude without the skill:
  even on 4 simple cases; on the two-stage gear reducer 18 checks out of 18 with the skill and 12 out of 18 without (without the skill the model
  had no joints and did not move). A single run per condition: a hint, not statistical proof.
- First series of 11 new parts, at the first attempt: **8 passed out of 11**. Not passed: a ring from STEP (a dimension taken from the
  drawing instead of from the 3D), a board holder (feet inside the board) and a drone correct in the numbers but rejected on form
  («a box with bars»).
- After the corrections, second series:

  | Case | Result |
  |---|---|
  | Complex part from STEP (139 faces), at the first attempt | 11 checks out of 11, form identical to the STEP |
  | Ring from STEP + drawing, redone | 11 out of 11 (now asks which source prevails) |
  | ESP32 board holder, redone | 9 out of 9 |
  | Ergonomic mouse, never-seen object | 10 out of 10, **approved** by the person on the images |
  | Folding drone, redone | 12 out of 14, **not passed**: much better than the first, but mechanisms not engineered (hinges without end stops or detents, shells without interior, gimbal without motors, no exploded view) |

- After the drone the skill also asks for the **functional level** (appearance only or working: `fusion-360/references/forma-e-dettaglio.md`).
  This rule has not yet been tested with a new drone.

## Limits
- Correct numbers do not guarantee the form: for recognizable objects the final judgment belongs to whoever looks at the images.
- Realistic mechanisms (hinges with detents, interiors, motors) in complex objects: they are the weakest point (see the drone).
- 2D drawings: they need 2 cloud documents (with your permission) and some commands can freeze Fusion (the skill says how to get out).
- Free forms via script: tested with elliptical sections and traced outlines, loft, fillets and shell; T-spline only from primitives.
- Very rich models: some operations done all together freeze Fusion for minutes; the skill works in groups.
- Fusion in a language other than Italian has been tested little or not at all: some checks read command names.
- Tested only on Windows and only with the Opus model.
- Fusion changes with automatic updates: recipes and traps were measured on a specific version.
- Language: Claude answers in the user's language; file names, script names and script outputs are in Italian.

## License
MIT, full text in the [`LICENSE`](LICENSE) file.

Copyright (c) 2026 sadplayerone82

The third-party input files used in the `evals/` examples are not covered by this license: sources and terms are in
`fusion-360/evals/LEGGIMI.md` (and `fusion-360-it/evals/LEGGIMI.md`).

## Contributing
Reports and proposals are welcome, as repository «issues». For a problem attach, if you can:
- an example `.f3d` or STEP file that shows it (without confidential data);
- the skill's `resoconto.md` and, if present, the `registro.json` of the project folder;
- the output of `python -X utf8 scripts\ambiente.py` and, if Fusion froze, of `python -X utf8 scripts\registri.py dialogo`
  (the last lines of Fusion's logs);
- the Fusion version (Help → About) and the license type (Personal or commercial).

People who modify the skill find the test cases in `fusion-360/evals/` and `fusion-360-it/evals/` (see `evals/LEGGIMI.md` in each folder); a change
should be made in both versions. The changes of each version are in `CHANGELOG.md`.
