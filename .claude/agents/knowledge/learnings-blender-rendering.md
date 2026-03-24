# Blender Rendering Learnings

Techniques discovered while configuring EEVEE, Freestyle, PNG sequences, and render settings. Updated by agents after each build.

---

## 1. **Engine string is 'BLENDER_EEVEE' in Blender 3.3.9**
Not `'BLENDER_EEVEE_NEXT'` (that's Blender 4.0+). Using the wrong string causes silent render failure or crashes. Always check the Blender version before setting the engine.

## 2. **Freestyle 2px lines work out of the box in EEVEE 3.3.9**
Enable `render.use_freestyle = True` and `view_layer.use_freestyle = True`, then set linestyle thickness to 2.0 on the default lineset. No special configuration needed. Clean outlines on all geometry edges.

## 3. **Freestyle adds significant render time**
With Freestyle enabled: ~1 second per frame at 960x540. Without: ~0.3 seconds per frame. Roughly 3x overhead. For draft iteration, consider disabling Freestyle and re-enabling for final renders.

## 4. **Freestyle + transparent materials can cause variable render times**
Alpha blend materials with Freestyle enabled cause render time per frame to vary from ~1s to ~3s. If this causes MCP timeouts, consider disabling Freestyle on transparent objects' collection specifically.

## 5. **Preview renders at half resolution (960x540) are fast and sufficient for checking**
Takes only 1-3 seconds per frame through MCP. Use after every major milestone to verify composition, colors, and framing before committing to full renders.

## 6. **Never use render(animation=True) through MCP**
`bpy.ops.render.render(animation=True)` blocks the MCP connection and times out even for 10+ frames. The connection returns "No data received" error. However, Blender continues rendering in the background after MCP timeout.

## 7. **Frame-by-frame render in batches is the reliable MCP pattern**
Loop with `scene.frame_set(f)` + `render(write_still=True)` in batches of 25-40 frames per MCP call. Sweet spot depends on scene complexity: simple scenes handle 40 frames, complex scenes (transparency + Freestyle) may need 25-30. This pattern successfully rendered 480-720 frame sequences across all 6 videos.

## 8. **MCP timeout recovery: connection restores automatically**
After a long render completes (check via filesystem: `ls frame_*.png | wc -l`), the MCP connection to Blender resumes working. No restart needed. If a batch times out, check which frames rendered and continue from the next unrendered frame.

## 9. **Render timeout table (960x540, EEVEE + Freestyle)**
| Operation | Result |
|-----------|--------|
| `render(write_still=True)` x1 | Works (1-3 seconds) |
| `render(write_still=True)` x30 | Works (~30 seconds) |
| `render(write_still=True)` x40 | Works (~40 seconds) |
| `render(animation=True)` any count | Times out MCP |

## 10. **Ortho camera scale sizing**
`ortho_scale` = framing width in Blender units. Kitchen (12x8 units) needs ortho_scale ~10-12. Full house needs ~24-35. Full street view needs ~42. Characters at ortho_scale 42 are barely visible at 960x540 -- consider scaling characters up 1.5x for wide shots or rendering at 1920x1080.

## 11. **Isometric camera angles**
Classic 30-degree isometric: rotation_euler (60, 0, 45), camera at ~(25, -30, 22). Alternative angle used across most videos: (52, 0, 32) for a slightly more top-down 3/4 view. Both work; the 52/32 variant shows more interior detail.

## 12. **Final render via command line, not MCP**
For production quality renders (1920x1080 with Freestyle), use command line: `blender -b scene.blend -a`. This avoids all MCP timeout issues and uses Blender's native render loop. MCP is for draft iteration; command line is for final output.

## 13. **PNG to MP4 compositing**
`ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video.mp4` for final delivery. PNG sequences preserve the ability to re-render individual frames without redoing the whole video.

## 14. **Viewport screenshot MCP tool returns "No filepath provided" error**
The `blender_get_viewport_screenshot` MCP tool doesn't work reliably. Workaround: use `bpy.ops.render.render(write_still=True)` at reduced resolution (50%). This actually gives better results since it includes Freestyle lines, which viewport screenshots might not show.

## 15. **339+ objects is manageable**
No performance issues creating or manipulating 339 objects through MCP. Blender saves and renders without lag. Video 5 reached 228 objects with 120 animated; Video 6 had 358 objects. All rendered successfully.
