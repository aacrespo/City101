# QA Log — Research Extension Outputs

**Reviewer:** QA Agent (Cairn Code)
**Date:** 2026-03-05
**Files reviewed:** 4
**Cross-reference sources:** CLAUDE.md, CONTEXT.md, LEARNINGS.md, handoffs/ (20 files), scripts/ (8 files)

---

## Summary

**Overall assessment:** All four files are substantially complete and high quality. No critical factual errors found against the City101 project files. Two critical structural issues (case_collection ICD Stuttgart duplication, booklet word count overshoot). Several minor issues and notes below.

| Severity | Count |
|----------|-------|
| Critical | 2 |
| Minor | 7 |
| Note | 6 |

---

## File 1: case_collection.md

### Case count
**20 cases.** Requirement: 15-20. **PASS.**

### Field completeness (8 required fields per case)

All 20 cases checked for: Firm/Lab, Project/tool, Year, Pattern, Tools, Scale, Key insight, Source URL.

| Field | Present in all 20? |
|-------|-------------------|
| Firm/Lab | Yes |
| Project/tool | Yes |
| Year | Yes |
| Pattern | Yes |
| Tools | Yes |
| Scale | Yes |
| Key insight | Yes |
| Source URL | Yes (all have 2-4 URLs) |

**PASS — all 8 fields present in all 20 cases.**

### Summary table at top
Present (lines 10-34). Contains #, Firm/Lab, Project or Tool, Year, Pattern, Scale, Tools. **PASS.**

Note: Summary table has 7 columns, not 8. Missing "Key insight" column. This is acceptable for a summary table (key insight is too long for a table cell), but worth noting.

### Duplicate check against 9 excluded cases

Excluded cases per brief:
1. Heatherwick Ge-Code — not in collection. OK.
2. ZHA + Omniverse — not in collection. OK.
3. Arup King's Cross R8 — not in collection. OK.
4. IAAC HyperBuilding — not in collection. OK.
5. ICD Stuttgart — **PRESENT as Case #17 (ICD Stuttgart IntCDC, ITECH Pavilion 2024).** SEE ISSUE BELOW.
6. Gramazio Kohler — not in collection as a standalone case. Referenced in section4_expanded.md re: COMPAS but not as a case entry. OK.
7. Vectorworks Text2BIM — not in collection. OK.
8. Autodesk Forma — not in collection as standalone. Referenced in Case #11 (Archistar integration) but Archistar is a distinct case. OK.
9. QGIS GIS Copilot — not in collection. OK.

**CRITICAL — Case #17 duplicates "ICD Stuttgart" from the excluded list.** The exclusion says "ICD Stuttgart (pavilions pre-2024)" and Case #17 is "ITECH Pavilion 2024" — the agent appears to have interpreted the exclusion as covering only pre-2024 pavilions and included the 2024 pavilion as distinct. This is a judgment call, but the exclusion names "ICD Stuttgart" without qualification, and the parenthetical "(pavilions pre-2024)" could be read as a description of what was already covered, not a limitation on the exclusion scope. **Recommend: either remove Case #17 (dropping to 19 cases, still within range) or get explicit confirmation that the 2024 pavilion is considered distinct from the existing ICD Stuttgart case.**

