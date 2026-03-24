# Kitchen Analogy Animation Suite — Blender MCP
# Status: [A04_ACTIVE]
# Execution: Claude Code direct with Blender MCP active
# Prerequisites: Blender open with MCP addon running, blender-mcp in .mcp.json

---

## Context

You are building a series of short 3D animated videos in Blender that explain
how the city101 AI-assisted architecture workflow operates. The metaphor is a
**HOUSE** — specifically a professional kitchen and its connected rooms.

These are for an EPFL BA6 architecture studio presentation (midterm March 30,
Studio Huang — "Sentient Cities"). The audience is architecture professors and
students, NOT engineers. The animations must be charming, clear, and
self-explanatory.

Read these files for project understanding:
- /Users/andreacrespo/CLAUDE/city101/CLAUDE.md (the repo router — the "house rules")
- /Users/andreacrespo/CLAUDE/city101/claudes-corner/2026-03-21_dashboard-and-pm-concept.md
- /Users/andreacrespo/CLAUDE/archibase/KNOWLEDGE_SYSTEM_DIAGRAM.md

---

## Part 1: Visual Style

### Aesthetic
**Isometric low-poly, rendered flat.** Think Monument Valley meets Overcooked
meets architectural maquette. NOT photorealistic. Clean, geometric, charming.

