# Research with Agent Team

Spawn multiple analyst subagents in parallel for a research sprint.

## How it works
1. **Define the research questions** — what are we investigating?
2. **Assign one question per agent** — each agent gets a focused task
3. **Each agent**:
   - Reads CLAUDE.md (automatic)
   - Reads datasets/INVENTORY.md + LEARNINGS.md for context
   - Does its assigned research
   - Writes output to `output/` (staging area — NOT datasets/)
   - Prints a comprehensive summary to stdout
4. **Lead agent (you)** collects results, cross-references, verifies
5. **Promote verified data** to `datasets/` after running `workflows/data-verification.md`

## Rules
- Agents write to `output/` only — never directly to `datasets/`
- Each agent uses tools from `tools/` (same rate limiting, same verification)
- Print full summaries: sources queried, row counts, unexpected findings, leads to follow
- Nothing gets promoted unverified

## Template for spawning
```
Agent task: [specific question]
Write output to: output/[descriptive_name].csv
Datasets to reference: [list relevant existing datasets]
```
