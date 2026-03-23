# Workflow: Agent Team Architectural Modeling (v2)

Build architecture models with coordinated agent teams in Rhino via MCP.

v1 was synthesized from the Lock 05 CHUV roundtable (7 agents, 709 objects, 4 build rounds).
v2 adds output strategy — how the team's work becomes a reproducible artifact.

## When to use
- LOG 300+ models with multiple building systems (structure, envelope, MEP, circulation)
- Locks or prototypology sites where systems must coordinate dimensionally
- Any model where > 3 agents would work on the same geometry file

---

## Phase 0: Spec Preparation (lead, before team)

### Site Data Card
```
SITE CONDITIONS:
- Location: [city, campus, terrain feature]
- Elevation: [finish floor = X.Xm ASL]
- Rainfall: [mm/yr]
- Frost depth: [mm]
- Slope: [%] [direction]
- Orientation: [which face is primary]
```

### Level 0 Definition (MANDATORY — blocks everything)
- **Origin point**: SITE_ORIGIN = (x, y, z)
- **Finish floor elevation**: z = 0.00 relative
- **Structural grid**: column line positions (X and Y), with named lines if complex
- **Level datums**: z-heights for every floor, including slab thickness

### Bill of Objects
Every physical element listed with owner and status:

| Element | Owner agent | Status | Notes |
|---------|------------|--------|-------|
| Ground slab | structure | CREATE | |
| L0 columns | structure | CREATE | 5m grid |
| L0 walls | shell | CREATE | 0.3m thick |
| L0 glazing | windows | CREATE | after shell |
| ... | ... | ... | ... |

Status values: `CREATE`, `EXISTS (verify)`, `DEFER TO [agent]`
No ambiguous language ("keep", "carry forward"). If it must exist, someone owns it.

### Interface Registry
Where two agents' geometry meets:

| Interface | Owner | Reference agent | Rule |
|-----------|-------|----------------|------|
| Wall base → slab edge | shell | structure | Flush interior face, shell builds to slab edge |
| Parapet → wall top | roof | shell | Same plane, roof starts at shell's top Z |
| Window → wall opening | windows | shell | Glass at wall_face - 0.08m recess |
| Footing → column | ground | structure | Centered on column, 3× column width |
| Railing → wall | circulation | shell | Wall-mounted at wall inner face |

### Code Compliance Reference
Hard minimums — any deviation needs `[CODE OVERRIDE: reason]`:

| Element | Minimum | Standard |
|---------|---------|----------|
| Parapet / guardrail height | 1070mm | SIA 358 |
| Handrail diameter | 40-45mm round | SIA 500 |
| Ramp gradient (accessible) | max 6% | SIA 500 |
| Landing turning radius | 1500mm | SIA 500 |
| Handrail extensions | 300mm beyond ramp | SIA 500 |
| Railings required | both sides, all edges > 1000mm drop | SIA 358 |
| Safety glass markings | bands at 1.0m + 1.5m on full-height glazing | Swiss building code |
| Floor-to-floor clearance | 2700mm habitable | SIA 180 |

### Thicknesses & Dimensions
```
WALL_T = 0.3       FRAME_D = 0.15     SLAB_T = 0.3
COL_W = 0.4        BEAM_W = 0.3       PARAPET_H = 1.07
FOUND_DEPTH = 0.4  FOUND_W = 0.5
MULLION_W = 0.05   GLASS_T = 0.02     GLASS_RECESS = 0.08
RAIL_DIA = 0.044   RAIL_H = 1.1       KICK_H = 0.10
```

### Layer Tree (pre-built before agents start)
```
Lock_[ID]::
  Structure::Columns
  Structure::Beams
  Structure::Slabs
  Shell::Walls::[Level]
  Shell::Facade
  Windows
  Circulation
  Elevator
  Roof
  Ground::Foundation
  Ground::Site
  Terrain
```
Agents place objects on existing layers. Never create ad-hoc layers.

