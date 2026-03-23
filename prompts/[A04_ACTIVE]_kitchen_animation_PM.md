# Kitchen Animation — Project Manager (Overnight Build)
# Status: [A04_ACTIVE]
# Execution: Single PM session that spawns teammates via Agent Teams
# Prerequisites: 3 Blender instances running with router MCP on ports 9876, 9877, 9878

---

## Your Role

You are the Project Manager for an overnight autonomous build of animated
videos in Blender. You coordinate teammates, sequence work, handle errors,
and ensure deliverables are ready by morning.

Read the full animation spec first:
- /Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md

That document contains EVERYTHING: visual style, character design, house layout,
all 9 video storyboards, color palette, execution strategy. Study it thoroughly
before spawning any teammates.

Also read:
- /Users/andreacrespo/CLAUDE/city101/CLAUDE.md

---

## Blender Router Setup

The Blender MCP uses a router (same pattern as Rhino). Every Blender tool call
takes a `target` parameter to route to a specific instance.

| Instance | Port | Assignment |
|----------|------|-----------|
| main | 9876 | Phase 1: House Set → Phase 2: Video animations |
| second | 9877 | Phase 1: Characters → Phase 2: Video animations |
| third | 9878 | Phase 1: Exterior + camera rigs → Phase 2: Video animations |

All teammates MUST specify `target` in every Blender MCP call.

**Router tool names are prefixed with `blender_`:**
- `blender_get_scene_info(target="main")` — get scene info
- `blender_execute_code(target="main", code="...")` — run Python/bpy code
- `blender_get_viewport_screenshot(target="main")` — capture viewport
- `blender_transfer_geometry(source="second", destination="main", ...)` — move geometry between instances
- `blender_list_instances()` — check all instances and connection status
- `blender_command(target, command_type, params)` — generic passthrough

---

## Phase 0: Smoke Test (before anything else)

Before spawning any teammates, verify the MCP pipeline works:

1. Create output directories:
   ```python
   import os
   for d in ["output/kitchen_animation/assets",
             "output/kitchen_animation/renders/video_01",
             "output/kitchen_animation/renders/video_02",
             "output/kitchen_animation/renders/video_04",
             "output/kitchen_animation/renders/video_05",
             "output/kitchen_animation/renders/video_06"]:
       os.makedirs(d, exist_ok=True)
   ```

2. Test each Blender instance:
   ```
   blender_get_scene_info(target="main")
   blender_get_scene_info(target="second")
   blender_get_scene_info(target="third")
   ```

3. Test code execution on one instance:
   ```
   blender_execute_code(target="main", code="""
   import bpy
   bpy.ops.mesh.primitive_cube_add(size=1, location=(0,0,0))
   mat = bpy.data.materials.new("Test_Mat")
   mat.diffuse_color = (0.77, 0.66, 0.51, 1.0)
   bpy.context.active_object.data.materials.append(mat)
   print(f"Created test cube: {bpy.context.active_object.name}")
   """)
   ```

4. Clean up: delete the test cube.

If ANY of these fail, log the error in BUILD_LOG.md and stop. Do not proceed
with the overnight build if the MCP pipeline is broken.

---

## Phase 1: Assets (parallel, ~2-3 hours)

Spawn TWO teammates simultaneously:

### Teammate A: "House Set Builder" → target: main (port 9876)

<house-builder-prompt>
You are building the complete house set for the kitchen analogy animations.
Work in Blender instance "main" (target: "main" on every MCP call).

Read the full spec:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
Focus on Part 1 (Visual Style) and Part 3 (The Complete House).

IMPORTANT STYLE RULES:
- Orthographic camera, 30 degrees, isometric view
- ALL materials: flat shading, solid colors from the palette, NO PBR
- Freestyle lines: 2px black outlines
- EEVEE renderer
- Everything is simple box/cylinder primitives. This is low-poly/voxel aesthetic.

BUILD THE HOUSE IN THIS ORDER:

