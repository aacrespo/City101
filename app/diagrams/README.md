# Architecture Diagrams — "Still on the Line"

Professional architecture diagrams for the EPFL BA6 Studio Huang relay-lock configurator project.

## Diagrams

### 1. System Architecture Overview
**File:** `system_architecture.svg` / `system_architecture.png`

Shows the complete 6-module system pipeline:
- **User Input** (left): Community & Region data flows
- **Module Pipeline** (left-to-right):
  1. Corridor Knowledge Base (grey-blue) — 49 stations, ~3,200 records
  2. Community Research Engine (purple/AI) — Google Places, transport.opendata.ch, OSM, Claude API
  3. Scoring Engine (teal) — 5 weighted criteria
  4. Proposition Generator (green) — Lock type assignment, chamber config
  5. Output Pipeline (warm) — 3 renderers + JSON
- **Interface** (bottom): Analysis + Outputs tabs
- **AI/Deterministic Boundary**: Gold dashed line separating AI-powered research (left) from deterministic processing (right)

**Dimensions:** 1200×800px (SVG), 2400×1600px (PNG)

---

### 2. AI vs Deterministic Boundary
**File:** `ai_boundary.svg` / `ai_boundary.png`

Detailed view of the critical handoff between AI and deterministic systems:
- **Left Zone (Purple/AI)**: Community chain research, break point identification, region validation reasoning, narrative generation
- **Center (Gold Box/Handoff)**: Chain Model containing worker counts, criticality scores, break point locations, flow type definitions
- **Right Zone (Green/Deterministic)**: Scoring, lock type assignment, weight adjustment, spec sheet generation, 3D preview parametrics, Rhino script templates

**Dimensions:** 1200×700px (SVG), 2400×1400px (PNG)

---

### 3. Scoring Funnel
**File:** `scoring_funnel.svg` / `scoring_funnel.png`

Data flow visualization showing how 9+ sources converge to 5 scoring criteria:
- **Top (Wide)**: 9 input sources — corridor_segments.csv, break_points.csv, temporal_frequency.csv, modal_diversity.csv, ridership_sbb.csv, shared_mobility.csv, Google Places API, transport.opendata.ch, AI chain analysis
- **Middle (Funnel Trapezoid)**: The 5 weighted scoring criteria:
  1. Affected Population (25%)
  2. Chain Criticality (25%)
  3. Modal Collapse Severity (20%)
  4. Gap Distance (15%)
  5. Infrastructure Readiness (15%)
- **Bottom (Narrow)**: Deterministic outputs — Site + Lock Type → Chamber Config → Spec + 3D + Script

**Dimensions:** 1200×900px (SVG), 2400×1800px (PNG)

---

### 4. Lock Decision Tree
**File:** `lock_decision_tree.svg` / `lock_decision_tree.png`

Flowchart showing the deterministic decision tree for lock type assignment:
- **Start:** Site qualifies (score ≥ 3.0)
- **Decision Path:**
  - Q1: Crosses national border? → **BORDER LOCK** (red)
  - Q2: Major logistics corridor?
    - Q2a: Adjacent to civic space? → **LOGISTICS ENGINE** / **CARGO LOCK**
  - Q3: Significant altitude change?
    - Q3a: Steep grade + equity gap? → **GRADIENT DISPATCHER** / **ALTITUDE LOCK**
  - Q4: Hospital off-rail? → **BRIDGE LOCK** / **VISIBILITY LOCK**
  - Q5: Between geographic voids? → **GAP RELAY**
  - Default: **TEMPORAL LOCK** (fallback)

**9 lock types total**, each color-coded for visual distinction.

**Dimensions:** 1200×900px (SVG), 2400×1800px (PNG)

---

### 5. Implementation Timeline
**File:** `implementation_timeline.svg` / `implementation_timeline.png`

