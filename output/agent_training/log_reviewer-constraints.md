# Reviewer-Constraints Log

## Reviews completed

### Session 3 — Batch reviews

**Ex65 — PASS** Sliding External Door Metal/Glass. 10 objects, single geometry set. All steel/aluminium/glass (naturally monolithic). Clean build.

**Ex66 — PASS** Internal Door Sound Insulation. 143 objects. REFERENCE EXERCISE for LOG 300-400 masonry. 129 wall objects: individual brick courses (62.5mm) + mortar joints (12.5mm). 9-layer acoustic door leaf at 60mm. First exercise to achieve true LOG 300-400 on masonry.

**Ex67 — FAIL** Sliding Internal Pocket Door. Duplicate geometry — two builds at x=10000 and x=80000. Both have correct pocket construction but neither is complete alone.

**Ex71 — REVISED PASS** Timber Panel Plinth. 226 objects on TrainingS3::Ex71_TimberPlinth (was FAIL — geometry on TrainingS3 prefix, not Training8). LOG 400: 195 individual larch shingles, 7 spruce T&G boards, 8 floor tiles with grout gaps. Stem wall 800mm deep, DPC, sole plate set back 30mm. Outstanding.

**Ex73 — FAIL** RC Stair. Duplicate geometry — Set 1 at x=120000 (31 obj), Set 2 at x=14000 (40 obj, superior — has mortar beds under treads). Blondel correct. Delete Set 1.

**Ex74 — FAIL** Stone Cantilevered Stair. Duplicates (2 builds) + masonry walls monolithic. Set 1 has correct L-shaped quarter-turn; Set 2 is straight run.

**Ex75 — FAIL** Metal Stair Box-Section. Duplicates (2 builds, neither complete). Width 700mm not 900mm per spec. Set 1 stringers flat (wrong), Set 2 missing mineral wool and landing.

**Ex76 — WARN** Spiral Stair. 14 objects, single geometry set. Excellent spiral: 12 steel treads at 15 deg, 150mm column, helical handrail. Missing outer stringer.

**Ex77 — WARN** RC Column Load Comparison. 9 objects. Correct sizing (250/400/500mm), 6m tall, scaled footings. Missing lean concrete + gravel under footings.

**Ex78 — PASS** Steel Column and Beam Connection. 12 objects (TrainingS3 prefix). I-sections decomposed into flanges + web. HEA 280 + HEB 300 match Vittone exactly. Base plate, anchor bolts, end plate.

**Ex79 — FAIL** Bearing Wall System. Masonry walls monolithic + building dimensions create 2.5m spans instead of 5m per spec.

**Ex80 — WARN** Frame System Column + Core. 14 objects matching spec. 8m grid, 400x400 columns, 3x3m core, 250mm flat slab. Minor slab/edge-beam z-overlap.

### Re-checks (TrainingS3 prefix correction)

**Ex57 — REVISED PASS** Window in ETICS. 90 objects on TrainingS3::Ex57_WindowETICS. LOG 300-400 masonry (49 courses). ETICS layers split around opening. 10 individual EPS boards. XPS returns. Triple glazing in PVC frame. Section test PASS.

**Ex64 — REVISED PASS** Hinged External Door Wood/Glass. 101 objects on TrainingS3::Ex64_ExtDoorGlass. LOG 300-400 masonry (62 courses). Glazed door (stiles/rails + glass). Prefab steel lintel. 8 rockwool boards, 8 fibre-cement slates, 3 battens. Section test PASS.

### Earlier reviews (from before context compaction)

Exercises Ex18-Ex62, Ex68-Ex72 reviewed in earlier batches. Key results:
- PASS: Ex56, Ex59, Ex62, Ex69 (all naturally monolithic)
- Most exercises FAIL on: LOG 200 masonry (monolithic blocks), duplicate geometry, or empty layers
- Foundations (Ex68-72) cleanest category overall
- Window exercises (Phase 6) best structural detail but masonry still monolithic

## Patterns observed

1. **Duplicate geometry (Pattern C)** persists across modelers — prior build attempts left at different x-positions. Stairs worst affected (Ex73, Ex74, Ex75 all duplicated; Ex76 clean).

2. **TrainingS3 layer prefix** — Modeler-1 built on TrainingS3::Ex{NN}_* layers, not Training{Phase}::Ex{NN}::*. Always check BOTH prefixes. Ex57 (90 obj), Ex64 (101 obj), Ex71 (226 obj) were all PASS but appeared empty under the wrong prefix.

3. **LOG 300-400 masonry achieved in multiple exercises** — Ex57 (49 courses), Ex64 (62 courses), Ex66 (129 courses), Ex71 (195 shingles + 7 boards + 8 tiles). All modeler-1 work on TrainingS3 layers.

4. **Structural exercises (Phase 10) cleanest** — all RC/steel, naturally monolithic, single geometry sets. Only Ex79 fails (has masonry + wrong dimensions).

5. **Section test** is the gold standard: clipping plane through model in both directions, every layer identifiable, every component visible.

6. **Three Laws** (absolute FAIL criteria): (1) everything has thickness, (2) no overlaps ever, (3) nothing floats.

7. **Monolithic vs discrete rule**: poured concrete/steel/glass/membranes = OK monolithic. Masonry/tiles/battens/joists/boards = MUST be discrete individual pieces.
