# Case Collection: Agentic AI Workflows in Architecture, Urban Design, and Construction

**Collected:** 2026-03-05
**Purpose:** Supporting evidence for research paper on agentic AI workflow patterns in architectural practice
**Method:** Web search across conference proceedings, firm websites, tech blogs, and press coverage
**Exclusions:** Heatherwick Ge-Code, ZHA + Omniverse, Arup King's Cross R8, IAAC HyperBuilding, ICD Stuttgart (pavilions pre-2024), Gramazio Kohler, Vectorworks Text2BIM, Autodesk Forma (general), QGIS GIS Copilot

---

## Summary Table

| # | Firm/Lab | Project or Tool | Year | Pattern | Scale | Tools |
|---|----------|----------------|------|---------|-------|-------|
| 1 | Thornton Tomasetti CORE studio | CORE.AI — MCP agents for structural engineering | 2025 | Blackboard | Single building | Strands SDK, AWS AgentCore, Glean, Cortex, custom ML |
| 2 | Foster + Partners ARD | Cyclops — real-time environmental analysis | 2025 | DAG | Single building / Campus | Rhino, Grasshopper, NVIDIA OptiX, CUDA C++ |
| 3 | Foster + Partners ARD | Ask F+P — LLM knowledge search | 2024 | Supervisor | Practice-wide | LLM (custom), Stable Diffusion, internal design guides |
| 4 | SOM | West Bund Convention Centre — AI multi-objective facade optimization | 2025 | DAG | Single building | Custom algorithms, multi-criteria optimization |
| 5 | KPF Urban Interface | Scout + CityBot — generative urban design | 2020-2025 | DAG | Urban / District | Custom generative engine, web apps, ML workflows |
| 6 | Augmenta | Agentic Design Environment — automated electrical routing | 2025 | Supervisor | Single building | Revit, generative AI, clash detection |
| 7 | SWAPP | AI co-pilot for construction documentation | 2024 | DAG | Single building | Revit, ACC, Design Decision Language |
| 8 | Dusty Robotics | FieldPrinter 2 — autonomous BIM-to-field layout | 2024 | DAG | Single building | BIM, autonomous mobile robot, FieldPrint Platform |
| 9 | Boston Dynamics + Foster + Partners | Spot — autonomous construction site monitoring | 2020-2024 | Blackboard | Single building | Spot robot, 3D laser scanning, digital twin |
| 10 | Woods Bagot | SUPERSPACE + CIVITAS — AI-driven spatial analytics | 2023-2025 | Blackboard | Urban / Campus | Data science, ML, custom urban search engine |
| 11 | Archistar | Urban Copilot + eCheck — AI zoning compliance | 2024 | Supervisor | Urban | GenAI, regulatory NLP, generative 3D, Autodesk Forma |
| 12 | ICON | Vulcan + Vitruvius + BuildOS — AI-driven 3D-printed construction | 2024 | Supervisor | Single building | Robotic 3D printing, ML, predictive analytics |
| 13 | Finch3D | AI generative floor plan copilot | 2024 | DAG | Single building | Rhino, Revit, Grasshopper, graph-based generation |
| 14 | TestFit | Generative Design for building optimization | 2024 | DAG | Single building | Computational AI, site solver |
| 15 | Perkins and Will | AI design experiments — iterative rendering + massing | 2024 | Blackboard | Single building | Midjourney, custom rendering app, massing tools |
| 16 | CITA Copenhagen | Adaptive robotic fabrication with ML | 2024 | Blackboard | Fabrication / Component | Robotic arms, ML models, sensor feedback |
| 17 | Autodesk | Neural CAD + Autodesk Assistant (agentic) | 2025 | Supervisor | Practice-wide | Forma, Revit, generative AI foundation models, MCP |
| 18 | Sidewalk Labs (Google) | Delve — generative urban masterplanning | 2020-2024 | DAG | Urban / District | ML, cloud computation, financial modelling |
| 19 | Morphosis | Combinatorial Design Studies with GANs | 2023-2024 | DAG | Single building | GANs, computational geometry, environmental analysis |

---

## Detailed Entries

### 1. Thornton Tomasetti CORE studio — CORE.AI

**Project:** CORE.AI initiative — converting structural engineering tools into MCP (Model Context Protocol) servers and building custom AI agents using AWS Strands SDK and AgentCore. Also deployed Glean.com as an enterprise RAG/search solution connected to Cortex endpoints, testing whether LLMs can autonomously use structural engineering tools (truss design, column stacks, steel bays, shear walls).

