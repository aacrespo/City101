# The Machine That Taught Me What I Was Looking At

*A chapter on how a workflow became a design artifact*

---

## The question

The question was simple enough to write on an index card: does the 101km rail corridor from Geneva to Villeneuve function as one continuous city?

Studio Huang's brief asked us to read the territory through data — not to impose a thesis, but to let spatial patterns surface from evidence. My teammate Henna and I were each responsible for a lens. Mine was "flow of people": what makes them stop, where infrastructure creates behavior, and whether the connective tissue between Geneva and Villeneuve has the characteristics of a single urban organism or something else entirely.

I knew early that this would not be a question you answer by visiting six sites and sketching. Forty-nine train stations. Seven time slots across the day. Five dimensions of continuity (connectivity, workspace, temporal access, transit frequency, comfort). Dozens of datasets from classmates covering everything from religious buildings to acoustic ecology to grocery stores. The combinatorial space was too large for manual analysis and too multi-dimensional for a single QGIS session. I needed to process data at a scale that exceeded what I could do by hand, and I needed to do it fast — A02 was due in two weeks.

So I started using Claude as an analytical partner. Not for writing or rendering — for data operations. Fetching APIs, cross-referencing datasets, computing indices. What I did not expect was that the *way* I organized this work would become as instructive as the findings themselves. Over eleven sessions, four Claude accounts, twenty handoff documents, and eight Python scripts, a workflow infrastructure emerged that I only later recognized as a design artifact in its own right.

[FIGURE: The QGIS project with 60+ layers — the spatial accumulation of eleven sessions of data work]

---

## The drowning phase

The first few sessions were a mess.

I would start a conversation, ask Claude to help me explore an API response, spend forty minutes inspecting JSON structures, filtering interactively, adjusting queries — and then the conversation would hit its context limit before I had a single usable output. The exploration was interesting. It produced nothing durable.

The naming problem was worse. I had classmate data from seven people, each using their own conventions. Thomas Riegert's religious buildings called it "Lausanne." Marek Waeber's grocery stores called it "Gare de Lausanne." The transport API returned "Lausanne." When I tried to join these datasets spatially, nothing matched. Three representations of the same station, three different strings, zero usable joins.

I was also losing context between sessions. I would discover something important — say, that the transport API's `limit=30` parameter was silently capping every station at thirty departures per hour, making Lausanne look identical to a village that gets two trains a day — and then in the next session, I would not remember the fix. Or I would remember it but Claude would not, because it was a different conversation. Insights were being generated and immediately lost.

The pattern was: explore, discover, lose the discovery, re-discover, lose it again. I was drowning not in data but in the absence of infrastructure for handling data.

[FIGURE: A before/after showing the API limit discovery — the flat frequency distribution (every station at ~30 trains/hr) versus the real 42-fold variation that appeared once the limit was removed]

---

## Building the machine

The infrastructure did not arrive as a plan. It arrived as a series of frustrations that each demanded a specific fix. Taken together, the fixes constitute a system.

**The canonical list.** The naming problem forced the first piece of infrastructure: a single CSV with all forty-nine corridor stations, each with an exact canonical name, WGS84 and LV95 coordinates, and a unique ID. Every dataset, from every source, had to map to this list before it could enter the analysis pipeline. When a classmate's CSV called a station "Gare de Lausanne" or "Lausanne CFF," the mapping happened at ingestion, not downstream. This one file — forty-nine rows, maybe ten columns — made everything else possible. Without it, the thirty-three-dataset cross-reference that eventually produced 2,093 spatially joined points could never have existed.

**Monolithic scripts.** The context-window problem forced the second piece: instead of exploring data interactively, I started writing self-contained Python scripts that ran end-to-end and printed only a summary. Fetch the data, filter it, process it, match it to the canonical list, write the output CSV, print a comprehensive summary listing every dataset queried, row counts, anything unexpected, and download URLs for data not fetched. The script `fetch_transport_frequency.py` is a good example — 387 lines that query the transport API for all forty-nine stations, compute trains per hour, break down by service type, and produce a frequency profile in one run. No interaction, no exploration, no context-window death. The session stays clean. The leads stay documented.

