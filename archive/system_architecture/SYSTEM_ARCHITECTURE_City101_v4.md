# SYSTEM ARCHITECTURE — City101 Multi-Agent Workflow
### Systems Engineering Specification v4.0
**Date**: 2026-03-07  
**Client**: Andrea Crespo & Henna Rafik — EPFL BA6 Studio Huang  
**Systems Architect**: Cairn (Claude Opus 4.6)  
**Project**: City101 Geneva–Villeneuve Corridor Analysis  
**Semester**: Spring 2026, 14 weeks (W1 = 16 Feb → W14 = 26 May)  
**Current position**: Week 3

---

## 0. THE PROBLEM THIS SOLVES

**Primary pain**: Andrea and Henna work independently, produce the same datasets, and discover the duplication too late. Eight Claude agent slots and two humans have no shared visibility into what's in progress.

**Secondary pains**: Context loss between sessions, agent output quality requiring rework, no self-documentation of the design process, growing tool sprawl (QGIS, Rhino, Blender, Claude Code ×4, Chrome, n8n) without a unifying coordination layer, and a semester structure with overlapping parallel assignments that intensifies all of the above.

**Context**: Andrea has been working with Claude since September 2025. The handoff system emerged organically during last semester. The workflow document (v04) was written when Andrea learned she'd be partnering with Henna. But AI tooling evolves faster than manual documentation can track — this system architecture formalizes and automates what was previously maintained by discipline alone.

**What this document specifies**: A complete system architecture that coordinates all agents, humans, tools, memory, and deliverables through a single git repository (with LFS for binaries), with n8n as the automation backbone once manual coordination is proven.

---

## 1. SYSTEM OVERVIEW

Six layers, from foundation to surface:

```
┌─────────────────────────────────────────────────────────┐
│  6. DELIVERABLES                                         │
│     Website · Booklet · Maps · Models · Paper            │
├─────────────────────────────────────────────────────────┤
│  5. PRODUCTION PIPELINE                                  │
│     2D (QGIS/Leaflet) · 3D (Rhino/Blender) · Web · Print│
├─────────────────────────────────────────────────────────┤
│  4. AGENT LAYER                                          │
│     Role-based agents with scoped context                │
├─────────────────────────────────────────────────────────┤
│  3. AUTOMATION LAYER (n8n)                               │
│     Event-driven workflows · Summarizer · Notifications  │
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
L0: git log --oneline
 ↓  [n8n trigger on git push → Claude API summarizes]
L1: session_logs/2026-03-06_cairn_S1.md
 ↓  [n8n scheduled trigger before crit → Claude API synthesizes]
L2: digests/pre_midterm.md
 ↓  [Human review + Claude updates]
L3: CLAUDE.md "Current State" section
```

Once n8n is active, L0→L1 summarization happens automatically on every git push. L1→L2 is triggered before events (crits, deadlines). L2→L3 is human-reviewed.

### 2.3 Commit Prefix Convention

```
[DATA]    Dataset created/modified/enriched
[FIND]    Analytical finding or pattern
[DEAD]    Dead end (attempted and abandoned)
[MAP]     Map or static visualization
[VIZ]     Interactive visualization
[MODEL]   3D model created/modified
[NARR]    Narrative text written/revised
[DECIDE]  Design decision (with rationale in body)
[SCRIPT]  Script created/modified
[AGENT]   Agent prompt or agent run completed
[FIX]     Bug fix or data correction
[SYNC]    Coordination (lockboard, handoff, merge)
[META]    Process documentation, workflow change
[BUILD]   Website/booklet assembly
[AUTO]    Automated by n8n (not human-initiated)
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
*Last updated: 2026-03-07 14:32 by Cairn*

## 🔒 IN PROGRESS
| Task | Assignment | Claimed by | Human | Started | Branch | Expected output |
|------|-----------|-----------|-------|---------|--------|-----------------|

## ✅ COMPLETED TODAY
| Task | Assignment | Done by | Human | Output | Commit |
|------|-----------|---------|-------|--------|--------|

## 📋 AVAILABLE (priority order)
| Task | Assignment | Priority | Intensity | Dependencies | Notes |
|------|-----------|----------|-----------|--------------|-------|

## ⚠️ BLOCKED
| Task | Blocked by | Waiting on |
|------|-----------|------------|
```

