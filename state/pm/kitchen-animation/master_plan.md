# Kitchen Animation — Master Plan
**Project ID:** kitchen-animation
**Owner:** Andrea (with Claude execution)
**Created:** 2026-03-27
**Deadline:** March 30 (midterm), March 27 (screen test with Alex)

---

## Goal
Produce a pixel-art RPG-style animation of the "Kitchen" analogy for the midterm presentation. 6 scenes, Blender-rendered characters on HTML environments. Tells the story of how Andrea and Henna built their AI-assisted architecture workflow.

## Key references
- **Storyboard:** `output/kitchen_animation/STORYBOARD.md` (locked v2)
- **Design system:** `design_system/SPEC.md`
- **Canonical story:** `observations/research/strategy/kitchen_analogy_canonical.md`
- **Existing assets:** `output/kitchen_animation/assets/` (see inventory below)
- **HTML v1:** `output/kitchen_animation/kitchen_scene_v1.html`
- **Sprite test:** `output/kitchen_animation/sprite_test.html`

## Decisions
- **Scrap Blender kitchen environment** — built autonomously without feedback, mostly wrong. HTML/CSS handles all environments.
- **Keep all character models** — personas, specialists, subagent are good. Need finishing (emotes v2 arms) + transparent re-renders.
- **Specialist accessories should stay subtle** — at sprite scale (64-128px), only bold differences read. Don't over-detail.
- **HTML is the animation medium** — Blender produces sprites only. Scene composition, camera, transitions all in HTML/CSS/JS.

## Asset inventory (what exists)

### Characters (Blender models exist, renders on grey bg)
| Character | Colors | Accessories | Animations | Status |
|-----------|--------|------------|------------|--------|
| **Base (Cairn)** | Warm gold | None | 21 sets, 636 frames | Has renders, needs transparent bg |
| **Lumen** | Bright yellow | None | Static only (iso+front) | Needs animation renders |
| **Meridian** | Blue | None | Static only | Needs animation renders |
| **Cadence** | Purple | None | Static only | Needs animation renders |
| **Nova** | Pink | None | Static only | Needs animation renders |
| **Analyst** | Base + teal orb | Teal accessory | Static only | Needs animation renders |
| **Modeler** | Base + gold hat | Gold hat/beret | Static only | Needs animation renders |
| **Builder** | Base + side tool | Tool accessory | Static only | Needs animation renders |
| **Cartographer** | Base + gold ring | Gold halo | Static only | Needs animation renders |
| **Visualizer** | Base + pink pen | Pink brush | Static only | Needs animation renders |
| **Coordinator** | Base + ? | Has closeup | Static only | Needs animation renders |
| **Knowledge** | Base + ? | Has closeup | Static only | Needs animation renders |
| **Subagent** | Smaller, simpler | None | Static only | Needs animation renders |

### Emotes (face expressions on the cube)
- v1: 8 emotions (test renders)
- v2: 8 emotions + big versions + variants (happy_crescent, happy_v2)
- v3: 9 emotions (latest, at root assets level)
- **Arm rig:** rest, wave, celebrate, point, casual — both normal and stubby variants
- **Status:** Andrea finishing v2 arm movements. Not production-ready yet.

### Environment
- kitchen_v2, kitchen_v3 renders — **SCRAPPED** (autonomous, no feedback)
- exterior, house previews — may be useful for context but not for animation

---

## Phases

### Phase 0: Character Sign-off (~1 session, Andrea)
**Goal:** Finalize character design — emotes v2 arms, confirm which poses/expressions to render for animation.
**Topology:** Solo (Andrea in Blender, manual)
**Team:** Andrea only
**Produces:**
- Final Blender files with working arm rig + emotes
- Decision: which 4-6 key poses per character for the animation
- Decision: which personas appear in which scenes
**Dependencies:** None
**Success:** Andrea says "characters are ready to render"

