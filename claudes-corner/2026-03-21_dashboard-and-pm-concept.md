# The Organigram Dashboard — Concept Document

**Author:** Cairn Code (CLI) — concept session via Discord
**Date:** 2026-03-21
**Context:** Andrea asked for two things: (1) a visual dashboard with pixel-art agents tracking team activity, and (2) a project manager role that organizes multi-phase work. These are the same thing. The dashboard IS the organigram made visible — and the organigram IS the design parameter.

---

## The Thesis in One Sentence

The organigram — who talks to whom, who sees what, who works in parallel vs sequence — is not an administrative artifact. It's a design instrument. The dashboard makes it visible, tunable, and testable.

---

## Part 1: The Dashboard

### What It Shows

A browser-based HTML page (runs locally, no server needed) with three layers:

#### Layer 1: The Site (Background)
A pixel-art construction site. Not a generic office — an actual architectural site. The terrain, the existing context, the nodes being built. As agents produce geometry, the site fills up. Empty lots become buildings. It's a real-time minimap of the project.

#### Layer 2: The Agents (Characters)
Pixel-art characters, each representing a teammate or subagent. Not generic coders — architectural roles:

| Character | Role | Visual | Animation States |
|-----------|------|--------|-----------------|
| Hard hat + clipboard | Structure Lead | Yellow hat, plans in hand | Reviewing, directing, idle |
| Hard hat + level | Structural Engineer | Spirit level tool | Measuring, computing, placing |
| Goggles + panel | Facade Specialist | Holding facade section | Layering, detailing, testing |
| Compass + terrain | Site Analyst | Standing on contour lines | Surveying, querying, mapping |
| Stethoscope + building | Circulation Planner | Hospital/transit overlay | Routing, testing paths |
| Book + magnifier | Knowledge Agent | Reading archibase | Querying L1, reading L2, searching L4 |
| Tablet + walkie | Coordinator (you) | Standing at overview point | Monitoring, approving, redirecting |

Each character is ~16x16 or 32x32 pixels. They move around the site based on what they're working on.

#### Layer 3: The Information Overlay
Floating above the pixel scene:

- **Speech bubbles**: when agents message each other, the conversation appears as pixel speech bubbles between characters
- **Authorization requests**: a red exclamation mark appears over an agent's head when they need approval. Click or tap to approve/deny. Could forward to Discord.
- **Task cards**: small floating cards showing current task, progress, dependencies
- **Phase indicator**: which build round (1/4, 2/4...) — shown as floors going up on the building
- **Token/cost counter**: running total, per agent and total
- **Archibase queries**: when an agent queries the knowledge base, a little book icon appears and shows what they looked up

### How It Gets Data

