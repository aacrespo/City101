# Kitchen Animation v7 — Grid Reference (Overcooked Style)

Kitchen: **14 columns (col: 0–13) × 12 rows (row: 0–11)**
Each cell = 1 grid unit. Characters sit at cell centers (col+0.5, row+0.5).

## Coordinate system
Use **(col, row)** format: col = column (left→right), row = row (top→bottom).
Example: **(5, 5)** = column 5, row 5 = H-island crossbar.

**Debug overlay**: Press **G** to toggle the grid overlay with color-coded cells and coordinates.

## Grid Layout (v7 — 14×12)

```
     col: 0    1    2    3    4    5    6    7    8    9   10   11   12   13
    ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
r=0 │WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│  ← Back wall
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=1 │WALL│    │ CT │ ST │ ST │ SK │ SK │    │ CT │ CT │    │ FR │    │WALL│  ← Back counters
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=2 │DOOR│    │    │    │    │    │    │    │    │    │    │    │    │WALL│  ← Top aisle + KITCHEN door
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=3 │    │    │    │    │    │    │    │    │    │    │    │ PP │    │WALL│  ← Open + pass start
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=4 │    │    │    │ CT │ CT │ CT │ CT │    │    │    │    │ PP │    │WALL│  ← Island top
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=5 │    │    │    │    │    │ CT │    │    │    │    │    │ PW │    │WALL│  ← Crossbar + PASS WINDOW
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=6 │    │    │    │ CT │ CT │ CT │ CT │    │    │    │    │ PW │    │WALL│  ← Island bottom + PASS WINDOW
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=7 │    │    │    │    │    │    │    │    │    │    │    │ PP │    │WALL│  ← Open + pass end
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=8 │    │    │    │    │    │    │    │    │ LB │    │    │ PP │    │WALL│  ← Logbook
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=9 │    │    │    │    │    │    │    │    │    │    │    │    │    │WALL│  ← Open floor
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=10│DOOR│    │    │    │    │    │    │    │    │    │    │    │    │WALL│  ← Bottom aisle + STAFF door
    ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
r=11│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│WALL│  ← Front wall
    └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘

CT = counter    ST = stove    SK = sink    FR = fridge
PP = pass counter (blocked)   PW = pass window (serves food, not walkable)
LB = logbook counter   DOOR = entry point   WALL = solid wall
```

## Key named positions

| Name | Position (col, row) | Notes |
|------|---------------------|-------|
| Kitchen door | (0, 2) | Where Claude enters in Scene 1 |
| Staff door | (0, 10) | Specialist doors for Scene 4 brigade |
| Stove left | (3, 1) | Cooking station |
| Stove right | (4, 1) | Cooking station |
| Sink left | (5, 1) | Washing |
| Sink right | (6, 1) | Washing |
| Back counter left | (2, 1) | Prep counter |
| Back counter right | (8-9, 1) | Prep counter |
| Fridge | (11, 1) | Cold storage |
| Island top row | (3-6, 4) | Upper island counter |
| Island crossbar | (5, 5) | Center connector |
| Island bottom row | (3-6, 6) | Lower island counter |
| Pass counter (solid) | (11, 3-4) and (11, 7-8) | Blocked pass sections |
| Pass windows | (11, 5-6) | Where food is served to user |
| User position | (12, 5) | Dining side of pass |
| Logbook | (8, 8) | Git reference counter |
| Claude home | (7, 3) | Default idle position |
| Archibase station | (4, 4) | Where big book lands (on island) |

## Movement rules

### Walkable cells
All cells marked as empty in the grid + DOOR cells. Characters move tile-to-tile using A* pathfinding (4-directional).

### Blocked cells
- WALL (rows 0, 11; col 0 except doors; col 13)
- All furniture: CT, ST, SK, FR, LB, PP, PW

### Margins
Characters sit at **cell centers** (col+0.5, row+0.5), creating a natural half-cell gap from adjacent furniture. No diagonal squeeze allowed between two blocked cells.

