# Funding Request — AI-Assisted Architectural Modeling Infrastructure

**EPFL AR-302k, Studio Huang — "Sentient Cities"**
Andrea Crespo & Henna Rafik | March 2026

*All costs are approximate projections based on publicly available pricing. Actual rates may vary depending on RCP allocation, usage, and licensing arrangements.*

---

## What we built

In a proof-of-concept test, 7 AI agents collaboratively built 709 objects on a single site, with all dimensions traceable to Swiss construction references — at a cost of ~2 CHF in API fees.

The system behind it: a knowledge-grounded AI modeling pipeline connecting a 4-layer construction knowledge base (375 Swiss LCA records, 33 curated guides, 35,000+ embedded document chunks from Dicobat, SIA norms, and academic sources) to Rhino and Blender via MCP (Model Context Protocol) for multi-agent 3D modeling and animation. We built custom routing servers for both tools so multiple AI agents can work on different tasks in parallel.

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
| Rhino 8 educational license (Windows) | ~95 CHF one-time | Needed (if no ENAC seats available) |
| Rhino core-hour billing (Cloud Zoo) | ~0.10 CHF/core-hour per VM | Needed with VMs |
| Blender + Blender MCP | Free (open source) | Available |
| **Subtotal** | **0–95 CHF one-time + usage** | |

One educational license covers all VM clones via Cloud Zoo. Core-hour billing scales with actual usage — pay only when Rhino is running. If ENAC-IT has floating seats available, the one-time license cost drops to zero.

### 3. Infrastructure — EPFL RCP (preferred) or Azure (fallback)

EPFL RCP is 10–22× cheaper than Azure for equivalent resources:

| Resource | EPFL RCP (U1 rate) | Azure (Switzerland) | Savings |
|----------|-------------------|---------------------|---------|
| Dedicated server/day | 6.40 CHF | ~84 CHF | 13× |
| GPU-hour (V100) | 0.14 CHF | ~3.06 CHF | 22× |
| Storage TB/year | 20.75 CHF | ~250 CHF | 12× |
| AI inference | 70+ models, possibly included | Pay per token | — |

| | RCP estimate | Azure estimate | Status |
|-|-------------|----------------|--------|
| VM compute (3–4 instances, 4 vCPU / 16–32 GB) | ~19–26 CHF/day | ~250–340 CHF/day | Needed |
| Persistent storage (golden image + clones) | ~21 CHF/year per TB | ~250 CHF/year per TB | Needed |
| **Subtotal** | **scales with usage** | | |

Golden image approach: set up one VM (Rhino + custom MCP server + SSH tunnel), capture the image, clone to spin up parallel instances on demand. Our routing server (already built and tested) distributes agent work across instances. VMs deallocate when idle — compute stops, only storage billed.

**Pending:** Windows support on RCP HAAS servers to be confirmed. Rhino requires Windows — if unavailable, fallback is Azure (at significantly higher cost).

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

## Cost scenarios (4 concurrent agents, 1 month)

| Scenario | Compute | Rhino | Total/month |
|----------|---------|-------|-------------|
| **Best: EPFL RCP + ENAC licenses** | ~770 CHF | 0 CHF | **~770 CHF** |
| Mid: EPFL RCP + buy licenses | ~770 CHF | ~720 CHF one-time | ~1,490 CHF first month |
| Worst: Azure + buy licenses | ~2,500 CHF | ~720 CHF one-time | ~3,220 CHF first month |

---

## Cost by phase

### Phase 0 — Knowledge + Training (complete)

**Duration:** 2 weeks (done)
**Cost:** ~2 CHF

Built: 4-layer knowledge base (35K+ chunks), training pipeline (80 exercises, 5,248 objects), multi-agent proof of concept (7 agents, 709 objects on Lock 05).

### Phase 1 — Validation + Setup (this week, March 23–28)

**Duration:** ~5 days
**New cost:** < 5 CHF

