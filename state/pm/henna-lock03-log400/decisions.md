# Decisions Log — henna-lock03-log400
# Append-only

---

## 2026-03-27 — Project created

**Decision**: 2-phase structure (Spec Roundtable → Full Build)
**Why**: Lock 03 is empty in Rhino. Building from scratch at LOG400 requires a spec that resolves the missing roof geometry before any Rhino calls are made. The lock 01 pattern (plan → roundtable → execute) proved effective and avoids mid-build conflicts.

**Decision**: Phase 0 uses Hierarchical topology (3 agents)
**Why**: The roof design for the inclined track enclosure has no precedent in the existing prompts. An Architect + Engineer pair working in parallel, synthesized by a Coordinator, produces better geometry decisions than a single agent. Flags can be raised and resolved before the spec is finalized.

**Decision**: Phase 1 uses a single executor (Flat topology)
**Why**: Rhino MCP calls are sequential. Multiple agents competing to write to the same Rhino instance creates conflicts. One executor with batched Python scripts is faster and more reliable.

**Decision**: Rhino instance `interior` (port 9003) confirmed for lock 03
**Why**: The original prompt specifies `target: "lock_03"` but the router maps to instance name. User confirmed port 9003. Instance name in router is `interior`. All Phase 1 calls must use `target: "interior"`.

**Decision**: Tower crown NOT given a solid roof
**Why**: The original prompt explicitly specifies "open top or lattice structure at crown." At LOG400 this means modeling the lattice members (4 columns + X-bracing), not a roof slab. This differentiates the tower from the station volumes.
