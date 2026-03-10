# SYSTEM ARCHITECTURE — City101 Multi-Agent Workflow
### Systems Engineering Specification v3.0
**Date**: 2026-03-06  
**Client**: Andrea Crespo & Henna Rafik — EPFL BA6 Studio Huang  
**Systems Architect**: Cairn (Claude Opus 4.6)  
**Project**: City101 Geneva–Villeneuve Corridor Analysis  
**Semester**: Spring 2026, 14 weeks (W1 = 16 Feb → W14 = 26 May)  
**Current position**: Week 3

---

## 0. THE PROBLEM THIS SOLVES

**Primary pain**: Andrea and Henna work independently, produce the same datasets, and discover the duplication too late. Eight Claude agent slots and two humans have no shared visibility into what's in progress.

**Secondary pains**: Context loss between sessions, agent output quality requiring rework, no self-documentation of the design process, growing tool sprawl (QGIS, Rhino, Blender, Claude Code ×2, Chrome) without a unifying coordination layer, and a semester structure with overlapping parallel assignments that intensifies all of the above.

**Context**: Andrea has been working with Claude since September 2025. The handoff system emerged organically during last semester. The workflow document (v04) was written when Andrea learned she'd be partnering with Henna. But AI tooling evolves faster than manual documentation can track — this system architecture formalizes and automates what was previously maintained by discipline alone.

**What this document specifies**: A complete system architecture that coordinates all agents, humans, tools, memory, and deliverables through a single git repository (with LFS for binaries) using progressive summarization, task locking, and automatic process documentation.

---

## 1. SYSTEM OVERVIEW

Five layers, from foundation to surface:

```
┌─────────────────────────────────────────────────────────┐
│  5. DELIVERABLES                                         │
│     Website · Booklet · Maps · Models · Paper            │
├─────────────────────────────────────────────────────────┤
│  4. PRODUCTION PIPELINE                                  │
│     2D (QGIS/Leaflet) · 3D (Rhino/Blender) · Web · Print│
├─────────────────────────────────────────────────────────┤
│  3. AGENT LAYER                                          │
│     Role-based agents with scoped context                │
├─────────────────────────────────────────────────────────┤
│  2. COORDINATION LAYER                                   │
│     Lockboard · Task routing · Conflict prevention       │
├─────────────────────────────────────────────────────────┤
│  1. MEMORY LAYER                                         │
│     Git repo (+ LFS) · Progressive summarization         │
└─────────────────────────────────────────────────────────┘
```

---

## 2. MEMORY LAYER — "The Cache Hierarchy"

### 2.1 Memory Levels

| Level | Name | Content | Updated | Size | Who reads |
|-------|------|---------|---------|------|-----------|
| **L0** | Raw commits | Every git commit message | Real-time | Unlimited | Drill-down only |
| **L1** | Session logs | Per-session summary | End of session | ~200 lines | Continuation agents |
| **L2** | Digest | Cross-session synthesis | Before each studio/crit (event-driven) | ~100 lines | All agents at start |
| **L3** | CLAUDE.md | Governance + router + state | When L2 updates | ~80 lines | Every agent, every session |
| **L4** | Project instructions | Stable rules, safety, LOD | Rarely | Unchanged | System prompt |

### 2.2 Progressive Summarization Flow

```
L0: git log --oneline (raw trail)
 ↓  [Summarizer Agent at session end]
L1: session_logs/2026-03-06_cairn_S1.md
 ↓  [Summarizer Agent, triggered before studio/crit]
L2: digests/pre_midterm.md  OR  digests/pre_W5_crit.md
 ↓  [Human review + Summarizer]
L3: CLAUDE.md "Current State" section updated
```

**Digest trigger is event-driven, not calendar-based.** Digests are generated before:
- Studio sessions / desk crits
- Assignment deadlines
- Midterm review
- Charette
- Final review

This aligns with the actual rhythm of work — the system summarizes when you need it, not on an arbitrary schedule.

### 2.3 Commit Prefix Convention

```
[DATA]    Dataset created/modified/enriched
[FIND]    Analytical finding or pattern
[DEAD]    Dead end (attempted and abandoned — critical to log)
[MAP]     Map or static visualization
[VIZ]     Interactive visualization
[MODEL]   3D model created/modified
[NARR]    Narrative text written/revised
[DECIDE]  Design decision (with rationale in message body)
[SCRIPT]  Script created/modified
[AGENT]   Agent prompt or agent run completed
[FIX]     Bug fix or data correction
[SYNC]    Coordination (lockboard, handoff, merge)
[META]    Process documentation, workflow change
[BUILD]   Website/booklet assembly
```

