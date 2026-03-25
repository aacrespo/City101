# EPFL RCP (Research Computing Platform) — Complete Service Inventory

**Research date:** 2026-03-25
**Sources:** All pages under https://www.epfl.ch/research/facilities/rcp/ + wiki.rcp.epfl.ch + official pricing PDF (Sept 2024)

---

## 1. ALL AVAILABLE SERVICES

### 1.1 GPU Cluster — Container as a Service (CaaS)
- **What:** 700+ GPUs in EPFL DC2020 Datacenter, accessed via Docker containers on Kubernetes with Run:AI scheduler
- **GPU types available:**
  - H200 SXM5 141GB HBM3 (up to 9 nodes, 8 GPUs each)
  - H100 SXM5 80GB (up to 10 nodes, 8 GPUs each)
  - A100 SXM4 80GB (up to 32 nodes, 8 GPUs each)
  - A100 SXM4 40GB (up to 17 nodes, 8 GPUs each)
  - V100 SXM2 32GB (up to 50 nodes, 4 GPUs each)
- **Two workload types:**
  - **Interactive jobs:** Testing/dev, max 1x A100 or 1x V100, 12h max, no preemption
  - **Train jobs:** Training/compute, up to lab's full quota (8x A100 + 4x V100), unlimited duration, preemptible (auto-restart)
- **Access:** Build Docker image, submit via Run:AI scheduler on Kubernetes
- **Storage access:** NAS1 collaborative storage (QoS), NAS3 high-throughput scratch (for I/O)
- **Scratch storage:** 2.5 PiB full flash, 8x100 Gbits/s, no replication
- **Onboarding:** Monthly sessions at AI Center lounge (ELE 117), or per-lab sessions
- **Wiki:** https://wiki.rcp.epfl.ch/en/home/CaaS
- **Scheduler:** https://rcpepfl.run.ai/
- **Registry:** https://registry.rcp.epfl.ch/

### 1.2 Hardware as a Service (HaaS) — Bare Metal Servers
- **What:** Dedicated physical servers for your unit, short or long-term
- **Use case:** Workloads not suitable for VMs in DSI's VSI cluster — specific software, simulations, tests
- **4 server types:**
  - **Standard HAAS** (28 servers in pool)
  - **Middle-End HAAS** (29 servers)
  - **High-End HAAS** (12 servers)
  - **Big-Mem HAAS** (2 servers)
