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
| 2026-03-25 ~13:21 | Andrea & Henna | "We are BA6 architecture students in Professor Huang's studio. We are setting up remote Windows machines to run multiple Rhino instances in parallel for a modeling project. Do you have Rhino licenses that could work on VMs connected through EPFL VPN? We'd need about 4 concurrent seats. We are presenting this work March 30, so knowing what is available before then would be really helpful for us." | — |
| 2026-03-25 13:42 | Sébastien | "It should be OK, for how long do you need these licenses?" | Reply with duration |
| 2026-03-25 13:53 | Andrea | "Thank you for the quick response. We would need them until the end of the semester (end of June). Would that work?" | — |
| 2026-03-25 13:58 | Sébastien | "Yes. I will need the name of the computer you will use. When the software asks you how you want to activate the license, use the 'LAN Zoo License Manager' and give it this address: mcneellic.epfl.ch" | **⚠️ Need computer name — depends on RCP VM response** |

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
| 2026-03-25 ~11:00 | Andrea & Henna | Ticket **INC0789496** opened. "We are BA6 architecture students in Professor Huang's studio. We use AI agents to build 3D models in Rhino (a CAD application). Right now everything runs on our laptops, but we need to move to remote machines. Windows is required because Rhino only supports multiple concurrent instances on Windows. Three or four machines with 16-32 GB RAM each, SSH accessible. What is the best way to get Windows VMs through EPFL for this kind of setup? We would also like to try AIaaS, specifically for document embeddings (we were looking into Gemini Embedding 2 for about 35k chunks of construction references). How do we get access? We are presenting this work March 30, so knowing what is available before then would be really helpful for us." | Wait for response |

### Status: 🟡 SENT — ticket INC0789496 being analyzed

### What we asked for
1. **Windows VMs**: 3-4 machines, 16-32 GB RAM each, SSH accessible, for running Rhino
2. **AIaaS access**: document embeddings, specifically Gemini Embedding 2 for 35K chunks of construction references

### Notes
- RCP is **on-premise** (not cloud) — EPFL's own data center
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
