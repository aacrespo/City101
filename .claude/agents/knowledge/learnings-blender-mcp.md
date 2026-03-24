# Blender MCP Learnings

Techniques discovered while using the Blender MCP router, code execution, geometry transfer, and error recovery. Updated by agents after each build.

---

## 1. **State does not persist between execute_code calls**
Each `blender_execute_code` call runs in a fresh Python context. Variables, imports, and helper functions from a previous call do not exist. All helpers (flat_mat, make_box, hex_rgb) must be redefined at the top of every code block. This is the single most important MCP constraint to internalize.

## 2. **Failed code blocks leave partial objects**
When an execute_code call fails mid-execution, objects created before the error line remain in the scene. The retry then creates duplicates with `.001` suffixes. Fix: always run a cleanup pass after any failure, checking for `.001`/`.002` suffixed objects and removing them.

## 3. **bpy.context.active_object can be None after primitive creation in loops**
Creating objects (especially cylinders) inside loops can leave `active_object` as None. Fix: pass rotation/scale as parameters to the creation function, or access the object immediately via `bpy.context.object` right after the `ops` call, rather than referencing `active_object` later.

## 4. **Collection management pattern**
Create object with `bpy.ops.mesh.primitive_*_add()`, then unlink from all current collections, then link to target collection. Order matters: if you link first then unlink, you might accidentally unlink from the target. Always unlink first.

## 5. **Appending collections from .blend files is reliable**
Use `bpy.ops.wm.append()` with `filepath`, `directory`, and `filename` parameters. Collections come through with all objects, materials, parenting, and shape keys intact. Check available collections first with `bpy.data.libraries.load()` in read mode. Append both collections AND actions in separate passes.

## 6. **Character parenting survives append**
When appending a character collection, all child objects (eyes, spark, backpack) remain properly parented to the body. No re-parenting needed after append.

## 7. **Actions also append correctly**
Load actions via `bpy.data.libraries.load()` and access them by name. Actions with `use_fake_user=True` persist and are available after append. 9 reusable actions (Walk, Idle, Spawn, Despawn, Blink, Working, etc.) loaded without issues across all 6 videos.

## 8. **Collection visibility toggling**
`layer_collection.children[name].exclude = True/False` controls viewport visibility. Combined with `collection.hide_render = True/False` for render-time control. Note: `collection.hide_viewport` / `collection.hide_render` CANNOT be keyframed -- use per-object hide keyframes instead.

## 9. **Always use absolute file paths**
MCP has no persistent working directory. All file paths in save, open, append, and render output must be absolute (e.g., `/Users/name/project/file.blend`).

## 10. **Print summary at end of every code block**
Print object count, collection membership, and any key results at the end of each execute_code call. This is the only way to verify what happened, since you cannot inspect state from a previous call.

## 11. **Break work into 3-5 separate execute_code calls per major element**
Don't try to build an entire room in one code block. If the block fails at line 200, you lose everything. Smaller blocks mean less re-work on failure. Each block should do one logical thing and save.

## 12. **Save after every major step**
`bpy.ops.wm.save_as_mainfile(filepath="/absolute/path/to/file.blend")` after building each room, after each animation pass, after each render batch. Blender crashes and MCP connection drops lose everything unsaved.

## 13. **Custom mesh via bmesh works through MCP**
For non-primitive shapes (triangular prisms, L-shapes, etc.), bmesh with manually specified vertices and faces works when boolean operations are not available. This is the way to create complex geometry without booleans.

## 14. **Boolean operations are unreliable via MCP**
Blender MCP doesn't support boolean operations reliably via code. For wall openings (doors, windows), delete the original wall and create 2-4 wall segments around the opening. More objects but zero risk of boolean artifacts.

## 15. **Wall openings: split into segments, not booleans**
Instead of a boolean cutout, create separate wall segments above/below/beside the opening. More objects in the scene but deterministic and artifact-free. This pattern was used for all doors and windows across the house set.

## 16. **Scene reset and append workflow**
Clear all objects/collections, purge orphans (`bpy.ops.outliner.orphans_purge()`), then append from source .blend files. This gives a clean starting point for each video without accumulated cruft from previous iterations.

## 17. **Always specify target in every MCP call**
When using the router, every call needs `target="main"` (or whichever instance). Forgetting the target routes to the default instance which may not be the one you're working in.

## 18. **MCP timeout does not kill Blender operations**
When MCP times out during a long operation (especially renders), Blender continues working in the background. Monitor via filesystem (check for output files) rather than assuming the operation failed. The MCP connection restores automatically once Blender finishes.
