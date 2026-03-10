# System Architecture v7 — City101

**Version**: 7.0
**Date**: 9 March 2026
**Authors**: Andrea Crespo + Cairn Code (Claude Code)
**Status**: Proposal — pre-implementation

---

## 1. What This Document Is

This is the coordination system for City101's shared repository. It defines how Claude Code reads project context, how agent roles work, how tools and workflows operate, and how Andrea and Henna collaborate through git.

It builds on v6 (three-layer context, 5+utility roles, fresh repo) and adds the **WAT-inspired execution layer**: reusable tools, explicit workflows (SOPs), and a controlled self-improvement loop.

### Key lineage
- v2-v3: context routing pattern (never implemented)
- v4: n8n automation (too complex — killed by audit)
- Audit: simplified 11 roles to 4+1, 5 memory levels to 3
- v5: incorporated audit, three-modes-of-access
- v6: three-layer context, 5+utility roles, Claude Code primary, fresh repo
- **v7**: adds WAT execution layer (tools + workflows + self-improvement), tightens autonomy rules

---

## 2. The Interface: Claude Code in VS Code

Claude Code is the primary working interface for both Andrea and Henna. It runs in the VS Code integrated terminal.

**What you get with Claude Code:**
- Same Claude brain as Chat desktop
- Full MCP access: Rhino, QGIS, Chrome, OSM, filesystem
- Subagent teams (parallel workers for research sprints)
- Slash commands (`/analyst`, `/modeler`, `/session-start`, etc.)
- Native git integration
- File browser, diff view, extensions (via VS Code)

**What you don't need anymore:**
- Chat desktop for MCP work (Code has the same access)
- Chat browser for project knowledge (CLAUDE.md provides it)
- Handoff documents between sessions (git log + CONTEXT.md replace them)

Chat browser (claude.ai) remains available as a fallback for quick questions when VS Code isn't open.

---

## 3. The Four Layers

v6 had three context layers (auto-loaded, role-loaded, reference). v7 keeps those and adds a fourth: the **execution layer** — tools and workflows that make operations repeatable and reliable.

### Why this matters

When Claude handles every step by reasoning through it fresh, accuracy drops. If each step is 90% accurate, five steps in sequence = 59% success. By wrapping repeatable operations in deterministic scripts, Claude orchestrates instead of improvises. The context layers tell Claude *what to know*. The execution layer tells Claude *how to do things reliably*.

### Layer 1: Auto-loaded context (every session)

These files load automatically at the start of every Claude Code session. No command needed.

```
CLAUDE.md                        ~100 lines. Project identity, current state, file map, @imports.
.claude/rules/conventions.md     Coordinate system, commit prefixes, file safety rules.
.claude/rules/data-protocol.md   Data collection rules, canonical stations, quality gates.
.claude/rules/tool-protocol.md   How to use tools and workflows. Self-improvement rules.
```

CLAUDE.md is a **router**, not an encyclopedia. It points to everything but contains almost nothing itself.

`.claude/rules/` is a special Claude Code directory — every `.md` file in it is auto-loaded alongside CLAUDE.md. This is where stable, rarely-changing conventions live.

### Layer 2: Role-loaded context (on command invocation)

These load when you invoke a role with a slash command. Each role specifies which additional context files to read AND which workflows are relevant.

```
/analyst      → reads: datasets/INVENTORY.md + LEARNINGS.md
              → workflows: data-collection, data-verification
/cartographer → reads: design_system/SPEC.md + datasets/INVENTORY.md
              → workflows: map-generation, map-export
/modeler      → reads: 00_Workflow_v04.md (Sec 3.2) + design_system/SPEC.md
              → workflows: rhino-modeling
/visualizer   → reads: design_system/SPEC.md + site architecture
              → workflows: chart-generation, site-update
/builder      → reads: design_system/SPEC.md + deploy/ + narrative/
              → workflows: site-deploy, narrative-assembly
```

Utility commands:
```
/session-start → reads: CONTEXT.md + LOCKBOARD.md → recommends what to work on
/session-end   → updates: CONTEXT.md + LOCKBOARD.md → commits + pushes
/verify-data   → runs: workflows/data-verification.md
```

