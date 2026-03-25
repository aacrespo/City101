# The Kitchen — Canonical Reference

### How we accidentally built an architecture studio's digital infrastructure, explained through the only analogy that made sense

*Presentation + animation reference. Single source of truth.*

---

## 1. Why We Built It

It started with forgetting.

Every time a new conversation began, Claude walked in with an empty backpack. No memory of yesterday's work, no idea what was half-finished, what had failed, what to do next. The context window — the backpack — could only hold what was loaded right now.

So we started writing handoffs. After every session: here's what we did, here's the state of the model, here's the naming convention, here's what broke. Manually. Every time. Andrea copying into Henna's account, Henna copying back. Two people passing recipes through a window.

It worked. Barely. The cost wasn't the writing — it was the re-reading. Every new session burned backpack space just catching up. As the project grew, the handoffs got longer, the catching-up got heavier, and the actual cooking window got shorter.

We were spending more time explaining the kitchen than using it.

Every tool in this system — every single one — was introduced because something hurt. Not because we planned an infrastructure. The kitchen built itself around the need.

> *Animation note: show Andrea and Henna with their accounts (little Claudes with different personalities, colors, emotes), passing documents back and forth through a window. Backpacks getting heavier with each handoff.*

---

## 2. The Logbook: Git

We needed more than handoffs. We needed a persistent record of every decision, every change, every version — something you could flip back through and see: this is when we moved the circulation core south, this is when the cooling system changed, this is where that idea died.

That's Git. Not just memory for the process booklet — though it gives us that too. It's the logbook, the exploration record, the ability to recall paths already tried and threads left open. Every commit is a dated entry. Every branch is a design alternative explored without destroying the original. Every merge is a decision made.

We didn't adopt git because we're programmers. We adopted it because the only tools that existed for this kind of work were built for programmers — and Rhino MCP was the gateway. We were already handling scripts and iterations, so branches, version control, tracking back to where a mistake happened — it all made sense. And we wanted the memory. At the end, we flip through the whole book and the story of how we built everything is already written. No mental load of cataloguing every piece of paper.

### The shared kitchen: GitHub

Git is the logbook. GitHub is the shared kitchen.

Andrea created an empty repository — an empty kitchen. Cloned it to her machine. Furnished it: project brief, file structure, conventions. She was the only cook, so everything went straight to the main book.

Then Henna arrived. She cloned the kitchen to her own machine. Instantly: a full copy of everything — not just the current state, but the entire history of decisions. She inherited the kitchen and the story of how it was built.

From that point: pull requests. "I developed this dish at my station, please *pull* it into the menu when you're ready." Same recipe book, never the same counter. You can't knock over each other's pots.

> *Animation note: show the empty repo, Andrea furnishing it, pushing to GitHub (the shared cloud kitchen), Henna pulling a clone. Two kitchens, one book.*

---

## 3. The Brigade

Every kitchen has a hierarchy. Ours maps to three levels of operation — and three levels of how you use AI:

### The roles

| Brigade role | Our system | What they do |
|---|---|---|
| **Chef de cuisine** | The user (Andrea / Henna) | Decides the menu, runs the service, final call on everything. |
| **Sous chef** | Claude (main session) | Second in command. Can cook alone, can orchestrate the whole team. But has a backpack instead of a memory — every shift starts empty. |
| **Chef de partie** | Agent teams (TeamCreate sessions) | Station chiefs. Each runs their own station with specialized knowledge. They communicate across stations — "firing the main in 3 minutes!" — and build on each other's work. Persistent, not disposable. More like a research lab: different people doing different things that build upon each other. More brainpower, specialized knowledge for each. |
| **Commis** | Subagents | Junior cooks. Temporary. "Dice these onions." They do their task, hand it back, disappear. Can't talk to each other. Focused, fast, disposable. |

### The three levels

The brigade isn't just a hierarchy — it's three ways of working:

| Level | User role | What's happening |
|---|---|---|
| **Basic** | Chef de partie | You give direct orders, Claude is a commis. No context management, no specialization. "Make me a box." One station, one tool. |
| **Intermediate** | Sous chef | You manage Claude + subagents. Two tiers. Context starts mattering — what goes in the backpack, what doesn't. |
| **Advanced** | Chef de cuisine | You orchestrate through a main Claude (sous chef) who manages agent teams (chefs de partie) and subagents (commis). Full context architecture. The whole restaurant is running. |

