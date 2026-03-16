# Wave 2: Script Testing via Rhino MCP

**Branch:** `andrea/prototypology-v2` (confirm you're on it)
**Rhino needed:** YES — open Rhino before starting
**Duration:** ~1 session
**Commit when done:** `[MODEL] Verify 3 lock scripts via Rhino MCP`

---

## What to do

Use `/modeler` role. Test the 3 existing Rhino Python scripts via MCP to verify they produce correct geometry.

---

## Pre-flight

1. Confirm Rhino is open and MCP is connected (try `get_document_summary`)
2. Read the modeling workflow: `workflows/rhino-modeling.md`
3. Read LOG conventions: `00_Workflow_v04.md` Section 3.2
4. Read the lock concepts: `output/city101_hub/prototypology_content.json`

---

## Scripts to test

Run each via `execute_rhinoscript_python_code`:

1. `output/city101_hub/rhino_scripts/lock_03_morges_temporal.py`
2. `output/city101_hub/rhino_scripts/lock_05_chuv_gradient.py`
3. `output/city101_hub/rhino_scripts/lock_07_rennaz_bridge.py`

---

## For each script

1. **Read the script first** — understand the spatial plan in the docstring
2. **Run it via MCP**
3. **If errors:** document the error, diagnose, fix, re-run
   - Common issues: coordinate system, missing layers, syntax differences
   - Save fixes as new files (don't overwrite originals): `lock_03_morges_temporal_v2.py`
4. **After successful run:**
   - `capture_viewport` from 4 angles (perspective, top, front, side)
   - `get_document_summary` — list all layers created
   - Count objects per layer
   - Verify bounding box matches the spatial plan dimensions
5. **Check LOG level** — scripts claim LOG 200-300. Verify:
   - Volumes present? (LOG 200 ✓)
   - Floor plates? (LOG 200 ✓)
   - Structural elements (columns)? (LOG 300 ✓)
   - Openings? (LOG 300 ✓)

---

## Output

Write a test log to `output/city101_hub/script_test_log.md` with:

For each script:
- Success/fail
- Errors encountered and fixes applied
- Screenshot descriptions (4 views)
- Layer and object inventory
- LOG compliance check (what's present at which LOG level)
- Any issues the modeler should know about for Wave 4

---

## After all 3 scripts tested

1. Review the test log — are there patterns in the errors?
2. Note any geometry that needs fixing before LOG upgrade (Wave 4)
3. Commit: `[MODEL] Verify 3 lock scripts via Rhino MCP`
4. Push branch if not already pushed

---

## Reference files
- Modeling workflow: `workflows/rhino-modeling.md`
- LOG levels: `00_Workflow_v04.md` Section 3.2
- Lock concepts: `output/city101_hub/prototypology_content.json`
- LOG checklist: `workflows/log-400-checklist.md`
