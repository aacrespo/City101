# Rhino Modeling Playbook

How to model architecture in Rhino via MCP. Read this before any modeling session. Update after builds.

Two halves: HOW to think about modeling (assemblies, connections) and HOW to drive the tool (rhinoscriptsyntax, MCP).

See also: `claudes-corner/2026-03-21_how-to-model-architecture.md` for the full architectural study notes — wall/floor/roof assemblies, connection types, vapor rules, stairs. This playbook is the operational distillation.

## Team Builds

When modeling with agent teams (TeamCreate), follow `workflows/agent-team-modeling-v2.md` for coordination. Complete Phase 0 (site data card, bill of objects, interface registry, layer tree) before spawning any agents. This playbook covers HOW to model; the workflow covers HOW to coordinate the team.

---

## The Core Rule

**Everything has a thickness. Nothing is just a surface.**

A wall is not a box — it's a sequence of layers. A roof panel is not a surface — it's battens, counter-battens, sheathing, tiles. Terrain is not a plane — it's compacted ground. If you model anything as a zero-thickness surface, you've failed the section test. Every element in a building has material, thickness, and assembly logic.

**Model assemblies, not surfaces.**

Query archibase for the assembly layers before modeling any element. Don't guess — look up the real construction stack. For example, a timber roof is not "a surface on rafters" — it's:
- Chevrons / solives (rafters — structural)
- Pannes (purlins — if used)
- Contrelattage (counter-battens)
- Lattage (battens)
- Tuiles / couverture (tiles / roofing)

Each layer has a thickness from archibase. Model each one.

Put a clipping plane through your model: can you read a credible section? If you see a single rectangle or a zero-thickness line, you failed. If you see layers with metadata, you succeeded.

```python
# WRONG: concept model
wall = rs.AddBox(corner, 6.0, 0.2, 3.0)

# RIGHT: assembly model
layers = [
    {"name": "exterior_render", "t": 2, "mat": "lime_render"},
    {"name": "rammed_earth", "t": 40, "mat": "earth_rammed"},
    {"name": "interior_plaster", "t": 2, "mat": "lime_plaster"},
]
offset = 0
for layer in layers:
    geom = make_layer(origin, length, layer["t"], height, offset)
    rs.ObjectLayer(geom, "Wall_Assembly::{}".format(layer["name"]))
    rs.SetUserText(geom, "material", layer["mat"])
    offset += layer["t"]
```

---

## Rhinoscriptsyntax Techniques

### Boxes
- `rs.AddBox(pts)` — 8 corner points: [0-3] bottom face, [4-7] top face, counter-clockwise from above
- Helper for axis-aligned boxes:
  ```python
  def box(x, y, z, L, W, H):
      pts = [(x,y,z),(x+L,y,z),(x+L,y+W,z),(x,y+W,z),
             (x,y,z+H),(x+L,y,z+H),(x+L,y+W,z+H),(x,y+W,z+H)]
      return rs.AddBox(pts)
  ```
- For angled elements (rafters): compute all 8 corners from slope geometry

### Hollow Rings (monolithic wall courses, foundation strips)
- **Best**: outer + inner closed polylines → `rs.AddPlanarSrf([outer, inner])` → `rs.ExtrudeSurface(srf, path, cap=True)`
- Creates a TRUE monolithic ring — no corner joints
- Always check return value — `AddPlanarSrf` can fail silently
- **Fallback**: boolean union of 4 boxes (works but has corner joints)
- **With openings**: boolean cutting is unreliable. Use multiple boxes instead.

### Surfaces
- `rs.AddSrfPt(pts)` for 3 or 4 point surfaces (terrain, roof panels)
- Roof panels: extend beyond walls for overhang

### Lines and Polylines
- `rs.AddPolyline(pts)` — close by repeating first point as last
- Course annotation lines: trace BOTH outer and inner wall perimeter (two closed polylines per course)

### Metadata
- `rs.SetUserText(obj, key, value)` — always strings
- Minimum: `material`, `source` (provenance of the dimension)
- `rs.GetUserText(obj)` → list of keys; `rs.GetUserText(obj, key)` → value