### 2.4 Memory Types

| Type | Implementation | Persistence | Use |
|------|---------------|-------------|-----|
| **Long-term** | Git history + L2 digests + CLAUDE.md | Permanent | Decisions, findings, dead ends |
| **Short-term** | L1 session logs + lockboard | ~1 week relevant | Active tasks, recent context |
| **Working** | Claude context window + project knowledge | Per-session | Current task execution |
| **Shared** | GitHub repo (public, LFS-enabled) | Permanent, any Claude | Cross-agent coordination |
| **Binary** | Git LFS (QGZ, 3DM, BLEND, large PDFs) | Permanent | Model files, QGIS projects |

---

## 3. COORDINATION LAYER — "The Lockboard"

### 3.1 LOCKBOARD.md

Single file at repo root. Every agent checks before starting work.

```markdown
# LOCKBOARD — City101
*Last updated: 2026-03-06 14:32 by Cairn*

## 🔒 IN PROGRESS
| Task | Assignment | Claimed by | Human | Started | Branch | Expected output |
|------|-----------|-----------|-------|---------|--------|-----------------|
| WiFi temporal enrichment | A.02 | Cairn | Andrea | 06-03 | andrea/wifi-temporal | datasets/processed/wifi_temporal.csv |
| Ridership psycho-comfort | A.02 | Meridian | Henna | 06-03 | henna/psycho-comfort | datasets/processed/psycho_comfort.csv |

## ✅ COMPLETED TODAY
| Task | Assignment | Done by | Human | Output | Commit |
|------|-----------|---------|-------|--------|--------|
| EV charging v3 | A.02 | Cairn | Andrea | datasets/processed/ev_charging_v3.csv | a3f2b1c |

## 📋 AVAILABLE (priority order)
| Task | Assignment | Priority | Intensity | Dependencies | Notes |
|------|-----------|----------|-----------|--------------|-------|
| Train Pulse Phase 3 | A.02 | HIGH | Heavy | Phase 2 done | Passenger flow animation |
| A02 website scaffold | A.02 | HIGH | Heavy | Design system | Use PROMPT_BUILD_A02_v3 |
| Point cloud sections | A.02 | MEDIUM | Heavy | High-potential sites identified | swissSURFACE3D lidar |
| Network strategy sketch | A.03 | LOW | Medium | Depends on A.02 narrative | Brief not yet released |

## ⚠️ BLOCKED
| Task | Blocked by | Waiting on |
|------|-----------|------------|
| — | — | — |
```

**Key addition vs v1**: the **Assignment column**. With A.02, A.03, and A.04 running in parallel before midterm, you need to see at a glance how work distributes across deliverables.

### 3.2 Lockboard Protocol

**Start of session** (2 actions):
1. Read LOCKBOARD.md
2. Claim your task (update + commit `[SYNC] Claim: <task>`)

**End of session** (2 actions):
1. Update LOCKBOARD.md (complete, in-progress, or release)
2. Commit `[SYNC] Session end — <summary>`

That's it. Four touchpoints per session. No more.

### 3.3 Branch Strategy

```
main                           ← stable, reviewed outputs only
├── andrea/[task-slug]         ← Andrea's work branches
├── henna/[task-slug]          ← Henna's work branches  
├── agent/cairncode/[task]     ← Cairn Code agent branches
├── agent/lumencode/[task]     ← Lumen Code agent branches
├── agent/cadencecode/[task]   ← Cadence Code agent branches
├── agent/meridiancode/[task]  ← Meridian Code agent branches
└── docs/[topic]               ← Documentation branches
```

### 3.4 GitHub + LFS as Single Source of Truth

**Public repo** (studio about AI workflows — openness is a feature).

