# foundation Modeling Learnings

Techniques discovered while modeling. Updated by agents after each build round.

---

## 2026-03-21 — Foundation Agent (team build)

1. **Sublayer creation via `rhino_create_layer` tool fails for `Parent::Child` syntax** — the MCP tool throws a null reference. Workaround: use `rs.AddLayer("Parent::Child", color)` inside `rhino_execute_python_code`. This is reliable and gives full control over color.

2. **Box helper function is essential for foundation work.** The 8-point `rs.AddBox(pts)` API is error-prone for axis-aligned boxes. A simple `box(x, y, z, L, W, H)` wrapper that computes the 8 corners from origin + dimensions eliminates mistakes. Define it once per script call since state does not persist.

3. **Door gap in plinth: use multiple boxes, not boolean subtraction.** The playbook warns that boolean cutting is unreliable. Splitting the south plinth into `Plinth_South_Left` and `Plinth_South_Right` with a gap at x=205-295 worked cleanly and is easier for downstream agents to reason about than a single object with a cut.

4. **Splash aprons protect rammed earth bases from rain erosion.** A thin concrete apron (60cm wide, at grade level) around the plinth perimeter prevents rain splash-back from eroding the rammed earth wall base. Modeled as a ring surface using boolean difference of outer and inner rectangles — boolean worked here because it was a simple planar surface, not a solid. Material: concrete C25/30.

## 2026-03-21 — Structure Agent (cabin-v2 team build)

5. **DPC (damp-proof course) is a critical connection element.** The playbook's connection table lists "Wall base -> plinth: Capillary break" — don't skip it. A 0.5cm bitumen membrane at the plinth-wall interface (z=30) prevents rising damp into rammed earth. Model as thin boxes matching plinth footprint with door gap. The 0.5cm overlap with Course_01 is acceptable — it represents an embedded membrane.

6. **Bounding box audits can be misleading for extruded profiles with voids.** Courses modeled as extrusions (type=16) of ring profiles with door/window cutouts show bounding boxes spanning the full perimeter — the voids are invisible to `rs.BoundingBox()`. Use volume checks (`rs.SurfaceVolume()`) to verify voids exist, not bounding box dimensions. This caused a false alarm in Round 1 where courses 7-14 appeared to be SE corner fragments when they were actually complete rings.

7. **Apron material should be gravel, not concrete.** The spec calls for gravel drainage apron (material=gravel_drainage). The previous learning incorrectly notes concrete C25/30. Gravel allows water to drain away rather than pooling against the plinth.

8. **Foundation publishes coordination geometry for downstream agents.** After building, immediately send to team lead: plinth top z, finish floor z, outer/inner perimeters, door gap coordinates, foundation strip extents. Other agents (walls, openings, roof) depend on these numbers to align their work. Publishing early unblocks parallel work.

## 2026-03-22 — Structure Agent (cabin-v3 stone masonry build)

9. **No stone wall assembly in archibase — construct your own.** The `ConstructionDB.get_assembly('stone_wall')` returns None. Use `stone_masonry.md` knowledge file to derive layers: 2cm lime render (exterior) + 36cm molasse sandstone (structural) + 2cm lime plaster (interior) = 40cm total, matching SIA 266 minimum for single-leaf load-bearing.

10. **Corner overlap convention matters for coursed walls.** When building 4 walls as boxes, the South and North walls should run full building length (x=0 to 800), while West and East walls fill between the inner faces (y=36 to y=564). This prevents double-thickness stone at corners and gives a clean overlap pattern. The same convention applies to render/plaster layers.

11. **Align openings to course boundaries.** Rather than placing openings at exact spec dimensions (door z=0-210, windows z=90-210), round to the nearest course boundary (20cm increments). Door: z=0-200, windows: z=80-200. This is how real coursed masonry works — you don't cut stones mid-course. The Openings agent adds lintels at the top of the void.

12. **Wall plate (sabliere) section: 15x10cm oak, centered on structural stone.** The plate sits at z=260 (top of 13 courses x 20cm), centered on the 36cm stone with 10.5cm offset from exterior face. South/North plates run full x-length; West/East fit between them. This gives the timber frame agent a level bearing surface at z=260-270.

## Training Session 2 — 2026-03-22 (Deplazes book exercises)

### DPC at sole plate
**Rule:** Damp-proof course at the timber-to-concrete transition is a separate object — 3mm bitumen felt strip. It sits between the timber sole plate and the concrete plinth/stem wall. Model it explicitly.
**Source:** Deplazes p.417, timber platform frame plinth.

### Basement floor positioning
**Issue:** Basement floor slab extended under the concrete wall, causing 48,000 cm³ overlap.
**Fix:** Floor slab must start at the INNER face of the concrete basement wall, not extend underneath it. The wall sits on the foundation, the floor sits next to it.
**Source:** Deplazes p.417.

### Drainage pipe in gravel bed
**Note:** Drainage pipe embedded in coarse gravel is an intentional overlap (gravel wraps around the pipe). Don't flag this as an error in overlap audits. Mark as "intentional_overlap" in metadata.
**Source:** Deplazes p.417-418.