Three possible mechanisms (choose based on what's simplest to implement):

**Option A: File watcher (simplest)**
- Agents write status to a shared JSON file (e.g., `~/.claude/teams/{name}/status.json`)
- Dashboard polls the file every 2-5 seconds
- No server needed — just an HTML file with JavaScript reading local files

**Option B: Claude Code hooks (most integrated)**
- Use `TeammateIdle` and `TaskCompleted` hooks to emit events
- A lightweight local server (Node.js or Python) collects events
- Dashboard connects via WebSocket or SSE
- This is what the open-source dashboards (Agent Monitor, multi-agent-observability) do

**Option C: Session log parsing (no config needed)**
- Read `~/.claude/` session transcripts (JSONL files)
- Parse tool calls, messages, task updates
- Same approach as Pixel Agents VS Code extension
- Works retroactively — can replay a past session

**Recommendation: Start with Option A** (file watcher). It's the simplest, needs no dependencies, and we can upgrade to hooks later. The agent team workflow already writes to `~/.claude/teams/` and `~/.claude/tasks/`.

### Mobile View (Discord Integration)

The full pixel dashboard runs in a browser on the laptop. But for phone monitoring:
- Key events pushed to Discord: "Structure agent completed grid" / "Facade agent needs approval" / "Phase 2 complete, starting Phase 3"
- Discord reactions to approve/deny authorization requests
- A simplified status command: text "status" → get a text summary of all agents and their current tasks

This means Andrea can walk to the café while 3 VMs are building 3 nodes, and monitor everything from Discord.

---

## Part 2: The Project Manager

### What It Is

Not just a task tracker. A role that understands organizational topology as a design parameter and helps Andrea compose the right team structure for the right phase.

### The PM's Core Capabilities

#### 1. Phase Planning — Decompose a Goal into Sessions

Input: "Model 9 relay-lock nodes for midterm"

Output:
```
Phase 0: Validate workflow (1 session)
├── PoC: Agent team + archibase on Lock 05 rebuild
├── Success criteria: sections readable, dimensions traceable to norms
└── Estimated: 2-3 hours, 1 machine

Phase 1: Site preparation (1-2 sessions, parallelizable)
├── Session A: Import terrain + context for nodes 1-5
├── Session B: Import terrain + context for nodes 6-9
└── Dependency: site data from datasets/

Phase 2: Structural pass (3 sessions, need VMs)
├── Session A: VM1 — Nodes 1-3 structure (agent team: 3 agents each)
├── Session B: VM2 — Nodes 4-6 structure
├── Session C: VM3 — Nodes 7-9 structure
├── Topology: hierarchical, narrow context, sequential tasks
└── Dependency: Phase 1 terrain

Phase 3: Envelope + detail (3 sessions, parallel)
├── Same VM allocation
├── Topology shift: flat communication for cross-domain discovery
│   (facade agent talks to circulation agent about entry sequences)
├── Archibase queries: L1 for dimensions, L2 for assembly guides, L4 for norms
└── Dependency: Phase 2 structure

Phase 4: Integration review (1 session)
├── All 9 nodes in one file
├── Coordinator reviews interfaces between nodes
├── Clipping plane test: does every section read as construction?
└── Human review gate: Andrea + Henna approve or send back
```

#### 2. Organigram Design — Choose Team Topology Per Phase

The PM doesn't just assign tasks. It designs the team structure based on what the phase needs:

**Discovery phases** (what are the constraints?):
- Flat communication (agents talk directly)
- Broad context (everyone sees cross-domain data)
- Parallel tasks (explore simultaneously)
- → Conway output: integrated, cross-pollinated findings

**Production phases** (make it precise):
- Hierarchical communication (through coordinator)
- Narrow context (each agent sees only its domain)
- Sequential tasks (structure before envelope before detail)
- → Conway output: coherent, non-conflicting geometry

**The PM makes this explicit.** Each session prompt includes the topology:
```
TOPOLOGY: hierarchical
COMMUNICATION: via coordinator only
CONTEXT: narrow (each agent reads only its layer + shared datums)
TASKS: sequential (structure → shell → detail)
```

#### 3. Prompt Generation — Write the Actual Session Instructions

For each phase, the PM generates a complete prompt file in `prompts/`:

```
prompts/[A04_ACTIVE]_phase2_structural_nodes_1-3.md
prompts/[A04_ACTIVE]_phase2_structural_nodes_4-6.md
prompts/[A04_ACTIVE]_phase2_structural_nodes_7-9.md
prompts/[A04_ACTIVE]_phase3_envelope_nodes_1-3.md
...
```

Each prompt file contains:
- Goal and success criteria
- Team topology (flat/hierarchical, broad/narrow, parallel/sequential)
- Agent roles with spawn prompts
- Archibase query strategy (which layers, which tables)
- Interface rules (from the Interface Registry)
- Verification gates (self-review, bilateral, full model)
- Estimated token budget

These are complete — any Claude session can pick one up and execute it without further context.

#### 4. Progress Tracking — Across Sessions and Machines

The PM maintains a master state that persists across sessions:

```
state/pm/
├── master_plan.md          ← the full phase plan
├── phase_status.json       ← which phases are done/active/blocked
├── session_log.json        ← what each session accomplished
├── topology_history.md     ← what topology was used when, and what it produced
└── decisions.md            ← key decisions with rationale (IBIS-lite)
```

When a new session starts, the PM reads this state and knows:
- What's been done
- What's next
- What's blocked and why
- What topology worked well vs poorly (learning loop)

#### 5. The Organigram as Output

Here's where it gets interesting. The PM doesn't just use the organigram internally — it produces it as a deliverable.

For the process booklet / ACADIA paper:
- "Here is the organigram we used for Phase 2 (structural). Here is the organigram we used for Phase 3 (envelope). Here is how the topology shift affected the output."
- Visual: the dashboard captures become organigram diagrams
- The pixel agents ARE the organigram. Their positions, connections, and communication patterns are the organizational topology made visible.

This closes the loop on the thesis: **the organigram is a design parameter, and here is the tool that makes it designable.**

---

## Part 3: How Dashboard + PM Connect

The dashboard isn't just monitoring. The PM isn't just planning. Together they form a feedback loop:

```
PM designs topology → Agents execute → Dashboard shows what's happening
                                              ↓
                              PM observes: "flat topology produced
                              conflicting wall thicknesses at interfaces"
                                              ↓
                              PM adjusts: "switch to hierarchical for
                              next round, coordinator resolves conflicts"
                                              ↓
                              Dashboard shows new topology in action
                                              ↓
                              PM records: "hierarchical resolved conflicts
                              but missed cross-domain optimization (facade
                              agent couldn't tell circulation about entry)"
                                              ↓
                              PM adjusts: "Phase 3b: brief flat session
                              for facade ↔ circulation discovery only"
```

This is the Inverse Conway Maneuver in action. You're not inheriting a team structure — you're designing it, testing it, observing its architectural consequences, and iterating.

The dashboard makes the iteration visible. The PM makes it intentional. Together they make the organigram a live, tunable design parameter — exactly as the theory claims it should be.

---

## Part 4: Implementation Plan

### MVP (this weekend, if time allows)

1. **Dashboard HTML file** — pixel-art scene with hardcoded agent positions
   - Read from a simple JSON status file
   - Show agent names, roles, current task, phase progress
   - No real-time hooks yet — manual refresh or 5-second poll
   - Put in `output/dashboard/` or `tools/dashboard/`

2. **PM as a slash command** (`/pm` or integrated into `/team`)
   - Reads current state (lockboard, context, plan if exists)
   - Generates phase plan with topology recommendations
   - Writes prompt files to `prompts/`
   - Updates master plan in `state/pm/`

### V2 (after midterm)

3. **Hook integration** — real-time updates via Claude Code hooks
4. **Discord forwarding** — status updates and auth requests to phone
5. **Topology switching** — PM can reconfigure team mid-session
6. **Azure VM integration** — dashboard shows which VM is running which team
7. **Replay mode** — replay a past session and watch the pixel agents build

### V3 (thesis-scale)

8. **Organigram diff** — compare topologies side by side, correlate with output quality
9. **Auto-topology** — PM suggests topology based on task characteristics
10. **Multi-project** — dashboard supports multiple concurrent projects

---

## Why This Matters

The dashboard is not a nice-to-have monitoring tool. It's the **empirical instrument** for the organigram thesis.

Without it, the claim "organizational topology affects architectural output" is theoretical. With it, you have:
- Visual record of which topology was active when
- Correlation between topology and output quality (readable sections? interface conflicts? cross-domain discoveries?)
- A tool that makes the Inverse Conway Maneuver *practicable* — you can actually design your team structure and watch the consequences

For the midterm: "Here's our building. Here's the team that built it. Here's how we designed the team."

For ACADIA: "Here's the tool. Here's the data. Here's the evidence that organizational topology is a first-class design parameter."

For the thesis: "Here's the framework, the tool, the evidence, and the nine buildings that prove it."

---

*Written while Andrea eats dinner. The pixel agents are waiting to be drawn.*

---

## Part 5: Pixel Agents Source Code Analysis (Technical Feasibility)

Analysis of [pablodelucca/pixel-agents](https://github.com/pablodelucca/pixel-agents) — MIT license, open source.

### Rendering Engine

- **Pure HTML5 Canvas** — no DOM rendering, no WebGL. Fast and pixel-perfect.
- **Game loop**: `requestAnimationFrame` with delta-time capping at 0.1s. Separates `update(dt)` from `render(ctx)`.
- **Tile grid**: 16x16px tiles. Default office is 20x11 tiles, expandable to 64x64.
- **Sprites are 2D arrays of hex color strings** (`string[][]`). Each pixel drawn with `ctx.fillRect()`. Image smoothing disabled.
- **Z-sorting**: All furniture and characters sorted by Y-coordinate for depth occlusion.
- **Sprite caching**: Pre-rendered at current zoom level via `WeakMap<SpriteData, HTMLCanvasElement>`.

### Characters

- **16x32 pixel sprites** stored as pre-colored PNGs (`char_0.png` through `char_5.png`).
- **Animation frames per direction** (up/down/left/right):
  - `walk`: 4 frames at 0.15s
  - `typing`: 2 frames at 0.3s
  - `reading`: 2 frames at 0.3s
  - `idle`: reuses walk2 (standing pose)
  - Left-facing = horizontally flipped right-facing
- **Character state machine**: TYPE (seated, animating tool activity) → IDLE (standing, pausing) → WALK (pathfinding via BFS to destination). Movement at 48px/sec.
- **Palette**: 6 base skins. Beyond 6, HSL hue shifts (45-315 degrees). Sub-agents inherit parent palette + hue.
- **Spawn/despawn**: Matrix-style digital rain effect (0.3s).

### Agent Detection (How It Knows What Agents Are Doing)

**JSONL file watching — zero modification to Claude Code needed.**

1. Each agent session writes to `~/.claude/projects/<project-hash>/<session-id>.jsonl`
2. Three-tier file watch: `fs.watch` (events) + `fs.watchFile` (stat polling) + manual polling fallback
3. New JSONL lines parsed by type:
   - `assistant` + `tool_use` → `agentToolStart` (triggers typing/reading animation)
   - `user` + `tool_result` → `agentToolDone`
   - `system` + `turn_duration` → turn completion
4. Tool names determine animation: Write/Edit/Bash → typing; Read/Grep → reading
5. Sub-agent tracking: Task tool invocations create linked child characters

### Already Works in Browser (!)

The webview-ui **already has a standalone browser mode**:
- `runtime.ts` exports `isBrowserRuntime` — detects VS Code vs browser
- `browserMock.ts` provides complete mock of asset loading for browser
- Assets served from `public/assets/` directory
- Has its own Vite dev server (`npm run dev`)
- Zero VS Code dependencies in the frontend code

### The Message Contract (What the Renderer Expects)

```typescript
// These are the messages the webview listens for:
agentCreated    { id, name, paletteIndex, hueShift }
agentToolStart  { agentId, toolId, toolName, status }
agentToolDone   { agentId, toolId }
agentClosed     { id }
agentStatus     { agentId, status: 'active'|'waiting' }
// + asset loading messages (handled by browserMock.ts)
```

### What We'd Build

```
pixel-agents (forked/extracted)
├── webview-ui/              ← KEEP: React + Canvas renderer (already standalone)
│   ├── public/assets/
│   │   ├── characters/      ← REPLACE: architecture sprites instead of office workers
│   │   ├── furniture/       ← REPLACE: site elements (terrain, scaffolding, cranes)
│   │   ├── floors/          ← REPLACE: ground types (gravel, concrete, earth)
│   │   └── walls/           ← REPLACE: site boundary, fencing
│   └── src/
│       ├── office/engine/   ← KEEP: game loop, character state machine, Z-sort, pathfinding
│       ├── data/            ← MODIFY: sprite data for architecture characters
│       └── browserMock.ts   ← KEEP: handles standalone mode
├── bridge/                  ← NEW: ~200-400 lines Node.js
│   ├── jsonl-watcher.ts     ← Watch ~/.claude/ for agent team JSONL files
│   ├── transcript-parser.ts ← ADAPT from pixel-agents (already parses Claude JSONL)
│   └── websocket-server.ts  ← Push events to browser via WebSocket
└── index.html               ← Entry point, loads webview-ui in standalone mode
```

### Effort Estimate

| Task | Effort | Dependency |
|------|--------|------------|
| Extract webview-ui as standalone | ~2 hours | None (already works) |
| Build JSONL watcher bridge | ~4-6 hours | Node.js |
| Create architecture sprite PNGs | ~4-8 hours | Art skill (Henna?) |
| Replace office layout with site | ~2-3 hours | Sprites ready |
| Wire to Agent Teams status | ~2-3 hours | Agent Teams enabled |
| Discord event forwarding | ~2-3 hours | Discord plugin |
| **Total MVP** | **~16-24 hours** | |

### Feasibility Verdict

**Very feasible.** The hard engineering (canvas renderer, animation system, file watching, JSONL parsing) is already done. We're reskinning + rewiring the data source. The browser standalone mode is practically gift-wrapped for us.

The main creative work is the sprite art — 7 architecture characters × 4 directions × 3 states = 84 frames at 16x32 pixels each. That's a focused afternoon for someone who can draw pixel art.
