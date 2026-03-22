# Rhino Router MCP

A TCP proxy MCP server that routes commands to multiple Rhino instances, enabling parallel modeling via Claude Code agent teams or multiple sessions.

## Architecture

```
Claude Code ──[stdio/MCP]──> Router ──[TCP:9001]──> Rhino 1 (shell.3dm)
                                    ──[TCP:9002]──> Rhino 2 (mep.3dm)
                                    ──[TCP:9003]──> Rhino 3 (bridge.3dm)
```

Every tool includes a `target` parameter that selects which Rhino instance receives the command. Agent teams share this single MCP server but each agent routes to its own Rhino instance.

## Wire Protocol

The router speaks the same raw TCP protocol as the rhinomcp plugin:

```
Request:  {"type": "command_name", "params": {...}}   → TCP socket
Response: {"status": "success|error", "result": {...}} ← TCP socket
```

No HTTP, no framing — just JSON over TCP with incremental parsing for response completion (matching rhinomcp's `RhinoConnection.receive_full_response()`).

## Prerequisites

### 1. Rhino MCP plugin port fix (required)

The upstream rhinomcp C# plugin hardcodes port 1999. You need a fork that accepts a port argument:

**Changes needed in the C# plugin:**

`RhinoMCPServerController.cs`:
```csharp
// Before:
public static void StartServer() {
    if (server == null) { server = new RhinoMCPServer(); }  // always 1999
    server.Start();
}

// After:
public static void StartServer(int port = 1999) {
    if (server == null) { server = new RhinoMCPServer("127.0.0.1", port); }
    server.Start();
}
```

`MCPStartCommand.cs`:
```csharp
// Before:
protected override Result RunCommand(RhinoDoc doc, RunMode mode) {
    RhinoMCPServerController.StartServer();
    return Result.Success;
}

// After:
protected override Result RunCommand(RhinoDoc doc, RunMode mode) {
    var gi = new GetInteger();
    gi.SetCommandPrompt("Port number (default 1999)");
    gi.SetDefaultInteger(1999);
    gi.SetLowerLimit(1024, false);
    gi.SetUpperLimit(65535, false);
    gi.AcceptNothing(true);
    var result = gi.Get();
    int port = (result == GetResult.Number) ? gi.Number() : 1999;
    RhinoMCPServerController.StartServer(port);
    return Result.Success;
}
```

Build the modified .rhp and install in Rhino.

### 2. Python dependencies

Handled automatically by `uv run` via inline script metadata:
```
mcp[cli] >= 1.0
pydantic >= 2.0
```

## Setup

### 1. Start multiple Rhino instances

Open N Rhino windows. In each one, run:
```
mcpstart 9001   (window 1 — e.g. shell.3dm)
mcpstart 9002   (window 2 — e.g. mep.3dm)
mcpstart 9003   (window 3 — e.g. bridge.3dm)
```

### 2. Configure .mcp.json

Replace the standard rhinomcp config with the router:

```json
{
  "mcpServers": {
    "rhino_router": {
      "command": "uv",
      "args": ["run", "experiments/rhino mcp server/rhino_router_mcp.py"],
      "env": {
        "RHINO_INSTANCES": "{\"shell\": 9001, \"mep\": 9002, \"bridge\": 9003}"
      }
    }
  }
}
```

### 3. Verify

In Claude Code:
```
Use rhino_list_instances to see all connected Rhino windows.
Then try: rhino_get_document_summary(target="shell")
```

## Tools (28)

### Instance Management
| Tool | Purpose |
|---|---|
| `rhino_list_instances` | Show registered instances + connection status |
| `rhino_register_instance` | Add instance at runtime (name, port) |
| `rhino_unregister_instance` | Remove instance |

### Document & Object Queries
| Tool | Purpose |
|---|---|
| `rhino_get_document_summary(target)` | Document overview (layers, counts, units) |
| `rhino_get_objects(target, ...)` | Query objects with filters (layer, type, bbox) |
| `rhino_get_object_info(target, id)` | Detailed info for one object |
| `rhino_get_selected_objects_info(target)` | Info about selected objects |

### Object Creation & Modification
| Tool | Purpose |
|---|---|
| `rhino_create_object(target, type, params, ...)` | Create geometry |
| `rhino_create_objects(target, objects)` | Batch create |
| `rhino_modify_object(target, id, ...)` | Modify properties |
| `rhino_modify_objects(target, objects)` | Batch modify |
| `rhino_delete_object(target, id)` | Delete object |
| `rhino_select_objects(target, filters)` | Select objects |

### Code Execution
| Tool | Purpose |
|---|---|
| `rhino_execute_python_code(target, code)` | Run RhinoScript Python |
| `rhino_execute_csharp_code(target, code)` | Run RhinoCommon C# |

### Layers
| Tool | Purpose |
|---|---|
| `rhino_create_layer(target, name, ...)` | Create layer |
| `rhino_get_or_set_current_layer(target, ...)` | Get/set active layer |
| `rhino_delete_layer(target, name)` | Delete layer |

### Viewport
| Tool | Purpose |
|---|---|
| `rhino_capture_viewport(target, ...)` | Screenshot (PNG) |

### Boolean Operations
| Tool | Purpose |
|---|---|
| `rhino_boolean_union(target, ids)` | Union objects |
| `rhino_boolean_difference(target, base, subtractors)` | Subtract objects |
| `rhino_boolean_intersection(target, ids)` | Intersect objects |

### Advanced Geometry
| Tool | Purpose |
|---|---|
| `rhino_loft(target, curve_ids)` | Loft through curves |
| `rhino_extrude_curve(target, id, direction)` | Extrude curve |
| `rhino_sweep1(target, rail, profiles)` | Sweep along rail |
| `rhino_offset_curve(target, id, distance)` | Offset curve |
| `rhino_pipe(target, id, radius)` | Pipe along curve |

### Undo/Redo
| Tool | Purpose |
|---|---|
| `rhino_undo(target, steps)` | Undo operations |
| `rhino_redo(target, steps)` | Redo operations |

### Passthrough & Transfer
| Tool | Purpose |
|---|---|
| `rhino_command(target, command_type, params)` | Generic passthrough for any command |
| `rhino_transfer_geometry(source, dest, ...)` | Export from one instance, import to another |

## Design Decisions

1. **Sync TCP** — matches rhinomcp's proven approach. Rhino processes commands sequentially anyway.
2. **Per-instance locks** — commands to different instances run concurrently via FastMCP's thread pool; commands to the same instance are serialized by the connection lock.
3. **Connect on demand** — router starts even if Rhino instances aren't ready yet. First command triggers TCP connection.
4. **File-based geometry transfer** — `rhino_transfer_geometry` uses RhinoScript `rs.Command('-_Export ...')` and `rs.Command('-_Import ...')` via temp .3dm files. Not streaming, but reliable.
5. **No httpx** — the old prototype used HTTP but rhinomcp's actual protocol is raw TCP. This version matches the real protocol.

## Usage Patterns

### Pattern 1: Multiple sessions, different nodes (Level 1)
```
Session 1 (.mcp.json with RHINO_INSTANCES={"node_a": 9001})
  → Models node A in Rhino window 1

Session 2 (.mcp.json with RHINO_INSTANCES={"node_b": 9002})
  → Models node B in Rhino window 2
```
Each session gets its own router with one instance. Simple, no coordination needed.

### Pattern 2: Agent team, shared router (Level 2)
```
One session, one router with RHINO_INSTANCES={"shell": 9001, "mep": 9002}

Lead agent:     "Shell modeler, build the envelope on target='shell'"
Shell modeler:  rhino_create_object(target="shell", type="BOX", ...)
MEP agent:      rhino_execute_python_code(target="mep", code="...")
```
All agents use the same router, `target` param routes to different Rhino windows.

### Pattern 3: Full coordination with geometry exchange (Level 3)
```
Lead agent:     "Shell modeler is done. Transfer envelope to MEP."
                rhino_transfer_geometry(source="shell", destination="mep",
                                       source_layer="envelope",
                                       destination_layer="context::shell")
MEP agent:      "I can see the shell. Routing pipes against it."
                rhino_execute_python_code(target="mep", code="...")
```

## Environment Variables

| Variable | Default | Purpose |
|---|---|---|
| `RHINO_INSTANCES` | `""` | JSON map of instance names to ports |
| `RHINO_ROUTER_TIMEOUT` | `30.0` | TCP socket timeout in seconds |
| `RHINO_ROUTER_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |

## Limitations

- **Plugin port fix required** — the upstream rhinomcp C# plugin hardcodes port 1999. Without the fork, you can only run one instance.
- **Geometry transfer uses temp files** — not streaming. Works fine for sub-100k object transfers.
- **No cross-machine support** — router assumes localhost TCP. Could be extended with SSH tunnels.
- **Same Rhino instance is serialized** — by design (Rhino is single-threaded for geometry ops). Different instances run concurrently.
