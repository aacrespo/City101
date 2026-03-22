# Session Log — Rhino Multi-Instance Modeling

**Date**: 2026-03-19 → 2026-03-20 (overnight session)
**Branch**: `andrea/prototypology-v2`
**Who**: Andrea + Claude (Cairn Code CLI, Opus 4.6 1M)

## What we set out to do

Implement the plan from the earlier research session: enable parallel Rhino modeling via Claude Code — either multiple sessions or agent teams. The plan identified 3 levels of capability, a plugin blocker, and a router architecture.

## What we built

### 1. Router MCP Server (`rhino_router_mcp.py`)

**Complete rewrite** of the HTTP prototype → TCP transport matching rhinomcp's actual wire protocol.

- 1209 lines, 31 MCP tools
- `RhinoInstanceConnection` class — TCP socket per Rhino instance, per-instance threading lock, connect-on-demand, incremental JSON parsing (mirrors rhinomcp's `RhinoConnection`)
- `InstanceRegistry` — thread-safe name-to-connection mapping, loaded from `RHINO_INSTANCES` env var
- `_route(target, command_type, params)` — core routing function

**Tools (31):**
- 3 management: `rhino_list_instances`, `rhino_register_instance`, `rhino_unregister_instance`
- 4 queries: `rhino_get_document_summary`, `rhino_get_objects`, `rhino_get_object_info`, `rhino_get_selected_objects_info`
- 6 create/modify: `rhino_create_object`, `rhino_create_objects`, `rhino_modify_object`, `rhino_modify_objects`, `rhino_delete_object`, `rhino_select_objects`
- 2 code execution: `rhino_execute_python_code`, `rhino_execute_csharp_code`
- 3 layers: `rhino_create_layer`, `rhino_get_or_set_current_layer`, `rhino_delete_layer`
- 1 viewport: `rhino_capture_viewport`
- 3 booleans: `rhino_boolean_union`, `rhino_boolean_difference`, `rhino_boolean_intersection`
- 5 advanced geometry: `rhino_loft`, `rhino_extrude_curve`, `rhino_sweep1`, `rhino_offset_curve`, `rhino_pipe`
- 2 undo/redo: `rhino_undo`, `rhino_redo`
- 1 passthrough: `rhino_command` (generic, covers all 28 TCP command types)
- 1 transfer: `rhino_transfer_geometry` (cross-instance via RhinoScript export/import)

**Tested:**
- 5/5 mock TCP server tests (routing, create, error handling, dynamic registration)
- 5/5 live Rhino tests (document summary, create sphere, query objects, undo)
- Agent team test: 7 agents, 709 objects, 4 build rounds on Lock 05 CHUV

### 2. C# Plugin Port Fix

**Forked** `jingcheng-chen/rhinomcp` → `aacrespo/rhinomcp`, branch `feature/configurable-port`.

**Two files changed:**

`RhinoMCPServerController.cs`:
- `StartServer()` → `StartServer(int port = 1999)`
- Passes port to `new RhinoMCPServer("127.0.0.1", port)`
- Second commit: stops existing server before creating new one (fix for Mac single-process)

`MCPStartCommand.cs`:
- Added `GetInteger()` prompt for port number
- Default 1999, range 1024–65535
- `AcceptNothing(true)` — Enter key accepts default

**Two commits:**
1. `feat: allow configurable port for mcpstart command`
2. `fix: stop existing server before starting on new port`

**Built with:** .NET SDK 10.0.105 (installed via `brew install dotnet`)
**Installed to:** `~/Library/Application Support/McNeel/Rhinoceros/packages/8.0/rhinomcp/0.2.1/net8.0/rhinomcp.rhp`

### 3. Supporting files

| File | What |
|---|---|
| `experiments/rhino mcp server/rhino_router_mcp.py` | Router (complete rewrite) |
| `experiments/rhino mcp server/README.md` | Router architecture, all 28 tools documented |
| `experiments/rhino mcp server/SETUP.md` | Complete setup guide, Mac limitations, Henna's setup |
| `experiments/rhino mcp server/plugin_port_fix.md` | Exact C# diffs |
| `experiments/rhino mcp server/mcp_router.json` | Drop-in `.mcp.json` for router mode |
| `experiments/rhino mcp server/rhinomcp_wrapper.sh` | Port 9001 wrapper |
| `experiments/rhino mcp server/rhinomcp_wrapper_9002.sh` | Port 9002 wrapper |
| `experiments/rhino mcp server/SESSION_LOG.md` | This file |
| `workflows/agent-team-modeling.md` | Full workflow from the 7-agent test |

## Key discovery: Mac single-process limitation

Rhino 8 on Mac only allows one process. `open -n -a "Rhino 8"` shows "Rhinoceros already running" dialog.

**Impact:**
- Level 1 (separate sessions, separate Rhinos) — **not possible on Mac**
- Level 2 (router + agent team, one Rhino) — **works perfectly**
- All agents share one Rhino process, use `target="main"`, work on different layers

This makes the router the essential piece, not just an optimization.

## Debugging timeline

### rhinomcp env var saga
Tried 5 approaches to pass `RHINO_MCP_PORT` to the MCP server process:
1. `.mcp.json` `env` field → didn't work
2. `env RHINO_MCP_PORT=9001 uvx rhinomcp` as command → didn't work
3. `sh -c "RHINO_MCP_PORT=9001 uvx rhinomcp"` → didn't work
4. Wrapper script as `.mcp.json` command → didn't work (wrapper never ran)
5. **Root cause**: `/mcp` reconnects to existing process, doesn't restart. Need full Claude Code restart.

**Resolution**: Wrapper script works when starting a **new** Claude Code session. Also: `RHINO_MCP_PORT=9001 claude` works (env inherited by child process).

### Plugin location
Build output went to `/Applications/Rhino 8.app/Contents/PlugIns/` but Rhino loads from `~/Library/Application Support/McNeel/Rhinoceros/packages/8.0/rhinomcp/0.2.1/net8.0/`. Had to copy to the right location.

### "Server is already running" bug
First version of `StartServer(int port)` used `if (server == null)` — if a server existed from a previous `mcpstart`, it reused the old one on the old port. Fixed by always stopping the old server first.

### Mac single-process
`open -n -a "Rhino 8"` spawned a second PID but Rhino showed "Rhinoceros already running" dialog. Only one Rhino process allowed on Mac, confirmed by Apple's app model for Rhino 8.

## What to do next

1. **PR upstream** — the plugin port fix is clean and backward-compatible. Good candidate for `jingcheng-chen/rhinomcp`.
2. **Henna setup** — documented in SETUP.md. Clone fork, build, copy .rhp.
3. **Prototypology at scale** — use the agent team workflow for all 9 nodes.
4. **Geometry transfer testing** — `rhino_transfer_geometry` is built but untested with live Rhino (needs multi-instance, i.e. Windows, or could test within same instance between layers).
5. **Workflow refinement** — `workflows/agent-team-modeling.md` is v1 from one test. Will evolve.

## Config state after session

- `.mcp.json` — reverted to standard `uvx rhinomcp` (port 1999)
- Plugin — modified version installed (supports custom ports, backward compatible)
- `~/repos/rhinomcp` — fork with 2 commits on `feature/configurable-port`
- Router — ready in `experiments/rhino mcp server/`, not active
