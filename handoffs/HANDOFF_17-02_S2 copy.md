# HANDOFF — 17-02 Session 2

## Last action
Finalized 00_Workflow_v02.md and project instructions. System is now live — workflow doc in project files, instructions updated to reference it.

## Current state
- **00_Workflow_v02.md** in project files (1044 lines) — the source of truth
- **Project instructions** updated to reference workflow doc
- EV charging dataset (194 points) still in QGIS, unchanged from S1
- No new datasets created this session — focused on workflow/methodology

## Open threads
- A.01 still needs second dataset (due 23.02)
- Dwell context classification for EV stations not yet finalized
- Connection to sentient city narrative needs articulation
- System needs testing on school account

## Key decisions made (cumulative)
- **LOG/LOI/LOD framework adopted** (industry-standard BIM terminology):
  - LOG (Level of Geometry) = visual complexity — start low, increase as design locks
  - LOI (Level of Information) = data richness — start high, filter for export
  - LOD (Level of Development) = design certainty — increases over time
- **Differentiated principles:**
  - LOI: "Work rich, export lean"
  - LOG: "Start lean, refine progressively"
- **Data Collection Protocol** added — maximize LOI with attribute checklist before querying
- Framing is "flow of people" not energy (energy = Siméon's territory)
- EV charging analyzed through human experience lens
- LV95 / EPSG:2056 as working coordinate system
- Scale conventions are guidelines, not laws — adapt to output medium
- Color can replace line weight hierarchy
- Digital output: legibility relative to viewport matters, not absolute scale

## Technical notes
- 00_Workflow_v02.md location: `/mnt/project/00_Workflow_v02.md`
- Document structure: 7 parts (A–G), 24 sections, ~1000 lines
- Handoff template now includes: Data sources + Crit notes (optional)
- QGIS project unchanged — still using Swisstopo geodata
