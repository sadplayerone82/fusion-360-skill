# Fusion «Personal» license: what is there and what is not

This file applies to the **Personal** license (personal, non-commercial use: the most common for personal use). If you do not know
which license the user has, ask them or read it with `fusion_mcp_read` (`{"queryType": "licensing"}`). With the Personal license, check
here before proposing a function: proposing something that then does not work, or that costs money, wastes trust and time. With a
commercial license many of the limits below do not apply (not tested with this skill): tell the user when it matters.

## From the official Autodesk page (Personal / commercial comparison, read in October 2026)
In Personal the following are **limited**: CAM, electronics and PCB, **2D documentation and drawings**, **file types for import and export**;
data management is single-user. **Only in the paid version**: **automated** drawings and modeling,
**configurations**, **bill of materials (BOM)**, **cloud rendering**, cloud simulations.

## What was verified for real
| Function | Result with Personal |
|---|---|
| Solid modeling, surfaces, freeform, sheet metal (including flat pattern and DXF), assemblies and joints | works |
| AutoConstrain (automatic constraints) | **not available** («user is restricted») → the script writes the constraints |
| Sheet metal: bend-to-bend junction, overlapping corner closures | not available |
| Export 3MF, STEP, STL, `.f3d` archive; import STEP, STL, `.f3d` | works |
| **Local** render | works (free); the cloud one is paid |
| Automatic drawing | works but in a reduced version: only 3 overall dimensions; the other dimensions must be added or placed by the user |
| Documents in the cloud | **only 10** editable (files in the trash count until it is emptied) → projects are saved as `.f3d` on the PC |
| Mesh → «Prismatic» solid (cylinders and planes recognized) | **denied** («No rights for mesh conversion», tested); only «faceted» → rebuild from sections (`ricette-stampi-mesh-pezzi.md`) |
| CAM | works for 2–3 axes; **rapids are slowed** to the feed rate (written in the G-code) |
| Simulation, generative design | **not available** («upgrade to subscription», tested) → hand calculations, declared |
| Exploded view and AVI video (animation) | work from the UI, not from the API |
| BOM table and balloons in drawings | balloons have no API; BOM table only in the automatic drawing of an assembly |

## What has no API (done by hand or another way)
T-spline forms from sketch, bridge and repair (there are only primitives, edge insertion and TSM files); Solid primitives
(use sketch + extrude); component color cycling in the view; deleting or moving drawing objects.

## Rules that follow
- **Never** `purchase`; **never** `editImage` or `generatePowerpoint` (they consume credits) without an explicit request from the user.
- **Never save to the cloud** without permission: a cloud document takes one of the 10 slots. A 2D drawing takes **2 slots** (the
  design it comes from and the drawing itself, `tavole-e-render.md`): ask permission, reuse two test documents as new
  versions if you can, export the PDF; deletions in the cloud are done by the user.
- If a request needs a paid function (automatic BOM, configurations, cloud render), say so right away and propose
  the free alternative (table written in the report, variants as parameters, local render).
