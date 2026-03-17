# Script Test Log — Wave 2

**Date:** 2026-03-17
**Branch:** `andrea/prototypology-v2`
**Rhino document:** Untitled (new), units set to Meters
**Tester:** Claude Code (Cairn Code)

---

## Pre-flight

- [x] Rhino open, MCP connected
- [x] Document units changed from Millimeters to Meters (scripts use meter-scale coordinates)
- [x] Read modeling workflow, LOG conventions, lock concepts

---

## Script 1: Lock 03 — Morges Temporal Lock

**File:** `lock_03_morges_temporal.py`
**Result:** PASS (no errors, ran on first attempt)

### Errors & Fixes
None — script ran cleanly.

### Layer & Object Inventory

| Layer | Objects | Content |
|-------|---------|---------|
| Lock_03::Volumes | 3 | Night Chamber, Gate Threshold, Dawn Chamber envelopes |
| Lock_03::FloorPlates | 6 | Ground slab, 2 upper floors, 3 roof slabs |
| Lock_03::Structure | 20 | Columns at 5m rhythm (8 night + 8 dawn + 4 gate) |
| Lock_03::Openings | 10 | Dawn east window, night entrance, 2 gate passages, 6 secondary windows |
| Lock_03::Circulation | 2 | Night stair, dawn stair |
| **Total** | **41** | All BREP |

