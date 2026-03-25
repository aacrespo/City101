# Team Drive Structure — City101 (Andrea + Henna)
**Created**: 2026-03-01  
**Purpose**: Organize shared Drive so both team members (and Claude instances) can find anything fast.

---

## Structure

```
City101_Team_Drive/
│
├── 📁 00_Workflow/
│   ├── 00_Workflow_v03.md
│   └── MCP_SAFETY_RULES.md
│
├── 📁 01_Handoffs/
│   ├── TEAM_HANDOFF_01-03_S1.md            ← THE LIVE ONE (start here)
│   ├── HANDOFF_01-03_S1.md
│   ├── HANDOFF_01-03_S2.md
│   ├── HANDOFF_01-03_S3.md
│   ├── HANDOFF_01-03_S4.md
│   ├── HANDOFF_01-03_S5.md
│   ├── HANDOFF_LUMEN_STATION_REVIEWS.md
│   ├── HENNA_S_HANDOFF_23-02_S1.md
│   └── HENNA_S_HANDOFF_23-02_S2.md
│
├── 📁 02_Narrative/
│   ├── TODO_4_POINTS.md                 ← the 4 investigations framework
│   ├── CROSSREF_CLASSMATES_FINDINGS.md  ← classmate cross-reference analysis
│   ├── city101_WCI_summary.md           ← WCI computation report
│   ├── opendata_trawl_categorized.md    ← federal dataset scoring
│   └── data_inventory_v.1.md            ← full file inventory (233 files)
│
├── 📁 03_Datasets/
│   ├── corridor_analysis/
│   │   ├── city101_corridor_segments_WCI.csv          (49 segments, the index)
│   │   ├── city101_break_points.csv                   (49 stations, severity)
│   │   ├── city101_journey_workability.csv             (618 connections)
│   │   ├── city101_journey_workability_summary.csv     (35 OD pairs)
│   │   ├── city101_train_workability.csv               (49 stations)
│   │   └── city101_station_crossref_classmates.csv     (49 stations × 46 cols)
│   │
│   ├── ev_charging/
│   │   ├── city101_ev_charging_ENRICHED_v3.csv         (194 stations, 53 cols)
│   │   ├── city101_ev_charging_REVIEWS.csv             (109 reviews)
│   │   └── swiss_charging_keyfigures_monthly.csv       (63 months national)
│   │
│   ├── remote_work/
│   │   ├── city101_remote_work_places.csv              (68 workspaces)
│   │   ├── city101_remote_work_HOURS.csv               (63 with opening hours)
│   │   ├── city101_remote_work_REVIEWS.csv             (109 reviews)
│   │   ├── city101_remote_work_CROSSREF.csv            (68 × 31 cols)
│   │   ├── city101_wifi_MERGEDv.2.csv                  (81 hotspots)
│   │   ├── city101_cell_towers.csv                     (3,218 towers)
│   │   └── city101_international_anchors.csv           (15 institutions)
│   │
│   ├── transit/
│   │   ├── city101_service_frequency_v2.csv            (49 stations, trains/hr)
│   │   ├── city101_ridership_sbb.csv                   (174 stations, daily pax)
│   │   ├── city101_shared_mobility.csv                 (2,062 stations)
│   │   └── sbb_passagierfrequenz_raw.csv               (raw SBB source)
│   │
│   └── stations/
│       ├── city101_station_ratings.csv                 (37 stations, Google)
│       └── city101_station_REVIEWS.csv                 (71 reviews, tagged)
│
├── 📁 04_Scripts/
│   ├── compute_wci.py                    (WCI + break points + crossref)
│   ├── journey_workability.py            (618 connections analysis)
│   ├── fetch_transport_frequency.py      (v1 — API pattern)
│   ├── fetch_transport_frequency_v2.py   (v2 — corrected, use this)
│   ├── fetch_ridership.py               (SBB Passagierfrequenz)
│   ├── opendata_swiss_trawl.py          (phase 1 — dataset discovery)
│   └── opendata_trawl_phase2_3.py       (phase 2+3 — WMS + API fetch)
│
├── 📁 05_Maps/
│   └── (exported print PDFs — Monday morning)
│
└── 📁 06_Research/
    ├── opendata_swiss_trawl_top50.md     (top 50 federal datasets scored)
    ├── corridor_place_dictionary.json    (station metadata cache)
    └── rail_history_v3.html              (interactive timeline — from Claude Code)
```

---

## Upload checklist (tonight)

### From `~/CLAUDE/City101_ClaudeCode/` on Mac:

**00_Workflow/** — already on Drive, check version is current

**01_Handoffs/**
- [ ] `handoffs/TEAM_HANDOFF_01-03_S1.md` ← Henna reads this FIRST
- [ ] `handoffs/HANDOFF_01-03_S1→S5.md` (5 files)
- [ ] `handoffs/HANDOFF_LUMEN_STATION_REVIEWS.md`

**02_Narrative/**
- [ ] `TODO_4_POINTS.md` (root)
- [ ] `datasets/corridor_analysis/CROSSREF_CLASSMATES_FINDINGS.md`
- [ ] `research/city101_WCI_summary.md`
- [ ] `research/opendata_trawl_categorized.md`
- [ ] `research/data_inventory_v.1.md`

**03_Datasets/** — upload the entire `datasets/` folder structure as-is

**04_Scripts/** — upload from `scripts/` folder

**05_Maps/** — empty for now, create folder for tomorrow

**06_Research/**
- [ ] `research/opendata_swiss_trawl_top50.md`
- [ ] `research/corridor_place_dictionary.json`
- [ ] Rail history HTML (from Claude Code output, if saved locally)

---

## Rules

- **TEAM_HANDOFF is the entry point.** Anyone joining the project reads this first.
- **datasets/ mirrors the Mac structure exactly.** Same folder names, same files.
- **Scripts are reference, not execution.** They document methodology for the crit.
- **Narrative/ is the intellectual backbone.** Arguments, findings, frameworks — not data.
- **Never delete from Drive.** Superseded files get renamed with `_OLD` suffix.
- **New outputs go to the matching subfolder.** If it's a new CSV about transit, it goes in `03_Datasets/transit/`.
