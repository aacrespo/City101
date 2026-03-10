# Workflow: Data Collection

## Objective
Collect data from an API source and produce a verified, staged dataset.

## When to use
When fetching new data from any API (transport.opendata.ch, Google Places, sharedmobility.ch, data.geo.admin.ch, Overpass/OSM, etc.).

## Required inputs
- API endpoint or source identified
- Clear definition of what data we need and why

## Steps
1. **Check LEARNINGS.md** for known issues with this API (rate limits, parameter gotchas, etc.)
2. **Check `tools/data/`** for an existing fetch script. If one exists, use it.
3. **If no tool exists**: write a self-contained Python script. Follow the pattern: fetch → filter → process → match → write output → print summary.
4. **Rate limiting**: respect API limits (transport.opendata.ch: 0.35s between calls; others: check docs)
5. **Run the script** — output goes to `output/`, never directly to `datasets/`
6. **Verify output** using `workflows/data-verification.md`
7. **Print comprehensive summary**: sources queried, row counts, unexpected findings, leads to follow
8. **Promote to `datasets/`** only after verification and approval

## Expected output
- CSV file in `output/` with: unique ID, name, coordinates (WGS84 + LV95), source, fetch date, all metadata
- Summary printed to stdout

## Edge cases
- API returns empty results: log it, check parameters, try alternative query. Don't write empty files.
- API rate-limited or down: back off, retry with delay. Log the issue in LEARNINGS.md.
- Data has coordinates in wrong CRS: use `tools/data/convert_coordinates.py` to add the missing system.

## History
- 10 March 2026: Created (v7 repo setup)
