# Email Draft — EPFL RCP Services Request

**To:** supportrcp@epfl.ch
**CC:** Alexandre Sadeghi (alexandre.sadeghi@epfl.ch), Monique Amhof (monique.amhof@epfl.ch)
**From:** Andrea Crespo (andrea.cresposalas@epfl.ch)
**Subject:** RCP services for AI-assisted architectural modeling — LDM, AR-302k

---

Hi,

I'm a BA6 architecture student in Professor Jeffrey Huang's Sentient Cities studio (AR-302k, LDM). Alex Sadeghi (CC'd) recommended I contact you — this work will be included in the LDM unit account. Monique Amhof (CC'd) can confirm.

We've built an AI-assisted modeling pipeline where LLM agents build 3D geometry in Rhino via MCP (Model Context Protocol). We're interested in three RCP services:

**1. HaaS — Headless Rhino instances**
We need bare metal servers running Windows with headless Rhino + our custom MCP server, so our routing system can distribute modeling work across instances. 3–4 Standard servers would cover our 9 corridor sites.

Key question: **Can HaaS servers run Windows?** Rhino requires it.

**2. AIaaS — Embedding and inference**
We have a construction knowledge base (~35K chunks from Swiss building standards, technical references, PDFs) that we need to embed and query. The /v1/embeddings and /v1/rerank endpoints look like exactly what we need. We'd also use chat completions for agent workflows.

Can we get an API key? And which embedding models are currently available on the platform?

**3. Credits — Student eligibility**
We saw that Master students can receive 4,000 CHF in free credits via the portal. Does this apply to BA6 (Bachelor) students as well? Our approved project budget is 1,200 CHF, but credits would extend what we can do.

I have a detailed cost sheet with full infrastructure specs — happy to share. Our midterm is March 30, so any guidance on timeline would be very helpful.

Best regards,
Andrea Abril Crespo Salas & Henna Rafik
EPFL BA6 Architecture — AR-302k, Studio Huang (LDM)

---

*Attachment: Funding Request — AI-Assisted Architectural Modeling Infrastructure.pdf*
