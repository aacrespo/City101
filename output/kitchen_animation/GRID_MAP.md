# Kitchen Animation — Grid Reference

Kitchen: 10 columns (x: 0–9) × 8 rows (y: 0–7)
Each cell = 1 grid unit. Characters sit at cell centers (x+0.5, y+0.5).

## Coordinate system
Use **(x, y)** format: x = column (left→right), y = row (top→bottom).
Example: **(3, 4)** = column 3, row 4 = center of H-island crossbar.

## Scene 1 + 2 Grid (same layout — pass present from Scene 1)
```
     x: 0    1    2    3    4    5    6    7    8    9
   ┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
y=0│ CT │ CT │ CT │ ST │ ST │ SK │ CT │ CT │    │ FR │  ← Back wall
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=1│    │    │    │    │    │    │    │ PP │    │    │  ← Pass
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=2│    │    │    │    │    │    │    │ PP │    │    │  ← Pass
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=3│    │    │ CT │ CT │ CT │ CT │    │ ▓▓ │    │ CT │  ← Island + PASS WINDOW
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=4│    │    │    │ CT │ CT │    │    │ ▓▓ │    │ CT │  ← Crossbar + PASS WINDOW
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=5│    │    │ CT │ CT │ CT │ CT │    │ PP │    │ CT │  ← Island + Pass
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=6│    │    │    │    │    │    │ LB │ PP │    │    │  ← Logbook
   ├────┼────┼────┼────┼────┼────┼────┼────┼────┼────┤
y=7│    │    │    │    │    │    │    │    │    │    │  ← Open
   └────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘

CT = counter  ST = stove  SK = sink  FR = fridge
PP = pass counter (blocked)  ▓▓ = pass window (OPEN — walkable)
LB = logbook counter
```

## Key positions (Scene 2)
| What | Position (x,y) | Cell center |
|------|---------------|-------------|
| Claude start | (6, 2) | (6.5, 2.5) |
| Claude cooking | (2-4, 1) | (x.5, 1.5) |
| Claude home | (5, 2) | (5.5, 2.5) |
| Claude backpack phase | (1, 3) | (1.5, 3.5) |
| Claude logbook phase | (5, 6) | (5.5, 6.5) |
| User | (8, 4) | (8.5, 4.5) |
| Books/archibase | (2, 3) | on counter |
| Index card box | (2, 3) | on counter |
| Logbook | (6, 6) | on counter |

## How to reference
- **Grid position**: "(x, y)" e.g. "(3, 4)"
- **Scene time**: "at st=15" or "between st 18-21"
- **Phase**: "during 2b" or "in phase 2c"

## Frame reference
The animation runs at ~60fps. Key scene timestamps:
- **Scene 1**: 0–38s (phases 1a→1e)
- **Scene 2**: 0–44s (phases 2a→2e)

| Phase | Scene time | What happens |
|-------|-----------|-------------|
| 2a-setup | 0–3s | Pass visible, user appears |
| 2a-loop | 3–18s | 3 order cycles |
| 2b | 18–21s | Backpack highlight, Claude at (1,3) |
| 2c | 21–28s | Archibase book thrown to (2,3) |
| 2d-CAG | 28–31s | 5 books stack on (2,3) |
| 2d-RAG | 31–35s | Index cards replace books |
| 2e | 35–44s | Logbook overlay, Claude at (5,6) |
