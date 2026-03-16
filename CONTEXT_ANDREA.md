# Andrea — Working Context

**Owner**: Andrea (Cairn, Cairn Code, Lumen)
**Last updated:** 2026-03-10

---

## Current priorities

### A03 deliverables (due March 10)
1. **Investigation report** — text, images, updated maps from field visit. ⚠️ [NEEDS: field visit findings, photos, verification table]
2. **Combined path dataset** — CSV/GeoJSON of investigated sites. ⚠️ [NEEDS: GPS coordinates from field visit, verified claims]
3. **Networked intervention concept** — the relay-lock as strategy. 🟡 [Concept exists, needs writeup]
4. Submit path dataset to Drive: [00-student-paths-datasets](https://drive.google.com/drive/folders/1excOP2HKgnr9jiqCYVhdgHcd3y33cdin?usp=drive_link)

### A03 remaining fieldwork
5. **Friday March 13** — eastern corridor visit: CHUV, Montreux-Glion, Rennaz (3 sites)

### A04 (due March 30 — midterm)
6. **Rhino MCP prototypology** — siteless project adaptable to different sites
7. **Midterm PPTX** — 6-screen template (see `briefs/Templates/`)
8. **Point-cloud sections** of potential sites (A03 requirement, not yet done)

## Handoff

**What was done:** Strategic session — researched Huang's current work (Blue City digital twin, generative AI publications, "Artificial Architecture" exhibition). Key insight: the project should be framed as a **skill environment / human-AI collaboration methodology**, not as "an agentic workflow." The term ages fast; the design principle doesn't. Saved to memory for midterm framing.

**What's next:**
1. **Run v2 plan** — see `~/.claude/plans/elegant-humming-stream.md`
   - Session A (research): terrain data + point cloud deep dive + build skills/agents/rules
   - Session B (Rhino MCP): test scripts → LOG 400 upgrade with 5-reviewer panel
2. **Open the HTML** to test it: `open output/city101_hub/city101_prototypology.html`
3. Transport Pulse v3 still needs browser test + basemap fix
4. **Midterm framing**: lead with design methodology and knowledge architecture, not AI buzzwords

**Watch out for:**
- Rhino MCP is configured (`.mcp.json`) — restart Claude Code to activate
- Scripts are in `output/city101_hub/rhino_scripts/` — can also run manually in Rhino's Python editor
- HTML works from file:// but needs internet for CDN libs (D3, Leaflet) and map tiles
- `source/00-datasets 2/lhiamrossier/GPKG/` may have building heights — inspect in next session

**Files to look at:**
- `output/city101_hub/city101_prototypology.html` — Relay-Lock Explorer v1
- `output/city101_hub/rhino_scripts/` — 3 lock chamber scripts (LOG 200-300)
- `~/.claude/plans/elegant-humming-stream.md` — v2 plan (approved)

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
