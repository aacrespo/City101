# Rhino Multi-Port MCP Setup

How to connect Claude Code to Rhino on a custom port, and how to use the router for agent teams.

## Mac limitation

Rhino 8 on Mac only allows **one process**. You cannot run two separate Rhino windows as independent instances. This means:
- **Level 1** (separate Claude sessions, separate Rhinos) — not possible on Mac
- **Level 2** (router + agent team, one Rhino) — works. Agents share one Rhino but work on different layers.

On Windows, multiple Rhino instances are possible.

## Normal use (single session, single Rhino)

Default `.mcp.json` — no changes needed:
```json
{
  "mcpServers": {
    "rhino": {
      "command": "uvx",
      "args": ["rhinomcp"]
    }
  }
}
```
In Rhino: `mcpstart` + Enter (default port 1999).

## Custom port (single session)

Useful if port 1999 is taken or you want explicit control.

1. In Rhino: `mcpstart 9001` (or any port 1024–65535)
2. Launch Claude Code with the port:
   ```bash
   RHINO_MCP_PORT=9001 claude
   ```

Or use a wrapper script — edit the port in `rhinomcp_wrapper.sh`, then set `.mcp.json`:
```json
{
  "mcpServers": {
    "rhino": {
      "command": "/path/to/rhinomcp_wrapper.sh",
      "args": []
    }
  }
}
```

**You must restart Claude Code** (not just `/mcp`) for config changes to take effect.

## Router (agent teams)

The router lets multiple agents work in the same Rhino instance on different layers. Each tool call includes a `target` parameter.

1. In Rhino: `mcpstart 9002` (or any port)
2. Copy `mcp_router.json` to `.mcp.json` (edit the port to match):
   ```json
   {
     "mcpServers": {
       "rhino_router": {
         "command": "uv",
         "args": ["run", "experiments/rhino mcp server/rhino_router_mcp.py"],
         "env": {
           "RHINO_INSTANCES": "{\"main\": 9002}"
         }
       }
     }
   }
   ```
3. Start Claude Code. Tools will have `target` parameter (e.g. `rhino_create_object(target="main", ...)`).

**Switch back to normal:** Revert `.mcp.json` to the standard `uvx rhinomcp` config above.

## Modified plugin

The upstream rhinomcp C# plugin hardcodes port 1999. We forked it to accept a port argument.

- Fork: `~/repos/rhinomcp` (branch `feature/configurable-port`, GitHub: `aacrespo/rhinomcp`)
- Installed at: `~/Library/Application Support/McNeel/Rhinoceros/packages/8.0/rhinomcp/0.2.1/net8.0/rhinomcp.rhp`
- Changes: 2 files, ~10 lines total (see `plugin_port_fix.md`)
- Backward compatible: plain `mcpstart` still uses port 1999

## Setting up on another machine (Henna's)

1. Clone the forked repo:
   ```bash
   gh repo clone aacrespo/rhinomcp ~/repos/rhinomcp
   cd ~/repos/rhinomcp && git checkout feature/configurable-port
   ```

2. Build the plugin (requires .NET SDK):
   ```bash
   brew install dotnet
   cd ~/repos/rhinomcp/rhino_mcp_plugin
   dotnet build -c Release
   ```

3. Find Henna's installed rhinomcp version:
   ```bash
   ls ~/Library/Application\ Support/McNeel/Rhinoceros/packages/8.0/rhinomcp/
   ```

4. Copy the built plugin over the latest version:
   ```bash
   cp ~/repos/rhinomcp/rhino_mcp_plugin/bin/Release/net8.0/rhinomcp.rhp \
      ~/Library/Application\ Support/McNeel/Rhinoceros/packages/8.0/rhinomcp/<VERSION>/net8.0/rhinomcp.rhp
   ```

5. Restart Rhino. Test: `mcpstart 9001` should prompt for port and show "MCP server started on port 9001."

## Files in this directory

| File | Purpose |
|---|---|
| `rhino_router_mcp.py` | Router MCP server (TCP proxy to Rhino) |
| `README.md` | Router architecture and full tool reference |
| `SETUP.md` | This file |
| `plugin_port_fix.md` | Exact C# diffs for the plugin modification |
| `mcp_router.json` | Drop-in `.mcp.json` for router mode |
| `rhinomcp_wrapper.sh` | Wrapper script for port 9001 |
| `rhinomcp_wrapper_9002.sh` | Wrapper script for port 9002 |
