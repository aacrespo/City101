# foundation Modeling Learnings

Techniques discovered while modeling. Updated by agents after each build round.

---

## 2026-03-21 — Foundation Agent (team build)

1. **Sublayer creation via `rhino_create_layer` tool fails for `Parent::Child` syntax** — the MCP tool throws a null reference. Workaround: use `rs.AddLayer("Parent::Child", color)` inside `rhino_execute_python_code`. This is reliable and gives full control over color.

2. **Box helper function is essential for foundation work.** The 8-point `rs.AddBox(pts)` API is error-prone for axis-aligned boxes. A simple `box(x, y, z, L, W, H)` wrapper that computes the 8 corners from origin + dimensions eliminates mistakes. Define it once per script call since state does not persist.

3. **Door gap in plinth: use multiple boxes, not boolean subtraction.** The playbook warns that boolean cutting is unreliable. Splitting the south plinth into `Plinth_South_Left` and `Plinth_South_Right` with a gap at x=205-295 worked cleanly and is easier for downstream agents to reason about than a single object with a cut.

4. **Splash aprons protect rammed earth bases from rain erosion.** A thin concrete apron (60cm wide, at grade level) around the plinth perimeter prevents rain splash-back from eroding the rammed earth wall base. Modeled as a ring surface using boolean difference of outer and inner rectangles — boolean worked here because it was a simple planar surface, not a solid. Material: concrete C25/30.
