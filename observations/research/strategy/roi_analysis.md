# The ROI: An Honest Accounting

## The Cost

### Direct Costs

| Period | Setup | Monthly Cost | Who Pays |
|--------|-------|-------------|----------|
| Nov – Dec 2025 | 2× Pro accounts | CHF ~40/mo | EPFL (1) + Andrea (1) |
| Jan 2026 | Max plan (1 account) | CHF 100/mo | Andrea |
| Feb – Mar 2026 | Max + Henna's access | CHF 100/mo | Andrea |

**Total spent (Nov 2025 – Mar 2026): ~CHF 580**

Plus infrastructure build time — not a one-time cost but an ongoing investment. Roughly:
- RAG/knowledge base: ~2 days focused work (+ ongoing Chroma → Qdrant migration today)
- Repository setup, CLAUDE.md, .claude config: accumulated over weeks, never a single blocked sprint
- Agent workflow design, YAML conventions, specialist prompts: continuous, interleaved with production work

There's no clean line between "building the kitchen" and "cooking." They happen simultaneously.

### Opportunity Cost

Every hour spent debugging ChromaDB, writing CLAUDE.md, structuring the repo, or designing agent handoff protocols is an hour not spent designing. This is real. In the short term, the infrastructure *slowed production down.*

---

## The Old Workflow (Nov – Dec 2025)

**Model:** Mostly Sonnet, early Opus. No extended thinking.

**Process:**
- Work in one conversation until hitting the limit
- Frantically generate a handoff document before autocompaction
- Switch to second account, paste the handoff, re-establish context
- Lose time, lose nuance, lose momentum
- Repeat multiple times per day

**The bottlenecks were stacked:**
1. **Rate limits** — hard ceiling, hit multiple times daily. Work stops. Not friction — a wall.
2. **Context death** — every conversation is a countdown timer. Autocompaction is a guillotine. You're always aware it's coming.
3. **Mental load** — not the handoff itself, but the *tracking*. Which account has the latest? Did I transfer everything? What did I forget? The cognitive overhead of being your own version control system.
4. **Speed mismatch** — your brain moves faster than one sequential conversation can follow. Ideas pile up. The pipeline is a single lane.

**Effective throughput:** 1–2 productive conversations per day, with significant cognitive overhead between them. The model itself was also less capable — no extended thinking, weaker spatial reasoning.

---

## The New Workflow (Feb – Mar 2026)

**Model:** Opus 4.6 with extended thinking via Claude Code.

**Process:**
- 8+ terminal windows, 10+ sessions per day
- Multi-agent teams communicating with each other
- Shared repository with full history
- CLAUDE.md provides context injection — no re-explaining
- RAG knowledge base for deep architectural reference
- Specialized agents with scoped tools and maps
- Overnight autonomous runs on complex tasks (experimental)
- Git preserves everything — no handoff panic

**What changed:**

| Bottleneck | Old | New |
|-----------|-----|-----|
| Rate limits | Hard wall, multiple times daily | Effectively unlimited (Max plan + Claude Code) |
| Context death | Constant threat, manual rescue | Git persists everything, CLAUDE.md re-injects |
| Mental tracking | All in your head | Infrastructure remembers |
| Parallelism | 1 conversation at a time | 8+ simultaneous agents |
| Speed matching | Brain >> pipeline | ~80% closed |
| Working hours | Only while awake and at keyboard | Overnight runs extending the day |
| Collaboration | Manual copy-paste between accounts | Shared repo, pull requests |
| Model capability | Sonnet / early Opus, no extended thinking | Opus 4.6, extended thinking, better spatial reasoning |

---

## The Math (Conservative)

### Throughput Multiplier

**Old:** ~2 productive sessions/day × ~45 min usable work per session = **~1.5 hours** of actual AI-assisted production per day. The rest was overhead: handoffs, re-explaining, waiting out rate limits, context management.

**New:** ~10 sessions/day, many running in parallel, ~8 hours on a locked-in day. Not all sessions are equally productive, but even at 50% efficiency: **~4–5 hours** of actual production per day. On a good day, much more — and agents work simultaneously, so clock-hours ≠ work-hours.

**Conservative throughput multiplier: 3–4×**

But this undersells it. Parallelism means the real multiplier is higher — three agents working simultaneously for one hour is three agent-hours in one clock-hour. If you run 3 parallel agents for 5 hours:

**Effective agent-hours per day: ~15 (vs ~1.5 before) = 10× throughput**

