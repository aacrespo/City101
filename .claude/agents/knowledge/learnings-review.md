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
