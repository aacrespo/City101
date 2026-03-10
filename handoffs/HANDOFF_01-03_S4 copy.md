# HANDOFF — 01-03 Session 4 (Cairn)

## Last action
Built interactive HTML timeline visualization of rail network evolution along the Geneva–Villeneuve corridor (1855–2025). Researched abandoned/closed rail infrastructure for "horizontal elevator" concept. Parked A02 print layout refinement for tomorrow.

## Current state

### A02 Deliverables (due 03.03)
- **7 print layouts created in QGIS** — see HANDOFF_01-03_S3 for full details
- **PARKED FOR TOMORROW**: Review layouts in Layout Manager, adjust legends, export PDFs
- Narrative document still needed to tie formula + findings + maps together

### Rail History Research — New Thread
Comprehensive research on abandoned/closed rail along the corridor, feeding the "horizontal elevator" concept (Huang loves this per assistant feedback). Key findings:

#### Active Lines Along Corridor
- 1855: Morges–Renens (first section)
- 1856: Extended to Lausanne
- 1858: Geneva–Lausanne mainline complete (three companies close gaps)
- 1861: Simplon line reaches Villeneuve → the 101km corridor is born
- 1877: Lausanne-Ouchy funicular (first in Switzerland)
- 1888: Eaux-Vives–Annemasse (isolated shuttle, not connected to Cornavin)
- 1892–1911: Mountain railways boom (Rochers-de-Naye, MOB, CEV network, Pléiades)

#### Peak Network Density: ~1911
Two new lines open in one year: Clarens–Chailly–Blonay tramway + Blonay–Les Pléiades rack. The Riviera has maximum rail connectivity. Everything after this is contraction.

#### Closed/Abandoned Lines (the dead zones)
1. **Clarens–Chailly–Blonay tramway** (1911–1955, DEMOLISHED)
   - 5.6km metre gauge, mostly on road
   - Lake landing to Blonay via Chailly, Fontanivent, Brent
   - Lakeside section closed 1943, full line closed 31 Dec 1955
   - Tracks torn up. Only Brent viaduct remains visible
   - Replaced by VMCV bus 214

2. **Blonay–Chamby** (regular service 1902–1966, HERITAGE from 1968)
   - 3km metre gauge, steep adhesion
   - Tracks STILL EXIST, owned by MVR
   - Heritage museum railway (weekends May–Oct) — oldest in Switzerland
   - Attempted commercial revival 1998–2000, failed (low ridership)
   - Key horizontal elevator candidate: dormant operable infrastructure

3. **St-Légier–Châtel-St-Denis** (1904–1969, DEMOLISHED)
   - CEV branch line, metre gauge
   - Closed 31 May 1969, tracks dismantled
   - Right-of-way likely still visible in landscape
   - Replaced by VMCV bus 13

4. **6 Ghost Stations on La Côte mainline** (closed 2004, Rail 2000)
   - Founex, Céligny, Crans-près-Céligny, Prangins, Gilly-Bursinel, Perroy
   - Regional service between Allaman and Coppet eliminated entirely
   - Platforms dismantled, third track built for express service
   - Infrastructure ghost in the WCI data (these segments score low)
   - KEY INSIGHT: the corridor sacrificed local accessibility for speed

5. **Eaux-Vives–Annemasse** (isolated shuttle 1888–2012)
   - Technically not abandoned but functionally disconnected for 131 years
   - Bridge abutments for Cornavin connection built in 1888, unused until 2019
   - CEVA project: 1912 contract → 2019 opening (107 years!)

6. **Cornavin–La Praille** (freight only 1949–2002)
   - First CEVA ring section, no passengers for 53 years
   - Passenger service from 2002 (Lancy-Pont-Rouge)

#### The Horizontal Elevator Argument
The most architecturally provocative sites:
- **La Côte ghost stations**: on the mainline, third track exists, platforms removed for express trains. An on-demand autonomous module on this track = re-activating exactly the service that was killed. Infrastructure exists, was just deprioritized.
- **Blonay–Chamby**: dormant tracks, proven operable, failed commercial revival. What if not a scheduled train but an on-demand pod?
- **St-Légier–Châtel-St-Denis right-of-way**: erased but route still legible. Could be reimagined as light autonomous transit.

### Visualization Created
- `rail_history.html` — interactive HTML timeline
- Scrubable slider + play button animating 1855–2025
- SVG schematic map showing lines appearing (green), closing (red), becoming heritage (gold), demolished (dashed grey)
- Ghost stations marked with ✕ after 2004
- Event cards with context for each change
- Running stats: active lines, closed lines, ghost stations, total km

## Key Insight
**The network peaks in 1911 and contracts from the 1940s onward.** The Riviera (Vevey–Montreux) loses the most — three entire lines gone. Then in 2004, La Côte loses six stations. The corridor has been trading local connectivity for express speed for 80 years. The "horizontal elevator" reverses this trade: using existing or dormant infrastructure to restore local access without slowing the express network.

## Open threads
- [ ] **TOMORROW**: Finalize A02 layouts (legend cleanup, PDF export)
- [ ] **TOMORROW**: Write narrative document for A02
- [ ] Map the ghost station locations + abandoned right-of-ways in QGIS
- [ ] Overlay abandoned rail with WCI scores to quantify the connectivity loss
- [ ] Swisstopo historical maps for tracing demolished right-of-ways
- [ ] Zurich comparison (still pending)
- [ ] Point cloud sections for high-potential sites

## Data sources this session
- Wikipedia: Lausanne–Geneva railway, Simplon Railway, CEV, Blonay–Chamby, CCB, CEVA
- blonay-chamby.ch museum history
- mob.ch company history
- e-periodica.ch (1913 engineering article on CCB)
- histoireferroviaire.wordpress.com (Swiss railway history blog)