### Pattern distribution
- DAG: 10 cases (listed as 10 in summary, but summary table lists "Autodesk Neural CAD (partially)" which should be counted under Supervisor per the detailed entry #18 which classifies it as Supervisor)
- Supervisor: 5 cases
- Blackboard: 5 cases (summary lists 6: CORE.AI, Spot+F+P, Woods Bagot, CITA, ICD Stuttgart, Perkins and Will — that is 6, not 5)

**Minor — Pattern distribution summary table says Blackboard count is 5 but lists 6 cases.** The text on line 464 reads "5" but enumerates six entries. Correct to 6.

### Source quality
All 20 cases cite 2-4 URLs each. Sources include firm websites, industry press (Dezeen, AEC Magazine, ArchDaily, TechCrunch), conference proceedings, and research portals. No obviously broken or fabricated URLs detected (though live verification was not performed). Morphosis (Case #20) has the weakest sourcing — one generic "top firms" listicle and one tangentially related IE University page.

**Minor — Case #20 (Morphosis) sourcing is thin.** Two sources, neither directly from Morphosis. Recommend finding a primary Morphosis source (firm website, Tom Mayne lecture, or published paper).

### Other observations

**Note — Case #19 (Sidewalk Labs Delve) says "disabled May 2026."** This is a future date relative to the paper's context. Verify whether this has actually happened or is projected.

---

## File 2: section4_expanded.md

### Structure check (must match 4.1-4.6)

| Subsection | Present | Topic |
|-----------|---------|-------|
| 4.1 | Yes | Spatial Reasoning as First-Class Capability |
| 4.2 | Yes | Blackboard Architecture Suits Design Better Than Supervisor |
| 4.3 | Yes | The Multidimensional Model as Coordination Medium |
| 4.4 | Yes | Temporal and Experiential Dimensions |
| 4.5 | Yes | The Design-Certainty Gradient |
| 4.6 | Yes | Narrative as Integration Layer |

**PASS — all 6 subsections present.**

Summary table at end synthesizes all 5 capabilities. Wait — 6 subsections but 5 rows in the summary table. 4.2 (Blackboard) and 4.3 (Multidimensional Model) are merged into one row ("Blackboard coordination") and one row ("Multidimensional model"). That is actually 5 rows for 6 subsections, which is fine — 4.2 and 4.3 are closely related.

### Citation quality

Each subsection cites specific tools, projects, or publications:

- **4.1:** COMPAS (compas.dev), Huang et al. 2018 (Construction Robotics), compas_fab_choreo workshop (GitHub), ICD ABM research area, Leder and Menges 2025, ICD "Agent-based modeling and simulation in architecture" 2022, Rhino.Compute (GitHub), ShapeDiver. **Well-cited.**
- **4.2:** NVIDIA Omniverse/OpenUSD (openusd.org), Foster + Partners 2021 deployment, Bentley iTwin (developer.bentley.com), Bentley AI agents (AEC Magazine 2025, engineering.com 2025). **Well-cited.**
- **4.3:** nD BIM framework (described but no specific citation for the nD concept), Autodesk Tandem (intandem.autodesk.com, AEC Magazine 2025), Autodesk Forma (autodesk.com/products/forma). **Adequate.** The nD BIM framework could use a citation.
- **4.4:** Gehl and Svarre 2013 (How to Study Public Life), PLDP (github.com/gehl-institute/pldp), Lerman et al. 2014 (Geographical Analysis), Raford and Ragland 2017 (CEUS), He Kanxuan 2024 (ResearchGate), Sorscher et al. 2024 (eLife, arxiv). **Well-cited.** Space Syntax movement observation cites spacesyntax.online.
- **4.5:** ISO 19650-1:2018, PAS 1192-2, rvtparametrix.co.uk, thenbs.com, Speckle (speckle.guide, docs.speckle.systems), Autodesk Forma. **Well-cited.**
- **4.6:** Kunz and Rittel 1970 (Working Paper 131), Conklin and Begeman 1988 (gIBIS, CSCW '88), McCall 1983 (PHIBIS), Compendium (compendium.open.ac.uk), Ito et al. AAAI-20, ADRs (adr.github.io), MADR, AWS prescriptive guidance. **Well-cited.**

### Unsupported or weakly supported claims

1. **Minor — "Software teams mostly use the supervisor pattern" (4.2, line 41).** This is an assertion about industry practice without citation. It may be broadly true but is not sourced. Recommend adding a reference or softening to "Software teams frequently use..."

2. **Minor — "40-70% time reduction" for documentation (4.5 area, but actually in case_collection Case #7 SWAPP).** Not in this file, disregard.

3. **Note — nD BIM framework (4.3, line 75):** "The nD BIM framework assigns each dimension a natural agent specialization (3D geometry, 4D scheduling, 5D cost, 6D sustainability, 7D operations)." The nD concept is well-established in BIM literature but no citation is provided here. Recommend citing Lee et al. (2005) "nD modelling road map" or Eastman et al. BIM Handbook.

4. **Note — "No single queryable artifact in a software project that embeds codebase, deployment topology, performance, cost, and user experience" (4.2, line 61).** This is a strong claim. One could argue that observability platforms (Datadog, Grafana) or platform engineering dashboards approach this. The claim is defensible but could be challenged. Consider qualifying.

### City101 references in this file
- "Nyon-Gland gap is 19.3km" (4.1) — **Verified against CLAUDE.md and CONTEXT.md.** Correct.
- "correlation coefficients between 0.63 and 0.71" (4.2) — **Verified against CONTEXT.md** (r = 0.63-0.71). Correct.
- "City101's LOI/LOG/LOD framework" (4.5) — **Verified.** CLAUDE.md Working Principles section confirms LOI/LOG/LOD. Correct.
- "City101's CONTEXT.md ... LEARNINGS.md ... handoff files" (4.6) — **Verified.** All exist. Correct.
- "42-fold frequency variation (Lausanne at 28.5 trains/hr, St-Saphorin at 0.0)" (4.4) — **Verified against CONTEXT.md** ("42x frequency variation: Lausanne 28.5 tr/hr → St-Saphorin 0.0"). Correct.
- "160,000 ghost citizens" (4.6) — **Verified against CONTEXT.md** ("160,000 frontaliers"). Correct.

**All City101 claims in section4 verified. PASS.**

---

## File 3: AGENTS_template.md

### Section completeness (8 required sections)

| # | Required section | Present | Line |
|---|-----------------|---------|------|
| 1 | Team roster | Yes | 21 |
| 2 | Data contracts | Yes | 86 |
| 3 | File governance | Yes | 160 |
| 4 | Living state files | Yes | 267 |
| 5 | Handoff protocol | Yes | 347 |
| 6 | Safety rules | Yes | 426 |
| 7 | Design-specific governance | Yes | 473 |
| 8 | Naming conventions | Yes | 558 |

**PASS — all 8 sections present.**

### Bracket placeholder check

Searched for `[` patterns. Found extensive use of `[bracketed placeholders]` throughout:
- `[Lead Designer]`, `[Domain Expert / Teammate]`, `[Current task]`, `[Software stack: Rhino, QGIS, etc.]`
- `[Name 1]` through `[Name 4]`
- `[project_prefix]`, `[project_root]`, `[staging-path]`
- `[EPSG code, e.g., EPSG:2056 Swiss LV95]`
- `[min_lat]`, `[max_lat]`, `[min_lon]`, `[max_lon]`
- `[entity_name]`, `[entity_id]`, `[join_key]`
- `[CAD/BIM project file]`
- `[API 1]`, `[API 2]`, `[API 3]`
- `[Manual versioning / Git LFS / Speckle branches / other]`
- Many more throughout Sections 7-8

**PASS — extensive bracket placeholders for project-specific values.**

### Usability (forkable in 15 min)

Positive indicators:
- HTML comments with PURPOSE explanations for each section
- Quick Start Checklist at end (line 637) with 10 concrete setup steps
- Adaptation Notes section (line 652) explaining what to scale down for simpler projects
- Verification script template with actual Python code (lines 241-263)
- Concrete examples throughout (file naming, layer naming, branch naming)
- Promotion workflow diagram (lines 219-226)

**Minor — The "15 minutes" claim in the brief is tight.** The template has 8 sections and ~660 lines. A first-time user would need 30+ minutes. The template itself says "Estimated setup time: 15-30 minutes" (line 13), which is more realistic. The 30-minute upper bound is honest.

**Note — Section 7 (Design-Specific Governance) is the strongest differentiator** from generic software templates. The LOI/LOG/LOD framework, phase-dependent permissions, geometric modification rules, and clash detection checklist are genuinely architectural. This section alone justifies the template's existence beyond a generic AGENTS.md.

**PASS — practically usable.**

### Missing elements

**Note — No explicit "how to delete this template's scaffolding" instruction.** The HTML comments say "Delete the HTML comments once you understand each section" but some users may want a clean version without comments. Consider providing a "clean" variant or a script that strips comments.

---

## File 4: booklet_chapter.md

### Word count
**2,683 words.** Requirement: ~2,000-2,500. **CRITICAL — overshoots by ~180 words (7% over upper bound).** This is a soft target ("~2,000-2,500") so whether this is truly critical depends on strictness. At 2,683 it is close enough to edit down but should be flagged. The "What I would do differently" section (6 subsections, ~500 words) is the most obvious candidate for trimming.

### First-person voice
Checked throughout. The entire document uses first-person ("I knew," "I started," "I would," "my teammate Henna and I"). No lapses into third person or academic passive detected.

**PASS — first-person throughout.**

### Figure placeholders

| # | Location | Placeholder text |
|---|----------|-----------------|
| 1 | After line 17 | `[FIGURE: The QGIS project with 60+ layers...]` |
| 2 | After line 33 | `[FIGURE: A before/after showing the API limit discovery...]` |
| 3 | After line 47 | `[FIGURE: Screenshot of CONTEXT.md showing its evolution...]` |
| 4 | After line 53 | `[FIGURE: A handoff document (HANDOFF_01-03_S9.md)...]` |
| 5 | After line 69 | `[FIGURE: The temporal WCI heatmap...]` |
| 6 | After line 75 | `[FIGURE: The 49-station canonical list...]` |

**6 figure placeholders. PASS.**

### Honest limitations section
Present as "What I would do differently" (lines 79-93). Contains 6 concrete self-criticisms:
1. Should have started canonical list on day one
2. Should have used version control from the start
3. Should have written fewer, better scripts earlier
4. Should have separated analysis from presentation sooner
5. Should have documented dead ends more systematically
6. Should have trusted cross-referencing earlier

**PASS — honest and specific, not performative.**

### Voice and tone
The writing is confident without being boastful. The "drowning phase" section is genuinely self-critical. The "what the machine revealed" section presents findings without overclaiming. The closing paragraph ("the machine did not replace judgment") is well-calibrated.

**Note — The sentence "Four Claude accounts sounds excessive for a student project" (line 51) is effective and should stay.**

---

## Cross-reference Verification

### Handoff count
- booklet_chapter.md claims: "twenty handoff documents" (line 15)
- Actual count in `/handoffs/`: **20 files**
- **PASS — exact match.**

### Script count
- booklet_chapter.md claims: "eight Python scripts" (line 15)
- Actual count in `/scripts/`: **8 files**
- **PASS — exact match.**

### QGIS layer count
- booklet_chapter.md claims: "sixty-layer QGIS project" (line 105)
- CLAUDE.md says: "~60 layers" (QGIS section)
- CONTEXT.md says: "52 layers" (folder structure) but also elsewhere describes ~60
- **Minor — CONTEXT.md folder structure says 52, CLAUDE.md says ~60, booklet says 60.** The discrepancy between 52 and 60 may reflect layers added after CONTEXT.md was last updated (2026-03-02). Not a factual error but an inconsistency across project files.

### Session count
- booklet_chapter.md claims: "eleven sessions" (line 15)
- Handoff files: S1 through S11 on the 01-03 date, plus S8.0-S8.3 (Lumen sub-sessions), plus sessions on other dates (02-03, 04-03). The "eleven" likely refers to the Cairn sessions S1-S11 on the primary date.
- **PASS — reasonable count.** The exact number depends on whether Lumen sub-sessions and later-date sessions are counted. "Eleven" is defensible as the primary sequence.

### Claude account count
- booklet_chapter.md claims: "four Claude accounts" (line 15)
- CLAUDE.md Team System lists: Cairn, Cairn Code, Lumen, Meridian, Cadence = 5 accounts total, but Cadence is "not yet used for studio"
- CONTEXT.md lists: Cairn, Lumen (Andrea's), Meridian, Cadence (Henna's)
- The booklet says "four" which matches Cairn + Cairn Code + Lumen + (Meridian or one other). Since the booklet is Andrea's first-person account, "four" likely means: Cairn (desktop), Cairn Code (CLI), Lumen (browser), and possibly Meridian (Henna's). CLAUDE.md lists 5 named accounts but one (Cadence) was unused.
- **PASS — "four" is reasonable for the actively used accounts.**

### Specific numbers verified against CONTEXT.md / CLAUDE.md

| Claim in booklet | Source | Match? |
|-----------------|--------|--------|
| 49 train stations | CLAUDE.md: "49 stations" throughout | Yes |
| 7 time slots | CLAUDE.md: "7 time slots" | Yes |
| 5 dimensions of continuity | CONTEXT.md: "Five dimensions of breakage" | Yes |
| 11 of 49 stations maintain working continuity | CONTEXT.md: "11/49 stations continuous" | Yes |
| Nyon to Gland 19.3km | CLAUDE.md: confirmed | Yes |
| Gland to Morges 20km | CLAUDE.md: confirmed | Yes |
| Lavaux Fracture 17.5km | CLAUDE.md: confirmed | Yes |
| 14 stations workable at peak, 13 at 11pm | CONTEXT.md: "14/49 at peak, 13/49 at 11pm" | Yes |
| Correlation coefficients 0.63 and 0.71 | CONTEXT.md: "r = 0.63-0.71" | Yes |
| Shannon diversity phase transition at ~1.0 | CONTEXT.md: "Shannon 1.0 threshold" | Yes |
| Below 1.0: avg richness 8.8, above: 70.5 | CONTEXT.md: "Below it, avg richness 8.8. Above it, 70.5" | Yes |
| 160,000 frontaliers | CONTEXT.md: "160,000 frontaliers" | Yes |
| 33 datasets in cross-reference | CLAUDE.md: "33 datasets" | Yes |
| 2,093 spatially joined points | CLAUDE.md: "2,093 points from 33 datasets" | Yes |
| 42-fold frequency variation | CONTEXT.md: "42x frequency variation" | Yes |
| Lausanne 28.5 trains/hr | CONTEXT.md: confirmed | Yes |
| Transport API limit=30 issue | LEARNINGS.md: "limit=30 made every station look identical" | Yes |
| CHF 26 Geneva-Lausanne | CONTEXT.md: "CHF 26 Geneva→Lausanne full price" | Yes |
| CHF 10.50/day GA amortized | CONTEXT.md: "CHF 10.50/day" | Yes |
| 85% of connections not workable | CONTEXT.md: "85% of connections not workable" | Yes |
| 343 API calls for temporal analysis | 49 stations x 7 time slots = 343. Arithmetic checks. | Yes |

**All 22 cross-referenced claims verified. PASS.**

### booklet_chapter.md claims about CONTEXT.md and LEARNINGS.md

- "CONTEXT.md tracks the state of sixteen datasets across six categories" — CONTEXT.md dataset tables show: corridor analysis (~15 datasets), EV charging (3), remote work (7), transit (4), stations (2) = 5 categories with ~31 datasets listed. The "sixteen" and "six" don't match current CONTEXT.md exactly. However, CONTEXT.md was last updated 2026-03-02, and the numbers may have been accurate at an earlier session.

**Minor — "sixteen datasets across six categories" is imprecise relative to current CONTEXT.md counts.** The actual counts are higher. This may reflect the state at the time of writing vs. the current state. Recommend updating to match current CONTEXT.md or using approximate language ("dozens of datasets across six categories").

- "LEARNINGS.md holds twenty-five entries" — Counting entries in LEARNINGS.md: I count approximately 22-25 entries depending on how sub-entries are counted. **PASS — approximately correct.**

---

## Issue Registry

### Critical

| # | File | Issue | Recommendation |
|---|------|-------|---------------|
| C1 | case_collection.md | Case #17 (ICD Stuttgart ITECH 2024) may duplicate excluded case "ICD Stuttgart" | Remove Case #17 or confirm the 2024 pavilion is considered distinct from the excluded "ICD Stuttgart" entry |
| C2 | booklet_chapter.md | Word count 2,683 — exceeds ~2,500 target by ~180 words | Trim "What I would do differently" section (currently ~500 words) by 1-2 items to bring total under 2,500 |

### Minor

| # | File | Issue | Recommendation |
|---|------|-------|---------------|
| M1 | case_collection.md | Blackboard pattern summary says count=5 but lists 6 cases | Change count to 6 |
| M2 | case_collection.md | Case #20 (Morphosis) has weak sourcing — no primary Morphosis source | Find direct Morphosis firm page or Tom Mayne lecture/paper |
| M3 | section4_expanded.md | "Software teams mostly use the supervisor pattern" — unsupported assertion | Add citation or soften language |
| M4 | section4_expanded.md | nD BIM framework referenced without citation | Add Lee et al. 2005 or Eastman et al. |
| M5 | AGENTS_template.md | "15 minutes" setup claim in brief is tight; template itself says 15-30 min | Acceptable as-is (template is honest), but brief should say 15-30 min |
| M6 | booklet_chapter.md | "sixteen datasets across six categories" doesn't match current CONTEXT.md | Update to approximate language or current counts |
| M7 | booklet_chapter.md | QGIS layer count discrepancy (52 in CONTEXT.md vs 60 in booklet) | Minor — use "60+" or "~60" consistently |

### Notes (suggestions, not issues)

| # | File | Note |
|---|------|------|
| N1 | case_collection.md | Summary table omits "Key insight" column — acceptable for space but worth noting |
| N2 | case_collection.md | Case #19 (Delve) "disabled May 2026" — verify if this is confirmed or projected |
| N3 | section4_expanded.md | Claim about no single queryable artifact in software (4.2) could be challenged — consider qualifying |
| N4 | AGENTS_template.md | Section 7 (Design-Specific Governance) is the template's strongest unique contribution — consider highlighting in any introduction |
| N5 | AGENTS_template.md | Consider providing a "clean" version stripped of HTML setup comments |
| N6 | booklet_chapter.md | "Four Claude accounts sounds excessive for a student project" — effective line, keep it |