**Living state files.** The cross-session memory problem forced the third piece. I created two files that lived in the project root: `CONTEXT.md` (what exists right now — every dataset, every finding, every open question) and `LEARNINGS.md` (things discovered across all sessions that should never be re-learned). Every new session started by reading these two files. They accumulated over eleven sessions into substantial documents — CONTEXT.md tracks the state of dozens of datasets across six categories, LEARNINGS.md holds twenty-five entries ranging from API quirks to theoretical frameworks. The handoff documents still existed for traceability, but the living files became the primary memory.

[FIGURE: Screenshot of CONTEXT.md showing its evolution — the dataset tables, the key numbers section, the critical gaps checklist with items being marked complete across sessions]

**Staged promotion.** By session four or five, I had multiple Claude accounts producing data in parallel — Cairn on the desktop running QGIS validation, Lumen on the browser doing diversity research, Cairn Code spawning scripts. The risk of bad data contaminating good data was real. So I established a rule: agents write to `output/` (a staging directory). Nothing moves to `datasets/` (the production directory) until it passes verification — coordinate range checks, null value scans, canonical name matching, and spatial validation against the QGIS basemap. A charging station that falls in the middle of Lake Geneva passes every schema check but is obviously wrong. The QGIS step catches what code cannot.

**Multi-account coordination.** Four Claude accounts sounds excessive for a student project. It was not planned — it emerged from platform constraints. Cairn on the desktop app had MCP access, meaning it could directly control QGIS and the filesystem. Cairn Code (the CLI) could run Python scripts and spawn parallel subagents. Lumen on the browser had project knowledge files but no tool access. Each platform enabled different work. The handoff system — twenty structured markdown documents — kept them synchronized. A handoff from Session 9 reads like a shift report: what was accomplished, what files were produced, what bugs were found and fixed, what to do next.

[FIGURE: A handoff document (HANDOFF_01-03_S9.md) showing the session-to-session continuity — files produced, bugs caught, findings documented, next steps specified]

I did not know, while building all of this, that I was reinventing patterns that software engineering had already named. The canonical list is a data contract. The monolithic scripts are the "unit of work" pattern. Staged promotion is code review. Living state files are configuration management. The multi-account system is a supervisor architecture. I found out later, when I started reading about how software teams coordinate AI agents, that everything I had built out of frustration had a formal name and a body of literature behind it.

That recognition — that the demands of rigorous spatial analysis had independently produced software engineering patterns — was the seed of the paper that sits alongside this chapter.

---

## What the machine revealed

The workflow was not the point. The corridor was the point. But the workflow made findings possible that I am certain I could not have reached through manual analysis alone.

**The archipelago.** The Working Continuity Index — a composite of connectivity, workspace availability, frequency, comfort, and temporal access — revealed that only eleven of forty-nine stations maintain full working continuity. The corridor is not a linear city. It is an archipelago: clusters of workable stations separated by structural gaps. Three gaps dominate: Nyon to Gland (19.3km), Gland to Morges (20km), and the Lavaux Fracture (17.5km through UNESCO-protected vineyards). This finding required computing the WCI for every station, which required having all five input dimensions already cleaned, canonically named, and joinable. Without the infrastructure, I would have had five separate maps that each told part of the story. With it, I had one index that told the whole story.

**The structural persistence.** The temporal analysis — forty-nine stations across seven time slots, 343 API calls — showed that the archipelago barely pulses. Fourteen stations are workable at morning peak. Thirteen are workable at eleven at night. The three gaps persist at every hour. This finding killed a hypothesis I had been carrying: that the corridor might "work" during rush hour and fragment only at off-peak times. It does not. The fragmentation is permanent. Architectural interventions at break points cannot rely on temporal variation — the deficit is always there.

[FIGURE: The temporal WCI heatmap showing the archipelago pattern — 49 stations on the y-axis, 7 time slots on the x-axis, color-coded by workability. The gaps are visible as persistent dark bands regardless of time.]

**The diversity convergence.** This one genuinely surprised me. Lumen (running on a parallel track while Cairn did temporal analysis) cross-referenced four independent diversity metrics: religious Shannon diversity (from Thomas Riegert's data), modal Shannon diversity (transport modes), cuisine Shannon diversity (from Mohamad Ali's restaurant data), and economic category diversity. They all converged on the same spatial pattern, with correlation coefficients between 0.63 and 0.71. There is a phase transition at Shannon diversity of approximately 1.0: below it, stations average 8.8 classmate data points within one kilometer; above it, they average 70.5 — an eightfold jump. Four independently collected datasets, from four different classmates studying four different topics, all drawing the same line on the map. That is not something you find by looking at one dataset at a time. It is something you find by joining everything to a canonical spatial key and letting the correlations surface.

