# Blender Animation Learnings

Techniques discovered while creating keyframe animations, shape keys, actions, and character movement. Updated by agents after each build.

---

## 1. **Shape keys work on subdivided meshes**
Shape keys (squash/stretch, blink, look, surprise) operate on the base mesh. Subdivision surface modifier applies on top. No need to apply the modifier before adding shape keys.

## 2. **Eye blink shape key uses Z-axis squish, not Y**
UV sphere eyes are oriented with Z up in local space. Scaling Z to 0.1 gives a convincing blink. Getting the axis wrong produces a horizontal squeeze instead of a vertical close.

## 3. **Shape key actions live on separate animation data from object actions**
Object actions go on `object.animation_data.action`. Shape key actions go on `object.data.shape_keys.animation_data.action`. These are independent -- you must assign both when animating a character that uses both location/scale keyframes and shape keys.

## 4. **Cyclic modifiers on fcurves for seamless loops**
Apply via `fcurve.modifiers.new('CYCLES')` after creating keyframes. Makes idle breathing, bobbing, and blinking animations loop seamlessly without manual keyframe duplication.

## 5. **Actions with use_fake_user=True persist in the .blend file**
Essential for reusable action libraries. Without fake_user, unassigned actions get purged on save/reload.

## 6. **Stale actions accumulate -- clean them up**
Keyframe operations auto-create actions (e.g., `KeyAction`, `Key.001Action`). Clean these explicitly with `bpy.data.actions.remove()` after setting `use_fake_user = False`. Otherwise the action list becomes cluttered.

## 7. **Character root empty pattern for animation**
Create a `CharName_Root` empty as parent for all character objects (body, eyes, spark, backpack). Animate the root for location/scale -- everything follows. After parenting, move body to local origin (0,0,0) and set root position to where body was.

## 8. **Spawn pop animation: scale 0 -> overshoot -> settle**
Scale (0.01, 0.01, 0.01) -> (1.1-1.2) -> (0.9-0.97) -> (1.0) over ~12 frames gives a bouncy "pop into existence" effect. Reverse (1.0 -> 1.3x0.4h -> 0.01) for despawn. These read clearly even at small character scale.

## 9. **Walk animation: location keyframes + scale oscillation**
Sine-wave squish (scale X +5%, Z -5%) alternating every few frames during movement creates a convincing walk bounce without rigging. Applied per walk segment between location keyframes.

## 10. **Chopping/working animation: small Z-axis oscillation**
Moving the character body up/down by 0.06-0.08 units in a sine pattern at ~3 frame intervals reads as chopping/working activity.

## 11. **Boolean hide properties MUST use CONSTANT interpolation**
When applying Bezier interpolation to all keyframes, explicitly skip `hide_render` and `hide_viewport` properties. These must stay CONSTANT or objects will blend between visible/invisible states instead of snapping. This is a common gotcha when doing bulk interpolation sweeps.

## 12. **BEZIER with AUTO_CLAMPED handles for all motion keyframes**
After setting all keyframes, run a pass setting `interpolation='BEZIER'` and `handle_left_type/handle_right_type='AUTO_CLAMPED'` on all keyframe points (except hide properties). Produces smooth motion without manual curve editing.

## 13. **Object-level visibility keyframing (not collection-level)**
Collection `hide_viewport` / `hide_render` cannot be keyframed in Blender 3.3.9. Workaround: iterate all objects in a collection, keyframe `hide_render` and `hide_viewport` on each object individually. Used for room reveals with 190+ objects.

## 14. **Staggered spawns feel more dynamic**
6-frame offset between teammate spawns makes sequences feel organic rather than mechanical. Same principle applies to particle appearances and prop materializations.

## 15. **Camera location keyframes require frame_set() first**
Camera location keyframes must be inserted with `scene.frame_set(frame)` called before each `keyframe_insert()`. Without setting the frame first, only the last keyframe registers. This differs from object location keyframes which work without frame_set.

## 16. **Camera zoom via ortho_scale animation**
Animating `camera.data.ortho_scale` (e.g., 16 to 8 over 72 frames) creates smooth zoom. Combined with camera target movement for reframing. Prefer this over animating camera position for pure zoom effects.

## 17. **Three-camera strategy over ortho_scale animation**
For large scale changes, having three cameras at different ortho_scales (close=5, medium=10, wide=35) and cutting between them is cleaner than animating ortho_scale across huge ranges. Animate target empties for smooth pans within each scale level.

## 18. **Camera rig: empty parent + Track To constraint**
The cleanest way to animate cameras. Move/animate the empty, camera follows. Track To with TRACK_NEGATIVE_Z and UP_Y works for standard isometric. Alternative: fixed rotation (52-60 deg X, 0, 32-45 deg Z) without Track To is simpler and more predictable for static isometric angles.

## 19. **Bezier curve point keyframing for tethers**
Keyframe individual `spline.bezier_points[i].co` values via `keyframe_insert(data_path="co", frame=f)`. Animation data lives on the curve data, not the object. Handle types should be AUTO for smooth interpolation.

## 20. **Ticket/prop arc motion via Bezier handles**
Position keyframes with a mid-point offset in Y/Z create smooth arcs automatically when using BEZIER interpolation. No need for path constraints or complex rigging.

## 21. **Text objects need rotation to face isometric camera**
For camera at rotation (60, 0, 45), text objects need rotation_euler = (90, 0, 45) to face the camera plane. Without this, text appears edge-on. Font size 0.35+ for draft resolution; 0.5+ recommended for 1080p final.

## 22. **Vertical camera transitions for multi-floor scenes**
Animate camera Z position (e.g., 12 to 19 over 24 frames) to follow characters between floors. Combined with ortho_scale adjustments to maintain framing at each level.

## 23. **Constraint enum values use full names in Blender 3.3.9**
The track_axis enum is `'TRACK_NEGATIVE_Z'` not `'TRACK_NEG_Z'`. Always use full enum strings or you get cryptic errors.

## 24. **Bottom squish for blob characters via vertex editing**
Iterating mesh vertices and scaling those with z < -0.3 by 0.5 (with a gradual blend zone between -0.3 and 0) creates a natural "sitting on surface" look without proportional editing tools.

## 25. **Re-parenting required after object duplication**
Duplicated children (`bpy.ops.object.duplicate`) still point to the original parent. Must explicitly set `child.parent = new_body` for each child in the duplicated set.
