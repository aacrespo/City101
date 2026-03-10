# Working Continuity Index (WCI) — City101 Corridor
**Generated:** 2026-03-01 | **Assignment:** A02 Data Synchronicity

---

## Formula

```
WCI = 0.30 × transit_score
    + 0.25 × workspace_density
    + 0.20 × temporal_coverage
    + 0.15 × connectivity_score
    + 0.10 × mobility_score
```

All sub-scores are min-max normalized (0–1) across the 49 corridor segments.

### Weight Justification

| Weight | Component | Rationale |
|--------|-----------|-----------|
| 0.30 | **Transit score** | Train frequency is the backbone of corridor traversal. A knowledge worker's ability to move continuously depends first on transport availability. The 42x variation (Lausanne 28.5 tr/hr vs Bossiere 2.0) is the primary determinant of working continuity. |
| 0.25 | **Workspace density** | Physical places to work (coworking, cafes, libraries) are the second requirement. Without a desk, power, and a seat, transit connectivity is irrelevant. |
| 0.20 | **Temporal coverage** | Opening hours determine *when* continuity is possible. A workspace that closes at 5pm breaks the evening commuter's flow. 24h access, early opening, and weekend availability extend the temporal window. |
| 0.15 | **Connectivity** | WiFi quality and 5G coverage enable the actual work. Weighted lower because mobile hotspots can partially substitute, but public WiFi and strong cellular are still necessary for reliable sessions. |
| 0.10 | **Mobility score** | Shared mobility (e-bikes, scooters, carshare) provides last-mile access from station to workspace. Important but supplementary — most corridor movement is rail-based. |

---

## Top 5 Segments (Highest WCI)

| Rank | Station | WCI | Transit | Workspace | Temporal | Connect. | Mobility | Workspaces | WiFi |
|------|---------|-----|---------|-----------|----------|----------|----------|------------|------|
| 1 | Genève | 0.6431 | 0.30 | 1.00 | 0.50 | 0.69 | 1.00 | 13 | 13 |
| 2 | Lausanne | 0.5536 | 0.34 | 0.85 | 0.47 | 0.72 | 0.37 | 11 | 8 |
| 3 | Vernier, Blandonnet | 0.4647 | 1.00 | 0.00 | 0.00 | 0.80 | 0.45 | 0 | 2 |
| 4 | Vevey | 0.4011 | 0.24 | 0.54 | 0.46 | 0.60 | 0.14 | 7 | 7 |
| 5 | Lausanne-Flon | 0.3951 | 0.05 | 0.54 | 0.44 | 0.64 | 0.62 | 7 | 10 |

## Bottom 5 Segments (Lowest WCI)

| Rank | Station | WCI | Transit | Workspace | Temporal | Connect. | Mobility | Workspaces | WiFi |
|------|---------|-----|---------|-----------|----------|----------|----------|------------|------|
| 45 | Founex, est | 0.0135 | 0.04 | 0.00 | 0.00 | 0.00 | 0.01 | 0 | 0 |
| 46 | Rivaz | 0.0128 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| 47 | Perroy, Couronnette | 0.0107 | 0.04 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |
| 48 | Territet | 0.0081 | 0.02 | 0.00 | 0.00 | 0.00 | 0.01 | 0 | 0 |
| 49 | St-Saphorin (Lavaux), gare | 0.0003 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0 | 0 |

---

## Geographic Patterns

### Cluster Analysis

| Cluster | Stations | Avg WCI | Interpretation |
|---------|----------|---------|----------------|
| **Geneva** (lon < 6.3) | 18 | 0.1830 | Dense urban core with strong transit, multiple coworking spaces, and full 5G coverage. The corridor's western anchor. |
| **La Cote** (6.3–6.5) | 6 | 0.0904 | Suburban commuter belt. Moderate transit but few dedicated workspaces. Working continuity depends on train frequency alone. |
| **Lausanne area** (6.5–6.7) | 9 | 0.2118 | Second urban pole. University presence (EPFL/UNIL) boosts workspace and connectivity. Rivals Geneva in WCI. |
| **Lavaux** (6.7–6.85) | 8 | 0.0754 | The critical gap. UNESCO protection actively resists infrastructure. Minimal workspaces, low frequency, poor connectivity. This is where working continuity breaks. |
| **Riviera** (> 6.85) | 8 | 0.1368 | Montreux-Villeneuve stretch. Tourism-oriented, moderate transit, few work-focused spaces. Partial recovery from Lavaux gap. |

### Key Insight: Where Working Continuity Breaks

The corridor's working continuity is not a gradient — it is **bimodal with a fracture**.

The Geneva and Lausanne poles sustain continuous work sessions: high-frequency trains (25+ per hour), abundant workspaces (coworking, cafes, libraries), 24h temporal access, strong 5G connectivity, and dense shared mobility. A knowledge worker moving through these zones barely notices transitions.

**The Lavaux gap (km ~60–75) is an absolute break.** Train frequency drops below 3/hr (20+ minute waits), workspaces vanish, WiFi coverage disappears, and shared mobility is absent. The UNESCO-protected vineyard landscape actively resists the infrastructure that working continuity requires. This is not a gradual decline — it is a cliff.

The Riviera (Montreux-Villeneuve) partially recovers but never matches the urban poles. Its tourism orientation means workspaces exist but with limited hours and work-oriented amenities.

**The architectural question:** Can the Lavaux gap be bridged without violating its protected character? Or is the fracture itself a feature — a designed disconnection that forces the corridor to be two cities, not one?

---

## Distribution Statistics

| Metric | Value |
|--------|-------|
| Total segments | 49 |
| WCI range | 0.0003 – 0.6431 |
| WCI mean | 0.1518 |
| WCI median | 0.0844 |
| Segments with workspace | 19 / 49 |
| Segments with WiFi | 23 / 49 |
| Total workspaces assigned | 68 |
| Total WiFi spots assigned | 81 |
| Total EV chargers assigned | 194 |
| Total shared mobility assigned | 2062 |
| Total cell towers assigned | 3218 |
