# QA Log: "From Codebase to Corridor: Agentic AI Workflows for Architectural Design"

**Reviewed by:** Cairn Code (QA agent)
**Date:** 2026-03-05
**Document path:** `/Users/andreacrespo/CLAUDE/City101_ClaudeCode/research/agentic_workflows_for_architecture.md`

---

## Word Count

Estimated word count: ~5,400 words (335 lines of markdown, excluding blank lines and table formatting).

---

## Section-by-Section Status

### Introduction (lines 1-18)
**Status: PASS with notes**

- Claim: "4 Claude accounts" coordinated across "11 sessions." CLAUDE.md lists 5 accounts (Cairn, Cairn Code, Lumen, Meridian, Cadence). Paper lists 4 (Cairn, Cairn Code, Lumen, Meridian), omitting Cadence. Defensible because Cadence is documented as "Not yet used for studio," but should be acknowledged.
- Claim: "20+ datasets." CLAUDE.md Tier 1 table lists 16 dataset files in `datasets/`, plus 7 classmate groupings integrated into crossref. "20+" is a reasonable rounding.
- Claim: "2 human collaborators." Verified: Andrea and Henna per CLAUDE.md.

### Section 1: The Territory (lines 21-74)
**Status: PASS**

- Section 1.1-1.2: Conceptual framework, no verifiable claims against project files.
- Section 1.3: Two direct quotes verified:
  - "Prefer fewer, broader agents over many narrow ones..." -- VERIFIED in `.claude/commands/research-with-agent-team.md` lines 60-62. Exact match.
  - "If one agent writes 'Lausanne Gare'..." -- VERIFIED in `.claude/commands/research-with-agent-team.md` lines 97-99. Exact match.
- Section 1.4: External claims about Speckle, BIMcollab, AGENTS.md format. Not verifiable against project files. Treated as external references.

### Section 2: Six Patterns from City101 (lines 77-147)
**Status: FAIL -- contains critical factual errors**

**Pattern A table row:**
- Claim: "20 handoff files spanning S1-S11 plus Lumen sub-sessions S8.1-S8.3."
  - Actual file count: **20 files.** VERIFIED.
  - Breakdown: S1-S7, S8.0, S8.1, S8.2, S8.3, S9, S10, S11, plus HANDOFF_02-03_S1, HANDOFF_04-03_S1, HANDOFF_04-03_S2, TEAM_HANDOFF_01-03_S1, TEAM_HANDOFF_01-03_S2, and HANDOFF_LUMEN_STATION_REVIEWS. The session numbering includes more files beyond the S1-S11 + S8.x sub-sessions described. The count is correct but the characterization omits the post-March-1 handoffs and team handoffs.

**Pattern B table row:**
- Claim: "8 scripts in `scripts/` (compute_wci.py, fetch_ridership.py, journey_workability.py, etc.)"
  - Actual .py file count: **8 Python files.** VERIFIED.
  - Files: opendata_swiss_trawl.py, opendata_trawl_phase2_3.py, fetch_ridership.py, fetch_transport_frequency.py, fetch_transport_frequency_v2.py, compute_wci.py, journey_workability.py, export_maps_print.py.
  - **However:** CONTEXT.md (line 86) says "7 monolithic Python scripts." The paper's count of 8 matches the filesystem but contradicts CONTEXT.md. This is an internal project inconsistency, not a paper error -- the paper is more accurate than CONTEXT.md here.

**Pattern C table row:**
- Claim: "Move verified outputs from staging to production paths. Only the lead does this."
  - VERIFIED in `.claude/commands/research-with-agent-team.md` lines 347-348. Exact match.

**Pattern D table row:**
- Claim: "CONTEXT.md updated through 10+ sessions."
  - CONTEXT.md header says "post S9 + Lumen S8.1-S8.3." Counting S1-S9 plus sub-sessions: plausible. "10+" is reasonable.
