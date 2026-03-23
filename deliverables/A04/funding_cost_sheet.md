# Funding Request — AI-Assisted Architectural Modeling Infrastructure

**EPFL AR-302k, Studio Huang — "Sentient Cities"**
Andrea Crespo & Henna Rafik | March 2026

---

## What we built

We developed a knowledge-grounded AI modeling system for architecture: a 4-layer construction knowledge base (375 Swiss LCA records, 33 curated guides, 35,000+ embedded document chunks from Dicobat, SIA norms, and academic sources), connected to Rhino via MCP for multi-agent 3D modeling. We built and modified the MCP infrastructure ourselves to support multi-instance and multi-session Rhino workflows. In a proof-of-concept test, 7 AI agents collaboratively built 709 objects on a single site, with all dimensions traceable to construction references. The entire system was built at near-zero cost (~2 CHF in API fees).

---

## Cost by category

### 1. AI Capability — Claude Max

| | Cost | Status |
|-|------|--------|
| Andrea (since February 2026) | 100 CHF/month | Active |
| Henna (since March 2026) | 100 CHF/month | Active |
| **Subtotal** | **200 CHF/month** | |

Powers all AI modeling, code generation, agent coordination, research, and data analysis. This is the core of the system — everything else is infrastructure that extends its reach.

### 2. Software — Rhino + Blender

| | Cost | Status |
|-|------|--------|
| Rhino 8 educational license (Windows) | ~95 CHF one-time | Needed |
| Rhino core-hour billing (Cloud Zoo) | ~0.10 CHF/core-hour per VM | Needed with VMs |
| Blender + BlenderMCP | Free (open source) | Available |
| **Subtotal** | **~95 CHF one-time + usage** | |

One educational license covers all VM clones via Cloud Zoo. Core-hour billing scales with actual usage — pay only when Rhino is running.

### 3. Infrastructure — Azure Cloud Compute

| | Cost | Status |
|-|------|--------|
| VM compute (B2ms, 2 vCPU / 8 GB, Windows) | ~0.10 CHF/hr per instance | Needed |
| Managed SSD storage (128 GB per VM) | ~20 CHF/month per disk | Needed |
| EPFL Azure credits | –100 CHF (one-time offset) | Available |
| **Subtotal** | **scales with usage (see phases below)** | |

Golden image approach: set up one VM (Rhino + custom MCP server + SSH tunnel), capture the image, clone to spin up parallel instances on demand. Our routing server (already built and tested) distributes agent work across instances. VMs deallocate when idle — compute stops, only storage billed.

### 4. Knowledge Base — Embeddings + RAG

| | Cost | Status |
|-|------|--------|
| Gemini API (300 USD free credits) | ~0 CHF | Active |
| Embedding cost (text) | ~0.65 CHF per 2,500 pages | Negligible |
| **Subtotal** | **~0 CHF (covered by free credits)** | |

### 5. Hosting + Publishing

| | Cost | Status |
|-|------|--------|
| GitHub Pages (dashboard, visualizations) | Free | Active |
| **Subtotal** | **0 CHF** | |

---

## Cost by phase

### Phase 0 — Knowledge + Training (✅ complete)

**Duration:** 2 weeks (done)
**Cost:** ~2 CHF

| Category | Spend |
|----------|-------|
| Claude Max | 200 CHF/month (already running) |
| Gemini embeddings | ~2 CHF |
| Everything else | 0 CHF |

Built: 4-layer knowledge base (35K+ chunks), training pipeline (80 exercises, 5,248 objects), multi-agent proof of concept (7 agents, 709 objects on Lock 05).

### Phase 1 — Validation + Setup (this week, March 23–28)

**Duration:** ~5 days
**New cost:** < 100 CHF

| Category | Min | Max | Notes |
|----------|-----|-----|-------|
| Claude Max | 200 | 200 | Running |
| Gemini embeddings | 0 | 5 | Remaining PDFs (Deplazes, tutorials) |
| Blender MCP setup | 0 | 0 | Free |
| Henna laptop routing test | 0 | 0 | Uses existing hardware |
| **Phase 1 total (new spend)** | **0** | **5 CHF** | |

