# Ralph Loop — City101 Setup Guide

**For Andrea — paste into Claude Code sessions as needed**

---

## Step 0: Install the plugin (one time)

```bash
# In Claude Code, run:
/plugin marketplace add claude-plugins-official
/plugin install ralph-loop
```

Verify it's working:
```bash
/help ralph-loop
```

You now have two new commands: `/ralph-loop` and `/cancel-ralph`.

---

## Step 1: Understand the safety fit

Ralph works for **mechanical, verifiable tasks** in your project:
- Data pipeline scripts (fetch → filter → enrich → export)
- Batch API calls with rate limiting
- Coordinate conversions (WGS84 → LV95) across datasets
- CSV cleaning, deduplication, schema normalization
- HTML visualization builds with test criteria
- Script debugging loops (run → fail → fix → repeat)

Ralph does NOT work for:
- Narrative/thesis writing (judgment calls, no programmatic verification)
- QGIS styling decisions (aesthetic, not testable)
- Design decisions (what to map, how to frame arguments)
- Anything touching Henna's work (coordination ≠ automation)

---

## Step 2: The injection prompt

**Paste this at the start of any Claude Code session where you plan to use Ralph.**
It gives the agent all the project context it needs to work autonomously.

---

### CITY101 RALPH CONTEXT (paste into Claude Code)

```
You are working in the City101 repository — an EPFL BA6 Architecture studio project analyzing the Geneva–Villeneuve corridor (101km). This repo is shared between two humans (Andrea and Henna) and multiple Claude instances.

BEFORE DOING ANYTHING, read these files in order:
1. CLAUDE.md (project state + router — tells you what's active)
2. LOCKBOARD.md (who's working on what — do NOT touch tasks claimed by others)
3. datasets/inventory.md (what data exists)

CONVENTIONS YOU MUST FOLLOW:
- Coordinates: LV95 / EPSG:2056 is the working CRS. WGS84 inputs must be converted.
- Commit prefixes: [DATA] [FIND] [DEAD] [MAP] [VIZ] [BUILD] [SYNC]
- 49 canonical stations along the corridor are FROZEN — do not rename or reorder them.
- NEVER modify files in datasets/raw/ — those are source-of-truth originals.
- ALL new data goes to datasets/processed/
- ALL new scripts go to scripts/data/ or scripts/viz/
- Update datasets/inventory.md when creating new datasets.
- Rate limit all API calls: minimum 0.25s between requests.
- Write monolithic scripts: fetch → filter → process → match → write → print summary. No interactive exploration.

WHEN YOU FINISH A TASK:
1. Commit with the appropriate prefix: git add -A && git commit -m "[DATA] description"
2. Update datasets/inventory.md if you created/modified datasets
3. If you hit a dead end, write it to dead_ends/ with rationale

WHEN YOU ARE STUCK:
- Check dead_ends/ — this may have been tried before
- After 10 iterations without progress: document what's blocking in dead_ends/, list what was attempted, suggest alternative approaches, then output <promise>BLOCKED</promise>

DATA SOURCES YOU HAVE ACCESS TO:
- transport.opendata.ch (stationboard API — query from 20:00, limit=200 for last-train; rate limit 0.35s)
- data.sbb.ch (SBB Passagierfrequenz — semicolon-delimited CSVs)
- data.geo.admin.ch (federal geodata, DIEMO — often gzip-compressed)
- api.openchargemap.io (EV charging — free, no key needed for basic queries)
- sharedmobility.ch API

PYTHON ENVIRONMENT:
- pyproj for coordinate conversion (WGS84 ↔ LV95)
- pandas for CSV operations
- requests for API calls
- json, csv, gzip for data handling
- If a package isn't installed, install it with: pip install [package] --break-system-packages
```

---

## Step 3: Ready-to-use Ralph invocations

Copy-paste these directly. Replace the `[bracketed parts]` with your specifics.

### A. Data enrichment pipeline

```
/ralph-loop "Read CLAUDE.md first. Then: Process the CSV at datasets/processed/[FILENAME].csv. For each row, call [API_ENDPOINT] to fetch [WHAT_YOU_NEED]. Add the results as new columns. Write output to datasets/processed/[FILENAME]_enriched.csv. Update datasets/inventory.md. Print a summary: rows processed, rows failed, null counts per new column. Commit with prefix [DATA]. Output <promise>COMPLETE</promise> when the enriched CSV is written and inventory updated." --max-iterations 15 --completion-promise "COMPLETE"
```