The **Assignment column** is critical — with A.02, A.03, and A.04 running in parallel, you need to see at a glance how work distributes across deliverables.

### 3.2 Lockboard Protocol

**Start of session** (2 actions):
1. Read LOCKBOARD.md
2. Claim your task (update + commit `[SYNC] Claim: <task>`)

**End of session** (2 actions):
1. Update LOCKBOARD.md (complete, in-progress, or release)
2. Commit `[SYNC] Session end — <summary>` + push

Four touchpoints per session. No more.

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

**Git LFS tracks binary files** (`.gitattributes`):
```
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

**Access matrix:**

| Instance | Read repo | Write + commit | How |
|----------|----------|---------------|-----|
| Cairn Code / Lumen Code | Yes | Yes (auto-commit) | Direct filesystem |
| Cadence Code / Meridian Code | Yes | Yes (auto-commit) | Direct filesystem |
| Cairn / Lumen (desktop + MCP) | Yes | Yes (human commits) | Filesystem via MCP |
| Cadence / Meridian (desktop + MCP) | Yes | Yes (human commits) | Filesystem via MCP |
| Any instance (browser) | Read-only | No | web_fetch raw GitHub URLs |
| **n8n** (automated) | Yes | Yes (auto-commit) | GitHub API / webhook |

### 3.5 Rhino / Blender Collaboration Protocol

Binary .3dm and .blend files can't be merged by git. Protocol:

1. **One active file per branch.** Andrea models station X on `andrea/station-x`. Henna doesn't touch it.
2. **Parametric scripts are the source of truth when possible.** The script is mergeable; the binary is regenerable.
3. **Manual merge when needed:** Person A saves `_andrea` suffix, Person B saves `_henna` suffix, joint session merges into combined file.
4. **QGIS projects:** One owner at a time. Others modify data CSVs, which reload automatically.

---

## 4. AUTOMATION LAYER — n8n

### 4.1 Architecture: Claude Code Builds, Claude API Runs

```
┌─────────────────────────────────────────────┐
│  DESIGN TIME (one-off setup)                │
│                                             │
│  Claude Code + n8n-MCP                      │
│  ├── Builds workflows node by node          │
│  ├── Tests each node incrementally          │
│  ├── Self-corrects on failure               │
│  └── Deploys to n8n instance                │
└───────────────┬─────────────────────────────┘
                │ deploys
                ▼
┌─────────────────────────────────────────────┐
│  RUNTIME (automated, no human needed)       │
│                                             │
│  n8n workflows                              │
│  ├── Trigger: git push webhook              │
│  │   └── Claude API: summarize commits → L1 │
│  ├── Trigger: schedule (pre-crit)           │
│  │   └── Claude API: synthesize L1s → L2    │
│  ├── Trigger: lockboard change              │
│  │   └── Notify partner (Discord/email)     │
│  ├── Trigger: new CSV in datasets/          │
│  │   └── Claude API: validate schema        │
│  └── Trigger: branch merge to main          │
│      └── Update output/registry.md          │
└─────────────────────────────────────────────┘
```

**Claude Code + n8n-MCP** = the architect. It builds the workflows by connecting to the n8n instance via API, constructing nodes, testing each one, and deploying.

**Claude API as n8n node** = the worker. Once workflows are deployed, they fire on triggers and call the Claude API (via HTTP Request node) to do actual work: summarize, validate, write, analyze.

### 4.2 n8n Workflows to Build (Priority Order)

| # | Workflow | Trigger | What it does | Priority |
|---|----------|---------|-------------|----------|
| 1 | **Push Notifier** | GitHub webhook (push to any branch) | Sends message to Discord/Slack: "[Human] pushed to [branch]: [commit message]" | HIGH — solves duplication problem directly |
| 2 | **Auto-Summarizer** | GitHub webhook (push with 3+ commits) | Calls Claude API with commit diff → writes session summary → commits as `[AUTO]` | HIGH — reduces manual session-end work |
| 3 | **Lockboard Watcher** | GitHub webhook (LOCKBOARD.md changed) | Notifies partner: "Andrea claimed [task] on A.02" | HIGH — real-time coordination visibility |
| 4 | **Pre-Event Digest** | Scheduled (day before known crit dates) | Reads all L1 logs since last digest → Claude API writes L2 → commits | MEDIUM — event-driven memory |
| 5 | **CSV Validator** | Folder watch (datasets/processed/) | Claude API checks schema, null counts, joins against canonical stations | MEDIUM — catches data bugs early |
| 6 | **Branch Merge Logger** | GitHub webhook (PR merged to main) | Updates output/registry.md automatically | LOW — nice to have |
| 7 | **Booklet Collector** | Weekly schedule | Claude API identifies "booklet-worthy" moments from session logs → drafts to process/reflections/ | LOW — booklet automation |

### 4.3 n8n Setup Requirements

| Component | What | How to install |
|-----------|------|---------------|
| **n8n instance** | Self-hosted (Docker) or n8n Cloud | `docker run -it --rm -p 5678:5678 n8nio/n8n` or sign up at n8n.cloud |
| **n8n-MCP server** | MCP for Claude Code to build workflows | `npm install -g n8n-mcp` |
| **n8n-skills** | 7 Claude Code skills for workflow building | `git clone https://github.com/czlonkowski/n8n-skills.git` → copy to `~/.claude/skills/` |
| **Anthropic API key** | For Claude API calls inside n8n workflows | From console.anthropic.com (costs ~$0.003/1K tokens with Haiku) |
| **GitHub webhook** | Triggers n8n on repo events | Repo Settings → Webhooks → point to n8n webhook URL |

