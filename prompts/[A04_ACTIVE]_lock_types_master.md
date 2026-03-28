# Lock Types — Concept Modeling Master Prompt

## What this is
9 generic lock type models — pure architectural concepts without site context.
Each type runs on its own Rhino instance via the router MCP, modeled by a separate Claude Code terminal.

## Setup

### 1. Configure Rhino instances
Open 3 Rhino windows (or up to 9 if your machine handles it). In each, run `mcpstart` and assign a unique port.

**Batch approach (3 at a time):**

| Batch | Types | Ports |
|-------|-------|-------|
| Batch 1 | 01 Border, 02 Cargo, 03 Altitude N | 9001, 9002, 9003 |
| Batch 2 | 04 Temporal, 05 Visibility, 06 Gradient | 9001, 9002, 9003 |
| Batch 3 | 07 Gap Relay, 08 Altitude S, 09 Bridge | 9001, 9002, 9003 |

**Full parallel (9 at once) — update `.mcp.json`:**
```json
{
  "mcpServers": {
    "rhino": {
      "command": "uv",
      "args": ["run", "experiments/rhino mcp server/rhino_router_mcp.py"],
      "env": {
        "RHINO_INSTANCES": "{\"lock_01\": 9001, \"lock_02\": 9002, \"lock_03\": 9003, \"lock_04\": 9004, \"lock_05\": 9005, \"lock_06\": 9006, \"lock_07\": 9007, \"lock_08\": 9008, \"lock_09\": 9009}",
        "ARCHIBASE_PATH": "H:/Shared drives/City 101/archibase"
      }
    }
  }
}
```

### 2. Open terminals
One Claude Code terminal per lock type. Paste the corresponding prompt file:
- `prompts/[A04_ACTIVE]_lock_type_01_border.md`
- `prompts/[A04_ACTIVE]_lock_type_02_cargo.md`
- `prompts/[A04_ACTIVE]_lock_type_03_altitude_north.md`
- `prompts/[A04_ACTIVE]_lock_type_04_temporal.md`
- `prompts/[A04_ACTIVE]_lock_type_05_visibility.md`
- `prompts/[A04_ACTIVE]_lock_type_06_gradient.md`
- `prompts/[A04_ACTIVE]_lock_type_07_gap_relay.md`
- `prompts/[A04_ACTIVE]_lock_type_08_altitude_south.md`
- `prompts/[A04_ACTIVE]_lock_type_09_bridge.md`

### 3. Convention shared across all 9 prompts

**Origin**: All models at (0, 0, 0) — no site offset, no LV95.

**Layer naming**: `Type_XX_Name::Category`
- `::Volumes` — primary massing solids
- `::Circulation` — paths, ramps, stairs as curves or thin surfaces
- `::Structure` — columns, beams, cores
- `::Openings` — doors, windows, voids
- `::Annotations` — text dots labeling key spaces

**LOD target**: LOG 200–300 (volumetric concept with basic structure, not detail).

**Color convention** (matches architecture_diagram.html):
| Type | Color RGB |
|------|-----------|
| 01 Border | 255, 107, 107 |
| 02 Cargo | 255, 169, 77 |
| 03 Altitude N | 255, 212, 59 |
| 04 Temporal | 105, 219, 124 |
| 05 Visibility | 77, 171, 247 |
| 06 Gradient | 151, 117, 250 |
| 07 Gap Relay | 240, 101, 149 |
| 08 Altitude S | 252, 196, 25 |
| 09 Bridge | 32, 201, 151 |

### 4. After all models are done
Import all 9 into a single Rhino file, spaced 60m apart along X-axis, for comparison.
