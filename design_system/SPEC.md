# Design System v3 — "Still On The Line"

**Status**: Active — see `brand_guide.html` for interactive reference.

---

## Brand Assets

| File | Purpose |
|------|---------|
| `brand_guide.html` | Interactive brand guide — colors, type, components, examples |
| `still_on_the_line_logo.svg` | Logo/wordmark SVG with dark, light, compact, and monogram variants |
| `template_presentation.html` | 1920×1080 presentation template with 6 slide types |
| `template_map_layout.html` | Map header/footer overlay template with print support |

## Brand Name

**Still On The Line** — the project title. Three meanings:
1. **Still on the train line** — the 101 km Geneva–Villeneuve rail corridor
2. **Still connected** — the question of whether these places remain linked
3. **Still (motionless)** — the paradox of stopping within a transit corridor

**City101** is the studio theme, not our project name. Use "Still On The Line" in all deliverables.

## Logo

The wordmark stacks two voices:
- **STILL** in Instrument Serif — the narrative pause
- **ON THE LINE** in DM Mono — the measured infrastructure

The gold line with station dots runs beneath — the corridor itself, always present.

### Variants
| Variant | Use case |
|---------|----------|
| Dark (on `#0c0c14`) | Default — presentations, site, diagrams |
| Light (on `#f5f3ee`) | Print, light backgrounds |
| Compact (single-line) | Navigation bars, headers, small spaces |
| Monogram **S\|L** | Favicons, badges, map markers (min 24×24px) |

### Clear space
Minimum clear space = height of "S" on all sides.

## Palette

| Role | Hex | Where used |
|------|-----|------------|
| Background | `#0c0c14` | Site, QGIS page bg, diagrams |
| Gold accent | `#c9a84c` | Headings, data highlights, train lines, primary brand color |
| Text primary | `#e8e6e1` | Body text, labels |
| Text muted | `#9a9690` | Secondary info, captions (WCAG AA compliant) |
| Copper | `#b87a56` | Secondary warm accent, S-Bahn lines |
| Teal | `#5b8fa8` | Cool complement, Lake Léman association |
| Surface | `rgba(255,255,255,0.04)` | Glass panel backgrounds |
| Gold border | `rgba(201,168,76,0.12)` | Subtle borders on panels and cards |
| Data layer | `#ffffff` at varying opacity | Points, trails on dark bg |
| WCI gradient | `#c45d4a` → `#c9a84c` → `#5a9e6f` | WCI maps (0 → 0.65+) |
| Frequency gradient | red → green | Transit maps (0 → 16+ trains/hr) |

### Semantic Colors

| Role | Hex |
|------|-----|
| Success | `#5a9e6f` |
| Warning | `#c9a84c` |
| Error | `#c45d4a` |

## Typography

| Role | Font | Fallback | Usage |
|------|------|----------|-------|
| Display / headings | Instrument Serif | serif | Narrative voice — titles, pull quotes, "STILL" |
| Body | DM Sans (400/500/700) | sans-serif | Explanatory — body text, labels, UI |
| Data / code / mono | DM Mono (400/500) | monospace | Measurement — timestamps, coordinates, metrics, "ON THE LINE" |

## CSS Variables

```css
:root {
  --bg: #0c0c14;
  --bg-elevated: #12121c;
  --surface: rgba(255,255,255,0.04);
  --gold: #c9a84c;
  --gold-dim: rgba(201,168,76,0.12);
  --text: #e8e6e1;
  --text-muted: #9a9690;
  --copper: #b87a56;
  --teal: #5b8fa8;
  --font-display: 'Instrument Serif', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}
```

All UI elements (panels, legends, controls, overlays) reference these variables. To retheme, swap this block. Map canvas content (basemap tiles, data points) does NOT use CSS variables.

## QGIS

- Page background: rgb(12, 12, 20)
- Labels: DM Sans, white, dark halo
- Print exports: 300 DPI PDF + 150 DPI PNG
- Basemap: dark — no standard OSM tiles

## Leaflet / Web Maps

- Basemap tiles: CartoDB Dark Matter
- Accent color for lines/highlights: #c9a84c
- Popup styling: dark bg, light text, DM Sans
- Use `template_map_layout.html` for branded header/footer overlay
- Use IntersectionObserver for lazy loading

## Presentations

- Use `template_presentation.html` as starting point
- 1920×1080 fixed viewport with auto-scale
- 6 slide types: title, split, data, grid, quote, map
- Keyboard navigation (arrow keys, space, home/end)
- Always include datum lines (top/bottom branded bars)
- Footer brand: "STILL" + "ON THE LINE" (not City101)

## Key Animations

```css
/* Breathing pulse — the corridor's rhythm */
@keyframes breathe {
  0%, 100% { opacity: 0.4; }
  50% { opacity: 1; }
}
/* duration: 4s · easing: ease-in-out · infinite */

/* Fade-up entrance */
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
/* duration: 0.6s · stagger: 0.1s per element */
```
