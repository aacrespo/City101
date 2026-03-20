# Andrea — Working Context

**Owner**: Andrea (Cairn, Cairn Code, Lumen)
**Last updated:** 2026-03-18 (repo restructuring session)

---

## Current priorities

### A04 — midterm (due March 30)
1. **Rhino modeling**: LOG 400 upgrades for lock scripts. 3 scripts verified (Morges, CHUV, Rennaz) at LOG 200-300. 9 nodes defined in v2 paper — need to decide which to model at what LOD for midterm.
2. **App/interface architecture**: Design the typology generator system — Mermaid diagram, module definitions, data flow. Prompt written for systems architect session.
3. **Midterm PPTX** — 6-screen template (see `briefs/Templates/`)
4. **Finalize project concept** — lock down narrative so Henna can prompt slides from it
5. **Check other repo** for useful commands/automations to import

### Completed
- ✅ A03 deliverables submitted
- ✅ All 7 field sites visited (March 10)
- ✅ March 16 crit — green light from Huang, funding offered
- ✅ v2 research paper written — now at `deliverables/A04/city101_vertical_transport_research_v2.md`
- ✅ Brain dump captured (`handoffs/braindump_2026-03-17_three-things.md`)
- ✅ Repo restructured (March 18) — files promoted, copies renamed, hooks added, indexes updated

## Handoff

**What was done (March 19-20 — Rhino multi-instance + agent team session):**
- Built Rhino router MCP server (1209 lines, 31 tools, TCP transport)
- Forked rhinomcp C# plugin for configurable ports (`mcpstart 9001`)
- Discovered Mac limitation: one Rhino process only — router is the path
- Tested with 7-agent team on Lock 05 CHUV: 709 objects, 4 build rounds
- Created `workflows/agent-team-modeling.md` from the test results
- Full session log at `experiments/rhino mcp server/SESSION_LOG.md`

**What's next:**
1. **Prototypology at scale** — use agent team workflow for remaining nodes
2. **PR upstream** — plugin port fix is clean, good candidate for `jingcheng-chen/rhinomcp`
3. **Henna setup** — documented in `experiments/rhino mcp server/SETUP.md`
4. **Midterm prep** — modeling + slides (due March 30)
5. **Merge branch to main** when ready

**Watch out for:**
- `.mcp.json` is back to standard `uvx rhinomcp` (port 1999). To use router: copy `experiments/rhino mcp server/mcp_router.json` to `.mcp.json` and restart Claude Code
- Modified plugin is installed — `mcpstart` now prompts for port. Just press Enter for default 1999
- Henna doesn't have the modified plugin yet
- Ramp grades in existing scripts too steep for SIA 500 (35% and 26.7% vs 6% limit)

**Key files:**
- `experiments/rhino mcp server/` — router, setup docs, session log
- `workflows/agent-team-modeling.md` — agent team modeling workflow (from 7-agent test)
- `output/city101_hub/rhino_scripts/lock_05_chuv_gradient_v5_agent_team.py` — CHUV script (709 objects)
- `~/repos/rhinomcp` — forked plugin (branch `feature/configurable-port`)
- `LOCKBOARD.md` — task split for midterm

## Data verification gaps
- **Night worker counts unsourced** — 4,600 / 1,680 / 1,500 / 400 / 300 / 730 are load-bearing claims with no CSV source. Need: OFS employment data, hospital annual reports, or field visit interviews.
- **Hospital ratings** (Rennaz 2.6★, Nyon 3.4★) — not in station ratings CSV. Likely from Google directly, needs confirmation.
- **"Zero nocturnal transport" overstated** — real dead window is 01:00–05:00, not all night. Late-night frequency: Bussigny 9.0 tr/hr, Nyon 7.0, Montreux 10.5, Lausanne 22.0.
- **Renens commuter index**: JSX says 2.48×, dataset says 2.04.

## Session log

> For sessions before March 2 (pre-git), see `handoffs/` (S1–S11, Feb 17 → Mar 1).

