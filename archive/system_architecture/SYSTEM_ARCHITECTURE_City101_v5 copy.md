# SYSTEM ARCHITECTURE — City101 Multi-Agent Workflow
### v5.0
**Date**: 2026-03-08
**Client**: Andrea Crespo & Henna Rafik — EPFL BA6 Studio Huang
**Systems Architect**: Cairn (Claude Opus 4.6)
**Project**: City101 Geneva–Villeneuve Corridor Analysis
**Semester**: Spring 2026, 14 weeks (W1 = 16 Feb → W14 = 26 May)
**Current position**: Week 3

**Lineage**: v4 spec (2026-03-07) → independent audit (2026-03-08) → this document incorporates both, plus architectural discoveries from implementation planning session.

---

## 0. THE PROBLEM THIS SOLVES

Andrea and Henna work independently, produce the same datasets, and discover the duplication too late. Multiple Claude instances and two humans have no shared visibility into what's in progress. Context evaporates between sessions. Quality requires rework. The semester structure — with overlapping parallel assignments — intensifies all of the above.

This document specifies a single system that coordinates all agents, humans, tools, and deliverables through one git repository, with no external dependencies beyond GitHub (free).

---

## 1. THE KEY INSIGHT: ONE REPO, MULTIPLE INTERFACES

Every Claude interface — Chat, Code, Cowork — can read and write from the same repository. The repo is the shared brain. The interfaces are just different ways of interacting with it.

```
┌──────────────────────────────────────────────────────────┐
│                    GITHUB (remote copy)                    │
│                  The meeting point. Free.                  │
│           Andrea pushes ←→ Henna pulls (and vice versa)   │
└──────────────────┬───────────────────┬───────────────────┘
                   │ git push/pull     │ git push/pull
                   ▼                   ▼
        ┌──────────────────┐ ┌──────────────────┐
        │  Andrea's Mac    │ │  Henna's Mac     │
        │  ~/City101/      │ │  ~/City101/      │
        │  (local repo)    │ │  (local repo)    │
        └──────────────────┘ └──────────────────┘
              ▲ ▲ ▲                  ▲ ▲ ▲
              │ │ │                  │ │ │
              │ │ └── Chat+MCP      │ │ └── Chat+MCP
              │ └──── Code/Cowork   │ └──── Code/Cowork
              └────── Human (git)   └────── Human (git)
```

### 1.1 Three Modes of Access

| Mode | Interface | Reads repo | Writes repo | Git commands | Best for |
|------|-----------|-----------|-------------|-------------|----------|
| **Chat (browser)** | claude.ai | Via `web_fetch` from GitHub raw URLs | No | No | Quick questions, web search, when away from desktop |
| **Chat (desktop + MCP)** | Claude Desktop with filesystem MCP | Direct file read | Direct file write | Human pastes commands Claude drafts | Thinking + organizing: updating CLAUDE.md, lockboard, session logs, narrative planning |
| **Code / Cowork** | Terminal or Cowork tab | Direct file read | Direct file write | Native git (automatic) | Execution: scripts, data processing, building outputs, heavy iteration loops |

**The distinction is not intelligence — all modes run the same model (Opus 4.6 on Max).** The distinction is context access and workflow shape.

- **Chat + MCP** = the "big brain with hands" — it has web search, Google Places, project knowledge (stable docs), AND filesystem access. It thinks deeply and organizes.
- **Code / Cowork** = the "fast hands" — it iterates on scripts, runs commands, handles git natively. It builds.
- **Browser Chat** = the "brain in a box" — it can read from GitHub and think, but can't touch the filesystem. Use when away from the desktop app.

### 1.2 Context Sources Per Mode

