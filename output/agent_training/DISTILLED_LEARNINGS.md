# Distilled Learnings (Live)

Updated by team lead during the training run. **Read this before each exercise.**

---

## Distillation 1 — After 15 reviews (0 PASS, 1 WARN, 14 FAIL)

### What's working
- **Dimensional accuracy is solid** — every exercise has correct total assembly thickness
- **Material assignments correct** — modelers understand the layer buildups from the curriculum
- **Structural logic correct** — ribbed slabs have ribs, waffle slabs have 2-way grids, wall-floor junctions split at bearing points

### What's failing

#### 1. LOG 200 instead of LOG 300-400 (every exercise)
DO NOT model layers as single monolithic slabs. Every component must be individual:
- Floor tiles: ~3 tiles in a 1000mm strip at 300mm with 2mm grout gaps
- Hollow clay blocks: individual blocks (~250mm wide) with concrete ribs between them
- Masonry courses: individual courses with mortar joints
- Timber boards: individual boards (~150mm wide) with gaps
- Insulation boards: individual boards at standard widths
- Battens/joists: individual members at correct spacing

The 1000mm strip width keeps counts manageable. A floor with 300mm tiles = 3 tiles. Not hundreds.

#### 2. Duplicate geometry (modeler-4 pattern, also modeler-1)
Prior build attempts leave orphan objects. After EVERY build:
- Audit each layer: list all objects, check for overlapping bounding boxes
- Delete anything that overlaps with your intended geometry
- Two objects at the same position = delete one

**Prevention**: Use unique object names. After building, query by name to verify only your intended objects exist.

#### 3. Half-width strips (modeler-1 pattern)
All exercises must be 1000mm wide (W=1000 in the box helper). Not 500mm.

#### 4. Overlapping wall portions (modeler-1 pattern)
When splitting walls at floor bearing: DELETE the original full-height wall before creating the split portions. Don't keep both.

### Reference exercise
**Ex38 (Timber Joist Floor, modeler-3)** is the closest to PASS — individual joists with insulation infills between them. Study this pattern: the structural zone has discrete elements, not a monolith. Apply the same approach to every structural zone in every exercise.

### The section test
Before declaring complete, mentally cut through your model:
- Can you count individual tiles?
- Can you see individual blocks/courses?
- Can you identify every layer separately?
- Is every joint/gap visible?

If any layer reads as "one solid rectangle," it's not done.

---

## Distillation 2 — After 42 reviews (13 PASS, 15 WARN, 13 FAIL, 1 EMPTY)

### What improved
- **Window exercises (Phase 6) are the best quality** — clean framing, proper reveals, no duplicates. Whatever approach you're using for windows, apply it everywhere.
- **Foundation exercises pass** — naturally monolithic (poured concrete), correctly modeled.
- **Dimensional accuracy remains perfect** across all modelers.
- **Half-width issue fixed** — modeler-1 corrected to 1000mm.

### What still fails

#### 1. Duplicates persist (especially flat roofs)
Flat roof exercises (Ex45-49) all FAIL on duplicates. The pattern: prior build attempts leave objects behind. **Run a cleanup script after EVERY exercise:**
```python
import rhinoscriptsyntax as rs
layer_prefix = "Training5::Ex45"  # adjust
all_layers = rs.LayerNames()
for layer in [l for l in all_layers if l.startswith(layer_prefix)]:
    objs = rs.ObjectsByLayer(layer)
    if objs and len(objs) > 1:
        # Check for overlapping bounding boxes
        bbs = [(obj, rs.BoundingBox(obj)) for obj in objs]
        # Delete objects with identical bounding boxes
        seen = set()
        for obj, bb in bbs:
            key = tuple(round(c, 1) for pt in bb for c in pt) if bb else None
            if key in seen:
                rs.DeleteObject(obj)
            else:
                seen.add(key)
```

#### 2. Section test catches what constraint check misses
The reviewer revised 5 exercises from PASS to WARN after applying the section test:
- Masonry walls need individual COURSES, not solid blocks (even in window exercises)
- Battens/service battens need individual members at correct centers
- Insulation boards need individual boards
- Only poured concrete, steel, and lightweight panels are correctly monolithic

