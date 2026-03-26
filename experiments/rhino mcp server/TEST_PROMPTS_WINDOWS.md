# Router + Multi-Rhino Test Prompts — Windows

Test progression for validating the multi-instance Rhino MCP router on Windows.
Windows can run multiple Rhino processes (unlike Mac which is limited to one).

## Before you start

### Install the modified plugin

The upstream rhinomcp plugin hardcodes port 1999. You need the fork that accepts a port argument.

```powershell
gh repo clone aacrespo/rhinomcp ~\repos\rhinomcp
cd ~\repos\rhinomcp
git checkout feature/configurable-port
```

Build (requires .NET SDK):
```powershell
cd rhino_mcp_plugin
dotnet build -c Release
```

Find your installed rhinomcp version and copy over it:
```powershell
dir $env:APPDATA\McNeel\Rhinoceros\packages\8.0\rhinomcp\
# Copy the built .rhp over the existing one (check net48 vs net8.0 in build output)
copy bin\Release\net48\rhinomcp.rhp $env:APPDATA\McNeel\Rhinoceros\packages\8.0\rhinomcp\<VERSION>\net48\rhinomcp.rhp
```

Restart Rhino. Test: type `mcpstart 9001` — should say "MCP server started on port 9001."

### Install router dependencies

```powershell
pip install mcp httpx pydantic
```

### Router config template

When tests say "use router config", put this in your project `.mcp.json`:

```json
{
  "mcpServers": {
    "rhino_router": {
      "command": "python",
      "args": ["experiments/rhino mcp server/rhino_router_mcp.py"],
      "env": {
        "RHINO_INSTANCES": "<see each test>"
      }
    }
  }
}
```

**You must restart Claude Code** (not just `/mcp`) after changing `.mcp.json`.

---

## Test 1 — Sanity: single Rhino, default port

**Goal:** Confirm basic MCP works before touching the router.

**Setup:**
- Open Rhino, type `mcpstart`
- Use default `.mcp.json` (`"command": "uvx", "args": ["rhinomcp"]`)

**Prompt:**
```
Create a box at the origin, 5m x 5m x 3m, on a layer called "test_basic".
Then list all objects in the scene to confirm it worked.
```

**Expected:** One box appears in Rhino. Claude reports 1 object.

---

## Test 2 — Custom port

**Goal:** Confirm the modified plugin accepts a port argument.

**Setup:**
- In Rhino: `mcpstart 9001`
- Launch Claude Code: `set RHINO_MCP_PORT=9001 && claude`

**Prompt:**
```
Create a sphere at (10, 0, 0) with radius 2m on a layer called "test_port".
Query the document summary to confirm one object exists.
```

**Expected:** Sphere appears. Document summary shows 1 object.

---

## Test 3 — Router with one instance

**Goal:** Confirm the router proxies correctly to a single Rhino.

**Setup:**
- In Rhino: `mcpstart 9001`
- `.mcp.json` with `RHINO_INSTANCES`: `{"main": "http://localhost:9001"}`
- Restart Claude Code

**Prompt:**
```
List available Rhino instances using rhino_list_instances.
Then create a cylinder on target "main", layer "test_router",
center at origin, radius 1m, height 5m.
```

**Expected:** `rhino_list_instances` shows "main" as connected. Cylinder appears.

---

## Test 4 — Two Rhino instances, manual routing

**Goal:** The big Windows-only test. Two separate Rhino processes.

**Setup:**
- Open Rhino window 1 (new file) → `mcpstart 9001`
- Open Rhino window 2 (new file) → `mcpstart 9002`
- `.mcp.json` with `RHINO_INSTANCES`: `{"structure": "http://localhost:9001", "envelope": "http://localhost:9002"}`
- Restart Claude Code

**Prompt:**
```
You have two Rhino instances: "structure" (port 9001) and "envelope" (port 9002).

In the "structure" instance:
- Create layer "columns"
- Place 4 columns (boxes 0.3x0.3x3m) at corners of a 6m x 6m grid

In the "envelope" instance:
- Create layer "walls"
- Place 4 walls (boxes 6m x 0.2m x 3m) connecting the column positions

Then query both instances to confirm the object counts.
```

**Expected:** 4 columns in Rhino 1, 4 walls in Rhino 2. Claude reports counts from each.

---

## Test 5 — Geometry transfer between instances

**Goal:** Test `rhino_transfer_geometry` — the killer feature.

**Setup:** Same two-instance setup as Test 4.

**Prompt:**
```
In the "structure" instance, create a floor slab:
a box 6m x 6m x 0.25m at z=3m on layer "slabs".

Transfer the slab geometry from "structure" to "envelope"
so the envelope agent can see where the floor lands.

Then in "envelope", create a window opening (box 2m x 0.15m x 1.5m)
on layer "windows" positioned on one of the walls,
with its head aligned to the bottom of the transferred slab.

Report what's in each instance.
```

**Expected:** Slab appears in both instances. Window positioned correctly relative to slab.

---

## Test 6 — Agent team: simple pavilion

**Goal:** First real agent team test. Two agents, clear separation.