### B. Coordinate conversion batch

```
/ralph-loop "Read CLAUDE.md first. Find all CSVs in datasets/processed/ that have WGS84 coordinates (columns containing 'lat' and 'lon' or 'latitude' and 'longitude') but no LV95 columns (E_LV95, N_LV95). For each such file, add E_LV95 and N_LV95 columns using pyproj (EPSG:4326 → EPSG:2056). Write to a new file with suffix _lv95.csv. Update datasets/inventory.md. Print summary of files converted. Commit with [DATA]. Output <promise>COMPLETE</promise> when all conversions are done." --max-iterations 10 --completion-promise "COMPLETE"
```

### C. Transport API data fetch

```
/ralph-loop "Read CLAUDE.md first. Read the 49 canonical stations from datasets/processed/[STATION_FILE].csv. For each station, query transport.opendata.ch/v1/stationboard?station=[NAME]&limit=200&datetime=[TARGET_TIME]. Rate limit: 0.35s between calls. Write a single monolithic script to scripts/data/fetch_[PURPOSE].py that does the full pipeline. Save results to datasets/processed/[OUTPUT_NAME].csv. Update inventory.md. Print summary: stations queried, successful, failed, total departures collected. Commit with [DATA]. Output <promise>COMPLETE</promise> when done." --max-iterations 20 --completion-promise "COMPLETE"
```

### D. HTML visualization build

```
/ralph-loop "Read CLAUDE.md and design_system/ first. Build an interactive HTML visualization at output/viz/[NAME].html. Requirements: [DESCRIBE WHAT THE VIZ SHOULD SHOW]. Use Leaflet.js for maps, D3.js for charts. Data source: datasets/processed/[FILE].csv. The viz must: (1) load without errors in a browser, (2) display all data points, (3) have a title and legend, (4) use the project color palette from design_system/ if it exists. Test by checking the file is valid HTML and all referenced data files exist. Commit with [VIZ]. Output <promise>COMPLETE</promise> when the HTML file renders correctly." --max-iterations 20 --completion-promise "COMPLETE"
```

### E. Dead-end audit / cleanup

```
/ralph-loop "Read CLAUDE.md, then scan the entire repo. Check: (1) Are there CSVs in datasets/processed/ not listed in inventory.md? Add them. (2) Are there scripts in scripts/ that reference files that don't exist? Flag them. (3) Are there empty directories? List them. (4) Is CLAUDE.md over 100 lines? If so, archive older decisions to findings/ and trim. Write a report to session_logs/audit_[DATE].md. Commit with [SYNC]. Output <promise>COMPLETE</promise> when audit is done." --max-iterations 10 --completion-promise "COMPLETE"
```

---

## Step 4: Safety notes

**ALWAYS use `--max-iterations`.** Without it, Ralph runs forever and burns through your API quota. Start with 10-15 for data tasks, 20 for complex builds.

**Watch the first 2-3 iterations.** Huntley's rule: sit ON the loop, not IN it. If Ralph is going in the wrong direction early, `/cancel-ralph` and retune the prompt. Don't let it burn 15 iterations on a bad trajectory.

**Ralph + LOCKBOARD.md**: Before starting a Ralph loop, update LOCKBOARD.md to claim the task. If Henna pulls and sees the lockboard, she'll know not to touch those files.

**Ralph + git**: Ralph commits as it goes. If things go wrong: `git log --oneline -10` to see what happened, `git reset --hard HEAD~N` to revert N commits.

**Ralph + the filesystem safety rules**: Ralph running with `--dangerously-skip-permissions` has FULL access to your machine. Since your repo is in a known directory and the prompts above scope all writes to the repo, the blast radius is contained. But if you modify the prompts to touch anything outside the repo, be very careful.

---

## Step 5: The Huntley philosophy (for your process booklet)

Worth documenting: Ralph is philosophically aligned with your project's approach.

- **Git as memory, not context windows** = your handoff system
- **Fresh context per iteration** = your monolithic script pattern  
- **Prompt tuning through observed failure** = your correction-round workflow with Claude
- **The operator's skill matters more than the model** = your architecture-first approach
- **Deterministically bad in an undeterministic world** = embrace iteration, not perfection

The difference: you discovered these patterns independently through architectural thinking. Huntley discovered them through software engineering. Same destination, different paths. That's Section 4 material for the research paper.
