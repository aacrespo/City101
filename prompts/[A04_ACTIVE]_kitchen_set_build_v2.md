# Kitchen Set Build — Agent Teams (v2)
# Status: [A04_ACTIVE]
# Execution: Agent Teams — coordinated multi-session build
# Prerequisites: 4 Blender instances on ports 9876, 9877, 9878, 9879

---

## Context

This is the SECOND attempt at the kitchen set. The first overnight build produced
geometry but with wrong character design (smooth blobs → now blocky voxel Clawds)
and poor visual quality (washed out, no atmosphere). This build gets it right.

**Read first:**
- /Users/andreacrespo/CLAUDE/city101/.claude/agents/knowledge/blender-playbook.md
- /Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
- /Users/andreacrespo/CLAUDE/city101/state/sessions/2026-03-24_0858.md (previous session decisions)

---

## Character Reference

The Clawd character is a blocky voxel creature (NOT a smooth blob):
- Body: beveled cube, ~0.5 wide, ~0.42 tall
- 8 legs: 2 rows of 4, octopus style, hanging from body bottom
- 2 arms: tentacle-like, same shape as legs but stubbier at rest (scale.z=0.7),
  stretch when reaching (scale.z up to 1.5). Shoulder at upper body.
- Eyes: 2 black squares on front face, slightly asymmetric
- Spark: ico sphere crystal above head, emission material
- Backpack: beveled cube on back

Character .blend files are at:
```
output/kitchen_animation/assets/cairn_final.blend        ← BASE (DO NOT OVERWRITE)
output/kitchen_animation/assets/cairn_final_BACKUP.blend  ← BACKUP
output/kitchen_animation/assets/lumen_final.blend
output/kitchen_animation/assets/meridian_final.blend
output/kitchen_animation/assets/cadence_final.blend
output/kitchen_animation/assets/teammate_*.blend          ← 7 role variants
output/kitchen_animation/assets/subagent.blend
```

**DO NOT open, modify, or save over any character .blend files.**
Append/link characters FROM these files INTO your scene files.

---

## Scale Convention

The Clawd character is ~0.5 wide, ~1.0 tall with legs. Design everything relative to this:

| Element | Size | Relative to Clawd |
|---------|------|--------------------|
| Kitchen floor | 4 x 3 units | Clawd fills ~12% of floor width |
| Counter height | 0.45 units | Just below Clawd's body center |
| Wall height | 1.5 units | 1.5x Clawd height |
| Door | 0.5 x 1.1 units | Clawd fits through comfortably |
| Chair/stool | 0.35 tall | Clawd can sit |
| Shelf height | 0.15 spacing | Fits jars/books |
| Mug/jar | 0.05-0.08 | Clawd can hold in tentacle arms |

---

## Critical Blender MCP Rules

### Transform apply bug (Blender 3.3.9)
```python
# WRONG — applies ALL transforms including location, moves origin to (0,0,0)
bpy.ops.object.transform_apply(scale=True)

# RIGHT — only applies scale, preserves location
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
```

### sRGB color conversion (required for correct colors)
```python
def srgb(hex_str):
    h = hex_str.lstrip('#')
    sr, sg, sb = [int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4)]
    def to_lin(c): return ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92
    return (to_lin(sr), to_lin(sg), to_lin(sb), 1.0)

# Material creation pattern
def mat(name, hex_str):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    for n in m.node_tree.nodes:
        if n.type == 'BSDF_PRINCIPLED':
            n.inputs['Base Color'].default_value = srgb(hex_str)
            n.inputs['Roughness'].default_value = 1.0
            n.inputs['Specular'].default_value = 0.0
    return m
```

### State doesn't persist between execute_code calls
Redefine ALL helpers (srgb, mat, add) at the top of every code block.

### Save after every major step
```python
bpy.ops.wm.save_as_mainfile(filepath="/absolute/path/to/file.blend")
```

### Render and CHECK visually
After every major element, render a preview and READ the image to verify.
Do NOT proceed without checking.

---

## Pixel Art Render Pipeline

Render at LOW resolution with NO anti-aliasing, upscale with nearest neighbor:

```python
# EEVEE settings for pixel art
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 480
scene.render.resolution_y = 270
scene.eevee.taa_render_samples = 1  # single sample, no AA
scene.render.use_freestyle = True
scene.render.film_transparent = False
```

Upscale to 1080p with ffmpeg:
```bash
ffmpeg -framerate 24 -i frame_%04d.png \
  -vf "scale=1920:1080:flags=neighbor" \
  -c:v libx264 -pix_fmt yuv420p -crf 18 output.mp4
```

---

## Color Palette

The kitchen is WARM with COLOR POPS. Not all beige.

| Element | Hex | Role |
|---------|-----|------|
| Floor (wood) | #9B7B5A | warm base |
| Walls | #F0E8DD | cream backdrop |
| Counter (wood) | #B89470 | furniture |
| Counter top | #E8DDD0 | lighter surface |
| Stove | #3A3A3A | dark appliance |
| Fridge | #CC4444 | RED — color pop |
| Mug | #E07B4A | ORANGE — color pop |
| Towel | #4ECDC4 | TEAL — color pop |
| Plant | #5B8C3E | GREEN — life |
| Books | #C0392B, #2980B9, #27AE60 | colored spines |
| Tickets | #FCF3CF | yellow paper |
| Corkboard | #BFA87A | natural |
| Pins | #E74C3C | red accents |