Gantt-style swimlane timeline from March 18 (today) to March 30 (midterm):
- **Andrea's track (blue tones):**
  - Mar 22-24: Lockboard prep
  - Mar 24-25: Scoring engine
  - Mar 25-26: Leaflet map
  - Mar 26-27: Spec cards
  - Mar 27-28: Rhino script
  - Mar 28-29: Integration + 3D
  - Mar 29: Demo rehearsal
- **Henna's track (purple tones):**
  - Mar 22-24: Lockboard prep
  - Mar 24-26: Brand identity
  - Mar 24-27: 3D corridor model
  - Mar 26-28: PPTX redesign
  - Mar 28: Tool styling
  - Mar 29: Presentation rehearsal
- **Joint Milestones (gold diamonds):**
  - Mar 22: Integration contract
  - Mar 27: Internal test
  - Mar 29: Presentation ready
  - Mar 30: MIDTERM

**Dimensions:** 1200×700px (SVG), 2400×1400px (PNG)

---

## Design System

**Colors:**
- Dark background: #0a0a0f
- Gold accent: #c9a84c
- AI zone: #4a2c6e (purple)
- Deterministic zone: #1a3a2a (green)
- Data/static: #2a2a3a (grey-blue)
- Interface: #3a2a1a (warm brown)
- Accent red: #d85555
- White text: #ffffff
- Light grey: #d0d0d0

**Typography:**
- Font: Arial, sans-serif
- Dark theme with gold accents for professional, technical appearance
- Rounded rectangles for modules
- Clean arrows with labels for data flow

**Style:**
- Professional enterprise architecture diagram aesthetic (inspired by IBM/AWS/Google Cloud)
- High contrast for clarity
- Modular, reusable component visualization
- Clear labeling and hierarchical information structure

---

## File Specifications

| File | Format | Size | Dimensions | Use Case |
|------|--------|------|-----------|----------|
| `system_architecture.svg` | Vector (SVG) | 4.8 KB | 1200×800 | Web, scalable, editing |
| `system_architecture.png` | Raster (PNG) | 90 KB | 2400×1600 | Presentation, print, high DPI |
| `ai_boundary.svg` | Vector (SVG) | 3.5 KB | 1200×700 | Web, scalable, editing |
| `ai_boundary.png` | Raster (PNG) | 78 KB | 2400×1400 | Presentation, print, high DPI |
| `scoring_funnel.svg` | Vector (SVG) | 7.3 KB | 1200×900 | Web, scalable, editing |
| `scoring_funnel.png` | Raster (PNG) | 98 KB | 2400×1800 | Presentation, print, high DPI |
| `lock_decision_tree.svg` | Vector (SVG) | 5.7 KB | 1200×900 | Web, scalable, editing |
| `lock_decision_tree.png` | Raster (PNG) | 85 KB | 2400×1800 | Presentation, print, high DPI |
| `implementation_timeline.svg` | Vector (SVG) | 6.7 KB | 1200×700 | Web, scalable, editing |
| `implementation_timeline.png` | Raster (PNG) | 65 KB | 2400×1400 | Presentation, print, high DPI |

---

## Usage

### For Web/Digital Presentation
Use PNG files (`*_large.png` or resize as needed). High DPI (2x) ensures crisp display on Retina/high-density displays.

### For Print
Use PNG files at 300 DPI. Provided PNGs are at 2x resolution, suitable for high-quality printing.

### For Further Editing
Use SVG files. All SVG files are created with `svgwrite` and maintain clean structure for manual editing. Fonts, colors, and layout can be modified easily in any SVG editor or text editor.

### For Presentations (PPTX)
1. Insert PNG files into slides
2. Size as desired (SVG can also be pasted, but PNG is more reliable across platforms)
3. Use the dark background color (#0a0a0f) as slide background for consistent styling

---

## Creation Details

- **Created:** March 18, 2026
- **Tool:** Python + svgwrite (SVG generation) + cairosvg (PNG conversion)
- **License:** Project-specific (EPFL BA6)
- **Contact:** Studio Huang, EPFL Architecture
