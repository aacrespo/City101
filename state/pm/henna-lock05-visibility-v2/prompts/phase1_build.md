# Phase 1 — Build
# Lock 05 Visibility Lock — v2 Full Rebuild
# PREREQUISITE: Phase 0 must be complete (coordination_spec.md exists and is signed off)

## Setup

1. **Clean Rhino** — delete ALL existing geometry from the v1 build
2. Read `output/city101_hub/lock_05_v2/coordination_spec.md` — this is the ONLY source of truth
3. Read `output/city101_hub/lock_05_v2/element_catalog.md` — this is the build checklist

MCP target: `envelope` (port 9002)

## Team

Spawn 3 agents:

### LEAD (coordinator)
- Does NOT build geometry
- Monitors progress, runs health checks after each batch
- Resolves any remaining ambiguities by consulting the coordination_spec
- Tracks element count: actual vs. catalog

### MODELER A (structure + volumes + openings + roof)
- Builds: columns, beams, slabs, core walls, ring volumes, stair walls, ring glazing, mullions, transoms, door frames, roof slab, parapets, roof assembly
- Uses `box()` for all axis-aligned elements
- Follows element_catalog exactly — name, layer, coordinates

### MODELER B (circulation + detail + material)
- Builds: ramp sloped slabs, landings, parapets (sloped), handrails (pipes), stair flights, stair landings, base/top plates, kickers, lintels, brackets, thresholds, formwork, joints, gap cladding
- Uses `sloped_slab()` for ramp geometry and sloped parapets
- Uses `pipe_handrail()` for all handrails
- Uses `box()` for flat detail elements

## Build Sequence

### Batch 1: Modeler A — Layers + Structure + Slabs
1. Create all 8 layers
2. Build all columns (core, outrigger, roof outrigger, ramp)
3. Build all beams (transfer, roof)
4. Build all floor slabs (ground, mezzanine, ring floor, ring ceiling, stair landings at Z=5, stair ceilings at Z=9)

→ LEAD: health check. Count objects on Structure and Volumes layers.

### Batch 2: Modeler A — Core Walls + Ring
5. Build all core walls (4 faces × ~6 pieces each)
6. Build ring outer walls (4 faces × 4 pieces each)
7. Build ring inner glazing frames
8. Build stair enclosure walls (NW + SE × 4 walls each)

→ LEAD: health check. Verify wall coverage on each face.

### Batch 3: Modeler B — Ramp (sloped geometry)
9. Build ramp sloped slabs (4 runs × 1 continuous slab each, using sloped_slab)
10. Build corner landings (3 flat slabs)
11. Build entry bridge + transition
12. Build ramp start landing

→ LEAD: health check. Verify ramp Z continuity at every junction.

### Batch 4: Modeler B — Parapets + Handrails
13. Build ramp parapets (8 run parapets + 6 corner parapets, all SLOPED)
14. Build ramp handrails (8 pipes, one per parapet)
15. Build stair flights (6 per stair = 12 total, using sloped_slab)
16. Build stair landings (2 per stair = 4 total)
17. Build stair handrails (6 per stair = 12 pipes)

→ LEAD: health check. Verify handrails exist on both sides of every run/flight.

### Batch 5: Modeler A — Openings
18. Build core viewing glass (4 faces)
19. Build door frames (worker, cargo)
20. Build ring slot window glass (4 faces)
21. Build mullions (4 faces × 8 each)
22. Build transoms (4 faces × 3 each)
23. Build door openings (ramp entry, stair doors, stair exits)

### Batch 6: Modeler B — Detail + Material
24. Build base plates, top plates, ramp base plates
25. Build kickers (core + ring)
26. Build lintels (core × 4 faces + ring × 4 faces)
27. Build brackets, thresholds
28. Build roof assembly (vapor, insulation, membrane, gravel)
29. Build upstands, drip edges
30. Build formwork lines, expansion joints, facade joints
31. Build gap cladding panels
32. Build public path polyline
33. Build annotations (text dots)

→ LEAD: FINAL health check against full element_catalog.

## Verification Gates

After each batch, LEAD runs:
```python
expected = [count from element_catalog for this batch]
actual = len(rs.ObjectsByLayer(layer))
if actual < expected * 0.85:
    STOP — investigate before continuing
```

## Completion Criteria

- Every element in element_catalog is present in Rhino
- Object count matches catalog ±0 (exact match)
- No unnamed objects
- No objects on wrong layer
- Ramp Z values verified at 3 points per run (start, mid, end)
- Handrails verified: both sides of every ramp run and stair flight
