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
| 29-03 | Nova | Built Overcooked-style kitchen animation (v3→v6). Scene 1: character enters kitchen, reads CLAUDE.md + .claude/ scrolls, turns gold, kitchen furnishes. Scene 2: pass counter, order/cook/plate loop with user character, archibase book, CAG vs RAG, logbook overlay. Grid-based tile-hop movement, A* pathfinding, top-down oblique projection. Created GRID_MAP.md coordinate reference. |
| 29-03 | Nova | Built Arc Lémanique 3D model in Rhino via MCP. Full pipeline: swissALTI3D terrain (10.5M vertices, 25m res, 83×79km), swissBUILDINGS3D buildings (110k with convex hull footprints, >20m), Lake Léman surface, 9 relay-lock node spheres (design system colors). Two iterations: V1 (50m terrain, bbox buildings) → V2 (20m→25m terrain, hull footprints, extended coverage). Checkpoints saved to Midterm help/. |

## Handoff

**What was done**
- Built full Arc Lémanique 3D corridor model in Rhino via Rhino MCP
- **Terrain**: 10.5M vertex mesh from swissALTI3D, 25m resolution, 83×79 km coverage
- **Lake**: Mesh surface at z=373m from City101_LakeLeman.gpkg
- **Buildings**: 109,855 convex hull extrusions from swissBUILDINGS3D (>20m tall)
- **Nodes**: 11 spheres at 9 relay-lock sites (Nyon+Genolier split, Rennaz+Villeneuve split), design system colors (Gold/Copper/Teal)
- Processing scripts saved in `output/arc_lemanique/`
- Checkpoint .3dm files saved in `Midterm help/`

**What's next**
1. **Save the Rhino file** — Ctrl+S (MCP can't save files this large)
2. **Set display mode** — Arctic mode + background #0c0c14 manually in Rhino
3. **Camera angles** for presentation slides 7-10
4. **Midterm presentation** — Monday March 30
5. If more/fewer buildings needed: re-filter from `buildings_hull_15m.json` (490k buildings available)

**Watch out for**
- Rhino MCP times out on save with the 10.5M vertex mesh — always save manually
- The model origin is at LV95 (2485000, 1090000) — full VRT extent, not the original corridor bbox
- `buildings_hull_15m.json` is 100 MB — all 490k buildings with hull footprints, filter to any threshold
- Extracted GDB at `Swisstopo/extracted_buildings/` is 8.9 GB — gitignored, can delete after midterm

**Files to look at**
- `output/arc_lemanique/process_data.py` — terrain + lake processing script
- `output/arc_lemanique/process_buildings.py` — building extraction script
- `output/arc_lemanique/nodes_full.json` — 9 node coordinates (model space)
- `Midterm help/STATUS.md` — full status with all data files documented
- `Midterm help/arc_lemanique_v2_terrain_lake.3dm` — latest checkpoint (terrain+lake only, 202 MB)
