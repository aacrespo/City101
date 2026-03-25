# Idea: `/architect` agent role

**From:** Cairn Code, 2026-03-18 03:25
**Context:** Just ran 6 parallel agents to produce system architecture docs (2,877 lines, 45 Mermaid diagrams). Agents were general-purpose — a dedicated architect agent would be sharper.

## What it would do
- Read project context (CONTEXT.md, v2 paper, data inventory, design system)
- Output system diagrams (Mermaid), data flow, decision logic, phasing
- Understand the AI vs deterministic boundary question
- Know the LOI/LOG/LOD framework from 00_Workflow_v04.md
- Produce implementation-ready docs, not just abstractions

## Why it's useful
- This session proved the pattern: brain dump → prompt → parallel architecture docs → review → fix
- A dedicated agent would skip the hallucination problems (wrong lock types, wrong criteria names) because it would have the project vocabulary baked in
- Could be reusable beyond City101 — any project with a data layer + logic layer + output layer

## To build
- Agent definition in `.claude/agents/architect.md`
- Slash command `/architect` in `.claude/commands/`
- Reads: CONTEXT.md, relevant research paper, datasets/INVENTORY.md, design_system/SPEC.md
- Outputs to: `output/app_architecture/` (or wherever specified)

Not urgent. Post-midterm backlog item.
