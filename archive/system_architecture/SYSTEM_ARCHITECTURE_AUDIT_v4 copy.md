# SYSTEM ARCHITECTURE AUDIT — City101 Multi-Agent Workflow
### Independent Review of SYSTEM_ARCHITECTURE_City101_v4.md
**Reviewer**: Systems engineering perspective (agentic workflows + architecture studios)
**Date**: 2026-03-08
**Reviewed for**: Andrea Crespo & Henna Rafik — EPFL BA6 Studio Huang
**Constraint**: Implementation must be complete by Sunday evening (2026-03-09)

---

## EXECUTIVE SUMMARY

The v4 spec is architecturally sound but operationally oversized for a 2-person student team with 11 weeks remaining. This audit consolidates every recommendation made during the review conversation, incorporating the discovery of Claude Code's native `/loop` and scheduled task features — which eliminate the need for n8n entirely.

**Core thesis of this audit**: The spec's instincts are right (capture decisions, route context, reduce friction, coordinate humans + agents). The implementation layer needs to be thinner. The right tool for automation is Claude Code itself, not an external orchestration platform.

---

## PART 1: WHAT THE SPEC GETS RIGHT

These elements should survive into v5 unchanged or with minor refinement.

### 1.1 The problem diagnosis is accurate
The primary pain (silent duplication between Andrea and Henna), secondary pains (context loss, quality rework, tool sprawl), and the recognition that handoffs depend on discipline at the worst possible moment — all correct. The system needs to solve these.

### 1.2 Memory as a cache hierarchy (L0–L4)
The conceptual model is strong. Commit logs (L0) → session summaries (L1) → digests (L2) → CLAUDE.md (L3) → project instructions (L4). This mirrors real cache hierarchies: each level is smaller, more distilled, and read more frequently. Keep this model.

### 1.3 CLAUDE.md as a router, not an encyclopedia
The spec correctly limits CLAUDE.md to ~80 lines that *point to* other files rather than *containing* all context. This is essential for making lower-tier accounts (Lumen, Cadence, Meridian) productive — a focused router loads fast and lets the agent read only what it needs.

### 1.4 Commit prefix convention
Valuable for institutional memory. The prefixes make `git log --oneline` immediately scannable. However, 15 prefixes is too many — see recommendation below.

### 1.5 Phased activation with go/no-go gates
"Each activation is a decision point: did the previous workflow actually help?" — This is the single best sentence in the entire document. Keep this principle and apply it to the spec itself.

### 1.6 Context routing per role
The idea that different roles read different files (Analyst reads datasets/, Cartographer reads design_system/) is genuinely valuable. It's prompt engineering, not org design, and it's the right kind of prompt engineering — scoping context windows for efficiency and relevance.

### 1.7 The shared interface definition (Section 10.1)
Clear domain boundaries between Andrea and Henna, with explicit shared resources. This prevents territorial ambiguity.

---

## PART 2: WHAT NEEDS TO CHANGE

### 2.1 n8n — REPLACE WITH CLAUDE CODE NATIVE FEATURES

**Original spec**: n8n as Docker container + n8n-MCP + n8n-skills + Anthropic API key + GitHub webhooks + Discord webhooks. 9 integration points, ~6-10 hours setup.

**New recommendation**: Use Claude Code's native `/loop` command and scheduled tasks. These were released recently and do exactly what the n8n workflows were designed to do, but from inside Claude Code with zero external dependencies.

**What `/loop` does**: You type `/loop 30m check the lockboard and summarize what changed` and Claude Code runs that prompt every 30 minutes as long as the session is open. Session-scoped, auto-deletes after 3 days, fires between your turns.

**What scheduled tasks do** (via Claude Desktop/Cowork): You define a task once with a prompt and a cadence (hourly, daily, weekly). It runs automatically when the desktop app is open. Task definitions are stored as skill files at `~/.claude/scheduled-tasks/<task-name>/SKILL.md`.

**Mapping the 7 n8n workflows to native features:**

