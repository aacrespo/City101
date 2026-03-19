# Chamber Transport App — Implementation Plan

## Context

City101 "Still on the Line" midterm (March 30) needs an interactive app showing the 7-node relay-lock corridor system. The app integrates Rhino MCP (3D modeling) and Blender MCP (animation/rendering) with a web-based viewer. The existing `city101_prototypology.html` is 90% of the foundation — it already has Leaflet maps, particle flows, time controls, and lock detail panels.

## Architecture

```
Browser App (Three.js + Leaflet + D3)
    ↕ WebSocket (ws://localhost:8765)
Python Backend (agent_server.py)
    ↕ Claude Agent SDK + MCP protocol
  Rhino 8 (modeling)     Blender (animation/render)
    ↓                        ↓
  .glb export            .mp4 / .png render
    ↓
  Three.js GLTFLoader → displayed in browser
```

## File Structure

```
output/chamber_app/
├── chamber_transport.html      ← Main app (single HTML, embedded CSS/JS)
├── chamber_data.js             ← Extracted station/node/flow data
├── chamber_models.js           ← Three.js 3D viewer module
├── models/                     ← Exported glTF/GLB from Rhino
│   ├── lock_03_morges.glb
│   ├── lock_05_chuv.glb
│   └── lock_07_rennaz.glb
├── backend/
│   ├── agent_server.py         ← Claude Agent SDK WebSocket server
│   └── requirements.txt        ← claude-agent-sdk, websockets
└── README.md
```

## Build Phases

### Phase 1: Multi-Panel Layout (March 20-21)
Restructure `city101_prototypology.html` into the wireframe layout.

**Layout (CSS Grid):**
- **Left panel** (280px): Node list with radar/score cards, "Generate Script" buttons
- **Center** (flex): Main canvas — Leaflet map (existing) with 2D/3D toggle
- **Right panel** (360px): Lock detail panel (currently slide-out → make permanent)
- **Top bar**: Time controls + view-switch toggle
- **Bottom bar**: 5 corridor region tabs (Geneva / La Cote / Lausanne / Lavaux / Riviera)

**Tasks:**
- [ ] Copy `city101_prototypology.html` → `chamber_transport.html`
- [ ] Extract inline data → `chamber_data.js` (prototypology_data.json + prototypology_content.json)
- [ ] Restructure HTML into CSS Grid shell
- [ ] Add D3 radar charts per node (frequency, WCI, staff, catchment, flow)
- [ ] Add corridor region navigation (zoom to bounds presets)

**Reuse:** `city101_maps.js` (bounds presets, color scales), existing particle animation code

### Phase 2: Three.js 3D Viewer (March 22-23)
Add the "Carte corridor 3D" — lock chamber models in browser.

**Tasks:**
- [ ] Export 3 existing Rhino models to .glb via Rhino MCP (`rs.Command("-Export ...")`)
- [ ] Create `chamber_models.js` — Three.js scene, GLTFLoader, OrbitControls
- [ ] Style: dark bg (#0c0c14), gold wireframe + subtle fill, accent lighting
- [ ] Wire toggle button: 2D Map ↔ 3D Corridor (hide/show canvases)
- [ ] Right panel: dedicated small Three.js renderer for selected lock detail
- [ ] Camera presets: corridor overview + per-lock close-ups

**CDN setup (no build step):**
```html
<script type="importmap">
{ "imports": {
    "three": "https://unpkg.com/three@0.160.0/build/three.module.js",
    "three/addons/": "https://unpkg.com/three@0.160.0/examples/jsm/"
}}
</script>
```

**Note:** ES module imports require a local server (`python -m http.server 8000`), not file://.

### Phase 3: MCP Backend (March 24-25)
Connect browser to Rhino/Blender via Claude Agent SDK.

**Tasks:**
- [ ] Create `agent_server.py` — WebSocket server on localhost:8765
- [ ] Configure MCP servers: Rhino (existing) + Blender (`pip install blender-mcp`, install Blender addon)
- [ ] Define 3 agent tools:
  - `generate_lock_chamber(node_id, params)` → runs Rhino script, exports .glb
  - `render_lock_view(node_id, camera)` → Blender render to PNG
  - `export_corridor_model()` → assemble all 7 locks into one scene
- [ ] Browser WebSocket client: "Generate Script" buttons send commands, status indicator
- [ ] Hot-reload: when backend returns new .glb path, Three.js viewer reloads it
- [ ] **Graceful degradation**: app works fully offline with pre-exported static models

**`.mcp.json` update:**
```json
{
  "mcpServers": {
    "rhinomcp": { "command": "uvx", "args": ["rhinomcp"] },
    "blender": { "command": "blender-mcp" }
  }
}
```

### Phase 4: Polish & Presentation (March 26-28)
Make it midterm-ready.

**Tasks:**
- [ ] Visual polish: breathe animation on active nodes, fadeUp entrances
- [ ] Keyboard shortcuts: Space (play/pause), 1-7 (jump to lock), Tab (cycle views)
- [ ] Write 2-4 more Rhino scripts for remaining lock chambers, export to .glb
- [ ] Presentation mode: curated auto-sequence through corridor overview → each lock → flows
- [ ] Lock to 1920x1080 viewport for projection
- [ ] Blender hero renders for PPTX slides (stretch goal)

## What's Realistic for Midterm vs Stretch

| Must-have (March 30) | Stretch goal |
|---|---|
| Multi-panel layout with Leaflet map | Full MCP backend with live generation |
| 3 pre-exported lock models in Three.js | All 7 lock models |
| 2D/3D toggle | Flow particles in 3D |
| Radar charts per node | Blender rendering pipeline |
| Presentation mode | Live "Generate Script" execution |
| Keyboard navigation | Parametric editing from browser |

## Key Risks

| Risk | Mitigation |
|---|---|
| ES modules need server, not file:// | Use `python -m http.server 8000` |
| Rhino glTF export issues | Test 1 simple model first; apply materials in Three.js, not Rhino |
| MCP fails during presentation | Pre-export all models; backend is optional |
| Layout breaks on projector | Lock to 1920x1080 like template_presentation.html |

## Critical Files

| File | Role |
|---|---|
| `output/city101_hub/city101_prototypology.html` | Starting point — restructure into new app |
| `output/city101_hub/prototypology_data.json` | Station/node/flow data to extract |
| `output/city101_hub/prototypology_content.json` | Narrative content for 7 nodes |
| `output/city101_hub/rhino_scripts/*.py` | 3 existing parametric lock scripts |
| `design_system/SPEC.md` | CSS variables, typography, animations |
| `output/transport_pulse_v2/transport_pulse_24h_v2.html` | Reference for advanced panel layout |
| `visualizations/site/city101_maps.js` | Reusable Leaflet module |

## Verification

1. `chamber_transport.html` loads in browser via `python -m http.server`
2. All 5 panels visible, radar charts render, region tabs zoom map
3. 2D/3D toggle switches between Leaflet and Three.js views
4. At least 3 .glb models load and display in Three.js
5. Presentation mode auto-cycles through locks
6. (If Phase 3 done) WebSocket connects to backend, "Generate" button triggers Rhino
