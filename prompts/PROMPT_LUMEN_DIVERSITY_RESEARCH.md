# PROMPT — Lumen: Diversity Research Deep Dive
**Date**: 2026-03-01 night
**From**: Cairn (S8)
**For**: Lumen (browser, web search + Google Places)
**Priority**: MEDIUM — enrichment for crit and beyond, not critical path

---

## Context

Your DIVERSITY_CREATES_UNITY.md is strong. Cairn reviewed it and has two additions to the framework before you continue:

### Cairn's additions

**1. The chicken-and-egg is productive, not a problem.**
You framed three causal stories (diversity attracts completeness / centrality causes both / co-evolution ratchet). The architectural insight is that you don't need to *resolve* causality — you need to design the *interface where the ratchet starts*. That's the prototypological question: what's the minimum intervention that initiates co-evolution at a dead node? The unresolved causality becomes a design generator, not a blocker.

**2. The deficit IS the asset.**
Your inversion ("don't fill deficits, introduce difference") is the strongest design principle to emerge from this analysis. Push it further: at Grandvaux (WCI ≈ 0), the instinct is "add a coworking space" — making it a worse Lausanne. The Comtesse move is to make it something Lausanne *can't* be. A silent workspace in UNESCO vineyards. The absence of infrastructure isn't a failure — it's a specificity that no hub can replicate. The break point's emptiness is its competitive advantage if programmed correctly.

---

## Your tasks

### A. Quick win first: Shannon vs Commuter Index (Tier 1, item #4)

You identified this as the fastest test. The data exists in project knowledge:
- Shannon index: in `city101_station_crossref_classmates.csv` (column: `religious_shannon_index` or similar)
- Commuter Index: in the SBB ridership data or journey workability files

Cross them. Key question: **Do stations with balanced CI (~1.0) also have high Shannon diversity?** If yes, social diversity extends temporal life — different groups use the station at different times, so it never dies. This directly connects Andrea's flow-of-people argument to Henna's night city work.

Write up findings as a short section that could slot into the narrative.

### B. Web research — Tier 1 items you can do from browser

**Item #1: Nationality diversity by commune**
- Search: OFS stat-tab commune nationality data, or "population résidante permanente selon la nationalité commune vaud genève"
- Look for: foreign resident %, number of nationalities, any diversity index already computed
- Key communes to check: Geneva, Lausanne, Nyon, Vevey, Montreux, Aigle, plus a Lavaux commune (Chexbres, Rivaz, Épesses)

**Item #2: Language diversity by commune**
- Search: OFS Relevé structurel, "langue principale commune vaud"
- The corridor is Romandie but Geneva has major English, Portuguese, Spanish, Italian populations

**Item #5: Modal diversity per station**
- You can build this from what's already in project knowledge: shared mobility data, service frequency, CGN boat schedules
- Count transport modes per station: CFF, bus, Léman Express, shared bikes, boat, funicular, metro

### C. Web research — Tier 2 items

**Item #6: NOGA business diversity**
- Search: OFS STATENT, "statistique structurelle des entreprises commune NOGA"
- Even partial data (e.g., number of NOGA 2-digit sectors per commune) would test whether economic diversity tracks with social diversity

**Item #7: Cuisine diversity**
- You have Google Places access. For 5-8 key stations (Geneva, Nyon, Lausanne, Vevey, Montreux, Aigle, plus 1-2 Lavaux stations), search restaurants within 500m and tag by cuisine type
- Compute a cuisine Shannon index per station
- This is the most visceral diversity indicator — "8 cuisines vs. only pizzerias" is immediately legible

### D. Tier 3 — Write, don't research

These are theoretical extensions for the crit discussion. Write short paragraphs (not data) for:

**Item #10: GA as diversity multiplier**
Frame the argument: GA converts spatial diversity into personal diversity. A Nyon GA-holder's city includes Geneva's diplomacy, Lausanne's culture, Montreux's tourism. Without GA, your city is wherever you can afford to reach. Connect to the CHF 20 = 41km finding from Cairn's GA cost analysis.

**Item #11: Diversity threshold hypothesis**
Is there a minimum Shannon below which richness collapses? Look at the crossref data — is there a visible step function? Even a qualitative observation ("below Shannon 1.0, no station in our dataset has richness above X") would be powerful.

---

## Output

Write a single document: `DIVERSITY_RESEARCH_FINDINGS.md`
Structure:
1. Shannon vs CI quick analysis (with numbers)
2. Nationality/language diversity (whatever you find)
3. Cuisine diversity (if you get to it)
4. GA as diversity multiplier (paragraph)
5. Diversity threshold (paragraph)

Sign it at the bottom: *Produced by Lumen (school account) · [date]*

---

## What NOT to do

- Don't try to fetch transport.opendata.ch APIs — that's Cairn's job (Point 2 temporal)
- Don't try to write Python scripts that need filesystem access
- Don't duplicate the GA cost analysis — Cairn already did it, just reference the findings
- Don't rewrite the narrative draft — Andrea will refine it tomorrow with Henna

## Files you should have in project knowledge
- city101_station_crossref_classmates.csv (Shannon + richness data)
- GA_COST_FINDINGS.md (Cairn's GA analysis)
- DIVERSITY_CREATES_UNITY.md (your own doc from earlier)
- Latest handoffs (S6, S7, S8)
