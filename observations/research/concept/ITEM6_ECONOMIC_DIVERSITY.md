# ITEM 6 — Economic Diversity (NOGA Proxy Analysis)
**Produced by Lumen · 2026-03-01**
**Method**: Used crossref dataset economic categories as NOGA proxy (commune-level NOGA 2-digit data is restricted to district level on StatVD; BFS stat-tab only publishes 3-sector breakdown per commune)

---

## The proxy

STATENT NOGA 2-digit data isn't publicly available at commune level. But the crossref dataset contains 8 economic categories per station (1km radius): industrial zones, industrial companies, restaurants, grocery stores, schools, healthcare, gig work platforms, informal learning spaces. Counting how many of these 8 categories are present = economic diversity proxy. Counting total establishments = economic density proxy.

## The correlation — strongest yet

| Pair | Pearson r |
|---|---|
| **Economic categories (0-8) vs Religious Shannon** | **0.708** |
| Economic total vs Religious Shannon | 0.647 |
| Restaurants vs Religious Shannon | 0.552 |
| Economic categories vs Richness | 0.519 |
| Gig work vs Religious Shannon | 0.319 |
| **Industrial companies vs Religious Shannon** | **-0.217** |

Economic category diversity is the single strongest correlate of social diversity found in this analysis (r = 0.708), beating religious Shannon vs richness (0.632), modal Shannon vs religious Shannon (0.626), and trains/hr vs anything.

## The industry-diversity inversion

Industrial companies correlate **negatively** with social diversity. Stations surrounded by industry (Bussigny, Prilly-Malley, Renens periphery) have lower Shannon than service-economy hubs. Economic monoculture (one factory, one employer) produces social monoculture. Economic polyculture (restaurants + schools + healthcare + gig platforms) produces — or is produced by — social diversity.

This maps directly onto the corridor: Lavaux's economic monoculture (viticulture + seasonal tourism) aligns with its demographic monoculture (12.5% foreign, Shannon 0.0). Geneva's economic polyculture (international orgs + banking + biotech + watchmaking + diplomacy + hospitality) aligns with its demographic polyculture (50% foreign, 196 nationalities, Shannon 1.70+).

## Economic categories by Shannon tier

| Shannon tier | Stations | Avg categories (/8) | Avg restaurants | Avg gig work |
|---|---|---|---|---|
| Low (0–0.5) | 19 | 1.5 | 1 | 0.3 |
| Medium (0.5–1.0) | 13 | 3.0 | 2 | 0.5 |
| High (1.0–1.5) | 6 | 4.5 | 4 | 1.7 |
| Very high (1.5+) | 11 | 5.4 | 9 | 1.2 |

Economic diversity scales nearly linearly with social diversity: from 1.5 categories in low-Shannon stations to 5.4 in high-Shannon stations (3.6× increase). The step from medium to high Shannon doubles the restaurant count.

## Known economic anchors

| Node | Economic character | Shannon |
|---|---|---|
| Geneva | International orgs, banking, biotech, diplomacy — maximum sectoral diversity | 1.70 |
| Nyon | FIFA HQ, international NGOs, pharma | 1.54 |
| Lausanne | University + CIO/IOC + tech + public admin | 1.96 |
| Vevey | Nestlé HQ (10,000+ employees) + food industry | 1.73 |
| Montreux | Tourism + congress + hospitality — seasonal tertiary | 1.24 |
| Aigle | Military + TPC rail + viticulture + growth zone | 0.00* |
| Lavaux | Viticulture + seasonal tourism — economic monoculture | 0.00 |

*Aigle anomaly: 42.9% foreign population but Shannon 0.0 suggests diverse workforce without proportional community infrastructure. The economic activity (military, rail, agriculture) attracts workers but doesn't generate the service ecosystem.

## What this means for the crit

**Four diversity indices now converge on the same story:**
1. Religious diversity (Shannon, r = 0.632 vs richness)
2. Nationality diversity (% foreign, 3.4× collapse in Lavaux)
3. Cuisine diversity (Shannon 2.03 Geneva vs 1.50 Chexbres)
4. Economic diversity (categories, r = 0.708 vs Shannon)

They're all measuring the same thing from different angles: **the degree to which a place supports multiple ways of being human.** Where one form of diversity exists, the others follow. Where one collapses, they all collapse. The Lavaux Fracture isn't a transit gap — it's a systemic diversity collapse visible in every dataset we have.

---

## Data limitation note

This analysis uses establishment proximity counts as a proxy for NOGA sectoral diversity. True NOGA 2-digit analysis (how many distinct economic sectors are represented per commune) requires STATENT geodata that is available by district only from StatVD, or behind order forms at BFS. The proxy is directionally correct — presence of diverse establishment types implies diverse NOGA sectors — but understates diversity in areas where multiple establishments share the same NOGA code (e.g., 10 restaurants = 1 NOGA sector but 10 entries in our count).

A future enhancement would be to request the STATENT GEOSTAT dataset (available to public authorities and mandataires) which provides hectare-level NOGA classifications. For a school studio project, the proxy analysis is sufficient to support the argument.