**Git LFS tracks binary files:**
```
# .gitattributes
*.qgz filter=lfs diff=lfs merge=lfs -text
*.qgs filter=lfs diff=lfs merge=lfs -text
*.gpkg filter=lfs diff=lfs merge=lfs -text
*.3dm filter=lfs diff=lfs merge=lfs -text
*.blend filter=lfs diff=lfs merge=lfs -text
*.blend1 filter=lfs diff=lfs merge=lfs -text
*.pdf filter=lfs diff=lfs merge=lfs -text
*.png filter=lfs diff=lfs merge=lfs -text
*.jpg filter=lfs diff=lfs merge=lfs -text
*.tif filter=lfs diff=lfs merge=lfs -text
*.stl filter=lfs diff=lfs merge=lfs -text
```

This eliminates the need for a separate Google Drive sync. One repo, one truth. The tradeoff: GitHub LFS free tier gives 1GB storage + 1GB/month bandwidth. If you exceed that, GitHub charges $5/month per 50GB data pack — worth it for a semester project.

**Access matrix:**

| Instance | Read repo | Write + commit | How |
|----------|----------|---------------|-----|
| Cairn Code / Lumen Code | Yes | Yes (auto-commit) | Direct filesystem |
| Cadence Code / Meridian Code | Yes | Yes (auto-commit) | Direct filesystem |
| Cairn / Lumen (desktop + MCP) | Yes | Yes (human commits) | Filesystem via MCP shell |
| Cadence / Meridian (desktop + MCP) | Yes | Yes (human commits) | Filesystem via MCP shell |
| Any instance (browser) | Read-only | No | web_fetch raw GitHub URLs |

### 3.5 Rhino Collaboration Protocol

Rhino .3dm files are binary — even with LFS, git can't merge them. Protocol:

1. **One active Rhino file per branch.** If Andrea is modeling station X, the file is `models/station_X.3dm` on branch `andrea/station-x`. Henna doesn't touch it.

2. **Parametric scripts are the source of truth when possible.** If the model is generated by `scripts/rhino/station_x.py`, the script is the mergeable file. The .3dm is a disposable output that can be regenerated.

3. **Manual merge when both touch the same file:**
   - Person A saves as `models/station_X_andrea.3dm`
   - Person B saves as `models/station_X_henna.3dm`
   - Joint session: open both, copy-paste geometry into a new combined file
   - Commit combined file, archive the two sources
   - This is exactly what you did last semester — the system just makes it explicit.

4. **Same protocol for Blender .blend files.**

5. **QGIS projects (.qgz):** Same binary merge problem. Solution: one QGIS project file, owned by whoever has the desktop session. Others modify data (CSVs, GeoPackages) which QGIS picks up on reload.

---

## 4. AGENT LAYER

### 4.1 Claude Instances (8 Agent Slots)

Both Andrea and Henna have **identical MCP setups**: QGIS, Rhino, Blender, Chrome, OSM. The only asymmetry is account tier (Max vs Pro).

Each account has an interactive mode (claude.ai / desktop app) and a Code mode (Claude Code terminal). Which slots are active at any moment is a **runtime decision** based on usage budgets — the Coordinator checks limits and allocates per 00_Workflow_v04 Section 27.

| Interactive | Code variant | Owner | Tier | Usage role |
|-------------|-------------|-------|------|------------|
| **Cairn** | **Cairn Code** | Andrea | Max | Default workhorse — highest limits |
| **Lumen** | **Lumen Code** | Andrea | Team | When Cairn hits cap, or school resources needed |
| **Cadence** | **Cadence Code** | Henna | Pro | Henna's primary heavy lifting |
| **Meridian** | **Meridian Code** | Henna | Team | When Cadence hits cap, or school resources needed |

**All 8 slots have identical capabilities when on the desktop app** (same MCPs, same filesystem access). The difference is only in usage limits and account-bound features (e.g., Google Places is per-account).

### 4.2 Agent Roles

