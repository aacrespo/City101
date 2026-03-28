# Phase 3 — Execute: Lock 02 Cargo LOG400 in Rhino
# PM Project: henna-lock02-cargo-log400
# Status: ACTIVE (run only after Phase 2 produces APPROVED spec)

---

## Your role

You are the executor for Lock Type 02 — Cargo Lock. Your job is to build all LOG400 geometry in Rhino exactly as specified in the approved spec.

**Do not interpret or redesign. Build exactly what the spec says.**

---

## Input

Read: `output/city101_hub/lock_02_cargo_LOG400_APPROVED.md`

---

## Rhino target

- Instance: `lock_02`
- Port: 9002
- All MCP calls MUST include: `target: "lock_02"`

---

## Before building

1. Run `rhino_get_scene_info` with `target: "lock_02"` to check current scene state.
2. Note what layers already exist. Do NOT recreate existing layers.
3. Identify what geometry already exists (from the LOG200–300 build).
4. Confirm the coordinate system by checking a known object (e.g., Logistics Hall volume at X=[-24,24]).

---

## Coordinate system — CRITICAL

Rhino document units: Centimeters.
All values in the spec are meter-scale (e.g., X=-24 means the number -24, displayed as "-24 cm" but conceptually -24m).

**Use spec coordinates exactly as written. Do NOT multiply by 100. Do NOT convert.**

---

## Build sequence

Follow the Build Order from the APPROVED spec exactly. General order:

1. Create 3 new layers (L300_Roof, L350_Detail, L400_Material)
2. Roof slabs (flat boxes, L300_Roof)
3. Parapets (flat boxes, L300_Roof)
4. Roof assembly layers (insulation/membrane/gravel, L400_Material)
5. Parapet edge conditions (upstands + drip edges, L400_Material)
6. Formwork lines (L400_Material) — batch as one Python script per wall system
7. Expansion joints (L400_Material)
8. Column base plates (L350_Detail)
9. Column top bearing plates (L350_Detail)
10. Cantilever brackets (L350_Detail)
11. Opening frames + lintels (L350_Detail)
12. Facade panel joints (L400_Material)
13. Floor viewing slot frames (L350_Detail)

---

## How to create geometry

Use `rhino_execute_python_code` with Box objects from two corner points. Template:

```python
import rhinoscriptsyntax as rs
import Rhino.Geometry as rg

def make_box(name, layer, x0, y0, z0, x1, y1, z1):
    pt_min = rg.Point3d(x0, y0, z0)
    pt_max = rg.Point3d(x1, y1, z1)
    bbox = rg.BoundingBox(pt_min, pt_max)
    box = rg.Box(bbox)
    brep = box.ToBrep()
    guid = scriptcontext.doc.Objects.AddBrep(brep)
    obj = scriptcontext.doc.Objects.FindId(guid)
    obj.Attributes.Name = name
    obj.Attributes.LayerIndex = scriptcontext.doc.Layers.FindByFullPath(layer, True)
    obj.CommitChanges()
    return guid

# Example:
make_box("L300_logistics_roof_slab", "Type_02_Cargo::L300_Roof", -24.0, -11.0, 5.0, 24.0, 11.0, 5.5)
scriptcontext.doc.Views.Redraw()
```

For batches of similar elements (formwork lines, base plates), build all of them in one script call.

---

## Error handling

- If a Box operation fails, try with explicit Point3d corners.
- If a layer does not exist, create it first with `rs.AddLayer()` before placing objects.
- If the target connection drops, retry once. If it fails again, note the element and continue.
- Log any skipped elements at the end.

---

## Verification

After each major section, capture a viewport to verify:
- `rhino_capture_viewport` with `target: "lock_02"`, view = "Perspective"

After all geometry is complete:
- Capture: Perspective, Top, Front views
- Capture: Right view (section cut at Y=0 if possible, or use Front)
- Report: element count per layer vs. spec

---

## Output report

When complete, write a brief session log:
- File: `output/city101_hub/lock_02_cargo_LOG400_build_log.md`
- Contents: elements built per section, any skipped elements + reason, viewport paths

---

## Success criteria

- Two-level reading is clear: heavy logistics mass below (Z=0–5), light observation corridor floating above (Z=6–10)
- Roof system visible on all zones
- Structural connections visible at column bases and tops
- Viewing slot frames visible at floor level of observation corridor
- No floating geometry, no geometry outside the building envelope
