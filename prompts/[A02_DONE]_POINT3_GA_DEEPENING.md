# Point 3: GA Hypothesis — Deepening Prompt
**For**: Lumen (browser, web search) or Cairn
**Priority**: MEDIUM — core cost map done (S8), this is enrichment
**Status**: Cost map ✅ completed. What remains: real-world validation + behavioral segmentation data.

---

## What's done

- Distance-based tariff pricing for 35 OD pairs and 49 corridor stations ✅
- GA breakeven analysis (85 trips / 4.2 months) ✅
- Budget corridor concept (CHF 20 = 41km city) ✅
- Short-hop penalty analysis ✅
- Findings document ✅

## What would strengthen the argument

### A. Validate 5-10 key prices against SBB website (Lumen via Chrome)
Navigate to sbb.ch, search connections, extract actual 2nd class full-fare prices for:
1. Genève → Lausanne
2. Genève → Nyon
3. Genève → Morges
4. Lausanne → Vevey
5. Lausanne → Montreux
6. Montreux → Villeneuve VD
7. Genève → Montreux
8. Genève → Villeneuve VD
9. Nyon → Lausanne
10. Vevey → Aigle

**Method**: On sbb.ch, enter from/to, select a Monday morning connection, click on the connection, find "Point-to-point ticket" price in 2nd class. Make sure price display is set to "Full fare" not "Half Fare Travelcard" (default shows Halbtax prices).

**Output**: Simple table of validated prices → update `city101_ga_cost_corridor.csv` with a `price_validated_chf` column for the stations we checked. Note the delta vs our estimate.

### B. GA penetration data (web research)
Search for:
- "GA Travelcard statistics Switzerland" or "Generalabonnement Statistik"
- SBB annual report → number of GA holders
- OFS MRMT (Mikrozensus Mobilität und Verkehr) → GA penetration by canton
- Any commune-level or corridor-level data on GA ownership rates

**Key questions:**
- What % of Vaud/Geneva residents hold GA?
- How does GA penetration vary along the corridor?
- Is there data on GA holders by commune?

### C. Frontalier transport data
Search for:
- OCSTAT (Geneva statistics office) frontalier commuting data
- Léman Express ridership by station (especially cross-border stations)
- CTSO (Conférence des transports de Suisse occidentale) reports
- Any data on how frontaliers actually commute (car vs train vs bus)

**Key questions:**
- What % of Geneva frontaliers use public transport?
- Léman Express ridership at Annemasse, Lancy-Pont-Rouge, Genève-Eaux-Vives?
- Cost of a Léman Express monthly pass (Unireso) vs GA?

### D. Commune-level modal split
Search for:
- OFS "pendlermobilität" (commuter mobility) data
- Commune-level car vs PT vs bike modal split along the corridor
- Any opendata.swiss datasets on transport mode choice

This would let us map: "In communes with >60% car commuting, GA penetration is low, and the corridor fragmentates further."

### E. Behavioral segmentation framework
The classmate crossref (S7) already provides evidence for different corridor populations:
- **Commuters** (high CI stations): Lancy-Pont-Rouge 4.04, Zimeysa 6.86
- **Tourists** (low CI): Épesses 0.47, Montreux 1.02
- **Students** (EPFL/UNIL effect): Lausanne, Renens
- **Gig workers** (Charlene's data): 50 locations, following tourist flows
- **Healthcare users** (Thomas's data): 389 medical facilities
- **Industrial workers** (Siméon's data): 195 companies + 25 zones

Each group experiences the corridor differently. GA holders are "corridor citizens." Non-GA holders are "city residents who occasionally visit another city." Frontaliers are "ghost citizens." Tourists are "corridor consumers."

**Output**: A behavioral segmentation table mapping each group to their likely ticket type, corridor experience, and where they break.

## Output files

- `city101_ga_prices_validated.csv` — if prices are validated via SBB website
- `GA_HYPOTHESIS_RESEARCH.md` — findings from B, C, D, E
- Updates to `GA_COST_FINDINGS.md` if significant new numbers

## Time budget

- Price validation (A): 30 min (if Chrome MCP available)
- Web research (B-D): 45 min
- Segmentation framework (E): 20 min
Total: ~90 min, but can be split across sessions

## Note

This is enrichment, not critical path. The core GA argument is already strong enough for the desk crit with what we have. This work strengthens it for the final submission and design phase.