### Layer 3: Reference files (loaded on demand)

These are the detailed context files. Not auto-loaded. Read when a role command says to, or when needed.

| File | What it contains | Updated when |
|------|-----------------|--------------|
| `CONTEXT.md` | Living state, decisions, what just changed | Every /session-end |
| `LEARNINGS.md` | Accumulated pitfalls, API gotchas | When discoveries happen |
| `LOCKBOARD.md` | Who's doing what right now | When focus shifts |
| `datasets/INVENTORY.md` | Dataset catalog: rows, columns, provenance | When data changes |
| `observations/INDEX.md` | Findings, dead ends, theoretical references | Per assignment |
| `design_system/SPEC.md` | Palette, typography, CSS variables | Rarely |
| `00_Workflow_v04.md` | Scale conventions, Rhino rules, LOI/LOG/LOD | Rarely |

### Layer 4: Execution (tools + workflows)

This is what v7 adds. Two directories that make operations repeatable:

```
workflows/       Markdown SOPs — step-by-step procedures that reference specific tools
tools/           Python and shell scripts — deterministic execution of repeatable operations
```

**The relationship:** A workflow says *what to do and in what order*. A tool *does one thing reliably*. Claude's job is to read the workflow, call the tools in sequence, handle edge cases, and ask when something is unclear.

---

## 4. Tools

### What a tool is

A tool is a self-contained script that does **one repeatable operation**. It takes defined inputs, produces defined outputs, and doesn't require Claude to reason about the implementation each time.

### Directory structure

```
tools/
├── data/
│   ├── fetch_sbb_timetable.py      Queries transport.opendata.ch for a station
│   ├── fetch_google_places.py       Queries Google Places API with rate limiting
│   ├── fetch_shared_mobility.py     Queries sharedmobility.ch
│   ├── convert_coordinates.py       WGS84 ↔ LV95 conversion (pyproj)
│   └── verify_dataset.py            Row counts, coordinate ranges, null checks, source attribution
├── maps/
│   ├── load_base_layers.py          Lake, train lines, communes — standard Leaflet setup
│   ├── apply_design_system.py       Dark bg, gold accent, DM Sans, CSS variables
│   └── export_map.py                300 DPI PDF + 150 DPI PNG with standard settings
├── git/
│   ├── session_end.sh               Updates CONTEXT.md, commits [SYNC], pushes. Never force-pushes.
│   ├── new_branch.sh                Creates andrea/ or henna/ branch after checking LOCKBOARD
│   └── safe_push.sh                 Pushes with pre-flight checks. Never force-pushes. Never deletes.
└── util/
    ├── csv_to_geojson.py            Standard conversion with coordinate validation
    └── merge_datasets.py            Merge with duplicate detection and conflict reporting
```

### Tool rules

1. **Check `tools/` before building anything new.** If a tool exists for the task, use it.
2. **Each tool does one thing.** `fetch_sbb_timetable.py` fetches timetables. It doesn't also verify the data or convert coordinates.
3. **Tools are deterministic.** Same input → same output. No randomness, no LLM calls inside tools.
4. **Tools handle their own errors.** Rate limits, timeouts, malformed responses — the script handles them and returns a clear error message, not a stack trace.
5. **Tools never delete files.** They create new files or append. Deletion is a human action.
6. **Tools log what they did.** Every tool prints: what it received, what it did, what it produced, and anything unexpected.

### Safety rules for git tools

Git tools (`tools/git/`) have hardcoded safety:
- **Never** `--force` push
- **Never** delete branches
- **Never** modify history (`rebase`, `amend` on pushed commits)
- **Never** commit to `main` directly (only via PR merge)
- **Always** check LOCKBOARD before branch operations
- **Always** pull before push

These are in the script logic, not left to Claude's judgment.

---

## 5. Workflows (SOPs)

### What a workflow is

A workflow is a markdown file that defines a **complete procedure**: what you're trying to do, what inputs you need, which tools to run in what order, what the output should look like, and what to do when things go wrong.

Think of it as a recipe. Claude is the cook — it follows the recipe, adapts to what's in the fridge, and asks the chef (you) when something is unclear.

