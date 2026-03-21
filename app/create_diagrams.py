#!/usr/bin/env python3
"""
Create 5 professional architecture diagrams for "Still on the Line" project.
Uses svgwrite for SVG creation, then cairosvg for PNG conversion.
"""

import svgwrite
from svgwrite import cm, mm, px
import math

# Color scheme
DARK_BG = "#0a0a0f"
GOLD_ACCENT = "#c9a84c"
AI_ZONE = "#4a2c6e"
DETERMINISTIC = "#1a3a2a"
DATA_GREY = "#2a2a3a"
INTERFACE_BROWN = "#3a2a1a"
WHITE = "#ffffff"
LIGHT_GREY = "#d0d0d0"
RED_ACCENT = "#d85555"
TEAL = "#2a5a5a"
WARM = "#5a4a3a"

# Output directory
OUTPUT_DIR = "/sessions/kind-tender-carson/mnt/app_architecture/diagrams"

def add_rounded_rect(dwg, x, y, width, height, rx=15, fill="#333", stroke="#ccc", stroke_width=2, text="", text_color=WHITE, font_size=14, bold=False):
    """Helper: add rounded rectangle with optional text."""
    rect = dwg.rect(insert=(x, y), size=(width, height), rx=rx, ry=rx,
                     fill=fill, stroke=stroke, stroke_width=stroke_width)
    dwg.add(rect)

    if text:
        weight = "bold" if bold else "normal"
        text_elem = dwg.text(text, insert=(x + width/2, y + height/2),
                             font_size=f"{font_size}px", font_family="Arial, sans-serif",
                             font_weight=weight, text_anchor="middle", dominant_baseline="middle",
                             fill=text_color)
        dwg.add(text_elem)

def add_arrow(dwg, x1, y1, x2, y2, label="", color=GOLD_ACCENT, label_offset=15):
    """Helper: add arrow with optional label."""
    line = dwg.line(start=(x1, y1), end=(x2, y2),
                    stroke=color, stroke_width=2)
    dwg.add(line)

    # Arrow head
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_size = 10
    arrow_x = x2 - arrow_size * math.cos(angle)
    arrow_y = y2 - arrow_size * math.sin(angle)

    points = [
        (x2, y2),
        (arrow_x - arrow_size * math.sin(angle), arrow_y + arrow_size * math.cos(angle)),
        (arrow_x + arrow_size * math.sin(angle), arrow_y - arrow_size * math.cos(angle))
    ]
    polygon = dwg.polygon(points=points, fill=color, stroke=color)
    dwg.add(polygon)

    # Label
    if label:
        mid_x = (x1 + x2) / 2
        mid_y = (y1 + y2) / 2 - label_offset
        text_elem = dwg.text(label, insert=(mid_x, mid_y),
                             font_size="11px", font_family="Arial, sans-serif",
                             text_anchor="middle", fill=LIGHT_GREY)
        dwg.add(text_elem)

