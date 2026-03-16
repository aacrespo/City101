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

**What was done:** Built healthcare supply chain diagram v1→v3 for A04 midterm PPTX. v1 is an interactive explorer (tooltips, time toggles, side panel). v2 is a split-view Day vs Dead Window at 1920×1080. v3 is the final version: 4 stacked layers (Emergency Response, Staff Access, Supply Chain, Facility Access), each showing the same 101km corridor split into Day vs Dead Window. Designed for screenshot → PPTX. Integrates Henna's 112-row medical supply chain dataset. Key finding confirmed: only 1 pharmacy open 24h on the entire 101km corridor (Pharma24 at HUG).

**What's next:**
1. **Screenshot v3** for PPTX — open in Chrome, DevTools → 1920×1080 → Capture Full Size Screenshot
2. **Continue A04 midterm** — other diagrams/visualizations needed for 6-screen display
3. **Henna** should review v3 and add any missing facilities from her dataset
4. Transport Pulse v3 still needs browser test + basemap fix

**Watch out for:**
- v3 auto-scales to viewport but is designed at 1920×1080 — screenshot at that resolution for best results
- CHUV ER cases = 92,674 (from Henna's data) — different from the "NOT FOUND" in v1 research
- Pharma24 at HUG = only 24h pharmacy. "Pharmacie 24 Lausanne" is NOT 24h despite name (closes at midnight)

**Files to look at:**
- `deliverables/A04/healthcare_chain_diagram_v3.html` — final 4-layer gap analysis (USE THIS)
- `deliverables/A04/healthcare_chain_diagram_v2.html` — split-view version (backup)
- `deliverables/A04/healthcare_chain_diagram.html` — v1 interactive explorer
- `deliverables/A04/healthcare_chain_research.md` — full sourced research document
- `output/healthcare_chain/city101_medical_supply_chain_v2.numbers` — Henna's 112-row dataset

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