### Directory structure

```
workflows/
├── data-collection.md          How to collect data from an API source
├── data-verification.md        How to verify a dataset before promoting to datasets/
├── map-generation.md           How to create a new map (Leaflet or QGIS)
├── map-export.md               How to export maps for print and web
├── site-update.md              How to add a section or map to the scrollytelling site
├── chart-generation.md         How to create a D3/HTML visualization
├── narrative-assembly.md       How to compile narrative sections into deliverables
├── site-deploy.md              How to deploy the site
├── rhino-modeling.md           How to model in Rhino via MCP
├── session-management.md       How session-start and session-end work
└── new-dataset-integration.md  How to integrate a new classmate dataset
```

### Workflow template

Every workflow follows the same structure:

```markdown
# Workflow: [Name]

## Objective
What this workflow produces.

## When to use
The trigger — when should Claude follow this workflow?

## Required inputs
What must exist before starting.

## Steps
1. [Action] — using `tools/[script]`
2. [Action] — using `tools/[script]`
3. [Decision point] — if X, do Y; if Z, ask Andrea/Henna
...

## Expected output
What gets produced, where it goes, what format.

## Edge cases
- [Situation]: [What to do]
- [Situation]: [What to do]

## History
- [Date]: Created
- [Date]: Updated — [what changed and why]
```

### Workflow rules

1. **Follow the workflow.** If a workflow exists for your task, follow it step by step. Don't skip steps.
2. **Ask when the workflow doesn't cover your situation.** Don't improvise around gaps — flag them.
3. **Never create or overwrite a workflow without asking.** Propose the change, explain why, wait for approval.
4. **Never delete a workflow.** If it's obsolete, propose marking it as deprecated.
5. **Workflows reference tools by name.** "Run `tools/data/verify_dataset.py`" — not "verify the dataset."

---

## 6. The Self-Improvement Loop

This is how the system gets better over time without getting worse.

### The loop

```
1. Something fails or works poorly
2. Claude identifies the root cause
3. Claude proposes a fix (tool change, workflow update, or both)
4. Andrea or Henna approves or adjusts
5. Claude implements the approved fix
6. Claude verifies the fix works
7. The system is now stronger for next time
```

### Rules

**Always ask before:**
- Creating a new tool
- Modifying an existing tool
- Creating, updating, or deprecating a workflow
- Changing anything in `.claude/rules/`
- Changing CLAUDE.md

**What Claude CAN do without asking:**
- Retry a failed tool with adjusted parameters (same tool, same intent)
- Read any project file to diagnose a problem
- Run verification tools on output
- Add entries to LEARNINGS.md (append-only, never delete)

**How to propose a change:**
```
"[Tool/Workflow] `tools/data/fetch_sbb_timetable.py` failed because the API now
requires a date parameter. I'd like to:
1. Add a `date` parameter (defaults to today)
2. Update `workflows/data-collection.md` step 3 to mention the date requirement
3. Add a note to LEARNINGS.md about the API change

Approve?"
```

Short, specific, actionable. Not a paragraph of reasoning.

### What gets logged where

| What happened | Where it goes |
|--------------|---------------|
| API behavior change, rate limit discovery | LEARNINGS.md |
| Tool fix (after approval) | The tool itself + History section of relevant workflow |
| New edge case | Edge cases section of relevant workflow |
| Decision about approach | CONTEXT.md (via /session-end) |

---

## 7. Agent Roles

### 5 Production Roles

| Role | What they do | Context loaded | Workflows used | Commit prefix |
|------|-------------|----------------|----------------|---------------|
| **Analyst** | Data collection, API queries, dataset creation, cross-referencing | datasets/, scripts/data/, LEARNINGS.md | data-collection, data-verification | `[DATA]` `[FIND]` `[DEAD]` |
| **Cartographer** | QGIS maps, spatial analysis, print layouts | QGIS MCP, design_system/, datasets/ | map-generation, map-export | `[MAP]` |
| **Modeler** | Rhino 3D modeling, spatial plan geometry, 3D print prep | Rhino MCP, 00_Workflow_v04.md Sec 3.2, design_system/ | rhino-modeling | `[MODEL]` |
| **Visualizer** | Leaflet maps, D3 charts, interactive HTML, the website | design_system/, scripts/viz/, site architecture | chart-generation, site-update | `[VIZ]` |
| **Builder** | Deployment, narrative assembly, final output packaging | design_system/, deploy/, narrative/, output/ | site-deploy, narrative-assembly | `[BUILD]` |

