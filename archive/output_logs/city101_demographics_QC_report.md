# City101 Demographics QC Audit Report

**Auditor:** QC Agent (Cairn Code)
**Date:** 2026-03-04
**Files audited:**
1. `output/city101_demographics_geneva.json`
2. `output/city101_demographics_lausanne.json`
3. `output/city101_demographics_comparison_context.json`
4. `source/animation/corridor_demographics_v2.csv` (cross-reference)

---

## 1. Executive Summary

| Dataset | Verdict | Critical Issues |
|---------|---------|-----------------|
| Geneva JSON | **CONDITIONAL PASS** | Age pyramid brackets are estimated. 6/10 nationality counts unsourced. Language data 26yr old. Pop growth 2015-2020 interpolated. |
| Lausanne JSON | **CONDITIONAL PASS** | Income is complete gap. Age pyramid estimated. All 10 nationality counts estimated. Language is cantonal proxy. Total jobs missing. |
| Comparison context JSON | **CONDITIONAL PASS** | GE pop (203,951) contradicts GE JSON (209,061). Frontalier 115k vs 112k. GDP "approximate". |

**Overall:** Research is honest about limitations — estimates labelled. But cross-file inconsistencies in population and frontalier numbers must be fixed. Geneva nationality counts have arithmetic impossibility (top 10 sum > total foreign pop).

---

## 2. Critical Findings

### 2.1 CRITICAL: Geneva nationality arithmetic
Top 10 counts sum to 128,670 but total foreign population is only 103,800. **Impossible.** Portugal (36,500) and France (33,500) appear to be canton-level, not commune-level.

### 2.2 HIGH: Population contradictions

| Source | Geneva | Lausanne |
|--------|--------|----------|
| City JSON | 209,061 (2024) | 148,810 (2024) |
| Context JSON | 203,951 (2024) | 145,000 (2024) |
| corridor_demographics_v2.csv | 203,856 (BFS 2022) | 140,000 (BFS 2022) |

Context JSON's 203,951 is likely mislabelled BFS 2022 data. Geneva JSON's 209,061 may be municipal register vs BFS permanent resident definition.

### 2.3 HIGH: Age pyramid totals wrong
- Geneva: M+F = 204,400 vs pop 206,635 (missing 2,235)
- Lausanne: labelled "2020" but sums to ~148,300 (matches 2024 pop, not 2020 pop of 140,202)

### 2.4 MEDIUM: Frontalier contradiction
Geneva JSON: 112,000. Context JSON: 115,000. The 160k corridor figure only works with 115k.

---

## 3. Completeness Matrix

| Dimension | Geneva | Lausanne | Match? |
|-----------|--------|----------|--------|
| Population total | ✓ | ✓ | Yes |
| Population growth | ✓ (heavy interpolation) | ✓ (heavy interpolation) | Yes |
| Age aggregates | 8 brackets | 4 brackets | **NO** |
| Age pyramid 5yr M/F | ✓ (estimated) | ✓ (estimated) | Yes |
| Nationality split | ✓ | ✓ | Yes |
| Nationality top 10 | ✓ (4 confirmed, 6 est) | ✓ (0 confirmed, 10 est) | Yes |
| Languages | ✓ (2000!) | ✓ (2019, cantonal) | **NO** (26yr gap) |
| Employment sectors | ✓ | ✓ | Yes |
| Total jobs | 215,000 | **null** | **NO** |
| Unemployment | 3.8% | 5.0% | Yes |
| Income | 6,788 CHF/mo | **null** | **NO** |
| Education | 44.3% (2011) | 51% (2020) | **CAUTION** (9yr gap) |
| Housing ownership | 18.9% | 12.8% | Yes |
| Avg rent | 1,850 | 1,600 | Yes (both est) |
| Vacancy | 0.34% | 0.82% | Yes |
| Domestic commuters | **null** | 49k in / 21k out | **NO** |
| Frontaliers | 112,000 | 8,500 (est) | Yes |
| Universities | 7 inst / 25,332 | 7 inst / 37,362 | Yes |
| International orgs | 38 orgs | **absent** | **NO** |

---

## 4. Recommendations

### Must fix (blockers)
1. **Reconcile population figures** — pick one source, apply consistently
2. **Fix Geneva nationality counts** — top 10 cannot exceed total foreign pop
3. **Fix age pyramid totals** — M+F must sum to stated pop for stated year
4. **Reconcile frontalier figures** — choose 112k or 115k

### Should fix
5. Harmonize age bracket definitions for comparison
6. Fill Lausanne income gap (use cantonal VD proxy)
7. Fill Lausanne total jobs gap
8. Add IOC/sport feds to Lausanne (parallel to Geneva intl orgs)

### Non-blocking
9. Flag all interpolated/estimated data clearly in visualization
10. Document age pyramid estimation methodology

---

## Severity Summary
- **CRITICAL:** 1 (nationality arithmetic)
- **HIGH:** 2 (population contradictions, age pyramid errors)
- **MEDIUM:** 2 (frontalier inconsistency, bracket incompatibility)
- **LOW:** 4 (data age issues, missing sections)
