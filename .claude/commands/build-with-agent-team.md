# Build with Agent Team

Spawn subagents in parallel for build tasks (maps, visualizations, processing).

## How it works
1. **Define the build targets** — what are we producing?
2. **Assign one target per agent** — each gets a focused build task
3. **Each agent**:
   - Reads CLAUDE.md (automatic)
   - Reads design_system/SPEC.md for visual identity
   - Reads relevant datasets from datasets/
   - Builds its assigned output
   - Writes to `output/` (staging)
   - Prints summary of what was built
4. **Lead agent (you)** reviews output quality and design system compliance
5. **Promote verified output** to final location (visualizations/, maps/, etc.)

## Rules
- Agents write to `output/` only
- All visualizations must follow design_system/SPEC.md (dark theme, correct fonts, CSS variables)
- Maps must use correct CRS (EPSG:2056 for QGIS, WGS84 for Leaflet)
- Use tools from `tools/maps/` for base layers and design system application
- Verify all referenced data files exist before building

## Template for spawning
```
Agent task: [specific build target]
Write output to: output/[descriptive_name]
Design reference: design_system/SPEC.md
Data sources: [list datasets to use]
```
