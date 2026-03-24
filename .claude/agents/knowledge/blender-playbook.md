# Blender Animation Playbook

## How this knowledge system works

This playbook uses a legal framework to organize animation knowledge:

| Concept | What it is | Where it lives | When to read |
|---------|-----------|----------------|--------------|
| **Law** | The animation spec: visual style, character design, storyboards, color palette | `prompts/[A04_ACTIVE]_kitchen_analogy_animations.md` | Before every build — it has the exact requirements |
| **Doctrine** | Our animation principles — how we approach every Blender build | **This file** | Every session, before building |
| **Jurisprudence** | Precedents from past builds — techniques, failures, workarounds | `.claude/agents/knowledge/learnings-blender-*.md` | When facing a specific problem similar to a past build |

**Doctrine is short and universal.** Specific hex values, frame counts, and storyboard details belong in the spec (law). Techniques that worked or failed belong in learnings (jurisprudence). This file holds only the principles that apply to EVERY Blender animation build.

---

## Doctrine

### 1. Everything is flat-shaded

No PBR, no reflections, no bump maps, no procedural textures. The proven pattern: `mat.use_nodes = False` with `mat.diffuse_color = (r, g, b, 1.0)`. This is simpler and more reliable than Principled BSDF with Metallic=0/Roughness=1. Exception: emission materials and transparency require `use_nodes = True` (see learnings-blender-materials.md). If you see specular highlights, you have failed the style test. Colors come from the palette in the spec only.

### 2. Orthographic camera, always

No perspective. 30-degree isometric tilt. Ortho scale sized to frame the action. Camera movement is slow pans and zooms on the empty parent — never dramatic rotations or perspective switches.

### 3. Freestyle outlines define the look

2px black Freestyle lines on all geometry. This is the single most important visual element after flat shading. Fallback chain if Freestyle causes render errors: (1) reduce to 1px, (2) try Compositor edge-detect node, (3) disable as last resort. Document which approach worked in learnings.

### 4. EEVEE, not Cycles