| Role | What it does | Reads (context scope) | Autonomy | Commit prefix |
|------|-------------|----------------------|----------|---------------|
| **Researcher** | Finds data, queries APIs | CLAUDE.md, data inventory, API notes, source log | R+W. Ask before paid APIs. | [DATA] |
| **Analyst** | Processes data, patterns | CLAUDE.md, datasets/, findings/, dead_ends/ | R+W+Run scripts. Auto-commit. | [FIND] or [DEAD] |
| **Narrator** | Thesis, website copy, booklet | CLAUDE.md, narrative/, findings/, feedback/ | R+W drafts. Human reviews text. | [NARR] |
| **Cartographer** | QGIS maps, print layouts | CLAUDE.md, output registry, design system, datasets/ | R+W+MCP. Auto-commit. | [MAP] |
| **Visualizer** | Interactive HTML/JS | CLAUDE.md, output registry, design system, scripts/viz/ | R+W+Run code. Auto-commit. | [VIZ] |
| **Modeler** | Rhino + Blender 3D | CLAUDE.md, models/, spatial plans, scripts/rhino|blender/ | R+W. Ask before modifying geometry. | [MODEL] |
| **Builder** | Website, booklet assembly | CLAUDE.md, deploy/, design system, all output/ | R+W+Deploy. Auto-commit. | [BUILD] |
| **Coordinator** | Lockboard, handoffs, allocation | CLAUDE.md, LOCKBOARD.md, session_logs/, handoffs/ | Coordination files only. | [SYNC] |
| **Summarizer** | L0→L1→L2→L3 compression | Git log, session_logs/, digests/, CLAUDE.md | R all + W summaries. | [META] |
| **Documenter** | Process booklet content | Everything (read-only) + process/ | R all + W to process/. | [META] |

### 4.3 Context Routing (CLAUDE.md routing table)

Each role reads ONLY its listed files. This prevents context pollution.

```
Researcher  → CLAUDE.md + datasets/inventory.md + research/
Analyst     → CLAUDE.md + datasets/ + findings/ + dead_ends/
Narrator    → CLAUDE.md + narrative/ + findings/ + feedback/
Cartographer→ CLAUDE.md + output/registry.md + design_system/ + datasets/processed/
Visualizer  → CLAUDE.md + output/registry.md + design_system/ + scripts/viz/
Modeler     → CLAUDE.md + models/ + scripts/rhino/ + scripts/blender/
Builder     → CLAUDE.md + deploy/ + design_system/ + output/final/
Coordinator → CLAUDE.md + LOCKBOARD.md + session_logs/ + handoffs/
Summarizer  → git log + session_logs/ + digests/ + CLAUDE.md
Documenter  → Everything (read-only) + process/
```

### 4.4 Roles as Claude Code Commands

Each role becomes a command file in `.claude/commands/roles/`:

```
.claude/commands/
├── roles/
│   ├── researcher.md      ← context routing + autonomy rules + examples
│   ├── analyst.md
│   ├── narrator.md
│   ├── cartographer.md
│   ├── visualizer.md
│   ├── modeler.md
│   ├── builder.md
│   ├── coordinator.md
│   ├── summarizer.md
│   └── documenter.md
├── research-with-agent-team.md   ← existing
├── build-with-agent-team.md      ← existing
└── session-end.md                ← ritual: summarize + lockboard + commit + push
```

Invoking `/roles/analyst` loads that role's context scope and rules. The `session-end` command automates the end-of-session ritual.

---

## 5. PRODUCTION PIPELINE

### 5.1 Data Flow

```
RAW SOURCES → datasets/raw/ → [Analyst] → datasets/processed/
                                               ↓
                               ┌────────────────┼────────────────┐
                               ↓                ↓                ↓
                          output/maps/     output/viz/     output/models/
                          [Cartographer]   [Visualizer]    [Modeler]
                               ↓                ↓                ↓
                               └────────────────┼────────────────┘
                                                ↓
                                           [Builder]
                                                ↓
                                  ┌─────────────┼─────────────┐
                                  ↓             ↓             ↓
                            deploy/website  deploy/booklet  deploy/print
```

### 5.2 Tool Ecosystem

| Tool | MCP | Primary use | Notes |
|------|-----|------------|-------|
| **QGIS** | Yes (PyQGIS) | Geospatial analysis, maps | Full Python via MCP — same safety rules |
| **Rhino** | Yes (RhinoScript) | 3D modeling, parametric | Binary .3dm files → LFS |
| **Blender** | Yes (blender-mcp) | 3D modeling, rendering, animation | Needs installation (Andrea to approve) |
| **Chrome** | Yes | Web interaction, testing | Existing safety rules apply |
| **Claude Code** (×4) | N/A (IS the agent) | Autonomous multi-agent | Cairn/Lumen/Cadence/Meridian Code |
| **VS Code + Claude** | Via extension | Coding with git integration | Natural git workflow, context bar visible |
| **Google Places** | Built into claude.ai | Reviews, ratings, coords | Account-bound, no transferable key |
| **Leaflet/D3** | Via code generation | Interactive web viz | Generated by Visualizer agent |