**Setup:**
- Two Rhino windows: `mcpstart 9001`, `mcpstart 9002`
- Router config: `{"structure": "http://localhost:9001", "landscape": "http://localhost:9002"}`

**Prompt:**
```
Assemble a team of 2 agents to model a simple pavilion:

Agent 1 — "Structure": Works on Rhino instance "structure" (port 9001).
Builds: 4 steel columns (simplified as 0.2x0.2m boxes, 4m tall)
at an 8m x 8m grid. Then a roof slab (8.4m x 8.4m x 0.15m) on top
with 0.2m overhang.
Layer: "structure"

Agent 2 — "Landscape": Works on Rhino instance "landscape" (port 9002).
Builds: A ground plane (20m x 20m at z=0), a circular path (radius 6m,
1.5m wide) around the pavilion, and 4 benches (boxes 1.5m x 0.4m x 0.45m)
at cardinal points.
Layer: "landscape"

Coordination: both agents share the same origin (0,0,0).
The landscape agent should leave clear zone inside 5m radius for the structure.
No geometry transfer needed — they work independently.

When done, capture viewports from both instances.
```

**Expected:** Pavilion in one Rhino, landscape in the other. Both centered on same origin.

---

## Test 7 — Agent team: coordinated building (the real test)

**Goal:** Full coordination with geometry handoff. This is what Lock 05 was on Mac, now with real separate instances.

**Setup:**
- Three Rhino windows: `mcpstart 9001`, `mcpstart 9002`, `mcpstart 9003`
- Router config: `{"structure": "http://localhost:9001", "envelope": "http://localhost:9002", "interior": "http://localhost:9003"}`

**Prompt:**
```
Model a small 2-story building using an agent team of 3:

Shared reference:
- Origin: (0, 0, 0)
- Grid: 5m x 5m, 2 bays each direction (total 10m x 10m)
- Floor-to-floor: 3.2m
- Slab thickness: 0.25m

Agent 1 — "Structure" (target: structure)
Build sequence:
1. Ground floor slab (10m x 10m x 0.25m at z=0)
2. 9 columns (0.3m x 0.3m x 2.95m) at grid intersections, z=0.25 to z=3.2
3. First floor slab at z=3.2
4. 9 more columns z=3.45 to z=6.4
5. Roof slab at z=6.4

Agent 2 — "Envelope" (target: envelope)
Wait for structure to finish the ground floor slab, then:
1. Transfer slab geometry from "structure" to "envelope" for reference
2. Build perimeter walls (0.2m thick, 2.95m tall) on all 4 sides, ground floor
3. Cut 4 window openings (1.5m wide x 1.8m tall, sill at 0.9m) on south wall
4. Repeat for first floor
5. Build a parapet (0.9m tall) at roof level

Agent 3 — "Interior" (target: interior)
Wait for structure to finish both floors, then:
1. Transfer floor slabs from "structure" to "interior" for reference
2. Build a stair core (2.5m x 5m footprint) in the northeast bay
3. Add partition walls (0.1m thick) dividing ground floor into 2 rooms
4. Add a reception desk (2m x 0.8m x 1.1m) in the larger ground floor room

Coordination rules:
- Structure goes first (slabs and columns define everything)
- Envelope and Interior start after structure completes their floor
- Use rhino_transfer_geometry for handoffs
- Each agent reports object count when done
- Lead captures viewport from each instance at the end
```

**Expected:** Coherent building across 3 Rhino windows. Slabs align, walls meet columns, interior fits within envelope.

---

## Test 8 — Dynamic instance registration

**Goal:** Test adding a Rhino instance mid-session.

**Setup:** Start with 2 instances only: "structure" (9001), "envelope" (9002).

**Prompt:**
```
List the current Rhino instances.

Now I've opened a third Rhino window and ran mcpstart 9003.
Use rhino_register_instance to add it as "landscape" at http://localhost:9003.
Verify with rhino_list_instances that all 3 appear.

Then build site context in "landscape":
a ground plane (30m x 30m at z=0), an access path (2m wide)
from the south edge to the building, and 3 trees
(cylinder trunks 0.3m radius x 4m tall, sphere crowns radius 2m at z=5m).
```

**Expected:** Third instance registered on the fly. Landscape geometry built without restarting Claude.

---

## Troubleshooting

- **"Connection refused"**: Rhino MCP not started, or wrong port. Check Rhino command line.
- **Router shows instance as disconnected**: Firewall blocking localhost? Try `Test-NetConnection localhost -Port 9001` in PowerShell.
- **Rhino freezes on MCP call**: Run `mcpstop` then `mcpstart <port>` again in Rhino.
- **"target not found"**: Instance name in prompt doesn't match RHINO_INSTANCES key. Check spelling.
- **Plugin build fails**: Check .NET SDK version. Rhino 8 on Windows may need `net48` target, not `net8.0`.
- **Changes to .mcp.json not taking effect**: Must fully restart Claude Code, not just `/mcp`.

## What to report back

For each test, note:
1. Did it work? (yes / partial / no)
2. Latency feel — any noticeable lag vs direct connection?
3. Any error messages (screenshot or copy)
4. For agent team tests: did geometry align between instances?
5. Windows-specific quirks (paths, firewall prompts, .NET framework version)