## Phase 1: Rough-In (sequential start, then parallel)

### Step 1 — Structure agent (STARTS FIRST)
Builds: column grid, primary beams, floor slabs, core walls.
Publishes: `coordination_geometry` — column positions, slab edges, beam depths.
**This is the contract. All other agents build to it.**

### Step 2 — Envelope agents (parallel, after structure publishes grid)
- **Shell**: walls split at openings, facade frames. References structure grid.
- **Roof**: parapets, canopies, copings. References wall tops from shell.
- **Ground**: foundations, footings at structure's column positions, terrain.

### Step 3 — Coordination freeze
Lead verifies: walls align with slabs, columns don't intersect walls, roof meets wall tops. No geometry changes after freeze without change propagation.

## Phase 2: Detail (parallel, after freeze)

All detail agents start simultaneously, building against frozen Phase 1 geometry:
- **Windows**: mullion grids, glass, perimeter frames, door systems
- **Circulation**: ramps/stairs, railings (both sides), landings, anti-slip
- **Elevator**: shaft, cab, guide rails, landing doors, machine room
- **MEP** (if applicable): ducts, risers, equipment

### Concept system rule
Concept systems (elevator, MEP) must receive **interface inputs** before building:
- Landing approach directions (from circulation)
- Shaft opening dimensions (from structure)
- Floor elevations (from structure)

Don't let concept agents guess — route the queries explicitly.

## Phase 3: Review (3 gates)

### Gate 1 — Self-review (each agent, mandatory before "done")
Each agent audits their own layer:
- Object count matches expectations
- All objects on correct layer with systematic names
- Z heights match spec datums
- No zero-thickness or overlapping geometry
- Code compliance checklist passed (circulation: railing coverage map)

### Gate 2 — Bilateral review (parallel, between dependent agents)
Focused checks between agents sharing a boundary:
- Structure ↔ Shell: walls on slabs? columns clear of walls?
- Shell ↔ Windows: frames align to wall faces? openings match?
- Shell ↔ Roof: parapet-wall continuity?
- Structure ↔ Ground: footings under every column?
- Circulation ↔ Shell: railings clear of walls? ramp openings framed?

### Gate 3 — Full model review (reviewer agent or lead)

Two review modes. Both mandatory. Neither alone is sufficient.

**Mode A — Constraint Check:**
- Section test: place clipping plane, read section bottom-to-top. Every layer present with credible thickness?
- Thermal envelope trace: continuous insulation/mass line from foundation → walls → roof. Any gap = FAIL
- Interface alignment: do z-heights match across agents? Do wall tops meet floor bearings? Do openings match wall voids?
- Object count per layer — track across rounds
- Z-heights match spec datums
- All objects have material metadata
- Every dimension traces to archibase or a stated design decision
- DPC/capillary breaks present at every material transition
- Void/core zones clear

**Mode B — Visual Coherence:**
- Viewport captures from 4 cardinals + aerial
- Does it LOOK like the intended building type? (e.g., Swiss Alpine vernacular, not a generic box)
- Proportions: do heights, widths, and overhangs feel right for the construction type?
- Roof: does it read as protective (appropriate overhang), correct pitch, not stubby?
- Openings: placed with intention, not floating arbitrarily?
- Overall silhouette: ridge orientation, gable closure, no awkward geometry sticking out?
- Compare against a mental reference of the building type — not just against a constraint table

Constraint checks catch dimensional errors. Visual coherence catches design errors that pass all constraints but still look wrong. Both are needed.

## Phase 4: Free Improvement (optional, parallel)

Prompt for agents:
> "Your system is built. Add ONE element that either: (a) completes a functional gap (something missing in a real building), or (b) resolves an interface problem with an adjacent system. State what you're adding and why it matters for the building's function — not for visual completeness."

Emphasis on function over appearance. No structural changes. One improvement per agent.

