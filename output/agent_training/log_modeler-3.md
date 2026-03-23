# Modeler-3 Log

## Exercises completed

### Session 1-2 (original builds)
| Ex | Objects | Notes |
|----|---------|-------|
| Ex23 | 37 | Non-loadbearing wall-floor. Tagged TrainingS3 objects. |
| Ex41 | 11 | Pitched roof. 3 Eternit slates, 2 insulation boards. |
| Ex43 | 16 | Cold deck metal. 3 rafters, 6 roof decking boards. |
| Ex52 | 20 | Dormer. Main roof + dormer wall/roof layers. |
| Ex55 | 22 | Window in facing masonry. Individual courses. |
| Ex56 | 12 | Window in fair-face concrete. Naturally monolithic. |
| Ex59 | 18 | Window in heavyweight cladding. Individual stone slabs. |
| Ex60 | 21 | Window in timber frame. Individual boards/panels. |
| Ex62 | 15 | Window non-loadbearing. Lightweight framing. |
| Ex66 | 143 | Internal acoustic door. 129 wall courses, 9-layer leaf. |
| Ex67 | 31 | Sliding pocket door. Double-stud wall, pocket cavity. |
| Ex71 | 34 | Timber plinth foundation. Below-grade stem wall. |
| Ex73 | 117 | RC stair. Inclined slab + step infills + finishes. |
| Ex74 | 92 | Stone cantilevered stair. L-shaped quarter-turn. |
| Ex75 | 23 | Metal box-section stair. Angled stringers + treads. |
| Ex76 | 37 | Spiral stair. Cylindrical column, pie treads, helical handrail. |

### Session 3 (tagging + Ex79 rebuild)
| Ex | Objects | Notes |
|----|---------|-------|
| Ex79 | 12 | Bearing wall system rebuilt. Correct 5000mm spans, masonry courses. |

### Batch tagging (all exercises)
Tagged metadata on all 63 exercises (Ex18-Ex80): 2989 objects total.
Many exercises were built by other modelers without `exercise` metadata — all now tagged.

## Learnings

See `learnings/learnings_modeler-3.md` for detailed technical notes.

Key patterns:
1. Always check both `Training{Phase}::` and `TrainingS3::` layer prefixes
2. SetUserText tags can be lost between sessions — re-tag as needed
3. Monolithic vs discrete: concrete/steel/glass/membranes = monolithic OK; masonry/tiles/boards = must be discrete
4. 8-point box for angled geometry (inclined slabs, stringers)
5. Course height for masonry: 62.5mm brick + 12.5mm mortar = 75mm
6. Insulation boards: 600mm standard width with 2mm gaps
7. CapPlanarHoles returns bool in some Rhino versions — always check return type
