# HANDOFF_01-03_S8.2
**Date**: 2026-03-01, late evening
**Account**: Lumen (school team account)
**Platform**: Browser (claude.ai) — no MCP
**Continues from**: HANDOFF_01-03_S8.1

---

## What happened this session

### Item 5 — Modal Diversity per Station ✅

Built modal inventory for all 49 stations. Classified 11 transport mode types across the corridor: CFF regional, CFF longdist, Léman Express, metro, tram, urban bus, regional bus, CGN boat, funicular, narrow gauge, shared bikes.

**Files produced:**
- `city101_modal_diversity.csv` — 49 stations × 17 columns (n_modes, modal_shannon, boolean flags per mode type, cross-referenced with religious Shannon + richness)

**Key findings:**
- Modal Shannon vs Religious Shannon: **r = 0.626** (nearly identical to religious-richness correlation)
- Lausanne tops at 8 modes. Geneva/Vevey/Montreux at 7 each.
- 12 stations are mono-modal (CFF regional only) — all in La Côte small halts or Lavaux
- St-Saphorin: 0 modes (ghost station)
- Modal threshold mirrors religious threshold:
  - 0-1 modes: avg richness 3.2, avg Shannon 0.23
  - 6-8 modes: avg richness 81.6, avg Shannon 1.48

**Design insight:** The same urban complexity that justifies 7 transport modes also sustains 9 denominations and 250 amenities. Mono-modal = mono-cultural = mono-amenity. The fracture is total.

### Item 6 — Economic Diversity (NOGA Proxy) ✅

STATENT NOGA 2-digit data isn't publicly available at commune level (district only from StatVD, or behind BFS order forms). Used crossref dataset's 8 economic categories as proxy.

**Files produced:**
- `ITEM6_ECONOMIC_DIVERSITY.md` — full analysis with correlations, tier breakdown, known economic anchors

**Key findings:**
- Economic categories vs Religious Shannon: **r = 0.708** — strongest correlation in the entire analysis
- Industrial companies vs Religious Shannon: **r = -0.217** (negative!) — economic monoculture = social monoculture
- Low-Shannon stations: 1.5 economic categories avg. High-Shannon: 5.4 categories (3.6× increase)
- Lavaux = viticulture + seasonal tourism = economic monoculture → demographic monoculture

---

## All prompt items — final status

| Item | Description | Status | Key number |
|------|-------------|--------|------------|
| #1 Nationality diversity | Commune-level foreign % | ✅ S8.1 | Geneva 50% → Rivaz 12.5% |
| #2 Language diversity | OFS Relevé structurel | ✅ S8.1 | 25% English at work in Vaud |
| #5 Modal diversity | Transport modes per station | ✅ S8.2 | r = 0.626 vs Shannon |
| #6 NOGA business diversity | Economic categories proxy | ✅ S8.2 | r = 0.708 vs Shannon |
| #7 Cuisine diversity | Google Places restaurant survey | ✅ S8.1 | Geneva H=2.03, Chexbres H=1.50 |
| #10 GA as diversity multiplier | Theoretical write-up | ✅ S8.1 | CHF 20 = 41km city |
| #11 Diversity threshold | Phase transition analysis | ✅ S8.1 | Shannon 1.0 threshold, 8× jump |
| Shannon vs CI | Cross-tabulation | ✅ S8.1 | r = 0.632 Shannon vs richness |

**All items from PROMPT_LUMEN_DIVERSITY_RESEARCH.md are complete.**

---

## Correlation summary — the convergence table

| Pair | r | Source |
|------|---|--------|
| Economic categories vs Religious Shannon | **0.708** | crossref proxy |
| Religious Shannon vs Station richness | **0.632** | crossref |
| Modal Shannon vs Religious Shannon | **0.626** | modal inventory |
| Economic total vs Religious Shannon | 0.647 | crossref proxy |
| Restaurants vs Religious Shannon | 0.552 | crossref |
| Modal diversity vs Trains/hr | 0.499 | modal inventory |
| Religious Shannon vs Trains/hr | 0.371 | crossref |
| Gig work vs Religious Shannon | 0.319 | crossref |
| Industrial companies vs Religious Shannon | **-0.217** | crossref |
| Trains/hr vs Station richness | 0.176 | crossref |

**Four independent diversity indices converge on the same story. The Lavaux Fracture is a systemic diversity collapse, not a transit gap.**

---

## Files in outputs (for Andrea to download)

| File | Type | Status |
|------|------|--------|
| DIVERSITY_RESEARCH_FINDINGS.md | Final deliverable | ✅ Already downloaded by Andrea |
| HANDOFF_01-03_S8.1.md | Handoff | Add to project knowledge |
| HANDOFF_01-03_S8.2.md | Handoff | Add to project knowledge |
| city101_modal_diversity.csv | Dataset | For QGIS (Cairn) |
| ITEM6_ECONOMIC_DIVERSITY.md | Analysis | Merge into findings or keep standalone |
| WIP_01_SHANNON_ANALYSIS.md | Superseded | Can delete |
| WIP_02_NATIONALITY_LANGUAGE.md | Superseded | Can delete |

---

## New angles still open (for next conversation)

1. **Anomalies deep dive** — Vernier-Blandonnet + Coppet as design briefs
2. **Frontalier diversity perspective** — ghost citizens, temporal diversity
3. **Cuisine-migration correlation** — map cuisine origins against OFS nationality data

---

*Signed: Lumen (school team account) · 2026-03-01*
