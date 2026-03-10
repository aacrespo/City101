# System Architecture v6 — City101

**Version**: 6.0
**Date**: 8 March 2026
**Authors**: Andrea Crespo + Cairn Code (Claude Code)
**Status**: Proposal — pre-implementation

---

## 1. What This Document Is

This is the coordination system for City101's shared repository. It defines how Claude Code reads project context, how agent roles work, and how Andrea and Henna collaborate through git.

It replaces the previous architecture versions (v2-v5). Key lineage:
- v2-v3 designed the context routing pattern (never implemented)
- v4 added n8n automation (too complex — killed by audit)
- Audit simplified 11 roles to 4+1, 5 memory levels to 3
- v5 incorporated audit, added three-modes-of-access
- **v6** finally implements the routing pattern, adds the Modeler role back, and designs for Claude Code as the primary interface

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

## 3. Three-Layer Context Architecture

The core design principle: **Claude reads only what it needs.** A data analyst doesn't need Rhino modeling rules. A cartographer doesn't need API rate limit notes. Context is layered so each role loads the right files.

### Layer 1: Auto-loaded (every session)

These files load automatically at the start of every Claude Code session. No command needed.

```
CLAUDE.md                        ~100 lines. Project identity, current state, file map, @imports.
.claude/rules/conventions.md     Coordinate system, commit prefixes, file safety rules.
.claude/rules/data-protocol.md   Data collection rules, canonical stations, quality gates.
```

CLAUDE.md is a **router**, not an encyclopedia. It points to everything but contains almost nothing itself. The current 500-line CLAUDE.md will be split: conventions go to `.claude/rules/`, datasets go to `datasets/INVENTORY.md`, design system goes to `design_system/SPEC.md`, observations go to `observations/INDEX.md`.

`.claude/rules/` is a special Claude Code directory — every `.md` file in it is auto-loaded alongside CLAUDE.md. This is where stable, rarely-changing conventions live.

### Layer 2: Role-loaded (on command invocation)

These load when you invoke a role with a slash command. Each role specifies which additional context files to read.

```
/analyst      → reads: datasets/INVENTORY.md + LEARNINGS.md
/cartographer → reads: design_system/SPEC.md + datasets/INVENTORY.md
/modeler      → reads: 00_Workflow_v04.md (Sec 3.2) + design_system/SPEC.md
/visualizer   → reads: design_system/SPEC.md + site architecture
/builder      → reads: design_system/SPEC.md + deploy/ + narrative/
```

Utility commands:
```
/session-start → reads: CONTEXT.md + LOCKBOARD.md → recommends what to work on
/session-end   → updates: CONTEXT.md + LOCKBOARD.md → commits + pushes
/verify-data   → runs: quality checks on output files
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

### What CLAUDE.md looks like (~100 lines)

```markdown
# City101 — Geneva-Villeneuve Corridor Analysis
101km corridor through the lens of "flow of people."

## Current State
- A02 final submission: [date]
- Narrative: [current direction]
- Last session: [who did what]

## Active Tasks
See @LOCKBOARD.md

## Context Files
@CONTEXT.md — living decisions, findings, current direction
@LEARNINGS.md — accumulated pitfalls
@datasets/INVENTORY.md — all datasets with provenance
@observations/INDEX.md — findings, dead ends, theory
@design_system/SPEC.md — visual identity

## File Map
datasets/          — produced data (verified)
source/            — frozen inputs (classmate data, raw files)
visualizations/    — HTML viz + the scrollytelling site
scripts/           — processing scripts
design_system/     — visual identity spec
observations/      — research findings
output/            — staging area for agent team work
.claude/commands/  — role slash commands
.claude/rules/     — auto-loaded conventions

