# Roof Modeling Learnings

Techniques discovered while modeling. Updated by agents after each build round.

---

## Build 1 — Rammed Earth Cabin Roof (2026-03-21)

### 1. Angled rafter geometry via vertical offset (not perpendicular)
For the 8-corner box approach to rafters, offsetting the top face vertically by the rafter depth (24cm) rather than perpendicular to the slope is simpler and produces acceptable geometry at low pitch angles (~22 degrees). The visual difference is negligible. At steeper pitches (>30 degrees), perpendicular offset would matter more and you'd need to compute the normal vector.

### 2. Roof panel z at ridge = sill_top + slope_rise + rafter_depth, not ridge_z
The roof panel surface sits on TOP of the rafters, not at the ridge beam top. So ridge panel z = 345 (sill top) + 45 (slope rise) + 24 (rafter depth) = 414, not 410 (ridge beam top). This means the panel overshoots the ridge beam by 4cm — correct since sheathing sits on rafters, and rafters bear on the ridge beam at their underside.

### 3. Overhang coordination with ridge beam cantilever
The 60cm south/north overhang and 30cm east/west overhang must be coordinated with the ridge beam extension (30cm past walls). The ridge beam cantilever supports overhanging rafters at gable ends. Without fly rafters or outriggers at x=-30 and x=530, the panel edges are unsupported — a real build would need additional framing there.

---

## Round 1 Fixes (2026-03-21)

### 4. Rammed earth walls need minimum 60cm roof overhang on ALL sides
The initial build had only 30-40cm overhang, which is insufficient for rammed earth wall protection. Rammed earth is highly vulnerable to rain erosion — 60cm is the minimum overhang on every side (eaves and gables). When setting panel corner points, compute each coordinate as wall_face ± overhang, not wall_face ± some arbitrary extension.

### 5. Rafter tops overshooting ridge beam is expected at LOG 300
Rafters modeled as vertical-offset boxes (learning #1) will have their top face at sill_top + slope_rise + rafter_depth = 414, while the ridge beam top is at 410. This 4cm overshoot is an artifact of the simplified vertical offset approach — in reality, rafters are birdsmouth-cut to sit on the ridge beam with their top edge flush. At LOG 300 (massing/layout), this is acceptable. At LOG 400+, rafter geometry would need angled cuts at the ridge intersection.

---

## Build 2 — Cabin v2 Roof (2026-03-21)

### 6. Ridge orientation: ALWAYS confirm long axis before modeling
Cabin v2 attempt 1 had the ridge running along Y (the short 400cm axis) instead of X (the long 500cm axis). This produced a steep, wrong-looking roof. The ridge beam MUST run along the building's long axis. Before scripting any roof geometry, explicitly state: "Long axis = [X/Y], ridge runs along [X/Y], rafters slope [N-S / E-W]" and verify against the floor plan.

### 7. Sill plate placement: center on structural wall, not on plaster face
Sill plates sit on the rammed earth structure, not on the interior plaster. For a 40cm wall (y=0..40 south), the sill plate center is at y=20, which aligns with the structural wall center. The plaster inner face (y=40..42) is irrelevant for sill plate positioning. This also means the sill plate is inboard of the exterior render face.

### 8. Eave z-height calculation from slope rate
For panels with overhang past the sill plate, compute eave z from the slope rate:
- slope_rate = rise / run (e.g., 80/180 = 0.444 cm/cm)
- rafter_top_at_sill = sill_plate_top + rafter_depth (e.g., 346 + 16 = 362)
- distance from sill center to eave edge (e.g., y=20 to y=-80 = 100cm)
- eave_z = rafter_top_at_sill - distance × slope_rate (e.g., 362 - 44.4 = 317.6)
This ensures the panel surface is a true plane continuous from ridge to eave.

### 9. Sill plate cantilever through gable zone is acceptable overlap at LOG 300
Sill plates extending past the wall ends (for gable overhang rafter bearing) pass through the solid gable prisms. This geometry overlap is invisible in most views and architecturally correct — in reality, the gable would be notched around the sill plate, or the sill plate would be a separate piece within the gable. At LOG 300, the overlap is fine. At LOG 400+, model the notch or split the sill plate.

### 10. Gable render/plaster should follow triangular profile at LOG 400
In cabin v2, gable render and plaster were added as rectangular prisms (full bbox from z=330 to z=426) rather than triangular prisms matching the gable slope. At LOG 300 the excess material above the slope is hidden by the roof panel. At LOG 400+, trim these to the actual gable triangle profile.

### 11. Panel z-values for this build (cabin v2 reference)
- Sill plate top: z=346 (330 wall top + 16 plate height)
- Ridge beam: z=406..426
- Rafter bottom at ridge: z=426, rafter top at ridge: z=442 (16cm overshoot above ridge beam)
- Rafter top at sill: z=362
- Panel at ridge: z=442
- Panel at eave (80cm past sill): z=317.6
- Slope: rise=80cm / run=180cm = 24.0 degrees

### 12. Observation mode is valuable for cross-agent review
Staying alive after task completion to review the full model caught the courses 07-14 issue (appeared as partial fragments in bounding box data but were actually full rings with voids — volume analysis proved correctness). Also identified gable zero-thickness and missing gable render/plaster. Reviewing other agents' work through bounding box analysis is an effective quality gate even without visual inspection.
