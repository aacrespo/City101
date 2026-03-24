# Video 4 — "The Brigade de Cuisine" — Learnings

## Build date: 2026-03-24

## What worked

### Scene assembly
- Appending collections from `house_set.blend` works cleanly. Kitchen (54 objects) and Pantry (39 objects) loaded without issues.
- Character collections from Phase 1 (79 objects, 14 collections) were already in the Blender instance. All teammates (Analyst, Modeler, Visualizer, Knowledge) plus Cairn were present with proper parenting (Body as root, Eyes/Spark/Backpack/Apron as children).

### Animation approach
- Keyframing `hide_viewport` and `hide_render` as booleans works for show/hide timing (ticket pieces appear/disappear, dishes appear/disappear).
- Staggered spawns (6-frame offset between teammates) make the sequence feel more dynamic than simultaneous spawns.
- BEZIER interpolation with AUTO_CLAMPED handles on all keyframes produces smooth motion without manual curve editing.
- The scale-based spawn pop (0 -> 1.1 -> 1.0 -> 0.97 -> 1.0) reads well as a bounce even at small character size.

### Camera
- Orthographic with scale 12.0 frames the kitchen + pantry well from isometric angle.
- Camera rotation (52deg, 0, 32deg) gives a good 3/4 view showing both the kitchen interior and pantry.
- Slight zoom (12.0 -> 11.0 ortho scale) during the inspection phase (frames 432-528) adds focus without being jarring.

### Freestyle
- Freestyle 2px lines render correctly in Blender 3.3.9 EEVEE. No errors encountered.
- Adds significant render time (~1 second per frame at 960x540 vs ~0.3s without).

## What to watch for

### MCP timeout on renders
- `bpy.ops.render.render(animation=True)` blocks the MCP connection. For 720 frames at ~1s each, the call times out (MCP default timeout appears to be ~30-60s).
- **Workaround**: Blender continues rendering after MCP timeout. The render completes in background. Monitor via filesystem (`ls frame_* | wc -l`).
- **Better approach for future**: Render in small batches (50-100 frames) per MCP call, or use a Python script that manages the render loop with periodic saves.

### Character visibility at wide shot
- At ortho_scale 12-14, the teammate blobs (0.6 units tall) are small but visible. Cairn (1.1 units) reads clearly.
- For presentation, consider a tighter crop or larger character scale if readability is a concern.

### Prop positioning
- Ticket pieces fly in arcs (position keyframes with mid-point at Y=2.5) -- BEZIER handles create smooth arcs automatically.
- Dishes are small cylinders (radius 0.2) -- visible but could be larger for impact.

## Timing breakdown (24fps)
| Phase | Frames | Seconds | Content |
|-------|--------|---------|---------|
| Cairn idle | 1-48 | 0-2s | Breathing, blink at f30 |
| Ticket drop | 48-96 | 2-4s | Paper falls, eyes track |
| Ticket tear + fly | 96-144 | 4-6s | 4 colored pieces arc to stations |
| Teammate spawn | 144-192 | 6-8s | Staggered pop-in (6f offset each) |
| All working | 192-360 | 8-15s | Squash/stretch, pantry walk |
| Knowledge shares | 360-432 | 15-18s | Book floats between K and M |
| Dish inspection | 432-528 | 18-22s | Slides to pass, red X bounce-back |
| Revision + combine | 528-624 | 22-26s | Green check, grand plate merge |
| Grand plate exit | 624-720 | 26-30s | Through hatch, text overlay |

## Technical notes
- Engine: `BLENDER_EEVEE` (not `BLENDER_EEVEE_NEXT` -- that's Blender 4.0+)
- Total scene objects: 186 (kitchen 54 + pantry 39 + characters ~65 + props ~15 + lights/camera)
- 23 animated objects total
- Render: 960x540, PNG sequence, ~1s/frame with Freestyle
