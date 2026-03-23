# Constraint Reviewer Learnings — Training Session 3

## S3-R1: Duplicate geometry pattern (1000x500 + 500x500)
**Issue:** Multiple exercises (Ex31, Ex35, Ex37) had every layer duplicated — one object at 1000x500mm and another at 500x500mm, overlapping in the 0-500mm x-range. This produces double-thickness material in the overlap zone.
**Detection:** Compare object footprints within the same layer. If two objects share the same z-range and one's footprint is a subset of the other's, it's a duplicate.
**Source:** Ex31, Ex35, Ex37.

## S3-R2: LOG 200 vs 300-400 is the dominant failure mode for pre-directive builds
**Issue:** All 7 exercises reviewed (Ex30-Ex35, Ex37) were modeled at LOG 200 — every layer as a single monolithic slab. None had individual tiles, blocks, boards, battens, or joists.
**Rule:** For LOG 300-400 review, check: are discrete elements (tiles, blocks, boards) modeled as separate objects? A single slab for a layer that should contain multiple discrete elements is an automatic FAIL.
**Quick test:** If clay tiles layer has 1 object and the strip is 1000mm wide, it's LOG 200. At 30x30cm tiles it should have ~9 objects.

## S3-R3: Dimensional accuracy was universally correct
**Observation:** Despite LOG level failures, every exercise had correct total thickness, correct individual layer thicknesses, correct z-stacking with no gaps, and correct material metadata. The modelers understand the buildups perfectly — they just need to model at higher resolution.
**Implication:** When reviewing rebuilds, dimensions will likely still be correct. Focus review time on LOG 300-400 compliance (discrete elements, gaps, spacing) rather than re-checking thicknesses.

## S3-R4: Which layers need discrete elements vs acceptable as single solid
**Guidance for LOG 300-400:**
- **Must be discrete:** tiles (floor/roof), masonry blocks/courses, timber boards/planks, battens, joists, counter-battens
- **Acceptable as single solid:** poured concrete slabs, screed, plaster, insulation boards (borderline — individual boards preferred), rubber membrane strips, adhesive beds, bonding coats
- **Edge case:** Prefab elements (hollow-core planks, hourdis blocks) — should show individual prefab units side by side with grouted joints at LOG 300
- **Naturally monolithic:** Rupli prefab timber elements, poured bitumen, planting substrate, copper sheet, glass panels — acceptable as single solids

## S3-R5: Three distinct duplicate patterns by modeler
**Pattern A (Modeler-4):** Two overlapping geometry sets per layer — one at 1000x500mm, one at 500x500mm. Consistent across Ex31, Ex35, Ex36, Ex37, Ex39, Ex40, Ex26, Ex29.
**Pattern B (Modeler-3/1):** Full-height wall (z=0-3000) PLUS partial wall (z=0-1000), and floor duplicated at two different z-positions. Seen in Ex20, Ex21, Ex23.
**Pattern C (Modeler-4):** Complete identical duplicates at same position/size (Ex26 — every object doubled).
**Detection:** Count objects per layer. If any layer has >1 object with overlapping z-ranges and one bbox is a subset of another, it's a duplicate.

## S3-R6: Roof exercises often miss membrane layers
**Observation:** Ex24 missing vapour barrier + tar paper. Ex25 missing vapour barrier + breather membrane. Ex43 missing F3 film secondary WP.
**Rule:** Always check for thin membrane layers (vapour barriers, WP membranes, breather films) — these are the most commonly omitted at LOG 200 and the most important to add at LOG 400. Count membrane layers in spec vs model.

## S3-R7: Exercises with naturally monolithic layers pass dimensional review easily
**Observation:** Ex44 (flat roof bitumen) has 6 layers, all naturally monolithic (concrete, bitumen, insulation, planting substrate). It achieved near-PASS with perfect dimensions. Ex36 (composite metal-concrete) similarly has only monolithic elements. These exercises need only duplicate cleanup to pass.
**Implication:** Prioritize re-review of monolithic-layer exercises (Ex36, Ex39, Ex44) after duplicate cleanup — they'll pass fastest.

## S3-R8: Section test is the gold standard, not visual appearance
**Correction from lead:** The review standard is SECTION REALISM via clipping plane, not perspective appearance. Put a clipping plane through the model in both directions — can you identify every single layer? Is every component there?
**What this means for masonry:** A section through masonry must show individual brick/block courses with mortar joints — not a monolithic block. Even window exercises (Ex54, Ex55, Ex58) that have excellent window detailing FAIL if their masonry walls read as solid blocks in section.
**What this means for tiles:** Floor/roof tiles in section must show individual units. A single slab labeled "tiles" fails the section test.
**What this means for timber:** Battens, counter-battens, joists must be individual members visible in section at correct spacing.
**Impact:** Revised 5 previously-PASSed exercises (Ex54, Ex55, Ex58, Ex60, Ex68) down to WARN because their masonry layers fail section test despite correct dimensions and good window/structural detailing.

## S3-R9: Window exercises (Phase 6) have best structural detailing but masonry still LOG 200
**Observation:** Phase 6 window exercises (Ex53-Ex62) have dramatically better quality than earlier phases: no duplicates, correct framing details (lintels, cavity trays, flashings, header beams), proper insulation returns. But the masonry wall layers around openings are still monolithic blocks. The window-specific components pass section test; the wall construction doesn't.
**Implication:** Window exercises are closest to full PASS — they only need masonry courses added to their wall layers. The window framing itself (frame, glazing, lintel, sill, flashing) is already at LOG 300-400.

