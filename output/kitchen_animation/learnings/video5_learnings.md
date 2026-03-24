# Video 5 — "Opening More Kitchens" — Learnings

## Build date: 2026-03-24

## What worked

### Scene assembly from existing assets
- Opening `exterior_rigs.blend` as the base scene worked cleanly — provided the street, buildings, cameras, and lighting pre-configured.
- Appending `Kitchen` collection from `house_set.blend` brought in all 54 objects with materials intact.
- Appending three character collections (`Char_Cairn`, `Char_Meridian`, `Char_Cadence`) from `characters.blend` worked without issues.
- All 9 reusable actions loaded via `bpy.data.libraries.load()`.

### Character root empties
- Creating `*_Root` empties as parents for all character objects makes animation simple — animate the root, everything follows.
- Spawn pop animation (scale 0 -> 1.15 -> 0.95 -> 1.0) reads well even at small character scale in wide shots.

### Building cross-section transparency
- EEVEE `blend_method = 'BLEND'` with alpha 0.15 on building shells creates a good cross-section effect.
- Technique: create an opaque duplicate that hides when the transparent original appears. This avoids material keyframing issues.
- The transparent shells let you see the mini-kitchens and characters inside.

### Camera progressive pull-back
- Isometric camera at rotation (52, 0, 32) with progressive ortho_scale increase creates a nice zoom-out effect.
- Key insight: when pulling back, also shift the camera target point. If the camera stays centered on origin but the buildings are at Y=14, the buildings stay at the edge of frame. Centering the target between house (Y=0) and buildings (Y=14) at Y~7 frames everything properly.
- Camera position calculation: `cam_pos_from_target(target_x, target_y, target_z, distance)` with offsets based on the rotation angles.

### Window glow via overlay planes
- Creating emission-material planes slightly in front of dark windows is simpler than material keyframing.
- `CONSTANT` interpolation on hide/show keyframes ensures instant on/off (no fade).
- `BEZIER` interpolation on location/scale for smooth motion.

### MCP timeout handling
- 30-frame batches are the safe limit for frame-by-frame rendering through MCP with Freestyle enabled at 960x540.
- When MCP times out, Blender continues rendering in background. Monitor via filesystem (`ls frame_*.png | wc -l`).
- Some batches of 30 still timed out (inconsistent — likely depends on scene complexity at those frames). Always check frame count after timeout.

## What to watch for

### Transparency + Freestyle
- Transparent (alpha blend) materials with Freestyle enabled can cause slower renders on some frames. The render time per frame varied from ~1s to ~3s.
- If Freestyle causes issues with transparent objects, consider disabling Freestyle on the transparent building shells' collection.

### Character visibility in wide shots
- Characters are very small in the full street view (ortho_scale=42). At 960x540 draft resolution, they're barely visible inside the transparent buildings.
- For final quality: render at 1920x1080 and consider scaling characters up 1.5x inside the buildings.

### Pneumatic tube capsules
- The capsule paths follow straight lines between buildings via the street. They read as "things moving between buildings" but are very small.
- For better visibility: increase capsule radius to 0.2 or add a glow trail (emit material with motion blur).

### Extra buildings in wide shot
- Buildings D, E, F appear only at frame 528+. They have no interior detail — just shells with glow windows. This is fine for the progressive reveal but at full wide they look sparse.
- Consider adding 2-3 more buildings for a fuller street.

## Timing breakdown (24fps)

| Phase | Frames | Seconds | Content |
|-------|--------|---------|---------|
| Cairn working | 1-72 | 0-3s | Kitchen close-up, squash/stretch work, chimney smoke |
| Camera pull-back | 72-192 | 3-8s | Pull from close to medium, street and buildings emerge |
| Building A lights up | 192-264 | 8-11s | Windows glow, shell goes transparent, mini-kitchen appears, tunnel glow |
| Meridian spawns | 264-336 | 11-14s | Pop animation in Building A kitchen, starts working |
| Building C lights up + Cadence | 336-408 | 14-17s | Building C glow + transparency, Cadence spawn pop |
| All three cooking + capsules | 408-528 | 17-22s | Work particles, pneumatic tube capsules shooting between buildings |
| Wider pull-back + more buildings | 528-648 | 22-27s | Buildings B, D, E, F appear and light up, camera widens |
| Dishes converge + text | 648-720 | 27-30s | Three dishes fly to main house, end text pops in |

## Technical notes
- Engine: `BLENDER_EEVEE` (Blender 3.3.9)
- Total scene objects: 228 (exterior 40 + kitchen 54 + characters 15 + mini-kitchens 12 + tunnels 10 + capsules 6 + particles 32 + extras 15 + smoke 16 + dishes 3 + text 1 + extras 24)
- Animated objects: 120
- Render: 960x540, PNG sequence, EEVEE + Freestyle 2px
- Render time: ~30-50 minutes total (batches of 25-30 frames, with MCP timeouts)
- MCP batch size sweet spot: 25-30 frames for this scene complexity

## File locations
- **Animated .blend**: `output/kitchen_animation/renders/video_05/video_05_animated.blend`
- **PNG sequence**: `output/kitchen_animation/renders/video_05/frame_0001.png` through `frame_0720.png`
- **Character source**: `output/kitchen_animation/assets/characters.blend`
- **House source**: `output/kitchen_animation/assets/house_set.blend`
- **Exterior source**: `output/kitchen_animation/assets/exterior_rigs.blend`

## Next steps for polish
1. Re-render at 1920x1080 with Freestyle (command line overnight)
2. Composite to MP4: `ffmpeg -framerate 24 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p video_05.mp4`
3. Scale characters up 1.5x inside buildings for better readability
4. Add more extra buildings (6-9 total) for fuller street
5. Consider adding building labels ("Kitchen 2", "Kitchen 3") for clarity
6. Add capsule glow trails for better visibility of pneumatic tube system