## Conventions
See .claude/rules/conventions.md (auto-loaded)
See .claude/rules/data-protocol.md (auto-loaded)
```

### What this means for subagents

When `/research-with-agent-team` spawns an analyst subagent, the spawn prompt includes:
1. CLAUDE.md (auto — the map)
2. `.claude/rules/*` (auto — conventions)
3. `datasets/INVENTORY.md` (role-specific — the analyst needs this)
4. `LEARNINGS.md` (role-specific — API pitfalls)

That's it. No design system, no Rhino rules, no site architecture. Clean context = faster, more focused agents.

---

## 4. Agent Roles

### 5 Production Roles

| Role | What they do | Context loaded | Commit prefix |
|------|-------------|----------------|---------------|
| **Analyst** | Data collection, API queries, dataset creation, cross-referencing | datasets/, scripts/data/, LEARNINGS.md | `[DATA]` `[FIND]` `[DEAD]` |
| **Cartographer** | QGIS maps, spatial analysis, print layouts | QGIS MCP, design_system/, datasets/ | `[MAP]` |
| **Modeler** | Rhino 3D modeling, spatial plan geometry, 3D print prep | Rhino MCP, 00_Workflow_v04.md Sec 3.2, design_system/ | `[MODEL]` |
| **Visualizer** | Leaflet maps, D3 charts, interactive HTML, the website | design_system/, scripts/viz/, site architecture | `[VIZ]` |
| **Builder** | Deployment, narrative assembly, final output packaging | design_system/, deploy/, narrative/, output/ | `[BUILD]` |

### Why Modeler is day-one

`00_Workflow_v04.md` already contains:
- Spatial plan rule and corner-point geometry
- `box()` helper function for Rhino
- LOG levels (100-500) for progressive geometry detail
- 3D print preparation guidelines
- Rhino MCP coordinate handling (LV95 → Rhino units)

This was built from last semester's modeling work. The role is ready.

### Utility commands

| Command | What it does |
|---------|-------------|
| `/session-start` | Reads CONTEXT.md + LOCKBOARD.md, recommends work |
| `/session-end` | Updates CONTEXT.md + LOCKBOARD.md, commits with `[SYNC]`, pushes |
| `/verify-data` | Runs quality checks: coordinates in range, no nulls, source attribution |

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

## 5. Two Staging Flows

### Solo session (you + Claude Code directly)

```
You open VS Code → work with Claude → files go where they belong → /session-end
```

No staging needed. You see everything happening. Write outputs directly to `datasets/`, `scripts/`, `visualizations/`, etc.

### Agent team session (you as lead + spawned subagents)

```
You spawn 3 analyst agents → they write to output/ → you verify → promote to datasets/
```

Subagents write to `output/` (staging area). The lead agent or a QA agent verifies:
- Row counts match expectations
- Coordinates valid (lat 46.1-46.6, lon 6.0-7.1)
- No null/empty required fields
- Source attribution present
- No absurd outliers

**Nothing goes to `datasets/` unverified.**

The existing `/research-with-agent-team` command already implements this pattern with canonical entity lists, output schemas, data contracts, and structured summaries.

---

## 6. Git + Collaboration

### Repository

New GitHub repo: `city101/` (public). Both Andrea and Henna clone it.

### Branch strategy

```
main                    ← stable, verified work
andrea/[task-name]      ← Andrea's working branches
henna/[task-name]       ← Henna's working branches
```

Simple. No agent-prefixed branches. No release branches. Two people, two namespaces.

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

## 7. Fresh Repo Strategy

### Migrate from current project

| What | Path | Why |
|------|------|-----|
| All datasets | `datasets/` | The core asset — 7 subdirectories |
| The website | `visualizations/site/` | Scrollytelling site + maps |
| Scripts | `scripts/` | Reusable processing |
| Workflow doc | `00_Workflow_v04.md` | Rhino rules, scale conventions |
| Existing commands | `.claude/commands/` | research-with-agent-team, build-with-agent-team |

### Create new

| What | Path | Why |
|------|------|-----|
| Router CLAUDE.md | `CLAUDE.md` | ~100 lines, replaces current 500-line version |
| Context | `CONTEXT.md` | From current, updated to today |
| Learnings | `LEARNINGS.md` | From current |
| Lockboard | `LOCKBOARD.md` | New — coordination |
| Design spec | `design_system/SPEC.md` | Extracted from current CLAUDE.md |
| Dataset inventory | `datasets/INVENTORY.md` | Extracted from current CLAUDE.md |
| Observations | `observations/INDEX.md` | Findings + dead ends + theory |
| Auto-loaded rules | `.claude/rules/conventions.md` | Extracted from current CLAUDE.md |
| Auto-loaded rules | `.claude/rules/data-protocol.md` | Extracted from current CLAUDE.md |
| Role commands | `.claude/commands/analyst.md` etc. | 5 roles + 3 utilities |
| Agent definitions | `.claude/agents/` | QA subagent YAML |

### Handle carefully

| What | Approach |
|------|----------|
| `source/` (classmate data) | Selective. Git LFS for large files, .gitignore the rest |
| `CITY101_WORKING.qgz` | LFS tracked, one owner at a time (LOCKBOARD) |

### Don't migrate

`archive/`, old handoffs, superseded files, session-specific outputs.

---

## 8. Henna Onboarding

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

- Subagent system, memory hierarchies, role definitions
- The architecture docs (this document)
- Scheduled tasks, `/loop`

The system works transparently. She opens the repo, Claude Code reads CLAUDE.md and the rules automatically, and she can just work. The slash commands are there if she wants them (`/analyst`, `/session-start`), but they're optional.

### Key question for her

"What datasets have you already produced? What's in your project folder?"

We need to map her existing work into the repo structure.

---

## 9. Automation (deferred)

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

## 10. Implementation Timeline

| Step | Time | Who |
|------|------|-----|
| Create GitHub repo + LFS + .gitattributes + .gitignore | 15 min | Andrea |
| Create CLAUDE.md (router) + CONTEXT.md + LEARNINGS.md + LOCKBOARD.md | 45 min | Claude Code |
| Extract design_system/SPEC.md + datasets/INVENTORY.md + observations/INDEX.md | 30 min | Claude Code |
| Write slash commands (5 roles + 3 utilities) | 45 min | Claude Code |
| Migrate datasets/, scripts/, visualizations/site/, 00_Workflow | 20 min | Claude Code |
| Initial commit + push | 5 min | Andrea |
| Henna clones + tests full loop | 15 min | Henna |

**Total: ~3 hours** (mostly Claude Code doing the work while Andrea reviews)

---

## 11. Verification Checklist

After implementation, verify:

- [ ] Push a commit → appears on GitHub
- [ ] Henna clones → can read everything, LOCKBOARD shows current state
- [ ] Run `/session-end` → produces clean `[SYNC]` commit with CONTEXT.md update
- [ ] Both push to their own branches → no conflicts
- [ ] Spawn a test subagent → it reads only the files its role specifies
- [ ] `/analyst` loads INVENTORY.md but NOT design_system/SPEC.md
- [ ] `/modeler` loads 00_Workflow_v04.md but NOT LEARNINGS.md

---

## Appendix A: Version History

| Version | Date | Key changes |
|---------|------|-------------|
| v2 | Feb 2026 | 10 roles, context routing design (never implemented), 5 memory levels |
| v3 | Feb 2026 | 8 agent slots, n8n as "break glass," assignment-specific sections |
| v4 | Feb 2026 | 11 roles, full n8n layer (Docker + 7 workflows), 15 commit prefixes |
| Audit | Feb 2026 | Independent review: kill n8n, 4+1 roles, 3 memory levels, 7 prefixes |
| v5 | Mar 2026 | Incorporated audit, three modes of access, filesystem MCP |
| **v6** | Mar 2026 | Three-layer context, 5+utility roles, Claude Code primary, fresh repo |

### What stayed constant across all versions
- Context routing per role (different roles, different files)
- CLAUDE.md as router, not encyclopedia
- Lockboard for coordination
- Commit prefix convention
- Output staging for agent teams

### What was correctly simplified
- n8n automation → killed (too complex for 2 people)
- 11 roles → 5 + utilities (right-sized)
- 5 memory levels → 3 layers (cleaner)
- Agent-prefixed branches → main + human/* (simpler)

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

For systematic data collection, Python scripts are better than Chat's built-in because they're scriptable and repeatable.
