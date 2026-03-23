# Blender Router MCP — Setup Guide

Multi-instance Blender routing for agent teams. Each Claude agent/teammate gets its own Blender instance.

## How it works

```
Claude Code ──[MCP]──> Router ──[TCP:9876]──> Blender 1 (terrain.blend)
                              ──[TCP:9877]──> Blender 2 (buildings.blend)
                              ──[TCP:9878]──> Blender 3 (landscape.blend)
```

The router is a single MCP server that proxies commands to multiple Blender instances. Every tool call includes a `target` parameter that selects which Blender receives the command.

## Prerequisites

- **Blender 3.0+** (tested with 4.x)
- **uv** (Python package manager): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **BlenderMCP addon** installed in Blender

### Installing the BlenderMCP addon

1. Open Blender → Edit → Preferences → Add-ons
2. Click **Install from Disk** (top right)
3. Navigate to `tools/blender/blender_mcp_addon.py` and select it
4. Enable the checkbox next to "Interface: Blender MCP"
5. **Repeat for each Blender instance** (if using separate Blender installations)

## Step-by-step: Single instance (testing)

1. **Open Blender**
2. Press `N` to open the sidebar → click the **BlenderMCP** tab
3. Set port to **9876** (default)
4. Click **Connect**
5. Edit `.mcp.json` in the repo root:
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "uv",
         "args": ["run", "tools/blender/blender_router_mcp.py"],
         "env": {
           "BLENDER_INSTANCES": "{\"main\": 9876}"
         }
       }
     }
   }
   ```
6. **Restart Claude Code** (MCP config only loads on startup)
7. Test: ask Claude to `blender_get_scene_info` with target "main"

## Step-by-step: Multiple instances (agent teams)

1. **Open Blender instance 1** — for terrain
   - Sidebar → BlenderMCP → port **9876** → Connect
   - Save as `terrain.blend`

2. **Open Blender instance 2** — for buildings
   - Sidebar → BlenderMCP → port **9877** → Connect
   - Save as `buildings.blend`

3. **Open Blender instance 3** (optional) — for landscape
   - Sidebar → BlenderMCP → port **9878** → Connect
   - Save as `landscape.blend`

4. Edit `.mcp.json`:
   ```json
   {
     "mcpServers": {
       "blender": {
         "command": "uv",
         "args": ["run", "tools/blender/blender_router_mcp.py"],
         "env": {
           "BLENDER_INSTANCES": "{\"terrain\": 9876, \"buildings\": 9877, \"landscape\": 9878}"
         }
       }
     }
   }
   ```

5. **Restart Claude Code**

6. Each agent uses their assigned target:
   - Terrain agent → `target: "terrain"`
   - Building agent → `target: "buildings"`
   - Landscape agent → `target: "landscape"`

## Adding instances at runtime

You don't need to restart Claude Code to add more instances. Open a new Blender, connect on a new port, then:

```
blender_register_instance(name="detail", port=9879)
```

## Available tools

All tools take a `target` parameter (instance name).

| Tool | Description |
|------|-------------|
| `blender_list_instances` | Show all instances and connection status |
| `blender_register_instance` | Add a new instance at runtime |
| `blender_unregister_instance` | Remove an instance |
| `blender_get_scene_info` | Get scene objects, materials, etc. |
| `blender_get_object_info` | Get details for a specific object |
| `blender_get_viewport_screenshot` | Capture viewport image |
| `blender_execute_code` | Run arbitrary Python (bpy) code |
| `blender_search_polyhaven_assets` | Search PolyHaven HDRIs/textures/models |
| `blender_download_polyhaven_asset` | Download and apply PolyHaven asset |
| `blender_set_texture` | Apply texture to an object |
| `blender_search_sketchfab_models` | Search Sketchfab |
| `blender_download_sketchfab_model` | Download Sketchfab model |
| `blender_generate_hyper3d_model_via_text` | AI-generate 3D model from text |
| `blender_generate_hyper3d_model_via_images` | AI-generate 3D model from images |
| `blender_generate_hunyuan3d_model` | Generate with Hunyuan3D |
| `blender_transfer_geometry` | Transfer objects between instances |
| `blender_command` | Generic passthrough for any command |

## Cross-instance geometry transfer

The `blender_transfer_geometry` tool exports from one instance and imports into another — this is how agents share work:

```
blender_transfer_geometry(
    source="terrain",
    destination="buildings",
    source_collection="Terrain_Final",
    destination_collection="Context_Terrain",
    file_format="fbx"
)
```

## Switching between router and standard mode

### Router mode (multi-instance)
```json
{
  "mcpServers": {
    "blender": {
      "command": "uv",
      "args": ["run", "tools/blender/blender_router_mcp.py"],
      "env": {
        "BLENDER_INSTANCES": "{\"main\": 9876}"
      }
    }
  }
}
```

### Standard mode (single instance, no routing)
```json
{
  "mcpServers": {
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    }
  }
}
```

**Always restart Claude Code after changing `.mcp.json`.**

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Cannot connect to Blender instance" | Check Blender is open and MCP addon is connected on the right port |
| "Unknown instance 'X'" | Use `blender_list_instances` to see registered instances, or `blender_register_instance` to add |
| Timeout errors | Increase timeout: add `"BLENDER_ROUTER_TIMEOUT": "60.0"` to env in .mcp.json |
| Addon not showing in sidebar | Re-install the addon, make sure it's enabled in preferences |
| Port already in use | Another Blender/process is using that port. Pick a different one. |
| Tools not appearing after restart | Check `uv run tools/blender/blender_router_mcp.py` runs without errors |

## Key differences from Rhino router

| | Rhino | Blender |
|---|---|---|
| Multiple processes on Mac | No (one Rhino only) | Yes (multiple Blender windows) |
| Port config | Modified plugin needed | Built into addon (sidebar panel) |
| Protocol | TCP + JSON | TCP + JSON (identical) |
| Code execution | RhinoScript Python / C# | bpy Python |
| Geometry transfer | .3dm export/import | FBX/OBJ/GLB export/import |
| Layer vs Collection | Layers | Collections |