### Why Modeler is day-one

`00_Workflow_v04.md` already contains:
- Spatial plan rule and corner-point geometry
- `box()` helper function for Rhino
- LOG levels (100-500) for progressive geometry detail
- 3D print preparation guidelines
- Rhino MCP coordinate handling (LV95 → Rhino units)

### Utility commands

| Command | What it does | Workflow |
|---------|-------------|----------|
| `/session-start` | Reads CONTEXT.md + LOCKBOARD.md, recommends work | session-management.md |
| `/session-end` | Updates CONTEXT.md + LOCKBOARD.md, commits with `[SYNC]`, pushes | session-management.md |
| `/verify-data` | Runs quality checks on output files | data-verification.md |

### 8 Commit prefixes

| Prefix | Used by | Meaning |
|--------|---------|---------|
| `[DATA]` | Analyst | New or updated dataset |
| `[FIND]` | Analyst | Discovery worth noting |
| `[DEAD]` | Analyst | Dead end documented |
| `[MAP]` | Cartographer | Map or spatial output |
| `[VIZ]` | Visualizer | Visualization or chart |
| `[MODEL]` | Modeler | 3D model or geometry |
| `[BUILD]` | Builder | Deployment or packaging |
| `[SYNC]` | session-end | Context/lockboard update |

---

## 8. Two Staging Flows

### Solo session (you + Claude Code directly)

```
You open VS Code → work with Claude → files go where they belong → /session-end
```

No staging needed. You see everything happening. Write outputs directly to `datasets/`, `scripts/`, `visualizations/`, etc.

### Agent team session (you as lead + spawned subagents)

```
You spawn 3 analyst agents → they write to output/ → you verify → promote to datasets/
```

Subagents write to `output/` (staging area). The lead agent or a QA agent runs `workflows/data-verification.md`:
- Row counts match expectations
- Coordinates valid (lat 46.1-46.6, lon 6.0-7.1)
- No null/empty required fields
- Source attribution present
- No absurd outliers

**Nothing goes to `datasets/` unverified.**

### How tools fit into staging

Subagents use the same tools from `tools/`. This means:
- API calls use the same rate limiting every time
- Coordinate conversions are identical across agents
- Verification runs the same checks regardless of who triggers it

Consistency from shared tools, not from hoping each agent implements things the same way.

---

## 9. Git + Collaboration

### Repository

New GitHub repo: `city101/` (public). Both Andrea and Henna clone it.

### Branch strategy

```
main                    ← stable, verified work
andrea/[task-name]      ← Andrea's working branches
henna/[task-name]       ← Henna's working branches
```

Simple. No agent-prefixed branches. No release branches. Two people, two namespaces.

### Merging Henna's work

When setting up the fresh repo, we need to account for Henna's existing work:

1. **Ask Henna**: What datasets, scripts, QGIS projects, and Claude configs does she have?
2. **Map her structure to ours**: Where does her work fit in the repo layout?
3. **Merge datasets**: Deduplicate, verify coordinates, reconcile any overlaps
4. **Preserve her CLAUDE.md insights**: If she has project knowledge, extract and merge into CONTEXT.md or LEARNINGS.md

The fresh repo starts with the union of both people's verified work.

### LOCKBOARD.md

A plain markdown file tracking who's doing what right now:

```markdown
# Lockboard

## Andrea
- Working on: temporal frequency deep-dive
- Branch: andrea/temporal-v2
- Since: 8 March 2026

## Henna
- Working on: thermal comfort overlay
- Branch: henna/thermal
- Since: 7 March 2026

## Blocked
- (nothing currently)
```

Updated by `/session-start` (read) and `/session-end` (write). Prevents duplicate work.

### Binary files (Git LFS)

These are tracked with Git LFS (Large File Storage):

