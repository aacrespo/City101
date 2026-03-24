# House Builder Learnings — Kitchen Analogy Animations

## Session: 2026-03-24

### Build Process

1. **Failed code blocks leave partial objects.** When a Blender MCP execute_code call fails mid-execution, objects created before the error line remain in the scene. The retry then creates duplicates with `.001` suffixes. Fix: always run a cleanup pass after any failure, checking for `.001`/`.002` suffixed objects and removing them.

2. **Context object references don't survive across execute_code calls.** Each `blender_execute_code` call runs in a fresh Python context. You cannot reference variables from a previous call. All helper functions (flat_mat, make_box, make_cyl) must be redefined at the top of every code block. This is a Blender MCP fundamental limitation.

3. **bpy.context.active_object can be None after cylinder creation in some cases.** The coat hook rotation code failed because `bpy.context.active_object` returned None after creating a cylinder inside a loop. Fix: pass rotation as a parameter to the creation function rather than setting it on the object afterward via a separate reference.

4. **Material creation pattern that works reliably:** `mat.use_nodes = False` with `mat.diffuse_color = (r, g, b, 1.0)` gives perfect flat shading every time. No specular, no PBR, exactly what the doctrine requires. Create all materials upfront in one block so they're available by name everywhere.

5. **Wall openings (doors, windows, hatches) require splitting the wall into segments.** Blender MCP doesn't support boolean operations reliably via code. Instead, delete the original wall and create 2-4 wall segments around the opening. More objects but zero risk of boolean artifacts.

6. **Freestyle 2px lines work out of the box in Blender 3.3.9 EEVEE.** Just set `render.use_freestyle = True` and `view_layer.use_freestyle = True`, then set linestyle thickness to 2.0 on the default lineset. The render preview confirmed clean outlines on all geometry.

7. **Collection organization matters enormously.** Having 10 named collections (one per room) makes the manifest readable and enables per-video toggling. The naming convention `Room_Element_Detail` was easy to maintain with the helper functions.

8. **Ortho camera scale needs to be large for multi-story buildings.** Started at ortho_scale=25 which was too tight. Final value of 35 frames the full building including basement, attic, and neighboring buildings.

9. **Isometric angle: rotation_euler (60, 0, 45) for classic 30-degree iso.** X=60 degrees gives the 30-degree tilt (90-30=60), Z=45 gives the 45-degree azimuth. Camera positioned at (25, -30, 22) looks down at the cross-section.

10. **Render engine string is 'BLENDER_EEVEE' in Blender 3.3.9.** Not 'BLENDER_EEVEE_NEXT' (that's 4.0+). The playbook confirms this. If you use the wrong string, rendering fails silently or crashes.

11. **Custom mesh via bmesh works through MCP.** The attic roof prism was built using bmesh with manually specified vertices and faces. This is the way to create non-primitive shapes (triangular prisms, L-shapes, etc.) when boolean operations aren't available.

12. **339 objects is manageable.** No performance issues creating or manipulating this many objects through MCP. The Blender file saves and renders without lag. For reference: Kitchen alone is 54 objects, Basement is 66 (most detailed room due to shelf rack repetition).

13. **Preview renders at half resolution (960x540) are fast and sufficient for checking.** Takes only a few seconds through MCP. Use this after every major room to verify the visual before proceeding.

14. **Blue-tinted point light for the basement freezer effect.** A POINT light with color (0.7, 0.85, 1.0) and energy=50 placed in the basement gives a convincing cold/frost atmosphere without changing any materials. Combined with the frost_blue floor material.

15. **Pneumatic tubes connecting buildings are just rotated cylinders.** Simple approach: place cylinders at midpoints between buildings with appropriate rotations. Not physically accurate curves but reads clearly in the isometric view as connecting tubes.