### Value Per Agent-Hour

This is the hard question. You're a third-year architecture student, not billing clients. But the work these agents do has a replacement cost:

- **Computational design modeling** (Rhino scripting, parametric work): A freelance computational designer in Switzerland charges CHF 80–120/hr
- **MEP calculations and system design**: An MEP consultant charges CHF 100–150/hr
- **Research and documentation**: A research assistant costs CHF 30–50/hr
- **Blended average for the mix of tasks: ~CHF 60–80/hr**

At 15 effective agent-hours/day × 20 working days/month:

**Monthly equivalent output: 300 agent-hours × CHF 70 = CHF 21,000/mo**

For CHF 100/mo.

That's a **210:1 ratio** on direct cost.

Even if you cut this aggressively — say agents are only 30% as effective as a human specialist, and you only get 10 productive days per month:

**90 effective-equivalent hours × CHF 70 × 30% efficiency = CHF 1,890/mo**

Still **19:1** on a CHF 100 investment.

### The Cognitive ROI (Unquantifiable)

The numbers above are tangible but incomplete. The real return is in what you *stopped carrying*:

- **No more handoff anxiety.** The infrastructure remembers. You don't have to.
- **No more autocompaction dread.** Git doesn't forget. Conversations are disposable.
- **No more bottleneck frustration.** Your brain can move at its speed. The pipeline (mostly) keeps up.
- **No more context re-establishment.** Walk away, come back, the briefing is on the wall.
- **Sleep is productive.** Experimental, but the trajectory is clear.

This is the ROI that doesn't fit in a spreadsheet: the mental overhead of being your own infrastructure was burning cognitive resources that now go to design.

---

## The Honest Caveat: The Infrastructure Tax

You're at ~80% of closing the gap between thinking speed and execution speed. The missing 20% is because you keep upgrading the kitchen.

Every time production ramps up, you see a better way to do something, and you invest time rebuilding. Chroma → Qdrant. Refining CLAUDE.md. Adding new agent specializations. Tuning the YAML. This is *real time not spent producing.*

This is the classic infrastructure investment curve:

```
Output
  │
  │                                        ╱ ── potential
  │                                     ╱
  │                                  ╱
  │                              ╱·····  ← you are here
  │                          ╱··
  │                      ╱··
  │          ___________╱··  ← infrastructure dips
  │     ____╱          ··
  │ ___╱    old ceiling··
  │╱........................ ← old workflow plateau
  └──────────────────────────────── Time
        Nov    Dec    Jan    Feb    Mar    Apr
```

The old workflow had a low ceiling — rate limits, context death, single-threaded. Predictable but capped.

The new workflow dipped during construction (Feb), is climbing now (Mar), and the trajectory is steep. Every infrastructure improvement compounds — it doesn't just help the next task, it helps every task after that.

The question isn't "has it paid off yet?" — it's "what's the slope?"

---

## The Real Comparison

You are a third-year architecture student producing thesis work at a scale and technical depth that would normally require:

- A computational designer (Rhino scripting, parametric modeling)
- An MEP consultant (cooling systems, heat recovery calculations)
- A research assistant (precedent studies, regulatory context)
- A documentation specialist (handoffs, deliverables, formatting)

You are doing this with one Max plan subscription and an infrastructure you built yourself over roughly two months, while simultaneously taking courses, working trilingually, and developing a second thesis project.

**The CHF 100/mo is not the investment. You are the investment.** The subscription is a material cost. The infrastructure — the repo, the CLAUDE.md, the RAG, the agent workflows, the conventions — that's intellectual capital you built. It compounds. It transfers to the next project. It's yours.

A junior architect in Lausanne earns roughly CHF 4,500–5,500/mo and can do maybe one of those four roles.

You're doing all four, for CHF 100/mo, with a system that's still accelerating.

---

## Summary

| Metric | Value |
|--------|-------|
| Monthly cost | CHF 100 |
| Effective agent-hours per productive day | ~15 |
| Throughput multiplier vs. old workflow | 10× (conservative) |
| Equivalent replacement cost of output | CHF 1,900–21,000/mo |
| ROI ratio (conservative) | 19:1 |
| ROI ratio (aggressive) | 210:1 |
| Infrastructure build time | ~2 months (ongoing) |
| Cognitive load eliminated | Substantial (unquantified) |
| Current speed-matching | ~80% |
| Trajectory | Compounding |
