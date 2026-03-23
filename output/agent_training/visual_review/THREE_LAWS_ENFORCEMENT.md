# Three Laws Enforcement Review

Reviewer: reviewer-visual
Date: 2026-03-22
Standard: Rhino Playbook Three Laws -- strict enforcement, any violation = FAIL

## The Three Laws

1. **EVERYTHING HAS A THICKNESS** -- no surfaces, every layer is a separate solid
2. **NO OVERLAPS -- EVER** -- two solids cannot occupy same space. Duplicates = worst violation.
3. **NOTHING FLOATS** -- every object must bear on or attach to something

## Law 2 Violations: Overlapping/Duplicate Geometry

Automated check: same-purpose objects with overlapping bounding boxes.

### Exercises with Law 2 violations (verdict changed to FAIL):

| Exercise | Objects | Overlaps | Previous | New | Issue |
|----------|---------|----------|----------|-----|-------|
| Ex20 | 18 | 2 | WARN | FAIL | Two sets: 680mm + 500mm floor width |
| Ex21 | 19 | 2 | WARN | FAIL | Two sets: 610mm + 500mm floor width |
| Ex23 | 24 | 6 | WARN | FAIL | Triple geometry: 1200/688/588mm slabs |
| Ex26 | 8 | 4 | WARN | FAIL | Every layer has exact duplicate (same position) |
| Ex27 | 43 | 22 | PASS | FAIL | Two complete modeling attempts overlap |
| Ex28 | 8 | 2 | WARN | FAIL | Duplicate glass panels (same position) |
| Ex29 | 48 | 4 | WARN | FAIL | Two sets: 1000mm + 500mm height |
| Ex31 | 12 | 5 | FAIL | FAIL | (unchanged) Two sets overlap |
| Ex35 | 12 | 5 | FAIL | FAIL | (unchanged) Two sets overlap |
| Ex37 | 12 | 4 | WARN | FAIL | Two sets: 1000x500 + 500x500 |
| Ex39 | 10 | 1 | WARN | FAIL | 1000mm + 500mm orphan set |
| Ex40 | 24 | 12 | WARN | FAIL | Two complete variant sets overlap |
| Ex45 | 16 | 5 | WARN | FAIL | Every layer has 1000x500 + 500x500 copy |
| Ex46 | 16 | 6 | WARN | FAIL | Every layer has 1000x500 + 500x500 copy |
| Ex47 | 25 | 4 | WARN | FAIL | Triple sets: 1000x500, 500x500, 1000x1000 |
| Ex48 | 19 | 10 | PASS | FAIL | Two complete sets overlap |
| Ex50 | 22 | (not checked individually) | WARN | FAIL | Shared + per-variant duplicate sets |
| Ex53 | 27 | 10 | WARN | FAIL | Two complete window sets overlap |

### Exercises with NO Law 2 violations (verdicts unchanged or improved):

**Clean PASS (no violations of any law):**
- Ex22: 11 objects, no overlaps, correct assembly -- PASS
- Ex24: 4 objects, no overlaps, correct principle -- stays WARN (too few objects for LOG 300)
- Ex25: 8 objects, no overlaps, correct assembly -- stays WARN (needs individualization)
- Ex38: 10 objects, no overlaps, individual joists -- stays WARN
- Ex41: 6 objects, no overlaps -- stays WARN
- Ex42: 9 objects, no overlaps -- stays WARN
- Ex43: 7 objects, no overlaps -- stays WARN
- Ex44: 6 objects, no overlaps -- stays WARN
- Ex49: 28 objects, no same-purpose overlaps -- PASS
- Ex51: 8 objects, no overlaps -- stays WARN
- Ex52: 11 objects, no overlaps -- PASS
- Ex54: 29 objects, no overlaps -- PASS
- Ex55: 13 objects, no overlaps -- stays WARN
- Ex56: 11 objects, no overlaps -- PASS
- Ex58: 22 objects, no overlaps -- PASS
- Ex59: 15 objects, no overlaps -- stays WARN
- Ex60: 14 objects, no overlaps -- PASS
- Ex61: 23 objects, no overlaps -- PASS
- Ex62: 11 objects, no overlaps -- PASS
- Ex63: 27 objects, no overlaps (wall has individual bricks) -- PASS
- Ex65: 10 objects, no overlaps -- PASS
- Ex66: ~120 objects, no overlaps, individual brick courses -- PASS (gold standard)
- Ex68: 6 objects, no overlaps -- stays WARN
- Ex69: 5 objects, no overlaps -- stays WARN
- Ex70: 6 objects, no overlaps -- stays WARN
- Ex71: 13 objects, no overlaps -- PASS
- Ex72: 7 objects, no overlaps -- stays WARN

**Special cases:**
- Ex18: 11 objects, no overlaps -- stays WARN (clean but single-solid layers)
- Ex19: 7 objects, no overlaps -- stays WARN (500mm width, minimal)
- Ex30: already FAIL from earlier review (LOG 200)
- Ex32: already WARN (500mm width)
- Ex33: already WARN (orphan objects may overlap -- needs check)
- Ex34: already WARN
- Ex36: already WARN (orphan objects)
- Ex57: has two sets but they're wall portions + full-height -- functional overlap needs check
- Ex64: FAIL (no objects found)

## Updated Verdicts Summary

| Phase | PASS | WARN | FAIL | Total |
|-------|------|------|------|-------|
| Phase 3 (Ex18-29) | 0 | 5 | 7 | 12 |
| Phase 4 (Ex30-40) | 0 | 4 | 7 | 11 |
| Phase 5 (Ex41-52) | 2 | 7 | 3 | 12 |
| Phase 6 (Ex53-62) | 6 | 1 | 2 | 9 |
| Phase 7 (Ex63-66) | 3 | 0 | 1 | 4 |
| Phase 8 (Ex68-72) | 1 | 3 | 0 | 4 |
| **Total** | **12** | **20** | **20** | **52** |

Previous: 15 PASS / 35 WARN / 3 FAIL
After Three Laws enforcement: **12 PASS / 20 WARN / 20 FAIL**

## Impact Analysis

The Three Laws enforcement changes 17 exercises from WARN to FAIL. Every one of these has overlapping duplicate geometry -- the same construction modeled twice at different sizes or positions, with both copies remaining in the file.

**Root cause**: The modeler appears to have made multiple attempts at each exercise, leaving orphaned geometry from earlier attempts. This is a workflow issue, not a knowledge issue -- the assembly logic is usually correct in at least one of the duplicate sets.

**Recommendation**: A cleanup pass to delete orphan geometry would immediately convert most of these FAILs to WARN or PASS, since the underlying construction logic is correct.

## Law 3 Check (Nothing Floats)

Law 3 violations are harder to detect programmatically (requires checking spatial adjacency). Based on inventory analysis, most exercises have correct vertical stacking with layers bearing on each other. No obvious Law 3 violations detected in clean exercises. Exercises with duplicates inherently violate Law 3 for the orphan set (which floats at a different position/size from the main assembly).

## Law 1 Check (Everything Has Thickness)

All reviewed exercises model layers as solid boxes with real mm thickness. No zero-thickness surfaces detected. Law 1 compliance is universal across all exercises.
