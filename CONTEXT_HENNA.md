# Henna — Working Context

**Owner**: Henna Rafik (Meridian, Cadence, Nova)
**Last updated:** 2026-03-27

---

## Current priorities

### A04 — midterm (screen test Fri March 27 / presentation Mon March 30)

**Modeling**
- [ ] **Finish corridor model** — verify geometry works in QGIS → Rhino pipeline
- [ ] **Model 9 écluse types** (without site)
- [ ] **Model Crissier-Busigny node** (with site) — Henna's 1 of 2
- [ ] **Model Nyon-Genolier node** (with site) — Henna's 2 of 2

**Presentation**
- [ ] Redo presentation format — aesthetics, transitions, PowerPoint
- [ ] **Slides 2-3 — Chambre-Lock concept**: All content — diagrams + write speech (2 slides)
- [ ] **Slide 4 — Software architecture**: One big diagram of app info flow + architecture. Gif with highlighted steps if possible.
- [ ] **Slide 5 (partial) — Before/after workflow**: Compare how we worked before vs now. Explain agent interactions, Claude-Rhino MCP, Blender MCP, router architecture. Visual diagrams.
- [ ] **Slide 6 — Archibase**: Explain the knowledge base architecture

**Setup needed**
- [ ] Blender MCP + router setup (Rhino multi-instance already working)

### Completed
- ✅ Geodata pipeline operational — extract terrain, buildings, infrastructure for any site via `extract_site.py`
- ✅ Rhino MCP site import working — terrain meshes, LOD2 buildings, railways, roads, water all import correctly
- ✅ Modified Rhino plugin installed — multi-instance confirmed
- ✅ Onboarded to git repo
- ✅ All 7 field sites visited (March 10)

## Session log

> For sessions before March 2 (pre-git), see `handoffs/` (Henna handoffs, Feb 23+).

| Date | Account | What happened |
|------|---------|---------------|
| 02-03 | Cadence | Karim's diary v4 — narrative anchor for A02 crit. |
| 08-03 | Meridian | Built 24 candidate sites for horizontal elevator. Interactive React artifact. |
| 26-03 | Cadence | Built full geodata pipeline: swisstopo extraction (terrain, LOD2 buildings, infrastructure from swissTLM3D), site-selector agent, Rhino MCP import. Fixed building triangles (TIN mesh export). Tested Morges + Vevey end-to-end. |
| 27-03 | Nova | Comic book production: reviewed McNaught-style nurse temporal lock prompt (12 panels). Switched from Midjourney to Gemini — created v3 prompt file with natural language aspect ratios, no-bubble instructions, HOSPITAL sign fix. Designed dynamic asymmetric panel grid (inspired by reference comic) — compressed cold panels at top, expanding warm panels at bottom. InDesign A2 setup spec provided. |
| 27-03 | Nova | Built interactive data sequence diagram for relay-lock pipeline. Landscape SVG: Architect → AI → Corridor/Healthcare datasets → Site Analysis → 5-criteria scoring → 8 decision questions → Lock types → Ranked propositions with sliders → 3 outputs (Rhino3D, Blender, Spec Sheet). Feedback loops for low scores and unclassified. PR #6 open (claude/thirsty-cray → henna/visuals). |

## Handoff

**What was done**
- Built interactive data sequence diagram (`output/data_sequence_diagram_v2.html`) showing the full relay-lock pipeline
- Corrected the flow based on Henna's verbal walkthrough — Architect gives problem+region → AI → datasets → site analysis → scoring → decision tree → propositions → sliders → outputs
- PR #6 open: `claude/thirsty-cray` → `henna/visuals`

**What's next**
1. Merge PR #6 after review
2. Minor fix: remove the circle behind the architect stick figure in v2
3. Continue with presentation slides — this diagram is for Slide 4 (software architecture)
4. Comic panels still pending (Gemini generation)

**Watch out for**
- The v2 file lives in both the worktree and `output/` in main — after merge, the worktree copy is canonical
- The 3 feedback loop labels (score < 3.0, unclassified, slider change) now have step assignments but test they hide/show correctly

**Files to look at**
- `output/data_sequence_diagram_v2.html` — the landscape diagram (use this)
- `output/data_sequence_diagram.html` — v1 vertical version (superseded)