### Phase 1: Sprite Rendering (~1-2 sessions, Blender MCP)
**Goal:** Batch render all needed sprites with transparent backgrounds.
**Topology:** Hierarchical, narrow context. One coordinator directing Blender.
**Team:** 1 agent (Blender MCP)
**Reads:** Storyboard, character sign-off decisions from Phase 0
**Produces:** (all to `output/kitchen_animation/sprites/`)
- Key poses for each persona (idle, walk, type, hold, celebrate — 4-6 frames each)
- Grey (desaturated) variants for Scene 1
- Grey → color transition frames (3-4 per persona)
- Specialist agents with accessories (2-3 poses each)
- Subagent (2 poses)
- Props: scrolls (gold + teal), backpack states, big book
- ALL on transparent background, 128×128px
- Sprite sheets + JSON coordinate maps
**Dependencies:** Phase 0 complete
**Success:** All sprites render cleanly at 64-128px on dark background. Sprite test page updated with new assets.

### Phase 2: Hero Illustrations (~1 session, could be HTML or Blender)
**Goal:** Create the two "Minecraft map moment" illustrations + specialist scroll zoom.
**Topology:** Flat, narrow context. Illustration work.
**Team:** 1 agent (HTML/CSS or manual design)
**Produces:**
- CLAUDE.md treasure map (parchment, warm, repo as locations)
- .claude/ blueprint (technical drawing, cool, kitchen equipment specs)
- Specialist scroll example (zoomed map of one area)
- Git branch diagram (for Scene 3 zoom)
**Dependencies:** Can run parallel to Phase 1
**Success:** Illustrations read clearly at 1920×1080 and feel distinct from each other (warm map vs cool blueprint).

### Phase 3: HTML Scene Assembly (~2-3 sessions, Claude)
**Goal:** Build each of the 6 storyboard scenes as HTML with real sprites.
**Topology:** Hierarchical, broad context. One builder with full storyboard knowledge.
**Team:** 1-2 agents (builder + optional visualizer)
**Reads:** Storyboard, all sprites from Phase 1, illustrations from Phase 2, design system
**Produces:** (to `output/kitchen_animation/`)
- `kitchen_scene_v2.html` — complete 6-scene animation
- Scene-by-scene: room layouts, furniture, character placement, transitions
- Integrated sprites replacing CSS placeholders
- Camera movement, dialogue, typewriter text
- Keyboard/click navigation
- Responsive scaling (works on laptop + presentation screen)
**Dependencies:** Phase 1 (sprites) + Phase 2 (illustrations)
**Success:** Full walkthrough of all 6 scenes, characters animate, story reads clearly.

### Phase 4: Polish + Screen Test (~1 session, Andrea + Claude)
**Goal:** Iterate based on Andrea's feedback. Fix timing, adjust positions, tune animations.
**Topology:** Pair work (Andrea directs via desktop app screenshots, Claude edits)
**Team:** Andrea + 1 agent
**Produces:**
- `kitchen_scene_final.html`
- Screen-captured video for backup (in case live HTML fails during presentation)
**Dependencies:** Phase 3 complete
**Success:** Andrea and Alex approve at screen test. Runs smoothly on presentation hardware.

---

## Schedule

| Phase | When | Who | Est. time |
|-------|------|-----|-----------|
| 0 | March 27 (today) | Andrea | 1-2 hrs |
| 1 | March 27-28 overnight/morning | Claude (Blender MCP) | 2-3 hrs |
| 2 | March 27-28 (parallel with 1) | Claude | 1-2 hrs |
| 3 | March 28-29 | Claude | 3-4 hrs |
| 4 | March 29 | Andrea + Claude | 1-2 hrs |

**Total:** ~8-13 hrs across 3 days. Tight but doable if Phase 0 happens today.

---

## What was scrapped
- Blender kitchen environments (kitchen_v2, v3) — built without feedback, wrong layouts
- Full 3D animation approach — HTML handles composition, Blender handles characters only
- AI video generation — too imprecise for this specific narrative
