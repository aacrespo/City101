# Phase 2 — Verification + Capture
# Lock 05 Visibility Lock — v2 Full Rebuild

## Team
Lead + 1 Reviewer agent

## Verification Protocol

### 1. Element Count Audit
```python
# Compare every layer count against element_catalog.md
# MUST be exact match — 0 tolerance
```

### 2. Section Test (2 cuts)
Place clipping planes:
- **X-section** at Y=0 — reveals: ground slab, core wall E/W, ring floor, ring ceiling, roof, gap cladding, ramp on south side
- **Y-section** at X=0 — reveals: ground slab, core wall N/S, ring floor, ring ceiling, roof, ramp on west/east sides
- Read each section bottom-to-top: is every layer present with credible thickness?

### 3. Ramp Slope Verification
At 3 points per run (start, middle, end), query the walking surface Z:
```
Grade = (Z_end - Z_start) / horizontal_distance
Must be ≤ 6% (0.06)
```

### 4. Stair Riser Verification
```
Total rise per stair = 5.0m
Risers per flight × riser height × 3 flights = total rise ± 10mm
```

### 5. Handrail Presence
```python
# For every ramp run: verify 2 pipe objects exist (inner + outer)
# For every stair flight: verify 2 pipe objects exist (left + right)
# Total expected: 8 ramp + 12 stair = 20 pipes
```

### 6. Fire Compartment (VKF)
For each stair enclosure:
- 4 walls present (Z=0 to 9)?
- Ground slab present (Z=-0.3 to 0)?
- Landing at Z=5 present?
- Ceiling slab at Z=8.75-9.0 present?
- Door to ring present?
- Exit to ground present?

### 7. Fall Protection (SIA 358)
Every elevated edge with >1m drop has either:
- Ring outer wall (solid with slot windows)
- Ring inner glazing (curtain wall)
- Parapet (1.1m above walking surface)
- Stair enclosure wall

Check: any open edges?

### 8. Accessibility (SIA 500)
- Ramp grade ≤ 6%
- Ramp width ≥ 1.5m
- Handrails both sides, 850-900mm
- Landings at every turn
- Continuous path from ground to ring

### 9. Viewport Captures
Save to `output/city101_hub/`:
- `lock_05_v2_perspective.png` (shaded, from SE, elevated)
- `lock_05_v2_top.png` (plan)
- `lock_05_v2_front.png` (south elevation)
- `lock_05_v2_right.png` (east elevation)
- `lock_05_v2_section_X.png` (section at Y=0)
- `lock_05_v2_section_Y.png` (section at X=0)

## Output
- Updated `lock_05_visibility_LOG400_build_log_v2.md` with final counts and verification results
- Viewport captures
- PASS / FAIL verdict for each check
