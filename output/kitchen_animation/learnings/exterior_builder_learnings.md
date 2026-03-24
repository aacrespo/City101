# Exterior Builder Learnings
Agent: Exterior Builder (Blender instance "third")
Date: 2026-03-24

## Discoveries

1. **Ortho scale = framing width in Blender units.** ortho_scale=10 means the camera shows 10 units of width. With a 12-unit-wide house, ortho_scale=10 crops the sides slightly. For the house-focused shots this is fine (some framing), but for the full street view (Video 5), ortho_scale=35 was needed to fit house + street + three buildings.

2. **Freestyle works out of the box in EEVEE on Blender 3.3.9.** No special configuration beyond enabling `render.use_freestyle = True` and `view_layer.use_freestyle = True`. The 2px black lines rendered correctly on all geometry edges. This is a relief -- Freestyle can be finicky in newer Blender versions.

3. **MCP state does not persist between execute_code calls.** Helper functions (flat_mat, make_box) must be redefined in every code block. This is expected per the playbook but worth reiterating -- plan code blocks to be self-contained.

4. **Collection management pattern:** Create object with `bpy.ops.mesh.primitive_*_add()`, then unlink from all current collections, then link to target collection. The order matters -- if you link first then unlink, you might accidentally unlink from the target.

5. **Camera rig pattern: empty parent + Track To constraint.** This is the cleanest way to animate cameras. Move/animate the empty, camera follows. Track To with TRACK_NEGATIVE_Z and UP_Y works for standard isometric. Parent relationship means the empty's location offsets the camera position.

6. **Sun lamp warm color approximation for ~4500K:** RGB (1.0, 0.91, 0.78) gives a convincing warm white. Combined with the #F5F0EB world background, the scene reads as warm without being orange.

7. **Fill light with shadow disabled** prevents double-shadow artifacts while adding ambient illumination. Energy 0.8 (vs Sun at 3.0) gives about 25% fill ratio, which keeps the flat look while avoiding completely black shadows.

8. **Window placement on buildings:** Windows are thin boxes (depth 0.1) placed just in front of the building face. They're positioned at Y=10.95 for Building A (face at Y=11) -- slightly proud of the face so Freestyle draws their outlines distinctly from the wall.

9. **Viewport screenshot tool returned "No filepath provided" error.** The `blender_get_viewport_screenshot` MCP tool didn't work. Workaround: use `bpy.ops.render.render(write_still=True)` to render from the active camera. This actually gives a better result since it includes Freestyle lines, which viewport screenshots might not show.

10. **Ground plane layering:** Multiple overlapping ground planes at slightly different Z heights (ground at -0.05, street at -0.04, garden at -0.04) prevents z-fighting. The 0.01 unit separation is invisible but prevents flickering artifacts.

11. **Pneumatic tube creation with mathutils:** Cylinders default to Z-up orientation. To connect two arbitrary points, calculate the rotation quaternion from Z-up to the direction vector using `Vector.rotation_difference()`. Clean and general-purpose pattern.

12. **Three-camera strategy:** Rather than animating ortho_scale (which can look odd in orthographic), having three cameras at different scales (5, 10, 35) and cutting between them is cleaner. Animate the target empties for smooth pans within each scale level.