Validate Rhino routing across machines (Henna's Windows laptop). Complete knowledge base embeddings. Set up Blender MCP routing as secondary modeling/animation tool.

### Phase 2 — Cloud Infrastructure (March 26–28)

**Duration:** ~3 days
**New cost:** ~95–150 CHF (Azure fallback) or near-zero (RCP)

The gate: validate end-to-end cloud modeling — Claude on Mac → SSH tunnel → cloud VM → Rhino headless → geometry back. If this works, we scale. If not, we've spent only a Rhino license (usable locally regardless).

### Phase 3 — Production Modeling (March 30 – May)

**Duration:** ~8 weeks
**New cost:** depends on infrastructure path

| Scenario | Monthly (at full scale) |
|----------|----------------------|
| RCP + ENAC licenses | ~200 CHF (Claude Max only — compute covered by RCP) |
| RCP + bought licenses | ~200 CHF + 720 CHF one-time |
| Azure + bought licenses | ~360 CHF + 720 CHF one-time |

Scale from 1 to 3–4 VMs as modeling demands grow. Model all 9 corridor nodes with parallel agent teams. Multiple design iterations per node. VMs deallocated between sessions.

---

## Scaling over time (cumulative)

| Period | Monthly | Cumulative | What's running |
|--------|---------|------------|----------------|
| Feb 2026 | 100 | 100 | Andrea's Claude Max |
| Mar 1–22 | 200 | 500 | + Henna's Claude Max |
| Mar 23–31 (Phase 1–2) | ~200–205 | ~555 | + Rhino license (if needed) + first VM testing |
| Apr (Phase 3a) | ~200–305 | ~755–860 | 1–2 VMs, corridor modeling begins |
| May (Phase 3b) | ~200–360 | ~955–1,220 | 3–4 VMs, full parallel modeling |

**Total project cost through end of May: ~955–1,300 CHF** depending on infrastructure path.
Of which ~1,000 CHF is Claude Max subscriptions (the AI capability itself).

---

## Tools already built

- **Rhino MCP Router** — distributes modeling commands across multiple Rhino instances on different ports. Tested locally with 7 concurrent agents.
- **Blender MCP Router** — same pattern, for animation and visualization. Built and tested.
- **4-layer knowledge base** — SQLite (materials, codes, dimensions) + curated markdown guides + parametric scripts + RAG (35K+ embedded chunks from construction references).
- **Agent coordination** — multi-agent teams that divide building systems (shell, structure, facade, circulation, etc.) and resolve spatial conflicts autonomously.

---

## Proof of concept

Lock 05 (CHUV node): 7 AI agents built 709 objects — shell, windows, structure, circulation, elevator, roof, ground — in a single coordinated session. Every dimension traces to Swiss construction references (SIA loads, KBOB materials, fire codes). Agents caught and resolved spatial conflicts between building systems without human intervention.

---

## Risk mitigation

- **Phased cost gates**: each phase requires the previous to succeed. No bulk commitment.
- **Dominant cost is Claude Max** (200 CHF/month) — already running, already proven. Infrastructure adds only ~100–160 CHF/month at full capacity.
- **Free tiers cover secondary tools**: Gemini credits, Blender, GitHub Pages — all zero cost.
- **Golden image approach**: set up once, clone as needed, deallocate when idle. No wasted compute.
- **EPFL credits**: 100 CHF Azure offset available if needed as fallback.
- **Technical infrastructure built by the team**: multi-instance MCP routing (Rhino + Blender), SSH tunneling, agent coordination — all developed and tested in-house.
- **Rhino license retains value**: if cloud approach fails, the license works locally on any Windows machine.

---

## Contacts

| Who | For what |
|-----|----------|
| EPFL RCP (via Monique) | VM access, HAAS Windows support, AI inference |
| ENAC-IT (enac-it@epfl.ch) | Existing Rhino floating seats, Cloud Zoo, VM policy |
| McNeel (sales@mcneel.com) | Multi-seat research pricing (if ENAC has no seats) |
