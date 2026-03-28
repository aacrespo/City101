# Lock Type 03 — Altitude North
# LOG400 Build: Master Plan
# Project ID: henna-lock03-log400
# Owner: Henna
# Created: 2026-03-27

---

## Goal

Build Lock Type 03 (Altitude North) from scratch in Rhino at LOG400 detail.
Rhino instance: `interior` (port 9003, router mode).
Critical gap: the original prompt has NO ROOF. This must be designed and added.

---

## Context

Lock 03 is the funicular/altitude lock — a building that follows a slope connecting a valley and a hilltop.
Three distinct volume types require different roof strategies:
1. Valley Station (flat RC roof)
2. Inclined Track (sloped enclosure roof — most complex)
3. Hilltop Station (flat RC roof at elevation)
4. Tower (open lattice crown — not a roof, already specified)

The LOG400 pattern follows the same system used for Lock 01 (Border):
- L300_Roof: structural slabs and parapets
- L350_Detail: connections, kickers, bearing plates, frames
- L400_Material: formwork lines, roof assembly layers, hardware, joints

Coordinate convention: meter-scale values in a centimeter-unit Rhino document.
All numbers used as-written — DO NOT multiply by 100.

---

## Phase Breakdown

```
Phase 0: Spec Roundtable         [1 session, ~45 min]
  └── 3 agents (Coordinator + Architect + Engineer)
  └── Output: lock_03_altitude_LOG400_approved.md

Phase 1: Full Build               [1–2 sessions, ~90 min]
  └── 1 executor agent (sequential Rhino calls)
  └── Part A: Base volumes + layers (LOG200–300)
  └── Part B: LOG400 detail (roof, connections, hardware)
  └── Output: complete model in Rhino + viewport captures
```

---

## Phase 0: Spec Roundtable

**Goal**: Produce the complete LOG400 execution spec for lock 03, resolving all geometry conflicts — especially the missing roof system.

**Topology**: Hierarchical (Coordinator synthesizes after parallel specialist contributions)

**Team** (3 agents):
- **Coordinator**: Runs the roundtable, issues FLAGS for unresolved issues, synthesizes the approved spec
- **Architect Agent**: Specifies all new LOG400 elements. Primary focus: roof design for each of the 3 volume types, parapets, connection to inclined track, openings and frames
- **Engineer Agent**: Validates structural logic — span/thickness ratios, slope slab construction method, drainage falls, formwork lifts, kicker placement, column bearing

**Reads**:
- `prompts/[A04_ACTIVE]_lock_type_03_altitude_north.md` (base LOG200 spec)
- `output/city101_hub/lock_01_border_LOG400_approved.md` (LOG400 pattern reference)
- `00_Workflow_v04.md` §2.5 (LOG400 per-element definitions)

**Produces**: `output/city101_hub/lock_03_altitude_LOG400_approved.md`

---

## Phase 1: Full Build

**Goal**: Build the complete LOG400 model in Rhino from scratch (instance is currently empty).

**Topology**: Flat, single executor — Rhino calls are sequential by nature.

**Team**: 1 executor agent

**Build order**:
1. Create all layers (existing LOG200 layers + new L300/L350/L400 layers)
2. Build LOG200 base volumes (all 5 elements from original prompt)
3. Add LOG400 upgrades from approved spec:
   - Roof system (valley station + hilltop station + inclined track enclosure)
   - Parapets and assembly layers
   - Structure connections (column plates, kickers)
   - Formwork lines
   - Opening frames + lintels
   - Hardware
4. Capture Perspective, Top, and Section viewports

**Instance**: `interior` (port 9003). All MCP calls must include `target: "interior"`.

---

## Dependencies

Phase 1 cannot start until Phase 0 is complete and the approved spec is written.

---

## Success Criteria

- Building clearly follows a slope — not flat
- Valley and hilltop stations have roofs with visible parapets and assembly layers
- Inclined track is enclosed with a sloped roof
- Tower crown is open lattice (no solid roof — as specified)
- All LOG400 elements present: formwork lines, kickers, bearing plates, frames, hardware
- Viewport captures confirm: "someone sees this connects two levels of a hillside"
