# Lock Type 07 — Gap Relay
# LOG400 Build Log
# Date: 2026-03-27
# MCP target: structure (port 9001)

---

## Build Sequence

### Phase 0: Spec + Roundtable

1. Wrote LOG400 execution plan grounded in Archibase:
   - Hub: octagonal RC core (10m x 10m x 7m) with star beam pattern
   - Arm A: Rail corridor (south, 6m x 13m x 4m)
   - Arm B: Lateral connection (west, 6m x 13m x 4m)
   - Arm C: Uphill/funicular (NE diagonal, 6m x 13m x 5m, 6% ramp)
   - 3 canopies at arm tips

2. Roundtable review (5 parallel agents):
   - **Structural**: 3 showstoppers (roof slab, ring beam, Arm C transfer beam)
   - **Code Compliance**: 3 violations (ramp landings, skylight fall protection, turning radius)
   - **Envelope**: 4 breaks (arm roof insulation, junction details, NE chamfer gap, arm wall thickness)
   - **Visual Coherence**: 4 issues (Canopy C rotation, parapet opacity, canopy heights, arm proportion)
   - **Constructability**: Critical arm C length/ramp conflict, diagonal geometry approach, ~40 missing elements

3. Applied 13 corrections (documented in APPROVED spec)

### Phase 1: Structure (89 objects)

| Script | Elements | Content |
|--------|----------|---------|
| 1A | 24 | Hub columns (8), radial beams (8), ring beam (8) |
| 1B | 10 | Hub walls (8), hub floor slab (1), hub floor (1) |
| 1C | 14 | Arms A+B: walls (4), floors (2), roofs (2), columns (4), beams (2) |
| 1D | 7 | Arm C: diagonal walls (2), ramped floor (1), roof (1), columns (2), transfer beam (1) |
| 1E | 15 | Canopies: 3 roofs + 12 columns |
| 1F | 19 | Foundations (14), hub roof slabs (4), NE infill glazing (1) |

**Health check**: 89 objects — PASS (>70 expected)

### Phase 2: Detail (140 objects)

| Script | Elements | Content |
|--------|----------|---------|
| 2A | 22 | SE window (5), Arm A mullions+glass (8), Arm B mullions+glass (8), skylight glass (1) |
| 2B | 29 | Circulation paths (4), turntable (1), Arm C railings (2 rails + 20 posts), landings (2) |
| 2C | 17 | Roof assembly (5), skylight frame (4), skylight guardrail (4), roof edge railings (4) |
| 2D | 48 | Formwork lines (12), expansion joints (6), base plates (18), DPC (3), splice plates (4), panel joints (5) |
| 2E | 24 | Annotations (10), door+hardware (8), drainage (4), thresholds (2) |

**Health check**: 229 total objects — PASS (>170 expected)

### Phase 3: Review

**Gate 1 — Self-review**: 1 issue (15 objects missing material metadata — TextDots + polylines). Fixed. PASS.

**Gate 2 — Bilateral**: Structure-shell-roof interfaces aligned:
- Walls to Z=7.0, roof slab at Z=7.0 ✓
- Arm roofs to Z=4.0/5.0, canopy columns match ✓
- Foundations under all columns ✓
- Ring beam ties all column heads ✓

**Gate 3 — Full model**:
- Mode A (constraint): all Z-heights match spec, all LOG400 categories present
- Mode B (visual): 3-arm star reads as junction, hub taller than arms, octagonal form legible

---

## Key Dimensions

| Element | Value |
|---------|-------|
| Hub footprint | 10.6m x 10.6m (outer wall face) |
| Hub height | 7.0m (walls) + 0.35m (slab) + 1.37m (assembly + railing) = 8.72m total |
| Arm A/B length | 13.0m |
| Arm A/B height | 4.0m |
| Arm C length | 13.0m (diagonal) |
| Arm C height | 5.0m |
| Arm C ramp rise | 0.75m (6% over 12.5m) |
| Canopy A/B height | 3.5m |
| Canopy C height | 5.0m |
| Foundation depth | -0.70m |
| Overall model extent | 38.6m x 38.6m x 9.42m |

---

## Object Inventory (229 total)

| Category | Count | Layer |
|----------|-------|-------|
| Hub walls (octagon) | 9 | Volumes |
| Hub floor | 1 | Volumes |
| Arm A walls | 2 | Volumes |
| Arm A floor | 1 | Volumes |
| Arm B walls | 2 | Volumes |
| Arm B floor | 1 | Volumes |
| Arm C walls | 2 | Volumes |
| Arm C floor (ramped) | 1 | Volumes |
| Hub columns (8) | 8 | Structure |
| Hub radial beams (8) | 8 | Structure |
| Hub ring beam (8 segments) | 8 | Structure |
| Arm A columns (2) | 2 | Structure |
| Arm A transfer beam | 1 | Structure |
| Arm B columns (2) | 2 | Structure |
| Arm B transfer beam | 1 | Structure |
| Arm C columns (2) | 2 | Structure |
| Arm C transfer beam | 1 | Structure |
| Canopy A columns (4) | 4 | Structure |
| Canopy B columns (4) | 4 | Structure |
| Canopy C columns (4) | 4 | Structure |
| Hub footings (8) | 8 | Structure |
| Arm footings (6) | 6 | Structure |
| Base plates (18) | 18 | Structure |
| Splice plates (4) | 4 | L350_Detail |
| Hub roof slabs (4) | 4 | L300_Roof |
| Arm A roof slab | 1 | L300_Roof |
| Arm B roof slab | 1 | L300_Roof |
| Arm C roof slab | 1 | L300_Roof |
| Canopy A roof | 1 | L300_Roof |
| Canopy B roof | 1 | L300_Roof |
| Canopy C roof | 1 | L300_Roof |
| Skylight frame (4) | 4 | L350_Detail |
| Skylight guardrail (4) | 4 | L350_Detail |
| Roof edge railings (4) | 4 | L350_Detail |
| Thresholds (2) | 2 | L350_Detail |
| Drainage (4) | 4 | L350_Detail |
| Roof assembly (5 layers) | 5 | L400_Material |
| Formwork lines (12) | 12 | L400_Material |
| Expansion joints (6) | 6 | L400_Material |
| Panel joints (5) | 5 | L400_Material |
| DPC (3) | 3 | L400_Material |
| SE window (frame+glass) | 5 | Openings |
| Arm A mullions+glass (8) | 8 | Openings |
| Arm B mullions+glass (8) | 8 | Openings |
| NE chamfer infill glass | 1 | Openings |
| Skylight glass | 1 | Openings |
| Door + hardware (8) | 8 | Openings |
| Circulation paths (4) | 4 | Circulation |
| Turntable circle | 1 | Circulation |
| Arm C railing rails (2) | 2 | Circulation |
| Arm C railing posts (20) | 20 | Circulation |
| Ramp landings (2) | 2 | Circulation |
| Annotations (10) | 10 | Annotations |
| **TOTAL** | **229** | |