### 5.3 Realistic Auto-Logging by Interface

| Interface | Can auto-log to git? | Session-end ritual |
|-----------|--------------------|--------------------|
| **Claude Code** (any of 4) | YES — auto-commits throughout | Runs `/session-end` command |
| **VS Code + Claude** | YES — terminal access to git | Human runs `git add -A && git commit && git push` |
| **Desktop + QGIS MCP** (any of 4) | SEMI — can shell out to git via Python | Agent writes session log → human commits |
| **Desktop + Rhino/Blender MCP** | SEMI — same as QGIS | Agent writes session log → human commits |
| **claude.ai browser** (any of 4) | NO — read-only access | Human copies text output → commits in next filesystem session |

**The honest truth**: Only Claude Code and VS Code sessions auto-log cleanly. MCP sessions need the human to commit at the end. Browser sessions produce text that enters the repo later. The system is designed around this reality — the lockboard and session logs are lightweight enough that the "commit at end" ritual takes 60 seconds.

---

## 6. REPOSITORY STRUCTURE

```
city101/
├── CLAUDE.md                    ← L3: governance + router (~80 lines)
├── LOCKBOARD.md                 ← who's doing what RIGHT NOW
├── .gitignore
├── .gitattributes               ← LFS tracking rules
├── README.md                    ← public project description
│
├── datasets/
│   ├── inventory.md             ← what exists, LOI status, provenance
│   ├── raw/                     ← untouched originals (never modified)
│   └── processed/               ← cleaned, enriched, validated
│
├── research/
│   ├── source_log.md            ← every source consulted (append-only)
│   ├── api_notes.md             ← rate limits, auth, quirks
│   └── references/              ← papers, expert talk notes
│
├── findings/                    ← analytical findings (one per file)
├── dead_ends/                   ← failed attempts (one per file)
│
├── narrative/
│   ├── thesis.md                ← current thesis + argument
│   ├── versions/                ← thesis evolution history
│   └── feedback/                ← teacher/crit notes
│
├── design_system/               ← colors, typography, components
│
├── scripts/
│   ├── data/                    ← data processing
│   ├── viz/                     ← visualization generation
│   ├── rhino/                   ← RhinoScript Python
│   ├── blender/                 ← Blender Python
│   └── qgis/                    ← PyQGIS
│
├── models/
│   ├── inventory.md             ← 3D model registry
│   ├── spatial_plans/           ← coordinate plans (before modeling)
│   └── exports/                 ← STL, OBJ for printing
│
├── output/
│   ├── registry.md              ← master output list with versions
│   ├── maps/                    ← QGIS exports
│   ├── viz/                     ← interactive HTML
│   ├── models/                  ← renders, screenshots
│   └── staging/                 ← WIP before review
│
├── deploy/
│   ├── website/                 ← A02 scrollytelling
│   ├── booklet/                 ← process booklet
│   └── print/                   ← print-ready exports
│
├── process/
│   ├── prompts/                 ← agent prompts, build prompts
│   ├── screenshots/             ← process documentation
│   └── reflections/             ← first-person writing
│
├── session_logs/                ← L1 summaries
├── digests/                     ← L2 pre-event syntheses
│
├── handoffs/
│   ├── archive/                 ← all historical handoffs (W1 onward)
│   └── TEAM_HANDOFF_latest.md   ← current cross-team state
│
└── .claude/
    └── commands/
        ├── roles/               ← 10 role command files
        ├── research-with-agent-team.md
        ├── build-with-agent-team.md
        └── session-end.md       ← end-of-session ritual
```

---

## 7. SEMESTER TIMELINE (from studio Gantt)

```
W1  (16 Feb)  ── A.01 starts ──────────────────────────── INTRODUCTION
W2  (23 Feb)  ── A.01 due / A.02 starts
W3  (02 Mar)  ── A.02 continues ◄ WE ARE HERE
W4  (09 Mar)  ── A.02 + A.03 starts
W5  (16 Mar)  ── A.02 + A.03 + A.04 starts (peak overlap)
W6  (23 Mar)  ── A.02 + A.03 + A.04
W7  (30 Mar)  ── A.02 + A.03 + A.04 due ──────────────── MIDTERM
    ────────── EASTER BREAK ──────────
W8  (14 Apr)  ── A.05 starts
W9  (21 Apr)  ── A.05
W10 (28 Apr)  ── A.05
W11 (05 May)  ── A.05
W12 (12 May)  ── A.05
W13 (19 May)  ── A.05 due ────────────────────────────── CHARETTE
W14 (26 May)  ──────────────────────────────────────────── FINAL REVIEW
```

