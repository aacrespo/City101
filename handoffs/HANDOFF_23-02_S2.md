# HANDOFF — 23-02 Session 2 (Cairn)

## What happened
Finalized MAP1 and MAP3 styling for Monday pin-up. Extensive iterative refinement of cartographic hierarchy.

### MAP1 — "The Program of Stopping" ✅
- **Highway**: Switched from OBJEKTART to VERKEHRSBEDEUTUNG=100 (815 features vs 127). Black 0.8mm, full opacity (was 25% — root cause of "washed out" look)
- **Highway exits**: Crosses (3.5mm) instead of triangles — reads cleaner
- **EV stations**: Teal (pass-through) + amber (destination) + grey (residential), 3.2mm
- **Train lines**: Faded grey for MAP1 context (160,160,160, 0.3mm)
- **Legend**: Descriptions integrated into category labels, clean 3-column layout
- **Layer renamed**: Highway exits layer → "Highway Exits" (was long swisstlm name)
- **PDF on Desktop**: `MAP1_Program_of_Stopping.pdf`

### MAP3 — "Where Can You Work?" ✅
- **Backbone flip**: Train lines are the spine (black dashed 0.7mm), highway demoted to faint grey
- **Train stations**: 336 stations filtered from City101_Transit_Stops (OBJEKTART=0), shown as crosses
- **Layer renamed**: Transit stops → "Train Stations", train lines → "Train Lines"
- **Symbols**: All circles, two-color logic mirroring MAP1:
  - Coral (#ef5f50) = Dedicated workspace (35 coworking)
  - Deep teal-green (#0f766e) = Informal workspace (33 cafés + libraries)
  - Grey = WiFi (81 points, background layer)
- **WiFi deserts**: No special highlighting — gaps reveal themselves
- **Labels**: All map labels disabled
- **PDF saved by Andrea manually**

### Shared layer issue ⚠️
Streets layer is shared between MAP1 and MAP3. Current state = MAP1 mode (highway bold). Before exporting MAP3 again, need to:
1. Demote highway (grey 0.4mm, opacity 120)
2. Restore train (black dashed 0.7mm)
3. Export MAP3
4. Restore highway for MAP1

### MAP2 — "The Coverage Gradient"
- Basic layout exported but NOT refined this session
- Still needs the same level of polish as MAP1/MAP3

## Still TODO
- [ ] MAP2 visual refinement (5G/4G coverage + cell towers)
- [ ] Final sequential export of all 3 maps (handling shared layer styling)
- [ ] Print at FAR studio (Andrea will handle)
- [ ] Consider: should MAP1 also show train lines as dashed context?

### Scratch layers saved to disk ⚠️
Four layers were memory-only (would be lost on close):
- City101_EV_Charging_v3 (194 features)
- Public WiFi (81 features)
- City101_CellTowers (3,218 features)
- City101_InternationalAnchors (15 features)

All saved as .gpkg files in the Assignment 1 folder and re-linked in the project. **For future sessions**: when creating layers from scripts, always write to disk — memory layers don't survive project close.

## Key learnings this session
- **VERKEHRSBEDEUTUNG** is the correct hierarchy field for Swiss TLM roads, not OBJEKTART
- **Layer opacity** at 25% was the root cause of hours of "why is this grey" — always check layer-level opacity
- **Two-color logic** works: MAP1 (teal/amber = transit/destination), MAP3 (coral/teal-green = dedicated/informal)
- **Backbone principle**: Each map has one infrastructure spine (MAP1=highway, MAP3=train), everything else recedes
- Colors must harmonize with the lake blue — the lake is the dominant visual element

## Files
- QGIS project: `CITY101_TESTS_Charging stations_dots and colors.qgz`
- MAP1 PDF: Desktop
- MAP3 PDF: Saved by Andrea
- MAP2 PDF: Desktop (basic version)