| # | n8n Workflow | Native Replacement | Complexity |
|---|-------------|-------------------|------------|
| 1 | Push Notifier | GitHub Actions YAML (15 lines) → Discord webhook | 30 min setup |
| 2 | Auto-Summarizer | `session-end` skill in Claude Code (runs on command) | 1 hour to write |
| 3 | Lockboard Watcher | GitHub Actions on LOCKBOARD.md change → Discord | 30 min setup |
| 4 | Pre-Event Digest | Scheduled task in Claude Desktop (weekly or pre-crit) | 30 min setup |
| 5 | CSV Validator | Sub-agent skill invoked by Analyst role before commit | Built into role |
| 6 | Branch Merge Logger | Skip entirely | 0 |
| 7 | Booklet Collector | Skip entirely — git log + session logs ARE the material | 0 |

**Total setup time**: ~3 hours vs. 6-10 hours for n8n.
**Dependencies eliminated**: Docker, n8n instance, n8n-MCP, n8n-skills, Anthropic API key management.
**What you lose**: True event-driven automation (n8n fires on webhooks even when you're not at your computer). For a semester project where work only happens when humans are present, this isn't a meaningful loss.

### 2.2 Agent roles — CONSOLIDATE FROM 11 TO 4+1

**Original spec**: 11 roles (Researcher, Analyst, Narrator, Cartographer, Visualizer, Modeler, Builder, Coordinator, Summarizer, Documenter, Automator).

**New recommendation**: 4 production roles + 1 utility skill.

| Keep | Why it's distinct |
|------|-------------------|
| **Analyst** | Unique context: datasets/, APIs, scripts/data/. Unique tools: API calls, CSV processing. Absorbs Researcher (same workflow in practice — you find data and process it in the same session). |
| **Cartographer** | Unique context: QGIS MCP, design system, print layouts. Fundamentally different tool and output from Analyst. |
| **Visualizer** | Unique context: Leaflet/D3/HTML. Different output format from Cartographer despite both being "visual." |
| **Builder** | Unique context: deploy/, website assembly, booklet. Absorbs Narrator (narrative is part of assembly, not standalone). |

| Merge/Cut | Where it goes |
|-----------|---------------|
| Researcher → **Analyst** | Same workflow: find data, process data, output CSV. |
| Narrator → **Builder** | Narrative is part of assembling the deliverable. |
| Modeler → **Keep only if A.04/A.05 need it** | Premature until Rhino work is substantial. Create it when needed. |
| Coordinator → **Session-start prompt, not a role** | "Read CLAUDE.md and lockboard, recommend highest-value task." 2-minute interaction, not a persistent agent. |
| Summarizer → **session-end skill** | Automated by the session-end skill, not a human-assigned role. |
| Documenter → **Cut** | The git log + session logs + digests ARE the documentation. A dedicated role produces meta-noise. |
| Automator → **Cut** | Was n8n-specific. No longer needed. |

**The test for whether a role should exist**: Does it need *different files* in its context window than other roles? If yes, keep it. If it reads the same files but has a different "personality," merge it.

### 2.3 Skill file format — ADOPT YAML FRONT MATTER

**Original spec**: Role commands as markdown files in `.claude/commands/roles/`.

**New recommendation**: Write them as skill files with YAML front matter, following the Claude Code skill convention. This means they work natively with Claude Code's skill system and sub-agent delegation.

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
- Producing findings or documenting dead ends

## Context to load
1. CLAUDE.md (always first)
2. datasets/inventory.md
3. research/api_notes.md
4. The specific dataset(s) being processed

## Quality gate (run before every commit)
- [ ] Output CSV has canonical station IDs where applicable
- [ ] Coordinates are in LV95 (EPSG:2056) or clearly labeled WGS84
- [ ] Check dead_ends/ — has this analysis been attempted before?
- [ ] Data inventory updated with new/modified dataset
- [ ] Null counts and row counts printed in summary
- [ ] API rate limits respected (min 0.25s between calls)

## Commit prefix
[DATA] for datasets, [FIND] for analytical findings, [DEAD] for dead ends

## Autonomy
- Can read and write files freely within datasets/ and scripts/data/
- Can make API calls (state which API and why before calling)
- Must ask before paid APIs or APIs not previously used
- Auto-commit with appropriate prefix
```

Each of the 4 roles gets a file like this. The quality gate section is the most valuable part — it's an integrated checklist that runs where the work happens, not as a separate review step.

### 2.4 Commit prefixes — REDUCE FROM 15 TO 7

**Original**: DATA, FIND, DEAD, MAP, NARR, DECIDE, SCRIPT, AGENT, FIX, VIZ, MODEL, SYNC, META, BUILD, AUTO

**New recommendation**: 7 prefixes that map to the 4 roles + coordination.

| Prefix | Meaning | Used by |
|--------|---------|---------|
| [DATA] | Dataset created/modified/enriched | Analyst |
| [FIND] | Analytical finding or pattern discovered | Analyst |
| [DEAD] | Dead end documented | Analyst |
| [MAP] | Static map or QGIS output | Cartographer |
| [VIZ] | Interactive visualization | Visualizer |
| [BUILD] | Website/booklet/deploy output | Builder |
| [SYNC] | Coordination: lockboard, handoff, session log, merge | System |

Cut: NARR (merged into BUILD), DECIDE (decisions go in CLAUDE.md, not their own commits), SCRIPT (scripts serve a role — commit with that role's prefix), AGENT (unnecessary meta-prefix), FIX (use the role prefix of what you're fixing), MODEL (add back if Rhino work starts), META (merged into SYNC), AUTO (no longer needed without n8n).

### 2.5 Branch strategy — SIMPLIFY

**Original**: main + andrea/* + henna/* + agent/cairncode/* + agent/lumencode/* + agent/cadencecode/* + agent/meridiancode/* + docs/*

**New recommendation**: 3 branch types.

```
main                    ← stable, reviewed outputs only
├── andrea/[task-slug]  ← Andrea's work (any of her Claude instances)
└── henna/[task-slug]   ← Henna's work (any of her Claude instances)
```

Agent-prefixed branches add merge overhead without benefit — it doesn't matter which Claude instance produced the work, it matters which human is responsible. The `docs/` prefix is unnecessary; documentation lives on the human's branch.

### 2.6 Repository structure — FLATTEN

**Original**: 20+ directories with sub-directories.

**New recommendation**: Fewer directories, same organizational clarity.

```
city101/
├── CLAUDE.md                      ← Router (~80 lines)
├── LOCKBOARD.md                   ← (if using git for coordination)
├── .gitattributes                 ← LFS rules
├── .gitignore
├── README.md
│
├── datasets/
│   ├── inventory.md               ← What exists, where it came from
│   ├── raw/                       ← Unmodified source data
│   └── processed/                 ← Enriched, cleaned, analysis-ready
│
├── findings/                      ← Analytical findings (markdown)
├── dead_ends/                     ← What was tried and abandoned (and why)
│
├── output/
│   ├── maps/                      ← QGIS exports, print layouts
│   ├── viz/                       ← Interactive HTML visualizations
│   └── models/                    ← 3D model exports (when needed)
│
├── design_system/                 ← Colors, fonts, component specs
│
├── scripts/                       ← All code, organized by purpose
│   ├── data/                      ← Data processing scripts
│   ├── viz/                       ← Visualization generation
│   └── qgis/                      ← QGIS-specific scripts
│
├── deploy/
│   ├── website/                   ← A.02 scrollytelling site
│   └── booklet/                   ← Process booklet
│
├── session_logs/                  ← L1: per-session summaries
│
├── process/                       ← Process documentation for booklet
│   └── prompts/                   ← Saved prompts worth keeping
│
└── .claude/
    ├── skills/
    │   ├── analyst/skill.md
    │   ├── cartographer/skill.md
    │   ├── visualizer/skill.md
    │   ├── builder/skill.md
    │   └── session-end/skill.md
    └── agents/
        └── summarizer/agent.md    ← Haiku sub-agent for cheap summaries
```

**Cut**: research/ (findings and dead_ends cover this), narrative/ (part of deploy/), models/inventory.md (premature), handoffs/archive/ (session_logs replaces this), digests/ (CLAUDE.md IS the digest).

### 2.7 Coordination layer — USE WHATSAPP + GITHUB, NOT LOCKBOARD.md

**Original**: LOCKBOARD.md in git repo, updated at session start and end (4 touchpoints per session).

**The problem**: Updating a markdown file in git requires: open terminal → edit file → git add → git commit → git push. Too much friction for real-time coordination.

**New recommendation (2 options)**:

**Option A — WhatsApp-native (simplest)**:
Create a WhatsApp group called "City101 lockboard." Pinned message format:
```
🔒 Andrea: working on EV charging map (A.02)
🔒 Henna: transit ridership analysis (A.02)
✅ Andrea: finished OCM enrichment v3
```
Update it from your phone in 5 seconds. No git ceremony. LOCKBOARD.md in the repo becomes a weekly snapshot of the pinned message, committed during session-end.

**Option B — Notion (if you want structure)**:
Shared Notion database with columns: Task, Assignment (A.02/A.03/A.04), Status (Available/In Progress/Done/Blocked), Claimed By, Branch. Both of you can update from phone or browser. GitHub Actions can post to Notion via API on every push (free, runs on GitHub servers).

**Either way**: Git owns the work. The coordination tool (WhatsApp/Notion) owns the real-time status. Decisions made in WhatsApp/Notion must land in the git repo (CLAUDE.md or a commit message) before end of day, or they evaporate.

### 2.8 Memory hierarchy — SIMPLIFY TO 3 LEVELS

**Original**: L0 (git commits) → L1 (session logs) → L2 (digests) → L3 (CLAUDE.md) → L4 (project instructions)

**New recommendation**: 3 operational levels.

| Level | What | Updated | By whom |
|-------|------|---------|---------|
| **Git log** | Every commit message | Real-time | Automatic |
| **Session logs** | Per-session summary with decisions + dead ends | End of session | session-end skill |
| **CLAUDE.md** | Distilled state: current tasks, recent decisions, dead ends, pointers to files | End of session (auto-updated by session-end skill) | session-end skill + human review |

L2 (digests) becomes unnecessary because CLAUDE.md IS the running digest. If it gets too long (>100 lines), that's the signal to archive older decisions into `findings/` or `dead_ends/` and trim CLAUDE.md back down.

L4 (project instructions) stays but it's just the safety rules and stable conventions — it doesn't need a number in the hierarchy.

### 2.9 Quality control — ADD EXPLICIT GATES

**Original spec gap**: No definition of "done" for deliverables. No peer review mechanism. CSV Validator deprioritized to Phase 4.

**New recommendation**: Quality is built into each skill file as a checklist (see 2.3 above), plus three additional measures:

**A. Pre-commit checklist in session-end skill**: Before committing, the session-end skill runs through a general checklist:
- Were any new datasets created? → Update inventory.md
- Were any dead ends discovered? → Write to dead_ends/ with rationale
- Were any design decisions made? → Update CLAUDE.md "Recent decisions" section
- Does this output need to be registered? → Update output/registry.md if applicable

**B. Cross-review convention**: Andrea reviews Henna's merges to main. Henna reviews Andrea's. Not every commit — just merges to main. This is where quality improves for joint deliverables.

**C. Sub-agent validation**: The Analyst skill can invoke a Haiku sub-agent to validate CSVs before commit — check schema, null counts, coordinate system, join against canonical stations. This replaces the n8n CSV Validator at zero infrastructure cost.

### 2.10 Session-end skill — THE KEYSTONE

This is the single most important piece to build. It replaces: handoff files, manual lockboard updates, the summarizer role, and the n8n Auto-Summarizer.

```yaml
---
name: session-end
description: "End-of-session ritual: summarize, update CLAUDE.md, commit, push, notify"
---

# Session End Skill

## When to use
Run this when you're finishing a work session or switching to a different workstream.
Do NOT run this on every commit — only at natural stopping points (1-2x per day).

## Process
1. Read the git diff since last session-end tag
2. Summarize: what was done, what decisions were made, what dead ends found
3. Write session log to session_logs/YYYY-MM-DD_[agent]_S[n].md
4. Update CLAUDE.md:
   - "Current state" section: what changed
   - "Recent decisions" section: any new decisions (with rationale)
   - "Dead ends" section: anything tried and abandoned
   - "Active tasks" section: what's in progress, what's done
5. Run the pre-commit checklist (see quality gates)
6. git add -A
7. git commit -m "[SYNC] Session end — [one-line summary]"
8. git tag session-end-YYYY-MM-DD-SN
9. git push
10. (Optional) Post summary to WhatsApp/Discord if configured
```

### 2.11 Cost estimate — REVISED

| Component | Cost |
|-----------|------|
| GitHub repo + LFS (free tier, 1GB) | $0 |
| GitHub Actions (free tier, 2000 min/month) | $0 |
| Claude subscriptions (existing) | Already paid |
| Anthropic API for sub-agents (if using Haiku for validation/summarization) | ~$2-3/month |
| **Total** | **$0-3/month** |

n8n Cloud ($24/month) eliminated. Docker overhead eliminated.

---

## PART 3: CLAUDE CODE `/loop` AND SCHEDULED TASKS — HOW THEY FIT

### 3.1 What they are

**`/loop`** (CLI, session-scoped): Type `/loop 30m [prompt]` and Claude Code runs that prompt every 30 minutes in the current session. Dies when you close the terminal. Useful for polling ("check if the API finished processing") or ambient monitoring ("check the lockboard every hour").

**Scheduled tasks** (Desktop/Cowork, persistent): Define a task with a prompt and a cadence. Saved as a skill file at `~/.claude/scheduled-tasks/`. Runs automatically when the desktop app is open. Survives restarts. Useful for recurring workflows ("daily briefing", "weekly digest").

### 3.2 What they replace in your spec

| Spec component | Replaced by |
|---------------|-------------|
| n8n Push Notifier | GitHub Actions (free, runs on GitHub servers, always on) |
| n8n Auto-Summarizer | session-end skill (run manually) OR scheduled task (daily auto-summary) |
| n8n Lockboard Watcher | `/loop` in active session OR GitHub Actions |
| n8n Pre-Event Digest | Scheduled task set to day-before-crit dates |
| n8n CSV Validator | Built into Analyst skill as sub-agent call |
| n8n infrastructure (Docker, MCP, API keys) | Nothing — eliminated entirely |

### 3.3 Limitations to understand

- **Session-scoped `/loop` dies when you close the terminal.** Not suitable for 24/7 monitoring. Use GitHub Actions for always-on notifications.
- **Scheduled tasks only run when Claude Desktop is open.** Missed runs execute on next app open, but there's no catch-up for long absences.
- **Recurring tasks auto-expire after 3 days.** You'll need to recreate them if you don't interact for a long weekend (Easter break).
- **No cross-instance coordination.** A `/loop` on Cairn Code doesn't know what Cadence Code is doing. The lockboard (wherever it lives) is still the coordination layer.

### 3.4 Recommended setup

**Immediate (this weekend)**:
- Don't set up any loops or scheduled tasks yet. Get the repo, CLAUDE.md, and skill files working first.

**Week 4 (after proving the manual workflow)**:
- GitHub Actions workflow for Discord push notifications (always-on, free)
- `/loop` for ambient lockboard monitoring during active sessions

**Week 5+ (if manual session-end feels too heavy)**:
- Scheduled task for daily auto-digest (runs every evening, reads that day's commits, writes a summary)

---

## PART 4: IMPLEMENTATION PLAN — SUNDAY BUILD

### Priority order (must-have → nice-to-have)

| # | Task | Time | Criticality |
|---|------|------|-------------|
| 1 | Create GitHub repo + LFS + .gitattributes | 45 min | MUST HAVE |
| 2 | Write CLAUDE.md (seed from latest handoff) | 60 min | MUST HAVE |
| 3 | Write 4 skill files (analyst, cartographer, visualizer, builder) | 90 min | MUST HAVE |
| 4 | Write session-end skill | 45 min | MUST HAVE |
| 5 | Migrate existing datasets and scripts | 60 min | MUST HAVE |
| 6 | Write summarizer sub-agent (Haiku) | 30 min | SHOULD HAVE |
| 7 | Initial commit + push + test clone on Henna's account | 30 min | MUST HAVE |
| 8 | GitHub Actions for Discord notifications | 30 min | NICE TO HAVE |
| 9 | Test full loop: session → work → session-end → new session | 45 min | MUST HAVE |

**Total estimated time: ~7-8 hours**

### What's explicitly deferred

| Item | When to revisit |
|------|----------------|
| n8n (everything) | Only if shell scripts + Claude Code native features prove insufficient (unlikely) |
| Modeler role | When A.04/A.05 Rhino work starts |
| Scheduled tasks / `/loop` | Week 4+, after manual workflow is proven |
| Notion integration | Only if WhatsApp lockboard proves insufficient |
| Cross-review workflow | After midterm, when merges to main become frequent |
| Booklet automation | End of semester — manual curation from git log + session logs |
| CSV Validator as standalone | Built into Analyst skill quality gate instead |

---

## PART 5: RISK MATRIX — REVISED

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Git/LFS setup takes longer than estimated | Medium | Low | LFS is the only tricky part. If it fails, skip LFS initially — add it when first binary file needs tracking |
| CLAUDE.md gets bloated beyond 100 lines | High | Medium | Session-end skill archives old decisions to findings/ or dead_ends/. Hard limit: if >100 lines, trim before commit |
| Session-end skill doesn't get run | High | High | This is the #1 risk. Make it a single command. If even that's too much friction, make it the first thing the NEXT session does (retroactive summarization from git diff) |
| Henna doesn't adopt the system | Medium | High | Start with JUST the repo and WhatsApp lockboard. Zero new tools for her. She commits and pushes; the skill files and CLAUDE.md work invisibly |
| Three parallel assignments overwhelm the system | High | Medium | CLAUDE.md "Active tasks" section makes pressure visible. Quality gates prevent rushing — better to produce 2 good outputs than 4 rough ones |
| Context drift between instances | Medium | Medium | CLAUDE.md as router is the fix. Every session starts by reading it. Session-end updates it. The loop is tight as long as session-end runs |
| Skill files are too prescriptive and agents ignore them | Low | Low | The YAML front matter + quality checklist format is well-tested in Claude Code. Keep skills under 50 lines each |

---

## PART 6: WHAT I WAS WRONG ABOUT

For transparency and because this audit should be honest:

1. **I initially dismissed the role taxonomy too aggressively.** The roles aren't personality descriptions — they're context scoping instructions. That's legitimate prompt engineering. The consolidation from 11 to 4 is still right, but the principle of scoped context per task type is valuable and should be preserved.

2. **I initially recommended a shell script for session-end.** Claude Code's native skill system is better — it runs inside the same environment, has access to the full project context, and can invoke sub-agents. A shell script with curl to the Anthropic API would work but is more fragile and less integrated.

3. **I underestimated the value of the coordinator function.** Not as a persistent role, but as a session-start pattern. "Read everything, recommend what to work on" is genuinely useful when you have 3 parallel assignments and limited time. It just shouldn't be an agent role — it should be the first thing you ask any agent at session start.

---

## APPENDIX: COMPARISON — V4 SPEC VS. AUDIT RECOMMENDATIONS

| Dimension | v4 Spec | This Audit |
|-----------|---------|------------|
| Agent roles | 11 | 4 + 1 utility |
| Automation layer | n8n (Docker + MCP + API) | Claude Code native + GitHub Actions |
| n8n workflows | 7 | 0 (replaced by skills + GH Actions) |
| Coordination tool | LOCKBOARD.md in git | WhatsApp/Notion + weekly git snapshot |
| Memory levels | 5 (L0–L4) | 3 (git log, session logs, CLAUDE.md) |
| Commit prefixes | 15 | 7 |
| Branch strategy | 6+ prefix types | 3 (main, andrea/*, henna/*) |
| Directory count | 20+ | ~15 |
| Skill file format | Markdown commands | YAML front matter skills |
| Quality gates | CSV Validator (Phase 4) | Built into every role skill |
| Setup time | 10-15 hours | 7-8 hours |
| Monthly cost | $0-30 | $0-3 |
| External dependencies | Docker, n8n, n8n-MCP, n8n-skills, Anthropic API, GitHub webhooks | GitHub Actions (free) |

---

*This audit is a snapshot. v5 of the system architecture should incorporate these recommendations and be updated after the first 2 weeks of operation.*
