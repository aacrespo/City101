# Review Modeling Learnings

Techniques discovered while reviewing Rhino models built by agent teams. Updated after each build.

---

## Cabin v2 — Rammed Earth (2026-03-21)

### 1. Bounding boxes are necessary but not sufficient
Bounding boxes from `rhino_get_objects` show the outer extent of an object but cannot reveal voids (boolean cuts for doors/windows). A course with a door opening and a solid course have the same bbox. Volume analysis or face-count checks are needed to confirm voids exist. Don't flag an opening as missing based on bbox alone.

### 2. Always re-query after fixes — never assume
When a builder agent reports "fixed", always re-query the specific objects to verify: (a) new GUIDs (confirming old objects were deleted and new ones created), (b) changed geometry (bbox dimensions, z-values), (c) object count unchanged (no orphans left behind). Trust the data, not the report.

### 3. The section test is the gold standard
The most effective review technique: mentally trace a clipping plane through the model and read the section bottom-to-top. Every layer should be present in the right order with credible thicknesses. This catches things constraint tables miss — like a missing DPC, render/plaster that collides with a lintel, or gables without finish layers.

### 4. Object count tracking across rounds
Track total object count at each round boundary. It should change only by the exact number of objects added/removed in approved fixes. Count jumps signal orphans (old objects not deleted) or unintended additions. In this build: 78 -> 78 (Round 1-2, rebuilds were clean) -> 87 (Round 3, +9 intentional additions).

### 5. Viewport captures have token limits
Large perspective and right-side viewport captures can exceed response token limits. Front and Top views are typically smaller and more reliable. When captures fail, fall back to comprehensive bbox analysis — it's slower but complete.

### 6. Review the interfaces, not just the elements
The most valuable review checks are at interfaces between systems: wall-to-plinth (DPC present?), lintel-to-render (collision?), sill-plate-to-wall-top (z alignment?), gable-to-roof-slope (finish layers continuous?). Single-system checks (wall thickness, course count) are easy to pass — interface checks find the real problems.

### 7. Distinguish functional from cosmetic early
Round 1 proposals should focus exclusively on functional issues (structural, waterproofing, load path). Cosmetic issues (naming, corner overlaps, layer naming convention) can wait until later rounds. In this build, the critical Round 1 fix was courses 07-14 (structural), while gable naming (cosmetic) was correctly deferred.

### 8. DPC and finish layers are easy to forget
Thin elements that sit between systems — DPC at wall-plinth interface, lime screed on slab — are the most commonly omitted. They don't show up in a constraint table but are instantly visible in section. Always check for these explicitly.

### 9. Lintel collision with finish layers
When a lintel occupies a z-range (e.g., z=240-260), the render and plaster above the opening must start at lintel top (z=260), not at the opening top (z=240). This collision was caught in Round 3 — it's a subtle interface issue between the openings agent and the walls agent.

### 10. Improvement rounds have diminishing returns
Round 1: critical structural fix (courses). Round 2: geometry fix (gables). Round 3: assembly completion (DPC, gable finishes, lintel collision). Round 4: no functional issues found. The pattern is clear — functional issues concentrate in early rounds. By Round 3-4, proposals shift to cosmetic, which is the signal to stop.

---

## Cabin v3 — Stone + Timber (2026-03-22)

### 11. Search by material metadata, not object name
Roof assembly objects were all unnamed, so searching for "blocking" or "vapour" by name returned zero hits — a false negative. Querying `rs.GetUserText(obj, "material")` found all 24 inter-rafter blocking objects (`mineral_wool_blocking`) and the PE membrane vapour barrier. Always search by material metadata as a fallback when names are absent.

### 12. Rafter z-bottom below wall plate is normal for eave overhang
Half-span rafters with overhang will have their lowest z well below the wall plate top. In this build: wall plate top z=567.5, rafter bottom z=511.5 — a 56cm drop from the 60cm overhang at ~38 degrees. This is geometrically correct (eave tail). Don't flag it as a misalignment.

### 13. Object count inflation from assembly modeling
Cabin v3 spec said 664 objects; actual count was 721 (+57). This happens when builders model more assembly layers than initially estimated (e.g., 68 fire stops vs expected ~20, extra reveal insulation objects). Not a problem — it means assemblies are more detailed than planned, not that orphans exist. Cross-check by layer, not just total.

### 14. Unnamed objects are a minor but persistent issue
31 roof structure objects (all rafters + ridge beam) and 62 roof assembly objects had no `rs.ObjectName`. Material metadata was present on all, so functional review was unaffected. But naming helps debugging and spec sheets. Flag as MINOR, not blocking.