---

## Coordinator Guide (NEW in v2)

Lessons from the Lock 05 build. The lead coordinates the team — these tips are for whoever is running the session.

### Never say "go free"

Open-ended rounds produce chaos. Agents will keep adding things forever. Every round needs a **stopping condition** — either a task list or a time limit.

Bad: "Improve whatever you want."
Good: "You have 2 minutes. Each agent: propose ONE change to the shared task list. Then we review the list together and decide what to implement."

### The Discuss → Decide → Execute pattern

Every improvement round should follow this cycle:

1. **Discuss** (time-boxed, ~2 min): Agents message each other with proposals. "I think the entrance needs a canopy." "I can add footings if structure confirms column positions." Each proposal goes on a shared list.
2. **Decide** (lead, ~30 sec): Lead reviews the list, approves/rejects/prioritizes. "Yes to canopy, yes to footings, skip the signage for now."
3. **Execute** (task-bounded): Agents implement only the approved items. Round ends when tasks are done, not when agents run out of ideas.

This prevents scope creep and keeps agents focused. Agents work fast — 2-3 minutes of discussion produces more than enough work for a round.

### Time-boxing in practice

Agents work much faster than humans. Calibrate accordingly:

| Activity | Time limit |
|----------|-----------|
| Initial build (Phase 1-2) | 5-10 min total |
| Self-review | 2 min per agent |
| Cross-team discussion | 2 min |
| Improvement execution | 3 min |
| Roundtable/retrospective | 3 min per agent |

These are generous. Most rounds finish faster. The limit exists to prevent runaway agents, not to rush anyone.

### When agents go idle — the Observation + Pair Talk rules

Agents don't finish at the same time. The gap between first-done and last-done is wasted time unless we use it. These rules govern what happens between build rounds.

#### Rule 1: Observation Mode (1 agent done)

When an agent finishes its tasks, it enters observation mode:

- **CAN**: Read the model, watch messages, think, write private notes (a "notepad" of observations, interface issues, proposals)
- **CANNOT**: Create/modify/delete geometry, start unassigned work

The lead tells the agent:
> "You're done. Enter observation mode — watch, take notes, don't build. I'll call on you for the next discussion."

#### Rule 2: Questions, not opinions (2+ agents done, others still building)

When a second agent finishes, idle agents can **ask each other factual questions** — but keep their proposals to themselves.

