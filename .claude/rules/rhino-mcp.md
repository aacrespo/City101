# Rhino MCP Configuration

## Two modes

### Router mode (current default in .mcp.json)
Uses `tools/rhino/rhino_router_mcp.py`. Every tool call takes a `target` parameter to route to a specific Rhino instance.

**Use when:** agent teams, multi-agent modeling, any session where multiple agents build in Rhino simultaneously.

**Rhino setup:** run `mcpstart` in Rhino, type port `9002` when prompted.

**Add more instances:** edit `RHINO_INSTANCES` in `.mcp.json`:
```json
"RHINO_INSTANCES": "{\"main\": 9002, \"second\": 9003}"
```

### Standard mode
Uses `uvx rhinomcp`. Single instance, port 1999, no routing.

**Use when:** solo modeling, quick scripts, single-agent Rhino work.

**To switch:** replace `.mcp.json` contents with:
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

**Rhino setup:** run `mcpstart` in Rhino (default port 1999).

## Important
- Switching modes requires **restarting Claude Code** — MCP config only loads on startup.
- Mac limitation: only one Rhino process. Multiple agents share one instance via different layers, not different windows.
- Router mode requires a modified rhinomcp plugin that accepts custom ports. Setup instructions are in `tools/rhino/SETUP.md`.
- If `mcpstart` in Rhino doesn't ask for a port number, the modified plugin isn't installed. Follow the setup guide or fall back to standard mode.
