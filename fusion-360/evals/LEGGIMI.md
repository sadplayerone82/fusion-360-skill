# Test cases (evals)

This folder is for **those who develop or modify the skill**: each subfolder is a test case, that is a realistic request
with the answers to give to Claude's questions and the values the delivered model must have. They are used to check that a
change to the skill does not make the results worse.

Claude does not need them during normal use: **do not copy it** into the skills folder (the README says how to exclude it).

## How a folder is made
| File | What it contains |
|---|---|
| `prompt.md` | The user's request, as they would write it. At the top, between two `---` lines, some indications for the run (maximum number of turns, maximum time in seconds, allowed tools). At the bottom, `Input files:` lists the input files. |
| `risposte.md` | The answers of the **simulated user**. They are given **only after** Claude has asked its questions, never together with the request: the case also checks that Claude asks for the missing dimensions instead of inventing them. They cover the foreseeable questions; for the others there is usually a line «for the rest decide yourself and declare it». |
| `attesi.json` | The values checked on the delivered model, for example volume and bounding box in mm³ and mm, center distances, minimum number of components, files to deliver. The keys change from case to case. |
| `case.yaml` | Name of the case and `expected_outcome`, that is the expected result described in words: what must be there and what is evaluated. |
| `place-files.sh` | Copies the content of `files/` into the working folder before the run (bash script; on Windows run it from Git Bash, or copy the files by hand). |
| `files/` | The input files: drawings, STEP, STL, DXF, PDF. It can be empty (request in words only) or to be filled by hand (see «Sources of the input files»). |
| `graders/` | Only in some cases: criteria to evaluate by reading the delivery and the report, one per file (for example «it asked for the fourth hole», «the standoffs form a 58 × 49 rectangle»). |

## How to run a case
**No automatic tools are included** to run the cases and evaluate them: they are done by hand.

1. Install the skill (see the README) and open Fusion.
2. Create an empty working folder and copy into it the content of the case's `files/` (or run `place-files.sh` from that folder).
3. Open Claude Code in the working folder and paste the text of `prompt.md`, without the header between the `---` lines.
4. When Claude asks its questions, answer with the content of `risposte.md`. If it asks something that is not there, answer as the
   case's user would and note it down.
5. At delivery compare the model with `attesi.json` (measurements in Claude's report, re-checked in Fusion), re-read
   `expected_outcome` in `case.yaml` and, if present, the criteria in `graders/`.
6. Note the result check by check, with the measured number; for recognizable objects the judgment on the form is given by a
   person looking at the images.

Some requests contain placeholders such as `<user's printer>`: replace them with a real printer before using them. The cases that
declare 3D printing work better with a printing skill installed (optional, not included). The cases of recognizable objects
ask for official product images in a `riferimenti/` folder: they are not included, they must be downloaded from the
manufacturer's website.

## Sources of the input files
The third-party files below **are not covered by the MIT license** of the skill.

### NIST — included
Cases `esame-09-nist-ftc11` (FTC 11) and `esame-09b-nist-ctc01` (CTC 01): STEP models and PDF drawings of the NIST test cases
(National Institute of Standards and Technology), project «MBE PMI Validation and Conformance Testing».
- Official page: https://www.nist.gov/ctl/smart-connected-systems-division/smart-connected-manufacturing-systems-group/mbe-pmi-0
- Work of the United States government: public domain in the USA. The page says that test cases, CAD models and STEP files
  can be used without restrictions, asks to cite NIST when they are used and specifies that the use does not imply an endorsement by NIST
  (the NIST logo must not be used).

### Raspberry Pi 4 Model B — not included
Case `scatola-raspberry-pi-4`: official mechanical drawing of the Raspberry Pi 4 Model B.
- Official page (Raspberry Pi Product Information Portal): https://pip.raspberrypi.com/categories/545
- File: https://pip-assets.raspberrypi.com/categories/545-raspberry-pi-4-model-b/documents/RP-008343-DS-1-raspberry-pi-4-mechanical-drawing.pdf
- Save it in `files/` with the name `raspberry-pi-4-meccanico.pdf`.

### Arduino Uno R3 — not included
Case `supporto-arduino-uno`: official datasheet of the Arduino UNO R3, code A000066.
- Official page: https://docs.arduino.cc/hardware/uno-rev3/
- File: https://docs.arduino.cc/resources/datasheets/A000066-datasheet.pdf
- Save it in `files/` with the name `arduino-uno-r3-datasheet.pdf`. The drawing is in the «Board Outline & Mounting Holes» section; in
  the most recent versions of the PDF it may be on a different page from the one cited in the request.

### Espressif ESP32-DevKitC V4 — not included
Case `esame-11-esp32`: official dimensions of the ESP32-DevKitC V4 board, in PDF and DXF.
- Official page (board guide, related documents section):
  https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
- Files: https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.pdf and
  https://dl.espressif.com/dl/schematics/esp32_devkitc_v4_dimensions.dxf (about 4 MB)
- Save them in `files/` with the same names: `esp32_devkitc_v4_dimensions.pdf` and `esp32_devkitc_v4_dimensions.dxf`.

**Before using one of these three cases**, download the files from the official pages and put them in the case's `files/` folder with the names
given: the request in `prompt.md` cites them with those names.

The other input files present in the folder (for example the STL, the DXF of the floor plan, the `.f3d` model) were created for
these cases and fall under the skill's license.
