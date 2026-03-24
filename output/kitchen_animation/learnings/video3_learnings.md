# Video 3 Learnings — "Calling for Backup" (Subagents)

## Session: 2026-03-24
## Agent: Cairn Code (CLI) — third Blender instance

---

## Build Process

1. **Scene reset and append workflow is reliable.** Clearing all objects/collections, purging orphans, then appending from house_set.blend and characters.blend works cleanly. Collections come through with all objects, materials, and parenting intact.

2. **Character root empty pattern confirmed.** Creating a Cairn_Root and Subagent_Root empty as top-level parents makes animation straightforward — animate the root, everything follows. The Char_Cairn collection has Body -> (Eyes, Spark, Backpack) hierarchy that survives append.

3. **Bezier curve as tether line works well.** Using a CURVE object with `bevel_depth=0.03` creates a visible thin line. Keyframing individual bezier_point.co values lets the tether stretch and follow the subagent's path. Emission material (orange glow) makes it stand out.

4. **Curve point keyframing requires careful approach.** Bezier points are keyframed via `spline.bezier_points[i].keyframe_insert(data_path="co", frame=f)`. The animation data lives on the curve data, not the object. Handle types should be AUTO for smooth interpolation.

5. **Boolean hide properties MUST use CONSTANT interpolation.** When applying Bezier interpolation to all keyframes, explicitly skip `hide_render` and `hide_viewport` properties — these must stay CONSTANT or objects will blend between visible/invisible states instead of snapping.

6. **Info particles as simple UV spheres work fine.** 8 small spheres (radius=0.06) with gold emission material create readable "information flowing" effect. Staggered appearance (12 frames apart) and staggered absorption (3 frames apart) gives organic feel.

7. **Text overlay positioning in isometric view is challenging.** Text rotated to match camera angle (60, 0, 45 degrees) is readable but positioning for full visibility requires trial and error. The text needs to be within the camera frustum at the specific frame's ortho_scale. Shorter text works better — split the original two-line message to just "Send a smaller you."

8. **Camera ortho_scale animation creates smooth zoom.** Widening ortho_scale from 10 to 18 as the camera pans up to show both floors, then back to 12 for the ending, creates a natural "breathing" of the frame.

9. **Frame-by-frame render in batches of 40 is the reliable pattern.** 12 batches of 40 frames each, all completed without MCP timeout. Each batch takes ~40-60 seconds.

10. **Subagent spawn/despawn animation reads clearly.** Scale bounce (0.01 -> 1.2 -> 0.9 -> 1.0) for spawn and reverse squish (1.0 -> 1.3x0.4h -> 0.01) for despawn are visually distinct events.

## Scene Statistics
- 139 objects total (54 kitchen + 59 library + 5 Cairn + 5 subagent + 8 particles + 1 tether + 1 text + 2 lights + camera + empties)
- 480 frames at 24fps = 20 seconds
- 960x540 draft resolution
- EEVEE with Freestyle 2px outlines
- 2174 keyframe points across all animated objects
- All 480 frames rendered as PNG sequence

## Animation Structure
| Phase | Frames | Duration | Action |
|-------|--------|----------|--------|
| Cairn cooking | 1-36 | 0-1.5s | Chopping animation at counter |
| Cairn thinking | 36-48 | 1.5-2s | Pauses, eyes up, spark brightens |
| Spark pulse + spawn | 48-96 | 2-4s | Spark pulses, subagent pops in with bounce |
| Subagent to library | 96-192 | 4-8s | Bouncy travel up stairs to bookshelves |
| Research in library | 192-336 | 8-14s | Working animation, side-to-side, particles gather |
| Return to kitchen | 336-384 | 14-16s | Fast zip back, particles travel along tether |
| Absorb + despawn | 384-432 | 16-18s | Particles shrink into Cairn, subagent poofs |
| Resume cooking | 432-480 | 18-20s | Confident working, text overlay appears |

## Camera Animation
- Frames 1-72: Kitchen close-up (ortho_scale 10)
- Frames 72-168: Pan up and widen to show both floors (ortho_scale 18)
- Frames 168-300: Focus on library (ortho_scale 14)
- Frames 300-400: Pan back down, return to kitchen (ortho_scale 12)
- Frames 400-480: Hold on kitchen

## File Locations
- **Animated .blend**: `output/kitchen_animation/renders/video_03/video_03_animated.blend`
- **PNG sequence**: `output/kitchen_animation/renders/video_03/frame_0001.png` through `frame_0480.png`
- **House set source**: `output/kitchen_animation/assets/house_set.blend`
- **Character source**: `output/kitchen_animation/assets/characters.blend`

## What Worked
- The two-floor composition (kitchen + library) reads clearly in isometric
- Subagent spawn/despawn pop animations are visually clear events
- Tether curve stretching between floors communicates connection
- Info particle gather-and-return creates readable "knowledge transfer" visual
- Camera pan following the subagent up and back creates narrative flow

## What Could Be Improved
- Subagent is quite small and hard to see at draft resolution — consider scaling up 1.5x
- Tether could use a dashed material (texture-based) rather than solid for the dotted-line spec
- Info particles could orbit more dynamically around the subagent during research phase
- The walkie-talkie moment (spec says Cairn pulls out a walkie-talkie) was simplified to just a spark pulse
- Text "Send a smaller you." could be larger or positioned as a 2D overlay in post
- Library research phase (144 frames) could use more visual variety — book objects animating, desk lamp glow
- Consider adding a subtle glow/bloom on the tether during info transfer phase

## Next Steps for Polish
1. Re-render at 1920x1080 with Freestyle (command line: `blender -b video_03_animated.blend -a`)
2. Composite to MP4: `ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video_03.mp4`
3. Scale subagent up for better visibility
4. Add dashed texture to tether material
5. Consider 2D text overlay in post-production (ffmpeg drawtext or compositor)
