# Character Builder Learnings

## Milestone 1: Base Blob Template

1. **UV Sphere works well for blob body.** 32 segments, 16 rings, radius 0.5 with subdivision level 2 gives a smooth, friendly shape. Flat shading still reads well with subdivision.

2. **Bottom squish via vertex editing.** Rather than proportional edit (hard via MCP), directly iterating mesh vertices and scaling z < -0.3 by 0.5 gives a nice "sitting on surface" look. Gradual blend zone between -0.3 and 0 prevents a hard edge.

3. **Shape keys work on subdivided meshes.** Added squash/stretch to body and blink/look/surprise to eyes without needing to apply the subdivision modifier first. Shape keys operate on the base mesh and the modifier applies on top.

4. **Eye shape keys for blink use Z-axis squish** (not Y) because the UV spheres are oriented with Z up in local space. Scaling Z to 0.1 gives a convincing blink.

5. **Emission material for spark** requires node setup -- can't just use `use_nodes = False` with emission. Created Emission node + Output node manually. Strength=2.0 gives a visible glow in EEVEE.

6. **Backpack uses rounded cube** (cube + subsurf level 2). Positioned at Y=0.3 (behind body center) to sit on the back. Parented to body so it follows.

7. **Viewport screenshot MCP tool** returned "No filepath provided" error. Workaround: render a quick preview to PNG via `bpy.ops.render.render(write_still=True)` at 50% resolution. This is reliable.

8. **Freestyle outlines** enabled at scene level. Line thickness set to 2.0 on default lineset. Visible in render output.

## Milestone 2: Four Personas (Cairn, Lumen, Meridian, Cadence)

9. **Duplicating with bpy.ops.object.duplicate works** but each object gets its own copy of the mesh data. This is actually desired since we need different materials per persona. The shape keys also come along for free.

10. **Re-parenting after duplicate is essential.** Duplicated children still point to the original parent. Must explicitly set `child.parent = new_body` for each child in the duplicated set.

11. **Eye traits via simple transforms.** Narrowed eyes = `scale.z = 0.85`, wide eyes = uniform 1.1 scale, tilted = `rotation_euler.z = 5 degrees`. These are additive to shape keys and work well.

12. **Color darkening for backpacks** -- simple `int(channel * 0.75)` gives a natural darker shade. Works across all palette colors.

## Milestone 3: Teammates (7 roles)

13. **Teammates at 60% scale** (radius 0.3 vs 0.5) read well as subordinate characters. The props (magnifying glass, compass, hard hat, etc.) are small enough to not overwhelm the blob but large enough to be identifiable.

14. **Aprons as accent markers** -- a flat plane with 15-degree X rotation positioned at the front of the body works as a simple visual accent. Better than trying to paint a partial texture.

15. **Torus for compass ring** orbiting at 70-degree tilt gives a nice 3D compass feel. Major radius = body radius + margin.

## Milestone 4: Subagent

16. **Translucent material via Principled BSDF** -- need `use_nodes = True` and `blend_method = 'BLEND'` on the material. Set Alpha input on Principled BSDF to 0.85. `use_nodes = False` flat materials don't support transparency in EEVEE.

17. **TetherAnchor as empty object** -- `PLAIN_AXES` type empty parented to body, positioned slightly behind. Clean attachment point for dotted-line tether during animation.

## Milestone 5: Animation Actions

18. **Shape key actions live on separate animation data.** Object actions go on `object.animation_data.action`. Shape key actions go on `object.data.shape_keys.animation_data.action`. These are independent -- you need to assign both when animating a character.

19. **Cyclic modifiers on fcurves** make looping actions seamless. Applied via `fcurve.modifiers.new('CYCLES')` after creating keyframes.

20. **Actions with use_fake_user=True** persist in the .blend file even when not assigned to any object. Essential for reusable action libraries.

21. **Stale actions accumulate** from keyframe operations that auto-create actions (e.g., KeyAction, Key.001Action). Clean these up explicitly with `bpy.data.actions.remove()` after setting `use_fake_user = False`.

22. **Render preview at 50% resolution** is fast enough for checking composition (~2 sec) while still showing colors and shapes clearly. Use for every major milestone.
