# Prompt: AI Workflow Diagram — Studio Presentation Slide

## Context
You're working on City101, an EPFL architecture studio project. Read CONTEXT.md first.

Andrea and Henna use Claude (AI) as a core part of their design workflow — not just for text but for modeling (Rhino MCP), mapping (QGIS MCP), data analysis, visualization, and collaborative workflow management. They need a visual diagram showing HOW they work with AI for a studio critique.

## The concept

Create an interactive HTML page (`deliverables/A04/ai_workflow_diagram.html`) that looks like a **tmux or VSCode split-pane terminal** — because that's actually what the workflow looks like in practice. The aesthetic should feel like you're looking at their actual working environment.

## What to show

### Layer 1: The practical workflow
Show the actual tools and how they connect:

```
┌─────────────────────────────────────────────────────┐
│ ANDREA's TERMINAL (Claude Code)                     │
│                                                     │
│  claude > "model the relay-lock chamber at Morges"  │
│                                                     │
│  → reads CONTEXT.md (project state)                 │
│  → reads LEARNINGS.md (what NOT to do)              │
│  → calls Rhino MCP (geometry)                       │
│  → calls QGIS MCP (site data)                      │
│  → commits to git (version control)                 │
│  → writes handoff (for Henna)                       │
│                                                     │
├─────────────────────────────────────────────────────┤
│ HENNA's SESSION (Claude Desktop)                    │
│                                                     │
│  reads handoff → continues from Andrea's state      │
│  → analytical work, narrative, 24h artifacts        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Layer 2: The repo as shared brain
Show how the git repository works as shared memory between team members AND between AI sessions:

- `CONTEXT.md` = living project state (always loaded)
- `LEARNINGS.md` = accumulated mistakes (AI reads this to not repeat errors)
- `LOCKBOARD.md` = who's working on what (prevents conflicts)
- `handoffs/` = session-to-session continuity
- `prompts/` = reusable AI instructions
- `.claude/agents/` = specialized roles (analyst, cartographer, modeler, etc.)
- `deliverables/` = outputs

### Layer 3: The prototypology generator concept
This is the forward-looking part. Show the vision:

- Input: 2 geographic points along the corridor + site constraints (gradient, density, transport access)
- Process: Claude + Rhino MCP generates the prototypological model connecting those points
- Output: A site-adapted architectural intervention (the "chamber")
- The key idea: it's not vibecoded geometry. It's a SYSTEM — like Design Explorer (https://design-explorer.epfl.ch/DesignExplorer/) but for prototypology. Same building logic, different sites.

### Layer 4: What makes this different from "we used ChatGPT"
Show the depth:
- Version-controlled prompts (reproducible)
- Accumulated learnings (the AI gets better over sessions)
- Multi-agent collaboration (5 specialized agents)
- Direct tool integration (Rhino, QGIS — not copy-paste but live connection)
- Handoff system (async collaboration between team members through AI)

## Design specs

**Aesthetic: tmux/terminal themed**
- Dark background (#0a0a0f or #1e1e2e — catppuccin mocha vibes)
- Monospace font (DM Mono or JetBrains Mono)
- Green/cyan/gold accent colors for different sections
- Subtle glow effects on active elements
- Split-pane layout like a real terminal multiplexer
- Maybe a blinking cursor somewhere

**BUT also readable by non-technical critics:**
- Include clear labels and annotations
- A legend/key explaining what each pane represents
- Flow arrows showing the process direction
- Maybe a "play" button that animates the workflow step by step

**Size:** Designed for a single PPTX slide (16:9 aspect ratio, 1920x1080) but as HTML so it can also be shown live

## Output
- `deliverables/A04/ai_workflow_diagram.html` — the interactive diagram
- Self-contained (inline CSS/JS, no external deps except fonts)
- Commit with clear message

## Quality bar
This should make the critics go "wait, you actually built a system?" — not "oh they used AI."
The visual should look real, not corporate-diagram generic. It should feel like peering into the actual working environment.
