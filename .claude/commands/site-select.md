# Skill: Site Select

Analyze a region and select the optimal location for an architectural intervention.

## Input
Argument: a region or general location (e.g., "Morges area", "between Vevey and Montreux") and optionally a design intent (e.g., "temporal lock for night workers", "vertical connector").

If no region is given, ask.

## On start, read:
- `.claude/agents/site-selector.md` — full agent protocol and decision criteria
- `output/city101_hub/prototypology_content.json` — 7 lock node definitions
- `geodata/config.json` — reference points and coordinate system

## Process

Follow the site-selector agent protocol:

1. **Understand the brief** — what lock type, what flows, what temporal need
2. **Load corridor data** — WCI, break points, TWCI, modal diversity for stations in the region
3. **Evaluate 2-3 candidate locations** — score each against flow convergence, temporal fit, break severity, accessibility, terrain
4. **Select the best site** — define center point (LV95), bbox, orientation rationale
5. **Run extraction** — execute `geodata/scripts/extract_site.py` with the chosen coordinates
6. **Report** — present the selection with justification and cite data sources

## Output
- Site selection report with coordinates and justification
- Extracted site data in `geodata/sites/{name}/` (terrain, buildings, infrastructure, imagery)
- The exact command to import into Rhino: `/import-terrain {name}`

## Example prompts
- "Find the best site for a temporal lock near Morges"
- "Select a location for a vertical connector between Vevey and Montreux"
- "Where should we place a cargo lock in the Geneva industrial belt?"

## Troubleshooting
- If extraction fails, check `python geodata/scripts/find_drive.py` can find the shared drive
- If coordinates seem wrong, verify against reference points in `geodata/config.json`
- Use `--skip-infrastructure` if GeoPackage read is too slow from network drive
