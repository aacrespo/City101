# Design System — City101 "Still on the Line"

**Status**: Current prototypes — not locked. Swap palette when concept lands.

---

## Palette

| Role | Hex | Where used |
|------|-----|------------|
| Background | `#0a0a0f` | Site, QGIS page bg (rgb 10,10,15), diagrams |
| Gold accent | `#c9a84c` | Headings, data highlights, train lines on web maps |
| Text primary | `#e8e6e1` | Body text, labels |
| Text muted | `#8a8880` | Secondary info, captions |
| Data layer | `#ffffff` at varying opacity | Points, trails on dark bg |
| WCI gradient | red → yellow → green | WCI maps (0 → 0.65+) |
| Frequency gradient | red → green | Transit maps (0 → 16+ trains/hr) |

## Typography

| Role | Font | Fallback |
|------|------|----------|
| Display / headings | Instrument Serif | serif |
| Body | DM Sans | sans-serif |
| Data / code / mono | DM Mono | monospace |

## CSS Variables

```css
:root {
  --chrome-bg: #0a0a0f;
  --chrome-text: #e8e6e1;
  --chrome-accent: #c9a84c;
  --chrome-muted: #8a8880;
  --font-display: 'Instrument Serif', serif;
  --font-body: 'DM Sans', sans-serif;
  --font-mono: 'DM Mono', monospace;
}
```

All UI elements (panels, legends, controls, overlays) reference these variables. To retheme, swap this block. Map canvas content (basemap tiles, data points) does NOT use CSS variables.

## QGIS

- Page background: rgb(10, 10, 15)
- Labels: DM Sans, white, dark halo
- Print exports: 300 DPI PDF + 150 DPI PNG
- Basemap: dark — no standard OSM tiles

## Leaflet / Web Maps

- Basemap tiles: CartoDB Dark Matter
- Accent color for lines/highlights: #c9a84c
- Popup styling: dark bg, light text, DM Sans
- Use IntersectionObserver for lazy loading

## Architectural Drawings / Print

TBD — depends on design phase and output format. Will derive from the same palette.