### Interaction zones (stand here to USE an object)

| Object | Stand at | Face |
|--------|----------|------|
| Stove (3,1) | (3,2) | up |
| Stove (4,1) | (4,2) | up |
| Sink (5,1) | (5,2) | up |
| Sink (6,1) | (6,2) | up |
| Fridge (11,1) | (10,2) | up-right |
| Back counters (8-9,1) | (8-9,2) | up |
| Island top (3-6,4) | (3-6,3) or (2,4) or (7,4) | toward counter |
| Crossbar (5,5) | (4,5) or (6,5) | toward counter |
| Island bottom (3-6,6) | (3-6,7) or (2,6) or (7,6) | toward counter |
| Pass window (11,5) | (10,5) | right |
| Pass window (11,6) | (10,6) | right |
| Logbook (8,8) | (7,8) or (8,7) or (9,8) | toward counter |

## How to reference

- **Position**: "(col, row)" e.g. "(5, 5)" = island crossbar
- **Scene time**: "scene 2 at 12s" or "at st=12"
- **Phase**: "phase 2c" or "during 2c"
- **Combined**: "Claude at (3, 2) during phase 2a at st=5"

## Timeline reference

| Scene | Name | Duration | Cumulative | Phases |
|-------|------|----------|------------|--------|
| 1 | Entering the Kitchen | 38s | 0:38 | 1a(0-6) 1b(6-14) 1c(14-26) 1d(26-30) 1e(30-38) |
| 2 | The Pass | 44s | 1:22 | 2a(0-18) 2b(18-21) 2c(21-28) 2d(28-35) 2e(35-44) |
| 3 | The Logbook | 30s | 1:52 | 3a(0-10) 3b(10-20) 3c(20-30) |
| 4 | The Brigade | 35s | 2:27 | 4a(0-10) 4b(10-20) 4c(20-35) |
| 5 | Four Pillars | 30s | 2:57 | 5a(0-7) 5b(7-14) 5c(14-22) 5d(22-30) |
| 6 | The Full Kitchen | 18s | 3:15 | 6a(0-12) 6b(12-18) |

**Total: ~3:15**

### Scene 1 phases

| Phase | Time | What happens | Claude position |
|-------|------|--------------|-----------------|
| 1a | 0–6s | Empty dim kitchen, grey Claude approaches | (-1,2) → (1,2) |
| 1b | 6–14s | Picks up scrolls from shelf | (1,2) |
| 1c | 14–26s | Opens CLAUDE.md map + .claude/ blueprint overlays | (1,2) |
| 1d | 26–30s | Grey → gold color transition, backpack appears | (1,2) |
| 1e | 30–38s | Kitchen furnishes itself, Claude walks to station | (1,2) → (7,3) |

### Scene 2 phases

| Phase | Time | What happens | Claude position |
|-------|------|--------------|-----------------|
| 2a | 0–18s | 3 order cycles: cook → plate → serve through pass | (7,3) → (3,2) → (10,5) → (7,5) loop |
| 2b | 18–21s | Backpack grows, context weight visualized | (5,5) |
| 2c | 21–28s | Archibase book thrown from user, caught by Claude | (5,5) |
| 2d-CAG | 28–31.5s | 5 books stacked on island (pre-loaded knowledge) | near (4,4) |
| 2d-RAG | 31.5–35s | Index card box replaces books (on-demand fetch) | near (4,4) |
| 2e | 35–44s | Logbook glows, Claude moves to examine it | (7,8) |

## Controls

| Control | Action |
|---------|--------|
| **Space** | Play / Pause |
| **← →** | Skip ±3 seconds |
| **↑ ↓** | Previous / Next scene |
| **G** | Toggle grid overlay |
| Speed button | Cycle 0.5x / 1x / 1.5x / 2x |
| Timeline bar | Click to jump to any point |