**Year:** 2025

**Pattern:** Blackboard. Multiple specialized ML tools (each solving a specific structural problem) are exposed as MCP endpoints on a shared workspace. An LLM agent queries these tools as needed, with the shared context (the building model and engineering constraints) serving as the blackboard that coordinates tool invocation. No fixed pipeline — the agent decides which tool to call based on the engineering question.

**Tools:** AWS Strands SDK, AWS AgentCore, Glean.com (RAG), Cortex endpoints, custom ML models for structural design (inference in milliseconds vs. minutes for classical solvers), T2D2 (damage detection via computer vision)

**Scale:** Single building (structural engineering scope)

**Key insight:** The MCP-as-interface pattern lets a firm expose decades of specialized engineering tools to LLM agents without rewriting them — the agent becomes an orchestrator over a toolbox that already exists.

**Sources:**
- [CORE studio — Thornton Tomasetti](https://www.thorntontomasetti.com/core-studio)
- [Engineering Intelligence — Sergey Pigach, CDFAM](https://cdfam.com/engineering-intelligence-sergey-pigach-core-studio-thornton-tomasetti/)
- [Why CORE Studio is a Model for the Future — TRXL](https://www.trxl.co/leadership-edge-trxl-205/)

---

### 2. Foster + Partners ARD — Cyclops

**Project:** Cyclops, a free Grasshopper plugin for real-time environmental analysis (daylight autonomy, solar radiation, sky component, sunlight hours, shading mask). Built with CUDA C++ and NVIDIA OptiX ray-tracing engine. Computes up to 10 billion rays/second and 4 million views/minute on NVIDIA RTX PRO GPUs — 800 to 10,000x faster than CPU-based Radiance.

**Year:** 2025 (public beta release)

**Pattern:** DAG. The workflow is a pipeline: 3D model geometry feeds into GPU-accelerated raytracing, which feeds into performance metrics, which feeds back into the designer's iteration loop. Each stage has a clear input/output dependency.

**Tools:** Rhino, Grasshopper, NVIDIA OptiX, CUDA C++, NVIDIA RTX PRO 6000 Blackwell

**Scale:** Single building to campus/masterplan

**Key insight:** By collapsing multi-hour environmental simulations into real-time feedback, Cyclops shifts performance analysis from a validation gate at the end of design to a continuous co-design agent embedded in the modelling environment.

**Sources:**
- [Cyclops — Foster + Partners](https://cyclops.fosterandpartners.com/)
- [Foster + Partners NVIDIA RTX case study](https://www.nvidia.com/en-us/case-studies/foster-partners/)
- [Foster + Partners launches Cyclops — press release](https://www.fosterandpartners.com/news/foster-plus-partners-launches-cyclops-plugin-to-enhance-sustainable-design)

---

### 3. Foster + Partners ARD — Ask F+P

**Project:** Ask F+P, an internal LLM-powered search application that lets staff interrogate all design guides using natural language queries. Also deployed a locally hosted Stable Diffusion instance as a plugin for design software, allowing designers to generate photorealistic suggestions on top of existing 3D models.

**Year:** 2024

**Pattern:** Supervisor. A central LLM orchestrates retrieval from a corpus of design knowledge (guides, standards, precedents) and routes answers to the requesting designer. The LLM acts as a supervisor over the firm's accumulated knowledge base.

**Tools:** LLM (custom/local), Stable Diffusion (locally hosted), internal design guides, Rhino/Grasshopper

**Scale:** Practice-wide (knowledge management across 1,800+ staff)

**Key insight:** The "institutional memory" problem in large firms — where knowledge is distributed across thousands of documents and people — is exactly what RAG-based supervisor agents solve. Ask F+P makes the firm's collective design intelligence queryable.

**Sources:**
- [Foster + Partners R&D: AI and digital twins — Construction Management](https://constructionmanagement.co.uk/foster-partners-rd-taking-ai-and-digital-twins-to-the-next-stage/)
- [Applied R+D team — Foster + Partners](https://www.fosterandpartners.com/people/teams/applied-rplusd)

---

### 4. SOM — West Bund Convention Centre

**Project:** AI-assisted multi-objective optimization workflow for the 60,000 sqm West Bund Convention Centre in Shanghai. The design team defined constraints (site dimensions, room heights, program) and six competing objectives (occupant views, floor space, solar exposure, etc.). AI tested hundreds of facade variations, evaluating trade-offs that conflict (e.g., glass angle improves visibility but reduces lighting). Saved weeks of design time.

**Year:** 2025 (design), announced December 2025

**Pattern:** DAG. A staged pipeline: define constraints, encode six objectives, run multi-criteria optimization over hundreds of variations, human review of Pareto-optimal results, select and refine. Each stage feeds forward.

**Tools:** Custom algorithms, multi-objective optimization, proprietary in-house AI tools (under development)

**Scale:** Single building (60,000 sqm convention centre)

**Key insight:** The human role shifts from generating options to defining rules and judging results — the AI handles the combinatorial explosion of trade-offs that no human could manually test. SOM describes it as "AI as an aid to architectural thinking."

**Sources:**
- [SOM uses AI to design diamond-like convention centre — Dezeen](https://www.dezeen.com/2025/12/19/som-west-bund-convention-centre-shanghai/)
- [AI convention center designed by AI — CNN](https://edition.cnn.com/2025/12/02/style/shanghai-west-bund-convention-center-som-hnk-intl-dst)

---

### 5. KPF Urban Interface — Scout + CityBot

**Project:** Computational methodology ("Generative Design") producing tens of thousands of urban design schemes, with data science and ML workflows for analysis. Scout is an interactive 3D web platform for exploring design options across metrics (FAR, greenspace, park proximity, transit access). CityBot was a Twitter bot that let the public tweet urban design preferences and receive generated schemes.

**Year:** 2020-2025 (ongoing development)

**Pattern:** DAG. Generative engine produces design variants, ML evaluates performance metrics, web interface presents ranked options. A sequential pipeline from generation to evaluation to stakeholder selection.

**Tools:** Custom generative engine, data science/ML pipelines, Haystack (urban data exploration), web applications

**Scale:** Urban / District (masterplanning, Silicon Valley, multiple city projects)

**Key insight:** By generating tens of thousands of options and privileging performance over form, KPFui demonstrates that urban design can be treated as a search problem — the role of the designer shifts to defining what "good" means rather than producing individual schemes.

**Sources:**
- [The Smart(er) City — KPF Urban Interface](https://ui.kpf.com/smarter-city)
- [Scout — KPF Urban Interface](https://ui.kpf.com/scout)
- [CityBot — KPF Urban Interface](https://ui.kpf.com/citybot)
- [KPFui launches new tools — KPF](https://www.kpf.com/news/kpfui-launches-new-tools-for-public-engagement-with-urban-design)

---

### 6. Augmenta — Agentic Design Environment

**Project:** AI-powered platform that automates electrical raceway routing and coordination in construction. Analyzes Revit models and generates clash-free, constructible conduit routes optimized for length, bend degrees, installation time, and cost. First building constructed with AI-designed electrical system: Mt. Hope Elementary School, Lansing, Michigan (25% faster design, 15% less material waste).

**Year:** 2025

**Pattern:** Supervisor. A central AI agent orchestrates the entire routing process: it reads the Revit model (architectural + structural context), identifies all electrical loads, generates routes, checks for clashes against all disciplines, and outputs construction-ready models. The AI supervises the full design-to-fabrication pipeline for one discipline.

**Tools:** Revit, Autodesk Construction Cloud, generative AI, clash detection, schedule generation

**Scale:** Single building (tested on elementary schools through data centres)

**Key insight:** The first verified case of AI-designed building systems actually getting built. Augmenta proves that agentic AI can handle not just design exploration but construction-ready output — closing the gap between generative design and buildability.

**Sources:**
- [Agentic AI accelerates electrical design — AEC Magazine](https://aecmag.com/mep/agentic-ai-accelerates-electrical-design)
- [Augmenta unveils agentic design environment — GlobeNewsWire](https://www.globenewswire.com/news-release/2025/09/11/3148579/0/en/Augmenta-Unveils-Comprehensive-Agentic-Design-Environment-Making-AI-Powered-Design-a-Reality-for-Electrical-Contractors.html)
- [Mt. Hope Elementary — first AI-designed electrical system](https://www.globenewswire.com/news-release/2025/08/05/3127404/0/en/Powered-by-Augmenta-Mt-Hope-Elementary-Becomes-America-s-First-Building-with-an-AI-Designed-Electrical-System.html)
- [Augmenta at Autodesk University 2025](https://www.autodesk.com/autodesk-university/class/When-Augmentas-AI-Joins-the-Project-Team-Lessons-Learned-from-Real-World-AEC-to-Construction-with-AI-Workflows-2025)

---

### 7. SWAPP — AI Construction Documentation Co-pilot

**Project:** Firm-specific AI that learns each office's BIM standards and automates Revit deliverables — views, annotations, schedules, full DD/CD drawing sets. Uses a proprietary Design Decision Language (DDL) that encapsulates architectural rules linked to user-specific data, libraries, and building details. MOREgroup achieved a 5.5x increase in square footage handled after integration.

**Year:** 2024

**Pattern:** DAG. A pipeline: onboarding (learn firm standards from past Revit models) produces "recipes," which are applied to new projects in a sequence: model analysis, view generation, annotation, schedule creation, drawing set assembly. Each stage has clear dependencies on the previous.

**Tools:** Revit, Autodesk Construction Cloud, proprietary DDL engine

**Scale:** Single building (documentation phase)

**Key insight:** SWAPP targets the most labor-intensive and least creative phase of architecture (DD/CD documentation), where 40-70% time reduction has immediate business impact. The DDL approach — learning firm-specific rules rather than generic standards — is what makes it adoptable.

**Sources:**
- [SWAPP.ai](https://swapp.ai/)
- [Swapp: the algorithmic assistant — AEC Magazine](https://aecmag.com/ai/swapp-the-algorithmic-assistant/)
- [Swapp: the AI co-pilot — AEC+Tech](https://www.aecplustech.com/blog/swapp-the-ai-co-pilot-for-construction-documentation)

---

### 8. Dusty Robotics — FieldPrinter 2

**Project:** Autonomous mobile robot that translates BIM 3D models into full-scale 2D layout drawings printed directly on construction site floors. Achieves 1/16-inch accuracy, 10,000-15,000 sqft/day with one operator (75% faster than two-person manual crew). FieldPrint Platform provides end-to-end BIM-to-field workflow.

**Year:** 2024 (FieldPrinter 2 launched January 2024)

**Pattern:** DAG. A strict pipeline: BIM model extraction, coordinate transformation, path planning, robotic execution, field verification. Each stage feeds the next with no feedback loops during execution.

**Tools:** BIM (Revit/Navisworks), custom path planning, autonomous mobile robot, total station integration

**Scale:** Single building (construction phase)

**Key insight:** The BIM-to-field gap is where most construction errors originate. Dusty closes it by making the digital model literally print itself onto the building site — the robot is the final agent in a DAG that starts in the architect's software.

**Sources:**
- [Dusty Robotics](https://www.dustyrobotics.com/)
- [Dusty introduces FieldPrinter 2 — TechCrunch](https://techcrunch.com/2024/01/23/dusty-introduces-a-new-version-of-its-construction-layout-robot/)
- [Skanska case study — Dusty Robotics](https://www.dustyrobotics.com/customer-stories/skanska-case-study)

---

### 9. Boston Dynamics + Foster + Partners — Spot for Construction Monitoring

**Project:** Spot robot deployed at Battersea Roof Gardens (Phase 3 of Battersea Power Station redevelopment) for autonomous weekly construction site scanning. Captures 360-degree photos and 3D laser scans on repeatable missions, feeding data into a digital twin that compares design intent to as-built reality. Increased efficiency by 30%.

**Year:** 2020-2024 (ongoing deployment)

**Pattern:** Blackboard. The digital twin serves as a shared workspace (blackboard) that multiple agents write to and read from: Spot writes scan data, the BIM model provides design intent, comparison algorithms flag deviations, and human project managers consume the analysis. No fixed pipeline — Spot's missions can be reconfigured based on what the blackboard reveals.

**Tools:** Spot (quadruped robot), 3D laser scanning, 360-degree cameras, BIM, digital twin platform, Orbit (mission management)

**Scale:** Single building (large mixed-use development)

**Key insight:** The robot is not autonomous in the architectural sense — it does not make design decisions. But it closes the feedback loop between digital model and physical reality at a frequency (weekly) that was previously impossible, making the digital twin a living document rather than a snapshot.

**Sources:**
- [Foster + Partners collaborates with Boston Dynamics](https://www.fosterandpartners.com/news/foster-plus-partners-collaborates-with-boston-dynamics-to-monitor-construction-progress-with-spot)
- [Boston Dynamics — Foster + Partners case study](https://bostondynamics.com/case-studies/foster-partners/)
- [Spot in construction — AEC Magazine](https://aecmag.com/reality-capture-modelling/spot-in-construction-boston-dynamics/)

---

### 10. Woods Bagot — SUPERSPACE + CIVITAS

**Project:** SUPERSPACE is Woods Bagot's internal research and technology group fusing data science, AI, and ML into the design practice. CIVITAS is a search engine for urban conditions. Together they replace traditional area/space analysis with experiential analysis — mapping data across scales (cities, economies, clients, buildings, end-users) to create "user briefs" driven by data rather than assumptions.

**Year:** 2023-2025

**Pattern:** Blackboard. Multiple data sources (demographics, transport, climate, economics, user surveys) feed into a shared analytical workspace. Different ML models read from this workspace to produce spatial recommendations, urban condition assessments, and design briefs. The shared data environment coordinates the agents rather than a fixed pipeline.

**Tools:** Custom data science platform, ML models, interactive web tools, urban data APIs

**Scale:** Urban / Campus

**Key insight:** SUPERSPACE demonstrates the "blackboard for urban intelligence" pattern — instead of a single generative model, multiple specialized analytical agents contribute to a shared understanding of a site's conditions, and the design brief emerges from their collective output.

**Sources:**
- [SUPERSPACE — Woods Bagot](https://www.woodsbagot.com/enterprise/superspace)
- [Innovation — Woods Bagot](https://www.woodsbagot.com/innovations/)
- [Woods Bagot — NVIDIA customer story](https://www.nvidia.com/en-us/customer-stories/advancing-architectural-simulations-and-real-time-collaboration/)

---

### 11. Archistar — Urban Copilot + eCheck

**Project:** AI-powered platform for urban planning and zoning compliance. Urban Copilot uses GenAI to interpret regulations and assist with development applications. eCheck automates zoning compliance review by reading submitted drawings and evaluating them against digitized building/zoning codes, producing compliance reports in minutes. Over 130,000 active users, 850,000 sites assessed, 11 million designs generated in 2024 alone. Piloted across 13 NSW councils and with Queensland State Government.

**Year:** 2024

**Pattern:** Supervisor. A central AI orchestrates the workflow: ingest site parameters and zoning rules, generate compliant massing options, evaluate against code, produce compliance report. The AI supervises the entire feasibility-to-compliance pipeline.

**Tools:** GenAI (regulatory NLP), generative 3D design, Autodesk Forma integration, web platform

**Scale:** Urban (city-wide zoning, district planning)

**Key insight:** Archistar proves that regulatory compliance — architecture's most tedious constraint satisfaction problem — is a natural fit for supervisor agents. By digitizing zoning codes into machine-readable rules, the AI can generate and evaluate simultaneously, collapsing a process that typically takes weeks into minutes.

**Sources:**
- [Archistar — reflecting on a landmark year](https://www.archistar.ai/blog/reflecting-on-a-landmark-year/)
- [Urban Copilot — press release](https://www.prnewswire.com/apac/news-releases/artificial-intelligence-revolutionizing-urban-planning-with-new-urban-copilot-302289872.html)
- [City of Surrey deploys eCheck](https://www.archistar.ai/blog/city-of-surrey-partners-with-archistar-to-fully-deploy-ai-powered-echeck-for-zoning-compliance-and-enhanced-permitting-process/)

---

### 12. ICON — Vulcan + Vitruvius + BuildOS

**Project:** Integrated robotic construction system combining hardware (Vulcan 3D printer, Magma mixer), materials (Lavacrete), and software (BuildOS for print planning + ML, Vitruvius for AI-assisted home design). El Cosmico project in Marfa, TX (2024) and Austin Mueller community (2025) showcase architectural forms (domes, arches, vaults) only possible with 3D printing.

**Year:** 2024

**Pattern:** Supervisor. BuildOS acts as the central orchestrator: it takes architectural geometry, generates toolpaths, manages the robotic printer in real-time, and uses predictive analytics to adjust for material behavior. Vitruvius sits upstream as an AI design agent. The entire chain — from design through fabrication — is supervised by software.

**Tools:** Vulcan robotic 3D printer, BuildOS (CAD + ML + print control), Vitruvius (AI design), Lavacrete (proprietary material)

**Scale:** Single building (residential, up to 3,000 sqft)

**Key insight:** ICON represents the tightest coupling of AI design and robotic fabrication in the cases studied. The same software system that helps design the house also controls the robot that prints it — eliminating the translation gaps that plague conventional design-to-construction workflows.

**Sources:**
- [ICON Technology](https://www.iconbuild.com/technology)
- [ICON unveils next-gen 3D printer](https://www.iconbuild.com/newsroom/icon-unveils-its-next-gen-3d-printer-and-introduces-house-zero-designed-by-lake-flato-architects)
- [ICON's 3D printer extrudes a 100-home neighborhood — Singularity Hub](https://singularityhub.com/2024/08/11/icons-enormous-3d-printer-extrudes-a-new-100-home-neighborhood/)

---

### 13. Finch3D — AI Generative Floor Plan Copilot

**Project:** Generative AI copilot for architects that automates floor plan generation using a patented graph-based system ("Finch Graph") describing architectural relationships between rooms and objects. Generate Floor Plate 2.0 algorithm provides control, transparency, and precision. Integrates with Revit, Rhino, and Grasshopper.

**Year:** 2024

**Pattern:** DAG. A pipeline: architect defines building envelope and unit mix, Finch Graph encodes spatial relationships, generative algorithm fills floors with optimized layouts, architect reviews and iterates. The graph-based approach creates a clear dependency chain from constraints to generated plans.

**Tools:** Rhino, Revit, Grasshopper, proprietary graph-based generative engine

**Scale:** Single building (focused on multi-family residential)

**Key insight:** The "Finch Graph" is a domain-specific language for spatial relationships — it captures what architects intuitively know about how rooms relate but rarely formalize. By making this knowledge explicit and computational, Finch turns floor plan design into a well-defined optimization problem.

**Sources:**
- [Finch3D](https://www.finch3d.com/)
- [Finch3D advances AI floor plan generator — Architosh](https://architosh.com/2024/09/finch3d-advances-ai-based-floor-plan-generator/)
- [Finch Graph Rules — Medium](https://medium.com/finch3d/introducing-finch-graph-rules-revolutionizing-the-design-process-for-architects-2082d7d127bb)

---

### 14. TestFit — Generative Design for Building Optimization

**Project:** Computational AI that tests site solutions autonomously based on project requirements. Users define targets (FAR, parking ratio, yield on cost), and the AI generates and evaluates options. Launched June 2024 as a major platform update.

**Year:** 2024

**Pattern:** DAG. Sequential pipeline: define site constraints and targets, AI generates building configurations, evaluate against metrics, rank and present options. Straightforward staged processing.

**Tools:** Proprietary computational AI, web platform, BIM export

**Scale:** Single building (site planning and feasibility)

**Key insight:** TestFit automates the "test fit" — the speculative massing exercise that developers and architects use to evaluate site feasibility. By making this AI-driven, it compresses a week-long manual process into minutes and removes the bias of testing only a handful of schemes.

**Sources:**
- [TestFit launches generative design](https://www.testfit.io/news/testfit-launches-groundbreaking-generative-design-for-better-building-optimization)
- [Top generative design tools for AEC — AEC+Tech](https://www.aecplustech.com/blog/top-generative-design-tools-aec-how-far-have-they-come)

---

### 15. Perkins and Will — AI Design Experiments

**Project:** Over 30 AI experiments applying cutting-edge technologies to real-world design challenges. Key tool: an iterative rendering application that produces images from simple massing models, allowing incremental changes without wholesale redesign. Also conducted structured research on AI integration in early design phases (81% of architects wanted to incorporate AI after workshops).

**Year:** 2024

**Pattern:** Blackboard. Multiple AI tools (rendering, massing analysis, text generation) contribute to a shared design workspace. No single orchestrator — different experiments feed different parts of the design process, and the firm's Design Process Innovation Lab curates which tools are adopted.

**Tools:** Midjourney, custom iterative rendering application, massing tools, various AI experiments

**Scale:** Single building (early design phases)

**Key insight:** Perkins and Will's approach is notable for its experimental rigor — 30+ controlled experiments with before/after surveys. This is the closest to a scientific method for evaluating agentic AI's impact on design quality rather than just speed.

**Sources:**
- [Beyond Imagery: AI in Architectural Design — SmithGroup](https://www.smithgroup.com/perspectives/2024/beyond-imagery-the-application-of-ai-to-architectural-design)
- [Amplifying Creativity — Perkins and Will](https://perkinswill.com/news/amplifying-creativity-the-role-of-ai-in-our-design-process/)
- [Perkins and Will Research Journal vol. 16.01](https://webcontent.perkinswill.com/research/journal/issue_28_vol1601/issue_28_pwrj_vol1601_4_advantages_challenges_and_perceptions_in_using_ai_generative_images.pdf)

---

### 16. CITA Copenhagen — Adaptive Robotic Fabrication with ML

**Project:** Research on machine learning as an emerging modelling paradigm for architectural fabrication. ML enables shortcutting the costly setup of digital integrated design-to-fabrication workflows, making them more adaptable. Focus on programmable structures that respond to their environment through sensing and actuation, and on adaptive fabrication for conditions of material inconsistency (e.g., incrementally formed metal panels).

**Year:** 2024 (FABRICATE 2024, hosted by CITA)

**Pattern:** Blackboard. Sensor data, material behavior models, and robotic control systems all write to and read from a shared state. The ML model learns material inconsistencies in real-time and adjusts fabrication parameters — a classic blackboard pattern where the shared workspace (material state + robot state) coordinates multiple agents (sensors, ML model, robot controller).

**Tools:** Robotic arms, ML models, sensor systems, custom fabrication control software

**Scale:** Fabrication / Component

**Key insight:** CITA's contribution is the insight that material itself is an agent in the fabrication process — its inconsistencies and behaviors must be sensed and responded to in real-time, not predicted and controlled from a fixed plan. This makes the blackboard pattern essential.

**Sources:**
- [CITA — Royal Danish Academy](https://royaldanishacademy.com/en/CITA)
- [FABRICATE 2024 — Creating Resourceful Futures](https://royaldanishacademy.com/en/calendar/fabricate-2024-creating-resourceful-futures)
- [Adaptive Robotic Fabrication for Material Inconsistency — Danish Research Portal](https://adk.elsevierpure.com/en/publications/adaptive-robotic-fabrication-for-conditions-of-material-inconsist)

---

### 17. Autodesk — Neural CAD + Autodesk Assistant

**Project:** "Neural CAD" — a new category of 3D generative AI foundation models that Autodesk claims could automate 80-90% of routine design tasks. Autodesk Assistant evolving from chatbot to fully agentic AI that automates tasks across Autodesk products, third-party tools, and APIs. Plans to connect to Trusted MCP servers. Deeply integrated into BIM workflows through Forma.

**Year:** 2025 (announced at Autodesk University, Nashville)

**Pattern:** Supervisor. Autodesk Assistant is explicitly designed as a central orchestrator that connects across Autodesk products, third-party tools, and APIs. It receives natural-language instructions and delegates to specialized sub-systems (Forma for planning, Revit for BIM, etc.).

**Tools:** Autodesk Forma, Revit, generative AI foundation models, MCP servers, Autodesk Construction Cloud

**Scale:** Practice-wide (entire design-to-construction lifecycle)

**Key insight:** Autodesk's bet on "neural CAD" represents the platform vendor's vision of agentic AI: a single assistant that spans the entire AEC lifecycle. The MCP server architecture is significant — it means the agent can potentially orchestrate any tool that exposes an MCP endpoint, not just Autodesk products.

**Sources:**
- [Autodesk University 2025 — Cadalyst](https://blog.cadalyst.com/architecture-infrastructure-construction-solutions/autodesk-university-2025-a-connected-ai-powered-future-for-aeco)
- [Shaping the future of your agentic AI partner — Autodesk AEC blog](https://www.autodesk.com/blogs/aec/2025/12/08/shaping-the-future-of-your-agentic-ai-partner/)
- [Autodesk shows its AI hand — AEC Magazine](https://aecmag.com/features/autodesk-shows-its-ai-hand/)
- [Agentic AI for Civil 3D — Autodesk](https://www.autodesk.com/blogs/aec/2025/11/17/agentic-ai-developments-for-autodesk-assistant-in-civil-3d/)

---

### 18. Sidewalk Labs (Google) — Delve

**Project:** AI-based generative design tool for urban masterplanning. Used cloud computation and ML to sort through competing project considerations (density, daylight, amenity access, infrastructure) while accounting for priorities, constraints, and site context. Built-in financial models for individual segments and utility demand estimation (electricity, waste, water, solar). Operational 2020-2024; absorbed into Google Earth team 2022, disabled May 2026.

**Year:** 2020-2024

**Pattern:** DAG. Pipeline: define site constraints and priorities, generative engine produces millions of design possibilities, ML evaluates performance, financial model scores viability, ranked options presented to planners. Clear staged processing with each phase feeding the next.

**Tools:** ML, cloud computation, financial modelling, utility demand estimation, web platform

**Scale:** Urban / District (masterplanning)

**Key insight:** Delve is significant as a cautionary tale: a technically impressive agentic urban design tool that was ultimately absorbed and discontinued by its parent company (Google). Demonstrates that technical capability alone does not guarantee market survival — the business model and organizational context matter as much as the AI.

**Sources:**
- [Delve — Sidewalk Labs](https://www.sidewalklabs.com/products/delve)
- [Sidewalk Labs creates ML tool for designing cities — Dezeen](https://www.dezeen.com/2020/10/20/delve-sidewalk-labs-machine-learning-tool-cities/)
- [Sidewalk Labs reimagines urban planning — ArchDaily](https://www.archdaily.com/949392/sidewalk-labs-reimagines-urban-planning-with-new-delve-generative-design-tool)

---

### 19. Morphosis — Combinatorial Design Studies with GANs

**Project:** Tom Mayne and the Morphosis studio developed Combinatorial Design Studies using Generative Adversarial Network (GAN) technology to generate output that "could never be predicted." The approach uses AI to develop operational strategies that go beyond parametric variation into genuinely novel formal territory, combined with environmental data analysis for performance optimization.

**Year:** 2023-2024

**Pattern:** DAG. The GAN workflow is a pipeline: training data (precedent designs) feeds the GAN, which generates novel design candidates, which are evaluated against environmental performance criteria, and promising candidates are selected for development. The adversarial training process itself is a two-agent system (generator vs. discriminator).

**Tools:** GANs, computational geometry tools, environmental analysis software

**Scale:** Single building

**Key insight:** Morphosis's use of GANs targets the "surprise" dimension of design — generating forms that architects would not have conceived themselves. This positions AI not as an optimizer (finding the best version of what you already imagined) but as a genuine creative collaborator producing the unexpected.

**Sources:**
- [Top Architecture Firms Leading AI Innovation — Consulting for Architects](https://www.cons4arch.com/top-architecture-firms-leading-the-future-of-ai-innovation-in-design/)
- [BIG and IE University AI in Architecture challenge — referencing Morphosis GAN work](https://www.ie.edu/school-architecture-design/challenges/exploring-impact-opportunities-ai-big-architects/)

---

## Pattern Distribution Summary

| Pattern | Count | Cases |
|---------|-------|-------|
| **DAG** (pipeline/staged) | 9 | Cyclops, SOM, KPFui, SWAPP, Dusty, Finch3D, TestFit, Delve, Morphosis |
| **Supervisor** (centralized orchestration) | 5 | Ask F+P, Augmenta, Archistar, ICON, Autodesk Assistant |
| **Blackboard** (shared workspace) | 5 | CORE.AI, Spot+F+P, Woods Bagot, CITA, Perkins and Will |

**Observations:**
- DAG dominates in tools and products (clear input/output contracts make them shippable).
- Supervisor emerges when a single AI must coordinate multiple sub-systems end-to-end (compliance, fabrication control, enterprise knowledge).
- Blackboard appears in research labs and on construction sites — wherever the problem is too messy or unpredictable for a fixed pipeline (material behavior, evolving construction state, multi-source urban data).
- Several cases are hybrids: Autodesk's vision combines supervisor (Assistant) with DAG (Neural CAD pipelines); ICON combines supervisor (BuildOS) with DAG (design-to-print pipeline).

---

## Gaps and Opportunities for Further Research

1. **Missing voices:** No cases from Africa, South America, or South/Southeast Asia found in this search. Agentic AI in architecture appears heavily concentrated in North America, Europe, and Australia.
2. **Construction vs. design:** The construction-phase cases (Dusty, Spot, Augmenta) are arguably more mature than the design-phase cases, likely because construction has clearer success metrics (accuracy, speed, cost).
3. **Multi-agent coordination:** True multi-agent systems (where agents negotiate with each other) are rare. Most "agentic" tools are single-agent systems that call tools. ICD Stuttgart's reinforcement learning for multi-robot coordination is the closest to genuine multi-agent architecture.
4. **Regulatory AI:** Archistar's zoning compliance work suggests a large untapped domain — building codes, accessibility standards, fire regulations — where supervisor agents could be highly effective.
