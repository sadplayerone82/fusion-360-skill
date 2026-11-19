# Changelog

Versions follow semantic versioning (major.minor.patch); the most recent is at the top.

## [1.1.1] — 2026-11-19

### Fixed
- Scripts: `-h`/`--help` (and `sonde.py` with no arguments) print the usage and exit with code 0 without touching Fusion
  (before, `spessore_minimo.py --help` started measuring and `sonde.py --help` crashed; same fix in 13 other command-line scripts).

## [1.1.0] — 2026-11-19
English version; Italian version moved to fusion-360-it.

### Changed
- The English skill is in the `fusion-360/` folder (skill name `fusion-360`); the Italian one is in `fusion-360-it/` (skill name
  `fusion-360-it`). Install only one of the two.
- `README.md`, `LICENSE`, `CHANGELOG.md` and `.gitignore` are at the repository root; the Italian README is `fusion-360-it/README.md`.
- Test cases (`evals/`): removed references to the private development bench; all numbers unchanged.

## [1.0.0] — 2026-11-18
First public version.

### Contents
- **SKILL.md**: the workflow from the environment to delivery, with a check at every step (environment, request and specification,
  manufacturing if declared, plan and expected values, project, modeling in measured steps, verification, flexibility, outputs, drawings and
  renders, delivery, resuming); the points where to stop and wait for the user; the traps that give wrong parts without errors.
- **References** (`references/`): connector and API with the measured traps; method and work branches; 19 usage scenarios; projects with
  several parts; form and detail for recognizable objects; verification; tested recipes by family (sketches, solids, surfaces,
  sheet metal, assemblies, import and modification, views and renders, decorations, molds and meshes, photos and drawings, CNC, free forms); list of
  Fusion commands with API and availability in the Personal license; standard data (threads, clearance holes, screws, inserts,
  bearings); limits of the Personal license.
- **Scripts** (`scripts/`): check of the environment and of the MCP tools; settings outside the skill; connection to the MCP server;
  local projects in measured steps with project log and resuming; model report; probe points; interferences and clearances in assemblies;
  minimum thickness; poor-form signs; stability analysis; check of 3MF files; check of G-code; perspective photos and
  measurements from photos; symbols for drawings; reading Fusion's logs.
- **Templates** (`assets/`): specification and report.
- **Test cases** (`evals/`): examples for those who develop the skill, with their format in `evals/LEGGIMI.md`.

### Tested
- Fusion build 2706.1.x, Personal license, Windows, Opus model (November 2026). Results in the «Validation» section of the README.
