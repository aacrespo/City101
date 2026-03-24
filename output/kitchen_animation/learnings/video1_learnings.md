# Video 1 — "Moving In" — Build Learnings

## Date: 2026-03-24
## Agent: Cairn Code (CLI)

---

## What worked

### Character appending
- Appending `Char_Cairn` collection from `characters.blend` worked flawlessly via `bpy.ops.wm.append()`.
- All 5 objects (Body, Eye_L, Eye_R, Spark, Backpack) came through with materials intact (Mat_Cairn_Body, Mat_Eye_Black, Mat_Cairn_Spark, Mat_Cairn_Backpack).
- Actions also appended correctly (9 total: Walk, Idle, Spawn, Despawn, Blink, Working, etc).
- **Key pattern**: Append both the collection AND the actions in separate passes.

### Parenting for animation
- Created a `Cairn_Root` empty as parent for all character objects. This made location/scale animation trivial — animate the root, everything follows.
- Important: after parenting, moved the body to local origin (0,0,0) and set root position to where body was.

### Batched rendering through MCP
- Single-frame `render(write_still=True)` works fine through MCP.
- `render(animation=True)` times out even for small ranges (10+ frames).
- **Working pattern**: Loop with `frame_set(f)` + `render(write_still=True)` in batches of 30-40 frames per MCP call.
- 480 frames rendered successfully in 12 batches of ~40 frames each.

### Object-level visibility keyframing
- Collection `hide_viewport` / `hide_render` cannot be keyframed.
- **Workaround**: Iterate all objects in a collection, keyframe `hide_render` and `hide_viewport` on each object individually.
- Used this for the room reveal at frames 435-436 (190 objects across 6 collections).

### Smooth interpolation
- After setting all keyframes, run a pass setting `interpolation='BEZIER'` and `handle_*_type='AUTO_CLAMPED'` on all keyframe points. This makes all motion smooth.

## What to improve

### Freestyle
- Disabled Freestyle for speed (was enabled initially but renders were timing out).
- The frames look clean without it but lack the signature black outlines.
- **For final quality**: Re-enable Freestyle (`scene.render.use_freestyle = True`) and render overnight via command line: `blender -b video_01_animated.blend -a`
- Draft at 16 samples without Freestyle renders in ~1-2 seconds per frame. With Freestyle expect 3-5x slower.

### Character scale
- Cairn (1.1 wide, 1.26 tall) is proportionally correct for the kitchen (12x8 units) but reads small in 960x540 draft resolution.
- At 1920x1080 final resolution, the character will be more visible.
- Could also scale Cairn to 1.3x for better readability without breaking proportions.

### Camera framing
- Isometric camera at (14, -14, 16) with ortho_scale=12 frames the kitchen well.
- Pullback to (18, -18, 22) with ortho_scale=24 shows the full house.
- The transition is smooth with Bezier interpolation.
- **Note**: Track-To constraint was removed in favor of fixed rotation — simpler and more predictable.

### Text labels
- Room labels and end title use FONT text objects rotated to match isometric camera angle.
- They pop in with scale animation (0 -> 1.1 -> 1.0) at frames 445-462.
- At draft resolution they may be hard to read — verify at final 1080p.

### Work particles
- 6 small gold cubes fly off during work animation (frames 350-430).
- Simple but effective at communicating "work being done".
- Could add more particles or use actual particle system for final version.

## MCP timeout patterns

| Operation | Result |
|-----------|--------|
| `get_scene_info` | Always works |
| `execute_code` (no render) | Always works |
| `render(write_still=True)` x1 | Works (1-3 seconds) |
| `render(write_still=True)` x30 | Works (~30 seconds) |
| `render(write_still=True)` x40 | Works (~40 seconds) |
| `render(animation=True)` 10 frames | Times out |
| `render(animation=True)` 40 frames | Times out |
| `render(animation=True)` 80 frames | Times out |

**Conclusion**: Never use `render(animation=True)` through MCP. Always use the frame-by-frame loop pattern.

## Animation structure

| Phase | Frames | Duration | Action |
|-------|--------|----------|--------|
| Empty kitchen hold | 1-72 | 0-3s | Camera holds, Cairn invisible |
| Door opens + spawn | 72-120 | 3-5s | Door rotates, Cairn pops in (scale bounce) |
| Walk to corkboard + backpack | 120-216 | 5-9s | Walk with squash/stretch, backpack opens, scroll rises/falls |
| Reading corkboard | 216-264 | 9-11s | Hold position, eyes shift left-right |
| Walk to counter + recipe book | 264-336 | 11-14s | Walk to counter, recipe book opens |
| Working animation | 336-432 | 14-18s | Squash/stretch work, gold particles fly |
| Camera pullback + reveal | 432-480 | 18-20s | Ortho scale 12->24, rooms unhide, labels pop in, end text |

## File locations

- **Animated .blend**: `output/kitchen_animation/renders/video_01/video_01_animated.blend`
- **PNG sequence**: `output/kitchen_animation/renders/video_01/frame_0001.png` through `frame_0480.png`
- **Character source**: `output/kitchen_animation/assets/characters.blend`

## Next steps for polish

1. Re-render at 1920x1080 with Freestyle enabled (command line overnight)
2. Composite PNG sequence to MP4 (ffmpeg: `ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video_01.mp4`)
3. Consider scaling Cairn up 30% for better readability
4. Add spark bobbing animation (sinusoidal up/down on Cairn_Spark)
5. Add idle breathing animation during hold phases
6. Verify end text readability at final resolution
