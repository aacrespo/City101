# Topology Decisions Log

---

## 2026-03-26 — Framework choice: medical guidelines, not legal

**Decision:** Use the medical guidelines model (guideline + case notes + review board) instead of the legal framework (law + doctrine + jurisprudence).

**Why:** The legal framework allows jurisprudence to override statute — a single court ruling can change the effective law. That's dangerous for a knowledge base where base values are extracted from verified source code. One bad review shouldn't change a value.

Medical guidelines work differently: a guideline doesn't change from one adverse case. Case notes accumulate context-specific observations. Only when a pattern emerges across multiple cases (3+) does the review board consider updating the guideline. The practitioner (agent) reads both the guideline and relevant case notes, makes a judgment call.

**Decision:** Separate project from rhinobase-iboisbase. Test during lock modeling, not before midterm.

**Why:** This is infrastructure that changes how /rhino-review works. Changing that during midterm prep is risky. But lock modeling sessions post-midterm are the perfect test bed — real geometry, real reviews, real case notes. Phase 2 costs zero extra time because it piggybacks on modeling.
