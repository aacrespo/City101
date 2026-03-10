# Workflow: Data Verification

## Objective
Verify a dataset meets quality standards before promoting from `output/` to `datasets/`.

## When to use
- Before promoting any file from `output/` to `datasets/`
- When `/verify-data` is invoked
- After any agent team produces output

## Required inputs
- Path to the CSV file to verify
- Expected row count (approximate is fine)

## Steps
1. **Run `tools/data/verify_dataset.py`** on the target file:
   ```
   python tools/data/verify_dataset.py path/to/file.csv
   ```
2. **Review the output**:
   - Row count — does it match expectations?
   - Required columns present (ID, name, coordinates)?
   - Coordinate ranges valid (WGS84: lat 46.1–46.6, lon 6.0–7.1)?
   - No nulls in required fields?
   - No duplicate IDs?
   - Source attribution present?
3. **Manual spot-check**: look at 3-5 random rows — do values make sense?
4. **If PASS**: recommend promoting to `datasets/[subfolder]/` and update `datasets/INVENTORY.md`
5. **If FAIL**: report specific issues. Fix and re-verify, or flag for human review.

## Expected output
- PASS/FAIL summary with details
- If promoting: updated `datasets/INVENTORY.md` entry

## Edge cases
- File has coordinates in LV95 only: not a failure, but flag that WGS84 column should be added via `tools/data/convert_coordinates.py`
- File has extra columns beyond requirements: fine — we collect rich, export lean
- Row count is 0: automatic FAIL — empty datasets don't get promoted

## History
- 10 March 2026: Created (v7 repo setup)