- Claim about LEARNINGS.md API pitfalls quote ("The transport.opendata.ch stationboard with limit=30...").
  - VERIFIED in LEARNINGS.md lines 80-81. Exact match.

**Pattern F description (line 106):**
- Claim: Quote "Maximize LOI early, add LOG only as LOD increases."
  - Actual text in 00_Workflow_v04.md (line 70): "Maximize LOI early, add LOG only as LOD increases." **VERIFIED. Exact match.**
- Claim: Anti-pattern quote "High LOG + Low LOI + Low LOD: Pretty render, no data, design not locked. Dangerous -- looks done but isn't."
  - Actual text in 00_Workflow_v04.md (line 62): "High LOG + Low LOI + Low LOD | Pretty render, no data, design not locked | **Dangerous** -- looks done but isn't." **VERIFIED.** Paper reformats from table to prose but content is accurate.

**Pattern A expanded description (line 96):**
- Claim: "The insight from LEARNINGS.md: 'MCP access comes from the desktop app, not the account. Whichever account is on the desktop app can control spatial tools.'"
  - Actual LEARNINGS.md text (line 64): "MCP access (filesystem, QGIS, Rhino) comes from the desktop app, not the account."
  - The paper's quote is a **paraphrase, not an exact quote**. The original says "filesystem, QGIS, Rhino" where the paper omits those specifics. The second sentence ("Whichever account is on the desktop app can control spatial tools") is a loose paraphrase of "Whichever account is on the desktop app can read/write CONTEXT.md and control spatial tools." Minor but the use of quotation marks implies exact quote.

**QGIS MCP workflow section (lines 108-115):**
- Claim: "a live QGIS project containing 60 layers."
  - CLAUDE.md says "~60 layers." CONTEXT.md says "52 layers." The paper uses "60" which matches CLAUDE.md's approximation but not CONTEXT.md's specific count. **Minor inconsistency** -- CONTEXT.md is likely more current.

### Section 2: Other documented cases (lines 117-146)
**Status: PASS with notes**

- External claims about Heatherwick, ZHA, Vectorworks, IAAC, Arup, ICD Stuttgart, Autodesk Forma, QGIS GIS Copilot. These are not verifiable against project files. Spot-checked:
  - Vectorworks Text2BIM: Claims "ASCE Journal of Computing in Civil Engineering, Volume 40, Number 2, March 2026" and "91.1% validity across 692 test scenarios." Not verifiable here but the citation is specific enough to check externally.
  - Heatherwick "Ge-Code" team with "Dreamhopper" and "Climate Atlas": Specific names suggest real sourcing.
  - **Note:** The paper states the QGIS GIS Copilot paper is from 2025. The citation is plausible but unverifiable against project files.

### Section 3: Transferable Patterns (lines 150-201)
**Status: PASS with one critical error**

**Pattern mapping table (line 156-168):**
- Claim: "TODO_4_POINTS.md: 4 independent investigations (Break Points, Temporal, GA, Reviews), each with explicit inputs, outputs, and severity classification."
  - VERIFIED in TODO_4_POINTS.md. Four points: Break Point Map, Temporal Corridor, GA Hypothesis, Google Station Reviews. Severity classification is in Point 1.

- Claim: "Lumen's diversity research (S8.1-S8.3) as independent 'branch'."
  - VERIFIED. Handoff files S8.1, S8.2, S8.3 exist. CONTEXT.md attributes diversity findings to "Lumen S8.1-S8.3."

- **CRITICAL ERROR (line 166):** Claim: "CLAUDE.md as 800-line entry point."
  - **Actual CLAUDE.md line count: 382 lines.** This is off by more than 2x. The paper claims 800 lines; the file has 382. This is a clear factual error.

### Section 4: Where Architecture Can Go Beyond Software (lines 204-254)
**Status: PASS**