```
*.qgz       QGIS projects
*.3dm       Rhino files
*.blend     Blender files
*.pdf       Print outputs
*.png       Map exports
*.jpg       Photos
*.tif       Raster data
*.gpkg      GeoPackages
```

Rule: QGIS project (`CITY101_WORKING.qgz`) has **one owner at a time**. Check LOCKBOARD.md before touching it.

---

## 10. Fresh Repo Structure

### Full directory layout

```
city101/
├── CLAUDE.md                          ← Router (~100 lines)
├── CONTEXT.md                         ← Living project state
├── LEARNINGS.md                       ← Accumulated pitfalls
├── LOCKBOARD.md                       ← Who's doing what
├── 00_Workflow_v04.md                 ← Scale conventions, Rhino rules
│
├── datasets/                          ← Verified production data
│   ├── INVENTORY.md                   ← Dataset catalog with provenance
│   ├── corridor_analysis/
│   ├── ev_charging/
│   ├── remote_work/
│   ├── transit/
│   ├── stations/
│   ├── 24h_venues/
│   └── zurich_comparison/
│
├── source/                            ← Frozen inputs (classmate data, raw files)
│
├── tools/                             ← Deterministic scripts (NEW in v7)
│   ├── data/                          ← API fetches, coordinate conversion, verification
│   ├── maps/                          ← Base layers, design system, export
│   ├── git/                           ← Session management, branch safety
│   └── util/                          ← Format conversion, merge, dedup
│
├── workflows/                         ← Step-by-step SOPs (NEW in v7)
│   ├── data-collection.md
│   ├── data-verification.md
│   ├── map-generation.md
│   ├── map-export.md
│   ├── site-update.md
│   ├── chart-generation.md
│   ├── narrative-assembly.md
│   ├── site-deploy.md
│   ├── rhino-modeling.md
│   ├── session-management.md
│   └── new-dataset-integration.md
│
├── visualizations/                    ← HTML viz + the scrollytelling site
│   └── site/
├── scripts/                           ← Ad-hoc processing scripts (not tools)
├── design_system/
│   └── SPEC.md                        ← Visual identity
├── observations/
│   └── INDEX.md                       ← Findings, dead ends, theory
├── output/                            ← Staging area for agent team work
│
├── .claude/
│   ├── commands/                      ← Slash commands (5 roles + 3 utilities)
│   ├── rules/
│   │   ├── conventions.md             ← Coordinates, commits, file safety
│   │   ├── data-protocol.md           ← Collection rules, canonical stations
│   │   └── tool-protocol.md           ← How to use tools + workflows (NEW in v7)
│   └── agents/                        ← QA subagent definitions
│
├── .gitattributes                     ← LFS tracking rules
└── .gitignore
```

### scripts/ vs tools/ — what's the difference?

| | `tools/` | `scripts/` |
|--|---------|-----------|
| **Purpose** | Reusable building blocks called by workflows | One-off or exploratory processing |
| **Structure** | One function, defined inputs/outputs, error handling | Monolithic, end-to-end |
| **Called by** | Workflows, slash commands, other tools | Humans or Claude directly |
| **Stability** | High — changes require approval | Low — write and discard freely |
| **Examples** | `fetch_sbb_timetable.py`, `verify_dataset.py` | `explore_ridership_patterns.py`, `quick_merge.py` |

Rule of thumb: if you've done it twice, it should be a tool. If you're exploring, it's a script.

### What to migrate from current project

| What | Destination | Notes |
|------|------------|-------|
| All datasets | `datasets/` | The core asset |
| The website | `visualizations/site/` | Scrollytelling site + maps |
| Reusable scripts | `tools/` | Extract repeatable parts from current `scripts/` |
| Exploratory scripts | `scripts/` | Keep as-is |
| Workflow doc | `00_Workflow_v04.md` | Rhino rules, scale conventions |
| Existing commands | `.claude/commands/` | research-with-agent-team, build-with-agent-team |
| Henna's datasets | `datasets/` | After verification and dedup |
| Henna's insights | `LEARNINGS.md` / `CONTEXT.md` | If she has project knowledge |

### Don't migrate

`archive/`, old handoffs, superseded files, session-specific outputs.