- **Access to scratch HPC storage:** 2.5 PiB full flash, NFS only, 8x100 Gbits/s
- **Request via:** RCP Portal (https://portal.rcp.epfl.ch)
- **Contact:** supportrcp@epfl.ch
- **Wiki:** https://wiki.rcp.epfl.ch/en/home/HaaS

### 1.3 AI Inference as a Service (AIaaS)
- **What:** Managed, scalable AI inference platform — OpenAI-compatible REST API
- **Live since:** August 15, 2025
- **70+ models available** across: LLMs, vision, embedding, reranking, speech-to-text
- **Model families:** Apertus, Mistral, Qwen, Llama, and more
- **API endpoints:**
  - Internal: `https://inference.rcp.epfl.ch/v1`
  - External: `https://inference-rcp.epfl.ch/v1` (limited endpoints, HTTP method filtering)
- **API types:** /v1/models, /v1/chat/completions, /v1/completions, /v1/embeddings, /v1/rerank, /v1/audio/transcriptions
- **Inference stack:** LiteLLM proxy, vLLM/infinity/speaches backends, Knative autoscaling
- **Model loading:** Cold by default — first request triggers loading (minutes), then fast. 24/7 label for always-on models
- **Billing:** Per token, prices on RCP Portal Model Hub
- **API key:** Request via RCP Portal, max 5 parallel requests per key (can be increased)
- **Custom model hosting:** Submit request via form; common models free, custom/niche may have flat fee
- **Compatible with:** OpenWebUI, Claude Code (via env vars), OpenCode, any OpenAI-compatible client
- **Availability target:** 99.9% monthly, 24/7
- **Open to:** Every EPFL employee
- **Prerequisites:** EPFL network or VPN for portal access

### 1.4 Storage for Research
**Three tiers at EPFL:**

| Feature | NAS-RCP | NAS2023 (DSI) | Object Storage S3 (DSI) |
|---------|---------|---------------|------------------------|
| Protocols | NFS, SMB | CIFS, SMB | S3 |
| Replication | *** | *** | *** |
| Snapshots | *** | *** | - |
| Default Quota | None | 1 TB | None |
| Backup | No | Yes | No |
| Performance | ***** | ***** | *** |
| Confidential Data | *** | *** | *** |
| Typical Use | Active Research Data | Active Admin Data | Backups, Archives, Cold Data |
| Operator | VPA-RCP | VPO-SI | VPO-SI |
| **Price** | **20.75 CHF/TB/year (U1)** | TBD | **29 CHF/TB/year** |

- NAS-RCP: 10 PB currently available, multi-site, snapshotted (ransomware-resistant), multi-protocol (Mac/Linux/Windows)
- High-performance scratch: Vendor-backed, medium capacity, only accessible from compute environment

### 1.5 File Transfer Service (FTS)
- **What:** Secure file transfer with external partners
- **Based on:** VShell Enterprise Server
- **Protocols:** HTTPS, SFTP (supports resume)
- **Contact:** supportrcp@epfl.ch
- **Wiki docs available**

### 1.6 gnoto — GPU-enabled JupyterLab
- **What:** EPFL's noto JupyterLab platform + GPU (collaboration between CEDE and RCP)
- **For:** Education use cases
- **Contact:** CEDE

### 1.7 Dataset Sharing Service (DASh)
- **Status:** Coming soon (listed on wiki)
- **Wiki:** https://wiki.rcp.epfl.ch/en/home/DASh

### 1.8 Vault as a Service (VaaS)
- **Status:** Listed on wiki, authorization required
- **Wiki:** https://wiki.rcp.epfl.ch/en/home/VaaS (restricted)

---

## 2. PRICING / BILLING MODEL

### Billing structure
- **Pay per use** — all services
- **Three pricing tiers:** U1, U2, U3 (escalating cost levels based on what's included)
  - **U1** = direct costs only (salaries, energy, depreciation of short-lived goods)
  - **U2** = U1 + other direct costs (maintenance, depreciation of long-lived equipment)
  - **U3** = U2 + indirect costs (admin, central services, rent, overhead)

### GPU Cluster (CaaS) Pricing — from official Sept 2024 grid

| Resource | U1 (direct) | U2 (+ maintenance) | U3 (full cost) |
|----------|-------------|---------------------|----------------|
| **H100 GPU*h** | **0.543 CHF** | 0.567 CHF | 0.688 CHF |
| H100 Core*h | 0.00272 CHF | 0.00352 CHF | 0.00440 CHF |
| H100 GB*h | 0.00029 CHF | 0.00039 CHF | 0.00049 CHF |
| **V100 GPU*h** | **0.135 CHF** | 0.174 CHF | 0.207 CHF |
| V100 Core*h | 0.00307 CHF | 0.00515 CHF | 0.00607 CHF |
| **A100 GPU*h** | **0.295 CHF** | 0.317 CHF | 0.383 CHF |
| A100 Core*h | 0.00237 CHF | 0.00354 CHF | 0.00431 CHF |

### HaaS Server Pricing (per server per day)

| Server Type | U1 | U2 | U3 |
|-------------|-----|-----|-----|
| Standard | 6.40 CHF/d | 10.00 CHF/d | 12.32 CHF/d |
| Middle-End | 4.46 CHF/d | 8.04 CHF/d | 9.95 CHF/d |
| High-End | 7.29 CHF/d | 10.90 CHF/d | 13.74 CHF/d |
| Big-Mem | 13.49 CHF/d | 17.17 CHF/d | 24.14 CHF/d |

### Storage Pricing
| Type | U1 | U2 | U3 |
|------|-----|-----|-----|
| NAS-RCP (10PB) | **20.75 CHF/TB/year** | 91.79 CHF/TB/year | 111.32 CHF/TB/year |
| Object Storage S3 | 29 CHF/TB/year | - | - |

### AI Inference
- Billed per token, prices on Model Hub (portal)
- Prices displayed are U1; U2/U3 calculated at billing time

### Invoice schedule
- Storage: Once a year in October
- GPU & servers: Quarterly (Q4 split: one invoice early Dec, one early Jan)
- Per-project invoicing available on request

### Free tier / credits
- **EPFL Master Students: 4,000 CHF free credits** — managed by Head of Unit through RCP Portal
- **Test period for GPU cluster:** Not charged during initial onboarding — billing starts once you're comfortable

---

## 3. SERVICES RELEVANT TO CITY101

### 3a. VM / Server Provisioning (Windows for headless Rhino)
**Best option: HaaS (Hardware as a Service)**
- Bare metal servers, dedicated to your unit
- "Can be for any needs you may have, including specific software accessibility, specific simulations, tests"
- Explicitly for "workloads not suitable to run as VM within the VSI cluster operated by DSI"
- **Cost at U1:** ~6.40 CHF/day for Standard server = ~192 CHF/month
- **Windows support:** Not explicitly mentioned on public pages. The servers are bare metal, so OS choice likely negotiable. **Must ask RCP directly.**
- **Note:** DSI also runs a VSI (Virtual Server Infrastructure) cluster for VMs — RCP's HaaS is for when that doesn't fit. Worth asking about both.

### 3b. GPU Access (for embeddings, LLM inference)
**Two options:**

1. **AIaaS (AI Inference as a Service)** — BEST FIT for our needs
   - Already has **embedding models** available via API (/v1/embeddings endpoint)
   - Already has **reranking models** (/v1/rerank)
   - OpenAI-compatible API — drop-in replacement for our existing code
   - No need to manage infrastructure
   - Can request specific models (e.g., if we need a particular embedding model)
   - **Per-token billing** — very cost-efficient for our volume (~35K chunks)
   - Available to all EPFL employees, just need an API key from portal

2. **GPU Cluster (CaaS)** — if we need to run our own models
   - More control, custom Docker images
   - Interactive jobs: 1x A100 for 12h at a time
   - A100 GPU: ~0.30 CHF/hour at U1 = ~7 CHF for a 24h embedding run
   - Better for batch processing of our full knowledge base

### 3c. API Services
**AIaaS is the API service** — this is what you saw mentioned:
- Endpoint: `https://inference.rcp.epfl.ch/v1` (internal) or `https://inference-rcp.epfl.ch/v1` (external)
- OpenAI-compatible API: chat completions, completions, embeddings, reranking, audio transcription
- 70+ models including Qwen, Llama, Mistral, Apertus
- Can even run Claude Code against it (documented on wiki!)
- API key from RCP Portal, max 5 parallel requests (expandable)

### 3d. Storage
- **NAS-RCP:** 20.75 CHF/TB/year at U1 — absurdly cheap for our ~35K chunks (~few GB)
- Multi-protocol (NFS, SMB) — accessible from Mac, Linux, Windows
- Or just use the compute scratch storage if only needed during processing

### 3e. No managed database services
- RCP does not appear to offer managed databases (PostgreSQL, etc.)
- SQLite on NAS or HaaS server is our path

---

## 4. HOW TO REQUEST ACCESS

### General contact
- **Email:** supportrcp@epfl.ch
- **Portal:** https://portal.rcp.epfl.ch (requires EPFL login, Microsoft SSO)
- **Wiki:** https://wiki.rcp.epfl.ch/en/home

### Onboarding process (GPU Cluster)
1. Check if your Unit is already onboarded (ask professor/admin)
2. If not: email supportrcp@epfl.ch to request onboarding
3. RCP creates: NAS3 scratch space, Run:AI department, rcp-runai-<unit> group
4. New users added to the rcp-runai-<unit> group at https://groups.epfl.ch/
5. **Master students:** Request 4,000 CHF free credits via RCP Portal
6. After group sync (couple hours), user is ready
7. Follow Standard Tutorial or Fast-Track Tutorial on wiki

### Monthly onboarding sessions
- Location: AI Center lounge, ELE 117
- Frequency: Once a month (check events page)
- Bring laptop, individual help provided
- Also available: per-lab sessions, associated campus sessions

### HaaS request
- Via RCP Portal self-service

### AIaaS access
- Open to every EPFL employee
- Get API key from RCP Portal (EPFL network or VPN required)
- No onboarding session needed

### File Transfer Service
- Contact supportrcp@epfl.ch

---

## 5. KEY LINKS & DOCUMENTATION

| Resource | URL | Access |
|----------|-----|--------|
| RCP Main Website | https://www.epfl.ch/research/facilities/rcp/ | Public |
| RCP Wiki (full docs) | https://wiki.rcp.epfl.ch/en/home | Public (some pages restricted) |
| RCP Portal (self-service) | https://portal.rcp.epfl.ch | EPFL login (VPN) |
| Run:AI Scheduler | https://rcpepfl.run.ai/ | EPFL login |
| Container Registry | https://registry.rcp.epfl.ch/ | EPFL login |
| Pricing Grid PDF | https://www.epfl.ch/campus/services/finance/wp-content/uploads/2024/09/Grille-RCP-validee-1.pdf | Public |
| CaaS Wiki | https://wiki.rcp.epfl.ch/en/home/CaaS | Public |
| HaaS Wiki | https://wiki.rcp.epfl.ch/en/home/HaaS | Public |
| AIaaS Wiki | https://wiki.rcp.epfl.ch/en/home/AIaaS | Public |
| AI Inference API (internal) | https://inference.rcp.epfl.ch/v1 | EPFL network |
| AI Inference API (external) | https://inference-rcp.epfl.ch/v1 | API key |

---

## 6. RCP TEAM CONTACTS

| Person | Role | Email |
|--------|------|-------|
| Prof. Martin Jaggi | Chair & Academic Director | martin.jaggi@epfl.ch |
| Khadidja Malleck | Operational Director | khadidja.malleck@epfl.ch |
| Nicolas Barriere | Infrastructure Architect | supportrcp@epfl.ch |
| Miguel Fontes Medeiros | Systems Engineer | supportrcp@epfl.ch |
| Yoann Moulin | Infrastructure Architect | supportrcp@epfl.ch |

**Governance steering committee includes Alexandre Alahi from ENAC** — could be a useful connection since we're ENAC students.

---

## 7. RECOMMENDATIONS FOR OUR EMAIL

### What to ask for:

1. **AIaaS API key** — immediate, free, self-service via portal. Use for embedding pipelines and LLM inference. This replaces our Gemini dependency with on-prem EPFL infrastructure.

2. **HaaS bare metal server** — for headless Windows + Rhino. Key question: **Do they support Windows OS on HaaS?** The page says "specific software accessibility" is a valid use case. At ~6.40 CHF/day (U1), a month is ~192 CHF — well within the 1,200 CHF budget.

3. **Master student credits** — 4,000 CHF free credits, managed by Head of Unit via portal. Ask if this applies to BA6 students or only Master level.

4. **Unit account question** — Confirm that LDM (Media x Design Lab) is the correct unit, or if it should go through ENAC more broadly.

### What we probably don't need:
- GPU Cluster (CaaS) — AIaaS covers our inference needs without Docker complexity
- NAS-RCP storage — our data is small enough for local + git
- File Transfer Service — not transferring with external partners
