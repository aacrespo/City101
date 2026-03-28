# Multi-Model Infrastructure Strategy
## Sentient Cities Studio — EPFL LDM / AR-301(k)
### Andrea & Henna | March 2026

---

## 1. Why Multi-Model

The current workflow runs entirely on Claude (Anthropic). This creates three risks:

1. **Single point of failure** — When Anthropic's servers go down, all 10+ parallel agent sessions stop. No amount of budget can fix this; you wait.
2. **Cost concentration** — Every task, from complex design reasoning to simple text formatting, costs the same premium rate.
3. **Vendor lock-in** — If Anthropic changes pricing, rate limits, or API terms, the entire pipeline is affected overnight.

A multi-model architecture solves all three by distributing tasks across providers based on capability, cost, and availability.

---

## 2. The Current Model Landscape (March 2026)

### Tier 1: Frontier Proprietary Models

These are the strongest available but require API payment and depend on external servers.

| Model | Provider | Strengths | Best For | Cost Range |
|-------|----------|-----------|----------|------------|
| **Claude Opus 4.6** | Anthropic | Deep reasoning, architecture planning, complex debugging, safety alignment | Core orchestration, design decisions, complex Rhino/Blender scripting | $15/$75 per 1M tokens |
| **Claude Sonnet 4.6** | Anthropic | Fast, strong coding, good balance | Daily coding tasks, agent loops | $3/$15 per 1M tokens |
| **Claude Haiku 4.5** | Anthropic | Very fast, cheap, reliable for simple tasks | High-frequency queries, formatting, simple text processing | $1/$5 per 1M tokens |
| **GPT-5.2** | OpenAI | Strong reasoning, multimodal, large ecosystem | Alternative reasoning engine, UI generation | $10–21/$30–168 per 1M tokens |
| **Gemini 3 Pro** | Google | Multimodal, long context, integrated with Google tools | Document analysis, image understanding, research | Variable |

### Tier 2: Open-Source / Self-Hostable Models

These can run on EPFL's own servers — independent uptime, no per-token cost (just compute).

| Model | Origin | Parameters | Strengths | Best For |
|-------|--------|------------|-----------|----------|
| **Llama 4 Maverick** | Meta | 400B total (17B active, MoE) | Multimodal, 1M token context, strong coding | General fallback, document processing |
| **Llama 4 Scout** | Meta | 109B total (17B active) | Lightweight, 10M token context, edge-friendly | Long document indexing, lightweight tasks |
| **DeepSeek V3.2** | DeepSeek | 685B (37B active, MoE) | GPT-5 level reasoning, MIT license, strong math/coding | Complex reasoning fallback, mathematical analysis |
| **Qwen 3.5** | Alibaba | Up to 397B (17B active, MoE) | 119 languages, strong coding, multimodal reasoning | Multilingual tasks (FR/ES/EN workflow), code generation |
| **Mistral Large 3** | Mistral (France) | 675B (41B active, MoE) | 40+ languages, GDPR-compliant (European), precise instruction following | European compliance, multilingual, structured outputs |
| **GLM-4.7** | Zhipu AI | — | Top open-source coding (94.2% HumanEval), strong reasoning | Coding agents, scientific reasoning |
| **Mistral Small 4** | Mistral | 24B | Fast, efficient, good instruction following | Real-time tasks, low-latency needs |
| **Phi-3** | Microsoft | 14B | Tiny but strong reasoning, runs on consumer hardware | Edge/laptop deployment, offline work |

### Key Takeaway

The gap between open-source and proprietary models has narrowed dramatically. For most tasks except the most complex reasoning and agentic orchestration, open models are now competitive.

---

## 3. Recommended Architecture

### 3.1 Task Routing Strategy

Not every task needs the most powerful model. Route by complexity:

**Claude Opus 4.6 — The Architect** (keep for highest-value work)
- Design decision reasoning
- Complex multi-step Rhino/Blender scripting
- Knowledge base synthesis and architectural analysis
- CLAUDE.md context injection and agent orchestration
- Overnight autonomous run supervision

**Claude Haiku 4.5 or Sonnet 4.6 — The Workhorse**
- Daily coding tasks, git operations
- RAG query processing against the knowledge base
- Formatting, documentation generation
- Repetitive agent loops (test → fix → test cycles)

**Open-Source Model (EPFL-hosted) — The Backbone**
- Simple text processing and formatting
- Batch processing of repetitive tasks
- Document parsing and extraction
- Basic code generation for routine scripts
- Fallback for all tasks during Claude downtime

