# HANDOFF — 01-03 Session 3 (Cairn, claude.ai + QGIS MCP)

## Last action
Created 7 A02 print layouts in QGIS, styled all data layers, loaded WCI + CROSSREF CSVs from Claude Code output. Project saved.

## What happened this session
1. **Claude Code prompt** — wrote and executed monolithic script producing 3 outputs:
   - `city101_remote_work_CROSSREF.csv` (68 rows × 31 cols) — each workspace cross-referenced against all infrastructure
   - `city101_corridor_segments_WCI.csv` (49 rows × 17 cols) — Working Continuity Index per train station segment
   - `city101_WCI_summary.md` — full analysis with formula, top/bottom 5, geographic patterns
   - Zurich skeleton attempted but ridership CSV has no ZH data — needs separate fetch

2. **QGIS layer setup** — loaded both new CSVs, styled all layers:
   - WCI: 5-class graduated red→green (Very Low/Low/Moderate/High/Very High)
   - Remote Work CROSSREF: categorized by place_type (coral coworking, teal café, blue library)
   - Transit frequency: graduated by trains/hr
   - Cell towers: 5G blue vs legacy grey
   - WiFi: graduated by quality score
   - EV charging: grey context dots
   - Shared mobility: faint grey dots
   - Base layers: soft lake, faint streets, dashed train lines, light commune fills

3. **7 print layouts created** (all A1 landscape, with title/subtitle/legend/scalebar/attribution):
   - A02_MAP1_Working_Continuity_Index — hero map, full corridor WCI
   - A02_MAP2_Remote_Work_Infrastructure — workspaces + WiFi, full corridor
   - A02_MAP3_Lavaux_Fracture — zoomed Lavaux gap
   - A02_MAP4_Geneva_Pole — Geneva zoom with EV + shared mobility
   - A02_MAP5_Lausanne_Pole — Lausanne zoom
   - A02_MAP6_Transit_Backbone — train frequency graduated
   - A02_MAP7_Data_Synchronicity — ALL layers combined

## Current state

### QGIS project: `~/CLAUDE/City101_ClaudeCode/CITY101_WORKING.qgz`
- 50 layers total (48 previous + 2 new CSVs)
- 9 print layouts (2 old + 7 new A02)
- All A02 layouts use locked layer sets — won't break if canvas visibility changes
- CRS: EPSG:2056

### Key WCI findings
- WCI range: 0.0003 (St-Saphorin) – 0.6431 (Genève)
- Top: Genève (0.64), Lausanne (0.55), Vernier/Blandonnet (0.46), Vevey (0.40), Lausanne-Flon (0.40)
- Bottom: Founex (0.01), Rivaz (0.01), Perroy (0.01), Territet (0.01), St-Saphorin (0.00)
- Lavaux gap confirmed: avg WCI 0.075 vs Geneva 0.183, Lausanne 0.212
- Bimodal distribution: 19/49 segments have zero workspaces, 26/49 have zero WiFi
- Vernier/Blandonnet = #3 WCI with ZERO workspaces (pure transit score from 84 tram/hr)

## Still TODO for A02 (due 03.03)
- [ ] **Review layouts visually** — open each in Layout Manager, adjust if needed
- [ ] **Export PDFs** from layouts
- [ ] **Zurich comparison** — need to fetch ZH ridership data separately (current file = GE/VD/VS only). Alternative: qualitative comparison in narrative doc.
- [ ] **Narrative document** — tie formula + findings + maps into coherent A02 text
- [ ] **Point cloud sections** — brief says week 2, may not be urgent for tomorrow
- [ ] **Legend cleanup** — auto-legends may include base layer names; may want to prune

## Key decisions made (cumulative)
- All previous decisions still hold
- **WCI weights**: transit 0.30, workspace 0.25, temporal 0.20, connectivity 0.15, mobility 0.10
- **5-class WCI symbology**: Very Low (<0.05), Low (0.05-0.15), Moderate (0.15-0.30), High (0.30-0.50), Very High (>0.50)
- **Print layout standard**: A1 landscape, Helvetica Neue, title+subtitle+legend+scalebar+attribution
- **Layer lock**: each layout has its own locked layer set — canvas changes won't affect exports

## Technical notes
- WCI script: `~/CLAUDE/City101_ClaudeCode/scripts/compute_wci.py` (stdlib only, rerunnable)
- Both new CSVs in `~/CLAUDE/City101_ClaudeCode/output/`
- Layouts use EPSG:2056 map CRS with on-the-fly reprojection of WGS84 CSV layers
- QuickMapServices plugin available for basemap tiles if needed in layouts
