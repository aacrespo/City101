# The Kitchen Analogy — How city101 Works

*A way to explain the city101 system architecture to anyone, using the metaphor of a professional kitchen.*

## The Pitch

> The repo is a professional kitchen. Claude is the head chef who reads the board, knows every station, and coordinates the team. Archibase is the pantry — verified ingredients and reference books. The parametric scripts are recipes. And the whole system improves after every service.

---

## The Full Map

### The Kitchen (city101 repo)

| Repo element | Kitchen equivalent |
|---|---|
| **CLAUDE.md** (router, loads every session) | **The kitchen layout diagram** on the wall — where everything is, which station does what, house rules. Every chef reads it on day one. |
| **.claude/rules/** (conventions, data protocol, tool protocol) | **Health & safety code + house standards** — how to label containers, storage temperatures, hygiene rules. Non-negotiable. |
| **Claude (main session)** | **The head chef** — reads the board, delegates to stations, decides what gets plated, coordinates the whole service. |
| **Subagents / Agent teams** | **Line cooks** — the head chef calls out "I need a risotto and a salad" and two cooks work in parallel. Each has their station, their tools, their specialty. |
| **Roles** (/analyst, /modeler, /cartographer...) | **Stations** — pastry, grill, saute, garde manger. Same person can work different stations, but each station has its own tools and techniques. |
| **Archibase (the knowledge system)** | **The pantry + reference library** — ingredients (L1 database), technique books (L2 guides), the photo binder of plated dishes (L4 visual search). You go in, get what you need, come back to your station. |
| **Parametric scripts** | **Recipes** — take inputs, produce a dish. Constraints are encoded: "always 120mm insulation" = "always deglaze with wine before adding stock." |
| **datasets/** (verified production data) | **The walk-in fridge** — quality-checked, labeled, dated ingredients ready for service. Nothing goes in without inspection. |
| **output/** (staging) | **The prep counter** — where raw ingredients get cleaned, cut, checked before going into the fridge. Might get rejected. |
| **source/** (frozen originals) | **The delivery crates** — untouched, exactly as the supplier sent them. You take from them, you never put anything back in. |
| **LOCKBOARD.md** (who's doing what) | **The ticket rail** — what's on order, who's working what, what's firing next. |
| **CONTEXT.md + CONTEXT_ANDREA/HENNA.md** | **The shift handover notes** — "table 5 has allergies, the fish delivery was late, we're 86'd on the lamb." |
| **LEARNINGS.md** | **The kitchen bible** — "never use copper with acidic sauces," "the oven runs 10 degrees hot." Hard-won lessons from past services. |
| **workflows/** | **Standard operating procedures** — "how to prep for brunch service," "how to close the grill station." Step-by-step, tested. |
| **tools/** | **Kitchen equipment** — mandoline, immersion blender, thermometer. Reusable, shared across stations. Check the rack before buying a new one. |
| **observations/** | **Tasting notes + R&D journal** — "tried fermenting the carrots, interesting but not ready for the menu." Dead ends and discoveries. |
| **design_system/SPEC.md** | **Plating guide** — the house aesthetic. What plates to use, garnish style, color palette. |
| **deliverables/** | **The pass** — plated dishes ready to go to the table. Final, presentation-quality. |
| **The learning loop** (build, review, learnings, next build) | **Post-service debrief** — "the souffle collapsed, the timing on table 12 was off, write it down." Next shift reads it. The kitchen gets better every night. |
| **The data flow** (source, output, verify, datasets) | **Supplier, prep counter, quality check, walk-in** — nothing hits the fridge without inspection, nothing hits the plate without coming from the fridge. |

---

### The Dining Room (Rhino MCP)

The kitchen is where all the thinking, prepping, and cooking happens. But none of it matters until it reaches the plate on the table. Rhino is where the food actually gets plated and served — where abstract knowledge becomes a physical thing someone can see and judge.

| Rhino MCP element | Kitchen equivalent |
|---|---|
| **Rhino itself** | **The dining room + pass** — the space where dishes materialize and get presented |
| **MCP connection** (the bridge between Claude and Rhino) | **The pass window** — the opening between kitchen and dining room. Chef calls out, plate comes through. |
| **Router mode** (multi-port, multiple agents) | **Multiple pass windows** — a busy restaurant where grill, pastry, and saute all slide dishes onto the pass simultaneously. One dining room, multiple stations feeding it. |
| **Standard mode** (single port) | **One pass window** — small bistro, one chef, one opening. Simpler but it works. |
| **Layers in Rhino** (agents share one instance via layers) | **Sections of the table** — one table, but each cook is responsible for their course. Starter on the left, main in the center, dessert on the right. They don't touch each other's plates. |
| **capture_viewport** (screenshot) | **Looking through the pass window** to check how the plate looks before it goes out |
| **The Mac one-Rhino limitation** | **One dining room** — you can't clone the restaurant. Everyone serves to the same room, just from different windows. |

The key insight: the kitchen doesn't serve itself. Without the pass window (MCP) and the dining room (Rhino), all that knowledge, all those recipes, all that prep — stays in the back. The MCP is what makes the kitchen useful.

---

### RAG vs CAG — Pantry Trips vs Mise en Place

**RAG** (Retrieval-Augmented Generation) = **Going to the pantry mid-service.** A ticket comes in, you don't know the recipe by heart, you walk to the pantry, scan the shelves, grab what looks right, walk back, cook. Every time. It works, but there's a trip involved — and you might grab the wrong jar if you're in a hurry.

**CAG** (Context-Augmented Generation) = **Mise en place.** Before service starts, you read tonight's menu, pull everything you'll need, chop it, measure it, line it up on your station. When the ticket comes in, everything is already at arm's reach. No pantry trip. Faster, and you know exactly what you're working with because you prepped it yourself.

| | RAG | CAG |
|---|---|---|
| **Kitchen version** | Walk to pantry per order | Mise en place before service |
| **What happens** | Query, search vector DB, retrieve chunks, feed to agent | Pre-load the right docs into context before the agent starts |
| **Archibase example** | Agent searches 35K chunks for "timber wall thickness" at runtime | Playbook + relevant L2 guides loaded into agent prompt from the start |
| **Tradeoff** | Can access everything, but retrieval might miss or return noise | Limited by what fits on the counter (context window), but faster and more reliable |
| **When it's better** | Unexpected questions, broad exploration, "what do we have on X?" | Known task, known knowledge needed — modeling a wall, you know which guides matter |

The system uses both — just like a real kitchen. You do your mise en place (CAG: load the playbook, the relevant guides, the learnings), but you keep the pantry open (RAG: search archibase if you hit something unexpected mid-build).

The playbook is literally this: it's the prep list that tells the chef what to have on the station before service starts.

---

*Written by Lumen (Andrea school account) — March 24, 2026*
*From a conversation with Andrea about explaining the city101 architecture through analogy.*