### 7.1 Assignment Map (known)

| Assignment | What | Dates | Status |
|-----------|------|-------|--------|
| **A.01** | Mapping City101 — geodata collection, QGIS maps, pin-up | W1–W2 | ✅ Complete |
| **A.02** | Data Synchronicity — narrative, index, Zurich comparison, point clouds, scrollytelling | W2–W7 | 🔄 In progress |
| **A.03** | Field Verification — on-site fieldwork (Mon 09-03), verify AI-generated sites, begin networked intervention strategy, area report + combined path dataset | W4–W7 | ⏳ Fieldwork Monday |
| **A.04** | Prototyping Interventions — generative design with Rhino MCP, architectural interventions at verified sites. Requires: Rhino MCP working, sites verified, network intervention program | W5–W7 | ⏳ Starts Tue 10-03 |
| **A.05** | *(Brief not yet released — final comprehensive project)* | W8–W13 | ⏳ Future |

### 7.2 System Implementation Phases

| Phase | When | What to do | Why now |
|-------|------|-----------|--------|
| **Init** | This week (W3) | Git repo + LFS + directory structure + CLAUDE.md + LOCKBOARD + migrate files + first coordinated session | Foundation must exist before A.03 starts |
| **Test** | W4 | First real parallel work session with lockboard. Andrea and Henna claim different tasks, work simultaneously, push at end | Prove the coordination works before peak overlap |
| **Peak** | W5–W7 | Three assignments in parallel. Lockboard is critical. Pre-midterm digest generated. | Maximum coordination pressure |
| **Reset** | Easter | Review what worked, strip what didn't. Update CLAUDE.md. Archive pre-midterm session logs. | Clean slate for A.05 |
| **Scale** | W8–W13 | A.05 full production. System is mature. Auto-documentation feeds booklet. | The system pays off here |
| **Ship** | W13–W14 | Charette → Final. Builder agent assembles. | Everything converges |

### 7.3 Digest Triggers (Event-Driven)