**Recommended EPFL-hosted model priority:**
1. **DeepSeek V3.2** — Best reasoning among open models, MIT license, closest to Claude capability
2. **Qwen 3.5** — Excellent multilingual (relevant for FR/ES/EN), strong coding
3. **Mistral Large 3** — European, GDPR-compliant, good instruction following (politically safe choice for Swiss university)
4. **Llama 4 Scout** — Massive context window for document-heavy work

### 3.2 Failover Protocol

The failover system must live *outside* Claude — because if Claude is down, Claude can't manage the switch.

```
FAILOVER CHAIN (automated, Claude-independent):

Level 0: Claude Opus 4.6 (primary)
    ↓ if unavailable (3 failed pings)
Level 1: Claude Sonnet 4.6 (same provider, different model)
    ↓ if unavailable
Level 2: Claude Haiku 4.5 (lightest Anthropic model)
    ↓ if Anthropic entirely down
Level 3: EPFL-hosted model (completely independent infrastructure)
    ↓ if EPFL servers down
Level 4: Graceful degradation — queue tasks, notify team, pause non-critical agents
```

**Implementation approach:**

A health-check script runs independently (cron job or systemd service on EPFL VM):

```
Every 30 seconds:
  1. Ping Anthropic API with lightweight test request
  2. If 3 consecutive failures → set PROVIDER_STATUS=degraded
  3. If Anthropic fully unreachable → set PROVIDER_STATUS=failover
  4. Route all new agent requests based on PROVIDER_STATUS
  5. Log everything for post-incident analysis
```

**Tool: LiteLLM** (recommended)
- Open-source Python proxy that sits between your agents and all LLM providers
- Unified API: write code once, route to any model
- Built-in failover, load balancing, cost tracking
- Supports 100+ models including Anthropic, OpenAI, and self-hosted via vLLM/Ollama
- Can run on EPFL's VM alongside the hosted models
- Config is a simple YAML file defining model priorities and fallback chains

```yaml
# Example LiteLLM config
model_list:
  - model_name: main-model
    litellm_params:
      model: anthropic/claude-sonnet-4-20250514
      api_key: os.environ/ANTHROPIC_API_KEY
  - model_name: fallback-model
    litellm_params:
      model: ollama/deepseek-v3  # EPFL-hosted
      api_base: http://epfl-gpu-server:11434

router_settings:
  fallbacks:
    - main-model: [fallback-model]
  retry_after: 30
```

### 3.3 Context Injection Compatibility

The current CLAUDE.md and agent skill configs are Claude-specific. For multi-model to work:

- Create **model-agnostic versions** of context injection files (simpler prompts, no Claude-specific features)
- Maintain a **translation layer** that adapts prompts to each model's optimal format
- The RAG knowledge base (Qdrant) is already model-agnostic — any model can query it
- YAML tool configs may need model-specific variants for tool-calling syntax differences

---

## 4. What Open Models Bring Beyond Redundancy

### 4.1 Cost Optimization

Running a self-hosted model for routine tasks can reduce API costs by 80–90%. The EPFL-funded VM essentially gives you free compute for these operations. Reserve Claude for the 20% of tasks that genuinely need frontier reasoning.

**Example cost scenario:**
- 10 parallel agents, ~100K tokens/hour each
- At Claude Sonnet rates: ~$18/hour
- Routine tasks (~60% of volume) on EPFL-hosted model: $0/hour
- Effective cost: ~$7.20/hour (60% savings)

### 4.2 Specialized Capabilities

Some open models outperform Claude in specific domains:

- **DeepSeek V3.2-Speciale**: Matches or exceeds Claude on competition-level math (relevant for parametric/structural calculations)
- **Qwen 3.5-VL**: Native vision-language model — could process architectural drawings, site photos, and diagrams directly
- **Mistral OCR**: Best balance of speed and accuracy for document scanning (SIA norms, building codes)
- **GLM-4.7**: Highest open-source coding benchmark scores — could handle IronPython/Grasshopper scripting

### 4.3 Privacy and IP Protection

Self-hosted models keep data on EPFL's servers. For the knowledge base containing copyrighted SIA norms and books (flagged as IP-sensitive), processing these through a local model avoids sending proprietary content to external APIs.

### 4.4 Experimentation and Fine-Tuning

Open-source models can be fine-tuned on your specific domain:
- Train on your architectural vocabulary and conventions
- Optimize for Rhino/Grasshopper/Blender command generation
- Create a model variant specialized in Swiss building code interpretation
- This is not possible with Claude or GPT — you can only prompt-engineer, not retrain

### 4.5 Speed and Latency

For tasks where response time matters more than quality (agent loop iterations, quick validations), a local model on EPFL hardware could be faster than a round-trip to Anthropic's servers, especially during peak usage hours.