- Claims about City101 findings (archipelago pattern, diversity correlations, temporal WCI) are all consistent with CONTEXT.md and CLAUDE.md observations.
- Claim (line 219): "r = 0.63-0.71" for diversity correlations. VERIFIED in CONTEXT.md (lines 182-183) and CLAUDE.md.
- Claim (line 219): "The correlation between religious Shannon diversity, modal Shannon diversity, cuisine Shannon diversity, and economic category diversity." VERIFIED in CONTEXT.md line 256.
- Claim (line 233): "14 at peak, 13 at 11pm." VERIFIED in CONTEXT.md line 177 and CLAUDE.md.
- Claim (line 235): "Lausanne at 28.5 trains per hour, St-Saphorin at 0.0." VERIFIED in CONTEXT.md line 163.
- Claim (line 249): "160,000 ghost citizens." VERIFIED in CONTEXT.md line 185.

### Conclusion: Practical Recommendations (lines 257-288)
**Status: PASS**

- Recommendation 2: "The City101 research protocol is explicit: 'Prefer fewer, broader agents over many narrow ones.'" VERIFIED in research-with-agent-team.md.
- Recommendation 7: "City101's CLAUDE.md is 800 lines." **Same CRITICAL ERROR as above -- actual count is 382 lines.**
- Recommendation 9: "City101's CONTEXT.md tracks which account produced which dataset ('NEW S8 (Lumen)' vs 'NEW Cairn S9')." VERIFIED -- CONTEXT.md uses these exact tags (e.g., line 109: "NEW S8 (Lumen)", line 111: "NEW Cairn S9").

### References (lines 291-336)
**Status: PASS with notes**

- Claim: "20 session handoff files (S1-S11 + sub-sessions)." Actual count: 20 files. VERIFIED.
- Claim: "8 monolithic Python scripts." Actual count: 8 .py files. VERIFIED.
- The references list firm case studies, tools, and academic papers. Cannot verify external citations against project files, but citations are specific with publication details.

---

## Issues Summary

### Critical Issues (2)

| # | Location | Issue | Details |
|---|----------|-------|---------|
| C1 | Line 166 (Section 3 table) | **CLAUDE.md line count wrong** | Paper claims "800-line entry point." Actual: 382 lines. Off by 2.1x. |
| C2 | Line 275 (Conclusion) | **Same error repeated** | "City101's CLAUDE.md is 800 lines -- too long for most projects." Same incorrect figure. |

### Minor Issues (4)

| # | Location | Issue | Details |
|---|----------|-------|---------|
| M1 | Line 96 | **Paraphrase presented as direct quote** | MCP insight is in quotation marks but is a loose paraphrase of LEARNINGS.md line 64, not an exact quote. Either use the exact text or remove quotation marks. |
| M2 | Line 112 | **QGIS layer count inconsistency** | Paper says "60 layers." CLAUDE.md says "~60." CONTEXT.md (likely more current) says "52 layers." |
| M3 | Line 81 | **Account count: 4 vs 5** | Paper counts "four Claude accounts." CLAUDE.md lists 5 (Cairn, Cairn Code, Lumen, Meridian, Cadence). Omitting Cadence is defensible since it was never used, but a footnote would be cleaner. |
| M4 | Line 87 | **Handoff characterization incomplete** | "S1-S11 plus Lumen sub-sessions S8.1-S8.3" does not account for all 20 files. Actual files also include post-March-1 handoffs (HANDOFF_02-03_S1, HANDOFF_04-03_S1, HANDOFF_04-03_S2), team handoffs (TEAM_HANDOFF_01-03_S1, TEAM_HANDOFF_01-03_S2), and HANDOFF_LUMEN_STATION_REVIEWS. The total count of 20 is correct but the description of what those 20 files are is incomplete. |

### Notes (3)