We started at level 1. The work demanded more.

> *Animation note: show the three levels as progressively larger kitchen setups. Level 1 = one person at a counter. Level 2 = small team. Level 3 = full brigade.*

---

## 4. The Kitchen: Three Pillars

The kitchen is organized around three things: infrastructure, context, and teamwork.

### Pillar 1 — Base infrastructure (nothing goes stale)

The workflows, commands, automations. The mental load relief. How the fridge is organized, how closing procedures work, the labeling system. Built once, saves time every service.

| Repo element | Kitchen equivalent |
|---|---|
| **workflows/** | **Standard operating procedures** — how to prep for brunch, how to close the grill station |
| **tools/** | **Kitchen equipment** — mandoline, thermometer. Check the rack before buying a new one |
| **/session-start, /session-end, /save-session** | **Opening and closing procedures** — read the board, update the handover notes, nothing gets forgotten |
| **LOCKBOARD.md** | **The ticket rail** — what's on order, who's working what, what's firing next |
| **CONTEXT.md + CONTEXT_ANDREA/HENNA.md** | **Shift handover notes** — "table 5 has allergies, the fish delivery was late, we're 86'd on the lamb" |
| **LEARNINGS.md** | **The kitchen bible** — "the oven runs 10 degrees hot." Hard-won lessons from past services |

### Pillar 2 — Context management (the backpack problem)

Everything is context management. The backpack is finite. Every scroll that goes in costs space. Context engineering IS the skill.