| Date | Account | What happened |
|------|---------|---------------|
| 02-03 | Cairn Code | Scrollytelling site: 7 static maps → interactive Leaflet. Print exports (7 PNG + 7 PDF, dark bg). |
| 04-03 | Cairn + Cairn Code | Animation data pipeline: 4 agents (GTFS, ridership, demographics, geometry). Phase 1 QA'd. v2/v3 validated. CLAUDE.md v2 rebuilt. Agent team commands created. |
| 08-03 | Cairn Code | Narrowed 24→6 sites. Healthcare supply chain narrative. Relay-Lock prototypology. Data verification. |
| 09-03 | Cairn Code | Expanded to 7 sites (added Montreux-Glion). Full field visit protocol. |
| 09-03 | In person | **Western corridor field visit** (Geneva North → Nyon → Morges → Crissier-Bussigny). Findings not yet documented. |
| 10-03 | Cairn Code | Migrated old repo → git. All files organized. CONTEXT.md updated. |
| 10-03 | Cairn Code | Git workflow setup: GitHub App, PR test, session commands updated, conventions updated, CONTEXT split. |
| 11-03 | Cairn Code | Workflow infrastructure session: Claude's Corner (shared creative space), `/brain-dump` command + `prompt-craft.md` rules, `/team` command for dynamic agent assembly, agent definitions for all 5 roles, retro + handoff integrated into session-end, break/lunch reminders in session-start. 6 commits. Also: field visit update — all 7 sites visited Monday (ahead of schedule), but on-site interviews blocked everywhere (pharmacies, hospitals, post offices all said to contact central offices). |
| 15-03 | Cairn Code | Built AI workflow diagram v1 for A04 midterm (6-screen HTML, tmux aesthetic, City101 design system). 6 panels: terminal workflow, repo file tree, prototypology flow, differentiators, agent roles, handoff system. Play animation + hover interactions. Henna takes over for v2. |
| 15-03 | Cairn Code | Transport Pulse v3: multimodal 24h animation (29,135 trips, all modes). MapLibre 3D terrain, dot/vector render modes, analytics sidebar (donut, sparkline, mode bars, direction, pulse), symbology overhaul (ferry wake, IC bright edge, funicular cable, size hierarchy), keyboard help panel, dead window label fix. 3 pipeline scripts + 21MB self-contained HTML. |
| 16-03 | Cairn Code | Healthcare supply chain diagram v1→v3 for A04 midterm. v3 = 4-layer gap analysis (emergency, staff, supply, facility access). Integrated Henna's 112-row dataset. Confirmed: only 1 24h pharmacy on 101km corridor. |
| 16-03 | Cairn Code | Relay-Lock Prototypology Explorer v1: HTML app (60KB, 7 nodes, 8 flows, particle animation, time slider, lock detail panels). 3 Rhino scripts at LOG 200-300 (Morges, CHUV, Rennaz). Configured Rhino MCP for Claude Code. Presented to teachers. v2 plan approved (LOG 400 + site context + point cloud pipeline). |
| 17-03 | Cairn Code | Strategic session: Huang research (Blue City, generative AI, digital twins). Framing insight — project is a skill environment, not "agentic workflow." No code/data work. |
| 18-03 | Cairn Code | Brain dump session: captured evolved concept (9 nodes, "holds the gap", anti-urban), app interface vision, modeling status assessment. Updated CONTEXT.md + CONTEXT_ANDREA.md. Wrote systems architect prompt. Committed all pending files. |
| 18-03 | Cairn Code | Repo restructuring: promoted outputs, archived superseded, renamed copies, prefixed prompts. Hooks (time/breaks/compaction) + new commands (save-session, resume-session, unlock). Task split documented. Equal team framing. 4 commits, 51+ files. |
| 19-03 | Cairn Code | Rhino multi-instance: built router MCP server (31 tools, TCP), forked rhinomcp plugin for custom ports, discovered Mac single-process limit. Tested 7-agent team on Lock 05 CHUV (709 objects). Created agent-team-modeling workflow. |
