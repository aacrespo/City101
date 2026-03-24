# Video 6 — "The Pantry Tour" — Learnings

## Build date: 2026-03-24
## Agent: Cairn Code (CLI)

---

## What worked

### Scene setup from house_set.blend
- Opening the saved `house_set.blend` via `bpy.ops.wm.open_mainfile()` provides a clean starting point with all rooms pre-built.
- Collection visibility toggling via `layer_collection.children[name].exclude = True/False` works cleanly. Combined with `collection.hide_render = True/False` for render-time control.
- 3 rooms visible (Kitchen 54 objects, Pantry 39 objects, Library_Study 59 objects) plus Char_Cairn (5 objects + root empty).

### Character appending (confirmed pattern)
- `bpy.ops.wm.append()` for Char_Cairn collection + 9 Actions from `characters.blend` — same reliable pattern as Videos 1-4.
- Created `Cairn_Root` empty as animation parent. All 5 Cairn objects parented to root. Animate root location/scale = all children follow.
- Scaled Cairn to 1.2x for readability at draft resolution (lesson from Video 1).

### Camera keyframing
- Camera location keyframes must be inserted with `scene.frame_set(frame)` called before each `keyframe_insert()`. Without setting the frame first, only one keyframe registers (the last one). This is different from object location keyframes which work without frame_set.
- 20 camera position/ortho_scale keyframes covering kitchen (ortho 10), pantry zoom (ortho 8-9), library (ortho 9-10), and transitions.
- Fixed isometric rotation (52 deg, 0, 32 deg) throughout — no rotation animation needed.

### Multi-room camera panning
- The camera successfully tracks Cairn through 3 different rooms at 2 different vertical levels:
  - Kitchen: cam at z=12, ortho 10
  - Pantry: cam at z=11-12, ortho 8-9 (tighter for detail)
  - Library: cam at z=19, ortho 9-10 (up one floor)
- Vertical transitions (going upstairs/downstairs) achieved by animating camera Z from 12 to 19 over ~24 frames.

### Prop interaction animation
- Pop-in scale (0.01 -> 1.15 -> 1.0) over 12 frames reads well as "item materializes/is picked up".
- Combined with hide_render/hide_viewport keyframes set to CONSTANT interpolation so objects snap in/out rather than fading.
- Props move toward Cairn's position after "pickup" using location keyframes.

### Batched rendering
- 18 batches of 40 frames each = 720 frames total.
- Each batch takes ~40 seconds through MCP (about 1s per frame with Freestyle).
- No timeouts or failures. The frame-by-frame loop with batches of 40 remains the reliable pattern.

## What to improve

### Text positioning in isometric view
- Text objects rotated to (90, 0, 45) degrees face the isometric camera, but sizing/positioning requires trial and error.
- At 960x540, font size 0.35 for main text and 0.22 for subtitle is readable but tight.
- At 1920x1080 final resolution, text will be clearer. Consider font size 0.5+ for final.
- Text position (1, -3.5, 0.1) on the kitchen floor plane works for the final "back in kitchen" camera view.

### Zone labels (L1-L4) timing
- Labels appear/disappear as Cairn visits each section. CONSTANT interpolation on hide properties makes them pop in/out cleanly.
- Could add a fade-out via material alpha animation for smoother transitions in a polish pass.

### Character readability in library
- Library scene has many objects (59 + props). Cairn at 1.2x scale is small against floor-to-ceiling bookshelves.
- For final render, consider tighter camera or larger Cairn (1.4x) in library sections.

### Stair transition
- Currently Cairn teleports vertically (Z 0.6 to 3.6 over 24 frames). No visible staircase geometry.
- Could add a simple stair box primitive between floors for visual continuity.
- The camera also transitions vertically during this time, so the "going upstairs" reads through context clues.

## Animation timing (24fps)

| Phase | Frames | Seconds | Content |
|-------|--------|---------|---------|
| Kitchen cooking | 1-48 | 0-2s | Cairn at counter, working motion, pauses |
| Walk to pantry | 48-96 | 2-4s | Walk with bounce, door opens at f72-84 |
| L1: Bins (SQLite) | 96-192 | 4-8s | Walk to bins, scoop appears f168, label f120-200 |
| L2: Cabinet (Markdown) | 192-312 | 8-13s | Walk to cabinet, card appears f288, label f240-320 |
| L3: Rack (Scripts) | 312-432 | 13-18s | Walk to pegboard, tool appears f408, label f360-440 |
| Walk back to kitchen | 432-480 | 18-20s | Return through door, door closes f480-492 |
| Needs more - looks up | 480-528 | 20-22s | Scale stretch up, walks to stairs |
| Library: bookshelf | 528-612 | 22-25.5s | Upstairs, pulls Deplazes at f594, label L4 f556-670 |
| Library: desk + lightbox | 612-660 | 25.5-27.5s | Reading at desk, lightbox glows f636 |
| Return to kitchen | 660-696 | 27.5-29s | Down stairs, back to counter |
| Final cooking + text | 696-720 | 29-30s | Confident working, text overlay at f690-700 |

## Technical notes

- Engine: `BLENDER_EEVEE` (Blender 3.3.9)
- Freestyle: 2px black outlines, enabled, no errors
- 14 animated objects (Cairn_Root, Camera, Door, 5 props, 6 text/labels)
- 770 keyframe points total, all smoothed to BEZIER/AUTO_CLAMPED (except hide properties = CONSTANT)
- 358 scene objects, 34 materials
- Render: ~1s per frame at 960x540 with Freestyle

## File locations

- **Animated .blend**: `output/kitchen_animation/renders/video_06/video_06_animated.blend`
- **PNG sequence**: `output/kitchen_animation/renders/video_06/frame_0001.png` through `frame_0720.png`
- **Character source**: `output/kitchen_animation/assets/characters.blend`
- **House set source**: `output/kitchen_animation/assets/house_set.blend`

## Next steps for polish

1. Re-render at 1920x1080 with Freestyle (command line: `blender -b video_06_animated.blend -a`)
2. Composite to MP4: `ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video_06.mp4`
3. Add staircase geometry between kitchen and library floors
4. Add blink animation on Cairn during hold phases
5. Add spark bobbing (sinusoidal on Cairn_Spark)
6. Consider adding "scoop contents" particle effect when opening bin
7. Lightbox could pulse/animate rather than just appearing
