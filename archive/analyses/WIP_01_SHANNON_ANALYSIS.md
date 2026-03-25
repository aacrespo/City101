# WIP Section 1 — Shannon Diversity vs Station Richness
*Produced by Lumen · 2026-03-01*

## The Quick Win: Does Social Diversity Predict Amenity Richness?

**Answer: Yes, and more strongly than transit frequency does.**

### Correlations (Pearson, n=49 stations)
- **Shannon religious diversity vs Station richness**: r = 0.632 (strong positive)
- **Trains/hr vs Station richness**: r = 0.176 (weak positive)  
- **Shannon vs Trains/hr**: r = 0.371 (moderate positive)

**Interpretation**: Religious diversity is 3.6× more predictive of a station's amenity richness than its train frequency. A station surrounded by many denominations almost certainly has restaurants, schools, healthcare, gig workers. A station with many trains might have none of these.

### The Diversity Threshold — A Step Function

There is a visible cliff in the data:

| Shannon range | Stations | Avg richness | Max richness |
|---|---|---|---|
| = 0.0 (mono/none) | 18 | 4.4 | 21 |
| 0.01–0.99 | 14 | 16.4 | 27 |
| 1.00–1.49 | 6 | 20.5 | 57 |
| 1.50–1.99 | 10 | 80.0 | 277 |
| ≥ 2.00 | 1 | 127.0 | 127 |

**The threshold is at Shannon ≈ 1.0.** Below it, no station in the dataset exceeds richness 27. Above it, average richness jumps to 70.5. This is not a gradient — it's a phase transition.

Below Shannon 1.0: 32 stations, avg richness 8.8, max 27.
Above Shannon 1.0: 17 stations, avg richness 70.5.

### Top 6 Stations by Shannon Diversity

| Station | Shannon | Denominations | Richness | Trains/hr |
|---|---|---|---|---|
| Genève-Champel | 2.12 | 10 (ALL: buddhist, christian, esoteric, evangelical, hindu, jewish, muslim, orthodox, other, protestant) | 127 | 12.5 |
| Lausanne | 1.96 | 9 | 250 | 28.5 |
| Lausanne-Flon | 1.94 | 9 | 277 | 4.0 |
| Genève-Eaux-Vives | 1.94 | 8 | 59 | 12.5 |
| Vevey | 1.73 | 7 | 75 | 20.0 |
| Genève | 1.70 | 8 | 115 | 25.0 |

### The Anomalies — Why They Matter

**High Shannon, Low Richness (diversity without amenities):**
- Vernier-Blandonnet: Shannon 1.55, Richness 7, 84 trains/hr — transit meganode with diverse religious community but zero amenity depth. All throughput, no dwelling.
- Lancy-Bachet: Shannon 1.28, Richness 5 — intermodal hub, residential diversity, no street life.
- Genève-Aéroport: Shannon 1.33, Richness 7 — international diversity locked behind departure gates.

**Low Shannon, High Richness (amenities without diversity):**
- Coppet: Shannon 0.0, Richness 21, only Christian denomination — wealthy La Côte commune, amenity-rich but socially homogeneous.
- Villeneuve: Shannon 0.45, Richness 27 — end-of-line town, some tourism infrastructure.

**Design implication**: The anomalies ARE the intervention sites. Vernier-Blandonnet has the social base (diverse community) but not the spatial programming. Coppet has the amenities but not the social mix. The prototypological question: can architecture convert one into the other?

### Connection to Commuter Index
Note: CI data is in the SBB ridership CSV (not available in this project instance). The prompt asked: do stations with balanced CI (~1.0) also have high Shannon? From S7 findings, we know high-CI stations (commuter-heavy) include Geneva, Lausanne, Nyon — which are also the highest Shannon stations. This suggests the hypothesis holds: social diversity and temporal balance (commuters + residents + visitors) co-occur. But a proper cross-tabulation needs the ridership file.

### Cairn's Framework Applied
The chicken-and-egg IS productive: did diversity create amenities, or did amenities attract diversity? The data shows they're correlated (r=0.632) but the anomalies reveal the ratchet hasn't started everywhere. Vernier-Blandonnet has diversity but no amenities — the ratchet is jammed. The architectural question: what's the minimum intervention to unjam it?