1. **Main Floor — The Kitchen** (priority, most videos use this)
   - Floor: 12x8 units, warm wood material (#C4A882)
   - Walls: 3 units tall, cream (#F5F0EB), one wall removed (cross-section)
   - Main counter (center island): 3x1.5x0.9 units, wood (#D4B896)
   - Stove: 1x0.6x0.9 units, stainless (#B8B8B8), with 4 circular burners
   - Prep counter (output/): 2x0.8x0.9 units, slightly messy looking
   - Serving hatch: opening in far wall, 1.2x0.8 units, with small shelf
   - Recipe book stand on counter: small angled surface with open book shape
   - Knife block: small block with blade shapes, on counter
   - Order ticket wire: thin cylinder above counter, with small rectangles hanging
   - Spice rack on wall: small shelf with tiny cylinder jars
   - Kitchen timer on wall: small circle
   - Front door: in near wall, 1x2.2 units, hinged (separate object for animation)
   - Coat hooks by door: small pegs
   - Corkboard by door: rectangle on wall, with small pinned rectangles
   - Framed CLAUDE.md: rectangle on wall near door
   - Vacuum sealer (sealing station): small box on far counter
   - Chimney: extends up from roof, visible from outside

2. **The Pantry** (attached room, through door in kitchen wall)
   - Smaller room: 4x6 units
   - Door connecting to kitchen
   - Left wall: ingredient bins — 6 large cylinder jars on shelves, with labels
   - Back wall: recipe card cabinet — rectangular furniture with small drawers
   - Right wall: equipment rack — pegboard (flat plane) with tool shapes hanging

3. **Three Windows in kitchen back wall** (MCP connections)
   - Window 1 → Workshop (Rhino): visible workbench + screen inside
   - Window 2 → Rendering Studio (Blender): camera + lights inside
   - Window 3 → Comms Room (Discord): intercom unit + message board
   - Each annexed room: 3x3 units, visible through window

4. **The Library / Study** (upstairs)
   - Floor above kitchen, slightly smaller
   - Bookshelves on walls (box shapes with vertical dividers)
   - Reading desk with chair
   - Lightbox table (flat glowing surface)
   - Filing cabinet

5. **The Gallery** (upstairs, next to library)
   - Pedestals (cylinders) with glowing rectangles on top (screens)
   - Frames on walls

6. **Basement — Freezer**
   - Below kitchen
   - Metal shelving (thin cylinders for frame, boxes for containers)
   - Frost effect: slightly blue-tinted lighting
   - Sealed boxes with labels

7. **Attic**
   - Triangular roof space
   - Boxes covered in sheets (rounded box shapes)

8. **Exterior**
   - Roof with chimney
   - Garden with mailbox
   - Street in front
   - 2-3 empty buildings across the street (for VM scaling video)
   - Pneumatic tube system connecting buildings (thin cylinders)

9. **Organization**
   - Put each room on a SEPARATE collection/layer in Blender
   - Name everything clearly: "Kitchen_Floor", "Kitchen_Counter_Main", etc.
   - This allows videos to show/hide rooms as needed

10. **Camera & Lighting**
    - Set up orthographic camera at isometric angle (30° tilt)
    - Single warm directional light (~4500K)
    - Ambient fill (world background: very light warm gray)
    - Enable Freestyle with 2px black lines

SAVE periodically via:
```python
bpy.ops.wm.save_as_mainfile(filepath="/Users/andreacrespo/CLAUDE/city101/output/kitchen_animation/assets/house_set.blend")
```
Final save to the same path when done.

When done, write a summary to output/kitchen_animation/assets/house_manifest.txt
listing all collection names, object counts per collection, and any missing elements.

IMPORTANT: If a Blender MCP call fails, try once more. If it fails again,
log the error, skip that element, continue with the next. Do not get stuck
on any single object. The house needs to be COMPLETE even if some details
are missing.
</house-builder-prompt>

### Teammate B: "Character Builder" → target: second (port 9877)

<character-builder-prompt>
You are building all blob characters for the kitchen analogy animations.
Work in Blender instance "second" (target: "second" on every MCP call).

Read the full spec:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
Focus on Part 2 (Characters — The Claude Blobs).

BUILD IN THIS ORDER:

1. **Base Blob** (template for all characters)

   The blob is inspired by the Claude AI icon — soft, rounded, friendly.

   Body construction via execute_blender_code:
   ```python
   # Start with UV sphere, 32 segments
   # Scale: X=1.0, Y=0.9, Z=1.1 (slightly tall, slightly narrow depth)
   # Apply subdivision surface modifier (level 2) for softness
   # Proportional edit to squish bottom slightly (sits on surface)
   ```

   Add as child objects:
   - Left eye: black sphere, scale 0.08, positioned upper-left of face
   - Right eye: black sphere, scale 0.1, positioned upper-right of face
     (slightly different sizes = personality)
   - Spark/antenna: small diamond/octahedron, positioned above head,
     with emission material (glows gently)
   - Backpack: rounded cube (~30% of body size), positioned on back,
     slightly darker shade of body color

   Shape keys (for animation):
   - "squash": compress Y by 10%, expand X by 5% (for walk bounce)
   - "stretch": expand Y by 10%, compress X by 5%
   - "blink": scale both eyes Y to near-zero
   - "look_left": translate both eyes X by -0.05
   - "look_right": translate both eyes X by +0.05
   - "surprise": scale both eyes up by 20%

2. **Four Personas** (duplicate base, recolor)

   | Name | Body Color | Spark Color | Eye trait |
   |------|-----------|-------------|-----------|
   | Cairn | #D4A574 (warm amber) | #FF8C42 (orange) | Slightly narrowed (scale eye Y to 0.85) |
   | Lumen | #FFD700 (soft gold) | #FFEB3B (yellow) | Wide open (scale eyes up 10%) |
   | Meridian | #6B9BD2 (cool blue) | #81D4FA (ice blue) | Even, calm (default size) |
   | Cadence | #9B8EC4 (soft purple) | #CE93D8 (lavender) | Slightly tilted (rotate one eye 5°) |

   Each gets a backpack in a slightly darker shade of their body color.

3. **Teammate Blobs** (7 roles, smaller)
   Scale: 60% of base blob size. Same shape, add role props:

   | Role | Accent | Prop to add |
   |------|--------|------------|
   | Analyst | #66BB6A green | Small sphere near eye (magnifying glass) |
   | Cartographer | #42A5F5 blue | Small torus orbiting body (compass) |
   | Modeler | #FFA726 orange | Flat cylinder on head (hard hat) |
   | Visualizer | #EC407A pink | Thin cylinder in one side (paintbrush) |
   | Builder | #78909C gray | Small wrench shape on side |
   | Knowledge | #8D6E63 brown | Small open book (two planes in V shape) |
   | Coordinator | #ECEFF1 white | Small rectangle held (tablet) |

   Body color for teammates: use a neutral base (#B0B0B0) with the accent
   color as an apron (a flat curved plane on the front of the body).

4. **Subagent Blob**
   Scale: 40% of base blob. Same color as parent but with transparency
   (alpha 0.85 in material). Add a small tether anchor point (empty object)
   for connecting to parent with a dotted line during animation.

5. **Reusable Animation Actions**
   Create these as Blender Actions (reusable across any character):

   "walk_cycle" (1 second loop):
   - Frame 1: position Y=0, squash shape key=0
   - Frame 6: position Y=0.5, squash=0.3 (compressed, mid-step)
   - Frame 12: position Y=1.0, squash=0 (back to normal)
   - Frame 18: position Y=1.5, squash=0.3
   - Frame 24: position Y=2.0, squash=0 (full cycle)
   - Spark bobs faster during walk (Z oscillation doubled)

   "idle_breathe" (3 second loop):
   - Gentle scale oscillation: all axes ±2%, sine wave
   - Occasional blink: every ~4 seconds, blink shape key 0→1→0 over 3 frames
   - Spark gentle rotation (Z axis, slow)

   "spawn_pop" (0.5 seconds):
   - Frame 1: scale=0, particle burst
   - Frame 6: scale=1.15 (overshoot)
   - Frame 9: scale=0.95 (settle)
   - Frame 12: scale=1.0 (final)

   "despawn_poof" (0.4 seconds):
   - Reverse of spawn, with upward particle puff

   "working" (2 second loop):
   - Rapid small squash/stretch (faster than breathe)
   - Small particles emit from front (work being done)

6. **Organization**
   - Each character in its own collection: "Char_Cairn", "Char_Lumen", etc.
   - Actions named: "Action_Walk", "Action_Idle", "Action_Spawn", etc.
   - All in one .blend file for easy linking

SAVE periodically via:
```python
bpy.ops.wm.save_as_mainfile(filepath="/Users/andreacrespo/CLAUDE/city101/output/kitchen_animation/assets/characters.blend")
```
Final save to the same path when done.

When done, write a summary to output/kitchen_animation/assets/character_manifest.txt
listing all character names, collection names, and available actions.

IMPORTANT: If shape keys or actions are tricky via MCP, prioritize having
the characters LOOK right (correct shapes, colors, eyes) over having
perfect animation rigs. Simple position keyframes can substitute for
shape key animations if needed. Do not get stuck.
</character-builder-prompt>

### Teammate C (Phase 1): "Exterior & Camera Rigs" → target: third (port 9878)

<exterior-builder-prompt>
You are building the exterior scene and reusable camera/lighting rigs.
Work in Blender instance "third" (target: "third" on every MCP call).

Read the full spec:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
Focus on exterior elements and visual style.

BUILD IN THIS ORDER:

1. **Camera rig** (reusable template)
   - Orthographic camera, 30° isometric angle
   - Ortho scale = 10 (wide enough to see full house)
   - Create a second camera "Cam_CloseUp" with ortho scale = 5
   - Parent both cameras to empties for easy animation

2. **Lighting rig**
   - Sun lamp, warm (~4500K), direction from upper-left
   - World background: very light warm gray (#F5F0EB)
   - Enable EEVEE
   - Enable Freestyle: line thickness 2px, black

3. **Exterior set**
   - Ground plane (large, #D4C5A9 sandy beige)
   - Main house footprint placeholder (12x8 box, low height — will be replaced with Phase 1 house)
   - Street in front (darker strip, #888888)
   - 2-3 empty buildings across street (simple box shapes, dark windows, for Video 5)
   - Garden area (green-tinted ground #8BC34A near house)
   - Mailbox (small box on stick)
   - Pneumatic tube stubs (thin cylinders between buildings, for Video 5)

4. **Render settings template**
   - Resolution: 960x540 (draft render — will upscale later if time)
   - Frame rate: 24fps
   - EEVEE with Freestyle
   - Color management: standard sRGB

5. **Organization**
   - Collections: "Exterior_Ground", "Exterior_Buildings", "Exterior_Street", "Camera_Rigs", "Lighting"
   - Name everything clearly

SAVE periodically via:
```python
bpy.ops.wm.save_as_mainfile(filepath="/Users/andreacrespo/CLAUDE/city101/output/kitchen_animation/assets/exterior_rigs.blend")
```

When done, write summary to output/kitchen_animation/assets/exterior_manifest.txt.
</exterior-builder-prompt>

---

## Phase 1 → Phase 2 Transition

When ALL Phase 1 teammates report completion:

1. **Verify assets exist** — check these files:
   - `output/kitchen_animation/assets/house_set.blend`
   - `output/kitchen_animation/assets/characters.blend`
   - `output/kitchen_animation/assets/exterior_rigs.blend`
   Read the manifest files to confirm what was built.

2. **Transfer assets between instances for Phase 2:**
   The house set is in "main", characters in "second", exterior in "third".
   Phase 2 videos need assets from multiple sources. Use file append:
   ```
   blender_execute_code(target="second", code="""
   import bpy
   # Append kitchen collections from house set
   filepath = "/Users/andreacrespo/CLAUDE/city101/output/kitchen_animation/assets/house_set.blend"
   with bpy.data.libraries.load(filepath, link=False) as (data_from, data_to):
       data_to.collections = [c for c in data_from.collections]
   for col in data_to.collections:
       if col is not None:
           bpy.context.scene.collection.children.link(col)
   print(f"Appended collections from house_set.blend")
   """)
   ```
   Repeat for each instance that needs assets from another.
   Alternatively, use `blender_transfer_geometry()` for targeted transfers.

3. **Clear Phase 1 work scenes if needed** — each video should start clean
   or build on the existing scene. The PM decides per-video.

4. If any Phase 1 teammate failed significantly, assess what's missing and
   decide whether to proceed or have another teammate rebuild it.

5. Update BUILD_LOG.md with Phase 1 results, then proceed to Phase 2.

---

## Phase 2: Video Animation (parallel, ~2-3 hours)

Spawn video teammates in priority order. Run up to 3 simultaneously
(one per Blender instance).

### Render Strategy (applies to ALL videos)

- **Draft resolution: 960x540** — use this for the overnight run.
- If all videos complete and there's time, re-render priority videos at 1920x1080.
- If EEVEE fails, try with Freestyle disabled first. If still failing, try Workbench renderer.
- Render as PNG sequence (not video file) — this way partial renders are still usable.

### Priority Batch 1 (spawn all 3 together):

**Teammate D: Video 1 "Moving In"** → target: main

<video1-prompt>
You are animating Video 1: "Moving In" — what happens when a Claude Code
session starts.

Read the full spec for visual style and storyboard:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
→ See VIDEO 1 in Part 4.

Work in Blender instance "main" (target: "main" on every MCP call).

SETUP:
1. The house set should already be built in this instance. If not, report
   the issue and stop.
2. Link/append the Cairn character from the character file.
3. Show: Kitchen (main floor), hallway/door, corkboard, recipe stand.
   Hide other rooms for now.

ANIMATE (24fps, ~20 seconds = ~480 frames):
- Frame 1-72 (0-3s): Empty kitchen. Isometric view. Hold.
- Frame 72-120 (3-5s): Door opens (rotate door object). Cairn spawn animation
  on doorstep. Pop into existence.
- Frame 120-216 (5-9s): Cairn walks into hallway. Stops at corkboard.
  Backpack opens (rotate backpack top face). Small scroll object rises,
  pauses, descends back. Backpack closes.
- Frame 216-264 (9-11s): Cairn moves to corkboard. Pauses (reading).
  Eyes shift left-right.
- Frame 264-336 (11-14s): Cairn walks to main counter. Opens recipe book
  (rotate book cover). Looks at order tickets.
- Frame 336-432 (14-18s): Cairn starts working animation at counter.
  Small particles from front (work being done).
- Frame 432-480 (18-20s): Camera slowly pulls back to show full house
  cross-section. All room labels fade in (text objects with animated
  visibility/opacity).

CAMERA: Start zoomed into kitchen level, slowly pull back at end.
Orthographic, isometric angle throughout.

TEXT OVERLAY: At frame 460+, add text object: "Every session begins here."
Place at bottom center of frame.

RENDER: Resolution 960x540 (draft). Output: output/kitchen_animation/renders/video_01/
PNG sequence. EEVEE, Freestyle ON (2px lines). If Freestyle causes errors, disable it.
Render the full sequence.

FALLBACK: If character linking fails, build a simple blob directly in
this scene (sphere + eyes + spark, Cairn colors). Don't let linking
issues stop the video.
</video1-prompt>

**Teammate E: Video 4 "The Brigade"** → target: second

<video4-prompt>
You are animating Video 4: "The Brigade de Cuisine" — how agent teams work.

Read the full spec for visual style and storyboard:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
→ See VIDEO 4 in Part 4.

Work in Blender instance "second" (target: "second" on every MCP call).

SETUP:
1. Build or link the kitchen set. If the house set is available from Phase 1,
   link it. If not, build a simplified kitchen (floor, walls, counter, a few
   stations — enough to stage the action).
2. Link/append characters: Cairn (coordinator) + 4 teammates (Analyst,
   Modeler, Visualizer, Knowledge Agent). If character files aren't
   available, build simplified blobs (sphere + eyes + accent color).

ANIMATE (24fps, ~30 seconds = ~720 frames):
- Frame 1-48 (0-2s): Cairn at the pass (elevated position, coordinator).
  Wearing coordinator look (white accent). Idle breathe.
- Frame 48-96 (2-4s): Order ticket drops from above (small rectangle,
  animated position Y from +3 to Cairn's position). Cairn catches it
  (eyes track it down).
- Frame 96-192 (4-8s): Cairn tears ticket — 4 smaller rectangles fly
  to 4 different stations:
  - Green piece → prep counter (Analyst spawns with pop)
  - Orange piece → near window/workshop (Modeler spawns)
  - Pink piece → plating station (Visualizer spawns)
  - Brown piece → pantry door (Knowledge Agent spawns)
  Each spawn: scale 0→1.1→1.0 bounce, particle ring.
- Frame 192-360 (8-15s): All 4 work simultaneously:
  - Analyst: squash/stretch at prep counter, particles flying
  - Modeler: arm extends toward workshop window
  - Visualizer: working at plating station
  - Knowledge Agent: walks into pantry, comes back with floating book icon
- Frame 360-432 (15-18s): Knowledge Agent walks toward Modeler. Small
  book icon floats between them. Modeler adjusts.
- Frame 432-528 (18-22s): Dishes (small cylinders) slide from each station
  toward the pass. Cairn inspects. One gets bounced back (small red X
  appears, dish slides back to Visualizer).
- Frame 528-624 (22-26s): Revised dish returns. Green checkmark. All dishes
  combine into one grand plate (objects merge at pass position).
- Frame 624-720 (26-30s): Grand plate slides through serving hatch.
  Camera follows it. Done.

CAMERA: Mostly static isometric showing full kitchen. Slight zoom-in
during the inspection moment (frames 432-528).

TEXT OVERLAY: Frame 700+: "One kitchen. One order. Five chefs. In parallel."

RENDER: Resolution 960x540 (draft). Output: output/kitchen_animation/renders/video_04/
PNG sequence. EEVEE, Freestyle ON (2px lines). If Freestyle causes errors, disable it.

FALLBACK: If you can't do 4 simultaneous character animations, reduce to
2 teammates (Analyst + Modeler) and simplify. The concept still reads.
</video4-prompt>

**Teammate F: Video 2 "Real vs TV Kitchen"** → target: third

<video2-prompt>
You are animating Video 2: "Real Kitchen vs TV Kitchen" — the difference
between Claude Code (CLI) and Claude Desktop.

Read the full spec:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
→ See VIDEO 2 in Part 4.

Work in Blender instance "third" (target: "third" on every MCP call).

SETUP:
1. Build or link the kitchen. You need: the main kitchen + a TV mounted
   on the wall showing a miniature kitchen inside it.
2. The TV: a flat rectangle on the wall (screen material with emission).
   Inside/on the TV surface: a tiny simplified kitchen scene (scaled down
   ~20%, rendered as a flat image or simplified geometry on a plane).
3. Characters: Cairn (full size, in real kitchen) + Lumen (small, gold,
   appears to be "inside" the TV — position behind the TV plane).

ANIMATE (24fps, ~25 seconds = ~600 frames):
- Frame 1-48 (0-2s): Split view established. Real kitchen left/center.
  TV on wall, right side. TV shows miniature kitchen (could be a still
  image or simplified geometry).
- Frame 48-192 (2-8s): Cairn walks in through real door. Touches counter
  (position moves to counter). Opens fridge (small box door rotates).
  Picks up knife (tool object parents to Cairn). Starts chopping.
- Frame 192-336 (8-14s): On the TV: Lumen appears (spawn pop, but small).
  Same actions but miniature and behind glass. When Lumen reaches toward
  the edge of the TV, a small "bonk" — Lumen bounces back slightly.
  Can't reach beyond the screen.
- Frame 336-432 (14-18s): Cairn opens a drawer (kitchen object).
  Lumen has no drawer — waves at screen. A copy of the file materializes
  in the TV kitchen (small rectangle appears with a sparkle).
- Frame 432-528 (18-22s): Both have plated dishes. Cairn's dish is on
  the real counter. Lumen's is inside the TV.
- Frame 528-600 (22-25s): Camera slowly zooms toward Cairn. The kitchen
  reflects in Cairn's eyes (or just the warm glow of the environment
  illuminates Cairn). Cairn is HERE.

TEXT OVERLAY:
- Frame 48: "In your kitchen" (near Cairn)
- Frame 192: "On your screen" (near TV/Lumen)
- Frame 560: "Same chef. Different kitchen."

RENDER: Resolution 960x540 (draft). Output: output/kitchen_animation/renders/video_02/
PNG sequence. EEVEE, Freestyle ON (2px lines). If Freestyle causes errors, disable it.

FALLBACK: If the TV-within-scene is too complex, simplify: just show
Cairn working in full kitchen, then cut to Lumen in a visibly smaller,
simpler, boxed-in kitchen (like a diorama). The contrast still reads.
</video2-prompt>

---

### Priority Batch 2 (spawn after Batch 1 completes, or as instances free up):

**Teammate G: Video 6 "Pantry Tour"** → first available instance

<video6-prompt>
You are animating Video 6: "The Pantry Tour" — how archibase works.

Read the full spec:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
→ See VIDEO 6 in Part 4.

Work in whichever Blender instance is assigned to you.

SETUP: Kitchen + Pantry room + Library (upstairs). Link Cairn character.

ANIMATE (24fps, ~30 seconds = ~720 frames):
- Frame 1-48 (0-2s): Cairn cooking in kitchen. Pauses. Needs something.
- Frame 48-96 (2-4s): Walks to pantry door. Opens it. Camera follows inside.
- Frame 96-432 (4-18s): Pantry tour. Camera pans across three walls:
  - Left: ingredient bins (L1). Cairn opens one, scoops exact amount.
  - Back: recipe card cabinet (L2). Cairn pulls a drawer, takes card.
  - Right: equipment rack (L3). Cairn takes a tool off the pegboard.
- Frame 432-480 (18-20s): Cairn walks back to kitchen with items.
- Frame 480-528 (20-22s): Cairn looks up. Needs more. Goes upstairs.
- Frame 528-672 (22-28s): Library. Pulls book from shelf. Reads at desk.
  Lightbox glows (image search). Takes notes.
- Frame 672-720 (28-30s): Back in kitchen. Starts cooking with precision.

TEXT: "Pantry for quick lookups. Library for deep research."

RENDER: Resolution 960x540 (draft). Output: output/kitchen_animation/renders/video_06/
PNG sequence. EEVEE, Freestyle ON (2px lines). If Freestyle causes errors, disable it.
</video6-prompt>

**Teammate H: Video 5 "Opening More Kitchens"** → second available instance

<video5-prompt>
You are animating Video 5: "Opening More Kitchens" — cloud VM scaling.

Read the full spec:
/Users/andreacrespo/CLAUDE/city101/prompts/[A04_ACTIVE]_kitchen_analogy_animations.md
→ See VIDEO 5 in Part 4.

SETUP: Need the house EXTERIOR + street + 2-3 other buildings.
Link Cairn, Meridian, Cadence characters.

ANIMATE (24fps, ~30 seconds = ~720 frames):
- Frame 1-72 (0-3s): Cairn's team working inside (seen through windows).
- Frame 72-192 (3-8s): Camera pulls back. House exterior. Street visible.
  Empty dark buildings across the road.
- Frame 192-264 (8-11s): One building lights up (window materials switch
  from dark to warm glow). Inside: kitchen materializes. Underground
  tunnel/pipe glows — shared pantry access.
- Frame 264-336 (11-14s): Meridian walks into that kitchen. Spawns team.
- Frame 336-408 (14-17s): Third building lights up. Cadence enters.
- Frame 408-528 (17-22s): All three kitchens visible, all cooking.
  Pneumatic tubes: small capsules shoot between buildings.
- Frame 528-648 (22-27s): Camera pulls back further. Street view.
  9 buildings. Most lit up.
- Frame 648-720 (27-30s): All dishes converge at integration kitchen.

TEXT: "Same recipes. Same pantry. Different kitchens. All at once."

RENDER: Resolution 960x540 (draft). Output: output/kitchen_animation/renders/video_05/
PNG sequence. EEVEE, Freestyle ON (2px lines). If Freestyle causes errors, disable it.
</video5-prompt>

---

### Priority Batch 3 (if time allows):

Spawn teammates for Videos 3, 7, 8, 9 using the storyboards from the
main spec file. Same pattern: link house + characters, animate, render.

These are lower priority. If Batch 1+2 complete and there's time, do V3
(subagents) next as it's the remaining core concept.

---

## Error Handling

You are running overnight without human supervision. Follow these rules:

1. **Blender MCP connection failure:** Wait 30 seconds, retry. If still
   failing after 3 retries, log the error and move to next teammate/task.

2. **Teammate reports failure:** Note what failed and why. If it's a
   blocking issue (e.g., can't create ANY geometry), skip that video.
   If it's partial (e.g., one prop missing), tell teammate to continue
   without it.

3. **File linking issues:** If teammates can't link house/character files
   from Phase 1, instruct them to build simplified versions directly.
   Every video prompt has a FALLBACK section for this.

4. **Rendering issues:** If EEVEE render fails, try reducing resolution
   to 1280x720. If Freestyle causes issues, disable it (outlines are
   nice-to-have, not critical).

5. **Never get stuck.** If something takes more than 10 minutes of
   retrying without progress, skip it and move on. Log what was skipped
   in output/kitchen_animation/BUILD_LOG.md.

---

## Progress Tracking

After each phase, write status to:
output/kitchen_animation/BUILD_LOG.md

Format:
```markdown
# Kitchen Animation Build Log

## Phase 1: Assets
- House Set: [DONE/FAILED/PARTIAL] — [details]
- Characters: [DONE/FAILED/PARTIAL] — [details]

## Phase 2: Videos
- Video 1 "Moving In": [DONE/FAILED/PARTIAL] — [frames rendered]
- Video 4 "Brigade": [DONE/FAILED/PARTIAL] — [frames rendered]
- Video 2 "CLI vs Desktop": [DONE/FAILED/PARTIAL] — [frames rendered]
- Video 6 "Pantry": [DONE/FAILED/PARTIAL] — [frames rendered]
- Video 5 "Cloud VMs": [DONE/FAILED/PARTIAL] — [frames rendered]

## Issues & Skipped Items
- [list anything that failed or was skipped]

## File Locations
- House set: [path]
- Characters: [path]
- Renders: [paths]
```

---

## Completion

When all priority videos are rendered (or all have been attempted), write
a final summary to the BUILD_LOG. Include:
- What was completed
- What needs manual touch-up
- Total render frame count
- Any recommendations for morning review

Then stop. Andrea will review in the morning.