---

## Team Roles

### Builder A: Kitchen Room (instance: main, port 9876)
Build the main kitchen floor — the primary set where most videos take place.

**Elements to build:**
- Floor (single plane, warm wood)
- 3 walls (front removed for cross-section), 1.5 units tall
- Center island counter with lighter top surface
- Stove (dark, back left, against wall) with 4 burners, pot, pan
- RED fridge (back right, against wall) with handle
- Prep counter (right side) with food items on it
- Recipe book stand (on center counter, open book)
- Knife block with blades (on center counter)
- Order ticket wire + 4 yellow tickets (above counter)
- Spice rack on back wall (5 jars with colored lids)
- Corkboard by door (left wall) with colored notes + red pins
- Framed CLAUDE.md (left wall)
- Door (left wall, separate object for animation)
- Coat hooks by door
- Serving hatch (opening in back wall with shelf)
- Orange mugs on counter (2)
- Teal towel draped on counter edge
- Plant in corner (pot + green sphere)
- Books stacked on shelf/floor
- Timer on wall (red ring + white circle)

**Critical: EVERYTHING FLUSH TO WALLS. No gaps between furniture and walls.**
The stove back should touch the back wall. The fridge side should touch the right wall.

**Camera:** Orthographic isometric, ortho_scale=5, Track To target at (0, 0.3, 0.5)
**Lighting:** Sun (warm, 2.0) + Fill (0.5, no shadow) + Ambient point light (warm, 15 energy)
**Save to:** output/kitchen_animation/assets/kitchen_final.blend

### Builder B: Pantry Room (instance: second, port 9877)
Build the pantry — attached to kitchen through a door in the right wall.
Smaller room, ~1.5 x 2.5 units. Three distinct wall sections:
- Left wall: Ingredient bins (L1 — SQLite) — 6 cylinder jars on shelves with colored lids
- Back wall: Recipe card cabinet (L2 — Markdown) — rectangular furniture with drawers
- Right wall: Equipment rack (L3 — Scripts) — pegboard with tool shapes
- Door connecting to kitchen
- A few items on floor (crate, sack) for lived-in feel

**Save to:** output/kitchen_animation/assets/pantry_final.blend

### Builder C: Library/Study (instance: third, port 9878)
Build the library — sits above the kitchen (upper floor).
About 3 x 2 units, warmer/darker scholarly tones.
- Bookshelves on walls with COLORED book spines (variety!)
- Reading desk with chair
- Lightbox table (slight glow emission)
- Filing cabinet with drawers
- Staircase/ladder suggesting connection to kitchen below
- Loose books on desk, open notebook, mug — lived-in

**Save to:** output/kitchen_animation/assets/library_final.blend

### Reviewer (instance: fourth, port 9879)
**Does NOT build.** Reviews work from other builders.

After each builder finishes a major section:
1. Open their .blend file
2. Render from multiple angles (front, iso, close-up)
3. READ each render image to check:
   - **Style compliance:** Flat shading, correct palette, no specular
   - **Scale:** Furniture proportional to Clawd (append cairn_final.blend character to check)
   - **Alignment:** Everything flush to walls, no floating objects, no gaps
   - **Atmosphere:** Does it feel warm, lived-in, populated?
   - **Pixel art readiness:** Will it look good at 480x270?
4. Report issues back to the builder's instance
5. Final: assemble all rooms into one cross-section scene

**The reviewer renders a frame with a Clawd character in the kitchen to verify scale.**

---

## Coordination Protocol

1. All builders read this prompt + the Blender playbook before starting
2. Each builder works in their OWN .blend file — never open another builder's file
3. Reviewer opens builder files READ-ONLY (open, render, close — don't save)
4. All rooms use the same Y=0 ground level, so they can be assembled into a cross-section later:
   - Kitchen: floor at Z=0
   - Pantry: floor at Z=0, offset in X (to the right of kitchen)
   - Library: floor at Z=1.6 (above kitchen, accounting for wall height + floor thickness)
5. Save after every major element. Render and CHECK after every major element.

---

## Learnings from First Build (apply these)

1. `transform_apply(scale=True)` bakes location too — use explicit flags
2. Render at correct scale — test with character in scene
3. Furniture MUST be flush to walls (no gaps)
4. Items need to be large enough to read at 480x270
5. Color contrast matters — not everything beige
6. Lived-in feel: mugs, food, towels, books, notes — not a showroom
7. Frame-by-frame render batches (30-40 per MCP call), never `render(animation=True)`
8. sRGB-to-linear conversion required for correct material colors
9. MCP state doesn't persist — redefine helpers every call
10. ALWAYS render and look at the image before proceeding

---

## Output Structure

```
output/kitchen_animation/assets/
├── kitchen_final.blend      ← Builder A
├── pantry_final.blend       ← Builder B
├── library_final.blend      ← Builder C
├── house_assembled.blend    ← Reviewer (final assembly)
└── set_previews/
    ├── kitchen_iso.png
    ├── kitchen_front.png
    ├── kitchen_with_cairn.png
    ├── pantry_iso.png
    ├── library_iso.png
    └── house_crosssection.png
```