## S3-R10: Foundation exercises are cleanest — naturally monolithic
**Observation:** Ex68 (strip footing), Ex69 (pad footing), Ex70 (ground slab), Ex72 (raft) all have clean geometry, no duplicates, correct dimensions. Foundation elements (poured concrete, gravel, lean concrete) are naturally monolithic and pass section test. Only the masonry wall above DPC in Ex68 needs courses.
**Implication:** Foundations are the fastest path to full PASS — only Ex68 and Ex70/Ex72 need minor fixes (masonry courses, discrete tiles respectively).

## S3-R11: Three Laws enforcement — strict FAIL criteria
**Directive from lead:** The Three Laws are absolute FAIL criteria, no exceptions:
1. Everything has thickness — no zero-thickness planes
2. No overlaps EVER — duplicates are the worst violation (100% overlap)
3. Nothing floats — every object must bear on/attach to something

Plus: "Model assemblies not surfaces" — masonry is courses+mortar, not a slab. Tiles are individual units, not a sheet. Battens are discrete members, not a plank.

**Impact on reviews:** Under strict Three Laws, ALL exercises with monolithic masonry walls FAIL (even window exercises with excellent framing). ALL exercises with single-slab tiles FAIL. ALL exercises with single-slab battens FAIL. This moved 8 WARN exercises to FAIL.

**Revised totals after Three Laws:** 8 PASS, 0 WARN, 33 FAIL, 1 EMPTY (42 reviewed).

## S3-R12: Only exercises with naturally monolithic construction can PASS strict review
**Observation:** Under strict Three Laws + section test + assemblies-not-surfaces, the only exercises that PASS are those where ALL layers are naturally monolithic:
- **Poured concrete** (slabs, walls, lintels, footings): monolithic = PASS
- **Steel** (columns, beams, plates, angles): monolithic = PASS
- **Lightweight panels** (plywood, particleboard, hardboard, Eternit): manufactured sheets = PASS
- **Membranes** (DPC, vapour barriers, WP): single sheets = PASS
- **Glass** (glazing): single pane = PASS
- **Insulation boards**: borderline — individual boards preferred but single slab acceptable

Surviving PASS: Ex56, Ex59, Ex62, Ex69 — all use naturally monolithic construction with no masonry, tiles, or battens.

## S3-R13: Ex66 achieves LOG 300-400 masonry — the gold standard
**Observation:** Ex66 (Internal Door Sound Insulation) has 129 wall objects: individual brick courses at 62.5mm with mortar joints at 12.5mm (= 75mm per course). Wall split into three zones: full-width courses above opening, left jamb courses, right jamb courses. Plus 9-layer acoustic door leaf, concrete lintel, filler strip. This is what every masonry exercise should look like.
**Implication:** Ex66 is now the reference exercise for masonry at LOG 300-400. Any exercise with masonry walls should match this pattern: individual courses + mortar joints + wall split around openings.

## S3-R14: Duplicate geometry persists in stairs and later doors
**Observation:** Stair exercises (Ex73, Ex74, Ex75) all have duplicate geometry sets at completely different positions (Pattern C — two complete builds). Ex67 (pocket door) also duplicated. Only Ex76 (spiral stair) is clean. The pattern: modelers run a build script, it fails or produces unexpected results, they re-run at a different position without cleaning up the first attempt.
**Detection for stairs:** Query all objects, group by x-position clusters. If there are 2+ clusters separated by >10000mm, it's duplicate builds.

## S3-R15: Structural exercises (Phase 10) are cleanest builds
**Observation:** Ex77 (column sizing), Ex78 (steel connection), Ex80 (frame system) all have single geometry sets, no duplicates, correct dimensions, and all-monolithic materials (RC, steel). The only failures are missing sub-grade layers (lean concrete, gravel) or minor overlap issues. These exercises benefit from being entirely poured concrete and steel — no masonry, tiles, or battens to model discretely.
**Exception:** Ex79 (bearing wall system) fails because it includes masonry facade walls (monolithic) and has incorrect building dimensions creating 2.5m spans instead of 5m.

## S3-R16: Empty exercises (Ex57, Ex64, Ex71) — layers without geometry
**Pattern:** Three exercises have full layer trees created (up to 45 layers) but zero objects in any layer. The build scripts created the layer structure but failed silently — no geometry was produced. Always verify object counts after running build scripts.

## S3-R17: Updated pass/fail totals after full curriculum review
**Final totals (all 80 exercises, or as many as reviewed):**
New PASSes this batch: Ex65 (sliding ext door), Ex66 (int door LOG 300-400), Ex78 (steel connection)
New WARNs: Ex76 (spiral stair), Ex77 (column sizing), Ex80 (frame system)
New FAILs: Ex67 (pocket door duplicates), Ex71 (empty), Ex73 (RC stair duplicates), Ex74 (stone stair duplicates + monolithic masonry), Ex75 (metal stair duplicates + wrong width), Ex79 (monolithic masonry + wrong dimensions)
