# Blender Sprite Sheet Generation — Kitchen Animation Characters

## Context

You're generating pixel-art-style character sprites for an animated HTML presentation called "The Kitchen." It tells the story of how Andrea and Henna built their AI-assisted architecture workflow, using a kitchen/brigade analogy. The sprites will be used in a top-down RPG-style HTML scene (think Stardew Valley / Pokemon / the reference images Andrea provided).

This also serves as a **rehearsal** for the pixel agent preview dashboard — the architecture workflow visualization where agents appear as pixel characters in an office/kitchen environment.

## What exists

- **Claude character emotes v1** — already modeled in Blender. Andrea is finishing v2 (arm movements).
- **Kitchen scene HTML** — at `output/kitchen_animation/kitchen_scene_v1.html`. Uses CSS placeholder characters. The sprites you generate will replace them.
- **Design system** — `design_system/SPEC.md`. Dark palette: bg #0c0c14, gold #c9a84c, copper #b87a56, teal #5b8fa8.

## Characters to generate

7 characters total. Each has a role color and personality.

| # | Character | Role | Color accent | Body notes |
|---|-----------|------|-------------|------------|
| 1 | **Andrea** | Chef de cuisine | Gold #c9a84c | Dark hair, casual outfit (dark blue/indigo #4a4a6a) |
| 2 | **Henna** | Chef de cuisine | Copper #b87a56 | Dark hair, outfit in muted plum/mauve #6a4a5a |
| 3 | **Claude (Sous Chef)** | Main session AI | Teal #5b8fa8 | Distinctive — not human. Warm skin tone #d4a574, teal shirt/apron, no hair (or minimal). Should feel friendly, capable. Carries a visible **backpack** on back. |
| 4 | **Commis (Subagent)** | Temporary helper | Muted #5a7a8a | Smaller than other characters (~75% scale). Light blue tint #b8d4e8 for head. Simple, disposable feel. |
| 5 | **Analyst (Chef de partie)** | Specialist agent | Copper variant | Similar to Claude but with brown apron, different stance. Name badge if possible. |
| 6 | **Modeler (Chef de partie)** | Specialist agent | Copper variant | Similar build, darker apron, maybe holding a tool. |
| 7 | **Builder (Chef de partie)** | Specialist agent | Copper variant | Similar build, work gloves or tool belt feel. |

## Poses / frames per character

**Camera angle: 3/4 top-down** (isometric RPG view — camera ~45 degrees above, slightly behind). ONE angle only. All characters face **down-right** (toward camera) as the default.

### Full grid (ideal — 12 frames per character)

| Pose | Frames | Description |
|------|--------|-------------|
| **Idle A** | 1 | Standing neutral, arms at sides |
| **Idle B** | 1 | Slight shift — weight on other foot, tiny bob. For idle animation loop (A→B→A→B) |
| **Walk 1** | 1 | Right foot forward |
| **Walk 2** | 1 | Left foot forward |
| **Walk 3** | 1 | Right foot passing |
| **Walk 4** | 1 | Left foot passing |
| **Sit** | 1 | Seated at desk (lower body hidden by desk in scene) |
| **Type** | 2 | Sitting, hands on keyboard, slight variation between frames |
| **Hold item** | 1 | Holding a document/scroll in front |
| **Pass item** | 1 | Arm extended, handing something off |
| **Emote: think** | 1 | Hand on chin or ? above head |

### Minimum viable (if time is short — 4 frames per character)

| Pose | Frames |
|------|--------|
| Idle A | 1 |
| Idle B | 1 |
| Sit/type | 1 |
| Hold item | 1 |

### Claude-specific extras

Claude (character 3) needs **backpack states** — the backpack visually grows:

| State | Description |
|-------|-------------|
| **Empty** | Small, flat backpack |
| **Medium** | Slightly bulging, a scroll poking out |
| **Full** | Stuffed, multiple scrolls visible |
| **Overflow** | Comically overstuffed, red tint, items falling out |

Render these as 4 variants of the Idle A pose. The HTML will swap between them as the story progresses.

## Render specifications

| Parameter | Value |
|-----------|-------|
| **Resolution per frame** | 128 x 128 px |
| **Background** | Transparent (PNG with alpha) |
| **Style** | Low-poly / stylized to read well at small sizes. NOT photorealistic. Think chunky, readable silhouettes. |
| **Lighting** | Soft top-down, consistent across all characters. Slight rim light for readability on dark backgrounds. |
| **Output format** | Individual PNGs named: `{character}_{pose}.png` (e.g., `andrea_idle_a.png`, `claude_walk_1.png`, `claude_backpack_full.png`) |

## Sprite sheet assembly

After rendering all individual frames, assemble into sprite sheets:

- One sprite sheet per character
- Grid layout: poses as columns, frames as rows
- 128px cells, no padding
- Save as: `spritesheet_{character}.png`
- Also save a JSON map: `spritesheet_{character}.json` with frame coordinates

Example JSON:
```json
{
  "character": "claude",
  "frameSize": [128, 128],
  "poses": {
    "idle_a": {"x": 0, "y": 0},
    "idle_b": {"x": 128, "y": 0},
    "walk_1": {"x": 256, "y": 0},
    "walk_2": {"x": 384, "y": 0}
  }
}
```

## Output location

All renders go to: `output/kitchen_animation/sprites/`

```
output/kitchen_animation/sprites/
├── individual/          ← single frame PNGs
│   ├── andrea_idle_a.png
│   ├── andrea_idle_b.png
│   ├── ...
│   ├── claude_backpack_empty.png
│   ├── claude_backpack_full.png
│   └── ...
├── spritesheet_andrea.png
├── spritesheet_andrea.json
├── spritesheet_henna.png
├── spritesheet_henna.json
├── spritesheet_claude.png
├── spritesheet_claude.json
├── spritesheet_commis.png
├── spritesheet_commis.json
├── spritesheet_analyst.png
├── spritesheet_analyst.json
├── spritesheet_modeler.png
├── spritesheet_modeler.json
└── spritesheet_builder.png
    spritesheet_builder.json
```

## Integration with kitchen HTML

Once sprites exist, the CSS swap is straightforward. In `kitchen_scene_v1.html`, replace each `.char-body` with:

```css
.character .sprite {
  width: 128px;
  height: 128px;
  background-image: url('sprites/spritesheet_andrea.png');
  background-position: 0 0; /* idle_a */
  background-size: auto;
  image-rendering: pixelated;
}

/* Idle animation */
.character.anim-idle .sprite {
  animation: sprite-idle 1s step-start infinite;
}
@keyframes sprite-idle {
  0% { background-position: 0 0; }       /* idle_a */
  50% { background-position: -128px 0; }  /* idle_b */
}
```

A follow-up session can handle the HTML integration — just generate the sprites.

## Priority order

If you can't do all 7 characters, prioritize:
1. **Claude** (with backpack states) — the main character
2. **Andrea** — chef de cuisine
3. **Henna** — chef de cuisine
4. **Commis** — for the brigade scene
5. Analyst / Modeler / Builder (can share a base with palette swaps)

## Style references

Look at Andrea's reference images (shared in conversation). Key traits:
- Warm pixel art aesthetic
- Characters are small but expressive (big heads relative to body)
- Furniture and characters coexist on checkered/wooden tile floors
- Dark environment (image 4 is the palette target) — characters need enough contrast/rim light to pop

The overall vibe: cozy RPG studio, not sterile office. A kitchen where work happens.
