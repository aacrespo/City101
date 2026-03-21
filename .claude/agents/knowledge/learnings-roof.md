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