---

## 11. The tool-protocol.md (auto-loaded rule)

This is what goes in `.claude/rules/tool-protocol.md` — loaded every session, so Claude always knows how to work with tools and workflows.

```markdown
# Tool and Workflow Protocol

## Before doing any repeatable operation
1. Check if a workflow exists in `workflows/` for this task
2. Check if tools exist in `tools/` for the steps
3. If both exist: follow the workflow, use the tools
4. If workflow exists but tool is missing: ask before creating the tool
5. If neither exists: do the task directly, then propose a tool/workflow if it's likely to recur

## When something fails
1. Read the full error
2. Diagnose the root cause
3. Propose a fix — state what you'd change in which file and why
4. Wait for approval
5. Implement the fix
6. Verify it works
7. Update the workflow's History section

## Never do without asking
- Create, modify, or delete any tool
- Create, modify, or deprecate any workflow
- Change any file in .claude/rules/
- Change CLAUDE.md

## You can do without asking
- Retry a failed tool with adjusted parameters
- Read any project file to diagnose a problem
- Run verification tools on data in output/
- Append to LEARNINGS.md
```

---

## 12. Henna Onboarding

### What she installs

1. **VS Code** (probably has it already)
2. **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
3. **Git LFS** (`brew install git-lfs && git lfs install`)

### Her daily workflow

```
1. Open VS Code in the repo folder
2. git pull
3. Check LOCKBOARD.md (or ask Claude: "what should I work on?")
4. Work on branch henna/[task-name]
5. Run /session-end when done (or commit + push manually)
```

### What she doesn't need to understand

- The WAT execution layer, self-improvement loop
- Subagent system, memory hierarchies, role definitions
- The architecture docs (this document)
- Scheduled tasks, `/loop`

The system works transparently. She opens the repo, Claude Code reads CLAUDE.md and the rules automatically, and she can just work. The slash commands are there if she wants them (`/analyst`, `/session-start`), but they're optional. The tools and workflows work behind the scenes — Claude uses them automatically when it follows a role command.

### Key question for her

"What datasets have you already produced? What's in your project folder? Do you have a CLAUDE.md or project knowledge?"

We need to map her existing work into the repo structure before the initial commit.

---

## 13. Automation (deferred)

### /loop

Session-scoped repeating prompt. Runs every N minutes while the terminal is open. Dies on close.

**Week 1**: Don't use. Manual `/session-start` + `/session-end`.
**Week 2+**: If lockboard checking feels annoying, add `/loop 30m check LOCKBOARD.md`.

### Scheduled tasks

Persistent, auto-expire after 3 days. Only run when the app is open.

**Week 1**: Don't use.
**Later**: If needed for monitoring.

### Notifications (if wanted)

GitHub Actions (free, always-on) with a Discord webhook. 15-line YAML file. Sends a message when someone pushes.

---

## 14. Implementation Timeline

| Step | Time | Who |
|------|------|-----|
| Create GitHub repo + LFS + .gitattributes + .gitignore | 15 min | Andrea |
| Create CLAUDE.md (router) + CONTEXT.md + LEARNINGS.md + LOCKBOARD.md | 45 min | Claude Code |
| Extract design_system/SPEC.md + datasets/INVENTORY.md + observations/INDEX.md | 30 min | Claude Code |
| Write slash commands (5 roles + 3 utilities) | 45 min | Claude Code |
| Create `tools/` directory with initial tools | 60 min | Claude Code |
| Create `workflows/` directory with initial SOPs | 45 min | Claude Code |
| Write `.claude/rules/tool-protocol.md` | 15 min | Claude Code |
| Migrate datasets/, scripts/, visualizations/site/, 00_Workflow | 20 min | Claude Code |
| Coordinate with Henna — merge her work | ? | Andrea + Henna |
| Initial commit + push | 5 min | Andrea |
| Henna clones + tests full loop | 15 min | Henna |

**Total: ~4-5 hours** (mostly Claude Code doing the work while Andrea reviews)

The Henna merge step is the unknown — depends on what she has.

---

## 15. Verification Checklist

After implementation, verify:

