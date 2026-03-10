# HANDOFF — 17-02 Session 6

## Last action
Verified new network domains are live, ran Script 3 (Open Charge Map enrichment + reviews). Output: 53-column `city101_ev_charging_ENRICHED_v3.csv` + `city101_ev_charging_REVIEWS.csv` (7 reviews). Google Places enrichment blocked — no API key on personal account.

## Current state
- **ENRICHED_v3.csv** — 194 rows, 53 columns (34 from v2 + 19 OCM columns)
- **REVIEWS.csv** — 7 reviews from OpenChargeMap (structure ready for Google reviews to be appended)
- **Script saved**: `enrich_ocm.py` — re-runnable, fetches OCM live, matches by proximity (200m threshold)
- **OCM API key**: `23617e07-95e4-4666-b1f6-f4dfcd6a8e64` (free tier, working)

### Network domain status (verified this session)
| Domain | Status | Notes |
|--------|--------|-------|
| api.openchargemap.io | ✅ Working | Needs API key (have it) |
| chargemap.com | ✅ Working | Web scraping possible |
| maps.googleapis.com | ✅ Working | Needs Google API key (don't have on personal account) |
| plugshare.com | ❌ Failing | Anti-bot protection, connection drops |

### OCM enrichment results
- OCM stations in corridor: 172 (vs our 194 — different coverage)
- Matched: 29/194 (14%) — OCM Swiss coverage is thin
- Reviews collected: 7 (sparse but structure ready)
- Gap fills: 8 power_kw + 2 operator
- Key OCM operators: eborn (43), Tesla (37) — lots of French-border contamination in bounding box

### CSV column progression
| Version | Columns | Source |
|---------|---------|--------|
| MERGED (original) | 16 | Google Places + OSM |
| ENRICHED | 27 | + DIEMO (Script 1) |
| ENRICHED_v2 | 34 | + distances + context (Script 2) |
| ENRICHED_v3 | 53 | + OCM (Script 3) |

### What's NOT yet done
**Needs Google API key (team account only):**
- google_rating, google_review_count, review text
- This is where the real review harvest is — the OCM 7 reviews vs potentially hundreds from Google

**Still missing from proposed schema:**
- mobile_signal, floor_level (truly manual)
- parking_fee, parking_max_hours (partial from reviews)
- nearby_amenities (OSM POI queries possible now)
- sentiment_tags (derivable once reviews collected)

## Open threads — PRIORITY ORDER
1. **Second dataset for A.01** (due 23.02) — STILL MISSING. Need one "straightforward" dataset. Candidates: public transport stops, lakeside access points, parking structures, public WiFi. All gettable from OSM MCP without API keys.
2. **Google Places enrichment** — needs API key from team account. When Andrea gets back on team account, grab the key and run enrichment for ratings + reviews.
3. **Spot-check classifications** — 59 unknown location_types, 39 unknown dwell_contexts need human review
4. **Pin-up map outputs** — need QGIS map compositions for Monday 23.02
5. **Load ENRICHED_v3 in QGIS** — replace old layer, restyle with new fields
6. **OSM nearby amenities** — can do now via OSM MCP, no API needed

## Key decisions made (cumulative)
- Framing: "flow of people" not energy (energy = Siméon's territory)
- EV charging analyzed through human experience lens
- LV95 / EPSG:2056 as working coordinate system
- LOG/LOI/LOD framework adopted (see 00_Workflow_v02.md)
- LOI principle: "Work rich, export lean"
- Two-CSV architecture: stations + reviews (reviews started — 7 from OCM)
- DIEMO as primary enrichment source for technical data ✓
- OCM as secondary enrichment source ✓ (thin coverage but useful)
- Google Places = primary source for ratings + reviews (pending key)
- Monolithic script pattern: fetch → process → match → write → summary
- Original MERGED.csv preserved as raw source of truth

## Technical notes
- OCM API key: `23617e07-95e4-4666-b1f6-f4dfcd6a8e64`
- OCM bounding box: `(46.10,6.05),(46.55,6.95)`
- OCM match threshold: 200m haversine
- OCM has different operator taxonomy than DIEMO (eborn, Power Dot = French operators near border)
- Scripts: `enrich_v2.py` (DIEMO), `enrich_distances_context.py` (distances), `enrich_ocm.py` (OCM)
- Team account rate limit resets ~1 hour from now (as of session end)

## Data sources (this session)
- Open Charge Map API: api.openchargemap.io (17.02.26) — 172 stations in corridor, 7 user reviews