# ============================================================================
# DIAGRAM 1: System Architecture
# ============================================================================
def create_system_architecture():
    dwg = svgwrite.Drawing(f"{OUTPUT_DIR}/system_architecture.svg",
                          size=('1200px', '800px'))
    # Add background
    bg = dwg.rect(insert=(0, 0), size=('1200px', '800px'), fill=DARK_BG)
    dwg.add(bg)

    # Title
    title = dwg.text("System Architecture Overview", insert=(600, 30),
                     font_size="24px", font_family="Arial, sans-serif",
                     font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(title)

    # User input on left
    add_rounded_rect(dwg, 30, 150, 100, 80, rx=10, fill="#555", stroke=GOLD_ACCENT, text="USER\n(Browser)", font_size=11)
    add_arrow(dwg, 130, 180, 180, 180, label="Community", label_offset=5)
    add_arrow(dwg, 130, 210, 180, 220, label="Region", label_offset=5)

    # Module positions
    modules = [
        (180, 100, "CORRIDOR\nKNOWLEDGE BASE\n49 stations\n~3,200 records", DATA_GREY),
        (380, 100, "COMMUNITY\nRESEARCH ENGINE\nAI-powered\n(Phase 2)", AI_ZONE),
        (580, 100, "SCORING\nENGINE\n5 criteria\nWeighted sum", TEAL),
        (780, 100, "PROPOSITION\nGENERATOR\nLock assignment\nChamber config", DETERMINISTIC),
        (980, 100, "OUTPUT\nPIPELINE\n3 renderers\n1 JSON", WARM),
    ]

    for i, (x, y, text, color) in enumerate(modules):
        add_rounded_rect(dwg, x, y, 160, 120, rx=12, fill=color, stroke=GOLD_ACCENT,
                        stroke_width=2, text=text, font_size=10, text_color=WHITE)

        if i < len(modules) - 1:
            add_arrow(dwg, x + 160, y + 60, modules[i+1][0], modules[i+1][1] + 60,
                     color=LIGHT_GREY)

    # AI/Deterministic boundary line
    boundary_x = 530
    dwg.line(start=(boundary_x, 50), end=(boundary_x, 280), stroke=GOLD_ACCENT, stroke_width=3, stroke_dasharray="5,5")
    label = dwg.text("AI / DETERMINISTIC BOUNDARY", insert=(boundary_x, 45),
                     font_size="10px", font_family="Arial, sans-serif",
                     font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT,
                     transform=f"rotate(-90 {boundary_x} 45)")
    dwg.add(label)

    # Interface module at bottom
    add_rounded_rect(dwg, 350, 300, 500, 100, rx=12, fill=INTERFACE_BROWN,
                    stroke=GOLD_ACCENT, stroke_width=2,
                    text="INTERFACE\nTwo tabs: Analysis + Outputs",
                    font_size=11, text_color=LIGHT_GREY)

    # Arrows from pipeline to interface
    add_arrow(dwg, 600, 220, 600, 300, color=LIGHT_GREY)

    # Sub-items for first module (small boxes)
    sub_y = 250
    subs = ["Modal diversity", "Break points", "Temporal freq", "Ridership"]
    for i, sub in enumerate(subs):
        sub_text = dwg.text(sub, insert=(250 + i*60, sub_y),
                           font_size="8px", font_family="Arial, sans-serif",
                           text_anchor="middle", fill=LIGHT_GREY)
        dwg.add(sub_text)

    dwg.save()
    print("✓ system_architecture.svg created")

# ============================================================================
# DIAGRAM 2: AI vs Deterministic Boundary
# ============================================================================
def create_ai_boundary():
    dwg = svgwrite.Drawing(f"{OUTPUT_DIR}/ai_boundary.svg",
                          size=('1200px', '700px'))
    # Add background
    bg = dwg.rect(insert=(0, 0), size=('1200px', '700px'), fill=DARK_BG)
    dwg.add(bg)

    # Title
    title = dwg.text("AI vs Deterministic Boundary", insert=(600, 30),
                     font_size="24px", font_family="Arial, sans-serif",
                     font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(title)

    # Left zone (AI)
    ai_bg = dwg.rect(insert=(30, 70), size=(300, 550), fill=AI_ZONE, opacity=0.15, stroke=AI_ZONE, stroke_width=2)
    dwg.add(ai_bg)

    ai_label = dwg.text("AI ZONE", insert=(180, 100),
                       font_size="14px", font_family="Arial, sans-serif",
                       font_weight="bold", text_anchor="middle", fill=AI_ZONE)
    dwg.add(ai_label)

    ai_items = [
        "Community chain research",
        "Breaking point identification",
        "Region validation reasoning",
        "Narrative generation"
    ]
    for i, item in enumerate(ai_items):
        text_elem = dwg.text(item, insert=(180, 150 + i*60),
                            font_size="10px", font_family="Arial, sans-serif",
                            text_anchor="middle", fill=LIGHT_GREY)
        dwg.add(text_elem)

    # Center (Handoff)
    center_x = 400
    center_label = dwg.text("HANDOFF", insert=(center_x + 50, 100),
                           font_size="14px", font_family="Arial, sans-serif",
                           font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(center_label)

    center_label2 = dwg.text("Chain Model", insert=(center_x + 50, 120),
                            font_size="10px", font_family="Arial, sans-serif",
                            text_anchor="middle", fill=LIGHT_GREY)
    dwg.add(center_label2)

    # Center box
    center_rect = dwg.rect(insert=(center_x - 40, 80), size=(180, 500),
                          fill="none", stroke=GOLD_ACCENT, stroke_width=3)
    dwg.add(center_rect)

    center_items = [
        "Worker counts",
        "Criticality scores",
        "Break point locations",
        "Flow type definitions"
    ]
    for i, item in enumerate(center_items):
        text_elem = dwg.text(item, insert=(center_x + 50, 160 + i*70),
                            font_size="10px", font_family="Arial, sans-serif",
                            text_anchor="middle", fill=LIGHT_GREY)
        dwg.add(text_elem)

    # Right zone (Deterministic)
    det_bg = dwg.rect(insert=(590, 70), size=(570, 550), fill=DETERMINISTIC, opacity=0.15,
                      stroke=DETERMINISTIC, stroke_width=2)
    dwg.add(det_bg)

    det_label = dwg.text("DETERMINISTIC ZONE", insert=(875, 100),
                        font_size="14px", font_family="Arial, sans-serif",
                        font_weight="bold", text_anchor="middle", fill=DETERMINISTIC)
    dwg.add(det_label)

    det_items = [
        "Scoring: 5 criteria",
        "Lock type: decision tree",
        "Weight adjustment",
        "Spec sheet: template + data",
        "3D preview: geometry",
        "Rhino script: parameters"
    ]
    for i, item in enumerate(det_items):
        text_elem = dwg.text(item, insert=(875, 150 + i*50),
                            font_size="10px", font_family="Arial, sans-serif",
                            text_anchor="middle", fill=LIGHT_GREY)
        dwg.add(text_elem)

    # Flow arrows
    add_arrow(dwg, 330, 350, 360, 350, color=GOLD_ACCENT)
    add_arrow(dwg, 540, 350, 590, 350, color=GOLD_ACCENT)

    dwg.save()
    print("✓ ai_boundary.svg created")

# ============================================================================
# DIAGRAM 3: Scoring Funnel
# ============================================================================
def create_scoring_funnel():
    dwg = svgwrite.Drawing(f"{OUTPUT_DIR}/scoring_funnel.svg",
                          size=('1200px', '900px'))
    # Add background
    bg = dwg.rect(insert=(0, 0), size=('1200px', '900px'), fill=DARK_BG)
    dwg.add(bg)

    # Title
    title = dwg.text("Scoring Funnel: Data → 5 Numbers → Deterministic", insert=(600, 30),
                     font_size="22px", font_family="Arial, sans-serif",
                     font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(title)

    # Top: Data sources (wide)
    sources = [
        "corridor_segments\n(49 × 17)",
        "break_points\n(49 × 25)",
        "temporal_freq\n(49 × 28)",
        "modal_diversity\n(49 × 17)",
        "ridership_sbb\n(174 × 13)",
        "shared_mobility\n(2,062 × 9)",
        "Google Places\nAPI",
        "transport.\nopendata.ch",
        "AI chain\nanalysis"
    ]

    y_start = 80
    box_width = 110
    spacing = 5
    total_width = 9 * box_width + 8 * spacing
    start_x = (1200 - total_width) / 2

    for i, source in enumerate(sources):
        x = start_x + i * (box_width + spacing)
        add_rounded_rect(dwg, x, y_start, box_width, 80, rx=8, fill=DATA_GREY,
                        stroke=LIGHT_GREY, stroke_width=1, text=source, font_size=7)

    # Funnel shape (trapezoid)
    funnel_top_y = 200
    funnel_points = [
        (100, funnel_top_y),
        (1100, funnel_top_y),
        (900, 500),
        (300, 500)
    ]
    funnel = dwg.polygon(points=funnel_points, fill="none", stroke=GOLD_ACCENT,
                        stroke_width=2, stroke_dasharray="5,5")
    dwg.add(funnel)

    # Middle: 5 criteria
    criteria = [
        ("①", "Affected\nPopulation", "25%"),
        ("②", "Chain\nCriticality", "25%"),
        ("③", "Modal\nCollapse", "20%"),
        ("④", "Gap\nDistance", "15%"),
        ("⑤", "Infra\nReadiness", "15%")
    ]

    crit_y = 350
    crit_width = 140
    crit_spacing = 20
    crit_total = 5 * crit_width + 4 * crit_spacing
    crit_start_x = (1200 - crit_total) / 2

    for i, (num, label, pct) in enumerate(criteria):
        x = crit_start_x + i * (crit_width + crit_spacing)

        # Colored box
        color = [TEAL, DETERMINISTIC, AI_ZONE, DATA_GREY, INTERFACE_BROWN][i]
        add_rounded_rect(dwg, x, crit_y, crit_width, 90, rx=8, fill=color,
                        stroke=GOLD_ACCENT, stroke_width=2, text=f"{num}\n{label}\n{pct}",
                        font_size=8)

    # Bottom: Downstream (narrow)
    downstream_y = 520
    downstream_items = [
        "Site +\nLock Type",
        "Chamber\nConfig",
        "Spec\nSheet",
        "3D\nPreview",
        "Rhino\nScript"
    ]

    down_width = 100
    down_spacing = 10
    down_total = 5 * down_width + 4 * down_spacing
    down_start_x = (1200 - down_total) / 2

    for i, item in enumerate(downstream_items):
        x = down_start_x + i * (down_width + down_spacing)
        color = [DETERMINISTIC, TEAL, WARM, INTERFACE_BROWN, DATA_GREY][i]
        add_rounded_rect(dwg, x, downstream_y, down_width, 70, rx=8, fill=color,
                        stroke=GOLD_ACCENT, stroke_width=1, text=item, font_size=8)

        if i < len(downstream_items) - 1:
            add_arrow(dwg, x + down_width, downstream_y + 35,
                     x + down_width + down_spacing, downstream_y + 35, color=LIGHT_GREY)

    # Flow labels
    flow_label1 = dwg.text("MANY DATA SOURCES", insert=(600, 160),
                          font_size="11px", font_family="Arial, sans-serif",
                          font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(flow_label1)

    flow_label2 = dwg.text("THE FUNNEL: 9 inputs → 5 scores", insert=(600, 300),
                          font_size="12px", font_family="Arial, sans-serif",
                          font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(flow_label2)

    flow_label3 = dwg.text("DETERMINISTIC DOWNSTREAM", insert=(600, 610),
                          font_size="11px", font_family="Arial, sans-serif",
                          font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(flow_label3)

    dwg.save()
    print("✓ scoring_funnel.svg created")

# ============================================================================
# DIAGRAM 4: Lock Decision Tree
# ============================================================================
def create_lock_decision_tree():
    dwg = svgwrite.Drawing(f"{OUTPUT_DIR}/lock_decision_tree.svg",
                          size=('1200px', '900px'))
    # Add background
    bg = dwg.rect(insert=(0, 0), size=('1200px', '900px'), fill=DARK_BG)
    dwg.add(bg)

    # Title
    title = dwg.text("Lock Type Decision Tree", insert=(600, 30),
                     font_size="24px", font_family="Arial, sans-serif",
                     font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(title)

    # Root node
    add_rounded_rect(dwg, 480, 70, 240, 60, rx=10, fill=TEAL, stroke=GOLD_ACCENT,
                    stroke_width=2, text="Score ≥ 3.0\n(Site qualifies)", font_size=10)

    # Decision nodes and outcomes
    decisions = [
        # Y1
        (600, 170, "Crosses\nnational\nborder?", 150, 250),
        (750, 250, "BORDER\nLOCK", RED_ACCENT),
        # Y1N
        (450, 170, "Major logistics\ncorridor?", 150, 250),
        (300, 250, "Adjacent to\ncivic space?", 100, 250),
        (150, 330, "LOGISTICS\nENGINE", TEAL),
        (450, 330, "CARGO\nLOCK", WARM),
        # Y2N
        (600, 320, "Significant\naltitude\nchange?", 150, 250),
        (750, 400, "Steep grade\n+ equity gap?", 100, 250),
        (650, 480, "GRADIENT\nDISPATCHER", DETERMINISTIC),
        (850, 480, "ALTITUDE\nLOCK", AI_ZONE),
        # Y3N
        (300, 400, "Hospital\noff-rail?", 100, 250),
        (150, 480, "BRIDGE\nLOCK", TEAL),
        (450, 480, "VISIBILITY\nLOCK", DATA_GREY),
        # Y4N
        (150, 560, "Between\ngeographic\nvoids?", 100, 200),
        (50, 640, "GAP\nRELAY", INTERFACE_BROWN),
        (250, 640, "TEMPORAL\nLOCK", WARM),
    ]

    # Simplified tree structure
    tree_y = 70

    # Level 1: Root
    add_rounded_rect(dwg, 480, tree_y, 240, 60, rx=10, fill=TEAL, stroke=GOLD_ACCENT,
                    stroke_width=2, text="Score ≥ 3.0\n(Site qualifies)", font_size=10)

    # Level 2: First question
    q1_y = tree_y + 120
    add_rounded_rect(dwg, 300, q1_y, 140, 70, rx=10, fill="none", stroke=GOLD_ACCENT,
                    stroke_width=2, text="Crosses\nnational\nborder?", font_size=9)
    add_rounded_rect(dwg, 560, q1_y, 140, 70, rx=10, fill="none", stroke=GOLD_ACCENT,
                    stroke_width=2, text="Major logistics\ncorridor?", font_size=9)

    # Arrows from root
    add_arrow(dwg, 600, tree_y + 60, 370, q1_y, label="YES", color=LIGHT_GREY)
    add_arrow(dwg, 600, tree_y + 60, 630, q1_y, label="NO", color=LIGHT_GREY)

    # Outcomes for Q1
    outcome_y = q1_y + 120
    add_rounded_rect(dwg, 230, outcome_y, 120, 60, rx=10, fill=RED_ACCENT,
                    stroke=RED_ACCENT, stroke_width=2, text="BORDER\nLOCK", font_size=10)

    # Outcomes for Q2
    add_rounded_rect(dwg, 450, outcome_y, 120, 60, rx=10, fill=DETERMINISTIC,
                    stroke=DETERMINISTIC, stroke_width=2, text="Q2a:\nCivic space?", font_size=9)
    add_rounded_rect(dwg, 650, outcome_y, 120, 60, rx=10, fill=TEAL,
                    stroke=TEAL, stroke_width=2, text="Q3:\nAltitude?", font_size=9)

    # More outcomes
    outcomes_bottom = outcome_y + 120
    lock_types = [
        (100, "LOGISTICS\nENGINE", TEAL),
        (250, "CARGO\nLOCK", WARM),
        (400, "GRADIENT\nDISPATCHER", DETERMINISTIC),
        (550, "ALTITUDE\nLOCK", AI_ZONE),
        (700, "BRIDGE\nLOCK", TEAL),
        (850, "VISIBILITY\nLOCK", DATA_GREY),
    ]

    for x, label, color in lock_types:
        add_rounded_rect(dwg, x, outcomes_bottom, 110, 60, rx=8, fill=color,
                        stroke=color, stroke_width=2, text=label, font_size=8)

    # Final outcomes
    final_y = outcomes_bottom + 120
    add_rounded_rect(dwg, 200, final_y, 120, 60, rx=8, fill=INTERFACE_BROWN,
                    stroke=INTERFACE_BROWN, stroke_width=2, text="GAP\nRELAY", font_size=10)
    add_rounded_rect(dwg, 450, final_y, 120, 60, rx=8, fill=WARM,
                    stroke=WARM, stroke_width=2, text="TEMPORAL\nLOCK\n(default)", font_size=9)

    # Legend
    legend_y = 750
    legend_text = dwg.text("9 lock types assigned deterministically based on site characteristics",
                          insert=(600, legend_y),
                          font_size="10px", font_family="Arial, sans-serif",
                          text_anchor="middle", fill=LIGHT_GREY, font_style="italic")
    dwg.add(legend_text)

    dwg.save()
    print("✓ lock_decision_tree.svg created")

# ============================================================================
# DIAGRAM 5: Implementation Timeline
# ============================================================================
def create_implementation_timeline():
    dwg = svgwrite.Drawing(f"{OUTPUT_DIR}/implementation_timeline.svg",
                          size=('1200px', '700px'))
    # Add background
    bg = dwg.rect(insert=(0, 0), size=('1200px', '700px'), fill=DARK_BG)
    dwg.add(bg)

    # Title
    title = dwg.text("Implementation Timeline (Mar 18–30)", insert=(600, 30),
                     font_size="24px", font_family="Arial, sans-serif",
                     font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(title)

    # Timeline axis
    timeline_y = 100
    timeline_x_start = 100
    timeline_x_end = 1100
    timeline_length = timeline_x_end - timeline_x_start

    # Main timeline line
    dwg.line(start=(timeline_x_start, timeline_y), end=(timeline_x_end, timeline_y),
            stroke=GOLD_ACCENT, stroke_width=2)

    # Date markers (Mar 18-30 = 12 days)
    dates = list(range(18, 31))
    for i, date in enumerate(dates):
        x = timeline_x_start + (i / len(dates)) * timeline_length
        dwg.line(start=(x, timeline_y - 5), end=(x, timeline_y + 5),
                stroke=LIGHT_GREY, stroke_width=1)

        if date in [18, 22, 24, 26, 28, 30]:
            label = dwg.text(f"Mar {date}", insert=(x, timeline_y + 20),
                            font_size="9px", font_family="Arial, sans-serif",
                            text_anchor="middle", fill=LIGHT_GREY)
            dwg.add(label)

    # TODAY marker
    today_x = timeline_x_start
    today_circle = dwg.circle(center=(today_x, timeline_y), r=8,
                             fill=GOLD_ACCENT, stroke=GOLD_ACCENT)
    dwg.add(today_circle)
    today_label = dwg.text("TODAY", insert=(today_x, timeline_y - 25),
                          font_size="10px", font_family="Arial, sans-serif",
                          font_weight="bold", text_anchor="middle", fill=GOLD_ACCENT)
    dwg.add(today_label)

    # Andrea's swim lane
    andrea_y = 200
    andrea_label = dwg.text("Andrea", insert=(50, andrea_y),
                           font_size="12px", font_family="Arial, sans-serif",
                           font_weight="bold", fill=LIGHT_GREY)
    dwg.add(andrea_label)

    # Andrea's tasks (dates -> x positions)
    def day_to_x(day):
        return timeline_x_start + ((day - 18) / 12) * timeline_length

    andrea_tasks = [
        (22, 24, "Lockboard\nprep", "#4a6fa5"),
        (24, 25, "Scoring\nengine", "#2a5a8a"),
        (25, 26, "Leaflet\nmap", "#1a4a6a"),
        (26, 27, "Spec\ncards", "#2a5a8a"),
        (27, 28, "Rhino\nscript", "#3a6aaa"),
        (28, 29, "Integration\n+ 3D", "#2a5a8a"),
        (29, 30, "Demo\nrehearse", "#1a4a6a"),
    ]

    for start, end, label, color in andrea_tasks:
        x1 = day_to_x(start)
        x2 = day_to_x(end)
        width = x2 - x1 - 2
        rect = dwg.rect(insert=(x1, andrea_y - 20), size=(width, 40),
                       fill=color, stroke=LIGHT_GREY, stroke_width=1, rx=3)
        dwg.add(rect)

        text_elem = dwg.text(label, insert=(x1 + width/2, andrea_y),
                            font_size="7px", font_family="Arial, sans-serif",
                            text_anchor="middle", dominant_baseline="middle",
                            fill=WHITE)
        dwg.add(text_elem)

    # Henna's swim lane
    henna_y = 350
    henna_label = dwg.text("Henna", insert=(50, henna_y),
                          font_size="12px", font_family="Arial, sans-serif",
                          font_weight="bold", fill=LIGHT_GREY)
    dwg.add(henna_label)

    henna_tasks = [
        (22, 24, "Lockboard\nprep", "#6a4a9a"),
        (24, 26, "Brand\nidentity", "#5a3a8a"),
        (24, 27, "3D corridor\nmodel", "#4a2a7a"),
        (26, 28, "PPTX\nredesign", "#6a4a9a"),
        (28, 29, "Tool\nstyling", "#5a3a8a"),
        (29, 30, "Presentation\nrehearse", "#4a2a7a"),
    ]

    for start, end, label, color in henna_tasks:
        x1 = day_to_x(start)
        x2 = day_to_x(end)
        width = x2 - x1 - 2
        rect = dwg.rect(insert=(x1, henna_y - 20), size=(width, 40),
                       fill=color, stroke=LIGHT_GREY, stroke_width=1, rx=3)
        dwg.add(rect)

        text_elem = dwg.text(label, insert=(x1 + width/2, henna_y),
                            font_size="7px", font_family="Arial, sans-serif",
                            text_anchor="middle", dominant_baseline="middle",
                            fill=WHITE)
        dwg.add(text_elem)

    # Joint milestones
    milestones = [
        (22, "Integration\ncontract"),
        (27, "Internal\ntest"),
        (29, "Presentation\nready"),
        (30, "MIDTERM"),
    ]

    milestone_y = 480
    for day, label in milestones:
        x = day_to_x(day)
        # Diamond marker
        diamond = dwg.polygon(points=[(x, milestone_y - 15), (x + 8, milestone_y),
                                      (x, milestone_y + 15), (x - 8, milestone_y)],
                             fill=GOLD_ACCENT, stroke=GOLD_ACCENT)
        dwg.add(diamond)

        text_elem = dwg.text(label, insert=(x, milestone_y + 40),
                            font_size="8px", font_family="Arial, sans-serif",
                            text_anchor="middle", fill=GOLD_ACCENT, font_weight="bold")
        dwg.add(text_elem)

    # Legend
    legend_y = 600
    legend_text = dwg.text("Color intensity indicates priority/criticality within each swim lane",
                          insert=(600, legend_y),
                          font_size="9px", font_family="Arial, sans-serif",
                          text_anchor="middle", fill=LIGHT_GREY, font_style="italic")
    dwg.add(legend_text)

    dwg.save()
    print("✓ implementation_timeline.svg created")

# ============================================================================
# Main execution
# ============================================================================
if __name__ == "__main__":
    print("\n🎨 Creating SVG diagrams...")
    create_system_architecture()
    create_ai_boundary()
    create_scoring_funnel()
    create_lock_decision_tree()
    create_implementation_timeline()
    print("\n✓ All SVGs created successfully!\n")