---

## 5. Implementation Roadmap

### Phase 1: Reconnaissance (This Week)
- [ ] Ask EPFL (school director / Alex) exactly which models are hosted and on what hardware
- [ ] Get inference key and test basic prompts against EPFL's models
- [ ] Benchmark EPFL model quality on 5–10 representative tasks from current workflow
- [ ] Determine key expiry/renewal process

### Phase 2: Gateway Setup (Week 2–3)
- [ ] Install LiteLLM proxy on EPFL VM (or local machine as test)
- [ ] Configure Claude as primary, EPFL model as fallback
- [ ] Test failover by temporarily using invalid Anthropic key
- [ ] Set up basic cost and usage logging

### Phase 3: Task Router (Week 3–4)
- [ ] Classify current agent tasks into complexity tiers
- [ ] Create model-agnostic prompt templates for Tier 2/3 tasks
- [ ] Route simple tasks to EPFL model, complex tasks to Claude
- [ ] Monitor quality — collect examples where open model underperforms

### Phase 4: Full Integration (Week 4–6)
- [ ] Integrate LiteLLM into GitHub repo and agent orchestration
- [ ] Create Llama/DeepSeek-compatible versions of CLAUDE.md context
- [ ] Build automated health monitoring dashboard
- [ ] Document failover protocol in repo README
- [ ] Test overnight autonomous runs with multi-model routing

### Phase 5: Optimization (Ongoing)
- [ ] Explore fine-tuning open models on architectural domain data
- [ ] Evaluate multimodal models for drawing/image processing
- [ ] Consider adding a second cloud provider (OpenAI/Google) as additional redundancy
- [ ] Track cost savings and production metrics for portfolio/presentations

---

## 6. Crit Talking Points

For the Monday midterm presentation, this multi-model strategy strengthens the infrastructure argument:

1. **Production maturity**: The workflow isn't just "we use AI" — it has redundancy, failover, and cost optimization like a real production system.
2. **Independence**: Not dependent on any single company's servers. If Anthropic disappears tomorrow, work continues.
3. **Cost efficiency**: Junior architect + subscriptions ROI argument is even stronger when routine tasks run on free EPFL compute.
4. **European sovereignty**: Using Mistral (French) on Swiss university servers aligns with European digital autonomy narratives.
5. **The kitchen metaphor**: "We're not just building the kitchen while cooking — we're building a kitchen with backup power generators."

---

## 7. Important Limitation: Claude Code is Claude-Only

The multi-model strategy applies to **API-based agents and batch tasks** — the programmatic layer where we can swap providers via LiteLLM.

**Claude Code itself (the interactive CLI) is locked to Anthropic.** The session you're in right now — with CLAUDE.md injection, slash commands, MCP tools, hooks, agent spawning — all of that is Claude Code infrastructure. It cannot run on GPT or Llama. This is not a limitation we can work around; it's architectural.

What this means in practice:
- **Interactive sessions** (you typing, Claude responding): always Anthropic
- **Subagents spawned by Claude Code**: always Anthropic (they inherit the CLI)
- **API scripts** (batch processing, RAG queries, simple generation): routable to any model
- **Standalone agents** (not using Claude Code features): routable to any model

The failover chain in Section 3.2 should be understood as applying to the API layer. For Claude Code sessions, the failover is: Claude is down → use the human-friendly task breakdown (Section 8 below).

---

## 8. When Claude is Down — ADHD-Friendly Task Breakdown

When Anthropic goes down, you lose all parallel agent capacity. But you don't lose the ability to work. This section maintains a breakdown of tasks that can be done by hand, written for an ADHD brain: small, concrete, no ambiguity.

### The Rules
- Every task fits in one sentence
- No task takes more than 15 minutes
- Each task has a clear "done" state
- Group by energy level (high focus vs autopilot)

### High Focus (design thinking, decisions)
- [ ] Open Rhino → pick one lock → rotate around it → write 3 things that bother you in `claudes-corner/`
- [ ] Read one observation in `observations/research/` → add a one-liner reaction at the bottom
- [ ] Sketch (paper) one alternative for any lock element that feels wrong
- [ ] Review LOCKBOARD.md → cross off anything that's done, add anything new
- [ ] Read the last 5 git commits (`git log --oneline -5`) → do they tell a coherent story?

### Medium Focus (production, tangible output)
- [ ] Open PPTX template → fill one slide with existing content from `deliverables/`
- [ ] Screenshot 3 Rhino viewports of current locks → save to Drive for presentation
- [ ] Open Google Drive → organize exported PNGs/PDFs into presentation folders
- [ ] Review one HTML visualization in browser → note what's missing/wrong in a text file
- [ ] Export one Rhino viewport as PNG at 300 DPI for print deliverable