### Layers
- `rs.CurrentLayer("Parent::Child")` before creating objects
- Agents use EXISTING layers. Don't create ad-hoc ones.
- Layer structure should mirror building systems, not modeling sequence

### Script Execution
- Break large builds into 3-5 separate `rhino_execute_python_code` calls
- Always `import rhinoscriptsyntax as rs` at top of each script
- Print summary at end (object count, key dimensions)

---

## Common Failures

| Problem | Cause | Fix |
|---------|-------|-----|
| `AddPlanarSrf` returns None | Curves not coplanar or not closed | Verify z-values match, verify closure |
| Boolean union fails | Complex geometry, near-tangent surfaces | Build constructively instead of subtractively |
| Script timeout | Too much geometry in one call | Split into multiple scripts |
| Objects on wrong layer | Forgot `rs.CurrentLayer()` | Set layer before EVERY creation block |
| Non-planar box face | Corner points don't share a plane | Compute corners carefully, especially for angled elements |

---

## Connections: Where Architecture Happens

Model the CONNECTION, not just the elements on either side. Key interfaces:

| Interface | What to model | Common mistake |
|-----------|--------------|----------------|
| Wall base → plinth | Capillary break, width change | Wall sitting directly on grade |
| Lintel → wall | Bearing surface (≥20cm each side), timber only for earth | Steel lintel, no bearing |
| Sill plate → wall top | Timber plate bedded in lime mortar | Rafter sitting directly on wall |
| Rafter → sill plate | Angled connection, bolt positions | Floating rafter |
| Foundation → wall | Width transition (foundation wider) | Same width as wall |
| Roof overhang → wall face | Min 60cm (rammed earth), protects wall | No overhang |

---

## Rammed Earth Modeling

- Courses are monolithic rings — NEVER 4 boxes meeting at corners
- Course height: 10-15cm (compaction layer)
- Wall sits on plinth (z = plinth_height), not on grade
- Plinth: 5cm overhang each side typical
- Openings: max 1/3 of wall length between structural elements
- Lintels: timber or stone ONLY (never steel in contact with earth)
- Render layers: 2cm lime/earth exterior, 2cm interior
- Foundation must be below frost depth (80cm in Swiss lowland)

## Timber Modeling

- Rafters: compute 8 corner points from slope angle
- Connections: model the joint, not just the members
- Never glue on site — only factory conditions
- Sill plates: 10×15cm typical, centered on wall
- Bearing: always model the bearing surface explicitly

## Openings: More Than Voids

Openings are not just holes in walls. A complete opening includes:
- **Lintel**: timber/stone beam with bearing (≥20cm into wall). Wall courses must be NOTCHED to receive the lintel — it's part of the construction, not floating in a void.
- **Course above lintel**: must sit ON the lintel at the opening span, not resume as a full ring ignoring the lintel below.
- **Door leaf**: frame, panel, hinges. Model the actual door.
- **Window frame + glass**: mullions, glass pane, reveal depth.
- **Reveals / jambs**: the cut face of the wall at openings needs finish (lime render return).
- **Threshold**: needs foundation under it — a threshold can't float over a gap in the plinth.
- **Sill**: sloped for drainage (5-10° outward) at higher LOD.

## Review Checklist

After building, verify:
- [ ] Clipping plane shows readable section (not just rectangles)
- [ ] **No zero-thickness elements** — every surface should be a solid with real thickness
- [ ] Every object has material metadata
- [ ] Every dimension traces to a source (archibase, norm, design decision)
- [ ] Connections are modeled, not assumed
- [ ] Missing elements? (roof ASSEMBLY not just structure, terrain not just a plane)
- [ ] Openings have lintels with proper bearing AND notched courses
- [ ] Door and window leaves modeled (not just voids)
- [ ] Layer organization matches building systems
- [ ] **Archibase queried** for assembly layers before modeling any element

---

*Seeded: 2026-03-21 — from POC wall test, cabin v1/v2, and study notes (claudes-corner/2026-03-21_how-to-model-architecture.md)*