| # | Location | Note |
|---|----------|------|
| N1 | Line 88 | CONTEXT.md says "7 monolithic Python scripts" but filesystem has 8 .py files. The paper's count of 8 is more accurate than CONTEXT.md. CONTEXT.md may have been written before export_maps_print.py was added. |
| N2 | Lines 117-146 | External case studies (Heatherwick, ZHA, Vectorworks, IAAC, Arup, ICD Stuttgart) cannot be verified against project files. Citations are specific but should be independently checked. |
| N3 | Throughout | Terminology is consistent throughout: "WCI," "Working Continuity Index," "archipelago," "break points," "LOI/LOG/LOD," "canonical entity list," "staged promotion" all used consistently and match project file terminology. |

---

## Source Verification Checklist

| Claim | Source cited | Verified against | Status |
|-------|-------------|-------------------|--------|
| 49 stations, 5 break dimensions | CLAUDE.md, TODO_4_POINTS.md | Both files | PASS |
| 20 handoff files | handoffs/ directory | Filesystem glob | PASS (count correct, description incomplete) |
| 8 scripts | scripts/ directory | Filesystem glob | PASS |
| "Maximize LOI early, add LOG only as LOD increases" | 00_Workflow_v04.md | Line 70 | PASS -- exact match |
| "Prefer fewer, broader agents" | research-with-agent-team.md | Lines 60-62 | PASS -- exact match |
| "Lausanne Gare" naming conflict example | research-with-agent-team.md | Lines 97-99 | PASS -- exact match |
| "Move verified outputs from staging to production" | research-with-agent-team.md | Lines 347-348 | PASS |
| "Nothing goes to datasets/ unverified" | CLAUDE.md | Line 358 | PASS |
| MCP desktop app insight | LEARNINGS.md | Line 64 | PASS (paraphrase, not exact) |
| limit=30 API pitfall | LEARNINGS.md | Line 80 | PASS -- exact match |
| Diversity correlations r = 0.63-0.71 | CONTEXT.md | Lines 182-184 | PASS |
| 14 workable at peak, 13 at 11pm | CONTEXT.md | Line 177 | PASS |
| 42-fold frequency variation | CONTEXT.md | Line 163 | PASS |
| 160,000 frontaliers | CONTEXT.md | Line 185 | PASS |
| Shannon phase transition at 1.0 | CONTEXT.md | Line 184 | PASS |
| CLAUDE.md is 800 lines | CLAUDE.md | Line count | **FAIL -- 382 lines** |
| QGIS project has 60 layers | CLAUDE.md / CONTEXT.md | CLAUDE.md: ~60, CONTEXT.md: 52 | MINOR DISCREPANCY |
| 4 Claude accounts | CLAUDE.md | Team system table | PASS (5 listed, 4 active) |
| TODO_4_POINTS.md: 4 investigations | TODO_4_POINTS.md | Full document | PASS |
| "NEW S8 (Lumen)" attribution tags | CONTEXT.md | Lines 109, 111 | PASS |

---

## Overall Assessment

The document is well-researched and the vast majority of claims about City101 project files are accurate. Direct quotes from project files are verified and match their sources. The six-pattern framework is a faithful abstraction of what the project files describe. External case studies are cited with enough specificity to be independently checkable.

**Two critical errors must be fixed before publication:**

1. **CLAUDE.md line count**: 382 lines, not 800. This appears twice (lines 166 and 275). The claim "800 lines -- too long for most projects" becomes "382 lines" which actually undermines the rhetorical point. The author may be thinking of a combined count (CLAUDE.md + CONTEXT.md + LEARNINGS.md + research-with-agent-team.md would approach 800+), or may have counted an earlier version. Either way, the number needs correcting or the scope of what is being counted needs clarification.

2. **The MCP paraphrase in quotation marks** (minor but sloppy for an academic document): either use the exact text from LEARNINGS.md or remove the quotation marks.

Everything else is solid. The project file cross-references are accurate, the terminology is consistent, and the pattern abstraction is faithful to the source material. The external case studies and academic references cannot be verified here but are cited with enough detail to check independently.

**Recommendation:** Fix C1/C2 (line count), clean up M1 (false direct quote), and optionally add a footnote for M3 (account count). Then the document is publication-ready from a factual accuracy standpoint.
