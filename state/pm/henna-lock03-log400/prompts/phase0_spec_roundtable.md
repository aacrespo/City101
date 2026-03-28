# [A04_ACTIVE] Lock Type 03 — Altitude North
# Phase 0: LOG400 Spec Roundtable
# PM Project: henna-lock03-log400

---

<context>

## What this session produces
A complete, approved LOG400 execution spec for Lock Type 03 (Altitude North):
`output/city101_hub/lock_03_altitude_LOG400_approved.md`

This spec will be read verbatim by an executor agent in Phase 1 to build the model.
It must be unambiguous, coordinate-exact, and resolve the MISSING ROOF before any executor touches Rhino.

## Base geometry (LOG200 — existing spec)

From `prompts/[A04_ACTIVE]_lock_type_03_altitude_north.md`:

### Coordinate system
All values are METER-SCALE in a centimeter-unit Rhino doc. Use numbers as-written. DO NOT multiply by 100.
X = transverse axis (±8m from centerline)
Y = slope axis (0 = valley, 45 = hilltop)
Z = vertical (0 = valley floor, 28 = hilltop station roof)

### Volumes
| Volume | X | Y | Z | Notes |
|--------|---|---|---|-------|
| Valley Station | [-8, 8] | [-5, 5] | [0, 6] | Arrival hall, grounded |
| Inclined Track | [-3, 3] | [5, 35] | [6, 22] | Slope: 16m rise / 30m run |
| Hilltop Station | [-8, 8] | [35, 45] | [22, 28] | Departure hall, elevated |
| Tower | [-3, 3] | [35, 41] | [22, 32] | Sits above hilltop station |
| Terrain Proxy | — | [-5, 45] | [-1, 21] | Tilted surface, NOT a solid roof |

### Existing LOG200 layers (do NOT rename or alter)
```
Type_03_Altitude::Volumes       — RGB(255, 212, 59)
Type_03_Altitude::Circulation   — RGB(255, 230, 140)
Type_03_Altitude::Structure     — RGB(180, 150, 40)
Type_03_Altitude::Openings      — RGB(255, 225, 100)
Type_03_Altitude::Annotations   — RGB(255, 240, 180)
Type_03_Altitude::TerrainProxy  — RGB(120, 110, 80)
```

### Openings (LOG200 spec)
- Valley south entry: Y=-5, X=[-4,4], Z=[0.5, 4.5]
- Hilltop north exit: Y=45, X=[-4,4], Z=[22.5, 26.5]
- Inclined track sides: continuous slot windows, X=±3, Z varies with slope, 1.5m tall
- Tower top: open all 4 faces, Z=[28,32], X=[-2,2], Y=[36,40]
- Midpoint landing window: X=[-3,3], Y=20, Z=[14.5, 16.5]

## LOG400 pattern reference

From `output/city101_hub/lock_01_border_LOG400_approved.md`, the LOG400 upgrade adds:

### New layers (to create)
```
Type_03_Altitude::L300_Roof     — roof structural slabs, parapets
Type_03_Altitude::L350_Detail   — connections, kickers, bearing plates, frames
Type_03_Altitude::L400_Material — formwork lines, roof assembly layers, hardware, joints
```

### Typical LOG400 elements (per 00_Workflow_v04.md §2.5)
- **L300_Roof**: RC roof slabs (span/30 thickness rule) + parapets (500mm tall, 300mm thick)
- **L350_Detail**: Column base plates, column top plates, beam brackets, wall kickers (50×50mm at Z=0)
- **L400_Material**: Roof assembly layers (XPS insulation 120mm + membrane 5mm + gravel 50mm), waterproofing upstand at parapet base, drip edge at parapet top, formwork lift lines (every 2400mm), expansion joints (at 10m centers), gate hardware (bolts, hinges), opening frames (100×100mm steel hollow section) + RC lintels

## The critical missing piece: ROOF

The original spec has NO roof geometry on any volume.
Three distinct roof conditions must be designed:

### 1. Valley Station roof (Z=6 plane)
- Flat RC slab on top of station walls (top at Z=6)
- Span: 10m (Y direction) → span/30 = 333mm → round up to 300mm for consistency
- Parapets on East, West, South faces (North opens to inclined track — NO parapet there)
- Full assembly layers (insulation + membrane + gravel) inside parapets

### 2. Hilltop Station roof (Z=28 plane)
- Flat RC slab on top of station walls (top at Z=28)
- Same span/thickness as valley station
- Parapets on East, West, North faces (South opens to inclined track — NO parapet there)
- Full assembly layers inside parapets

### 3. Inclined Track enclosure roof (SLOPE: Z=6@Y=5 → Z=22@Y=35)
- The track is enclosed — it is an inhabited space, not an open ramp
- The roof follows the slope
- Slope equation: Z = 6 + (Y - 5) × (16/30)  [i.e., 16m rise over 30m run]
- At LOG400: modeled as a sloped solid slab — use a Python Brep from 4 corner points
- Slab thickness: 200mm perpendicular to slope
- No parapets (the track walls continue up to the slab — wall IS the parapet condition)
- Assembly layers follow the slope (inset from X=±3 walls by 300mm = wall thickness)

### 4. Tower crown
- NO solid roof — open lattice, as specified
- At LOG400: model 4 X-brace members connecting the 4 corner columns at Z=28–32
- Plus 4 cap plates (horizontal boxes at column tops, Z=32)

## Structure (LOG200)
- Valley station: 4 corner columns, 350×350mm
- Hilltop station: 4 corner columns, 350×350mm
- Inclined track: 2 longitudinal beams at X=±3, following slope
- Tower: 4 corner columns, bracing at Z=25 and Z=28