Validate: Rhino routing works across machines (Henna's Windows laptop). Complete knowledge base embeddings. Set up Blender MCP as secondary modeling tool.

### Phase 2 — Cloud Infrastructure (this week, March 26–28)

**Duration:** ~3 days
**New cost:** ~95–150 CHF

| Category | Min | Max | Notes |
|----------|-----|-----|-------|
| Rhino license | 95 | 95 | One-time |
| Azure VM (1× B2ms) | 5 | 17 | Testing hours only |
| Azure storage (1 disk) | 5 | 20 | Prorated |
| Rhino core-hours | 3 | 16 | Testing usage |
| EPFL credit offset | –13 | –53 | Covers Azure costs |
| **Phase 2 total (new spend)** | **~95** | **~95 CHF** | Azure offset by EPFL credits |

The gate: validate end-to-end cloud modeling — Claude on Mac → SSH tunnel → Azure VM → Rhino headless → geometry back. If this works, we scale. If not, we've spent only a Rhino license (usable locally regardless).

### Phase 3 — Production Modeling (weeks 2–4, March 30 – April 20)

**Duration:** ~3 weeks
**New cost:** ~100–170 CHF/month

| Category | Min (1 VM) | Max (3 VMs) | Notes |
|----------|------------|-------------|-------|
| Claude Max | 200 | 200 | Running |
| Azure compute | 17 | 50 | 40 hrs/wk per VM |
| Azure storage | 20 | 60 | 1–3 disks |
| Rhino core-hours | 16 | 48 | Per running instance |
| EPFL credit offset | –47 | 0 | Remaining credits (if any) |
| **Phase 3 monthly** | **~253** | **~358 CHF/month** | |

Scale from 1 VM to 3 VMs as modeling demands grow. Model all 9 corridor nodes with parallel agent teams. Multiple design iterations per node. VMs deallocated between sessions.

---

## Scaling over time

```
           Monthly cost (CHF)
     400 ─┬─────────────────────────────────────────────
         │                              ┌─── 3 VMs ──── Phase 3b
     350 ─┤                              │   (~358)
         │                         ┌────┘
     300 ─┤                    ┌───┘  Phase 3a: 1-2 VMs
         │                    │       (~253-305)
     250 ─┤               ┌───┘
         │          ┌─────┘  Phase 2: testing
     200 ─┤──────────┘        (~205)
         │  Phase 0-1
         │  Claude Max only
     150 ─┤  (~200)
         │
     100 ─┤
         │
      50 ─┤
         │
       0 ─┴──┬──────┬──────┬──────┬──────┬──────┬──────
          Feb    Mar     Apr     May
              ↑        ↑              ↑
           Henna    Rhino +        Full
            Max    1st VM        corridor
```

| Period | Monthly | Cumulative | What's running |
|--------|---------|------------|----------------|
| Feb 2026 | 100 | 100 | Andrea's Claude Max |
| Mar 1–22 | 200 | 500 | + Henna's Claude Max |
| Mar 23–31 (Phase 1–2) | ~205 | ~555 | + Rhino license (95 one-time) + first VM testing |
| Apr (Phase 3a) | ~305 | ~860 | 1–2 VMs, corridor modeling begins |
| May (Phase 3b) | ~360 | ~1,220 | 3 VMs, full parallel modeling |

**Total project cost through end of May: ~1,200–1,300 CHF**
Of which ~1,000 CHF is Claude Max subscriptions (the AI capability itself).

---

## Proof of concept

Lock 05 (CHUV node): 7 AI agents built 709 objects — shell, windows, structure, circulation, elevator, roof, ground — in a single coordinated session. Every dimension traces to Swiss construction references (SIA loads, KBOB materials, fire codes). Agents caught and resolved spatial conflicts between building systems without human intervention.

---

## Risk mitigation

- **Phased cost gates**: each phase requires the previous to succeed. No bulk commitment.
- **Dominant cost is Claude Max** (200 CHF/month) — already running, already proven. Infrastructure adds only ~100–160 CHF/month at full capacity.
- **Free tiers cover secondary tools**: Gemini credits, Blender, GitHub Pages — all zero cost.
- **Golden image approach**: set up once, clone as needed, deallocate when idle. No wasted compute.
- **EPFL credits**: 100 CHF Azure offset, no credit card required.
- **Technical infrastructure built by the team**: multi-instance MCP routing, SSH tunneling, agent coordination — all developed and tested in-house.
- **Rhino license retains value**: if cloud approach fails, the license works locally on any Windows machine.
