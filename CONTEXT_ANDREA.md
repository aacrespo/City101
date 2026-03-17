# Andrea — Working Context

**Owner**: Andrea (Cairn, Cairn Code, Lumen)
**Last updated:** 2026-03-18

---

## Current priorities

### A04 — midterm (due March 30)
1. **Rhino modeling**: LOG 400 upgrades for lock scripts. 3 scripts verified (Morges, CHUV, Rennaz) at LOG 200-300. 9 nodes defined in v2 paper — need to decide which to model at what LOD for midterm.
2. **App/interface architecture**: Design the typology generator system — Mermaid diagram, module definitions, data flow. Prompt written for systems architect session.
3. **CONTEXT.md + repo cleanup**: Context updated (March 18). Repo needs restructuring — promote files from output/, reorganize folders, apply CLAUDE.md-as-map pattern.
4. **Midterm PPTX** — 6-screen template (see `briefs/Templates/`)
5. **v2 research paper**: `output/city101_vertical_transport_research_v2.md` — defines 9 nodes, scoring framework, full concept. Canonical reference.

### Completed
- ✅ A03 deliverables submitted
- ✅ All 7 field sites visited (March 10)
- ✅ March 16 crit — green light from Huang, funding offered
- ✅ v2 research paper written
- ✅ Brain dump captured (`output/braindump_2026-03-17_three-things.md`)

## Handoff

**What was done (March 17-18):**
- Brain dump session: captured evolved concept, app vision, modeling status assessment
- Updated CONTEXT.md with 9-node system from v2 paper, "holds the gap" framing, crit outcome
- Committed all pending output files and research
- Wrote prompt for systems architect session (app architecture Mermaid diagram)

**What's next:**
1. **Repo restructuring session** — promote files from output/, reorganize folders, apply CLAUDE.md-as-map pattern, Henna task split
2. **Systems architect session** — app architecture diagram in Mermaid (prompt ready in `prompts/`)
3. **Rhino modeling sessions** — LOG 400 upgrades, review panel execution (Wave 4)
4. **Midterm framing**: lead with design methodology and knowledge architecture, not AI buzzwords

**Watch out for:**
- Rhino MCP is configured (`.mcp.json`) — restart Claude Code to activate
- Scripts are in `output/city101_hub/rhino_scripts/` — can also run manually in Rhino's Python editor
- Wave 3 tooling (skills + review agents) is scaffolded but untested
- Ramp grades in existing scripts too steep for SIA 500 (35% and 26.7% vs 6% limit)

**Key files:**
- `output/braindump_2026-03-17_three-things.md` — full brain dump (concept, app vision, modeling)
- `output/city101_vertical_transport_research_v2.md` — v2 paper (9 nodes, scoring, concept)
- `output/city101_hub/rhino_scripts/` — 3 lock chamber scripts (LOG 200-300)
- `~/.claude/plans/humming-wishing-minsky.md` — modeling pipeline plan

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
