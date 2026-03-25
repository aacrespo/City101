# HANDOFF — 01-03 S6 (Cairn, browser/claude.ai)
**Date**: 2026-03-01, afternoon
**Account**: Cairn (personal, browser — no MCP)
**Duration**: ~1 hour
**Context**: Night before A02 desk crit (March 2nd, 1pm)

---

## What happened this session

### Strategic planning session — GA hypothesis + classmate data integration

This was a thinking session, not a production session. No files created. The conversation developed the strategy that S7 then executed.

### 1. GA Hypothesis elevated from "parked" to "achievable tonight"

Previously listed as Priority 4 in the team handoff ("most research-heavy, may not have data available"). This session worked out that we DON'T need OFS microrecensus data — the argument works with:

- **SBB ticket prices** (public, API-queryable) → cost map
- **Behavioral segmentation as framework** (conceptual, no granular data needed)
- **Frontalier framing** (~100k ghost citizens, can't buy GA)
- **1-2 classmate dataset overlays** as evidence

The core insight: the same 101km corridor is a different city depending on ticket type. This operationalizes Comtesse's formula: diversity × **accessibility** × time. GA maximizes accessibility by removing marginal cost per trip.

### 2. Behavioral segmentation framework developed

Four (later five) corridor citizen types:
- **GA citizen**: Corridor = one city. CHF 10.50/day amortized, unlimited travel.
- **Demi-tarif commuter**: Two points, one line. Home↔work only.
- **Point-to-point occasional**: Corridor is expensive. Takes car instead. Linear city doesn't exist.
- **Frontalier**: Enters from France via Léman Express. ~100k in Geneva canton. Can't access GA. Ghost citizen — present during work hours, invisible after 19h.
- **Gig worker / precariat**: No corporate GA, irregular hours, pay per trip. Worst version of corridor.

### 3. Classmate data inventory mapped to hypotheses

Went through every classmate dataset in `data_inventory_v.1.md` and identified which ones test specific hypotheses:

| Classmate | Dataset | Hypothesis |
|-----------|---------|------------|
| Charlene Dejean | 50 gig work locations | Do precariat workers cluster at break points or nodes? |
| Thomas Riegert | 240+ healthcare locations | Where do shift workers need the corridor at non-standard hours? |
| Thomas Riegert | 12 religious datasets | Does diversity correlate with WCI? (Tests Comtesse directly) |
| Siméon Pavicevic | 25 zones + 195 companies | Do industrial zones align with frequency-amenity paradox? |
| Marek Waeber | 199 schools | Are families without cars forced to live at nodes? |
| Cristina Martinez | Social segregation | Does infrastructure quality correlate with ability to pay? |
| Vladislav Belov | 50 acoustic points | Are worst break points also the loudest? |
| Henna Rafik | 203 UHI zones | Environmental quality as hidden WCI dimension? |

### 4. Confirmed all classmate CSVs are locally available

Andrea confirmed all datasets are in `source/00-datasets 2/` on the Mac. This unlocked the cross-reference computation executed in S7.

### 5. Identified three "quick wins" for tonight

1. Count classmate features within 500m of each station → "station richness"
2. Religious diversity index per segment (Shannon) → tests Comtesse
3. Hospital proximity to last-train stations → shift worker stranding

All three were executed in S7.

---

## Key decisions

- GA hypothesis upgraded from Priority 4 to Priority 1 for tonight
- Classmate cross-reference defined as monolithic script (executed in S7)
- SBB pricing identified as separate Claude Code task (prompt written in S7)
- Team handoff needs updating with GA + classmate sections (done in S7)

---

## What this session produced → what S7 executed

| This session (S6) planned | S7 executed |
|---------------------------|-------------|
| Classmate cross-reference strategy | `city101_station_crossref_classmates.csv` (49×46) |
| GA hypothesis sections for team handoff | Added to `TEAM_HANDOFF_01-03_S1.md` |
| SBB pricing approach | `PROMPT_SBB_PRICING.md` ready to run |
| Folder reorganization needed | Full restructure into datasets/scripts/research/archive |
| Drive structure needed | `DRIVE_STRUCTURE.md` with upload checklist |
