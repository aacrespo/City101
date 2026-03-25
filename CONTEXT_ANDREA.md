# Andrea — Working Context

**Owner**: Andrea (Cairn, Cairn Code, Lumen)
**Last updated:** 2026-03-25

---

## Current priorities

### A04 — midterm (screen test Fri March 27 / presentation Mon March 30)
1. **Emails TODAY**: EPFL VM services (specs for access) + ENAC (Rhino licenses)
2. **Presentation slides**: Kitchen analogy animation (slide 5), pixel agents concept (slide 5), character emotes v2, healthcare merry-go-round diagram
3. **Modeling**: Rennaz node (Lock 07) with site. "Before" scripts for Crissier-Busigny + Nyon-Genolier (no knowledge base — for before/after comparison)
4. **Infrastructure**: ChromaDB → Qdrant migration, continue embedding, token optimization, auto dream, /loop, DeepSeek, ruflow, lock files consistency

### Completed
- ✅ A03 deliverables submitted
- ✅ All 7 field sites visited (March 10)
- ✅ March 16 crit — green light from Huang, funding offered
- ✅ v2 research paper written — now at `deliverables/A04/city101_vertical_transport_research_v2.md`
- ✅ Brain dump captured (`handoffs/braindump_2026-03-17_three-things.md`)
- ✅ Repo restructured (March 18) — files promoted, copies renamed, hooks added, indexes updated

## Handoff

**What was done (March 25, 02:00–03:15):**
- RCP deep dive: found AIaaS (70+ models, embedding endpoints, OpenAI-compatible API at inference.rcp.epfl.ch). Could replace Gemini for embeddings.
- Discovered DSI runs a VM service (VSI) separate from RCP's HaaS. HaaS is bare metal overkill — VSI is probably what we need. Not publicly documented though.
- Both emails rewritten and humanized: RCP (ask which service fits, mention AIaaS) + ENAC (do you have floating Rhino licenses for VMs)
- Humanizer skill installed (~/.claude/skills/humanizer) — needs Claude Code restart to register as /humanizer
- README.md created and pushed (previous session)
- Brain dump captured: kitchen analogy refinements, disclaimer slide idea, Alex Friday agenda, before-scripts strategy, humanizer/Deerflow/when-Claude-is-down ideas

**What's next:**
1. **Send emails** — review drafts fresh, schedule for morning send
2. **Qdrant migration prompt** — write overnight autonomous migration (ChromaDB → Qdrant). Hold on re-embedding until RCP responds about AIaaS.
3. **Infrastructure master list** — collect all planned repo/workflow changes into one doc
4. **Before scripts** — Crissier-Busigny + Nyon-Genolier, naive (no archibase)
5. **Presentation prep** — slides, animations, models

**Watch out for:**
- Email drafts at `output/research/email_draft_rcp_vm.md` and `email_draft_enac_rhino.md` — review before sending
- RCP deep dive (`output/research/rcp_services_deep_dive.md`) has some unverified assumptions about HaaS specs (were in images, couldn't extract). Don't cite specs without checking.
- Dates: Friday March 27 = screen test with Alex. Monday March 30 = midterm. LOCKBOARD corrected.
- Humanizer won't show as /humanizer until restart — but patterns can be applied manually

**Key files:**
- `output/research/rcp_services_deep_dive.md` — full RCP service inventory
- `output/research/email_draft_rcp_vm.md` — RCP email (ready to review)
- `output/research/email_draft_enac_rhino.md` — ENAC email (ready to review)
- `claudes-corner/2026-03-25_brain-dump.md` — brain dump from this session
- `claudes-corner/2026-03-25_ai-architecture-landscape.md` — tool/people research
- `LOCKBOARD.md` — task split for midterm (dates corrected)

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
| 20-22 | Cairn Code | Weekend sprint: archibase built (4-layer knowledge system, 35K+ chunks), Gemini vision embedder, ChromaDB populated (2,480 entries), training sessions. App concept parked as thesis-scale. |
| 23-03 | Cairn Code | Kitchen analogy animation v1 in Blender (6 videos, character design, house set). Claude character (Cairn) designed + rigged. Emote renders v1. |
| 24-03 | Cairn Code | Cost sheet v2 finalized (1200 CHF budget). Email to Alex sent. Meeting notes: rehearsal Friday March 27, presentation guidance. Pushed 14 commits, resolved merge conflict with Henna's changes. Organized untracked files. Full LOCKBOARD rewrite with midterm task split + presentation structure (11 slides). |
| 25-03 | Cairn Code | Late night session (02:00–03:15). RCP deep dive: found AIaaS (70+ models, embeddings), discovered DSI's VSI for VMs vs HaaS bare metal. Both emails rewritten + humanized. Humanizer skill installed. README pushed. Brain dump + AI landscape scan in Claude's Corner. Dates corrected (Fri 27 screen test, Mon 30 midterm). |