- [ ] Push a commit → appears on GitHub
- [ ] Henna clones → can read everything, LOCKBOARD shows current state
- [ ] Run `/session-end` → produces clean `[SYNC]` commit with CONTEXT.md update
- [ ] Both push to their own branches → no conflicts
- [ ] Spawn a test subagent → it reads only the files its role specifies
- [ ] `/analyst` loads INVENTORY.md but NOT design_system/SPEC.md
- [ ] `/modeler` loads 00_Workflow_v04.md but NOT LEARNINGS.md
- [ ] Run `tools/data/verify_dataset.py` on a known-good dataset → passes
- [ ] Run `tools/data/verify_dataset.py` on a bad dataset → fails with clear error
- [ ] A workflow references tools by exact path → tools exist at those paths
- [ ] Self-improvement loop: break something, Claude proposes fix, waits for approval

---

## Appendix A: Version History

| Version | Date | Key changes |
|---------|------|-------------|
| v2 | Feb 2026 | 10 roles, context routing design (never implemented), 5 memory levels |
| v3 | Feb 2026 | 8 agent slots, n8n as "break glass," assignment-specific sections |
| v4 | Feb 2026 | 11 roles, full n8n layer (Docker + 7 workflows), 15 commit prefixes |
| Audit | Feb 2026 | Independent review: kill n8n, 4+1 roles, 3 memory levels, 7 prefixes |
| v5 | Mar 2026 | Incorporated audit, three modes of access, filesystem MCP |
| v6 | Mar 2026 | Three-layer context, 5+utility roles, Claude Code primary, fresh repo |
| **v7** | Mar 2026 | WAT execution layer (tools + workflows + self-improvement), ask-first autonomy |

### What stayed constant across all versions
- Context routing per role (different roles, different files)
- CLAUDE.md as router, not encyclopedia
- Lockboard for coordination
- Commit prefix convention
- Output staging for agent teams

### What was correctly simplified
- n8n automation → killed (too complex for 2 people)
- 11 roles → 5 + utilities (right-sized)
- 5 memory levels → 3 context layers (cleaner)
- Agent-prefixed branches → main + human/* (simpler)

### What v7 adds
- Deterministic execution via `tools/` — repeatable operations don't rely on Claude's reasoning
- Explicit SOPs via `workflows/` — procedures are documented, not reinvented
- Self-improvement loop with human approval — the system learns but doesn't drift
- `tool-protocol.md` auto-loaded rule — Claude always knows how to use the execution layer

---

## Appendix B: MCP Tools Available in Claude Code

| MCP | What it does |
|-----|-------------|
| **Rhino** | Create/modify 3D geometry, boolean ops, viewport capture |
| **QGIS** | Load/query layers, execute processing, render maps |
| **Chrome** | Browser automation, page reading, screenshots |
| **OSM** | Geocoding, routing, nearby places, area profiles |
| **Filesystem** | Read/write/edit files in the project |
| **Preview** | Start dev servers, screenshot, inspect, click, fill |

All available to both Andrea and Henna through Claude Code.

---

## Appendix C: Google Places Access

| Method | Where | Best for |
|--------|-------|----------|
| Built-in Google Places | Chat (claude.ai) only | Quick searches |
| Chrome MCP | Claude Code | Interactive browsing, Maps extraction |
| WebSearch + WebFetch | Claude Code | General web research |
| Python script with API key | Claude Code | Batch operations (49 stations) |

For systematic data collection, Python scripts (now in `tools/data/`) are better than Chat's built-in because they're scriptable and repeatable.

---

## Appendix D: WAT Inspiration Credit

The tools + workflows + self-improvement loop design is inspired by the **WAT framework** (Workflows, Agents, Tools). The core insight adopted: separate probabilistic reasoning (Claude) from deterministic execution (scripts). Claude orchestrates; tools execute.

What we kept from WAT:
- Tools as reusable, testable scripts
- Workflows as explicit SOPs
- The self-improvement loop

What we adapted:
- Added human approval gate (WAT allows more agent autonomy)
- Integrated with role-based context routing (WAT has flat context)
- Added staging/verification flow (WAT trusts tool output directly)
- Added multi-person coordination (WAT is single-user)
