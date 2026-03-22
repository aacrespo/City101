# Still On The Line — Midterm Presentation Speech
## A04 — Forms of Sentience
### ~12 minutes, two speakers

**Speakers**: Andrea (A), Henna (H)
**Format**: 4 HTML presentations, 6 screens each, shown sequentially.
**Tip**: Click "play sequence" on each HTML to auto-highlight panels, or just talk through them freely.

---

## PRESENTATION 01 — The Archipelago

### [Screen 1: Title]

**H:** Last semester we asked whether 101 kilometers of lakefront rail — Geneva to Villeneuve, 49 stations, a million inhabitants — functions as one continuous city.

We built an index to answer that. The Working Continuity Index measures five dimensions at every station: transit frequency, workspace, connectivity, temporal coverage, and mobility options. Behind it: 41 verified datasets, 8 API sources, 33 classmate datasets cross-referenced spatially.

The answer was no.

### [Screen 2: WCI Corridor Strip]

**A:** What you're looking at is every station on the corridor, west to east. The height is the WCI score. Red is broken. Green is connected.

Only 11 of 49 stations — 22% — maintain full working continuity. Three structural gaps rupture the line: Nyon to Gland, Gland to Morges, and the Lavaux Fracture — 17.5 kilometers of UNESCO-protected terrain where the infrastructure simply vanishes.

The corridor is not a city. It's an archipelago.

### [Screen 3: Evidence Layers]

**H:** We didn't stop at one visualization. We built nine interactive tools to interrogate the data from different angles — GA cost inequity, temporal pulse, diversity indices, journey workability, station exploration, demographic mapping. Plus a full scrollytelling site with seven Leaflet maps.

Each one confirmed the same pattern: the gaps are structural, not temporal. 14 stations work at rush hour. 13 work at 11 PM. The archipelago barely pulses.

### [Screen 4: Zurich Benchmark]

**A:** To verify this wasn't just how rail corridors work, we benchmarked against Zurich's S8 line. Same country, same operator, same rolling stock.

Zurich compresses frequency variation to 12 times. City101 produces 42 times — 3.5 times worse. Zurich's worst station gets 2 trains per hour. Ours gets zero. The problem is specific to this corridor.

A linear city has to *construct* the continuity that a radial city inherits from geometry.

### [Screen 5: Argument Chain]

**H:** So the argument builds in four phases. A01 collected the data — 49 stations, 41 datasets. A02 proved the archipelago — only 22% connected. A03 validated in the field — 7 sites visited, 24 candidates narrowed to 9. And A04, where we are now, is designing the architecture that holds the gap.

### [Screen 6: Core Thesis]

**A:** The thesis: the corridor is an archipelago. The architecture is the lock.

We're not proposing faster trains or more stations. We're proposing a new typology — the relay-lock — that holds people through the gap instead of trying to eliminate it. The dwell time *is* the architecture.

Three people define the problem: a night shift nurse stranded when the M2 stops at 1 AM. A home care worker doing 6 stops per shift with no transit after 01:30. A frontalier nurse — one of 160,000 — who earns 2.5 times her French salary but has zero reliable transport home after midnight.

---

*[Switch to Presentation 02]*

## PRESENTATION 02 — Healthcare Corridor

### [Screen 1: Title]

**A:** Why healthcare? Because this corridor operates as a single hospital.

32,000 workers across 6 major institutions — HUG in Geneva, GHOL Nyon, EHC Morges, CHUV Lausanne, HRC Rennaz, plus Genolier on the hilltop. They share patients, blood products, pharmaceutical supply, catering, staff. One system, 101 kilometers long.

And every night at 01:00, the entire transport network flatlines. For four and a half hours — zero public transport. 4,600 healthcare workers are on shift. Stranded.

### [Screen 2: The 9-Node Network]

**H:** This is the relay-lock network. Nine nodes, spaced roughly 11 kilometers apart — caravanserai logic applied to motorized travel.

Each node has a specific lock type based on what breaks there. Lancy-Pont-Rouge is a border lock — frontalier equalization. Nyon-Genolier is an altitude lock — valley to hilltop. Morges is a temporal lock — the dead window shelter. CHUV is the sky lobby — the dispatcher for the entire Vaud healthcare system.

Remove any one node and the healthcare chain breaks.

### [Screen 3: The Dead Window]

**A:** Let's be specific about what "dead window" means.