| Repo element | Kitchen equivalent |
|---|---|
| **CLAUDE.md** | **The map on the wall** — not what to know, but where to find what you need. First thing in the backpack, every time. |
| **.claude/rules/** | **Tool descriptions + instruction manuals** — conventions, protocols, safety rules. Goes in the backpack automatically. Be careful: ten manuals and the backpack is half full before cooking starts. |
| **Specialist agents** (/analyst, /modeler, /cartographer) | **Station knowledge** — when you call a specialist, their tools and knowledge enter the backpack. A modeling agent doesn't carry research context. A research agent doesn't carry Rhino commands. Specialization IS context management. |
| **Archibase** | **The pantry** — see Section 5 |

The specialists were introduced because the more we did a specific task, the more that agent learned it. But when we wanted something different — research vs visualization, modeling vs data — the main agent didn't need that extra context. Agent creation is context management. Everything is context management.

> *Animation note: show Claude entering the kitchen through a door. The map (CLAUDE.md) goes in the backpack first. Then the rules (.claude/) as scrolls. Backpack visibly grows. When a specialist is called, extra tools + knowledge scrolls go in — maybe an accessory or apron change to show the station switch. The backpack keeps growing. Show the tension: more knowledge = less room to cook.*

### Pillar 3 — Productivity and teamwork (the actual cooking)

MCP tools, agent teams, practical collaboration. How the dishes actually get made.

| Element | Kitchen equivalent |
|---|---|
| **MCP** | **The cable** connecting kitchen to dining room. Without it, everything stays in the back. |
| **MCP plugin** (e.g. rhinomcp) | **The socket** — what the cable plugs into on the Rhino/Blender side |
| **Router** (multi-port MCP) | **The multiprise** — one cable, multiple sockets. Multiple agents can connect to the same tool. |
| **Agent teams** (chefs de partie) | **The research lab** — different people doing different things that build on each other. They can communicate, figure things out together. |
| **Subagents** (commis) | **Prep cooks** — "dice these onions, come back when done." Fast, focused, disposable. |
| **deliverables/** | **The pass** — plated dishes, presentation-quality, ready for the table |

---

## 5. The Pantry: Archibase

Claude is an AI. It can reason, plan, orchestrate. It knows how to stack things — this goes on top of that. But it doesn't know how to *build*. No joints. No assemblies. No corners. No tectonic logic. No physics — nothing overlaps, everything has thickness, things have to fit together. It doesn't need to learn how to think. It needs to learn how to construct.

The more specific knowledge it has — parameters, dimensions, conventions, norms, construction details across domains — the better it can merge the modeling side and the knowledge side. But modeling is a huge task, and the backpack is finite. The context has to be well-engineered so it knows enough to build properly but still has room to actually work.

That's Archibase. The pantry.

| Pantry layer | What's inside |
|---|---|
| **L1 — Database (SQLite)** | Materials, KBOB (Swiss LCA), steel profiles, fire codes, SIA loads, room dimensions, spans, assemblies. The labeled jars. |
| **L2 — Guides (Markdown)** | 33 curated guides: materials, construction systems, typologies, norms, parametric design. The technique books. |
| **L3 — Scripts** | Parametric enforcement in code. The tested recipes. |
| **L4 — RAG (35K+ chunks)** | Dicobat, 21 SIA norms, Designing Buildings Wiki, Alexander patterns, Bloomsbury. The full reference library. Searchable. |

### RAG vs CAG — Pantry trips vs mise en place

**RAG** = going to the pantry mid-service. A ticket comes in, you don't know the answer, you walk to the pantry, search the shelves, grab what looks right, walk back, cook. Works, but there's a trip. You might grab the wrong jar.

**CAG** = mise en place. Before service, you read tonight's menu, pull everything you'll need, prep it, line it up at your station. When the ticket comes in, everything is at arm's reach. Faster, more reliable — but limited by counter space.

The system uses both. Mise en place for known tasks (load the playbook, the relevant guides, the learnings before the agent starts). Pantry open for surprises (search archibase if you hit something unexpected mid-build).

> *Animation note: show the pantry as a room adjacent to the kitchen. RAG = character walking to the pantry, scanning shelves, carrying jars back. CAG = character prepping ingredients on the counter before service starts. Both useful, different situations.*

---

## 6. The Booklet: Why the Kitchen Writes Its Own Story

Git means the process documents itself. Every commit is a dated entry. Every branch is an explored alternative. Every dead end is filed, not forgotten. Every merge is a decision made.

At the end, we open the logbook and the story of how we built everything is already there. We don't have to remember. We don't have to carry the mental load of cataloguing every decision. The kitchen keeps its own records, and the process booklet writes itself from the history.

This is what we wanted from the beginning. Not just a project — a documented process. Not just architecture — the story of how the architecture was made. The building and the residue.

> *Animation note: final shot — the logbook on the counter, pages filled with entries. Flip through and see the whole journey. The kitchen in the background, running, alive.*

---

## Quick Reference Map

For anyone who needs the one-page version:

| Repo / system element | Kitchen equivalent |
|---|---|
| city101 repo | The kitchen |
| CLAUDE.md | Map on the wall |
| .claude/rules/ | Tool manuals + safety code |
| .claude/ (config, MCP) | Wiring and plumbing |
| User (Andrea/Henna) | Chef de cuisine |
| Claude (main session) | Sous chef (with backpack) |
| Agent teams | Chefs de partie (station chiefs) |
| Subagents | Commis (prep cooks) |
| Context window | The backpack |
| Specialist roles | Station knowledge (enters backpack) |
| Archibase | The pantry |
| RAG | Pantry trip mid-service |
| CAG / playbook | Mise en place |
| datasets/ | Walk-in fridge (quality-checked) |
| output/ | Prep counter |
| source/ | Delivery crates (frozen, untouched) |
| LOCKBOARD.md | Ticket rail |
| CONTEXT files | Shift handover notes |
| LEARNINGS.md | Kitchen bible |
| workflows/ | Standard operating procedures |
| tools/ | Kitchen equipment |
| deliverables/ | The pass (plated, ready to serve) |
| observations/ | Tasting notes + R&D journal |
| design_system/SPEC.md | Plating guide |
| Git | The logbook |
| GitHub | The shared kitchen |
| MCP | The cable |
| MCP plugin | The socket |
| Router (multi-port) | The multiprise |
| Git branches | Design alternatives |
| Pull requests | "Pull this dish into the menu" |
| Commits | Dated logbook entries |

---

## What's NOT in this presentation

The essay version covers networking, packets, APIs, API keys, ports, localhost, Python environments, headless Rhino, Zoo/Cloud licensing. All valid and well-explained, but out of scope for the midterm. Kept in the source files for future use (paper, extended animation, technical appendix).

---

## Source files

- `the_kitchen_analogy.md` — the original narrative essay (prose, includes networking/API sections)
- `2026-03-24_kitchen-analogy.md` — the table mapping version (Lumen, includes RAG vs CAG)
- `kitchen_analogy_QA_transcript.md` — Q&A transcript about headless Rhino, APIs, MCP, licensing
- `2026-03-25_brain-dump.md` — animation ideas, presentation notes, rehearsal agenda

*Consolidated by Cairn Code — March 25, 2026*
*From conversations with Andrea about the presentation narrative.*
