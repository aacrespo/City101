# 6. The Frontier

Three capabilities that the extended architect needs but that do not yet exist — or exist only in embryonic form. These are research directions, not proposals. Each is grounded in something observed during City101 or the Lock builds, extended to where it points.

## 6.1 Spatial experience reasoning

City101 found that the Nyon–Gland gap is "19.3km — too far to walk, too short for a separate ticket." That sentence contains a judgment no current tool can make. COMPAS can plan an assembly sequence. Rhino.Compute can measure a distance. A GIS agent can calculate travel time. But none can judge that 19.3km *breaks the experience of continuity* — that it is simultaneously too long for pedestrian connection and too short to justify a separate transit fare, creating a gap that is economically irrational and experientially real.

This is spatial experience reasoning: agents that understand not just the geometry of a place but what it feels like to be in it, to move through it, to wait in it. Jan Gehl's distinction between necessary activities (functional, weather-independent), optional activities (dependent on spatial quality), and social activities (emergent from the presence of others) provides a framework. A station platform at 8am — all necessary activities, commuters in transit — is a fundamentally different space than the same platform at 11pm, when the absence of optional and social activities means the space has failed. The geometry hasn't changed. The experience has.

Space Syntax offers computational tools for part of this — network centrality predicts pedestrian volumes, morphological analysis correlates spatial configuration with movement patterns. But these operate on configuration, not experience. The 42-fold frequency variation along the City101 corridor (Lausanne at 28.5 trains/hr, St-Saphorin at 0.0) is not a spatial configuration problem — it's an experiential one. A 2-minute wait at Lausanne means the train is part of your walking rhythm. A 37-minute wait at Bossière means you need architecture: a chair, coffee, shelter, WiFi.

The frontier is tools that reason about temporal experience — the rhythm of stops, the duration of waits, the quality of in-between time — as design parameters, not just measurements. These tools do not yet exist.

## 6.2 Computational narrative

City101's most significant outputs are not datasets but arguments. "5 break dimensions" led to "archipelago" which led to "two corridors on the same tracks" which led to "160,000 ghost citizens." No single agent produced this narrative arc. The question is whether the connective tissue between findings — the argument that links a Shannon diversity analysis to a temporal frequency map to a GA pricing model — can be structured computationally.

Rittel's IBIS (Issue-Based Information System) provides the vocabulary: Issues (questions), Positions (possible answers), Arguments (evidence for or against). D-Agree, developed at Nagoya Institute of Technology, demonstrates that AI can extract IBIS structure from unstructured discussion — labeling contributions as issues, positions, or arguments and driving toward group consensus.

Software engineering's Architecture Decision Records (ADRs) capture individual decisions with context, alternatives, and consequences. But architecture needs something ADRs don't provide: the sustained argument that connects decisions into a coherent whole. City101's narrative arc is not a collection of independent decisions. It is a chain: the corridor appears continuous but functions as an archipelago → the pattern is structural, not temporal → the cause is a combination of frequency, pricing, workspace, and connectivity gaps → the 160,000 frontaliers who disappear at 18:00 are the human consequence. Each finding depends on the previous.

City101's CONTEXT.md — a living document updated each session with findings, patterns, and open questions — is a primitive version of computational narrative. The frontier is tools that formalize the argumentative links between independent analyses, so that agents can not only produce findings but trace their implications through a design argument. Rittel's IBIS, extended with spatial data and temporal evidence, points the direction. The tools do not yet exist.

## 6.3 Craft knowledge formalization

The piseur problem, restated: how do you encode the tacit constraints of skilled construction labor without flattening them?

The parametric script model (§4.1, Layer 3) can encode some craft knowledge as geometric constraints. A rammed earth wall script that raises a `ConstraintViolation` when the height-to-thickness ratio exceeds 8:1 is useful. But the constraint "maximum compaction reach is 600mm" is not the same as understanding *why* that constraint exists — which means an agent enforcing it can't adapt it to context, can't explain tradeoffs, and can't recognize when the constraint should be relaxed (a shorter wall on stable ground with experienced labor might tolerate a thinner section).

Scripts enforce but can't explain. They encode the *what* (the limit) without the *why* (the builder's experience that produced the limit). And as argued in §2, there is reason to believe that some craft knowledge is not just hard to formalize but *functionally resistant* to formalization — that the irregularity of human construction may produce materially better outcomes than robotic precision.

The frontier is formalization that preserves the builder's judgment: knowledge representations rich enough to carry the reasoning behind constraints, not just the constraints themselves. This is not a solved problem in any domain. It is the deep research question beneath the extended architect.
