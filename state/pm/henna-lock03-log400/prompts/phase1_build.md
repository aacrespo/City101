# [A04_ACTIVE] Lock Type 03 — Altitude North
# Phase 1: Full Build (LOG200 → LOG400)
# PM Project: henna-lock03-log400

---

## Prerequisites

Before running this prompt:
- [ ] Phase 0 is complete: `output/city101_hub/lock_03_altitude_LOG400_approved.md` exists
- [ ] Rhino instance `interior` (port 9003) is connected and empty
- [ ] Router MCP is active (run `mcpstart` in Rhino, port 9003)

---

<context>

## Your role
You are a Rhino executor. You build the complete Lock Type 03 model from scratch at LOG400.
You work alone — no parallel agents. You call Rhino sequentially, batching Python scripts per section.

## Rhino instance
- Target name: `interior`
- Port: 9003
- All MCP calls: `target: "interior"`
- Units: centimeters (but all coordinates are meter-scale values — use numbers as-written, do NOT multiply by 100)

## Source of truth
Read `output/city101_hub/lock_03_altitude_LOG400_approved.md` FIRST.
That spec is your complete build instruction. This prompt tells you HOW to execute, the spec tells you WHAT to build.

## Execution strategy

### Part A — Layers and LOG200 base (do first)
1. Create all layers — existing LOG200 layers + 3 new LOG layers from spec
2. Build LOG200 volumes as solid boxes on their respective layers:
   - Valley Station → `Type_03_Altitude::Volumes`
   - Inclined Track → `Type_03_Altitude::Volumes`
   - Hilltop Station → `Type_03_Altitude::Volumes`
   - Tower → `Type_03_Altitude::Volumes`
   - Terrain Proxy → `Type_03_Altitude::TerrainProxy` (surface, not solid)
3. Add structure elements (columns, beams) → `Type_03_Altitude::Structure`
4. Add circulation polyline + midpoint landing → `Type_03_Altitude::Circulation`
5. Add annotation text dots → `Type_03_Altitude::Annotations`
6. Capture: `Perspective` viewport (zoom to fit). Confirm volumes look correct before proceeding.

### Part B — LOG400 detail (after Part A confirmed)
Build in this order, one Python script per batch:

1. **Create L300_Roof, L350_Detail, L400_Material layers** (if not already done)
2. **Roof slabs** — valley station, hilltop station (flat boxes per spec)
3. **Parapets** — all parapet boxes per spec (note which faces have NO parapet)
4. **Inclined track roof** — sloped slab. Use method specified in approved spec (either tilted Brep or approximation)
5. **Tower crown** — X-brace members + cap plates (NO roof slab)
6. **Roof assembly layers** — insulation, membrane, gravel for valley + hilltop
7. **Parapet edge conditions** — upstands + drip edges
8. **Formwork lines** — all lift lines in one batch script
9. **Kickers** — all wall perimeters in one batch script
10. **Column base plates + top plates** — all in one batch script
11. **Track beam connections** (if specified)
12. **Opening frames + lintels** — in one batch script
13. **Tower bracing + cap plates** (if not done in step 5)
14. **Annotations** — add any missing text dots from spec

### Part C — Verification captures
After build complete:
- Perspective view (zoom to fit)
- Top view
- Section cut at X=0 (use Rhino section command or capture front view to approximate)
- Confirm the slope is visible, the roof is present, the tower crown is open

</context>

---

<instructions>

## Step-by-step execution

### Step 1: Read the approved spec
Read `output/city101_hub/lock_03_altitude_LOG400_approved.md` in full before writing any Rhino commands.
Note: total element count, build order, any special method notes for the sloped slab.

### Step 2: Check Rhino connection
Use `rhino_list_instances` to confirm `interior` is connected.

### Step 3: Build in batches
For each batch:
1. Write a Python script using `rhino_execute_python_code` with `target: "interior"`
2. Include all elements for that batch in one script
3. If the script fails: read the error, fix the issue, retry. Do not skip.
4. After each major batch (layers, volumes, roof, LOG400 details): capture a viewport to verify progress.