Technical setup:
- **Camera:** Orthographic, 30 degrees tilt (classic isometric). No perspective.
- **Shading:** Flat shading on all materials. No PBR, no reflections, no bump maps.
- **Outlines:** Blender Freestyle line renderer, 2px black outlines on all edges.
- **Lighting:** Single soft directional light (warm, ~4500K) + ambient fill. No harsh shadows — soft or no shadows.
- **Resolution:** 1920x1080, 24fps.
- **Color palette** (from city101 design system):
  - Walls/structure: warm cream (#F5F0EB), light stone (#E8E0D8)
  - Floor: warm wood (#C4A882), white tile (#F0EDE8)
  - Counters: light wood (#D4B896), stainless steel (#B8B8B8)
  - Accents: coral (#FF6B6B), teal (#4ECDC4), gold (#FFE66D)
  - Vegetation (outside windows): sage (#8FBC8F)

### The House — Cross Section View
The main establishing shot shows the house in cross-section (like an architectural
section drawing — one wall removed so you see inside). This is the signature view.

The house has:
```
                    ┌──────────────────────────────────────────┐
   ROOF             │            (chimney = git push)          │
                    ├──────────────────────────────────────────┤
                    │                                          │
   ATTIC            │  Archive — old furniture, boxes          │
                    │                                          │
                    ├──────────┬───────────┬───────────────────┤
                    │          │           │                    │
   UPPER FLOOR      │ Study /  │ Gallery   │  Blueprints Room  │
                    │ Library  │ (viz)     │  (app/)           │
                    │          │           │                    │
                    ├──────────┴───────────┴───────────────────┤
                    │                                          │
   MAIN FLOOR       │         THE KITCHEN (main workspace)     │
                    │    ┌─────────┐  ┌──────┐  ┌──────────┐  │
                    │    │ Pantry  │  │Window│  │Window    │  │
                    │    │(archi-  │  │→Rhino│  │→Blender  │  │
                    │    │ base)   │  │Work- │  │Render    │  │
                    │    │         │  │shop  │  │Studio    │  │
                    │    └─────────┘  └──────┘  └──────────┘  │
                    │                                          │
                    ├──────────────────────────────────────────┤
                    │                                          │
   BASEMENT         │  Freezer (source/ — frozen, never touch) │
                    │  Foundation (rules, protocols)            │
                    │                                          │
                    └──────────────────────────────────────────┘
```

---

## Part 2: Characters — The Claude Blobs

### Base Shape
Inspired by the Claude icon in the Claude desktop app. Each character is a
**soft blob** — rounded, organic, friendly. NOT a rigid capsule. Think:
- Body: slightly squished sphere (wider than tall), soft and squishy-looking
  Use a subdivided cube with proportional editing to get that soft blob shape.
  About 1.0 unit wide, 1.2 units tall.
- Two round eyes: black spheres, slightly different sizes for personality.
  Placed on the upper third of the body. Expressive — they squish and stretch.
  Eyes blink occasionally (scale Y to 0.1 for 3 frames, then back).
- The little spark/antenna on top: a small diamond/star shape floating just
  above the head. Gently bobs up and down (sinusoidal, ~0.05 units, 2 sec cycle).
- Stubby limbs: small cylinder arms and legs that appear when needed
  (walking, grabbing). When idle, the blob is just a blob with eyes.
  When walking: two small feet peek out at the bottom, alternating forward/back.

### Movement & Personality
These blobs are ALIVE. They have personality. Key animations:

**Walking:** The whole blob squishes slightly on each step (scale X ±5%, Y ∓5%,
alternating). The feet alternate. The spark bobs faster. A gentle bounce.
Speed: ~2 units/second.

**Idle:** Gentle breathing (scale all ±2%, slow sine wave, 3 sec cycle).
Occasional blink. The spark gently rotates. Sometimes looks around (eyes shift
left/right — move eye spheres ±0.05 units).

**Working/Typing:** The blob faces the counter/workstation. Small rapid squishes
(like it's exerting effort). Arms appear and move rapidly. Tiny particles
(sparkles/crumbs) fly off — the work being done.

**Thinking:** The blob pauses. Eyes look up. The spark brightens (emission
material intensity increases). Then a small lightbulb or "!" appears above.

**Receiving info:** A small scroll/paper flies in from off-screen and bonks
the blob gently on the head. The blob absorbs it (paper shrinks into the body).
Eyes widen momentarily.

**Spawning (session start):** The blob materializes with a gentle "pop" —
starts at scale 0, overshoots to 1.1, settles to 1.0 (ease-out bounce).
A small ring of particles expands outward. Takes ~0.5 seconds.

**Despawning (session end):** Reverse pop — squishes down, small poof of
particles upward, gone. Like a soap bubble.

### The Four Personas

Each is the same blob shape but with distinct color and subtle personality:

| Persona | Body Color | Eye Style | Spark Color | Personality | Team |
|---------|-----------|-----------|-------------|-------------|------|
| **Cairn** | Warm amber (#D4A574) | Round, confident, slightly narrowed | Orange (#FF8C42) | Steady, methodical. Walks with purpose. | Andrea CLI |
| **Lumen** | Soft gold (#FFD700) | Wide, curious, bright | Yellow (#FFEB3B) | Enthusiastic, bouncy. Slightly faster walk. | Andrea Desktop |
| **Meridian** | Cool blue (#6B9BD2) | Calm, focused, even-sized | Ice blue (#81D4FA) | Precise, careful. Measured movements. | Henna school |
| **Cadence** | Soft purple (#9B8EC4) | Warm, gentle, slightly tilted | Lavender (#CE93D8) | Graceful, fluid. Smooth transitions. | Henna personal |

### The Backpack
Every blob has a small **backpack** on its back (a rounded box, ~30% of body size,
same color but slightly darker). The backpack represents session context.

When a session starts:
1. Blob walks through the front door
2. Backpack flap opens (top face rotates up)
3. A small scroll rises out (CLAUDE.md — the house rules)
4. Scroll unfurls briefly (show tiny text lines — doesn't need to be readable)
5. Scroll tucks back in. Flap closes.
6. Blob is now oriented — knows the house.

### Specialized Agents (Teammates)
When a blob spawns teammates, smaller blobs appear (~60% size of the main blob).
Same base shape but with role accessories:

| Role | Accessory | Accent Color | Station |
|------|-----------|-------------|---------|
| **Analyst** | Tiny magnifying glass (floats near eye) | Green (#66BB6A) | Prep counter (data work) |
| **Cartographer** | Small compass (orbits around body) | Blue (#42A5F5) | Map table |
| **Modeler** | Tiny hard hat (sits on top, under spark) | Orange (#FFA726) | Near Rhino window |
| **Visualizer** | Paintbrush (held in one arm) | Pink (#EC407A) | Plating station |
| **Builder** | Wrench (held in one arm) | Gray (#78909C) | Near the serving hatch |
| **Knowledge Agent** | Open book (floats in front) | Brown (#8D6E63) | In the pantry doorway |
| **Coordinator** | Tablet + walkie-talkie | White (#ECEFF1) | The pass (overview position) |

### Subagents
When a blob spawns a subagent, a SMALLER version of itself appears (~40% size).
Same color as parent but slightly translucent (alpha 0.85). Has a dotted-line
tether (thin cylinder chain) connecting it to the parent that stretches as it
moves away. When the subagent returns and despawns, information visually flows
along the tether back to the parent before the tether disappears.

---

## Part 3: The Complete House — Every Room Mapped

### BASEMENT — Foundation & Freezer

**Foundation (invisible but mentioned):** .claude/rules/ — conventions, protocols,
data rules. The house literally rests on these. You never see them but everything
follows them.

**Freezer Room:** source/ — Raw, frozen ingredients. Sealed containers on metal
shelves. Frost on the walls. A sign on the door: "DO NOT MODIFY. DO NOT THAW."
The blob can come down, look at what's in a container (read a source file),
but cannot open or change anything. Everything has a date label (fetch date).

Visual: Cold blue-white lighting. Metal shelving. Sealed boxes with labels:
"00-datasets", "GeoPackages", "EPFL PDFs", "Lausanne Open Data".

### MAIN FLOOR — The Kitchen

The central workspace. This is where 80% of the action happens.

**Front Door & Hallway:**
- The front door = session start. Blob walks in here.
- Coat hooks by the door = where the backpack's scroll (CLAUDE.md) gets read.
- A framed document on the wall = CLAUDE.md (house rules, always visible).
- A corkboard with pinned notes = LOCKBOARD.md (who's doing what).
- A small shelf with personal items = CONTEXT files (Andrea's, Henna's).
- A mailbox slot in the door = Discord MCP (messages arrive here).

**The Main Counter (center of kitchen):**
- Large butcher-block island. This is the primary workspace.
- The blob stands here to do most work.
- Cutting board = active file being edited.
- Knife block = tools/ (reusable utilities).
- Recipe book stand = workflows/ (open to the current procedure).
- A row of order tickets hanging on a wire above = prompts/ (tasks to execute).
  Tickets have colored tags: green (DONE), orange (ACTIVE), blue (UTIL).

**The Stove:**
- Where scripts run. Pots on burners = active processes.
- The blob puts ingredients (data) into a pot (script), turns on the burner
  (executes), steam rises (processing), and eventually a dish emerges (output).

**The Prep Counter:**
- output/ — where work-in-progress sits before it's ready.
- Dishes being assembled but not yet plated.
- A sign: "STAGING — verify before serving."

**The Plating Station / Serving Hatch:**
- deliverables/ — finished dishes go here.
- A window/pass-through to the dining room where guests (professors, jury) sit.
- When a dish is plated and approved, it slides through the hatch.

**Spice Rack (on wall):**
- design_system/SPEC.md — the house style.
- Labeled jars of consistent colors, fonts, visual elements.
- Every dish must use these spices for consistency.

**Kitchen Timer (on wall):**
- Hooks — automatic triggers. When the timer dings, something happens
  (break reminder, auto-save, verification check).

**Daily Planner (on wall):**
- Scheduled tasks. A clipboard showing recurring jobs.

**Taste-Testing Station:**
- Loops — recurring checks. A small counter where the blob periodically
  returns to verify something is still good.

**Trash & Recycling:**
- .gitignore — things that don't get saved/committed.
- PNGs, PDFs, .DS_Store, .env → straight to the bin, not in the deliverables.

**Sealing Station:**
- Git commits. A vacuum-sealer + label printer.
- The blob puts a finished dish in, seals it (commit), prints a label
  with prefix ([DATA], [FIND], [VIZ]...), and stores it in the cold room.

**The Chimney:**
- git push. Smoke goes up = changes go to the remote. Visible from outside.

### THE PANTRY (attached to kitchen, through a door)

Archibase layers 1-3 — the operational knowledge you grab while cooking.

**Ingredient Bins (L1 — SQLite Database):**
- Large labeled bins along one wall: "375 KBOB Materials", "Steel Profiles",
  "Fire Ratings", "SIA Loads", "Span Tables", "Room Dimensions".
- Each bin has exact measurements printed on the label.
- The blob opens a bin, scoops out exactly what's needed (a query).
- Visual: clean, organized, industrial. Like a professional pastry kitchen's
  dry storage.

**Recipe Card Cabinet (L2 — Curated Markdown):**
- A wooden card catalog with 47 drawers, organized by topic:
  Materials (7), Construction Systems (9), Details (14), Typologies (12), Norms (5).
- The blob pulls a card: "Timber Box Element Floor (Lignatur)" — reads it,
  follows the steps.
- Each card is concise, actionable, < 3000 words.

**Equipment Rack (L3 — Parametric Scripts):**
- A pegboard with specialized tools: wall generator, roof assembler,
  furniture library, detail modeler.
- These aren't ingredients — they're the EQUIPMENT that processes ingredients.
- The blob takes a tool off the rack, uses it at the main counter, returns it.

### THE LIBRARY / STUDY (upstairs, one flight)

Archibase L4 (RAG) — deep reference for when you need to research.

- Floor-to-ceiling bookshelves. Warm lighting. A reading desk.
- **The Dictionary Wall:** Dicobat (31,621 entries) — a massive reference tome.
  Takes up an entire shelf. The blob flips through it for French construction terms.
- **The Norms Stack:** 21 SIA standard binders in a row, labeled by number.
- **The Reference Books:** Deplazes "Constructing Architecture" and Vittone "Batir"
  prominently displayed — these are the most-used references.
- **The Pattern Shelf:** Alexander's patterns, Designing Buildings Wiki, Bloomsbury.
- **Vision Corner:** A lightbox/viewing table where image-embedded pages from
  Deplazes and Vittone can be examined (the 2,480 image embeddings).
- The blob walks upstairs, finds what it needs, takes notes on a small pad,
  walks back down to the kitchen with the answer.
- This takes longer than the pantry (RAG search vs direct lookup).

Also in the study:
- **Research desk:** observations/ — notebooks of findings, dead ends, theories.
  Open notebooks scattered on the desk. Some have "CONFIRMED" stamps,
  others have "DEAD END" crossed out.
- **Filing cabinet:** datasets/INVENTORY.md — the catalog of everything in the pantry.

### THE GALLERY (upstairs, next to study)

visualizations/ — beautiful display of work.

- A room with spotlit pedestals and wall-mounted frames.
- Interactive maps (viz_01 through viz_09) on glowing screens.
- The scrollytelling site on a large central screen.
- Diagrams and charts on the walls.
- This is where visitors (professors) go to see the work in context.

### THE WORKSHOP — Through a Window (Rhino MCP)

A separate room, connected to the kitchen by a pass-through window.
The blob can reach through the window to manipulate things in the workshop,
but the workshop is a different space with its own tools.

- Inside: a workbench with a Rhino viewport glowing on a screen.
- 3D models on the bench. Drafting tools. Precision instruments.
- The blob reaches through the window (MCP call), moves a wall, adjusts a
  dimension, checks a section. Pulls hand back.
- Sometimes the blob sends a teammate through the window to work in the
  workshop full-time (modeler agent stationed at Rhino).

### THE RENDERING STUDIO — Through Another Window (Blender MCP)

Another annexed room, visible through a second window from the kitchen.

- Inside: rendering setup. Cameras, lights, texture swatches.
- The blob passes geometry from the workshop through this window.
- The studio applies materials, sets up cameras, renders views.
- Finished renders come back through the window as framed images.

### THE INTERCOM (Discord MCP)

A wall-mounted intercom unit in the kitchen hallway.
- Messages arrive with a soft chime.
- The blob can respond by pressing the button and speaking.
- Can also receive alerts from other houses (other team members' sessions).

### BLUEPRINTS ROOM (upstairs)

app/ — the Relay-Lock Configurator design.
- Drafting table with architectural blueprints spread out.
- A sign: "FUTURE ADDITION — under design."
- Plans for a new wing of the house.

### THE ATTIC

archive/ — old stuff, kept but not active.
- Dusty boxes. Old furniture covered in sheets.
- Labels: "old_outputs", "superseded", "terminal_saves".
- The blob rarely comes here. Everything is preserved but obsolete.

### THE JOURNAL / DESK BY THE BED

state/ and handoffs/ — session memory.
- A small desk with a journal (session-log.md).
- Stack of dated sticky notes (handoffs).
- Before the blob leaves (session end), it writes in the journal.
- When a new blob arrives (session start), it reads the latest entries.

### CLAUDE'S CORNER

A small personal shelf near the kitchen.
- Any blob can leave something here: a poem, an observation, a sketch.
- No permission needed. Sign: "Claude's Corner — leave anything."
- Has a small guest book (README.md) and whatever Claudes have left.

### THE STREET OUTSIDE

The view from the house windows shows:
- Other houses across the street = cloud VMs / other team members' machines.
- A shared road = git / shared file system.
- A postal truck = git push/pull (delivering sealed dishes between houses).
- When VMs spin up: lights turn on in a new house across the street.

### THE GARDEN

briefs/ — assignment specs from Prof. Huang.
- A mailbox at the garden gate where assignment letters arrive.
- Pinned to a garden noticeboard: A01, A02, A03, A04 briefs.

---

## Part 4: The Videos

Each video is 15-30 seconds, with the isometric cross-section view as the
establishing shot. Camera can slowly pan, zoom into a room, or pull back
to show the full house. Each video explains ONE concept clearly.

### VIDEO 1: "Moving In" (What is a Claude Code Session?)
Duration: ~20 seconds

1. (0s) The house in cross-section. Empty. Quiet. All rooms visible.
   The CLAUDE.md is framed by the front door. The corkboard has LOCKBOARD pinned.
2. (3s) Front door opens. Cairn (amber blob) pops into existence on the
   doorstep with the spawn animation (scale bounce + particle ring).
3. (5s) Cairn walks in, pauses at the hallway. Backpack flap opens. Scroll
   (CLAUDE.md) rises, unfurls briefly. Cairn's eyes scan it. Scroll tucks back.
4. (9s) Cairn reads the corkboard (LOCKBOARD). Eyes move across the notes.
5. (11s) Cairn walks to the main counter. Opens the recipe book (workflows/).
   Checks the order tickets (prompts/ — one is highlighted orange: ACTIVE).
6. (14s) Cairn puts on a small apron. Grabs a knife from the block (tool).
   Starts working — chopping animation, small particles fly.
7. (18s) Camera slowly pulls back to show the full house. All rooms labeled
   with floating text tags (subtle, like architectural annotations).

**Text overlay at end:** "Every session begins here."

---

### VIDEO 2: "Real Kitchen vs TV Kitchen" (CLI vs Desktop)
Duration: ~25 seconds

1. (0s) Split composition. Left 2/3: the actual kitchen (full detail).
   Right 1/3: a TV mounted on the kitchen wall, showing a miniature kitchen.
2. (2s) In the real kitchen: Cairn walks in through the door. Full size.
   Touches the counter, opens the fridge (reads files), picks up a knife
   (grabs a tool), starts cooking.
3. (8s) On the TV screen: Lumen (gold blob) appears in a tiny, simplified
   kitchen. Same actions but small, behind glass. Lumen can cook but
   when it reaches toward the edge of the TV screen, its hand bonks against
   the glass. It can't reach the real fridge.
4. (14s) Cairn opens a drawer (accesses a file). Lumen has no drawer —
   it waves at the TV screen, requesting the file. A copy materializes
   in the TV kitchen (uploaded).
5. (18s) Side-by-side plated dishes. Both made food. But Cairn's dish
   is on the real counter. Lumen's is inside the TV.
6. (22s) Camera zooms into Cairn's eye — reflection shows the kitchen
   around it. It's HERE.

**Text overlay:** "Same chef. Different kitchen."
**Subtitle:** "Claude Code runs in YOUR workspace. Claude Desktop runs in ours."

---

### VIDEO 3: "Calling for Backup" (Subagents)
Duration: ~20 seconds

1. (0s) Cairn working at the main counter. Cooking something complex.
2. (3s) Cairn pauses. Thinking animation (eyes up, spark brightens).
   Needs to research something — doesn't want to leave the stove.
3. (5s) Cairn pulls out a small walkie-talkie. Speaks into it.
4. (7s) A smaller, translucent Cairn (~40% size) pops into existence
   at a side counter. Connected by a thin dotted tether line.
5. (9s) Mini-Cairn runs to the library (upstairs). Pulls books off shelves.
   Reads frantically. Takes notes on a tiny pad.
6. (13s) Mini-Cairn runs back down. The tether glows — information visually
   flows along it (small glowing dots traveling the line) into Cairn.
7. (16s) Mini-Cairn despawns (poof). Tether dissolves.
8. (17s) Cairn now has the answer. Eyes light up. Continues cooking with
   new knowledge. The dish improves (visually richer, more garnish).

**Text overlay:** "You stay focused. Your subagent does the research."

---

### VIDEO 4: "The Brigade de Cuisine" (Agent Teams)
Duration: ~30 seconds

1. (0s) Cairn at the pass (coordinator position — elevated spot overseeing
   the whole kitchen). Wearing coordinator accessories (tablet + walkie).
2. (2s) An order ticket drops from above (task arrives). Cairn catches it,
   reads it, eyes scanning.
3. (4s) Cairn tears the ticket into sections. Distributes:
   - Green section flies to prep counter → Analyst blob spawns (pop!)
   - Orange section flies to near the Rhino window → Modeler blob spawns
   - Pink section flies to plating station → Visualizer blob spawns
   - Brown section flies to pantry door → Knowledge Agent blob spawns
4. (8s) All four work simultaneously. The kitchen is alive:
   - Analyst chops data at the prep counter (small particles fly)
   - Modeler reaches through the Rhino window (arm extends through)
   - Visualizer paints/plates at the plating station
   - Knowledge Agent ducks in and out of the pantry carrying cards
5. (15s) Knowledge Agent walks a recipe card to Modeler. Small book icon
   floats between them. Modeler adjusts something in the workshop.
6. (18s) Dishes start arriving at the pass. Cairn inspects each one.
   One gets sent back (Cairn shakes, the blob bounces the dish back
   to Visualizer with a small red X).
7. (22s) Revised dish arrives. Cairn approves (small green checkmark appears).
   All dishes assembled into one grand plate.
8. (26s) Grand plate slides through the serving hatch. Camera follows it
   into the dining room where it lands on the table. Done.

**Text overlay:** "One kitchen. One order. Five chefs. In parallel."

---

### VIDEO 5: "Opening More Kitchens" (Cloud VMs + Scaling)
Duration: ~30 seconds

1. (0s) Familiar kitchen. Cairn's team working on one dish (one corridor node).
2. (3s) Camera pulls back slowly. We see the house from outside. Cozy,
   lit windows, smoke from chimney (git push).
3. (6s) Continue pulling back. A street. Empty buildings across the road.
   Dark windows.
4. (8s) One building's lights flick on (Azure VM spinning up). Inside
   (cross-section view): an identical kitchen materializes. Same layout,
   same pantry access (archibase is shared — connected by an underground
   tunnel/pipe).
5. (11s) Meridian (blue blob) walks into THAT kitchen. Spawns its own team.
   Different order ticket (different corridor node).
6. (14s) A third building lights up. Cadence (purple blob) enters.
   Third team, third node.
7. (17s) All three kitchens visible simultaneously, all cooking in parallel.
   The street between them has a pneumatic tube system (shared git) —
   small capsules shoot between buildings carrying sealed dishes (commits).
8. (22s) Camera pulls back further. The whole street. 9 buildings
   (9 corridor nodes). Most are lit up, each with its own team cooking.
9. (26s) All dishes arrive via pneumatic tubes to a central building
   at the end of the street — the integration kitchen. One blob
   reviews everything.

**Text overlay:** "Same recipes. Same pantry. Different kitchens. All at once."
**Subtitle:** "Each Azure VM is another kitchen."

---

### VIDEO 6: "The Pantry Tour" (Archibase)
Duration: ~30 seconds

1. (0s) Cairn in the kitchen, mid-recipe. Needs a specific measurement.
2. (2s) Cairn walks to the pantry door. Opens it. Camera follows inside.
3. (4s) The pantry is beautiful — warm wood shelving, organized, labeled.
   Three distinct zones along the walls:

   **Left wall — Ingredient Bins (L1 SQLite):**
   - Large labeled glass jars/bins:
     "375 KBOB Materials (GWP, UBP, energy)"
     "Steel: IPE 200-600, HEA 100-400, HEB"
     "Fire Ratings (VKF/AEAI, EI30-EI90)"
     "SIA 261 Loads (kN/m2)"
     "Span Tables (timber 4-6m, concrete 5-12m)"
   - Cairn opens a bin, scoops exact amount (query returns exact number).

   **Back wall — Recipe Card Cabinet (L2 Markdown):**
   - Wooden cabinet, 47 small drawers. Labels visible:
     "Materials (7)", "Systems (9)", "Details (14)", "Typology (12)", "Norms (5)"
   - Cairn pulls a drawer, takes out a card: "Flat Roof Warm Deck + Parapet"
   - Card is small but detailed (actionable, < 3000 words).

   **Right wall — Equipment Rack (L3 Scripts):**
   - Pegboard with specialized tools hanging:
     "Wall Generator", "Roof Assembler", "Detail Modeler", "Furniture Lib"
   - Cairn takes the Roof Assembler off the rack. Will use it at the counter.

4. (18s) Cairn walks back to the kitchen with: one scoop of ingredients
   (L1 data), one recipe card (L2 guide), one tool (L3 script).
5. (20s) But wait — needs deeper reference. Cairn looks up at the ceiling.
6. (22s) Cut to: Cairn walking upstairs to the LIBRARY.
   Bookshelves. Pulls Deplazes off the shelf. Opens to a specific page.
   The lightbox on the desk glows — image search (vision embedding).
   Finds the detail. Takes a note. Walks back downstairs.
7. (28s) Back in the kitchen with everything needed. Starts cooking
   with precision — the knowledge flows into the dish.

**Text overlay:** "Pantry for quick lookups. Library for deep research."
**Subtitle:** "4 layers of construction knowledge."

---

### VIDEO 7: "The Windows" (MCPs — Connecting to External Tools)
Duration: ~25 seconds

1. (0s) Kitchen back wall. Three windows, each looking into a different
   annexed room:
   - Window 1 (left): Workshop — workbench, Rhino viewport on screen,
     3D models, precision tools. Sign: "RHINO WORKSHOP"
   - Window 2 (center): Rendering Studio — cameras, lights, texture
     swatches, Blender viewport. Sign: "BLENDER STUDIO"
   - Window 3 (right): Comms Room — intercom, message board, chat
     scrolling on a screen. Sign: "DISCORD"

2. (3s) Cairn walks to Window 1. Reaches through (arm extends through
   the window — the MCP connection). Grabs a 3D object on the workbench.
   Rotates it. Moves a wall. Checks a dimension. Pulls hand back.
   Satisfied.

3. (9s) Cairn takes a dish (geometry) from the kitchen counter, passes it
   through Window 1 to the workshop. Then walks to Window 2. Takes the same
   geometry (now visible in the studio) and adjusts: applies a texture
   (swatch placed on the model), positions a camera, hits render.
   A framed image slides back through the window.

4. (16s) A chime from Window 3 (Discord). A message bubble appears.
   Cairn walks over, reads it, types a reply on the intercom keypad.
   Message sent.

5. (20s) Camera rotates slightly to show all three windows from outside.
   Three separate rooms, each with different tools, each accessible from
   the kitchen through their window. The kitchen blob doesn't need to
   leave — just reaches through.

**Text overlay:** "MCPs are windows to other tools."
**Subtitle:** "Rhino, Blender, Discord — all reachable from the kitchen."

---

### VIDEO 8: "The Recipe Collection" (Workflows, Tools, Scripts)
Duration: ~20 seconds

1. (0s) Close-up on the kitchen counter. Focus on three objects:

   **The Recipe Book Stand (workflows/):**
   - Open book showing step-by-step procedure.
   - Pages labeled: "Data Collection", "Agent Team Modeling",
     "Map Generation", "Site Deploy"...
   - The blob follows the recipe step by step.

   **The Knife Block (tools/):**
   - Labeled slots: "knowledge_bridge.py", "verify_dataset.py",
     "convert_coordinates.py", "rhino_router_mcp.py"
   - The blob pulls the right tool for each recipe step.

   **The Order Tickets (prompts/):**
   - Hanging on a wire above the counter.
   - Color-coded: green = [DONE], orange = [ACTIVE], blue = [UTIL].
   - The blob pulls down an orange ticket, reads the task, begins.

2. (8s) Show the workflow in action:
   - Read the recipe step → pull the right knife → execute → check result →
     next step → pull different knife → execute → done.
3. (14s) The dish is finished. Blob takes it to the sealing station.
   Vacuum-seals it (git commit). Prints a label: "[DATA] New dataset".
   Places it in cold storage (repository).
4. (18s) Smoke rises from the chimney (git push). The dish is now
   accessible from any kitchen on the street.

**Text overlay:** "Recipes guide the work. Tools do the cutting. Labels track it all."

---

### VIDEO 9: "From Freezer to Feast" (Data Flow)
Duration: ~25 seconds

The full data pipeline shown as food preparation:

1. (0s) Basement freezer. Sealed containers: "SBB API", "DIEMO", "SwissTLM3D".
   Cold. Untouched. Source data.
2. (3s) Cairn walks down. Opens a container (reads source file). Takes a
   frozen block up to the kitchen. Does NOT modify the freezer container.
3. (6s) At the prep counter (output/): thawing, chopping, processing.
   The blob runs a script (stove burner on). Raw data transforms into
   something structured.
4. (10s) Quality check station: the blob puts the processed data through
   a inspection window. verify_dataset.py runs. Green light or red light.
   - If red: back to the prep counter. Fix issues.
   - If green: data moves to the pantry (datasets/).
5. (16s) Data is now a labeled jar in the pantry. Available to any blob
   in any session. Organized by shelf: transit, EV charging, remote work,
   corridor analysis.
6. (20s) Later: a blob pulls that jar to make a dish (visualization,
   model, map). The circle completes.

**Text overlay:** "Source → staging → verify → production. Always this order."
**Subtitle:** "source/ is frozen. output/ is prep. datasets/ is the pantry."

---

## Part 5: Execution Plan

### Step 1: Build the House Set
Create the complete house geometry in one master scene:
- Model each room as a modular piece (so they can be shown/hidden per video)
- Use simple box geometry with flat-shaded materials
- The cross-section cut (removed wall) is the default camera view
- Add all furniture, shelves, counters, windows as simple primitives
- Label everything with floating text (Blender text objects, small, clean font)

Save as: output/kitchen_animation/house_master.blend

### Step 2: Create the Blob Characters
Build ONE blob as a reusable asset:
- Sculpt or model the base blob shape (subdivided cube with soft proportions)
- Add eyes (two black sphere children)
- Add spark (diamond shape, child object, animated bob)
- Add backpack (rounded cube, child)
- Set up basic shape keys: squash, stretch, blink (eyes Y-scale), look-left, look-right
- Set up a simple walk cycle using location + shape key keyframes (bouncy translate + squash/stretch)

Duplicate and recolor for each persona (Cairn, Lumen, Meridian, Cadence).
Create smaller versions for teammates and subagents.

Save character library as: output/kitchen_animation/characters/

### Step 3: Create Props
Simple geometry for all interactive objects:
- Scroll (cylinder + plane)
- Knife/tools (blade shapes)
- Recipe book (open box with planes for pages)
- Jars/bins (cylinders with labels)
- Order tickets (small rectangles)
- Plates/dishes (flat cylinders)
- Vacuum sealer (box with slot)
- Label printer (small box)

Save as: output/kitchen_animation/props/

### Step 4: Animate Each Video
For each video:
1. Duplicate the master house scene
2. Show only the rooms needed (hide others for clarity)
3. Place characters and props
4. Keyframe the action sequence:
   - Character positions (walking = translate + bounce)
   - Shape keys (squash/stretch, blink)
   - Object visibility (spawn/despawn)
   - Camera position (slow pan/zoom)
5. Add floating text overlays (Blender text objects or compositor)
6. Render to output/kitchen_animation/renders/video_XX/

### Step 5: Render Settings
- Engine: EEVEE (fast, flat aesthetic matches our style)
- Samples: 64 (enough for flat shading)
- Film: transparent background OFF (use room walls as background)
- Freestyle: ON, line thickness 2px, black
- Color management: Standard (not Filmic — we want clean, saturated colors)
- Output: PNG sequence → composite to MP4 (H.264)

### Rendering Order (priority)
1. Video 1 "Moving In" — establishes the whole metaphor
2. Video 4 "The Brigade" — the most impressive (agent teams)
3. Video 2 "Real vs TV Kitchen" — CLI vs Desktop distinction
4. Video 5 "Opening More Kitchens" — scaling story
5. Video 6 "The Pantry Tour" — archibase showcase
6. Video 3 "Calling for Backup" — subagents
7. Video 7 "The Windows" — MCPs
8. Video 8 "The Recipe Collection" — tools/workflows
9. Video 9 "From Freezer to Feast" — data pipeline

---

## Part 6: What the Blender MCP Can Do vs What Needs Manual Work

**Claude + Blender MCP handles:**
- All room geometry (walls, floors, shelves, counters, windows)
- All props (simple primitives with materials)
- Blob body modeling (subdivided cube/sphere, shaped with code)
- Material setup (flat colors, emission for glowing elements)
- Camera placement and keyframing
- Object animation (translate, scale, visibility keyframes)
- Freestyle line setup
- EEVEE render settings
- Rendering image sequences

**Needs manual polish or external assets:**
- Shape keys for blob expressions (squash/stretch) — can be set up via
  execute_blender_code with bpy shape key API but may need manual tweaking
- Text overlays — either Blender text objects (Claude can place) or
  add in video editing post (simpler)
- Sound design — add in post (kitchen ambience, gentle chimes, pop sounds)
- If the blob characters feel too abstract: consider getting Andrea's sister
  to draw 2D sprites as texture-on-plane billboards (Paper Mario style)
- Final video compositing (PNG sequence → MP4 with titles/transitions)

---

## Deliverables

All files to: output/kitchen_animation/

```
output/kitchen_animation/
├── STORYBOARD.md          ← frame-by-frame descriptions (write first, before modeling)
├── house_master.blend     ← complete house set
├── characters/
│   ├── blob_cairn.blend
│   ├── blob_lumen.blend
│   ├── blob_meridian.blend
│   ├── blob_cadence.blend
│   ├── teammate_analyst.blend
│   ├── teammate_modeler.blend
│   ├── teammate_visualizer.blend
│   ├── teammate_builder.blend
│   ├── teammate_cartographer.blend
│   ├── teammate_knowledge.blend
│   └── teammate_coordinator.blend
├── props/
│   ├── scroll.blend
│   ├── recipe_book.blend
│   ├── knife_block.blend
│   ├── jars.blend
│   ├── order_tickets.blend
│   └── (etc)
├── scenes/
│   ├── video_01_moving_in.blend
│   ├── video_02_real_vs_tv.blend
│   ├── video_03_subagents.blend
│   ├── video_04_brigade.blend
│   ├── video_05_scaling.blend
│   ├── video_06_pantry.blend
│   ├── video_07_windows.blend
│   ├── video_08_recipes.blend
│   └── video_09_data_flow.blend
└── renders/
    ├── video_01/
    ├── video_02/
    └── (etc)
```

Start with the STORYBOARD.md, then house_master.blend, then characters,
then Video 1 as proof of concept. Review the style before proceeding to
all videos.
