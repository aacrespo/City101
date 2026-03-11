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

**What was done:** Pure workflow/infrastructure session. Built Claude's Corner (shared creative space in `claudes-corner/`), `/brain-dump` command (voice/messy input → structured prompts), `/team` command (dynamic agent team assembly), agent definitions for all 5 roles (`.claude/agents/`), and integrated retro + handoff + break reminders into session-start/end. `prompt-craft.md` added to auto-loaded rules.

**What's next:**
1. Finish doc review pass (still in progress)
2. Document field visit findings — all 7 sites visited Monday, no eastern trip needed
3. Get Henna onboarded to git repo
4. Start A04 prototypology planning (midterm TODO list exists)

**Watch out for:**
- Haven't pushed to remote yet — do `git push` when ready
- On-site interviews were blocked everywhere — staff at pharmacies, hospitals, post offices all refused and said to contact central offices. Need alternative data sourcing strategy (central office contacts, OFS data, annual reports).
- Henna still not onboarded to new repo — soft blocker for collaboration

**Files to look at:**
- `.claude/commands/brain-dump.md` — new command
- `.claude/commands/team.md` — new command
- `.claude/rules/prompt-craft.md` — new auto-loaded rules
- `.claude/agents/` — 5 agent definitions (analyst, cartographer, visualizer, builder, modeler)
- `claudes-corner/2026-03-11_opening-day.md` — first corner entry

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