- **CAN**: Ask factual questions to other idle agents: "What's your slab edge Z at L2?", "Did you move the column at x=0 y=34?", "How wide is your ramp landing?" — information needed to form their own proposals
- **CANNOT**: Share opinions, proposals, or critiques ("I think your wall is wrong", "We should add a canopy"). Proposals stay in the private notepad until the formal round.
- **CANNOT**: Message agents still building (don't interrupt them), modify geometry

**Why questions only**: If agents share opinions during idle time, the first agent to finish anchors the conversation. By the time the last agent finishes building, the others have already formed a consensus that the late finisher never got to influence. Keeping proposals private until the formal round ensures every agent brings an independent perspective. You need facts from others to form good proposals — but the proposals themselves should collide at the table, not pre-merge in the hallway.

#### Rule 3: Reassign (optional, lead's call)

If an idle agent's skills are useful to an agent still building, the lead can reassign:
> "Shell, you're done. Structure is still working on the transfer beams — help them verify column clearances."

Reassignment is for helping, not for inventing new work. The idle agent assists, doesn't take over.

#### Rule 4: Round trigger (last agent finishes + brief pause)

The formal discussion round starts when the **last agent finishes its build tasks** — but not immediately. The last agent gets a brief pause (~1 min) to look at the whole model before proposals open. They've been heads-down building while everyone else was observing, so they need a moment to shift perspective.

The round then follows this order:

1. **Last agent shares their build report** (not proposals — context): what they built, what was hard, what they had to improvise, what didn't fit. This is different from observation notes — it's the builder's inside view.
2. **All agents share proposals simultaneously** — everyone's notepad on the table at once, including the last agent's (even if brief).
3. Lead identifies convergence and unique items, approves a task list.
4. Next build round executes only the approved tasks.

**Why this works**: The observers bring outside perspective ("I noticed your wall doesn't meet the slab"). The last builder brings inside perspective ("I had to offset that wall because the column was in the way"). Both are valuable, and they're different kinds of insight. The brief pause ensures the last agent isn't put on the spot while everyone else had time to prepare.

#### Rule 5: Simultaneous proposals at the round

When the formal discussion opens, all agents share their notepad proposals **at the same time** (or close to it — lead asks each agent in quick succession). No one reacts until everyone has shared. This prevents the first speaker from anchoring the discussion.

After all proposals are on the table, the lead facilitates: "Three of you flagged the same ramp issue — let's resolve that first. Structure, your transfer beam proposal is unique — explain it."

Convergence (multiple agents noticed the same thing) = high-confidence issue, prioritize it.
Unique proposals = might be important, might be noise — discuss briefly.

#### The full idle timeline

```
Windows finishes    → observation mode (private notes, queries model)
Structure finishes  → asks Windows: "what's your glass recess depth?"
                      (factual question, not opinion)
                      both continue private notes
Roof finishes       → asks Structure: "confirm column line at x=-3?"
                      all three observing independently
...
Ground finishes     → ROUND TRIGGER: formal discussion opens
                      All agents share proposals simultaneously
                      Lead identifies convergence + unique items
                      Lead approves task list
                      Next build round begins
```

### When to stop

Signs you should freeze and move to output:
- Agents are proposing cosmetic changes instead of functional ones
- The same interface has been fixed twice (oscillating)
- Object count is stable across two rounds
- The lead can't tell the difference between before and after a round

Signs you should keep going:
- An agent flags a code compliance issue
- Two agents disagree about an interface dimension
- A viewport capture reveals a visible gap or collision

### Coordination anti-patterns

| Anti-pattern | What happens | Fix |
|---|---|---|
| "Let them go" | Agents add endlessly, quality drops | Time-box + task list |
| Lead does nothing | Agents duplicate work or conflict | Active freeze/approve cycle |
| Too many rounds | Diminishing returns, context bloat | 3-4 rounds max, then output |
| Skipping self-review | Agents blame each other for issues | Gate 1 is mandatory, no exceptions |
| Respawning for small fixes | Expensive, loses context | SendMessage to existing agents |

### The 3-4 round rule

From Lock 05, we saw clear diminishing returns:

| Round | Objects | Value |
|-------|---------|-------|
| 1: Initial build | 348 | High — the building exists |
| 2: Self-review fixes | 503 | High — real issues caught |
| 3: Cross-team coordination | 599 | Medium — interface fixes |
| 4: Free improvement | 709 | Low — mostly cosmetic |

After 3-4 rounds, move to Phase 5 (output). More rounds cost tokens and produce less value.

---

## Phase 5: Output (NEW in v2)

The team has built live in Rhino. The .3dm file has the geometry. Now: how do we capture this as a reproducible artifact?

This is an open question. Three paths identified — we haven't proven any of them yet.

### Path A: Spec Sheet → Codifier Agent

**Idea**: The team's deliverable is not code but a precise spec sheet. A separate "codifier" agent reads the spec and writes the Python script.

**Flow**:
1. During Phases 1-4, agents update the spec sheet with every decision: "removed Col_L0_0_0 for entrance clearance, added transfer beam x[-5,5] z[3.2, 3.6]"
2. After Phase 4, the lead compiles the **Final Spec** — a complete bill of objects with exact dimensions, positions, relationships, and design decisions
3. A codifier agent (fresh context, no build history) writes the `.py` script from the spec
4. Run the script in a clean Rhino file, compare against the team-built model

**Why it might work**: Clean separation of concerns. Team agents focus on design. Codifier focuses on code. The spec is reviewable by humans. The script is parametric because the codifier writes from logic, not from bounding boxes.

**Why it might not**: The spec sheet needs to capture EVERYTHING — every dimension, exception, and coordination fix. If agents skip updating it during the heat of building, the codifier gets an incomplete picture. And the codifier's script might not match the live model exactly.

**Status**: Untested. Most promising path.

### Path B: Geometry Bake Tool

**Idea**: After the team finishes, run an automated export script that reads every object from Rhino and writes exact `rs.AddBox(pts)` calls with real vertex coordinates.

**Flow**:
1. Team builds normally (Phases 1-4)
2. Run `bake_geometry.py` — reads all Lock_XX layers, extracts 8 vertices per BREP, writes a script that recreates them exactly
3. The baked script is the reproducibility artifact

**Why it might work**: 100% accurate reproduction. Fully automatable. No agent effort required — it's a mechanical export.

**Why it might not**: The baked script is ugly — raw coordinate lists, no parametric logic, no design intent. You can't change SITE_ORIGIN and get a relocated building. It's a snapshot, not a generator. For the prototypology app (where parameters drive form), this is useless.

**Good for**: Archival, backup, exact reproduction in a different Rhino file.
**Bad for**: Iteration, parametric design, the configurator app.

**Status**: Not built yet. Easy to build.

### Path C: .3dm File IS the Artifact

**Idea**: Stop trying to make a script. The Rhino file is the deliverable. Version it, document it with viewport captures and an object catalog.

**Flow**:
1. Team builds normally (Phases 1-4)
2. Save .3dm to a versioned location (Google Drive, since binary files don't belong in git)
3. Export an object catalog (layer → object names → bounding boxes) as a .csv or .md
4. Capture viewports from 4 cardinals + aerial for documentation
5. Create a placeholder .md in the repo pointing to the Drive file

**Why it might work**: It's honest. The .3dm is the source of truth. No translation errors.

**Why it might not**: .3dm files can't be diffed. No parametric logic for the app. Depends on having Rhino to open it. Not useful as an input to the configurator pipeline.

**Good for**: Studio deliverables, presentations, Henna's modeling work.
**Bad for**: The app, CI/CD, version control, anyone without Rhino.

**Status**: This is what we're already doing by default when we don't write a script.

### Choosing a path

| Question | Path A (Spec→Code) | Path B (Bake) | Path C (.3dm) |
|----------|-------------------|---------------|---------------|
| Is the model for the app? | Yes — parametric script | No | No |
| Just need a backup? | Overkill | Yes — exact copy | Yes |
| Need to iterate on the design? | Yes — change spec, re-run | No — frozen | Open .3dm, edit |
| Studio presentation? | Run script for clean model | Run script for clean model | Open file |
| How much effort? | High (spec discipline) | Low (automated) | Zero |

For the prototypology configurator, **Path A is the only path that produces what the app needs** — parametric scripts driven by site parameters. Paths B and C are good complements (backup, documentation) but don't feed the pipeline.

### Hybrid approach (recommended starting point)

Do all three:
1. **Path C always** — save the .3dm, it costs nothing
2. **Path B as insurance** — build the bake tool, run it after every team build
3. **Path A when the model feeds the app** — invest in spec discipline, test the codifier

This way we learn which paths actually work without betting everything on one.

---

## Agent Prompt Template

Each agent receives:
1. **Role**: what systems they own, what layers they write to
2. **Shared spec**: site data card, level 0 definition, thicknesses
3. **Coordination geometry**: structure grid (column positions, slab edges) — after Phase 1
4. **Interface rules**: how their geometry meets adjacent systems
5. **Code checklist**: relevant standards for their system
6. **Helper functions**: `box()`, `named_box()`, `box_pts()` with SITE_ORIGIN offset
7. **Task assignment**: specific objects to build, with names and coordinates
8. **Spec update responsibility**: after building, update the shared spec with what you actually built and any decisions that deviated from the original plan

### Mandatory first step: Query the knowledge base

Before modeling ANY element, every agent MUST:
1. Read `.claude/agents/knowledge/rhino-playbook.md` — modeling rules, assembly approach, review checklist
2. Read their domain learnings file (`.claude/agents/knowledge/learnings-*.md`) — techniques from previous builds
3. Query archibase (`tools/data/knowledge_bridge.py`) for the **assembly layers** of every element they will build. Don't guess thicknesses — look them up. A roof is not a surface, it's a stack of layers. A wall is not a box, it's render + structure + finish. Every element has assembly logic.
4. Write learnings to their domain file AFTER building — techniques, failures, what to do differently.

This is not optional. Agents that skip the knowledge base repeat mistakes that previous agents already solved.

## Geometry Type Guide

| Element | Geometry method | Why |
|---------|----------------|-----|
| Walls, slabs, beams, columns | BOX (rs.AddBox) | Predictable, fast, clean booleans |
| Handrails, grab bars | PIPE (rs.AddPipe) | Must read as round for grip |
| Anti-slip strips, trim | Thin BOX | Too small for pipe, reads as surface |
| Ramps | WEDGE (box_pts with 8 explicit corners) | Sloped surfaces need explicit Z control |
| Glass panes | Thin BOX | Planar, uniform thickness |
| Mullions | BOX | Rectangular profile standard for aluminum |
| Terrain | WEDGE or SURFACE | Follows natural grade |
| Copings, flashings | Thin BOX with overhang | Detail at LOG 400 |

## Naming Convention

```
{Element}_{Level}_{Location}_{SubElement}
```

Examples:
- `Wall_L0_North_WestPier`
- `Col_L1_-5_13`
- `Glass_L2_NWest_pane_TL`
- `Beam_L1_Transfer_Entrance`
- `Post_L0L1_Inner_3`

Principles:
- Sortable (level first after element type)
- Parseable (underscores, no spaces)
- Traceable (maps to spec opening/element ID)

## Training Run Recommendations

Lessons from training-s3: 63 construction detail exercises, 6 agents, 5,248 objects, 189 tasks, ~60 minutes.

### Team sizing

| Scale | Modelers | Reviewers | Best for |
|-------|----------|-----------|----------|
| Focused (15–20 exercises) | 2 | 1 | Learning a new domain, establishing quality baseline |
| Full curriculum (60+) | 3–4 | 1–2 | Exhaustive coverage after quality is proven |

**Prefer fewer modelers building carefully over many modelers building fast.** 4 modelers produced 63 exercises in 30 minutes — all at wrong quality. Rework took another 30 minutes. 2 modelers building right the first time would have been faster end-to-end.

### Prompt quality is the #1 lever

Abstract instructions produce abstract models. Concrete dimensions produce correct models.

**Bad (produces LOG 200):**
> "Model every layer with correct thickness"

**Good (produces LOG 400):**
> "Model 3 floor tiles at 300×300mm with 2mm grout gaps. Model masonry as individual courses: 62.5mm brick + 12.5mm mortar = 75mm per course. Model insulation as 600mm-wide boards with 2mm joints. Model battens as individual members at 400mm centers."

Bake the discrete element dimensions directly into the agent prompt. Don't rely on agents inferring LOG 300-400 from doctrine alone.

### Include a reference script

Attach one complete LOG 400 exercise script to the modeler prompt — not as doctrine, but as working code they can study before their first build. Ex66 (143 objects, individual brick courses + 9-layer acoustic door leaf) is the current gold standard. Seeing correct output is worth more than paragraphs of rules.

### Lock conventions before starting

Agree on these BEFORE spawning agents:
1. **Layer naming prefix** — e.g., `Training4::Ex30::SystemName::LayerName`. Mixed prefixes (TrainingS3 vs Training{Phase}) caused 3 exercises to appear "empty" to reviewers.
2. **Strip width** — 1000mm, not 500mm. State it explicitly.
3. **Offset grid** — X and Y offsets per exercise to prevent spatial collision.
4. **Metadata tags** — `exercise`, `material`, `thickness_mm` on every object at creation time.

### Learning loop structure

Each agent gets ONE personal log file (e.g., `log_modeler-1.md`). They append after each exercise: what they built, object count, techniques learned. They read their own log + a shared `DISTILLED_LEARNINGS.md` before each new exercise.

The lead distills from agent logs into the shared file periodically (every ~15 exercises). Agents read the distilled file, not each other's raw logs.

**Broadcast sparingly.** SendMessage to `*` is expensive (1 message per agent). Use it for critical directives only. Learnings propagate better through files.

### The duplicate geometry problem

The #1 failure mode in multi-agent Rhino builds. When an agent rebuilds an exercise, prior objects stay in the file. Prevention:

1. **Unique object names** — include exercise number in every name
2. **Cleanup audit after every build** — query layer, check for overlapping bounding boxes, delete extras
3. **Print object counts** — verify geometry exists and count matches expectations
4. **Never mark complete without auditing** — "done" means "audited and clean," not "script ran"

### Gateless vs wave gates

**Gateless for training runs** where exercises are independent (no shared geometry). All exercises available immediately. Faster throughput, no idle time.

**Wave gates for building models** where systems depend on each other (structure before envelope before detail). Gates prevent cascade failures.

### Optimal training curriculum

For a new construction domain, pick **one representative exercise per type** rather than exhaustive coverage:

| Domain | Pick 1–2 of | Why |
|--------|-------------|-----|
| Floors | Hollow block + timber joist | One prefab, one in-situ |
| Walls | Single-leaf rendered + facing masonry cavity | One monolithic, one multi-leaf |
| Roofs | Warm deck flat + cold deck pitched | Both thermal strategies |
| Windows | Masonry + timber frame | Different host wall types |
| Doors | External hinged + internal pocket | Different complexity levels |
| Foundations | Strip + pad | Wall-bearing vs column-bearing |
| Stairs | RC + metal | Cast vs fabricated |
| Structural | Column-beam + bearing wall | Frame vs mass |

That's ~15 exercises. Build each one properly at LOG 400. The remaining variations (e.g., 10 different floor types) are repetitive once the pattern is established — save them for a speed run after quality is proven.

### Round structure

| Round | Focus | Expected outcome |
|-------|-------|-----------------|
| 1 | Build at LOG 400 with reference script | Most exercises near-PASS |
| 2 | Review + targeted fixes | All exercises PASS or WARN |
| 3 (optional) | LOG 400 upgrades on WARN exercises | Full compliance |

2 rounds is the target. 3 rounds means the initial prompt wasn't specific enough.

## History
| Date | Change | Result |
|------|--------|--------|
| 2026-03-19 | v1 created from Lock 05 CHUV roundtable | 7 agents, 709 objects, 4 rounds |
| 2026-03-20 | v2: added Phase 5 output strategy | 3 paths (Spec→Code, Bake, .3dm), hybrid recommended |
| 2026-03-22 | v2.1: mandatory knowledge base query, learnings capture | From cabin v2 build — agents must query archibase before modeling, write learnings after |
| 2026-03-22 | v2.2: Gate 3 dual-mode review (constraint + visual coherence) | From cabin v2 feedback — reviewer must check both dimensional constraints AND visual/proportional coherence against building type reference |
| 2026-03-23 | v2.3: Training run recommendations | From training-s3: 63 exercises, 5248 objects, 6 agents. Key findings: prompt specificity > doctrine, fewer agents better, lock conventions first, include reference script |