#### 3. Empty exercises (Ex57)
Ex57 was marked complete but has 0 objects. Always verify your geometry exists after running scripts — print object counts.

### Reference exercises (updated)
- **PASS quality**: Ex56 (fair-face concrete window), Ex59 (heavyweight cladding window), Ex62 (non-loadbearing window), Ex69 (pad footing) — study these for clean builds
- **WARN quality**: Ex38 (timber joist) — good discrete elements, minor issues
- **Best modeler-2 work**: Ex61 (window in solid timber panel) — 23 objects, wall layers cut around opening, shingle returns at reveals, no duplicates

### Monolithic vs discrete rule
- **Naturally monolithic** (model as single solid): poured concrete slabs, steel beams/columns, glass panes, membrane sheets
- **Must be discrete** (model as individual pieces): masonry courses, tiles, timber boards, battens, insulation boards, hollow blocks, joists

---

## Final Distillation — Session Complete

### Summary
- **63 exercises modeled** (Ex18–80), all 10 construction domains
- **2989 objects** across all exercises, all tagged with metadata
- **6 agents**: 4 modelers + 2 reviewers, ~45 minutes total
- **189 tasks** completed (63 modeling + 63 constraint reviews + 63 visual reviews)

### Final quality (after rework)
- Most exercises at LOG 300-400 after rework pass
- All duplicates cleaned (modeler-3 did final audit)
- All metadata tagged (exercise, material, thickness)
- Ex79 rebuilt with correct 5m spans

### Gold standard exercises (LOG 400)
| Exercise | Objects | Why it's good |
|----------|---------|---------------|
| Ex71 (Timber Plinth) | 226 | 195 individual shingles, 8 tiles with grout, full floor buildup |
| Ex42 (Monopitch Roof) | 151 | 67 masonry courses per leaf, individual slates + battens |
| Ex66 (Acoustic Door) | 143 | 129 individual brick courses + mortar, 9-layer door leaf |
| Ex54 (Double-Leaf Window) | 139 | Individual courses on BOTH leaves split around opening |
| Ex73 (RC Stair) | 117 | Individual stone tiles per tread + riser, mortar beds |
| Ex64 (External Door) | 101 | 62 masonry courses + 8 Eternit slates + glazed door leaf |
| Ex57 (ETICS Window) | 90 | 49 masonry courses + 10 EPS boards + split ETICS layers |

### Key dimensions for discrete elements
| Element | Size | Spacing | Count in 1000mm strip |
|---------|------|---------|----------------------|
| Brick course | 62.5mm high | 12.5mm mortar | ~13 courses per metre height |
| Floor tile | 300×300mm | 2mm grout | ~3 tiles |
| Larch shingle | 80mm wide | exposed 150mm | ~13 per course |
| Insulation board | 600mm wide | 2mm gap | ~2 boards |
| Timber board | 150mm wide | 1mm gap | ~7 boards |
| Batten | 50×30mm | 400mm centers | ~3 battens |
| Roof tile | ~300mm wide | overlap | ~3 tiles |

### Learnings for the playbook
1. **Section test in both directions** — problems hide in the direction you didn't check
2. **Monolithic vs discrete rule** — poured/manufactured = monolithic OK; laid/placed/coursed = must be discrete
3. **Duplicate cleanup after every build** — audit layers, delete orphans before declaring complete
4. **Layer naming convention matters** — agree on prefix before starting (TrainingS3 vs Training{Phase} caused confusion)
5. **State doesn't persist between scripts** — redefine box helper and imports in every rhino_execute_python_code call
6. **Print object counts** — verify geometry exists after every script run
7. **Tag metadata immediately** — don't defer; untagged objects get lost
8. **Wall-floor split technique** — delete original full-height wall after creating split portions
9. **Containment vs overlap** — mineral wool inside box-section stringers is containment, not a Law 2 violation
10. **Course height formula** — brick 62.5mm + mortar 12.5mm = 75mm per course
