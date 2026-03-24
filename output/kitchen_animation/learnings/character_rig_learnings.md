# Character Rig Build Log

Building 21 emote animations for Cairn base character.
File: cairn_final.blend → cairn_final_all_emotes.blend

---

## 1. Bone parenting inverse matrix is unreliable via MCP
Setting `parent_type='BONE'` and computing `matrix_parent_inverse` manually
resulted in scattered objects. The operator `bpy.ops.object.parent_set(type='BONE')`
handles the inverse correctly but requires complex selection state via MCP.
**Solution:** Use direct object parenting (parent to body mesh) with
keyframes on individual objects. Less elegant than armature but reliable through MCP.

## 2. Direct object animation approach
Parent hierarchy: Root empty → Body → all parts as children.
Animate Root for world movement, Body for bounce/lean, children for individual motion.
Each object gets its own keyframes.

## 3. Per-object actions create duplicates
Each `animation_data_clear()` + rebuild creates new actions per object. With 14 objects
and 21 emotes, this generates 200+ actions with `.001`/`.002` suffixes. The keyframes
on the objects work correctly — it's just the action naming that's messy.

## 4. matrix_parent_inverse.identity() is critical
When setting `obj.parent = body` via script, always call `obj.matrix_parent_inverse.identity()`
immediately after. Without this, the inverse matrix from the previous parent persists.

## 5. Bevel modifier creates visual gaps at joints
Bevel rounds edges inward, making the surface smaller than mesh bounds.
Limbs that mathematically overlap can appear detached.
**Fix:** Push limbs deeper into body to compensate for bevel rounding.

## 6. Arm stretch via scale animation
Scaling arm.scale.z from 0.7 (stubby) to 1.5 (extended) with origin at shoulder
creates rubber-hose arm extension. Key: shift mesh vertices down so origin = top.

## 7. Eye expression vocabulary
- Normal: (1, 1, 1)
- Happy: (1, 1, 0.7) — Z squish
- Surprised: (1.3, 1, 1.3) — wide
- Focused: (0.95, 1, 0.85) — slight narrow
- Sleeping: (0.8, 1, 0.15) — nearly closed
- Frustrated: (0.9, 1, 0.7) — scrunched

## 8. Spark as emotion indicator
- Normal: scale 1.0, slow spin
- Thinking: pulsing 0.7-1.3, slow rise
- Happy: scale 1.2, faster spin
- Frustrated: scale 0.6, no spin
- Sleeping: scale 0.4, barely visible
- Surprise/Alert: flash to 1.8

## 9. 8-leg diagonal gait
Group A (1,3,6,8) vs Group B (2,4,5,7) alternate phase.
Walk: ±0.3 swing. Run: ±0.4, 2x speed.

## 10. sRGB color compensation
use_nodes=False doesn't render correct colors in EEVEE 3.3.9.
Use Principled BSDF with sRGB-to-linear: `((srgb + 0.055) / 1.055) ** 2.4`

## 11. Character design evolution
- Started as smooth blob (wrong) → blocky voxel cube (right)
- 4 legs → 8 legs (octopus reference)
- Flat paddle arms → leg-shaped tentacle arms (same geometry, different position)
- Arms: stubby at rest (scale.z=0.7), extend when reaching (scale.z=1.5)
- Shoulder pivot achieved by shifting arm mesh vertices to put origin at top
- Bevel on body only, limbs share the softness through their own smaller bevel

## 12. Always render and CHECK
Visual verification after every change. Code executing ≠ looking right.
Render from multiple angles (front, isometric, side) to catch issues.