**The 160,000 ghost citizens.** Combined frontalier data for Geneva and Vaud cantons shows approximately 160,000 cross-border workers entering the corridor daily — a population larger than Lausanne. They are present in the daytime economy, invisible in every diversity metric (they do not appear in residential census data), structurally excluded from the GA travelpass (the mechanism that makes the corridor function as one city for Swiss residents), and they vanish from the corridor at six in the evening. Henna's night-city analysis and my daytime-flow analysis were describing the same phenomenon from opposite ends: the corridor's population is time-dependent in a way that no static map captures.

[FIGURE: The 49-station canonical list — the data contract that made all cross-referencing possible, with station IDs, coordinates in both systems, and canonical names]

---

## What I would do differently

Honesty compels a list.

**I would start with the canonical list on day one.** It took until session seven to build the forty-nine-station cross-reference. Every session before that was partially wasted because datasets could not be joined. If I had established the canonical entity list in the first week, the entire analytical pipeline would have been two weeks faster.

**I would version-control from the start.** The project uses manual file versioning — `_v2`, `_v3` suffixes. This works until it does not. There were moments when I was unsure which version of a dataset was current, and the only way to check was to open the file and look at the metadata. Git would have solved this. I knew this. I still did not set it up. The activation energy of "initialize a repo and learn the workflow" always lost to the urgency of "produce the next dataset before the crit." This is a mistake I would not repeat.

**I would write fewer, better scripts earlier.** The eight scripts in the project represent the survivors. There were many more — quick hacks, one-off explorations, throwaway fetchers — that produced data of uncertain quality and then sat in the source directory confusing future sessions. The monolithic-script pattern works, but only if you commit to it from the beginning. Half-measures (interactive exploration that produces a CSV you then treat as canonical) create data provenance problems that are tedious to untangle.

**I would trust the cross-referencing earlier.** The diversity convergence finding — four independent metrics drawing the same spatial line — came from an exploratory cross-reference that I almost did not run. I had been focused on the five WCI dimensions and considered diversity a side investigation. The lesson is that the most valuable findings came from spatially joining datasets that were not designed to go together. The infrastructure exists precisely to enable these unexpected joins. I should have been running them from session three, not session eight.

---

## The workflow as artifact

Architecture studios produce drawings, models, and narratives. This studio also produced a workflow — a system of canonical lists, living state files, monolithic scripts, staged promotion gates, and multi-account coordination protocols that, taken together, constitute a design artifact as deliberate and purposeful as any map in the final submission.

The irony is that I did not design it. It designed itself, under pressure from the demands of the question. Software engineers would recognize this as "emergent architecture" — the patterns that arise when a team faces real coordination problems and solves them pragmatically rather than theoretically. The canonical list emerged because joins kept failing. The living state files emerged because sessions kept losing context. The staged promotion emerged because bad data kept contaminating good data. Each piece of infrastructure is a scar from a specific wound.

Whether this approach scales beyond a studio project is an open question. The patterns themselves — data contracts, staged verification, living state files — clearly do scale; software teams use them at enormous complexity. Whether architecture will adopt them systematically depends on whether the profession develops tools that make spatial data as manipulable as text. The QGIS MCP bridge, which let Claude directly validate coordinates against a live spatial model, is the closest thing I have seen to a genuinely architectural CI/CD pipeline. It is also a research prototype running on a student's laptop.

What I am confident about is the finding that emerged from both the workflow and the analysis: **the corridor is an archipelago, and the archipelago is structural.** That finding required processing forty-nine stations across seven time slots across five dimensions of continuity, cross-referenced with thirty-three classmate datasets, validated against a sixty-layer QGIS project. No amount of site visits would have revealed the temporal persistence of the gaps, or the diversity convergence, or the 160,000 ghost citizens. The machine did not replace judgment — I still had to decide what the findings *meant* for architecture. But the machine made the findings visible. And visibility, in a studio that asks us to read territory through data, is the whole game.
