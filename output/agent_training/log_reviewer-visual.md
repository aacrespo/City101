# Reviewer-Visual Log

## Reviews completed

### Phase 3: Wall-Floor Junctions + Facades (Ex18-29) — 12 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex18 | WARN | Monolithic layers where discrete courses needed |
| Ex19 | WARN | Monolithic layers |
| Ex20 | WARN | Monolithic layers |
| Ex21 | WARN | Monolithic layers |
| Ex22 | WARN | Monolithic layers |
| Ex23 | WARN | Monolithic layers |
| Ex24 | WARN | Monolithic layers |
| Ex25 | WARN | Monolithic layers |
| Ex26 | WARN | Monolithic layers |
| Ex27 | PASS | Individual board variants correct |
| Ex28 | WARN | Monolithic layers |
| Ex29 | WARN | Monolithic layers |

### Phase 4: Floor Systems (Ex30-40) — 11 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex30 | WARN | Monolithic slab, no individual blocks |
| Ex31 | WARN | Duplicates + monolithic |
| Ex32 | WARN | Half-width (500mm) + monolithic |
| Ex33 | WARN | Duplicates + monolithic |
| Ex34 | WARN | Monolithic waffle zone |
| Ex35 | WARN | Duplicates + monolithic |
| Ex36 | WARN | Monolithic composite zone |
| Ex37 | WARN | Duplicates + monolithic |
| Ex38 | WARN | Good joists, minor issues |
| Ex39 | WARN | Monolithic steel zone |
| Ex40 | WARN | Monolithic hourdis zone |

### Phase 5: Roof Systems (Ex41-52) — 12 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex41 | PASS | Clean pitched roof |
| Ex42 | PASS | Good monopitch |
| Ex43 | PASS | Good cold deck |
| Ex44 | WARN | Monolithic insulation |
| Ex45 | FAIL | Duplicates |
| Ex46 | WARN | Monolithic layers |
| Ex47 | FAIL | Duplicates |
| Ex48 | FAIL | Duplicates |
| Ex49 | WARN | Monolithic paving |
| Ex50 | PASS | Good metal variants |
| Ex51 | PASS | Good exposed rafters |
| Ex52 | PASS | Good dormer detail |

### Phase 6: Windows (Ex53-62) — 10 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex53 | PASS | Clean window install |
| Ex54 | PASS | Good double-leaf |
| Ex55 | WARN | Monolithic masonry courses |
| Ex56 | PASS | Good fair-face concrete |
| Ex57 | FAIL | Empty (0 objects) |
| Ex58 | PASS | Clean lightweight cladding |
| Ex59 | PASS | Good heavyweight cladding |
| Ex60 | PASS | Good timber frame |
| Ex61 | PASS | Excellent — 23 objects, shingle returns |
| Ex62 | PASS | Good non-loadbearing |

### Phase 7: Doors (Ex63-67) — 5 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex63 | PASS | Clean hinged door |
| Ex64 | FAIL | No objects (layer naming mismatch?) |
| Ex65 | PASS | Good sliding external |
| Ex66 | PASS | Excellent — ~120 objects, LOG 400 brick courses |
| Ex67 | FAIL | Duplicate leaves, tracks, guides |

### Phase 8: Foundations (Ex68-72) — 5 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex68 | PASS | Clean strip footing |
| Ex69 | PASS | Good pad footing |
| Ex70 | PASS | Good ground slab |
| Ex71 | PASS | Good timber plinth |
| Ex72 | PASS | Good raft foundation |

### Phase 9: Stairs (Ex73-76) — 4 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex73 | FAIL | Massive duplication — 66 objects, 2x slab, 2x infills, 2x risers |
| Ex74 | FAIL | Everything doubled — 12 treads (6 needed), 4 walls (2 needed) |
| Ex75 | PASS | Clean build, correct acoustic infill in box stringers |
| Ex76 | WARN | Good spiral geometry, missing outer stringer + balusters |

### Phase 10: Structural Elements (Ex77-80) — 4 exercises
| Ex | Verdict | Key Issues |
|----|---------|------------|
| Ex77 | PASS | Correct Vittone sizing, clean geometry |
| Ex78 | FAIL | EMPTY — 0 objects despite task marked complete |
| Ex79 | PASS | Correct structural system |
| Ex80 | PASS | Excellent — exact count, bonus edge beams |

### Three Laws Enforcement (applied retroactively to all exercises)
17 exercises changed WARN->FAIL after automated overlap detection.

## Overall Totals (63 exercises reviewed)
- After Three Laws enforcement: 12 PASS / 20 WARN / 20 FAIL (from earlier batch)
- Phase 9-10 batch: 4 PASS / 1 WARN / 4 FAIL
- **Grand total: ~16 PASS / 21 WARN / 24 FAIL** (2 empty = auto-FAIL)

## Patterns observed

### #1 failure mode: Duplicate geometry (Law 2)
Prior modeling attempts leave orphan objects. Most common pattern: two objects with identical or near-identical bounding boxes on the same or related layers. The modeler rebuilds but doesn't delete the first attempt. Affects Ex31, Ex33, Ex35, Ex37, Ex45, Ex47, Ex48, Ex67, Ex73, Ex74.

### #2 failure mode: Monolithic slabs (LOG 200 not LOG 300)
Layers that should contain individual discrete elements (tiles, blocks, courses, boards, battens) are modeled as single solid rectangles. This is the most widespread issue — nearly every Phase 3-4 exercise.

### What's consistently correct
- **Dimensional accuracy**: Total assembly thicknesses match specs every time
- **Material assignments**: Correct materials on correct layers
- **Structural logic**: Correct load paths, correct assembly order
- **Construction knowledge**: Blondel verified on all stairs, Vittone table matched for columns, structural systems properly represented

### Best exercises (gold standards)
- **Ex66** (Internal Door Sound Insulation): ~120 objects, LOG 400, individual brick courses with mortar — proves modeler can do it
- **Ex61** (Window in Solid Timber Panel): 23 objects, wall layers cut around opening, shingle returns
- **Ex80** (Frame System): Exact object count, bonus edge beams showing structural understanding
- **Ex75** (Metal Stair): Clean build with acoustic infill detail inside box stringers

### Review technique notes
- Bounding-box overlap detection catches most Law 2 violations but produces false positives for: (a) containment relationships like mineral wool inside box-section stringers, (b) helical geometry where curved elements share bounding boxes, (c) stair geometry where inclined slabs have large BBs overlapping step elements. Must evaluate each overlap for architectural justification.
- Spiral stair (Ex76) handrail-tread BB overlaps are false positives — the tube and plate don't actually intersect in 3D.
- "Slab" layer in Ex73 is a duplicate of "InclinedSlab" — same element on two layers. This inflates overlap count massively.
