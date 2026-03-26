# Henna — Working Context

**Owner**: Henna Rafik (Meridian, Cadence, Nova)
**Last updated:** 2026-03-25

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