### Step 4: Python coding pattern
Use this pattern for all box geometry:
```python
import rhinoscriptsyntax as rs

# Set layer (create if missing)
if not rs.IsLayer("Type_03_Altitude::L300_Roof"):
    rs.AddLayer("Type_03_Altitude::L300_Roof", (230, 200, 50))

# Build a box from corner points
pt1 = rs.CreatePoint(-8, -5, 6.0)
pt2 = rs.CreatePoint(8, 5, 6.3)
box = rs.AddBox(rs.BoundingBox([pt1, pt2]))
rs.ObjectLayer(box, "Type_03_Altitude::L300_Roof")
rs.ObjectName(box, "L300_valley_roof_slab")
```

For the sloped track roof (if spec calls for a tilted Brep):
```python
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

# Sloped slab: 4 bottom corners + 4 top corners (top offset perpendicular to slope)
# Slope: 16m rise / 30m run, angle ≈ 28°
# Perpendicular thickness: 0.2 units (200mm)
# Perpendicular vector: normalize(-dZ, 0, dY) × 0.2 = normalize(-16, 0, 30) × 0.2
import math
run, rise = 30.0, 16.0
length = math.sqrt(run**2 + rise**2)  # 34.0
nx, nz = -rise/length * 0.2, run/length * 0.2  # perpendicular outward normal × thickness

# Bottom face corners (the slope underside at the wall-top line)
bl = rg.Point3d(-3, 5,  6.0)   # bottom-left  (valley end)
br = rg.Point3d( 3, 5,  6.0)   # bottom-right
tr = rg.Point3d( 3, 35, 22.0)  # top-right    (hilltop end)
tl = rg.Point3d(-3, 35, 22.0)  # top-left

# Top face corners (offset by perpendicular normal × thickness)
bl_t = rg.Point3d(bl.X + nx, bl.Y, bl.Z + nz)
br_t = rg.Point3d(br.X + nx, br.Y, br.Z + nz)
tr_t = rg.Point3d(tr.X + nx, tr.Y, tr.Z + nz)
tl_t = rg.Point3d(tl.X + nx, tl.Y, tl.Z + nz)

# Build as 6-face Brep
bottom = rg.Brep.CreateFromCornerPoints(bl, br, tr, tl, 0.001)
top    = rg.Brep.CreateFromCornerPoints(bl_t, br_t, tr_t, tl_t, 0.001)
# Use Loft or CreateFromSurface for side faces — or use simpler ExtrudeSrf
# Simplest: loft between bottom and top face edges
# NOTE: If this method fails, fall back to a flat bounding box approximation and note it.
```

### Step 5: Final captures
After all geometry is placed:
```
rhino_capture_viewport(target="interior", viewport="Perspective", zoom_to_fit=True, width=1200, height=800)
rhino_capture_viewport(target="interior", viewport="Top", zoom_to_fit=True, width=1200, height=800)
rhino_capture_viewport(target="interior", viewport="Front", zoom_to_fit=True, width=1200, height=800)
```

### Step 6: Write a build report
Write a brief report to `output/city101_hub/lock_03_altitude_LOG400_BUILD_REPORT.md`:
- Element count by section (planned vs built)
- Any elements skipped + reason
- Any geometry method changes (e.g. sloped slab → flat approximation)
- Viewport capture status
- Rhino instance state

</instructions>

---

## Fallback rules

- If a complex geometry method (Brep loft, sweep) fails after 2 attempts → use a flat box approximation and note it in the build report.
- If a script creates objects on the wrong layer → use `rs.ObjectLayer(obj_id, correct_layer)` to fix.
- If the Rhino connection drops → re-check `rhino_list_instances` and retry the last script.
- If an element count doesn't match → keep building, note the discrepancy in the report.

---

## Element count to expect (estimate)

| Section | Type | Approx count |
|---------|------|-------------|
| LOG200 base | Volumes (5) + Structure (columns, beams, supports) + Circulation | ~20 |
| L300_Roof | Slabs (3) + Parapets (~8) | ~11 |
| L300_Roof | Inclined track slab (1) | 1 |
| L400_Material | Assembly layers (valley + hilltop: 3 each) | 6 |
| L400_Material | Upstands + drip edges | ~12 |
| L400_Material | Formwork lines | ~12 |
| L350_Detail | Kickers | ~16 |
| L350_Detail | Column plates (base + top, valley + hilltop) | ~16 |
| L350_Detail | Opening frames + lintels | ~12 |
| L350_Detail | Tower X-braces + cap plates | ~6 |
| **Total** | | **~112** |
