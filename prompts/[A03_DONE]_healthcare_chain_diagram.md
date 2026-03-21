# Prompt: Healthcare Supply Chain — Full System Diagram

## Context
You're working on City101, analyzing the 101km Geneva–Villeneuve rail corridor. Read CONTEXT.md first.

The project has identified that the healthcare system is the backbone of the corridor's 24h operation. We need to map the FULL healthcare supply chain — not just "nurses can't get home" but every flow that keeps the system running.

## Task

### Phase 1: Research the actual flows
Research and document the real logistics of the Swiss healthcare system along the Geneva–Villeneuve corridor. Be thorough. Triple-check sources. Use web search for real data.

Map these flow categories:

| Flow | Key questions |
|---|---|
| **Medication/pharma** | How do medications arrive at hospitals? Airport (Cointrin) → warehouse → hospital? By train? By road? Who delivers — La Poste, DHL, dedicated pharma logistics (Galenica, Voigt, Alloga)? What arrives at 3am? |
| **Food/catering** | Hospital kitchens — where does food come from? Central kitchens? External catering (Compass Group, SV Group)? When do deliveries arrive? Who cooks for the night shift? |
| **Staff circulation** | Shift patterns — standard Swiss hospital shifts (early/late/night). How do staff commute during 01:00–05:00 dead window? What percentage drive vs public transport? |
| **Patient flows** | Catchment areas: who goes to HUG vs CHUV vs EHC Morges vs Hôpital de Nyon vs Rennaz? Transfer between hospitals? Hôtel des patients concept? Ronald McDonald House in Geneva? Who can't access care without a car? |
| **Postal/logistics** | La Poste, DHL, FedEx — night operations along the corridor. Sorting centers (where?). When do medical supplies get sorted? |
| **Lab samples/blood** | Inter-hospital lab sample transport? Blood bank (Transfusion CRS)? How do urgent samples move between sites? |
| **Waste/sterile** | Medical waste collection routes? Sterile supply chains? |
| **Emergency/ambulance** | Ambulance response times across corridor. Gaps in coverage. REGA helicopter placement. |

**Important filters:**
- Focus on the IN-BETWEEN, not the big centers. HUG and CHUV are fine — who falls through the cracks between them?
- Think about EHC Morges, Hôpital de Nyon, Ensemble Hospitalier de la Côte — smaller facilities
- NOT the millionaire going to Clinique de Montreux for recovery. The STAFF with harsh hours, the patient who needs EHC but has no car, the postal worker delivering meds at 3am.
- Consider: Hôtel des patients (CHUV has one), Ronald McDonald House (HUG area) — transitional spaces for patients/families

### Phase 2: Build the diagram

Create an interactive HTML diagram (`deliverables/A04/healthcare_chain_diagram.html`) that visualizes:

1. **The full chain** — all flow categories as color-coded paths/connections
2. **Geographic anchoring** — placed along the corridor (doesn't need to be a full map, can be a schematic linear diagram like a metro map)
3. **Day vs Night** — toggle or split showing how the system changes between day (06:00–22:00) and night (22:00–06:00), with the dead window (01:00–05:00) highlighted
4. **The nodes** — hospitals, sorting centers, warehouses, pharmacies, blood banks
5. **The gaps** — where links are missing or weakest. Where the chain breaks.

**Design specs:**
- Dark background (#0a0a0f or similar)
- Use the project's design system fonts: Instrument Serif (display), DM Sans (body), DM Mono (data)
- Colors: use the existing chrome-accent gold (#c9a84c) for highlights
- Clean, scannable, presentation-ready (this goes in the midterm PPTX as a screenshot or live demo)
- Interactive: hover for details, click for more info
- Include a clear legend

### Phase 3: Verify everything

- Every claim must have a source (URL, report name, or dataset reference)
- Create a verification table at the bottom of the HTML or as a separate file
- Flag anything that's assumed vs confirmed
- Cross-reference with existing datasets in `datasets/` and `source/`

## Output
- `deliverables/A04/healthcare_chain_diagram.html` — the interactive diagram
- `deliverables/A04/healthcare_chain_research.md` — the research document with sources
- Commit both with a clear message

## Quality bar
This goes in the midterm. It must be conclusive, sourced, and visually clean. No hallucinated data. If you can't find something, say "NOT FOUND — needs manual verification" rather than making it up.
