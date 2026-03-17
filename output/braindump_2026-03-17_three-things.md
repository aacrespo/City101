# Brain Dump — 2026-03-17
**Session**: Cairn Code, Andrea
**Status**: Captured, not yet acted on

---

## 1. Concept Update (evolved since March 10)

### Core metaphor
Vertical elevator → Horizontal elevator. Communes/cities = floors. The corridor = the building.

### Key moves
- Elevator is **anti-architecture** (changes relationship of proportionality in construction — a little elevator now makes extremely different usage possible for different floors, variety beyond what architectural proportions consider realistic)
- Horizontal elevator is **anti-urban** (changes hierarchy, power dynamics)
- What "breaks" a vertical elevator = power outage. What breaks the horizontal elevator = **the gap in the 24hr chain** (1am–3am, no public transport)

### The chamber is NOT a backup generator
- A generator is a backup that restores the same thing
- The chamber is the **missing link** in the 24hr chain — it doesn't restore, it *fills*
- Unlike most technology that eliminates gaps or makes things faster/obsolete, **this typology holds the gap**
- "We design the experience of waiting" — the equalizer
- Infrastructure that doesn't want to skip the gap, doesn't want to make it disappear

### Chamber = waiting infrastructure
- Transports/carries/holds people and goods
- Also an expression of the information and coordination that happens between nodes
- At the breaking point of the 24hr chain for healthcare (1am–3am)

### Beyond healthcare
- Healthcare is the proof-of-concept, but the typology is **infrastructure for waiting**
- Applies to ANY community with breaks in the 24hr chain
- Example: **bakery industry** — early morning shifts (dough proofing, baking starts before dawn), lab-to-shop transport for chains, staff with non-standard working times needing transport
- Many more communities exist at the 1am–3am breaking point

---

## 2. The Interface / App Vision

### User flow
1. User comes to the interface
2. Says: "I want to use the Still on the Line typology to solve [community]'s problem in [region]"
   - Example: "Help the bakery industry between Rennaz and Montreux"
3. **AI researches** that community's full chain (like we did for healthcare)
   - Research all bakeries, enterprises, working chain
   - Which are local (bake in-store) vs need transport (lab → shop)
   - Same depth as the healthcare chain analysis
4. **Compare to existing 24hr chain research** on transport
5. **List breaking points** along the corridor for that community
6. **Check if breaking points are in user's specified region**
7. **AI is critical** — if the research shows the biggest breaking point isn't in the user's region, say so: "For this problem, it's better to implement in [other zone] because after my research, [reasoning]"
8. If user insists on their region, adapt: quick scan on how typology fits better there, through which communities

### Proposition generation
9. AI proposes a solution — **best compromise** considering typology values
   - AI-generated 3D image for quick visualization
   - Presented as: "considering all variables, this is the best compromise in my opinion"
10. **Parameter panel** where user adjusts criteria weights:
    - Invisible vs carbon-efficient
    - Low carbon footprint vs maximizing user comfort
    - (other typology criteria TBD)
11. Based on adjusted weights, **new propositions with their compromises**
12. Each proposition has an **info block** showing:
    - Main choices made
    - Compromises/tradeoffs (e.g., all glass → need AC → higher carbon footprint)

### Outputs
13. **Tech/spec sheet** of all variables for chosen proposition
14. **3D model script** — button to generate Rhino script for modelization
15. **3D preview** — OSM map in 3D in the interface (previsualisation)
16. **24hr usage video** — model in Blender, generate video of how usage looks across 24hr cycle (maybe Nona Banana or other AI generation with Blender/NotebookLM)

### Open questions
- **Rhino integration**: Can we embed viewport in app? Or require local Rhino + MCP? Or is script a separate output?
- **Output format**: .py Rhino script vs .json for easier web integration? Maybe both — .json for preview, .py for architect's tool
- **Cadastre**: Need to integrate cadastre data so AI knows where you can/can't build
- **Site placement**: Blank space (empty property) vs integrated into existing building vs connecting existing points with transport
- **Power source**: Solar? Water? Electric? Fuel?
- **Construction logistics**: Vents, water flows, drainage, electricity — post-midterm
- **Decentralized servers**: Data center nodes at each typology point — information flow infrastructure
- **Concept definition needed**: Is it actual transport or just a place? What are fixed vs flexible variables?

### Scaling vision
- First: corridor only (healthcare as model case)
- Then: any community on the corridor
- Then: any Swiss city with same data (point clouds, topography, transport systems)
- Typology transcends place

---

## 3. Modeling Status Check

See: plan file `~/.claude/plans/humming-wishing-minsky.md`

### Current state (from agent assessment)
- **Wave 1-2 complete**: Research done, 3 lock scripts verified (Morges, CHUV, Rennaz) at LOG 200-300
- **Wave 3 scaffolded**: Skills and review agents drafted but untested
- **Wave 4 not started**: Actual LOG 400 upgrades + review panel execution

### Midterm goal (March 30)
- LOG 400 visuals of nodes from v2 paper
- Show Rhino scripting quality + territory integration
- Build the iterative review system
- Structure repo tools and lessons for better modeling from scratch

### Post-midterm ambitions
- Construction-level detail (vents, water, drainage, electricity)
- Power source decisions
- Decentralized data nodes
- Blender/AI video of 24hr usage
- Full interface/app

---

## Priorities / Open threads
- **Read v2 paper** — defines 9 nodes, locks down concept. Everything flows from this.
- **Update CONTEXT.md** — a week stale, needs evolved concept, crit outcome, new phase
- **Henna task split** — already discussed, needs to be documented
- **App architecture** — diagram level, not implementation. For midterm: show logic, not product.
- **Session/brain-dump storage system** — idea for future: proper sessions folder or context-output system
