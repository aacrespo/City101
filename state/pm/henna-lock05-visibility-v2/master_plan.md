# Lock 05 Visibility Lock — v2 Full Rebuild
## Master Plan

**Owner:** Henna
**Created:** 2026-03-27
**Rhino:** port 9002, target `envelope`
**Archibase:** `H:\Shared drives\City 101\archibase`

---

## Problem Statement

The v1 build (361 elements) was assembled through 4 rounds of patching: build → review → fix → review → fix → review → fix. Each round uncovered problems the previous round created:

1. **Ramp geometry**: axis-aligned boxes instead of proper sloped slabs (0.5m steps, not walkable)
2. **Parapets/handrails**: boxes that don't follow slopes, handrails modeled as 4cm boxes instead of pipes
3. **Structural misplacement**: diagonal columns inside core wall footprint, had to be moved twice
4. **Missing enclosures**: stair ceilings, ground slabs, corner parapets all absent until round 3-4
5. **Missing circulation links**: no public entry, no stair doors, no stair landings until round 2
6. **Missing wall elements**: south wall was solid, east piers absent, south lintel missing until round 3-4

**Root cause:** Agents built independently without discussing interfaces first. The v3 workflow (discuss → decide → execute) was written in the workflow file but not actually followed. The lead (this session's Claude) acted as both lead AND builder, violating the "lead never builds" rule.

---

## Strategy: Discussion-First, Build-Second

This rebuild uses a fundamentally different sequence:

```
OLD:  Spec → Build → Review → Patch → Review → Patch...
NEW:  Discuss → Agree → Write shared spec → Build once → Verify
```

### Key principles:
1. **Agents discuss interfaces BEFORE any geometry exists.** Every agent proposes their system, then they negotiate where systems meet.
2. **One shared coordination document** — not separate specs. Every dimension is written once, referenced by all.
3. **Lead never builds.** Lead coordinates, resolves conflicts, runs health checks.
4. **Clean Rhino start.** Delete everything from the current file. No patching on top of patched geometry.
5. **Sloped geometry done right.** Ramps and parapets use `rs.AddSrfPt` for quad faces with different Z at each corner, not `rs.AddBox`.

---

## Phases

### Phase 0: Clean + Interface Negotiation (this session, ~20 min)
**Topology:** Flat, broad context, sequential discussion
**Team:** 4 agents (Lead + Structure + Envelope + Circulation) — NO building, discussion only
**Goal:** Produce a single shared interface document where every Z-height, every wall edge, every slab boundary, every column position is agreed upon by all agents before any geometry is created.

```
Produces:
├── coordination_spec.md — the ONE document all agents build from
├── interface_registry.md — every boundary between two systems, with owner + rule
└── element_catalog.md — every single element with name, layer, coordinates, owner
```

**What makes this different from v1:** In v1 the spec was written by one agent and errors propagated. In v2, four agents each propose their system, then they sit at a roundtable and negotiate conflicts. The output is a spec that has already survived scrutiny.

**Discussion agenda:**
1. Structure proposes: column grid, beam layout, slab levels, foundation strategy
2. Envelope proposes: wall splits, opening positions, thermal envelope trace
3. Circulation proposes: ramp geometry (true slopes), stair flights, handrails, landing sizes
4. ALL negotiate: where do your systems meet? What Z-height do you need? Where are the conflicts?
5. Lead resolves: any remaining disputes use the authority hierarchy from v3 workflow

### Phase 1: Build (this session, ~30 min)
**Topology:** Hierarchical, narrow context, parallel execution
**Team:** Lead (coordinator) + 2 modelers
**Goal:** Execute the agreed spec. Modelers build from the shared document. Lead runs health checks after each section.

**Why only 2 modelers:** Lock 02 proved that 2 careful modelers outperform 4 fast ones. The spec is already agreed — execution is mechanical.

**Build sequence:**
1. Modeler A: Structure + Volumes (columns, beams, slabs, core walls, ring volumes, stair enclosures, ground slabs)
2. Modeler B: Circulation + Detail (ramp sloped slabs, stair flights, parapets, handrails, landings)
3. Lead health check after each batch
4. Modeler A: Openings + L300_Roof (glazing, mullions, transoms, door frames, roof slab, parapets)
5. Modeler B: L350_Detail + L400_Material (base plates, kickers, lintels, brackets, roof assembly, formwork, joints, gap cladding)
6. Lead final health check

### Phase 2: Verification + Capture (this session, ~10 min)
**Topology:** Flat, single reviewer
**Team:** Lead + Reviewer
**Goal:** Section test, visual coherence, code compliance, viewport captures.

**Verification protocol:**
1. Object count per layer vs element catalog
2. Section planes (X and Y cuts) — trace envelope bottom to top
3. Ramp slope verification (measure Z delta / run length at 3 points)
4. Stair riser height verification
5. Handrail presence check (both sides of every ramp run and stair flight)
6. Fire compartment check (stair enclosures sealed — walls + floor + ceiling)
7. 4 viewport captures (perspective, top, front, right)

---

## Execution Timeline

```
Phase 0: Discussion (20 min)
  ├── 4 agents discuss interfaces
  ├── Lead compiles coordination_spec.md
  └── Roundtable: all agents verify, sign off
      │
Phase 1: Build (30 min)
  ├── Clean Rhino (delete all)
  ├── Modeler A: Structure + Volumes
  ├── Health check
  ├── Modeler B: Circulation + Detail
  ├── Health check
  ├── Modeler A: Openings + Roof
  ├── Modeler B: L350 + L400
  └── Final health check
      │
Phase 2: Verify + Capture (10 min)
  ├── Section test
  ├── Code compliance
  └── Viewport captures
```

**Total: ~60 min, 1 session**

---

## Geometry Standards (learned from v1 failures)

### Sloped elements (ramps, parapets, handrails)
**Use `rs.AddSrfPt` for each face, then `rs.JoinSurfaces` to create a closed Brep.** NOT `rs.AddBox` — boxes are axis-aligned and cannot represent slopes.

Pattern for a sloped slab:
```python
# 4 points for top face (sloped), 4 for bottom face (sloped, offset down by slab_t)
top = [(x1,y1,z1), (x2,y1,z2), (x2,y2,z2), (x1,y2,z1)]
bot = [(x1,y1,z1-t), (x2,y1,z2-t), (x2,y2,z2-t), (x1,y2,z1-t)]
# Create 6 faces: top, bottom, 4 sides
```

### Handrails
**Use `rs.AddPipe` around a polyline at 0.875m above walking surface.** Pipe radius = 0.02m (40mm diameter). NOT boxes — pipes read as graspable.

### Parapets following slope
Same `AddSrfPt` approach as ramp slabs but 1.1m tall above the walking surface at every point.

### Naming
`{System}_{Level}_{Location}_{Element}` — e.g., `Ramp_Z0_South_Slab`, `HR_F1_NW_West`
