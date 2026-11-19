# Form recipes: curved and filleted parts via script (tested in November 2026)

For recognizable objects (`forma-e-dettaglio.md`). They show **how to go from the extrude to the form** while staying parametric:
constrained sections on parallel planes → loft → round bosses and cuts → fillets → shell. Same definitions as the other recipes (`r`, `d`,
`F`, `P`, `S`, `OP`, `vol`, `out`, `controlla`: the header of `ricette.md` §1). API lengths in cm.

Measured on the two parts below: arm 18 faces and 5.9 % sharp edges (an extruded bar: 8 faces, 100 %); shell 0 % sharp
edges, constant 1.5 mm wall. No warnings from `scripts/segni_forma.py`, 0 errors, all sketches constrained, parameter changes held.

## 1. A constrained elliptical section on a plane parallel to YZ
```python
def piano_x(espr, nome):
    pi = r.constructionPlanes.createInput(); pi.setByOffset(r.yZConstructionPlane, S(espr)); pl = r.constructionPlanes.add(pi); pl.name = nome
    return pl
def sezione(pl, x_cm, z_cm, ea, eb, ez, nome):      # ea, eb, ez = parameter names: semi-axes and height of the centre (ez None = on the axis)
    sk = r.sketches.add(pl); sk.name = nome
    c = sk.modelToSketchSpace(P(x_cm, 0, z_cm)); pa = sk.modelToSketchSpace(P(x_cm, 1.0, z_cm)); pb = sk.modelToSketchSpace(P(x_cm, 0, z_cm + 0.5))
    el = sk.sketchCurves.sketchEllipses.add(c, pa, pb)
    o = sk.project(r.originConstructionPoint).item(0)
    g = sk.geometricConstraints; dm = sk.sketchDimensions
    orizz = abs(pa.x - c.x) > abs(pa.y - c.y)        # is the model Y axis horizontal or vertical in THIS sketch? do not take it for granted
    (g.addHorizontal if orizz else g.addVertical)(el.majorAxisLine)
    if ez is None: g.addCoincident(el.centerSketchPoint, o)
    else:
        asse = sk.sketchCurves.sketchLines.addByTwoPoints(o, el.centerSketchPoint); asse.isConstruction = True
        (g.addVertical if orizz else g.addHorizontal)(asse)
        dm.addDistanceDimension(o, el.centerSketchPoint, adsk.fusion.DimensionOrientations.AlignedDimensionOrientation, P(c.x + 0.5, c.y + 0.5, 0)).parameter.expression = ez
    dm.addEllipseMajorRadiusDimension(el, P(c.x + 0.3, c.y + 0.3, 0)).parameter.expression = ea
    dm.addEllipseMinorRadiusDimension(el, P(c.x - 0.3, c.y - 0.3, 0)).parameter.expression = eb
    return sk                                        # sk.isFullyConstrained == True (tested on 7 sections)
```

## 2. Loft between the sections
```python
i = F.loftFeatures.createInput(OP.NewBodyFeatureOperation)
for sk in (s0, s1, s2): i.loftSections.add(sk.profiles.item(0))
lo = F.loftFeatures.add(i); lo.name = "LOFT_braccio"; b = lo.bodies.item(0)
```
- **Expected values**: if the semi-axes decrease linearly, the volume is the sum of the frustums between neighbouring sections,
  `V = π·h/6·(2·a1·b1 + 2·a2·b2 + a1·b2 + a2·b1)` (arm: 3 701.84 mm³ computed and measured). With sections that do not decrease
  linearly the loft is a smooth surface with no closed formula: declare a range.
- **The smooth loft bulges beyond the largest section**: shell with maximum section 52 × 48 → measured bounding box 54.8 × 50.6. If a
  bounding box is a constraint (manufacturer's dimensions), check it after the loft and correct the sections, not the number.
- Check `lo.healthState == 0`, the volume and an image: a loft can self-intersect without errors.

## 3. Joining round bosses (knuckle, seat) without leaving cusps
A round boss = constrained circle on a plane offset by half the height + extrude `JoinFeatureOperation`; the hole with `CutFeatureOperation`.
Two defects that **the numbers do not see** and the image does (found by looking at it, with 10/10 in the checks):
- section **as tall as the boss** → the loft comes out of the top face with a wedge fold: keep the section 1 mm lower;
- section **as wide as the boss** → cusp where the sides touch the cylinder: keep it narrower (13 on Ø 16).

## 4. Fillets chosen by geometry (never by index)
```python
b = r.bRepBodies.item(0); tipo = lambda f: f.geometry.objectType.split("::")[-1]
unione = adsk.core.ObjectCollection.create(); orli = adsk.core.ObjectCollection.create()
rf = d.userParameters.itemByName("D_foro").value / 2
for e in b.edges:
    if e.faces.count != 2: continue
    t = sorted(tipo(f) for f in e.faces)
    if any(tipo(f) == "Cylinder" and abs(f.geometry.radius - rf) < 1e-6 for f in e.faces): continue     # the hole edges stay sharp
    if "NurbsSurface" in t: unione.add(e)             # between the loft surface and a round boss
    elif t == ["Cylinder", "Plane"]: orli.add(e)      # rims of the round bosses
fi = F.filletFeatures.createInput()
fi.edgeSetInputs.addConstantRadiusEdgeSet(unione, S("R_unione"), True); fi.edgeSetInputs.addConstantRadiusEdgeSet(orli, S("R_bordo"), True)
fe = F.filletFeatures.add(fi)                          # then fe.healthState == 0 and volume
```
Large (junction) and small (rim) fillets in the same feature: tested with R2 and R1.

## 5. Hollow shell of constant thickness
```python
col = adsk.core.ObjectCollection.create(); col.add(r.bRepBodies.item(0))
si = F.shellFeatures.createInput(col, False); si.insideThickness = S("spessore_guscio")
sh = F.shellFeatures.add(si)                           # body with 2 closed shells (b.shells.count == 2)
```
Before the shell, fillet the rims of the flat caps (R6 tested). Expected values: volume between 85 and 100 % of «outer area × thickness»
(measured 26 975 mm³ out of 28 188, 95.7 %); `scripts/spessore_minimo.py` must give the shell thickness (1.5 measured).

## 6. Declared limits
- **Two parts** tested, with elliptical sections. Freeform sections (splines traced on an image), lofts with rails or centre
  line, stitched surfaces and edited T-splines are **not tested here**: for T-splines see `ricette-superfici-forme-lamiera.md`.
- A smooth shell is a form, not yet a recognizable product: the details (cuts, seats, vents) and the comparison with the
  references are missing, and they remain the job of `forma-e-dettaglio.md`.
- The code above is that of the two tests, merged: the `sezione` function combines the two variants (centre on the axis or raised)
  and the choice of the junction edges is written in the shortest form.
- Test results: arm 10 checks out of 10, shell 9 out of 9; the same bar made as a simple extrude gets all three
  warnings S1, S2, S3 from `scripts/segni_forma.py`.
