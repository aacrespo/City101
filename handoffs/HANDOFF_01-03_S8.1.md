# HANDOFF_01-03_S8.1
**Date**: 2026-03-01, evening
**Account**: Lumen (school team account)
**Platform**: Browser (claude.ai) — no MCP, no filesystem
**Duration**: ~1 session
**Task**: PROMPT_LUMEN_DIVERSITY_RESEARCH.md (assigned by Cairn S8)

---

## What happened this session

### DIVERSITY_RESEARCH_FINDINGS.md — COMPLETED ✅

Delivered all 5 sections from the prompt:

**Section 1 — Shannon vs Station Richness**
- Pearson r = 0.632 (Shannon vs richness), vs r = 0.176 (trains/hr vs richness)
- Diversity predicts amenity richness 3.6× better than frequency
- Phase transition at Shannon ≈ 1.0: below it avg richness 8.8, above it 70.5 (8× jump)
- Anomalies identified: Vernier-Blandonnet (diverse but empty), Coppet (rich but homogeneous)

**Section 2 — Nationality & Language Diversity**
- Full corridor commune data from Statistique Vaud 2024 + OCSTAT Geneva 2024
- Lavaux Fracture confirmed in demographics: 50% foreign (Geneva) → 12.5% (Rivaz) = 3.4× collapse
- Language: 39% of Vaud residents report non-French principal language; 25% use English at work
- Religious secularization (42% sans confession in 2023) means Shannon captures genuine active communities

**Section 3 — Cuisine Diversity via Google Places**
- 6 stations sampled, ~10 restaurants each, classified by cuisine type
- Geneva: Shannon 2.03 (8 types, even distribution — "the world on a plate")
- Chexbres: Shannon 1.50 (6 nominal types but Swiss/European = 5 of 10 — illusory diversity)
- Vevey surprise: 7 cuisine types including Indian, Chinese, Syrian
- Aigle: Spanish + Portuguese restaurants reflect actual Iberian migration demographics

**Section 4 — GA as Diversity Multiplier** (theoretical write-up)
- Connected to Cairn's CHF 20 = 41km finding
- GA maximizes accessibility variable in Comtesse's formula
- Frontalier blind spot: ~100k can't buy GA, experience most fragmented diversity

**Section 5 — Diversity Threshold Hypothesis** (confirmed with data)
- No station below Shannon 1.0 exceeds richness 27 in entire 49-station dataset
- Step function maps geographically onto Lavaux Fracture
- Applied Cairn's framework: deficit IS the asset, chicken-and-egg IS productive

---

## Files produced

| File | Location | Status |
|------|----------|--------|
| DIVERSITY_RESEARCH_FINDINGS.md | outputs/ + should be added to project knowledge | ✅ Final |
| WIP_01_SHANNON_ANALYSIS.md | outputs/ | Superseded by final doc |
| WIP_02_NATIONALITY_LANGUAGE.md | outputs/ | Superseded by final doc |

---

## Still TODO from the original prompt

### Item #5 — Modal diversity per station 🟡 IN PROGRESS
Count transport modes per station (CFF, bus, Léman Express, CGN boat, shared bikes, funicular, metro, etc.). Compute modal Shannon index. Test: does modal diversity also track with religious/cuisine diversity? If yes, it's a triple-validated Comtesse finding.

### Item #6 — NOGA business diversity 🔴 NOT STARTED
OFS STATENT data: number of economic sectors (NOGA 2-digit) per commune. Would test whether economic monoculture maps onto the same fracture zones. May be hard to find at commune level — cantonal or district level more likely.

---

## New analysis angles opened by this session

### 1. Anomalies deep dive — design briefs
Vernier-Blandonnet (Shannon 1.55, Richness 7) and Coppet (Shannon 0.0, Richness 21) are the most architecturally interesting findings. They represent two failure modes:
- **Diversity without programming**: the social base exists but spatial design prevents the co-evolution ratchet from starting
- **Programming without diversity**: amenities exist but demographic homogeneity prevents the feedback loop

A short write-up of *what specifically* makes each one jammed → concrete design briefs for prototypological proposals. These could become studio intervention sites.

### 2. Frontalier diversity perspective
~100k ghost citizens present in Geneva's daytime economy but invisible in every diversity metric (not counted in resident nationality stats, can't buy GA, vanish after 19h). A section on what the corridor looks like *from their perspective* would:
- Strengthen the GA argument
- Add a temporal dimension (diversity changes by hour because frontaliers are daytime-only)
- Connect to Henna's night city (the corridor's diversity literally goes home to France at dusk)

### 3. Cuisine-migration correlation
The Aigle finding (Spanish + Portuguese restaurants = actual Iberian migration demographics) suggests you could map cuisine origins against OFS nationality data per commune. If they match, cuisine becomes a proxy indicator for migration patterns — more visceral than statistics for a crit audience.

---

## Key numbers for quick reference

| Metric | Value | Source |
|--------|-------|--------|
| Shannon vs Richness correlation | r = 0.632 | crossref CSV |
| Trains/hr vs Richness correlation | r = 0.176 | crossref CSV |
| Shannon threshold | ≈ 1.0 | crossref CSV |
| Richness below threshold | avg 8.8, max 27 | crossref CSV |
| Richness above threshold | avg 70.5 | crossref CSV |
| Geneva foreign % | ~50% (196 nationalities) | OCSTAT 2024 |
| Rivaz foreign % | 12.5% (lowest on corridor) | StatVD 2024 |
| Geneva cuisine Shannon | 2.03 (8 types) | Google Places |
| Chexbres cuisine Shannon | 1.50 (Swiss-dominated) | Google Places |
| Vaud English at work | 25% | OFS 2023 |
| Vaud sans confession | 42% (up from 26% in 2010) | OFS 2023 |

---

## Recommendations for Cairn

1. **Add DIVERSITY_RESEARCH_FINDINGS.md to project knowledge** for both accounts
2. The "3 sentences for the crit" at the bottom of the doc are ready to drop into the narrative
3. Consider a QGIS map colored by Shannon with cuisine/nationality annotations — the phase transition is visually dramatic
4. The anomalies (Vernier-Blandonnet, Coppet) could become named intervention sites in the prototypological proposals

---

*Signed: Lumen (school team account) · 2026-03-01*
