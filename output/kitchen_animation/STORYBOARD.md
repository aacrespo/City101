# The Kitchen — Animation Storyboard
**Locked: 2026-03-27**
**Status: DRAFT v2 — full flow revised with Andrea**

---

## Before the animation

The presentation has already explained the écluse concept, the software architecture, and ends with:
> "So we decided to be roommates with Henna. The repository is our shared apartment."

The repo = the apartment. The kitchen = the workspace. Animation picks up from there.

---

## Scene 1: "Entering the Kitchen"

### Setting
- An empty kitchen. The room exists but it's dim, bare, unused.
- Door on the left (entry). Main kitchen in center. Pass on the right.

### Sequence

**1a — Empty kitchen, grey character appears**
- Kitchen visible but empty/dim.
- Small Claude character walks toward the door. **GREY — no color, no context.** Blank agent.

**1b — The entryway: picking up the scrolls**
- Character enters through the kitchen door.
- Just inside: a small shelf with two scrolls waiting.
- Picks up **Scroll 1: CLAUDE.md** (gold, compass/map icon)
- Picks up **Scroll 2: .claude/** (teal, gear/blueprint icon)

**1c — Opening the maps (Minecraft moment)**
- Opens Scroll 1 → expands to fill view.
- **CLAUDE.md = THE MAP**: Parchment-style treasure map of the repo. "Datasets are here," "tools are here," "observations are here." Briefing on WHERE to find things. Warm, hand-drawn, organic.
- Brief pause. Map folds back.

- Opens Scroll 2 → expands.
- **.claude/ = THE BLUEPRINT**: Technical drawing of the kitchen. Every tool, machine, pipe labeled. Conventions, protocols, safety rules. HOW the kitchen works. Cool, precise, mechanical.
- Brief pause. Blueprint folds back.

**1d — Scrolls go in backpack, color appears**
- Both scrolls slot into backpack. Backpack grows (empty → small).
- **Grey washes to color**: gold (Andrea's accounts) or purple (Henna's accounts).
- Character is "loaded" — it has context.

**1e — Transition: kitchen furnishes itself**
- As the colored character walks from entryway into the main kitchen...
- **The kitchen furnishes itself around them.** Counters, stove, fridge, shelves, ticket rail — everything appears because the character now KNOWS where things are. Context = the kitchen taking shape.
- Character arrives at their station. Kitchen is alive.

---

## Scene 2: "The Pass" (basic interaction + knowledge)

### Setting
- Michelin star kitchen layout. The pass = the long counter with a window above.
- Claude is on the kitchen side. User (Andrea/Henna) is on the dining side.

### Sequence

**2a — First interaction**
- User stands at the pass, gives an order (speech bubble / ticket).
- Claude works: moves to stations, types, searches.
- Output gets "plated" — slides across the pass.
- User reviews. Basic loop: order → cook → plate → present.

**2b — Backpack grows with interaction**
- With each exchange, the backpack gets a little bigger. More conversation = more context consumed.
- Visual: after a few exchanges, backpack is noticeably fuller. The tension: working space shrinks.

**2c — The big book (archibase introduction)**
- User hands Claude a **big heavy book** — throws it across the pass.
- Claude catches it. Backpack grows significantly.
- BUT now Claude is more capable. The book = knowledge (archibase). It knows how to build things, not just reason.
- Claude places the book on their workstation.

**2d — CAG vs RAG (at the workstation)**
- **CAG visual**: 5 thick encyclopedic books stacked on the workstation — everything pre-loaded. Claude has it all at arm's reach. BUT the backpack is BIG because all that knowledge is sitting in context. Every book = more weight. Fast access, heavy carry.
- **RAG visual**: Instead of carrying all 5 books, Claude has a **small box with recipe index cards**. When Claude needs something specific, they check the index, walk to the pantry, grab just that one ingredient, come back. Backpack stays LIGHTER because knowledge is fetched on demand, not pre-loaded.
- Visual: every time Claude grabs something (a tool, a reference, a piece of knowledge) → it goes into the backpack → backpack grows. That's context being consumed.
- Point: CAG = everything upfront, heavy but fast. RAG = light and nimble, but you make trips. The system uses both depending on the situation.

**2e — The log (git introduction, light)**
- While all this happens, a logbook on the counter has been writing itself.
- The kitchen is **surveilled 24/7** — every change, every action gets automatically registered.
- Camera notices the logbook filling up in the background. Sets up Scene 3.

---

## Scene 3: "The Logbook — Git"

### Setting
- Focus shifts to the logbook. Same kitchen.

### Sequence

**3a — The automatic record**
- Every interaction Claude had in Scene 2 → already logged. Dated entries appearing.
- The kitchen cameras caught everything. No extra work needed.

**3b — Everyone copies from the master**
- Andrea's kitchen has a copy. Henna's kitchen has a copy.
- When Andrea updates her copy → it syncs back to the master.
- When Henna starts her shift → she pulls the latest from the master.
- Visual: two kitchens side by side, logbooks syncing. Arrows showing push/pull.

**3c — Zoom into the logbook (git branch viz)**
- Like the Minecraft map zoom from Scene 1.
- Logbook page becomes a branch diagram:
  - Main branch (gold line with commit dots)
  - Feature branch splits off (teal), explored, merges back (green dot)
  - Dead end branch stops (red, [DEAD] label)
- Every branch = a design alternative explored without destroying the original.
- Every merge = a decision made.
- Zoom back out. Logbook is thick.

---

## Scene 4: "The Brigade — Specialization"

### Setting
- Kitchen with multiple doors/cloakrooms visible.

### Objective
- Show HOW specialized agents are formed, not just that they exist.

### Sequence

**4a — The second door (specialization)**
- So far, Claude entered through ONE door and got the map + blueprint.
- But there are OTHER doors in the kitchen. Each one leads to a **cloakroom** for a specific role.
- A Claude walks to a different door: "ANALYST" written above it.

**4b — The specialist scroll**
- Inside the cloakroom: another scroll. But this one isn't the big map of the whole kitchen.
- **Zoom into the scroll** — it's a FOCUSED map. Like the big map, but zoomed into ONE area.
- Example: the Analyst scroll shows the contents of the fridge in detail. Every shelf, every ingredient, every label. The other agents didn't need to know this — but the Analyst does.
- Another example: the Modeler scroll shows a specific tool cabinet with specialized equipment.
- The specialist scroll goes into the backpack. **Backpack grows a tiny bit** — just enough for the role context. Not too much. Just what they need to do their job efficiently.

**4c — Scaling: counter → kitchen → brigade**
- **Small counter** (Level 1): One Claude, one task. Basic.
- **Medium kitchen** (Level 2): Claude + subagents (commis). Two tiers. Context matters now.
- **Full Michelin brigade** (Level 3): Chef de cuisine (user) at the pass. Sous chef (Claude) orchestrating. Chefs de partie at specialized stations (Analyst, Modeler, Builder — each wearing their role's scroll). Commis underneath.
- Communication: sous chef calls out, stations respond, dishes converge at the pass.

---

## Scene 5: "Four Pillars"

### Setting
- The full brigade kitchen from Scene 4, now highlighting what makes it work.

### Objective
- What does a Michelin brigade need to function? Four things.

### Sequence

**5a — Pillar 1: Organisation (infrastructure)**
- The ticket rail (LOCKBOARD) — what's on order, who's working what.
- Closing procedures (session-end) — nothing left behind.
- Labeling system (conventions) — everyone names things the same way.
- "Built once, saves time every service."

**5b — Pillar 2: Knowledge (what you know)**
- You can be talented, but if you don't know techniques, materials, temperatures — you're limited.
- The basic knowledge every cook needs. Recipes, methods, norms.
- This is what the big book from Scene 2 provided. Without it, you can cook but you can't BUILD.

**5c — Pillar 3: Tools (not too much, not too little)**
- The right equipment. Not an empty kitchen, not a cluttered one.
- Show tools being plugged in: MCP cable connecting kitchen to external tools.
- Maybe: Rhino icon as a specialized machine, Blender as another.
- The multiprise (router) = one cable, multiple tools connected.
- Point: just the right amount to be productive.

**5d — Pillar 4: Ingredients (archibase / the pantry)**
- The pantry door opens. Shelves revealed.
- Four layers: SQLite (labeled jars), Guides (technique books), Scripts (tested recipes), RAG (full reference library).
- This is what lets Claude actually produce. Knowledge is knowing how; ingredients are having what you need to make it real.

---

## Scene 6: "The Full Kitchen"

### Setting
- Pull back to show the entire system running.

### Objective
- NOT the booklet (that's personal/internal). This is: look at what we built, the whole system in action.

### Sequence

**6a — Everything running**
- Wide shot. The full kitchen: entryway with scrolls, the pass, the brigade at stations, the pantry, the logbook writing itself, cables connected to tools.
- Characters moving, plating, communicating. The system alive.

**6b — The takeaway**
- "Not just a project — a documented process. Not just architecture — the story of how the architecture was made."
- Or whatever the final line ends up being.
- Fade / transition to next slide (which covers pantry organization + feedback loop — not animated).

---

## What the next slide covers (NOT animated)
- Pantry organization in detail
- Feedback loop: how each session trains the model / improves the system
- This is a separate diagram, not part of the kitchen animation

---

## Sprites & Assets Needed

### Characters (Blender renders)
| Asset | Description |
|-------|-------------|
| Claude grey — idle + walk | Desaturated cube character, no color |
| Claude grey → gold transition | 3-4 frames, grey washing to gold |
| Claude grey → purple transition | 3-4 frames, grey washing to purple |
| Claude gold (Cairn) — full set | idle, walk, sit, type, hold item, celebrate |
| Claude purple (Nova) — full set | Same poses, purple palette |
| Commis — idle + walk | Smaller (75%), blue-grey, simple |
| Partie: Analyst — idle | With apron/badge, at fridge station |
| Partie: Modeler — idle | With apron/badge, at tool station |
| Partie: Builder — idle | With apron/badge, at build station |
| Claude catching book | Arms out, receiving big book |
| Claude placing book on counter | Setting book down at workstation |

### Props (Blender or illustration)
| Asset | Description |
|-------|-------------|
| Gold scroll (CLAUDE.md) | Warm, compass icon |
| Teal scroll (.claude/) | Cool, gear icon |
| Big book (archibase) | Heavy, thrown across pass |
| Recipe index box (CAG) | Small organized box with cards |
| Encyclopedic books x5 (RAG) | Stacked thick books |
| Specialist scroll variants | Focused maps per role |
| Backpack states | empty, small, medium, full, overflow |

### Hero Illustrations (separate designed assets)
| Asset | Description |
|-------|-------------|
| CLAUDE.md treasure map | Parchment, hand-drawn repo structure, warm palette |
| .claude/ blueprint | Technical drawing, kitchen equipment, cool palette |
| Specialist map (zoomed) | One area in detail (e.g., fridge contents for Analyst) |
| Git branch diagram | Gold/teal/green branches, commits as dots |

### HTML/CSS handles
- Room layouts, furniture, walls, floors, lighting changes
- Kitchen furnishing animation (Scene 1e)
- Pass interaction (tickets, plating)
- Logbook entries appearing
- Camera movement between scenes
- Dialogue / narration overlay
- All transitions and interactive controls
