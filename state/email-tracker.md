# Email Tracker — Studio Infrastructure Requests

**Created:** 2026-03-25
**Purpose:** Track two parallel but interdependent requests — ENAC Rhino licenses + RCP VM services. These are separate departments but the answers need to be compatible (licenses go ON the VMs).

**Key principle:** IT (RCP/VMs) and licenses (ENAC) are separate departments. Request them separately. Be precise — tell them exactly what you need so they don't have to think, just verify and execute.

---

## 1. ENAC Rhino Licenses

**Contact:** Sébastien Durussel (ENAC IT)
**Thread started:** 2026-03-25

### Timeline

| Date | From | Content | Action needed |
|---|---|---|---|
| 2026-03-25 13:21 | Andrea | Initial request: BA6 architecture students in Prof. Huang's studio, setting up remote Windows VMs, need floating Rhino licenses | — |
| 2026-03-25 13:42 | Sébastien | "It should be OK, for how long do you need these licenses?" | Reply with duration |
| 2026-03-25 13:53 | Andrea | "Until end of semester (end of June). Would that work?" | — |
| 2026-03-25 13:58 | Sébastien | **YES.** Needs: (1) the name of the computer, (2) use "LAN Zoo License Manager" and point to `mcneellic.epfl.ch` | **⚠️ Need computer name — depends on RCP VM response** |

### Status: ✅ APPROVED — waiting on computer name from RCP

### Next steps
- [ ] Get VM computer name from RCP (depends on request #2 below)
- [ ] Send computer name to Sébastien
- [ ] Configure LAN Zoo License Manager → `mcneellic.epfl.ch` on the VM
- [ ] Tell Henna about the license setup (she needs to know for her machine too if using VMs)

### Notes
- License activation method: **LAN Zoo License Manager** → `mcneellic.epfl.ch`
- Duration: until end of June 2026
- This is for VMs — separate from local machine licenses

---

## 2. RCP (Research Computing Platform) — VM Services

**Contact:** RCP team (via services portal)
**Thread started:** 2026-03-25

### Timeline

| Date | From | Content | Action needed |
|---|---|---|---|
| 2026-03-25 ~11:00 | Andrea | Sent request for VM services — described project, need Windows VMs with Rhino for headless MCP workflows | Wait for response |

### Status: 🟡 SENT — being analyzed

### What we asked for
- Windows VMs (3-4 instances ideally)
- Rhino 8 installed on each
- For AI-assisted architectural modeling (MCP protocol)
- Part of Prof. Huang's studio course

### Notes
- RCP is **on-premise** (not cloud) — EPFL's own data center
- The request as written requires them to understand the project context → could be slow
- Better approach: be super precise, tell them exactly what specs/config you need, even provide scripts they'd run
- If different departments (IT vs licenses), request the two things separately
- **For the presentation (Monday March 30): don't need everything working. Just need to present the concept.**
- Wait for their response before pushing further

### Next steps
- [ ] Wait for RCP response
- [ ] When they reply: get the VM computer name(s)
- [ ] Send computer name(s) to Sébastien (ENAC) for license activation
- [ ] If RCP asks for more details: prepare precise spec sheet (OS, RAM, storage, software list, network ports)

---

## Dependency Map

```
RCP approves VMs → get computer name(s) → send to Sébastien → licenses activated → configure LAN Zoo on VMs → ready to model
```

Both requests are in progress. The bottleneck is RCP — once we have VM names, the license side is already approved.

---

## For the Monday presentation

**Key insight:** You don't need this infrastructure running for the midterm. You need to *present* it. The VMs, licenses, and headless Rhino are the vision — show the architecture, show the proof of concept (which works on your local machines), explain the scaling plan. The actual provisioning can happen after.
