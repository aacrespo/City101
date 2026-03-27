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

## Handoff

**What was done**
- Adapted 12-panel comic prompt from Midjourney to Gemini format → `prompts/[A04_ACTIVE]_comic_temporal_lock_nurse_v3_gemini.md`
- Designed new asymmetric panel grid (cold panels compressed at top, warm panels expand at bottom — layout mirrors the palette shift)
- Provided full InDesign A2 document setup (margins, grid, swatches, paragraph styles, layers)

**What's next**
1. Generate all 12 panels in Gemini using v3 prompts — start with Panel 1 (now says HOSPITAL, no bubbles)
2. Set up InDesign document with the new asymmetric grid
3. Assemble panels + add narration text (Instrument Serif italic) and timestamps (DM Mono)
4. The new grid hasn't been written to a file yet — it was given in chat. Save it if needed.

**Watch out for**
- Gemini may still add text/bubbles — regenerate if it does, the anti-bubble instruction is in each prompt
- Palette discipline: panels 1–4 must stay cold (navy+blue), panels 7–12 must be warm (pink-mauve dominant)
- The v3 file still has the OLD grid layout in its Assembly Notes section — the new asymmetric grid from this session was discussed in chat but not yet written into the file

**Files to look at**
- `prompts/[A04_ACTIVE]_comic_temporal_lock_nurse_v3_gemini.md` — the Gemini prompts (use these)
- `prompts/[A04_ACTIVE]_comic_temporal_lock_nurse.md` — original MJ version (reference only)
- `prompts/[A04_ACTIVE]_comic_temporal_lock_nurse_v2_haugomat.md` — Haugomat style variant (reference only)
