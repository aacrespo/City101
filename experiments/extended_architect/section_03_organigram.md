# 3. The Organigram as Design Instrument

If the cost of domain presence collapses — if having a structural agent, a buildability agent, a sustainability agent in the room costs tokens instead of consulting fees — then a new question appears: *which* domains should be present, *when*, with *what* communication between them? The answer is no longer dictated by who the project can afford. It is a design decision.

The organigram becomes a design instrument.

## Three tunable dimensions

Through the City101 case study and the Lock builds, three independent dimensions of organizational topology emerged as configurable:

**Communication topology: hierarchical or flat.** In a hierarchical topology, every information flow passes through a coordinator. The architect (or lead agent) receives inputs from each specialist and synthesizes. No specialist talks to another directly. This is controllable — the coordinator holds all context and makes all decisions — but it creates a bottleneck: if the structural agent discovers something relevant to the buildability agent, the information must route through the coordinator, who must understand both domains well enough to relay it accurately.

In a flat topology, specialists communicate directly. The structural agent messages the buildability agent without routing through the lead. Cross-domain discoveries — the kind that produce the unexpected correlation, the constraint nobody anticipated — emerge from this lateral communication. But coordination overhead increases. More communication channels means more potential for conflicting instructions, duplicated work, or scope drift.

**Context scope: broad or narrow.** Each agent — or each specialist, in human terms — can see everything or only what's relevant to their domain. Broad context means the structural agent sees the sustainability data, the buildability constraints, the spatial intentions. It can make connections across domains. It can also get overwhelmed, distracted, or opinionated about things outside its competence. Narrow context means the structural agent sees only the geometry and the loads. It stays focused. It also misses the cross-domain collision that would have been obvious if it could see the energy model.

**Task dependency: sequential or parallel.** Even within a flat communication topology, some tasks depend on others. The facade detail cannot be resolved before the structural grid is established. The MEP routing depends on the floor-to-floor height. Task dependencies encode a temporal hierarchy — what must come before what — that is independent of the communication topology. A team can have flat communication (everyone talks to everyone) with strict sequential tasks (but you can't start the facade until the structure is done). Or hierarchical communication (everything through the lead) with parallel tasks (structure and envelope develop simultaneously, the lead mediates conflicts).

These three dimensions are independent. They create a design space, not a spectrum. And in agentic workflows, each can be reconfigured per phase, per task, per afternoon.

## Phase-adaptive reconfiguration

The most effective topology is not fixed. It changes as the nature of the work changes.

**Discovery phases** — when the project is moving from brief to analysis, when the question is "what is this site, what are its constraints, what are the possibilities" — favor a flat, broad, parallel configuration. Communication between domains is open. Each agent sees enough context to make cross-domain connections. Tasks run in parallel because the goal is coverage, not convergence.

City101's corridor analysis operated in this mode. Multiple agents — analyst, cartographer, visualizer — worked the same datasets with broad context and lateral communication. The archipelago finding — that the Geneva–Villeneuve corridor functions as an archipelago of workable stations rather than a continuous line — was not in any agent's task specification. It emerged from the spatial joining of datasets produced independently: transit frequency, remote work infrastructure, diversity metrics. The correlation (r = 0.63–0.71) between these independently produced measures of urban completeness was a cross-domain discovery that a hierarchical topology, routing every finding through a human coordinator, would likely have missed — or at least delayed.

**Production phases** — when the project moves from design to documentation, when the question shifts from "what could this be" to "make this precise and consistent" — favor a hierarchical, scoped, sequential configuration. A coordinator ensures coherence across deliverables. Each agent sees only its domain to prevent interference. Tasks follow dependencies to maintain consistency: the structural drawings are coordinated before the MEP drawings reference them.

The Lock 05 build operated closer to this mode. Seven agents, each assigned to a distinct layer group in a single Rhino file, producing 709 objects across four rounds. The communication was mediated through a coordinator. The context was scoped — each agent saw its own layers and a shared reference, not the full model. The task sequence was structured: terrain first, then buildings, then infrastructure. This produced coherent geometry because the topology matched the task: parallel production within a coordinated frame.

**The transition between modes** is itself a design decision. In the SIA model, the transition from avant-projet (preliminary design) to projet (detailed design) implies an organizational shift — the team expands, the hierarchy deepens, the communication becomes more formal. But the SIA model doesn't specify *how* to make that transition or *when* exactly the topology should shift. In practice, it happens gradually and often too late — the team is still in discovery mode when production discipline is needed, or the hierarchy tightens before exploration is complete.

Agentic workflows make the transition explicit and rapid. Reconfiguring a team from flat to hierarchical takes minutes, not months. This means the topology can shift within a single design session — flat and broad for the morning's exploration, hierarchical and scoped for the afternoon's production. The organigram becomes a living parameter, adjusted as the work demands, not a fixed structure inherited at project inception.

## The Inverse Conway Maneuver for architecture

Conway's Law says the building will mirror the team structure. The Inverse Conway Maneuver says: design the team structure to produce the building you want.

Want a deeply integrated building — a Passivhaus where structure, envelope, and systems are inseparable, where the thermal bridge at every junction is resolved, where the airtightness layer is continuous through every material transition? Structure the team for dense cross-disciplinary communication from Phase 0. Flat topology, broad context, every domain seeing every other domain's constraints. The collisions surface early. The integration happens in sketch, not in coordination meetings.

Want a modular building — a housing development with standardized units, where the structure is independent of the facade, where apartments can be reconfigured without touching the building systems? Structure the team around discrete scope packages. Hierarchical topology, narrow context, minimal inter-agent communication. Each domain develops its system independently. The interfaces are clean because the team structure enforces separation.

This is not a metaphor. It is a design method. The organigram — who communicates with whom, who sees what, what depends on what — produces the building as surely as the floor plan does. An architect who designs the organigram with the same intentionality as the plan is practicing at a level that traditional project management does not reach. The SIA's concept of *direction générale* — overall project leadership as a design act — finds its fullest expression here: the architect as designer of the organization that produces the building, not just occupant of a position within it.

## What the City101 system architecture demonstrates

The City101 project went through seven versions of its system architecture specification in three weeks. Each version represented a different organizational topology tested against real production tasks. The evolution — from ad hoc parallel work (two students with independent agent instances producing overlapping datasets) to a coordinated multi-role team (defined roles, scoped contexts, explicit communication channels, a lockboard tracking who is working on what) — mirrors, in compressed form, the professionalization of a design office.

This rate of iteration is the point. Reorganizing a human design team takes months. Reorganizing an agent team takes minutes. The compressed feedback loop — configure topology, produce work, observe the output, reconfigure — makes the organigram testable in a way it has never been before. The seven versions of the City101 system architecture are seven experiments in organizational design, each with observable consequences for the quality, coherence, and coverage of the analytical output.

The organigram is no longer drawn once and lived with. It is iterated, like a floor plan.
