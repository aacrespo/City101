# Email Draft — Infrastructure Request for Alex + Monique

**To:** Alex, CC Monique
**From:** Andrea
**Subject:** Infrastructure request — AI-assisted modeling pipeline (EPFL RCP + Rhino licenses)

---

Hi Alex,

Following our conversation this morning, here's the brief so Monique can bring it to the RCP team. Miguel Fontes is meeting them this afternoon, so this is what we're trying to do and what we need.

## What we built

We developed an AI-assisted architectural modeling system for the studio: Claude Code agents coordinated via MCP (Model Context Protocol) to build 3D geometry in Rhino and animations in Blender. In a proof of concept, 7 agents collaboratively built 709 objects on a single site, with all dimensions traced to Swiss construction references (SIA, KBOB). We also built our own routing servers for both Rhino and Blender, so multiple agents can work on different tasks in parallel.

Right now Andrea works on a Mac (limited to one Rhino instance) and Henna on a Windows laptop. To model our 9 corridor sites in parallel, we need dedicated VMs — each running its own Rhino instance with resources fully allocated to modeling, rather than competing with everything else on our local machines.

## Why EPFL RCP (not Azure)

RCP is 10–22× cheaper than Azure for equivalent resources:

| Resource | EPFL RCP | Azure (Switzerland) | Savings |
|----------|----------|---------------------|---------|
| Dedicated server/day | 6.40 CHF | ~84 CHF | 13× |
| GPU-hour (V100) | 0.14 CHF | ~3.06 CHF | 22× |
| Storage TB/year | 20.75 CHF | ~250 CHF | 12× |

RCP also offers 70+ AI inference models that may be included — we could potentially use these for parts of our pipeline instead of paying per-token externally.

## What we need from RCP

1. **3–4 Windows server instances** (4 vCPU, 16–32 GB RAM each) to run headless Rhino with our custom MCP server. Each VM runs one Rhino instance that receives modeling commands from Claude Code agents on our local machines via SSH tunnel.

2. **Persistent storage** for a golden image: we set up one VM (Rhino + MCP server + SSH config), capture it, and clone to spin up parallel instances on demand. VMs deallocate when idle — only storage billed between sessions.

3. **SSH access to the VMs.** We already have EPFL VPN on our laptops, so reaching the campus network isn't an issue — we just need the VMs to be SSH-accessible so our local routing server can distribute agent work across the remote Rhino instances.

4. **Critical question: Can HAAS servers run Windows?** Rhino requires Windows. If not, we need to know so we can fall back to Azure (at much higher cost) or explore Rhino.Compute (headless, REST-based — would require us to rewrite the MCP layer).

5. **AI inference access** (nice-to-have): If RCP's hosted models include embedding or generation endpoints, we could route parts of our knowledge base pipeline through them instead of external APIs.

## Rhino licenses — separate ask for ENAC-IT

We need **4 concurrent Rhino seats** for the VMs. One license = one simultaneous Rhino, even with floating licenses.

| Option | Cost | Notes |
|--------|------|-------|
| Borrow ENAC-IT floating seats | 0 CHF | Best path — ask if spare seats exist |
| Alex's lab seats (backup) | 0 CHF | If lab has unused licenses |
| Educational purchase | ~720 CHF (4 × $195) | Last resort |
| Rhino.Compute (future) | Free + 1 license | Headless mode, needs MCP rewrite — not ready yet |

**Suggested first step:** ask ENAC-IT (enac-it@epfl.ch) if there are existing floating seats we could use on cloud VMs.

## Cost scenarios (4 concurrent agents, 1 month)

| Scenario | Compute | Rhino | Total |
|----------|---------|-------|-------|
| **Best: RCP + ENAC licenses** | ~770 CHF | 0 CHF | **~770 CHF** |
| Mid: RCP + buy licenses | ~770 CHF | ~720 CHF one-time | ~1,490 CHF first month |
| Worst: Azure + buy licenses | ~2,500 CHF | ~720 CHF one-time | ~3,220 CHF first month |

Our original estimate of ~1,200 CHF through May assumed Azure. With RCP, the infrastructure portion drops significantly — the dominant cost becomes the Claude Max subscriptions we're already paying (200 CHF/month for two people).

## Tools already built

- **Rhino MCP Router** — distributes modeling commands across multiple Rhino instances on different ports. Tested locally, ready for remote VMs.
- **Blender MCP Router** — same pattern, for animation and visualization. Also built and tested.
- **4-layer knowledge base** — 35,000+ embedded document chunks (Swiss construction norms, materials, typologies) that ground the agents' modeling decisions.
- **Agent coordination system** — 7 agents working in parallel on one building, resolving spatial conflicts autonomously.

We just need the compute underneath.

Best,
Andrea

---

*Attachments:*
- *Full cost breakdown (PDF)*
- *Infrastructure comparison: EPFL RCP vs Azure (PDF)*

*We're contacting ENAC-IT separately about existing Rhino floating seats.*