CHUV shift change: 22:45. HUG shift change: 21:15. Both end after the last metro and the last Léman Express. 60% of HUG's nurses live in France — they have no way home.

A taxi from Morges to Nyon costs 55 francs. Lausanne to Vevey: 80. A round-trip night commute: 110 francs. For nurses earning modest salaries, that's not a transportation cost — it's a tax on essential work.

And ambulance coverage halves at night. Riviera goes from 4 crews to 2. SIS Geneva reduces from 3 casernes to 1. The Nyon-to-Morges gap — 23 kilometers — has no emergency department at all. 150,000 people.

### [Screen 4: Four Circulations]

**H:** The corridor carries four flows that never stop, even when transit does.

Staff — 32,000 workers, 6 night shifts per month, frontaliers crossing the border. Patients — 800,000 in CHUV's catchment alone, transferred between facilities daily. Cargo — Galexis in Ecublens processes 100,000 pharmaceutical packs per day for all of French-speaking Switzerland. Swiss Post delivers to 220 operating theaters by 6 AM. And home care — AVASAD and IMAD together employ 7,300 field workers doing insulin rounds and wound care through the night.

The corridor functions as one organism. The transport system treats it as a commuter pipeline that shuts off at midnight.

### [Screen 5: The Frontalier Trap]

**A:** The frontalier situation is a designed inequality.

7,200 healthcare workers cross the border daily. They earn 2.5 times what they'd make in France — that's what attracts them. But the Léman Express stops at 00:30 and starts at 05:00. Noctambus runs weekends only. Night buses: weekends only. Monday through Thursday, when night shifts actually run, there is nothing.

The salary attracts them. The infrastructure abandons them.

And there's a patient accommodation gap: CHUV has 108 rooms. HUG has 10. Nyon, Morges, Rennaz — zero. Families of hospitalized patients in those cities have nowhere to stay.

### [Screen 6: The Lock Proposition]

**H:** So the proposition is clear. Healthcare never stops. Transport does. The lock is the architecture of that contradiction — a chamber where people survive modal collapse.

Nine nodes. Four circulations. Seven lock types — border, altitude, temporal, logistics, sky lobby, gap relay, bridge. Each one designed for the specific break at that point in the corridor.

---

*[Switch to Presentation 03]*

## PRESENTATION 03 — AI Methodology

### [Screen 1: Title]

**A:** Now — how we're actually building this.

Claude is not a tool we use. It's the third member of our team. It has 12 specialized roles, persistent memory of our project, and coordinates with us through a shared lockboard. When I leave a session, I write what I did. When Henna picks up, Claude already knows what changed.

### [Screen 2: Agent Team]

**H:** The system has five primary roles — analyst, cartographer, modeler, visualizer, builder — plus seven specialist reviewers for things like structural code, accessibility compliance, and building envelope performance.

When we model a lock node, we don't run one agent. We assemble a team. For Lock 05 — the CHUV node — Andrea ran 7 agents in parallel: modeler, concept critic, structural reviewer, accessibility, envelope, log compliance, and site context builder. They produced 709 geometry objects across 4 rounds.

That's not us clicking buttons in Rhino. That's a roundtable of specialists debating the building.

### [Screen 3: MCP Router]

**A:** The technical innovation is the MCP router — Model Context Protocol. It's a TCP proxy I wrote, 1,200 lines, that lets multiple Claude agents talk to Rhino simultaneously.

One agent models the structural shell on port 9001. Another handles MEP systems on 9002. A third works on the envelope on 9003. They share the same Rhino session but work on separate layers, with thread-safe locks so they never collide.

31 routing tools — geometry creation, boolean operations, lofts, sweeps, code execution, viewport capture. The agents don't describe what to build. They build it.

### [Screen 4: Command Ecosystem]

**H:** The whole system is organized in four layers. Layer 1 loads automatically — project rules, conventions, data protocol. Layer 2 activates on demand — you type /analyst and Claude becomes an analyst with the right context. Layer 3 is reference — living project state, learnings, the lockboard. Layer 4 is execution — 14 Python tools and 15 workflow SOPs.

20 slash commands total. Session management, team assembly, parametric script generation, data verification, Rhino review, terrain import. Each one loads exactly the context that role needs — nothing more.

### [Screen 5: Relay-Lock Configurator]

**A:** The app ties it all together. Six modules: a corridor knowledge base with 3,200 records, a community research engine that will use Claude's API to identify who is stranded, a scoring engine with 5 weighted criteria, a lock type assignment algorithm, an output pipeline that generates spec cards and Rhino scripts, and a two-tab interface for analysis and output.

