# HANDOFF — 01-03 S7 (Cairn, QGIS MCP)
**Date**: 2026-03-01, late afternoon
**Account**: Cairn (personal, QGIS MCP connected)
**Duration**: ~1.5 hours
**Context**: Night before A02 desk crit (March 2nd, 1pm)

---

## What happened this session

### 1. CLAUDE folder reorganized

The `~/CLAUDE/City101_ClaudeCode/` directory was getting messy — outputs, scripts, source data, and documentation all mixed together. Reorganized into a clear structure:

```
City101_ClaudeCode/
├── CONTEXT.md, LEARNINGS.md, TODO_4_POINTS.md   (entry points)
├── CITY101_WORKING.qgz                          (QGIS project)
├── datasets/                                     (OUR produced data — share from here)
│   ├── corridor_analysis/  (7 files: WCI, break points, journey workability, classmate crossref)
│   ├── ev_charging/        (3 files: enriched v3, reviews, national stats)
│   ├── remote_work/        (7 files: places, hours, reviews, crossref, wifi, cell towers, anchors)
│   ├── transit/            (4 files: frequency, ridership, shared mobility, raw SBB)
│   ├── stations/           (2 files: ratings, reviews)
│   └── zurich/             (1 file: skeleton)
├── handoffs/               (session + team handoffs, drive structure)
├── scripts/                (7 monolithic Python scripts)
├── research/               (trawl data, inventory, reports + trawl/ subfolder)
├── maps/                   (empty — for exported PDFs tomorrow)
├── archive/                (old screenshots, obsolete outputs)
├── source/                 (FROZEN — raw inputs, classmate data, GeoPackages)
└── output/                 (empty — staging folder)
```

Key decisions:
- `share_with_team/` was created then removed — redundant. Just share from `datasets/` directly.
- `source/` untouched (QGIS references these paths)
- All loose files at `source/` root now have organized copies in `datasets/` or `scripts/`
- Created `DRIVE_STRUCTURE.md` with full upload checklist for the team Google Drive

### 2. Team handoff updated + versioned

`TEAM_HANDOFF_01-03.md` → `TEAM_HANDOFF_01-03_S1.md` (session-numbered like other handoffs).

Added two major sections:
- **GA Hypothesis**: Full behavioral segmentation (GA citizen / demi-tarif / point-to-point / frontalier / gig worker), cost map approach, what we can compute tonight, why it matters for the crit
- **Classmate Data Cross-Reference**: Which 7 datasets to overlay, what hypothesis each tests, quick wins (station richness count, religious diversity index, hospital-to-last-train proximity)

Updated task split: GA + classmate cross-ref → Andrea Priority 1 tonight.

### 3. Classmate cross-reference computed ★

**The headline deliverable of this session.** Monolithic script cross-referenced 49 corridor stations against 2,093 geocoded points from 33 classmate datasets at 500m and 1000m radii.

**Output**: `datasets/corridor_analysis/city101_station_crossref_classmates.csv` (49 rows × 46 columns)

Classmate datasets integrated:
- Charlene Dejean: 50 gig work locations
- Thomas Riegert: 389 healthcare points (hospitals, clinics, GPs, specialists)
- Thomas Riegert: 478 religious buildings + communities (10 denominations)
- Thomas Riegert: 43 esoteric practice locations
- Siméon Pavicevic: 25 industrial zones + 195 companies
- Marek Waeber: 199 schools + 121 grocery stores
- Vladislav Belov: 49 acoustic ecology points
- Henna Rafik: 203 UHI zones + 33 thermal comfort points
- Mohamad Ali: 150 restaurants + 132 informal learning spaces
- Charlene Dejean: 27 rooftop/viewpoint locations

**Key findings** (full writeup in `CROSSREF_CLASSMATES_FINDINGS.md`):

1. **Comtesse vindicated**: Religious diversity (Shannon index) correlates with station richness. Top 5 most diverse stations = top 7 richest. Geneva-Champel has all 10 denominations within 1km AND ranks 3rd for richness.

2. **The richness cliff**: Lausanne-Flon has 277 classmate features within 1km. Palézieux has 0. Binary, not gradient.

3. **Frequency-amenity paradox confirmed with 33 datasets**: Vernier Blandonnet (84 trains/hr, richness=7), Palézieux (11.5 tr/hr, richness=0), Aigle (16.5 tr/hr, richness=1), Bussigny (9 tr/hr, richness=3). These are intervention sites.

4. **Gig work follows tourism, not infrastructure**: Vevey (5), Montreux (5), Nyon (4). Zero at break points. The precariat follows tourists, not commuters.

5. **Industry disconnected from rail spine**: Top industrial station by company count is Begnins (6 companies, village stop). Production economy uses roads, knowledge uses rails.

6. **Healthcare generates night demand at rich nodes**: Hospitals cluster at Geneva (50 near Champel), Lausanne (92 near Flon), Vevey (13). Shift worker stranding problem when crossed with first/last train data.

7. **Schools as family filter**: 199 schools heavily concentrated at nodes. Aigle (16.5 tr/hr) has zero schools within 1km. Corridor selects for car-owners in gaps.

### 4. SBB pricing prompt prepared

`handoffs/PROMPT_SBB_PRICING.md` — ready-to-use prompt for Claude Code session. Covers:
- API endpoints to try (`transport.opendata.ch`, `timetable.search.ch`, SBB b2p)
- Distance-based tariff fallback table
- Output spec: cost matrix for 35 OD pairs × 3 ticket types
- Time budget: 30-60 min, switch to fallback after 15 min if API doesn't return prices

---

## Files created/modified this session

| File | Location | Action |
|------|----------|--------|
| `city101_station_crossref_classmates.csv` | `datasets/corridor_analysis/` | **Created** — 49×46, the cross-reference |
| `CROSSREF_CLASSMATES_FINDINGS.md` | `datasets/corridor_analysis/` | **Created** — findings writeup |
| `TEAM_HANDOFF_01-03_S1.md` | `handoffs/` | **Modified** — added GA + classmate sections |
| `DRIVE_STRUCTURE.md` | `handoffs/` | **Created** — Drive upload checklist |
| `PROMPT_SBB_PRICING.md` | `handoffs/` | **Created** — Claude Code prompt |
| `HANDOFF_01-03_S7.md` | `handoffs/` | **Created** — this file |
| Multiple files | `datasets/`, `research/`, `archive/`, `scripts/` | **Moved** — folder reorganization |

---

## What's next

**Tonight (priority order)**:
1. **SBB pricing** — run the prompt on Claude Code or Lumen. Produces GA cost map CSV.
2. **Load crossref + new data into QGIS** — the classmate crossref needs to become a layer
3. **Henna's first/last train** — check if she's produced anything, merge if so

**Tomorrow morning before 1pm crit**:
1. Map curation + export (7 layouts exist, need review + new ones for GA/classmate data)
2. 1-page narrative text (write with Henna)
3. Rehearse 2-minute opening pitch

---

## State of the data

| Category | Files | Status |
|----------|-------|--------|
| WCI + corridor analysis | 7 | ✅ Complete, findings documented |
| EV charging | 3 | ✅ Complete (194 stations, 53 cols) |
| Remote work | 7 | ✅ Complete (68 places, crossref'd) |
| Transit | 4 | ✅ Complete (49 stations + ridership) |
| Stations | 2 | ✅ Complete (ratings + reviews) |
| Classmate crossref | 2 | ✅ NEW this session |
| GA cost map | 0 | 🔴 Next task |
| First/last train | 0 | 🔴 Henna's task |
| QGIS layouts | 7 | 🟡 Exist but not reviewed/exported |