Render engine is EEVEE. No path tracing, no ray-traced shadows. The warm, clean look comes from simplicity, not computation. If EEVEE fails, try Workbench as emergency fallback. Engine string: `'BLENDER_EEVEE'` (not `BLENDER_EEVEE_NEXT` — that's Blender 4.0+; we run 3.3.9).

### 5. Warm palette, no cold colors in architecture

Walls: #F5F0EB. Floor: #C4A882. Counters: #D4B896. Accents: coral #FF6B6B, teal #4ECDC4, gold #FFE66D. The only cold colors are character-specific (Meridian blue, Cadence purple). If an architectural surface looks blue or gray-blue, it is wrong.

### 6. Simple primitives, never sculpted

Everything is box, cylinder, sphere, plane, or torus. Subdivision surface modifier (level 1-2) for softness when needed. No sculpting, no complex topology, no imported models. Monument Valley aesthetic — clean, geometric, readable.

### 7. Collections are rooms

Every room is a separate Blender collection. Every object is named `Room_Element_Detail` (e.g., `Kitchen_Counter_Main`, `Pantry_Shelf_Left`). This enables per-video visibility toggling. Unnamed objects are invisible to the team and will cause confusion.

### 8. Save after every major step

`bpy.ops.wm.save_as_mainfile()` after building each room, after each animation pass, after each render. Blender crashes lose everything. MCP connection drops lose everything. Save is free insurance — do it after every meaningful milestone.

### 9. Animations are shape keys + location keyframes

Walk = location keyframe + squash/stretch shape keys. Idle = scale oscillation + blink shape key. Spawn = scale 0→1.1→1.0 bounce. Keep it simple. If shape keys fail via MCP, fall back to pure location/scale/rotation keyframes. Simple movement that reads clearly beats complex rigging that breaks.

### 10. Render as PNG sequences, never video files

Output to numbered PNGs (`frame_####.png`). A partial render is still usable — you can see what worked. A crashed video file is worthless. Compositing to MP4 happens afterward, outside Blender if needed.

### 11. Characters are reusable, scenes are not

Characters (blob + eyes + spark + backpack) live in a shared `.blend` file and are linked/appended into video scenes. Each video scene is its own file or scene within a file. Never animate directly on the master character file — always work on copies.

### 12. Discover while building

This is the first Blender animation build. Techniques that work, MCP patterns that fail, timing that feels right — write it all down in per-agent learnings files (`output/kitchen_animation/learnings/`). These become jurisprudence for the next build.

---

## Blender MCP Essentials

```python
# Always import bpy at top of every execute_code call
import bpy

# Flat material creation pattern
def flat_mat(name, r, g, b):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (r, g, b, 1.0)
    mat.use_nodes = False
    return mat

# Hex color helper
def hex_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16)/255.0 for i in (0, 2, 4))

# Save pattern — use after EVERY major step
bpy.ops.wm.save_as_mainfile(filepath="/absolute/path/to/file.blend")
```

- Always use **absolute file paths** (MCP has no persistent cwd)
- Break work into **3-5 separate `execute_code` calls** per major element
- **Print summary** at end of each code block (object count, collection membership)
- **State does not persist** between `execute_code` calls — redefine helpers each time
- Always specify `target` in every MCP call: `blender_execute_code(target="main", code="...")`

---

## Review: Three Modes (Dedicated Reviewer Agent Required)

Every build MUST have a dedicated reviewer agent. Builders do not review their own work — they render preview frames, and the reviewer reads them and compares against references.

**Mode A — Style compliance**: Flat shading (no specular), palette match, Freestyle enabled, orthographic camera, correct resolution, PNG output format, collection naming. Reviewer renders a frame and checks pixel-level.

**Mode B — Visual quality & character fidelity**: Does it look like the references? Characters match the Clawd design (blocky body, four legs, square eyes, spark on top, role accessories)? Kitchen has color contrast, atmosphere, detail? Reviewer compares rendered frames against reference images.

**Mode C — Animation life**: Do characters feel alive? Check for:
- Idle emotes (fidgeting, looking around, ear/spark twitch)
- Reaction beats (surprise, satisfaction, frustration, thinking)
- Personality differences between characters (Cairn = steady, Lumen = bouncy, etc.)
- Timing pauses (not everything moves at constant speed — hesitation, anticipation, follow-through)
- "Breathing room" between actions (characters don't robotically move from A to B to C)

All three modes are mandatory. Render preview frames (`render(write_still=True)` at 50% resolution) after each major milestone. Do not use the viewport screenshot MCP tool — it fails with "No filepath provided."

### Character emote library (animate on ALL characters)

| Emote | Animation | When to use |
|-------|-----------|-------------|
| idle_fidget | Small random leg shifts, eye darts, spark flicker | Any pause > 1 second |
| thinking | Eyes up, spark brightens + slow pulse, body tilts slightly | Before decisions |
| surprise | Eyes widen (scale up 20%), small jump (Y +0.1), spark flash | Receiving unexpected input |
| satisfaction | Eyes narrow happily (Y squish), slight body bounce, spark steady glow | Task complete |
| frustration | Body shakes side-to-side (2 frames), eyes scrunch, spark dims | Error/retry |
| greeting | One leg lifts in a wave gesture, eyes brighten | Meeting another character |
| working_focused | Lean forward slightly, rapid spark flicker, squash/stretch | Intense work |
| celebratory | Jump + spin (Y rotation 360° over 12 frames), spark burst | Big achievement |

### 13. Never use render(animation=True) through MCP

`bpy.ops.render.render(animation=True)` blocks the MCP connection and times out even for 10 frames. Use frame-by-frame loop: `scene.frame_set(f)` + `render(write_still=True)` in batches of 25-40 frames per MCP call. This pattern rendered 4,080+ frames across 6 videos without failure.

### 14. Boolean hide properties stay CONSTANT

When smoothing all keyframes to BEZIER interpolation, explicitly skip `hide_render` and `hide_viewport` fcurves. These must remain CONSTANT interpolation or objects will partially fade between visible and invisible states instead of snapping.

### 15. Clean up after failures

Failed execute_code calls leave partial objects with `.001`/`.002` suffixes. Always run a cleanup pass after any error, removing suffixed duplicates before retrying.

---

*Doctrine updated after first overnight build (2026-03-24). 9 agent learnings files distilled into 4 topic files. 3 new doctrine rules added (13-15).*
