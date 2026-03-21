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

## 9. BooleanUnion can return multiple objects — pick by bounding box volume, not index
`rs.BooleanUnion()` with 6 boxes (courses with door+window gaps) returns **2 objects**: `result[0]` is a small fragment (one input box that didn't merge), `result[1]` is the actual full ring. Using `result[0]` blindly gives you a single corner piece instead of the complete course. **Fix:** after union, select the result with the largest bounding box volume: `best = max(result, key=lambda o: bb_volume(o))`. Delete all other results. This supersedes the advice in learning #4 — the real bug wasn't about naming inputs vs results, it was about picking the wrong result object.

## 10. MCP `create_layer` with `::` names creates orphan top-level layers
Calling `rhino_create_layer(name="Cabin::Walls::Courses")` creates a new top-level layer with the literal name "Cabin::Walls::Courses" rather than creating a sublayer "Courses" under the existing "Cabin::Walls". If the nested layer already exists (created by another agent), the objects still land on the correct nested layer (via `rs.CurrentLayer()`), but the orphan empty layer persists as clutter. **Fix:** don't use `create_layer` for sublayers that may already exist. Use `rs.CurrentLayer("Cabin::Walls::Courses")` directly — it will find the existing layer. Only use `create_layer` when you're certain the layer doesn't exist yet.

## 11. Courses at lintel height need voids — not just at opening height
Courses that overlap with lintels (z-range intersection) need voids at the lintel position, even though the opening itself may have ended below. In cabin v2: door lintel z=240-260 required voids in Course 15 (z=240-255) AND Course 16 (z=255-270). Window lintel z=230-250 required a void in Course 15 only (Course 16 starts at z=255, above lintel top). Think of lintels as occupying wall volume just like openings do.

## 12. Render/plaster above openings must start at lintel TOP, not opening top
Render_South_AboveDoor initially started at z=240 (door opening top), but the door lintel occupies z=240-260. The render/plaster should start at z=260 (lintel top). Same logic applies to any finish layer above a window — it starts above the lintel, not above the opening.

## 13. Gable infill needs full assembly treatment — not just structure
At LOG 300+, gables should be solid prisms (40cm thick matching wall below), AND they need exterior render and interior plaster on their outward-facing surfaces. The initial build only created zero-thickness surfaces with no finish layers. Build gables as: (1) solid prism via AddSrfPt + ExtrudeSurface, (2) render prism on outer face, (3) plaster prism on inner face.

## 14. Interior plaster corner coverage depends on Y-range coordination
When building plaster as separate pieces per wall face, the Y-ranges must overlap at corners to avoid gaps. If south plaster runs x=40-460 and west plaster runs y=42-358, the 2cm×2cm corner column (40-42, 40-42) is uncovered. Fix: extend east/west plaster to y=40-360 (full inner cavity width) so they meet the south/north pieces at the corner.

## 15. Volume comparison is the fastest way to verify voids
Comparing actual volume against expected volume catches missing voids instantly:
- Full solid ring (500×400 - 420×320) × 15 = 984,000 cm³
- Ring with door gap (−90×40×15): 930,000
- Ring with door + window gaps: ~681,000
- Ring with lintel voids: varies (657,000 for Course 15, 906,000 for Course 16)
If the volume matches the solid ring formula, the void is missing. Faster and more reliable than visual inspection.

## 16. Point-in-brep test (rs.IsPointInSurface) is definitive for void verification
Place a test point at the center of where the void should be. If `rs.IsPointInSurface(brep, point)` returns True, the void is missing. Returns False means the void exists. Use this as the final check after any course rebuild. Test both a point that should be void (returns False) AND a point that should be solid (returns True) to catch degenerate geometry.