### Autopilot (low energy, still useful)
- [ ] Open `datasets/INVENTORY.md` → check that every dataset listed actually exists at its path
- [ ] `git status` → are there untracked files? List them in a note for next session
- [ ] Open `LEARNINGS.md` → read through, see if anything clicks or needs updating
- [ ] Browse SIA norm PDFs in Drive → bookmark sections relevant to current locks
- [ ] Clean up Google Drive folders — rename, sort, delete obvious junk

### Session Prep (do before Claude comes back)
- [ ] Write 3 bullet points of what you want to accomplish next session
- [ ] Note any decisions you made while Claude was down (even small ones)
- [ ] If you modified any files by hand, note which ones so Claude can catch up

*This section should be regenerated at every `/session-end` based on current LOCKBOARD state. The above is a template — Claude should replace the task items with current, specific work.*

---

## 9. MCP Tools as Code Libraries

### The Problem
The current MCP setup (Rhino, Blender) loads **every tool definition** into context on session start. The Rhino MCP alone exposes 30+ tools. Blender adds another 30+. Each tool definition is ~200-500 tokens of schema. That's 12,000-30,000 tokens of context consumed before you've done anything — and most sessions only use 3-5 of those tools.

This is the equivalent of `import *` in Python. You wouldn't load every function from every library into memory; you'd import what you need.

### The Analogy
Think of MCP servers the way you think of code libraries:

| Code World | MCP World (current) | MCP World (proposed) |
|------------|---------------------|----------------------|
| `import numpy` | Load all 30 Rhino tools | Load Rhino "index" (list of available tools) |
| `from numpy import array, linspace` | (not possible) | Load only `create_object`, `modify_object`, `execute_python_code` |
| Library docs | Tool schemas in context | Tool schemas fetched on demand |

### Proposed Architecture

**Tier 1 — Always loaded (essential, used every session)**
- `rhino_get_scene_info` — orientation
- `rhino_execute_python_code` — the universal escape hatch
- `rhino_capture_viewport` — visual verification
- `blender_execute_code` — same for Blender
- `blender_get_viewport_screenshot`

**Tier 2 — Loaded on role activation**
- `/modeler` loads: `create_object`, `modify_object`, `boolean_*`, `extrude_curve`, `loft`, `sweep1`, `pipe`
- `/cartographer` loads: nothing extra (uses execute_python_code for GIS)
- `/visualizer` loads: nothing extra (works in HTML, not Rhino)

**Tier 3 — Loaded on demand**
- PolyHaven, Sketchfab, Hyper3D, Hunyuan3D — only when explicitly doing asset generation
- Transfer geometry — only during multi-app workflows

### Implementation Options

1. **Multiple MCP configs**: Create `mcp-minimal.json`, `mcp-modeling.json`, `mcp-full.json`. Switch by copying to `.mcp.json` + restart. Manual but works now.

2. **Router with lazy loading**: Modify the router MCP server to only advertise Tier 1 tools. When a role is activated, dynamically register additional tools. Requires MCP protocol support for dynamic tool registration.

3. **Consolidate into execute_code**: For Rhino, `execute_python_code` can do everything the individual tools do. The individual tools are convenience wrappers. An agent with the playbook knowledge + `execute_python_code` is arguably more capable than one with 30 rigid tool schemas. This is the "one good knife vs. a drawer of gadgets" approach.

### Context Savings Estimate
- Current: ~25,000 tokens for Rhino + Blender tool schemas
- Tier 1 only: ~2,500 tokens
- Savings: ~22,500 tokens per session — that's roughly 10 pages of context freed up

### Next Steps
- Audit which MCP tools are actually used (check git history for tool calls)
- Build the minimal MCP config for daily work
- Test whether `execute_python_code` + playbook can replace individual tool calls
- Consider this for the RhinoCommon knowledge base expansion (rhinobase project)

---

## 10. Open Questions

- What specific models does EPFL host? (Llama? DeepSeek? Mistral? What version?)
- What GPU hardware is available? (Determines which model sizes can run)
- Is the inference key per-student or shared? Rate limits?
- Can we install LiteLLM or other software on the VM, or is it locked down?
- Does EPFL's TTO have any policy on using university-hosted AI for student IP?
- Should we involve Alex (studio assistant) in the technical setup?

---

*Document generated March 28, 2026. Updated same day with Claude-down protocol, MCP optimization, and Claude Code limitation note. Model landscape evolves rapidly — revisit quarterly.*
