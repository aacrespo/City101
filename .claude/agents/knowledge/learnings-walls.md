# Walls Modeling Learnings

Techniques discovered while modeling. Updated by agents after each build round.

---

## 1. Boolean union works for multi-box wall courses
When building wall courses with openings (door/window gaps), constructing from multiple boxes and then `rs.BooleanUnion()` succeeded reliably. All 14 courses with openings (some with both door and window cuts) unified into single breps. This contradicts the playbook's warning that "boolean cutting is unreliable" — the key difference is we used **BooleanUnion** (additive, combining boxes into one shape) rather than **BooleanDifference** (subtractive, cutting holes). Additive booleans are far more reliable.

## 2. Boolean union leaves orphan input objects
`rs.BooleanUnion()` does NOT always consume its input objects. In courses 7-14 (the ones with both door and window cuts, built from 6 boxes each), 8 unnamed leftover breps remained on the layer after the union. Always scan for unnamed objects after boolean operations and delete them. The safe pattern: after union, check `rs.ObjectsByLayer()` for unnamed objects with bounding boxes matching the originals.

## 3. Monolithic ring technique (polyline + AddPlanarSrf + ExtrudeSurface) is reliable for simple rings
Courses 15-20 (no openings) used outer+inner polylines to create a planar surface with a hole, then extruded. All 6 succeeded without issues. This technique is the cleanest for courses without openings — produces true monolithic rings with no joints. Reserve the multi-box approach for courses that need opening cuts.

## 4. BooleanUnion result naming is unreliable — name AFTER union, not before
In Round 1, courses 7-14 were built by creating 5-6 boxes, naming the first one, then calling `BooleanUnion()`. The union returned a new object (the merged result) but the *original first input* survived as a separate named fragment (SE corner only). The result: each course appeared twice — one named fragment covering only part of the ring, and one unnamed full ring. **Fix:** never name input boxes before union. Instead: (1) create boxes, (2) union them, (3) name the union result, (4) scan for and delete any leftover unnamed inputs.

## 5. Render/plaster layers must account for openings — not just the structural courses
The initial build created render and plaster layers as solid rectangles covering the full wall face. This covered the door and window openings with a thin layer of material that shouldn't be there. Every finish layer (render, plaster, cladding) must be built with the same opening cutouts as the structural wall beneath it. Build them from multiple boxes around the opening, same as the courses.

## 6. Always verify bounding boxes after multi-part construction
The SE-corner-only bug in courses 7-14 was only caught because the review checked bounding boxes. A quick post-build verification — listing all objects with their bounding boxes and confirming each spans the expected dimensions — catches geometry bugs that look fine in a viewport but are structurally incomplete.

## 7. Gable infill is easily missed — reviewers catch what builders forget
Gable end walls (the triangular area between wall top and roof ridge) are a separate element from the rectangular wall courses. They sit above the wall plate line and fill the roof profile. Easy to forget because courses stop at the wall top and the roof agent handles everything above. The completeness reviewer correctly flagged this gap. Always treat gable infill as a walls responsibility, not a roof one.

## 8. rs.AddSrfPt() with 3 points creates clean triangular surfaces for gable infill
At LOG 300, a simple triangular surface per gable face is sufficient. `rs.AddSrfPt([(x, y1, z1), (x, y2, z1), (x, y_mid, z_peak)])` produces a clean planar surface. For LOG 400+, these should become solid prisms with wall thickness matching the structural walls below (40cm).
