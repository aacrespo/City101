# Video 2 Learnings — "Real Kitchen vs TV Kitchen"

## Session: 2026-03-24

### Build Process

1. **Appending collections from .blend files works reliably.** Use `bpy.ops.wm.append()` with `filepath`, `directory`, and `filename` parameters. Check available collections first with `bpy.data.libraries.load()` in read mode.

2. **Character parenting survives append.** When appending a character collection (Char_Cairn, Char_Lumen), all child objects (eyes, spark, backpack) remain properly parented to the body. No re-parenting needed after append.

3. **TV-within-scene composition works.** Placing a miniature kitchen inside/in-front-of a TV frame reads well in the isometric view. Key: make TV screen material semi-transparent (mix of transparent + emission shader, blend_method='BLEND') so the miniature objects behind it are visible.

4. **Constraint enum values in Blender 3.3.9 use full names.** The track_axis enum is `'TRACK_NEGATIVE_Z'` not `'TRACK_NEG_Z'`. Always use the full enum string. Error: `"enum 'TRACK_NEG_Z' not found in ('TRACK_X', 'TRACK_Y', 'TRACK_Z', 'TRACK_NEGATIVE_X', 'TRACK_NEGATIVE_Y', 'TRACK_NEGATIVE_Z')"`.

5. **Animation render via MCP will timeout the connection but still complete.** Calling `bpy.ops.render.render(animation=True)` for 600 frames blocks the MCP connection (returns "No data received" error) but Blender continues rendering in the background. Check the output directory for rendered frames rather than waiting for the MCP response.

6. **Render timeout recovery: connection restores automatically.** After a long render completes (checked via filesystem), the MCP connection to the Blender instance resumes working. No need to restart anything.

7. **hide_viewport + hide_render keyframes control object visibility per-frame.** Set both to True/False and keyframe_insert both data paths. The keyframe interpolation is "constant" by default for boolean properties, so objects pop in/out instantly at the keyed frame.

8. **Text objects need rotation to face isometric camera.** For a camera at rotation (60, 0, 45) degrees, text objects need rotation_euler = (90, 0, 45) degrees to face the camera plane. Without this, text appears edge-on and unreadable.

9. **Character scaling for TV miniature: 0.3x works well.** Scaling Lumen to 30% gives a clear "small, behind glass" reading against the full-size Cairn. The mini kitchen furniture should be similarly proportioned.

10. **Walk animation via location keyframes + scale oscillation.** Simple sine-wave squish (scale X +5%, Z -5%) alternating every few frames during movement creates a convincing walk bounce without rigging. Applied per walk segment between location keyframes.

11. **Chopping animation: small Z-axis oscillation.** Moving the character body up/down by 0.06-0.08 units in a sine pattern at ~3 frame intervals reads as chopping/working activity.

12. **File materialize effect: scale from near-zero to overshoot to settle.** Scale (0.01, 0.01, 0.01) -> (overshoot) -> (final size) over ~12 frames gives a nice "pop into existence" sparkle effect.

13. **Camera zoom via ortho_scale animation.** Animating `camera.data.ortho_scale` from 16 to 8 over 72 frames creates a smooth zoom-in effect. Combined with camera target movement for reframing.

14. **Warm glow effect: animate sun energy.** Increasing sun energy from 3.0 to 4.5 during the final zoom creates a subtle "warmth" that reinforces "Cairn is HERE" emotionally.

### Scene Statistics
- 90 objects total (54 kitchen + 5 Cairn + 5 Lumen + 9 mini kitchen + 4 TV + 3 text + lights/camera/empties + kitchen additions)
- 40 materials
- 600 frames at 24fps = 25 seconds
- 960x540 draft resolution
- Freestyle 2px outlines enabled
- Render completed all 600 frames as PNG sequence

### What Worked
- The split composition (real kitchen + TV miniature) reads clearly
- Character color distinction (amber Cairn vs gold Lumen) is visible even at small scale
- Text overlays on the floor plane are readable
- The "bonk" moment (Lumen reaching edge of TV) creates clear visual tension

### What Could Be Improved
- Mini kitchen objects could use more depth for better 3D reading
- The TV screen transparency could be adjusted for better contrast
- Knife "pickup" is a teleport rather than smooth transition (would need dynamic parenting)
- Consider adding particle effects for chopping and spawn moments in a polish pass