## Slab span reference table (span/30 rule)
| Volume | Span direction | Span | Thickness |
|--------|---------------|------|-----------|
| Valley Station | Y = 10m | 10m | 300mm (0.3 units) |
| Hilltop Station | Y = 10m | 10m | 300mm (0.3 units) |
| Inclined Track | X = 6m | 6m | 200mm (0.2 units) |

</context>

---

<instructions>

## Team assembly

Spawn 2 specialist agents in PARALLEL. Collect their outputs. Then synthesize.

---

### AGENT 1 — Architect

**Role**: Design the complete LOG400 geometry for lock 03.

**Your output** (write to your response as structured sections):

**SECTION A — New layers**
List all 3 new layer names + RGB values (follow the pattern above).

**SECTION B — Roof system**
For each of the 4 roof conditions:
- Give exact coordinates (meter-scale) for every box or surface
- Name each element (e.g. `L300_valley_roof_slab`)
- Layer assignment
- Any geometry method notes (Box vs Python Brep for sloped elements)

**SECTION C — Assembly layers**
For each roof zone: insulation, membrane, gravel boxes (inset from parapet inner faces).
Valley and hilltop: flat boxes.
Inclined track: note the slope angle and specify how to approximate with flat boxes at each end, OR specify a sloped surface method.

**SECTION D — Parapet edge conditions**
Waterproofing upstand (20mm wide × 150mm tall) against inner parapet faces.
Drip edge (30mm × 20mm) at outer parapet top.
Give coordinates for all.

**SECTION E — Opening frames**
Steel hollow section 100×100mm framing for:
- Valley south entry (Y=-5 face)
- Hilltop north exit (Y=45 face)
- Slot windows on inclined track sides (simplified: 3 window bays along track)
RC lintel above each opening.

**SECTION F — Tower LOG400 detail**
4 X-brace members at crown level (not a roof).
4 column cap plates at Z=32.
Specify as box pairs.

**FLAG any unresolved issues** with: `FLAG [N]: [description]`

---

### AGENT 2 — Engineer

**Role**: Validate the structural logic. Read the Architect's output and check:

**CHECK 1 — Slab thickness**
Verify span/30 ratios. If any slab is under-sized, correct it and state why.

**CHECK 2 — Bearing conditions**
Confirm each slab sits ON TOP of the walls (slab bottom = wall top). Give the exact Z values for valley station walls (top at Z=6), hilltop station walls (top at Z=28), inclined track walls (top follows slope).

**CHECK 3 — Parapet geometry**
Confirm parapet thickness matches existing wall thickness (0.3 units). Confirm 500mm height above slab top. State which faces have NO parapet and why.

**CHECK 4 — Inclined slab method**
For the sloped track enclosure: is a flat-box approximation acceptable at LOG400, or must a true tilted Brep be used? Rule: if the slope is >15° and the element will appear in section drawings, a true tilted surface is required. Calculate the slope angle and give a verdict.

**CHECK 5 — Formwork lifts**
Valley station walls are 6m tall → lifts at Z=2.4 and Z=4.8.
Hilltop station walls are 6m tall → lifts at Z=24.4 and Z=26.8 (valley + 22m offset).
Tower walls are 10m tall → lifts at Z=24.4, Z=26.8, Z=29.2 (relative to Z=22 base).
Confirm or correct these values.

**CHECK 6 — Kicker placement**
50×50mm RC kicker at base of all wall perimeters (Z=[0, 0.05] for valley, Z=[22, 22.05] for hilltop, Z=[22, 22.05] for tower base).
Confirm outer face coordinates for kicker runs.

**CHECK 7 — Column plate positions**
Valley station columns at corners: (-8,-5), (8,-5), (-8,5), (8,5) — or inner corners?
Hilltop station columns at corners: same footprint but at Z=22.
State base plate dimensions (500×500mm = 0.5×0.5 units) and Z positions.

**FLAG any unresolved issues** with: `FLAG [N]: [description]`

---

### COORDINATOR — Roundtable synthesis

After both agents complete, you resolve all FLAGS and produce the final approved spec.

**Format the output as**:
```
# Lock Type 03 — Altitude North
# LOG400 Upgrade: ROUNDTABLE-APPROVED Execution Spec
# Status: APPROVED — ready for executor
# Date: 2026-03-27
```

Then:
1. `## COORDINATE SYSTEM NOTE` — state the meter-scale convention clearly
2. `## CORRECTIONS FROM ROUNDTABLE REVIEW` — table of all FLAGS and resolutions
3. `## LAYERS TO CREATE` — 3 new layers
4. `## SECTION 1 — ROOF SYSTEM (L300_Roof)` — all slabs and parapets with exact coordinates
5. `## SECTION 2 — ROOF ASSEMBLY LAYERS (L400_Material)` — insulation, membrane, gravel, upstands, drip edges
6. `## SECTION 3 — FORMWORK LINES (L400_Material)` — all lift lines
7. `## SECTION 4 — STRUCTURAL CONNECTIONS (L350_Detail)` — kickers, column plates, track beam connections
8. `## SECTION 5 — OPENING FRAMES (L350_Detail)` — frames + lintels
9. `## SECTION 6 — TOWER CROWN DETAIL (L350_Detail)` — X-braces, cap plates (NO roof slab)
10. `## EXECUTION SUMMARY` — element count table + build order + executor notes

**Executor notes must include**:
- Rhino instance: `interior`, port 9003
- All MCP calls use `target: "interior"`
- Meter-scale convention (do NOT multiply by 100)
- Sloped slab method (if FLAG resolved to use Python Brep, give the code pattern)
- Batch strategy (which elements to group in one Python script)

Write the final spec to: `output/city101_hub/lock_03_altitude_LOG400_approved.md`

</instructions>
