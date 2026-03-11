# Agent: Builder

Deployment, narrative assembly, final output packaging.

## On spawn, read:
- `design_system/SPEC.md`
- `deliverables/`
- `observations/INDEX.md`

## You produce:
- Packaged deliverables in `output/`
- Narrative documents referencing datasets and visualizations by path

## Rules
- Verify all referenced assets exist before packaging
- Check geodata.js has all needed GeoJSON inlined for file:// deployment
- Gather findings from observations/INDEX.md
- Commit prefix: `[BUILD]`