| Context source | Chat (browser) | Chat (desktop+MCP) | Code / Cowork |
|---------------|----------------|--------------------|----|
| CLAUDE.md | Fetched from GitHub URL | Read from filesystem | Read from filesystem (automatic) |
| LOCKBOARD.md | Fetched from GitHub URL | Read from filesystem | Read from filesystem |
| Datasets, scripts, outputs | Not directly (can fetch individual files from GitHub) | Full filesystem access | Full filesystem access |
| Project knowledge (claude.ai) | Yes | Yes | No |
| Web search | Yes | Yes | No |
| Google Places | Yes | Yes | No |
| MCP tools (QGIS, Rhino, Chrome, OSM) | No | Yes (if MCP connected) | Yes (if MCP connected) |
| Conversation history | Yes (current chat) | Yes (current chat) | Per-session only |
| Auto-memory (persistent) | Yes | Yes | Yes (CLAUDE.md + memory files) |

### 1.3 How Chat Gets Live State

**Project knowledge** (uploaded files in claude.ai) = stable reference documents that rarely change. Course briefs, safety rules, workflow doc.

**GitHub fetch** (via project instructions) = live state. Project instructions tell Chat:

> *"At the start of every conversation, fetch the current CLAUDE.md from `https://raw.githubusercontent.com/[user]/city101/main/CLAUDE.md`. If relevant, also fetch LOCKBOARD.md."*

This means every Chat session reads the latest state without manual uploads. When Code or Chat+MCP updates CLAUDE.md and pushes, the next Chat session sees it automatically.

### 1.4 Filesystem MCP Setup

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y", "@modelcontextprotocol/server-filesystem",
        "/Users/andreacrespo/City101",
        "/Users/andreacrespo/CLAUDE"
      ]
    }
  }
}
```

This gives Chat (on desktop) clean file read/write access to the repo and the working folder. Scoped — can't access anything outside those paths. Replaces the QGIS MCP hack for file operations.

Git commands remain human-executed. Chat drafts the exact commands; the human pastes them into terminal. Three commands per session: `git pull` (start), `git add . && git commit -m "..."` (end), `git push` (end).

---

## 2. MEMORY LAYER

### 2.1 Three Operational Levels

| Level | What | Updated | By whom |
|-------|------|---------|---------|
| **Git log** | Every commit message with prefix | Real-time | Automatic (every commit) |
| **Session logs** | Per-session summary: what was done, decisions made, dead ends found | End of session | Session-end skill or manual |
| **CLAUDE.md** | Distilled state: current tasks, recent decisions, dead ends, file pointers | End of session | Updated by whoever runs session-end |

No separate digests layer. CLAUDE.md IS the running digest. If it exceeds ~100 lines, archive older decisions to `findings/` or `dead_ends/` and trim.

Project instructions in claude.ai hold stable rules (safety, conventions). They don't need a level number — they rarely change.

### 2.2 CLAUDE.md — The Router

~80 lines max. Points to files rather than containing all context. Every Claude instance (Chat, Code, Cowork) reads this first.

```
# City101 — Corridor Analysis
[One-line project summary]

