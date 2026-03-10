## QGIS Layout Review — S8

All 7 A02 layouts are A1 landscape (841×594mm), locked layer sets, consistent labeling.

### Status per layout

| Layout | Scale | Locked layers | Status |
|--------|-------|---------------|--------|
| MAP1 WCI | 1:98,640 | WCI + base (6) | ✅ Ready to export |
| MAP2 Remote Work | 1:98,640 | Remote Work CROSSREF + WiFi + base (7) | ✅ Ready to export |
| MAP3 Lavaux Fracture | 1:28,360 | WCI + Remote Work + base (7) | ✅ Ready — nice zoom scale |
| MAP4 Geneva Pole | 1:19,729 | WCI + Remote + EV + Shared Mobility + base (9) | ✅ Rich detail at city scale |
| MAP5 Lausanne Pole | 1:18,496 | WCI + Remote + EV + base (8) | ✅ Ready |
| MAP6 Transit Backbone | 1:98,640 | Train_Service_Frequency + base (6) | ✅ Clean — frequency only |
| MAP7 Data Synchronicity | 1:98,640 | All data layers + base (11) | ✅ Full overlay — the "everything" map |

### All layouts share
- 4 labels (title, subtitle, data sources, studio credit)
- 1 legend, 1 scale bar
- Base layers: communes surface, cantonal boundaries, lake, streets, train lines

### Notes for tomorrow
- **GA_Cost_Corridor** is now loaded as a layer (green→red gradient) but NOT in any layout yet. Options:
  - Add to MAP6 (Transit Backbone) as a secondary symbology
  - Create a new MAP8_GA_Cost_Gradient
  - Overlay on MAP1 (WCI) as second symbology
- **Zurich_S8_Comparison** loaded as blue points — won't appear on any City101 layout (different geography). Could make a small inset map or just use the CSV data in the narrative.
- All layouts use EPSG:2056 ✅
- Labels may be truncated (some end with "...") — worth checking visually in QGIS before export