Digests are generated BEFORE these events:
- Week 4 desk crit (first feedback on A.02 progress)
- A.03 brief release (context for new assignment)
- A.04 brief release
- **Midterm review (end W7)** — major digest
- Post-Easter restart (W8)
- A.05 milestones (as they're announced)
- **Charette (W13)** — major digest
- **Final review (W14)** — final digest = booklet backbone

---

## 8. HUMAN COORDINATION (Andrea + Henna)

### 8.1 Shared Interface

```
Andrea's domain                     Henna's domain
─────────────────                   ─────────────────
EV charging analysis                Transit ridership
Remote work infrastructure          Psycho-comfort
Working continuity thesis           Thermal comfort
Website front-end                   Cultural circuits
                    ↕
            SHARED INTERFACE
            ─────────────────
            49 canonical stations (join key — FROZEN)
            Corridor geometry v3
            Design system
            Narrative thesis (joint)
            Website structure (joint)
            Booklet (joint)
            LOCKBOARD + TEAM_HANDOFF
```

### 8.2 Conflict Prevention

1. **Datasets**: Domain-owned. Shared datasets (station list, geometry) are FROZEN — changes need TEAM_HANDOFF.
2. **Design system**: Joint ownership. Both must agree on changes.
3. **Narrative**: Joint ownership. Claim specific sections on lockboard before editing.
4. **Rhino/Blender**: One active file per branch. Parametric scripts are the mergeable truth. Manual merge for geometry.
5. **QGIS project**: One owner at a time. Others modify data CSVs, which reload automatically.

### 8.3 Daily Sync (2 minutes)

```
Start of work:  Read LOCKBOARD → Claim tasks → Go
End of work:    Update LOCKBOARD → Session log → Commit → Push
```

No meeting required. The lockboard IS the sync.

---

## 9. THE BOOKLET — Self-Documenting System

Two intertwined stories: the corridor (architecture) and the workflow (how AI made the corridor legible).

### 9.1 Auto-Generated Content

| Source | Becomes |
|--------|---------|
| Git commit log (L0) | Design diary timeline |
| Dead ends (dead_ends/) | "What didn't work" — methodological honesty |
| Session logs (L1) | Raw process material (curated selection) |
| Digests (L2) | Chapter structure / narrative backbone |
| Agent prompts (process/prompts/) | "How we instructed AI" |
| Findings (findings/) | Analytical results |
| Handoffs W1–W14 (handoffs/archive/) | The semester story from start to finish |
| Output registry | Visual portfolio |

### 9.2 The Semester Story

The handoffs from W1 onward (already in project knowledge) ARE the opening chapters. The system captures the evolution: from a single student with a handoff system (Sept 2025) → team workflow document (Feb 2026) → formalized system architecture (Mar 2026) → operating multi-agent team (Mar–May 2026). That arc IS the booklet's AI chapter.

---

## 10. INITIALIZATION CHECKLIST

**Estimated time: 45–60 minutes. Requires desktop session (Cairn or Cairn Code).**

```
 1. Create GitHub repo
    → github.com/new → "city101" → Public → MIT license → init with README
    → Settings → enable LFS

 2. Clone locally
    → cd ~/CLAUDE/City101_ClaudeCode && git clone [url] city101-repo

 3. Configure LFS
    → cd city101-repo && git lfs install
    → Create .gitattributes (Section 3.4)

 4. Create directory structure
    → mkdir -p datasets/{raw,processed} research/references findings dead_ends
      narrative/{versions,feedback} design_system scripts/{data,viz,rhino,blender,qgis}
      models/{spatial_plans,exports} output/{maps,viz,models,staging}
      deploy/{website,booklet,print} process/{prompts,screenshots,reflections}
      session_logs digests handoffs/archive .claude/commands/roles

 5. Write CLAUDE.md (≤80 lines, from L3 template)

 6. Write LOCKBOARD.md (from Section 3.1)

 7. Migrate existing files
    → CSVs → datasets/processed/
    → Scripts → scripts/data/
    → Historical handoffs → handoffs/archive/
    → Prompts → process/prompts/
    → Write datasets/inventory.md

 8. Write role command files (.claude/commands/roles/*.md)

 9. Write session-end.md command

10. Initial commit + push
    → git add -A
    → git commit -m "[META] Initialize City101 repository — system architecture v2"
    → git push

11. Share with Henna
    → She clones to her machine
    → She sets up LFS: git lfs install
    → Her Claude Code gets filesystem access
    → First coordinated lockboard test

12. Archive Google Drive sync
    → Keep Drive as read-only backup / legacy access
    → All new work goes through git
```

---

## 11. OPEN QUESTIONS

1. **A.05 brief**: When released, integrate milestones into timeline and lockboard.
2. **Blender MCP installation**: Both Andrea and Henna need to approve. Same security surface as Rhino MCP.
3. **VS Code + Claude extension**: Worth setting up as an alternative to Claude Code for sessions where you want IDE + git in one view?
4. **n8n as automation layer (break glass)**: Claude can be added as an n8n node. Potential automations: git push webhook → trigger Summarizer, auto-notify partner on shared branch push, schedule digest generation before known crit dates, watch folders for new CSVs → auto-validate schema. **Introduce only if manual coordination breaks down — not a foundation dependency.** Earliest: W8 (after midterm proves the manual system works or doesn't).
5. **Claude Cowork**: Desktop automation tool — experimental. Monitor but don't build around yet.
6. **LFS cost**: 1GB free. Monitor usage. If binary files accumulate, $5/month per 50GB data pack.

---

## 12. RISKS AND MITIGATIONS

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| Lockboard gets stale | High | Make it a 60-second ritual. `/session-end` command enforces it. |
| LFS bandwidth exceeded | Medium | Track usage monthly. Purge old model versions if needed. |
| Agent produces garbage that gets committed | Medium | Agent branches only. Human review before merge to main. |
| Henna doesn't adopt system | Medium | Start with JUST the lockboard. Add complexity only as needed. |
| Three parallel assignments overwhelm the system | Medium | The lockboard's Assignment column makes pressure visible. |
| Progressive summarization loses detail | Low | L0 (raw commits) is never deleted. Drill down always possible. |

---

*This document lives at `process/SYSTEM_ARCHITECTURE.md` in the repo. v4 will incorporate lessons from the first 2 weeks of operation (W4–W5).*