## Current State
[What's active, what just changed — updated every session-end]

## Active Tasks
[What's in progress, by whom, on which assignment]

## Recent Decisions (with rationale)
[Last 5-7 decisions. Older ones archived to findings/]

## Dead Ends (don't re-attempt)
[Last 5-7. Older ones in dead_ends/]

## File Map
datasets/ → [what's there]
output/ → [what's been produced]
scripts/ → [key scripts]
deploy/ → [website, booklet status]

## Conventions
- Coordinates: LV95 / EPSG:2056
- Commit prefixes: [DATA] [FIND] [DEAD] [MAP] [VIZ] [BUILD] [SYNC]
- 49 canonical stations (FROZEN)
```

### 2.3 Commit Prefix Convention

7 prefixes, mapping to roles:

| Prefix | Meaning | Used by |
|--------|---------|---------|
| [DATA] | Dataset created/modified/enriched | Analyst |
| [FIND] | Analytical finding or pattern | Analyst |
| [DEAD] | Dead end documented | Analyst |
| [MAP] | Static map or QGIS output | Cartographer |
| [VIZ] | Interactive visualization | Visualizer |
| [BUILD] | Website/booklet/deploy output | Builder |
| [SYNC] | Coordination: lockboard, session log, CLAUDE.md update | System |

Add [MODEL] when Rhino work starts. Don't pre-create prefixes for work that doesn't exist yet.

---

## 3. COORDINATION LAYER

### 3.1 WhatsApp + LOCKBOARD.md

**WhatsApp group** ("City101 lockboard") = real-time human pings. Quick, zero-friction. "I'm starting work on X" or "don't touch the WiFi CSV."

**LOCKBOARD.md** (in repo) = official record. Updated at session start (claim) and session end (complete/release). Pushed to GitHub so the other person sees it on next pull.

```markdown
# LOCKBOARD — City101
*Last updated: 2026-03-08 14:00 by Andrea (Cairn)*

## IN PROGRESS
| Task | Assignment | Claimed by | Started | Expected output |
|------|-----------|-----------|---------|-----------------|

## COMPLETED TODAY
| Task | Assignment | Done by | Output | Commit |
|------|-----------|---------|--------|--------|

## AVAILABLE (priority order)
| Task | Assignment | Priority | Dependencies |
|------|-----------|----------|--------------|

## BLOCKED
| Task | Blocked by | Waiting on |
|------|-----------|------------|
```

### 3.2 Session Protocol

**Start** (2 minutes):
1. `git pull` — get partner's latest
2. Read LOCKBOARD.md — see what's claimed
3. Claim your task — update lockboard, commit `[SYNC] Claim: <task>`, push

**End** (5 minutes):
1. Update LOCKBOARD.md (complete/in-progress/release)
2. Update CLAUDE.md if state changed (decisions, findings, dead ends)
3. `git add . && git commit -m "[SYNC] Session end — <summary>"` — Chat drafts this
4. `git push`

### 3.3 Branch Strategy

```
main                    ← stable, reviewed outputs only
├── andrea/[task-slug]  ← Andrea's work (any Claude instance)
└── henna/[task-slug]   ← Henna's work (any Claude instance)
```

It doesn't matter which Claude instance produced the work. It matters which human is responsible.

### 3.4 Binary File Protocol

.3dm, .blend, .qgz files can't be merged by git. Rules:
- One active file per branch. Andrea models station X, Henna doesn't touch it.
- Parametric scripts are the source of truth when possible (script is mergeable; binary is regenerable).
- QGIS projects: one owner at a time. Others modify data CSVs, which QGIS reloads.

---

## 4. AGENT LAYER

### 4.1 Claude Instances

| Interactive | Code variant | Owner | Plan | Notes |
|-------------|-------------|-------|------|-------|
| **Cairn** | **Cairn Code** | Andrea | Max | Primary workhorse. Highest limits. |
| **Lumen** | **Lumen Code** | Andrea | Team | Overflow. Hits Opus cap faster. |
| **Cadence** | **Cadence Code** | Henna | Pro | Henna's primary. |
| **Meridian** | **Meridian Code** | Henna | Team | Overflow. |

All have identical MCP setups: QGIS, Rhino, Chrome, OSM. Both teams add filesystem MCP (Section 1.4). Cowork is available as a friendlier alternative to Code — same capabilities, no terminal required.

### 4.2 Agent Roles — 4 Production + 1 Utility

The test: does the role need *different files* in its context window? If yes, it's a distinct role.

| Role | What it does | Context scope | Commit prefix |
|------|-------------|--------------|---------------|
| **Analyst** | Find data, query APIs, process CSVs, discover patterns, document dead ends | CLAUDE.md, datasets/, scripts/data/, findings/, dead_ends/ | [DATA] [FIND] [DEAD] |
| **Cartographer** | QGIS maps, print layouts, spatial analysis | CLAUDE.md, design_system/, datasets/processed/, output/maps/ | [MAP] |
| **Visualizer** | Interactive HTML/JS/Leaflet/D3 | CLAUDE.md, design_system/, scripts/viz/, output/viz/ | [VIZ] |
| **Builder** | Website assembly, booklet, narrative, deploy | CLAUDE.md, deploy/, design_system/, output/, narrative/ | [BUILD] |

| Utility | What it does |
|---------|-------------|
| **session-end** | Summarize session, update CLAUDE.md, pre-commit checklist |

Add **Modeler** when Rhino/Blender work starts (A.04/A.05). Don't pre-create roles for work that doesn't exist yet.

**Coordinator is not a role** — it's the first thing you ask any agent at session start: "Read CLAUDE.md and the lockboard, recommend what to work on."

### 4.3 Skill File Format

Skills live in `.claude/skills/` as YAML front matter markdown files. Claude Code and Cowork read these natively.

```yaml
---
name: analyst
description: "Data processing, API calls, and CSV output for City101 corridor analysis"
---

# Analyst Skill

## When to use
- Processing raw datasets into enriched/processed CSVs
- Making API calls (transport.opendata.ch, Open Charge Map, Google Places)
- Writing data analysis scripts
- Documenting dead ends

## Context to load
1. CLAUDE.md (always first)
2. datasets/inventory.md
3. research/api_notes.md
4. The specific dataset(s) being processed

## Quality gate (before every commit)
- [ ] Output CSV has canonical station IDs where applicable
- [ ] Coordinates in LV95 (EPSG:2056) or clearly labeled WGS84
- [ ] Check dead_ends/ — has this been attempted before?
- [ ] Data inventory updated with new/modified dataset
- [ ] Null counts and row counts printed in summary
- [ ] API rate limits respected (min 0.25s between calls)
```

### 4.4 Session-End Skill

The single most important piece. Replaces: handoff files, manual lockboard updates, the summarizer role.

```yaml
---
name: session-end
description: "End-of-session ritual: summarize, update CLAUDE.md, pre-commit checklist"
---

# Session End Skill

## When to use
At natural stopping points (1-2x per day). NOT on every commit.

## Process
1. Read git diff since last session-end tag
2. Summarize: what was done, decisions made, dead ends found
3. Write session log to session_logs/YYYY-MM-DD_[agent]_S[n].md
4. Update CLAUDE.md:
   - "Current state" — what changed
   - "Recent decisions" — any new ones (with rationale)
   - "Dead ends" — anything tried and abandoned
   - "Active tasks" — what's in progress, what's done
5. Run pre-commit checklist:
   - New datasets? → Update inventory.md
   - Dead ends? → Written to dead_ends/ with rationale
   - Decisions? → In CLAUDE.md recent decisions section
6. Stage, commit, tag, push (or draft commands for human to run)
```

---

## 5. REPOSITORY STRUCTURE

```
city101/
├── CLAUDE.md                      ← The brain (~80 lines, router)
├── LOCKBOARD.md                   ← Who's doing what right now
├── .gitattributes                 ← LFS tracking rules
├── .gitignore
├── README.md
│
├── datasets/
│   ├── inventory.md               ← What exists, provenance
│   ├── raw/                       ← Unmodified source data
│   └── processed/                 ← Enriched, analysis-ready
│
├── findings/                      ← Analytical findings (markdown)
├── dead_ends/                     ← What was tried and abandoned (with why)
│
├── output/
│   ├── maps/                      ← QGIS exports, print layouts
│   ├── viz/                       ← Interactive HTML visualizations
│   └── models/                    ← 3D exports (when needed)
│
├── design_system/                 ← Colors, fonts, component specs
│
├── scripts/
│   ├── data/                      ← Data processing
│   ├── viz/                       ← Visualization generation
│   └── qgis/                      ← QGIS-specific scripts
│
├── deploy/
│   ├── website/                   ← A.02 scrollytelling site
│   └── booklet/                   ← Process booklet
│
├── research/
│   ├── api_notes.md               ← API quirks, rate limits, keys
│   └── references/                ← Papers, links, expert notes
│
├── narrative/                     ← Thesis text, feedback, versions
│
├── session_logs/                  ← Per-session summaries
│
├── process/                       ← Process documentation for booklet
│   └── prompts/                   ← Saved prompts worth keeping
│
└── .claude/
    └── skills/
        ├── analyst/skill.md
        ├── cartographer/skill.md
        ├── visualizer/skill.md
        ├── builder/skill.md
        └── session-end/skill.md
```

### 5.1 Git LFS Tracking (.gitattributes)

```
*.qgz filter=lfs diff=lfs merge=lfs -text
*.qgs filter=lfs diff=lfs merge=lfs -text
*.gpkg filter=lfs diff=lfs merge=lfs -text
*.3dm filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.tif filter=lfs diff=lfs merge=lfs -text
```

---

## 6. PRODUCTION PIPELINE

```
RAW SOURCES → datasets/raw/ → [Analyst] → datasets/processed/
                                                │
                              ┌─────────────────┼─────────────────┐
                              ↓                 ↓                 ↓
                         output/maps       output/viz        output/models
                         [Cartographer]    [Visualizer]       [Modeler]
                              ↓                 ↓                 ↓
                              └─────────────────┼─────────────────┘
                                                ↓
                                          [Builder] → deploy/
                                                │
                                     ┌──────────┼──────────┐
                                     ↓          ↓          ↓
                                  website    booklet     print
```

### 6.1 Tool Ecosystem

| Tool | MCP | Used by |
|------|-----|---------|
| QGIS | Yes (PyQGIS) | Cartographer, Analyst |
| Rhino | Yes (RhinoScript) | Modeler (when needed) |
| Chrome | Yes | Research tasks |
| OSM | Yes | Geospatial queries |
| Filesystem | Yes (new — Section 1.4) | Chat on desktop — file read/write |
| Google Places | Built into claude.ai | Reviews, ratings, coordinates |
| Leaflet/D3 | Via code generation | Visualizer |

---

## 7. HUMAN COORDINATION (Andrea + Henna)

### 7.1 Domain Split

```
Andrea's domain                     Henna's domain
─────────────────                   ─────────────────
EV charging analysis                Transit ridership
Remote work infrastructure          Psycho-comfort
Working continuity thesis           Thermal comfort
                    ↕
            SHARED INTERFACE
            ─────────────────
            49 canonical stations (FROZEN)
            Corridor geometry v3
            Design system
            Narrative thesis (joint)
            Website + Booklet (joint)
            LOCKBOARD + WhatsApp
```

### 7.2 What Henna Needs to Know

Minimum viable onboarding — three things:

1. **`git pull`** before starting work (get Andrea's latest changes)
2. **`git push`** after finishing work (share your changes)
3. **Check LOCKBOARD.md** before starting (see what's claimed)

Everything else works invisibly. If she uses Claude Code or Cowork, it reads CLAUDE.md automatically. If she uses Chat, the project instructions point to GitHub. She doesn't need to understand skill files, memory levels, or architecture.

**Cowork** (non-terminal tab in Claude Desktop) may be a better entry point for Henna than Claude Code — same capabilities, friendlier interface, no terminal required.

---

## 8. SEMESTER TIMELINE

```
W1  (16 Feb)  ── A.01 ────────────────────────── INTRODUCTION
W2  (23 Feb)  ── A.01 due / A.02 starts
W3  (02 Mar)  ── A.02 ◄ WE ARE HERE ─────────── System init (this doc)
W4  (09 Mar)  ── A.02 + A.03 (FIELDWORK 09-03) ─ First full week on system
W5  (16 Mar)  ── A.02 + A.03 + A.04 (RHINO) ─── Add Modeler role if needed
W6  (23 Mar)  ── A.02 + A.03 + A.04
W7  (30 Mar)  ── MIDTERM ── A.02/03/04 due
    ────────── EASTER BREAK ── System review
W8  (14 Apr)  ── A.05 starts
W9–W12        ── A.05 production
W13 (19 May)  ── CHARETTE
W14 (26 May)  ── FINAL REVIEW
```

---

## 9. IMPLEMENTATION PLAN

### Phase 1: Foundation (this weekend, ~4 hours)

| # | Task | Time | Notes |
|---|------|------|-------|
| 1 | Create GitHub repo (public, with README) | 10 min | github.com → new repo → "city101" |
| 2 | Clone locally, set up LFS + .gitattributes | 15 min | |
| 3 | Create folder structure (Section 5) | 15 min | |
| 4 | Write CLAUDE.md (seed from latest handoff) | 45 min | ~80 lines, router format |
| 5 | Write LOCKBOARD.md (current state) | 15 min | |
| 6 | Write 4 skill files + session-end skill | 60 min | YAML front matter format |
| 7 | Add filesystem MCP to Claude Desktop config | 10 min | Section 1.4 |
| 8 | Migrate existing datasets and scripts | 30 min | |
| 9 | Initial commit + push + Henna clones | 15 min | |
| 10 | Update claude.ai project instructions with GitHub fetch URL | 10 min | |
| 11 | Test full loop: pull → work → commit → push → verify | 15 min | |

### Phase 2: Prove it (W4)

Use the system for actual A.02/A.03 work. Run session-end at least once per day. Identify friction. Don't automate anything.

### Phase 3: Optimize (W5+, only if manual workflow is annoying)

- GitHub Actions for Discord notifications (if WhatsApp isn't enough)
- `/loop` for ambient lockboard monitoring
- Scheduled tasks for auto-digest
- Add Modeler role when Rhino work starts

### Explicitly Deferred

| Item | Revisit when |
|------|-------------|
| n8n (everything) | Only if native features prove insufficient |
| Modeler role | When A.04/A.05 Rhino work starts |
| `/loop` and scheduled tasks | W5+, after manual workflow is proven |
| Anthropic API / Haiku summarizer | Not needed — session-end runs on same Claude instance |
| Cross-review workflow | After midterm |
| Booklet automation | End of semester |

---

## 10. WHAT CHANGED FROM V4

| Dimension | v4 | v5 |
|-----------|-----|-----|
| Automation layer | n8n (Docker + MCP + API) | None. Manual first, native features later |
| Agent roles | 11 | 4 + 1 utility (add as needed) |
| Memory levels | 5 (L0–L4) | 3 (git log, session logs, CLAUDE.md) |
| Commit prefixes | 15 | 7 |
| Branch types | 6+ | 3 (main, andrea/*, henna/*) |
| Coordination | LOCKBOARD.md only | WhatsApp (real-time) + LOCKBOARD.md (record) |
| Chat ↔ Repo | Not specified | Filesystem MCP (desktop) + GitHub URL fetch (browser) |
| Context for Chat | Project knowledge only | Project knowledge (stable) + GitHub fetch (live) |
| External dependencies | Docker, n8n, n8n-MCP, API key | GitHub (free) + Node.js |
| Monthly cost | $0–30 | $0 |
| Setup time | 10–15 hours | ~4 hours |

---

## 11. RISKS

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Session-end doesn't get run | High | High | Single command. Fallback: next session summarizes retroactively from git diff |
| CLAUDE.md bloats beyond 100 lines | High | Medium | Session-end archives old decisions. Hard rule: trim before commit |
| Henna doesn't adopt the system | Medium | High | Three commands: pull, push, check lockboard. Zero new concepts beyond that |
| Three parallel assignments overwhelm | High | Medium | LOCKBOARD makes pressure visible. 2 good outputs > 4 rough ones |
| Context drift between instances | Medium | Medium | CLAUDE.md router. Every session starts by reading it |
| Git conflicts on LOCKBOARD.md | Medium | Low | Whoever pushes first wins. Other pulls, re-edits, pushes. 30 seconds |
| GitHub fetch fails | Low | Low | Fallback: project knowledge (stale but available) |

---

## 12. THE BOOKLET

The semester arc from handoffs W1 onward documents the evolution: handoff system (Sept 2025) → workflow document (Feb 2026) → system architecture v1–v5 (Mar 2026) → git-based coordination (Mar 2026) → operating multi-agent team (Apr–May 2026).

The git commit log + session logs + CLAUDE.md history ARE the raw material. Curate at end of semester.

---

*This document lives at `process/SYSTEM_ARCHITECTURE_v5.md` in the repo. Update after the first 2 weeks of operation.*