### 15. Viewport captures at 800x600 routinely exceed token limits
All four viewport captures (Front, Right, Top, Perspective) exceeded the inline token limit and had to be saved to disk then read as images. This is consistent with learning #5 from v2. For future reviews: either reduce resolution (400x300) or plan to read from disk. The disk-read approach works reliably.

### 16. Account for every object in the delta
When re-reviewing after an improvement round, compute the exact object delta and trace every new object to a specific improvement task. In this build: 721 -> 850 (+129). Delta was fully accounted for across stairs (+35), rim boards (+2), floor opening framing (+4), fascia/soffit (+8), north window components (+18), and stone course splits (+18), plus floor layer adjustments. If the delta doesn't add up, there are orphans or unintended additions.

### 17. Improvement rounds can exceed initial build in object count growth
The improvement round added +129 objects (18% growth) from just 5 tasks. The biggest contributor was the staircase (+35 objects for treads, stringers, handrails, posts) and the north window requiring stone course splits (+18 objects). Plan for this — improvement rounds are not small.

### 18. Stair compliance checks are straightforward with named objects
When treads are named sequentially (Stair_Tread_01 through Stair_Tread_17), compliance verification is trivial: sort by z, compute rise between consecutive treads, measure going from bbox y-span, compute Blondel. The Timber agent's naming convention made this a 30-second check instead of a manual investigation.

### 19. Envelope breach at floor openings requires 3-element fix
When a floor opening (stair, service void) interrupts the floor assembly, the thermal envelope breaks at the opening edge. The fix requires three elements: (1) OSB closure panel sealing the floor cavity, (2) mineral wool blocking in exposed joist cavities, (3) vapour barrier bridge connecting the wall vapour layer to the closure panel. All three must be present — missing any one leaves a break in the envelope line. Search broadly by x-range when locating these elements, as the mineral wool and vapour bridge may extend further inward than the closure panel.

### 20. Widen x-range when searching for envelope elements at interfaces
Initial search for envelope fix objects at x=33-42 missed the mineral wool blocking (x=20.8-34.8) and vapour barrier bridge (x=30.2-37.0). These elements extend inward to fill joist cavities, not just the wall face. For interface searches, use a generous x-range (e.g., x=20-45 instead of x=33-42) to catch all related elements.

### 21. Corner posts and wind returns are critical for timber frame integrity
Timber frame walls need explicit corner posts (e.g., 16x16cm spruce) at all four building corners, plus wind barrier returns wrapping around the corners. These are easily missed in early builds because the main wall panels terminate at corners. The reviewer should verify: 4 corner posts, 4 wind returns, proper z-range matching the timber wall height.

### 22. Transition corner patches seal the most vulnerable envelope points
The stone-timber transition at building corners is the most exposed point of the thermal envelope — two different construction systems meeting at a geometric corner. Each corner needs both a capillary break (bitumen) and a thermal seal (compriband). Verify 8 total patches: 4 capillary + 4 thermal, one of each per corner.

### 23. Chimney penetration must be checked through ALL assemblies
A stove chimney must penetrate every horizontal assembly from ground floor to roof ridge. In cabin v3, the chimney pipe stopped at z=700 but the roof ridge was at ~788 — meaning no roof penetration was modeled. Always trace the chimney from stove top to above roof line, checking penetration through floor assembly and roof assembly, with appropriate fire clearances at each.

### 24. Interior furnishing validates spatial design
Adding furniture (beds, tables, shelving, stove) at LOG 350 tests whether the building's interior dimensions actually work. A building that passes all constraint checks can still fail as habitable space if circulation is blocked or rooms are impractical. The furnished interior is the final test of the design.

### 25. Chimney penetration requires layer-by-layer fire stops
When a chimney penetrates a multi-layer assembly (floor or roof), each layer needs its own calcium silicate collar — not a single sleeve. In cabin v3, the roof agent modeled 5 separate collar sets (gypsum, vapour barrier, rafter zone, sarking, counter-battens) with 4 pieces each forming a rectangle around the pipe. This ensures fire rating at every combustible layer crossing. The vapour barrier collar is especially important: PE membrane cannot touch a hot flue, so the calcium silicate board substitutes as the air seal at that level.

### 26. Lead flashing must extend beyond the outermost fire stop
The chimney's lead flashing apron should cover from mid-assembly to above the outermost assembly layer (counter-battens/tiles), extending 20cm+ beyond the pipe on all sides. In cabin v3: flashing z=624.5-666.6 covered the sarking and counter-batten zones. This ensures water sheds around the penetration before reaching any fire stop joint.
