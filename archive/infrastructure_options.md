# Infrastructure Options — Cost Comparison

Research conducted 2026-03-24 for funding email.

## EPFL RCP vs Azure

| Resource | EPFL RCP (U1 rate) | Azure (Switzerland) | Savings |
|----------|-------------------|-------------------|---------|
| Dedicated server/day | 6.40 CHF | ~84 CHF | 13x |
| V100 GPU-hour | 0.14 CHF | ~3.06 CHF | 22x |
| H100 GPU-hour | 0.54 CHF | ~4.50 CHF | 8x |
| Storage TB/year | 20.75 CHF | ~250 CHF | 12x |
| AI inference | 70+ models, possibly included | Pay per token | - |

**RCP access:** Email 1234@epfl.ch — Prof. Huang requests on behalf of studio.
**Critical question:** Can HAAS servers run Windows? (needed for Rhino)

## Rhino Licensing

| Option | Price | Notes |
|--------|-------|-------|
| Educational license | $195/seat | One concurrent instance per license |
| Lab license (ENAC) | May exist | Ask enac-it@epfl.ch |
| Rhino.Compute (headless) | Free + Rhino license | Needs MCP rewrite for REST API |
| Rhino via RDP on VM | Works now | Our rhinomcp works as-is |

**Key constraint:** One license = one simultaneous Rhino. 4 VMs = 4 licenses.
**Best path:** Ask ENAC-IT if spare seats exist before buying.

## Scenario Costing (4 concurrent Rhino agents, 1 month)

| Scenario | Infrastructure | Rhino | Total/month |
|----------|---------------|-------|-------------|
| **Best: EPFL RCP + ENAC licenses** | ~770 CHF | 0 CHF | ~770 CHF |
| **Mid: EPFL RCP + buy licenses** | ~770 CHF | ~720 CHF (one-time) | ~1,490 first month |
| **Worst: Azure + buy licenses** | ~2,500 CHF | ~720 CHF (one-time) | ~3,220 first month |

## API Costs

| Service | Cost | Notes |
|---------|------|-------|
| Gemini Embedding 2 | ~$1.60 spent of $300 GCP credits | 90-day free trial |
| Gemini Flash/Pro (generation) | ~$5-10 total for all extraction | Same credits |
| Claude Code | Covered by subscription | Already active |
| YouTube embedding | ~$0.61 | Same Gemini credits |

## Contacts to Email

1. **1234@epfl.ch** — RCP access, HAAS Windows support, AI inference
2. **enac-it@epfl.ch** — Existing Rhino seats, Cloud Zoo, VM usage policy
3. **sales@mcneel.com** — Research project multi-seat pricing


miguel fontes