### 4.4 Cost Estimate

| Component | Cost |
|-----------|------|
| n8n Cloud (Starter) | $24/month (or free if self-hosted on Docker) |
| Claude API (Haiku for summaries) | ~$2-5/month at estimated usage |
| GitHub LFS | Free tier (1GB), then $5/month per 50GB |
| **Total** | **$0–30/month** depending on hosting choice |

Self-hosting n8n on Docker is free and runs on any machine. For a semester project, self-hosted is the pragmatic choice.

### 4.5 Phased Activation

n8n is **infrastructure that's ready but not active** until manual coordination has been tested. The activation sequence:

| Phase | When | What activates | Why |
|-------|------|---------------|-----|
| **Install** | W3 (now) | n8n instance running, n8n-MCP connected to Claude Code | Infrastructure ready |
| **First workflow** | After A.03 fieldwork (W4) | Push Notifier (#1) — the simplest, highest-value workflow | Solves the #1 problem with minimal complexity |
| **Core automation** | W5 (if #1 works well) | Auto-Summarizer (#2) + Lockboard Watcher (#3) | Reduces manual session-end work |
| **Event-driven** | W6+ (before midterm) | Pre-Event Digest (#4) + CSV Validator (#5) | Memory and data quality automation |
| **Full system** | W8+ (post-Easter, if needed) | Branch Merge Logger (#6) + Booklet Collector (#7) | Nice-to-have automation |

Each activation is a decision point: did the previous workflow actually help? If not, don't add more complexity.

---

## 5. AGENT LAYER

### 5.1 Claude Instances (8 Agent Slots)

Both Andrea and Henna have **identical MCP setups**: QGIS, Rhino, Blender, Chrome, OSM, and (once set up) n8n-MCP.

Each account has an interactive mode (claude.ai / desktop app) and a Code mode (terminal). Which slots are active depends on usage budgets — the Coordinator checks limits and allocates per 00_Workflow_v04 Section 27.

| Interactive | Code variant | Owner | Tier | Usage role |
|-------------|-------------|-------|------|------------|
| **Cairn** | **Cairn Code** | Andrea | Max | Default workhorse — highest limits |
| **Lumen** | **Lumen Code** | Andrea | Team | Overflow, school resources |
| **Cadence** | **Cadence Code** | Henna | Pro | Henna's primary heavy lifting |
| **Meridian** | **Meridian Code** | Henna | Team | Overflow, school resources |

**All 8 slots have identical capabilities on the desktop app.** Difference is only usage limits.

### 5.2 Agent Roles

| Role | What it does | Context scope | Autonomy | Prefix |
|------|-------------|--------------|----------|--------|
| **Researcher** | Finds data, queries APIs | CLAUDE.md, inventory, API notes, source log | R+W. Ask before paid APIs. | [DATA] |
| **Analyst** | Processes data, patterns | CLAUDE.md, datasets/, findings/, dead_ends/ | R+W+Scripts. Auto-commit. | [FIND]/[DEAD] |
| **Narrator** | Thesis, copy, booklet | CLAUDE.md, narrative/, findings/, feedback/ | R+W drafts. Human reviews. | [NARR] |
| **Cartographer** | QGIS maps, layouts | CLAUDE.md, registry, design system, datasets/ | R+W+MCP. Auto-commit. | [MAP] |
| **Visualizer** | Interactive HTML/JS | CLAUDE.md, registry, design system, scripts/viz/ | R+W+Code. Auto-commit. | [VIZ] |
| **Modeler** | Rhino + Blender 3D | CLAUDE.md, models/, spatial plans, scripts/ | R+W. Ask before modifying. | [MODEL] |
| **Builder** | Website, booklet assembly | CLAUDE.md, deploy/, design system, output/ | R+W+Deploy. Auto-commit. | [BUILD] |
| **Coordinator** | Lockboard, handoffs | CLAUDE.md, LOCKBOARD, session_logs/, handoffs/ | Coordination files only. | [SYNC] |
| **Summarizer** | L0→L1→L2→L3 | Git log, session_logs/, digests/, CLAUDE.md | R all + W summaries. | [META] |
| **Documenter** | Process booklet content | Everything (read-only) + process/ | R all + W to process/. | [META] |
| **Automator** | Builds n8n workflows | CLAUDE.md, n8n-MCP, scripts/n8n/ | R+W+n8n-MCP. Human reviews. | [AUTO] |

### 5.3 Roles as Claude Code Commands

```
.claude/commands/
├── roles/
│   ├── researcher.md
│   ├── analyst.md
│   ├── narrator.md
│   ├── cartographer.md
│   ├── visualizer.md
│   ├── modeler.md
│   ├── builder.md
│   ├── coordinator.md
│   ├── summarizer.md
│   ├── documenter.md
│   └── automator.md       ← NEW: n8n workflow builder
├── research-with-agent-team.md
├── build-with-agent-team.md
└── session-end.md
```

---

## 6. PRODUCTION PIPELINE

### 6.1 Data Flow (with Automation)

```
RAW SOURCES → datasets/raw/ → [Analyst] → datasets/processed/
                                               │
                              ┌─────── n8n: CSV Validator ──────┐
                              │                                 │
                              ↓                                 ↓ (if invalid: notify)
                 ┌────────────┼────────────┐
                 ↓            ↓            ↓
            output/maps  output/viz  output/models
                 ↓            ↓            ↓
                 └────────────┼────────────┘
                              ↓
                         [Builder] → deploy/
                              │
                    ┌─────────┼─────────┐
                    ↓         ↓         ↓
               website    booklet    print
```

### 6.2 Tool Ecosystem

| Tool | MCP | Use | Who builds with it |
|------|-----|-----|-------------------|
| **QGIS** | Yes (PyQGIS) | Geospatial analysis, maps | Cartographer, Analyst |
| **Rhino** | Yes (RhinoScript) | 3D modeling, parametric | Modeler |
| **Blender** | Yes (blender-mcp) | 3D modeling, rendering | Modeler, Visualizer |
| **Chrome** | Yes | Web interaction, testing | Researcher, Builder |
| **OSM** | Yes | Geospatial queries | Researcher, Analyst |
| **n8n** | Yes (n8n-mcp) | Workflow automation | Automator (builds), Claude API (runs) |
| **Claude Code** (×4) | N/A (IS the agent) | Autonomous tasks | All roles |
| **VS Code + Claude** | Extension | Coding with git | All roles |
| **Google Places** | Built into claude.ai | Reviews, ratings | Researcher |
| **Leaflet/D3** | Via code generation | Interactive viz | Visualizer |

### 6.3 Auto-Logging by Interface

| Interface | Auto-log to git? | Session-end ritual |
|-----------|-----------------|-------------------|
| **Claude Code** (any of 4) | YES — auto-commits | Runs `/session-end` |
| **VS Code + Claude** | YES — terminal git | Human: `git add -A && git commit && git push` |
| **Desktop + MCP** (any of 4) | SEMI — needs human commit | Agent writes log → human commits |
| **claude.ai browser** (any) | NO — read-only | Human copies output → commits later |
| **n8n workflows** | YES — fully automated | Commits with `[AUTO]` prefix |

---

## 7. REPOSITORY STRUCTURE

```
city101/
├── CLAUDE.md                    ← L3: governance + router (~80 lines)
├── LOCKBOARD.md                 ← who's doing what RIGHT NOW
├── .gitignore
├── .gitattributes               ← LFS tracking rules
├── README.md
│
├── datasets/
│   ├── inventory.md
│   ├── raw/
│   └── processed/
│
├── research/
│   ├── source_log.md
│   ├── api_notes.md
│   └── references/
│
├── findings/
├── dead_ends/
│
├── narrative/
│   ├── thesis.md
│   ├── versions/
│   └── feedback/
│
├── design_system/
│
├── scripts/
│   ├── data/
│   ├── viz/
│   ├── rhino/
│   ├── blender/
│   ├── qgis/
│   └── n8n/                     ← n8n workflow exports (JSON backup)
│
├── models/
│   ├── inventory.md
│   ├── spatial_plans/
│   └── exports/
│
├── output/
│   ├── registry.md
│   ├── maps/
│   ├── viz/
│   ├── models/
│   └── staging/
│
├── deploy/
│   ├── website/
│   ├── booklet/
│   └── print/
│
├── process/
│   ├── prompts/
│   ├── screenshots/
│   └── reflections/
│
├── session_logs/
├── digests/
│
├── handoffs/
│   ├── archive/                 ← W1 onward (semester story)
│   └── TEAM_HANDOFF_latest.md
│
└── .claude/
    └── commands/
        ├── roles/               ← 11 role command files
        ├── research-with-agent-team.md
        ├── build-with-agent-team.md
        └── session-end.md
```

---

## 8. SEMESTER TIMELINE

```
W1  (16 Feb)  ── A.01 ──────────────────────────────────── INTRODUCTION
W2  (23 Feb)  ── A.01 due / A.02 starts
W3  (02 Mar)  ── A.02 ◄ WE ARE HERE ── System init + n8n install
W4  (09 Mar)  ── A.02 + A.03 (FIELDWORK MON 09-03) ── First n8n workflow
W5  (16 Mar)  ── A.02 + A.03 + A.04 (RHINO PROTOTYPING) ── Core automation
W6  (23 Mar)  ── A.02 + A.03 + A.04 ── Pre-midterm digest
W7  (30 Mar)  ── MIDTERM ── A.02/03/04 due
    ────────── EASTER BREAK ── System review + reset
W8  (14 Apr)  ── A.05 starts ── Full automation if needed
W9–W12        ── A.05 production
W13 (19 May)  ── CHARETTE
W14 (26 May)  ── FINAL REVIEW
```

### 8.1 Assignment Map

| Assignment | What | Status |
|-----------|------|--------|
| **A.01** | Mapping City101 — geodata, QGIS maps, pin-up | ✅ Complete |
| **A.02** | Data Synchronicity — narrative, index, scrollytelling, point clouds | 🔄 In progress |
| **A.03** | Field Verification — on-site fieldwork Mon 09-03, verify sites, networked intervention strategy | ⏳ Fieldwork Monday |
| **A.04** | Prototyping Interventions — Rhino MCP generative design, starts Tue 10-03 | ⏳ Starts Tuesday |
| **A.05** | Final project (brief TBD) | ⏳ Post-Easter |

---

## 9. DETAILED IMPLEMENTATION PLAN

### Phase 0: Pre-Fieldwork (Today/Tomorrow — URGENT)

**Goal**: Identify high-potential sites for A.03 fieldwork before Monday.

```
IF sites are NOT identified yet:
  → Drop everything else
  → Use Working Continuity Index to select sites
  → Prepare fieldwork plan (route, what to document)
  → This is the actual studio deliverable

IF sites ARE already identified:
  → Proceed to Phase 1
```

### Phase 1: Foundation (Saturday–Sunday, W3)

**Goal**: Git repo + n8n running. 60 minutes total.

**Step 1 — Git repo (20 min)**
```bash
# Andrea creates repo on github.com
# → "city101" → Public → MIT → init with README

# Clone locally
cd ~/CLAUDE/City101_ClaudeCode
git clone https://github.com/[username]/city101.git
cd city101

# Set up LFS
git lfs install
# Create .gitattributes (from Section 3.4)

# Create directory structure
mkdir -p datasets/{raw,processed} research/references findings dead_ends \
  narrative/{versions,feedback} design_system scripts/{data,viz,rhino,blender,qgis,n8n} \
  models/{spatial_plans,exports} output/{maps,viz,models,staging} \
  deploy/{website,booklet,print} process/{prompts,screenshots,reflections} \
  session_logs digests handoffs/archive .claude/commands/roles
```

**Step 2 — Core files (15 min)**
```bash
# Write CLAUDE.md (governance + router, ≤80 lines)
# Write LOCKBOARD.md (current tasks from latest handoff)
# Write .gitignore
```

**Step 3 — Migrate existing work (15 min)**
```bash
# Copy CSVs → datasets/processed/
# Copy scripts → scripts/data/
# Copy historical handoffs → handoffs/archive/
# Copy prompts → process/prompts/
# Write datasets/inventory.md
```

**Step 4 — Initial commit + push (5 min)**
```bash
git add -A
git commit -m "[META] Initialize City101 repository — system architecture v4"
git push
```

**Step 5 — Henna syncs (5 min)**
```bash
# Henna clones
git clone https://github.com/[username]/city101.git
cd city101
git lfs install
# Done — she can read lockboard, pull updates, push her branches
```

### Phase 2: n8n Installation (Sunday evening or W4, 30 min)

**Goal**: n8n instance running, n8n-MCP connected to Claude Code.

**Step 1 — Install n8n**
```bash
# Option A: Docker (recommended — clean, isolated)
docker run -d --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
# Access at http://localhost:5678

# Option B: npm (if no Docker)
npm install -g n8n
n8n start
```

**Step 2 — Install n8n-MCP for Claude Code**
```bash
npm install -g n8n-mcp

# Add to Claude Desktop config (claude_desktop_config.json):
# {
#   "mcpServers": {
#     "n8n": {
#       "command": "npx",
#       "args": ["n8n-mcp"]
#     }
#   }
# }
```

**Step 3 — Install n8n-skills for Claude Code**
```bash
git clone https://github.com/czlonkowski/n8n-skills.git
cp -r n8n-skills/skills/* ~/.claude/skills/
# Claude Code now knows how to build n8n workflows correctly
```

**Step 4 — Get Anthropic API key**
```
# Go to console.anthropic.com
# Create API key for n8n (separate from personal use)
# Store in n8n credentials (never in repo)
```

**Step 5 — Connect GitHub webhook**
```
# GitHub repo → Settings → Webhooks → Add webhook
# Payload URL: [n8n webhook URL from Push Notifier workflow]
# Content type: application/json
# Events: Pushes, Pull requests
```

### Phase 3: First Automation (W4, after A.03 fieldwork)

**Goal**: Push Notifier workflow — the simplest, highest-value automation.

Tell Cairn Code (with n8n-MCP):
```
Build an n8n workflow called "Push Notifier":
- Trigger: GitHub webhook on push events
- Action: Extract branch name, commit messages, and author
- Action: Format a message: "[author] pushed to [branch]: [first commit message]"
- Action: Send to Discord webhook URL: [your-discord-webhook]
- Test with a real push to the repo
```

Cairn Code uses n8n-MCP to build this node by node, test each step, and deploy it. Takes ~10 minutes.

**Validation**: Push a test commit. Discord message should appear within seconds.

### Phase 4: Core Automation (W5)

**Goal**: Auto-Summarizer + Lockboard Watcher.

**Auto-Summarizer workflow** (tell Cairn Code):
```
Build an n8n workflow called "Auto-Summarizer":
- Trigger: GitHub webhook on push with 3+ files changed
- Action: Fetch the commit diff via GitHub API
- Action: Call Claude API (claude-haiku-4-5) with prompt:
  "Summarize these git commits into a session log following this template:
   [L1 template from spec]. Keep it under 200 lines."
- Action: Write result to session_logs/[date]_auto.md
- Action: Commit with message "[AUTO] Session summary"
- Action: Push to repo
```

**Lockboard Watcher** (tell Cairn Code):
```
Build an n8n workflow called "Lockboard Watcher":
- Trigger: GitHub webhook on push where LOCKBOARD.md is in changed files
- Action: Fetch new LOCKBOARD.md content via GitHub API
- Action: Call Claude API to extract: who claimed what, any new completions
- Action: Format notification message
- Action: Send to Discord: "🔒 Lockboard update: [summary]"
```

### Phase 5: Event-Driven Memory (W6, before midterm)

**Pre-Event Digest** (tell Cairn Code):
```
Build an n8n workflow called "Pre-Event Digest":
- Trigger: Manual or scheduled (set dates for known crits)
- Action: Fetch all files in session_logs/ via GitHub API
- Action: Fetch previous digest from digests/ (if exists)
- Action: Call Claude API (claude-sonnet-4-6) with prompt:
  "Synthesize these session logs into a weekly digest following this template:
   [L2 template from spec]. Reference the previous digest for continuity."
- Action: Write to digests/[event_name].md
- Action: Commit + push with "[AUTO] Digest: [event_name]"
```

### Phase 6: Full System (W8+, post-Easter, only if needed)

CSV Validator, Branch Merge Logger, Booklet Collector — only build these if the core system proves valuable.

---

## 10. HUMAN COORDINATION (Andrea + Henna)

### 10.1 Shared Interface

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
            LOCKBOARD + TEAM_HANDOFF
            Discord notifications (from n8n)
```

### 10.2 Daily Sync (2 minutes — or fully automated)

**Manual (W3–W4)**:
```
Start: Read LOCKBOARD → Claim → Go
End:   Update LOCKBOARD → Commit → Push
```

**Automated (W5+, once n8n Push Notifier is active)**:
```
Start: Read LOCKBOARD (Discord already told you what changed overnight)
End:   Commit → Push (n8n notifies partner automatically)
```

The lockboard stays manual. The notifications become automatic. That's the sweet spot.

---

## 11. THE BOOKLET

Two stories: the corridor (architecture) and the workflow (AI).

The semester arc from handoffs W1 onward documents the evolution: handoff system (Sept 2025) → workflow document (Feb 2026) → system architecture (Mar 2026) → n8n automation (Mar–Apr 2026) → operating multi-agent team (May 2026).

n8n Booklet Collector workflow (Phase 6) can auto-identify "booklet-worthy" moments. But even without it, the git commit log + session logs + digests ARE the raw material.

---

## 12. OPEN QUESTIONS

1. **A.05 brief**: Integrate when released.
2. **Blender MCP**: Both Andrea and Henna approve installation. Same security as Rhino.
3. **n8n hosting**: Docker on Andrea's machine? Henna's machine? A shared cloud instance? Docker-on-laptop is simplest but only runs when laptop is on.
4. **Discord vs Slack vs email for notifications**: Discord is likely simplest (free, webhook-native). What do you and Henna use?
5. **Anthropic API costs**: Haiku is cheap (~$0.003/1K tokens). Budget ~$5/month. Monitor usage.
6. **Claude Cowork / VS Code extension**: Worth exploring alongside n8n-MCP, not instead of it.

---

## 13. RISKS AND MITIGATIONS

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| n8n setup takes too long | Medium | Phase 2 is only 30 min. If it goes wrong, skip — manual lockboard still works. |
| n8n Docker eats system resources | Low | Lightweight container (~200MB RAM). Stop when not needed. |
| Auto-Summarizer produces bad summaries | Medium | Use Haiku (fast, cheap), human reviews L1 before it feeds L2. |
| API costs spike | Low | Haiku + rate limiting in n8n. Budget ceiling in Anthropic console. |
| Lockboard gets stale | Medium | Push Notifier + Lockboard Watcher make staleness visible. |
| Henna doesn't adopt system | Medium | Start with JUST lockboard + Discord notifications. Lowest friction. |
| Three parallel assignments overwhelm | High | Lockboard Assignment column makes pressure visible. n8n notifications prevent silent duplication. |

---

*This document lives at `process/SYSTEM_ARCHITECTURE.md` in the repo. v5 will incorporate lessons from first 2 weeks of operation.*