The key design decision: the AI finds *who* is stranded — that's the research. Everything downstream — scoring, type assignment, parameter generation — is deterministic JavaScript. We know exactly why each site was chosen.

### [Screen 6: Data to Form]

**H:** The pipeline runs like this: 34 datasets become 21 visualizations. The visualizations reveal the 9 nodes. The nodes generate 3D models in Rhino through the MCP router.

Data to form. Not data *and* form. The architecture is a direct consequence of the measurement.

---

*[Switch to Presentation 04]*

## PRESENTATION 04 — Progress & Equipment

### [Screen 1: Where We Stand]

**A:** Three phases are complete. The fourth is active with 8 days to midterm.

34 verified datasets. 21 interactive visualizations plus 6 diagrams. 9 relay-lock nodes scored and positioned. 709 geometry objects in the CHUV prototype. A 46-page research paper. And the March 16 crit gave us the green light — you called it cutting edge.

### [Screen 2: Phase Timeline]

**H:** A01: we collected everything. 49 stations, 33 classmate datasets, 8 API sources. A02: we proved the archipelago — submitted March 3rd. A03: we went to the field — 7 sites visited, 24 candidates narrowed to 9. A04: we're building the prototypology.

The green light on March 16 was the turning point. We're now in full production.

### [Screen 3: Production Inventory]

**A:** A quick inventory of what exists. 34 CSV datasets across 8 categories. 27 visualizations and diagrams — including a transport pulse animation rendering 29,135 trips across all modes with 3D terrain. A full scrollytelling site. The CHUV prototype with 709 objects. 15 app architecture documents. And these four presentations.

### [Screen 4: Midterm Checklist]

**H:** For March 30, the brief requires at least 3 MCP-generated prototypological models with turntable animations, 3 axonometric site interpretations, and MCP methodology diagrams.

We have one full node — CHUV — with the workflow proven. The critical path is scaling that to Morges, Nyon, and Rennaz. Andrea has the agent team protocol ready. The workflow is repeatable — it's a matter of execution now.

### [Screen 5: Team Allocation]

**A:** Andrea — prototypology lead. Scaling the MCP modeling to all required nodes, building the scoring engine, coordinating the agent teams.

Henna — 3D corridor and presentation. Full corridor modeling, point cloud pipeline, axonometric drawings, and the brand identity that holds all of this together.

Claude — the third member. Agent team execution, research, data verification, visualization pipeline. Five accounts, persistent context across all of them.

### [Screen 6: Equipment Request]

**H:** To finish at this level of ambition, we need three things.

First: a virtual or extended monitor. Agent team modeling means running Rhino, Claude Code, and 3D preview simultaneously. On a single laptop screen, we're constantly switching windows. A second display would directly accelerate the modeling cycle.

Second: GPU access. The transport pulse animation renders nearly 30,000 trips with 3D terrain. MapLibre and Three.js need a dedicated GPU for smooth turntable captures. Our current setup struggles with complex scenes.

**A:** Third: continued Claude Max access. The agent team workflow — 12 roles, parallel execution, MCP routing — requires extended context and high throughput. You offered to fund the subscription at the March 16 crit. We'd like to take you up on that. Scaling from 1 node to 9 depends on it.

**H:** The data says the linear city doesn't exist. We're building the architecture that might make it possible. These are the tools we need to finish.

Thank you.

---

*[~12 minutes at conversational pace]*

## Speaker notes

- **Presentation switching**: Have all 4 HTML files open in browser tabs. Switch between them at the marked points.
- **Play sequence**: Each presentation has a play button that highlights panels one at a time (3.5s each). You can use it during pauses or skip it and point directly.
- **Pace**: The healthcare section (02) is the densest. Slow down for the numbers — they're powerful. Let the dead window cost (CHF 55/80/110) land.
- **Tone**: A02 speech was analytical. This one should feel more urgent — you're not just measuring anymore, you're proposing. The healthcare data makes it human.
- **The handoff**: Andrea handles the technical/conceptual (MCP, scoring, thesis). Henna handles the spatial/visual (corridor, nodes, brand, equipment). The split should feel natural, not rigid.
- **If short on time**: Cut Screen 5 (frontalier trap) from Presentation 02 — fold the key number (7,200 nurses, 2.5x salary) into the dead window section. Cut Screen 4 (command ecosystem) from Presentation 03.