### Bounding Box
`[-17.5, -5.5, -0.3]` to `[17.5, 5.5, 8.3]` = 35m x 11m x 8.6m
(Slightly larger than spatial plan's 34x10x8 due to openings extending 0.5m past envelope walls — correct behavior)

### Screenshot Descriptions
1. **Perspective**: Three-part composition — Night chamber (west, blue-grey), Gate threshold (center, taller at 8m), Dawn chamber (east). Columns at regular intervals. Amber openings visible on facades.
2. **Top**: Plan layout shows column grid at 5m spacing, opening volumes on north/south facades, stair enclosures flanking the gate.
3. **Front**: Elevation clearly shows height difference — 6m chambers, 8m gate threshold rising above. Floor plates and roof slabs visible.
4. **Right (side)**: Cross-section through Y-Z shows full 10m depth, gate columns taller, openings and floor plates at correct heights.

### LOG Compliance
- [x] Volumes present (LOG 200)
- [x] Floor plates present (LOG 200)
- [x] Structural elements / columns (LOG 300)
- [x] Openings (LOG 300)
- **Assessment:** Meets claimed LOG 200-300

### Notes for Wave 4
- No issues. Clean script, ready for LOG upgrade.
- Could add: wall thicknesses, facade panels, interior partitions for LOG 350+

---

## Script 2: Lock 05 — CHUV Gradient Dispatcher

**File:** `lock_05_chuv_gradient.py`
**Result:** FAIL on first run, PASS after fix

### Errors & Fixes

**Error:** `Precision not allowed in integer format specifier`
- **Cause:** Line 202 uses `"{:.0f}".format(level_idx, x, y)` — IronPython (Rhino's Python) does not allow the `{:.0f}` format specifier on integer values (from `range()`)
- **Fix:** Changed `{:.0f}` to `{}` in column naming
- **Fixed file:** `lock_05_chuv_gradient_v2.py`

### Layer & Object Inventory

| Layer | Objects | Content |
|-------|---------|---------|
| Lock_05::Terrain | 2 | Sloped ground wedge (15% grade) |
| Lock_05::Volumes | 8 | 4 level envelopes (some split into multiple breps by Rhino) |
| Lock_05::FloorPlates | 16 | 4 floor slabs + 4 roof slabs (some split) |
| Lock_05::Structure | 53 | Columns on 5m grid, excluding central void zone |
| Lock_05::Openings | 12 | Central atrium void, 8 north glazing panels, south entrance, emergency access |
| Lock_05::Circulation | 6 | 3 ramps (wedge geometry) + 3 inner guardrails |
| **Total** | **97** | All BREP |

**Note:** Script reports 82 objects created, but Rhino layer counts show 97. The discrepancy is because `rs.AddBox()` with non-coplanar corner points (terrain wedge, ramps, guardrails) may produce multi-surface polysurfaces that Rhino counts as multiple objects. Geometry is visually correct.

### Bounding Box (Lock_05 portion)
Approximately `[-14, -2, -3]` to `[14, 36, 14.3]` = 28m x 38m x 17.3m
(Includes terrain wedge extending beyond building footprint)

### Screenshot Descriptions
1. **Perspective**: 4 levels stepping upward from south to north, terrain wedge visible beneath. Central void gap, ramps (terracotta) on east side connecting levels.
2. **Top**: Column grid with clear void gap in center (6m wide). Overlapping level footprints visible. Ramp zone on east edge.
3. **Front**: Stepped massing reads clearly — each level offset 3.5m vertically and 8m in Y. Terrain wedge extends below.
4. **Right (side)**: Hero view — 4 ascending levels, diagonal ramps, terrain slope. The gradient concept is immediately legible.

### LOG Compliance
- [x] Volumes present (LOG 200)
- [x] Floor plates present (LOG 200)
- [x] Structural elements / columns (LOG 300)
- [x] Openings (LOG 300)
- [x] Terrain reference (bonus)
- **Assessment:** Meets claimed LOG 200-300

### Notes for Wave 4
- Object count discrepancy (82 vs 97) should be investigated — likely wedge geometry creating split breps
- Central void is modeled as a solid box on the Openings layer — for LOG 350+, consider boolean subtraction
- Ramp gradient (35%) is steep for accessibility — compressed for model clarity, note in LOI

---

## Script 3: Lock 07 — Rennaz Bridge Lock

**File:** `lock_07_rennaz_bridge.py`
**Result:** PASS (same `{:.0f}` bug existed but was pre-fixed before execution)

### Errors & Fixes

**Error (prevented):** Same IronPython `{:.0f}` format bug as Lock 05 — present in multiple lines (column, beam, post, opening, tactile strip naming)
- **Fix:** Changed all `{:.0f}` to `{}` and wrapped floats in `int()` where needed
- **Fixed file:** `lock_07_rennaz_bridge_v2.py`

### Layer & Object Inventory

| Layer | Objects | Content |
|-------|---------|---------|
| Lock_07::Volumes | 3 | Station platform, bridge span, hospital ramp envelopes |
| Lock_07::FloorPlates | 5 | Station deck, bridge deck, ramp (wedge), station roof, bridge roof |
| Lock_07::Structure | 26 cols + 22 beams + 22 posts | V-columns, station columns, ramp columns, bay frames |
| Lock_07::Openings | 25 | 20 lateral bay openings (10 east + 10 west), station south entrance, 4 station side openings |
| Lock_07::Circulation | ~15 | Lane divider, 10 tactile strips, 2 ramp guardrails, 2 bridge guardrails |
| **Total** | **118** | All BREP |

### Bounding Box (Lock_07 portion)
Approximately `[-6.3, -45.5, -0.25]` to `[6.3, 45, 8.2]` = 12.6m x 90.5m x 8.45m

### Screenshot Descriptions
1. **Perspective**: Long linear bridge structure — wider station platform (south/foreground), narrow bridge span with bay frames, hospital ramp descending (north/background). Most detailed of the three scripts.
2. **Top**: Linear plan clearly shows station widening (12m) narrowing to bridge (6m). Bay rhythm at 6m spacing. Lane divider strip visible down center. Tactile strips on west (slow) lane.
3. **Front**: Elevated deck at 4m above ground, station wider than bridge span. Columns supporting from ground level. Bay frame posts and beams creating structural rhythm.
4. **Right (side)**: Profile view — elevated walkway on V-columns, station end (left), long bridge span, descending hospital ramp (right) to grade. Clean horizontal connector reading.

### LOG Compliance
- [x] Volumes present (LOG 200)
- [x] Floor plates / decks present (LOG 200)
- [x] Structural elements — columns, beams, posts (LOG 300)
- [x] Openings — lateral views, entrances (LOG 300)
- [x] Circulation detail — lane divider, tactile strips, guardrails (approaching LOG 350)
- **Assessment:** Meets LOG 200-300, with some elements at LOG 350

### Notes for Wave 4
- Most detailed script — already has tactile strips, lane dividers, guardrails
- Ramp guardrails use wedge geometry (non-coplanar AddBox) — may create split breps
- Bay frame system (beam + post pairs at 6m) is a strong structural rhythm — good base for LOG 400 mullion/cladding detail
- Hospital ramp at 26.7% grade (4m over 15m) — steep for accessibility, note in LOI

---

## Cross-Script Patterns

### Common Error
All three scripts used `{:.0f}` format specifiers for naming objects. This works in CPython but fails in IronPython (Rhino's Python engine) when the value is an integer from `range()`. Lock 03 happened to avoid this because its format strings used `{:.0f}` only on float values.

**Fix applied:** Replace `{:.0f}` with `{}` (or `int()` wrapper) in all scripts.

### Geometry Notes
- `rs.AddBox()` with non-coplanar corners (wedges for terrain, ramps, guardrails) may produce split brep objects, inflating object counts vs. what the script tracks
- All scripts use the `box()` helper correctly for axis-aligned geometry
- All scripts follow the spatial plan convention from `00_Workflow_v04.md` Section 3.2.1

### LOG Summary

| Script | Claimed LOG | Actual LOG | Elements Present |
|--------|-------------|------------|-----------------|
| Lock 03 | 200-300 | 200-300 | Volumes, floors, columns, openings, stairs |
| Lock 05 | 200-300 | 200-300 | Volumes, floors, columns, openings, ramps, terrain, void |
| Lock 07 | 200-300 | 200-350 | Volumes, decks, columns, beams, posts, openings, lane dividers, tactile strips, guardrails |

### Ready for Wave 4 (LOG Upgrade)
All 3 scripts provide a solid LOG 200-300 base. For LOG 400:
- Add wall thicknesses and facade panels
- Boolean-subtract openings from volumes
- Add material assignments via object attributes
- Refine ramp grades to realistic accessibility standards
- Add interior partitions and program zones
