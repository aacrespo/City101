# .claude/ — Claude Code Infrastructure

This directory contains all Claude Code configuration for the city101 project. Everything here is shared via git — both team members get the same commands, agents, and rules.

## Commands (slash commands) — 20

### Roles
| Command | What it does |
|---------|-------------|
| `/analyst` | Data collection, verification, API queries |
| `/cartographer` | Map generation, spatial outputs |
| `/modeler` | Rhino 3D modeling via MCP |
| `/visualizer` | Charts, interactive visualizations |
| `/builder` | Deployment, packaging, narrative assembly |

### Session
| Command | What it does |
|---------|-------------|
| `/session-start` | Load context, check lockboard, brief |
| `/session-end` | Full close-out — update context, lockboard, commit |
| `/save-session` | Quick bookmark for resuming later |
| `/resume-session` | Pick up from last saved session |

### Teams
| Command | What it does |
|---------|-------------|
| `/team` | Dynamic team assembly — multi-role parallel work |
| `/build-with-agent-team` | Rhino agent team modeling session |
| `/research-with-agent-team` | Multi-agent research session |

### Skills
| Command | What it does |
|---------|-------------|
| `/parametric` | Generate knowledge-grounded Rhino scripts (queries archibase) |
| `/import-terrain` | Import SwissALTI3D terrain into Rhino |
| `/site-context` | Assemble site context (buildings, roads, terrain) |
| `/rhino-review` | Review current Rhino document state |
| `/pdf` | Export to PDF |
| `/unlock` | Remove PDF restrictions |

### Utilities
| Command | What it does |
|---------|-------------|
| `/verify-data` | Run quality gates on a dataset |
| `/brain-dump` | Structure raw ideas into actionable prompts |

## Agents — 11

| Agent | Role |
|-------|------|
| `analyst` | Data collection and verification |
| `builder` | Deployment and packaging |
| `cartographer` | Maps and spatial work |
| `modeler` | Rhino 3D modeling |
| `visualizer` | Charts and interactive viz |
| `site-context-builder` | Site data assembly |
| `structural-reviewer` | Structure review |
| `envelope-reviewer` | Envelope/facade review |
| `accessibility-reviewer` | Accessibility compliance |
| `log-compliance-reviewer` | LOI/LOG/LOD compliance |
| `concept-critic` | Design concept critique |

## Rules — 5 (auto-loaded every session)

| File | What it governs |
|------|----------------|
| `conventions.md` | Coordinates (LV95), commit prefixes, file safety, git workflow |
| `data-protocol.md` | Collection requirements, quality gates, corridor reference |
| `tool-protocol.md` | When to use tools/workflows, error handling, permissions |
| `prompt-craft.md` | Prompt structure principles, execution modes, naming convention |
| `rhino-mcp.md` | Router vs standard MCP mode, setup, when to switch |

## Settings

| File | Shared? | What |
|------|---------|------|
| `settings.json` | Yes (git) | Hooks config (session logging, break reminders) |
| `settings.local.json` | No (local) | Personal permissions — each person has their own |

## For Henna

When you pull the repo, you get everything above. To set up:
1. Run any slash command — it just works
2. For Rhino MCP: see `rules/rhino-mcp.md` for setup steps
3. For archibase (construction knowledge): copy the folder from shared drive, see archibase/README.md
4. Your `settings.local.json` is your own — set permissions as you like
