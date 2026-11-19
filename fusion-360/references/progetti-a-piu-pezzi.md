# Multi-part projects: everything must fit, assemble and work

Read it when several parts share the same space: enclosures with electronics, machines, vehicles, shells, furniture with hardware.
It is not needed for a single part.

The risk: **every part is right and the whole does not work**. The model is valid, the volumes match, no errors, and then the battery does not
come out, the plug does not go in, the screw cannot be reached. No check on a single part finds it.

## 1. Before the geometry: the space budget
List **everything** that must fit in the volume: part, connectors, cables, room for fingers and for the tool. Use real dimensions: from the
manufacturer or from the user. If a dimension is missing, ask for it. Then add up, direction by direction, and write the sum in the specification:

```
Internal space = sum(size of the parts in a row) + sum(clearances) + cable space
Space for a cable = connector length + R + d/2,   with R = k × d
Space to remove a part = size of the part + 2 × clearance, along the whole exit path
External size = internal space + 2 × wall
```

- **The cable is a part.** A 60 mm battery with a 10 mm connector and a Ø 1.5 wire needs 61 mm without cable and about 81–87 mm with the
  cable in line. If the cable is not in the model, no check sees it: put it in as a solid, at least the section that comes out and the connector.
- **k** for cable bundles: ≥ 10 is the cautious value quoted by an industry source (not universal); the manufacturer's figure applies if there is one.
- **Plugs, tools, flying connectors**: the true dimension is the user's; if they cannot measure, assume a cautious value and **declare it**.
- **It does not fit?** Do not squeeze silently: say which part or which constraint prevents it and propose what to move.

## 2. The order of work
1. Space budget and layout **in numbers**, approved by the user, with images of the bounding boxes as simple blocks.
2. **One** form pass around the layout. If the form is not convincing, measure the proportions and check the layout first:
   it is often the cause, and redoing the surface does not change it.
3. Seats, fasteners, openings. Details last.
4. **Re-read the specification before every phase.** Decisions taken are constraints: if a number pushes to change one, say so and ask.

## 3. Clearances: «interference 0» is not enough
| Result | What it really means |
|---|---|
| No interference | the parts do not interpenetrate; they may **touch** (faces in contact are excluded, unless requested) |
| Zero volume, with coincident faces included | they touch |
| Positive volume | real collision, or intended overlap: declare it |
| **Minimum distance ≥ decided clearance** | **this is the criterion** |

- The clearance is **decided** and written in the specification. For FDM printing 0.5 mm is a starting point for assembly, not a
  universal value (the printing skill gives the details).
- Intended contacts (board on the standoffs, screw in its seat) are exceptions **declared one by one**.
- Measure each pair with `app.measureManager.measureMinimumDistance(a, b)`, also between bodies: it gives the distance and the two points, i.e. where to look.
- `d.createInterferenceInput(corpi)` with `areCoincidentFacesIncluded = True`: contacts come out with volume 0, collisions with their volume
  (`x.interferenceBody.volume`). Tested in a parametric design. Do not use `createBodies`: according to the official example it only works in direct modeling.

## 4. Checking all pairs
After every feature that touches a part, and at the end: **all pairs**, not only those you think touch (n parts = n(n−1)/2 pairs;
7 parts = 21). The most common defect is in a pair you had not thought of.

```
python -X utf8 scripts/controlla_pezzi.py --franco 1 --appoggi "*/albero*:*/ruota*,cuscinetto*:guscio*" [--giunto NOME --angoli 0,30,90]
```
It gives collisions (with volume and point), contacts and clearances below the limit (with the two points); OK only if every contact or small clearance is declared.
Declare only what is intended: shaft in the hole, bearing in its seat, screw on the flange, **meshing gears** (the backlash between teeth is ~0.1 mm).
With `--giunto` it tests the mechanism in several positions. On a 31-body gearbox: about 1 minute per position.

## 5. Assembly, written down
Write the sequence in the specification, step by step, and for each step check:
- **In and out**: does the part have a straight-line path, with the clearance along the whole travel, without having to disassemble what must not
  be disassembled? Test it with temporary copies, without touching the model: `t = adsk.fusion.TemporaryBRepManager.get()`, `cb = t.copy(pezzo)`,
  `cs = t.copy(altro)`, `t.transform(cb, M)`, `t.booleanOperation(cb, cs, adsk.fusion.BooleanTypes.IntersectionBooleanType)`; a volume greater
  than 0 is a collision (`cb.volume` only if `cb.faces.count` is not 0). Repeat in steps along the whole travel.
- **Tool**: for each screw, along its axis, is there room for the tool with the hand and for the screw head? A seat is designed
  together with the access, not just the hole.
- **Use**: can ports and buttons be reached with the object closed, with the real plug and not only with the board connector? Can what is changed
  often be reached without tools or with few screws?
- **Convenience rules** (from assembly literature, secondary source): assemble along one axis, generally from above; a part is
  located before it is let go; avoid turning the assembly over halfway; few screw types; where possible, snap fits instead of screws.

## 6. Printability part by part
If it is printed, each part has its orientation, decided **while you model it**: overhangs, bridges, suspended floors, holes on the edge of a
standoff, and what touches the bed. The rules belong to the printing skill. What goes below the resting plane of a part often has to be separated.

## 7. Looking up close
Numbers confirm, they do not replace: a hole that breaks out of its edge is valid geometry, and passes volume, interference and probes.
- After every detail, a **close-up image of that detail**: in the overall view a 1 mm defect cannot be seen.
- **Section views** for cavities: hide the bodies that cover them.
- **Identical copies** (4 arms, 4 feet): compare 2 images with each other, the difference jumps out.
- Show the images to the user **together** with the numbers: the form can only be judged there.

## 8. If a zone is tangled in the timeline
A change that breaks distant features is not patched over and over, and the whole project is not redone:
measure the existing geometry, agree on what is redone, rebuild **only that zone**. Then repeat §3 and §4.

## 9. What to say at delivery
Besides the normal report: the space budget, the table of pairs with the minimum distance and the declared exceptions, the
assembly sequence with what was checked by calculation. **None of this replaces real assembly**: say so.
Cable bending, forces on fasteners and strength are not covered by these checks.
