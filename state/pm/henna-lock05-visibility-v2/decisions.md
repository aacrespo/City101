# Decisions Log — Lock 05 Visibility v2

## 2026-03-27: Why rebuild instead of patch further

The v1 model reached 361 elements after 4 rounds of patching. Each round introduced new problems:
- Round 1 review: found 27 spec errors (structural showstoppers, geometry issues)
- Round 2 review (3 agents): found 33 model errors (missing slabs, walls, entries)
- Round 3 review: found 12 more (ramp columns, diagonal columns, connector gaps)
- Round 4 review: found 29 more (all handrails missing, corner parapets, stair ceilings, south lintel)

The root cause: agents built independently without discussing interfaces. The v3 workflow's "discuss → decide → execute" pattern was documented but not followed. The lead both coordinated AND built geometry, losing overview.

**Decision:** Full rebuild with discussion-first protocol. 3 phases: negotiate → build → verify. Clean Rhino start.

## 2026-03-27: Topology choice

**Phase 0 — Flat, broad context, sequential discussion.**
Why flat: agents need to hear each other's proposals and negotiate directly. A hierarchical structure would filter information through the lead, losing nuance at interfaces.
Why broad context: every agent needs to see the full building concept to propose their system in context.

**Phase 1 — Hierarchical, narrow context, parallel execution.**
Why hierarchical: the spec is agreed — execution is mechanical. Lead coordinates, modelers execute.
Why narrow: each modeler reads only the element catalog, not the full discussion. Reduces token cost.
Why only 2 modelers: Lock 02 proved 2 careful > 4 fast. The spec quality is the lever, not modeler count.

**Phase 2 — Flat, single reviewer.**
Why: one reviewer with full context is better than multiple partial reviewers. The 3-agent review in v1 found different issues but nobody saw the whole picture.

## 2026-03-27: Geometry method decisions

**Sloped elements via `rs.AddSrfPt` + `rs.JoinSurfaces`.**
Why: `rs.AddBox` creates axis-aligned geometry — it CANNOT represent slopes. The v1 ramp had 0.5m steps between "flat slab" segments, which is not a walkable ramp. `AddSrfPt` creates quad faces with arbitrary corner Z values, enabling true slopes.

**Handrails via `rs.AddPipe`.**
Why: SIA 500 requires 40-50mm round/oval graspable profiles. A 40mm box does not read as graspable and fails the section test. `AddPipe` creates actual cylindrical geometry.

**Parapets as sloped elements (not boxes).**
Why: parapets must maintain constant 1.1m height above the walking surface at every point. An axis-aligned box has a fixed Z range — at the low end of the ramp it's 2.5m tall, at the high end it's 1.1m. Only sloped geometry maintains the correct height along the entire run.
