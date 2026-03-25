# AI + Architecture Tool Landscape Research

Research scan of seven tools, platforms, and people working at the intersection of AI and architectural design. Compiled for the City101 team as reference material.

*Cairn Code, 2026-03-25*

---

## 1. Pascal Editor

**What:** Open-source, browser-based 3D building editor. No install, no license fees. Built with React Three Fiber and WebGPU, so it renders on the GPU at near-native speed.

**Who:** Maintained by the `pascalorg` GitHub organization. The team keeps a low profile -- no named founder in public materials. The repo is TypeScript, actively updated (March 2026).

**Key capabilities:**
- Draft, model, and collaborate in-browser
- Snap-in library of doors, windows, furniture
- Targets residential design, interior layout, office planning, real estate viz
- Fully open source (github.com/pascalorg/editor)

**Relevance to us:** A free, zero-friction 3D editor that runs in the browser. Could be useful for quick massing or layout explorations without firing up Rhino. Not parametric, not AI-powered -- but the open-source WebGPU architecture is worth watching.

**Links:** [pascaleditor.org](https://pascaleditor.org/) | [GitHub](https://github.com/pascalorg/editor)

---

## 2. Finch 3D

**What:** Generative AI platform for early-stage building design. Uses graph algorithms + architectural logic to auto-generate and optimize floor plans against real constraints (circulation, daylighting, area ratios, code compliance).

**Who:** Founded 2019 in Malmo, Sweden by architects Jesper Wallgren and Pamela Nunez Wallgren, plus software engineer Martin Kretz. Raised ~$4.2M total (seed led by Inventure, Series A by Ampli Ventures). Peter Neubauer (co-founder of Neo4j) is an angel investor.

**Key capabilities:**
- Patented graph-based floor plan generation: maps spatial relationships, then generates layouts
- "Graph Rules" system lets designers encode regulatory/programmatic constraints
- Integrates with Revit, Rhino, and Grasshopper
- Architects maintain creative control; AI handles optimization

**Relevance to us:** Directly relevant to our "flow of people" analysis. Finch thinks about buildings the way we think about the corridor -- as a graph of spatial relationships and movement patterns. Their constraint-based generation approach parallels what our prototypology agents do. Worth testing for housing typology generation along the 101km strip.

**Links:** [finch3d.com](https://www.finch3d.com/) | [ArchDaily interview with Jesper Wallgren](https://www.archdaily.com/929300/can-a-machine-perform-the-work-of-an-architect-a-chat-with-jesper-wallgren-founder-at-finch-3d)

---

## 3. D5 Render

**What:** Real-time ray tracing renderer for architecture, built on Unreal Engine + NVIDIA RTX. Combines rasterization, ray tracing, and real-time path tracing. Free tier available.

**Who:** D5 Render (company based in China). Growing rapidly in the arch-viz market as a competitor to Enscape, Lumion, and Twinmotion.

**Key capabilities:**
- Real-time GI with adaptive sampling (proprietary "D5 GI")
- LiveSync plugins for SketchUp, 3ds Max, Revit, Archicad, Rhino, C4D, Blender
- 10,000+ ready-to-use assets
- AI features: AI Enhancer, AI Atmosphere Match, AI Ultra HD Texture, AI PBR Material Snap, AI Style Transfer, AI Inpainting
- Video, panorama, and still output

**Relevance to us:** The Rhino LiveSync is interesting for quick visualization of our corridor models. The AI material/atmosphere features could speed up presentation renders without leaving the modeling environment. Free tier makes it accessible for a student project.

**Links:** [d5render.com](https://www.d5render.com/) | [ArchDaily profile](https://www.archdaily.com/catalog/us/products/32321/real-time-rendering-software-d5-render)

---

## 4. xFigura

**What:** All-in-one AI sandbox for architectural ideation. Infinite canvas supporting 2D/3D workflows: text-to-image, sketch-to-image, image-to-3D, video generation, upscaling, inpainting, and in-browser 3D massing. Web-based, real-time collaboration.

**Who:** Created by George Guida -- architect, educator, PAACADEMY instructor. Background includes Foster + Partners and Harvard. Connected to the PAACADEMY ecosystem (parametric architecture education).

**Key capabilities:**
- Integrates multiple AI models: SDXL, FLUX, Ideogram, Gemini Flash, SD3
- 3D generation via Tripo, CSM, Rodin, Hunyuan3D 2.0
- Real-time multi-user collaboration
- Designed specifically for early-stage design exploration

**Relevance to us:** This is essentially a collaborative AI sketchpad for architects. The image-to-3D pipeline (using Tripo/Hunyuan3D) is similar to what we explored with our Blender MCP integration. Could be useful for rapid concept visualization in team sessions. The multi-model approach (letting you pick the right AI for each task) is a pattern we should consider for our own workflows.

**Links:** [xfigura.ai](https://paacademy.com/software/xfigura-ai) | [Parametric Architecture feature](https://parametric-architecture.com/xfigura-all-in-one-ai-sandbox/)

---

## 5. Gendo AI

**What:** Browser-based generative AI rendering platform built specifically for architects. Takes 2D drawings/sketches and generates photorealistic renders while maintaining design fidelity.

**Who:** Founded by George Proud (architectural designer/visualizer) and Will Jones (software engineer). London-based. Beta users include Zaha Hadid Architects, KPF, and David Chipperfield Architects.

**Key capabilities:**
- Upload 2D drawings, get photorealistic renders in minutes
- Selective area editing: change wall material or lighting without regenerating entire scene
- Style presets: Cinematic, Hand Sketch, Watercolor, Impressionism
- Design integrity preservation (the AI respects your geometry, not just vibes)

**Relevance to us:** The "selective modification" feature is notable -- most AI rendering tools regenerate everything, losing design intent. Gendo's approach of respecting the architect's geometry while adding materiality and lighting is more trustworthy for professional work. Could be valuable for presentation renders of our corridor analysis diagrams or site proposals. The fact that ZHA and Chipperfield use it signals professional-grade output.

**Links:** [gendo.ai](https://gendo.ai/) | [Architect's Newspaper feature](https://www.archpaper.com/2024/07/gendo-ai-platform-zaha-hadid-architects-david-chipperfield-architects-and-others-for-in-house-cgis/)

---

## 6. Motif (Amar Hanspal)

**What:** Next-generation cloud-native 3D CAD platform for buildings. Aims to replace legacy AEC software (read: Autodesk) with a modern, AI-integrated, cloud-first design platform.

**Who:** Founded 2023 by Amar Hanspal (former Autodesk co-CEO and CPO, 20+ years at Autodesk, then co-founded Bright Machines) and Brian Mathews. Raised $46M in seed + Series A -- led by CapitalG (Alphabet's growth fund) and Redpoint Ventures. Named to Forbes "Next Billion-Dollar Startups" 2025 list.

**Key capabilities:**
- Cloud-native 3D CAD tools with ML/AI integration
- Targeting the full AEC workflow: design, collaboration, sustainability
- Building from scratch (not retrofitting legacy software)
- Still in development -- product not yet publicly available

**Relevance to us:** This is the biggest signal in this list. The former co-CEO of Autodesk raised $46M to build what he thinks Autodesk should have become. He knows exactly where Revit/AutoCAD fall short and is building the replacement. For our thesis on AI extending the architect's integrative capacity, Motif is evidence that industry leadership sees the same gap. Worth tracking closely -- if their platform launches during our project timeline, it could validate (or challenge) our approach.

**Links:** [motif.io](https://www.motif.io/) | [TechCrunch coverage](https://techcrunch.com/2025/01/30/ex-autodesk-execs-snag-46m-to-build-the-next-gen-of-architecture-design/)

---

## 7. Greg Demchak (Bentley Systems)

**What:** VP of Emerging Technologies at Bentley Systems. Leads the iTwin Innovation Lab (iLab), which prototypes how digital twin tech, generative AI, and immersive experiences reshape infrastructure design and construction.

**Who:** Greg Demchak. MIT SMArchS (architecture + design technology). 20+ years in software development. Currently the "resident visionary" at Bentley Systems.

**Key work:**
- iTwin Innovation Lab: combines generative AI with BIM, geospatial data, point clouds, and photogrammetry into unified immersive experiences
- Uses text-to-image AI + edge detection + segmentation to create interactive 3D exhibits
- Advocates for human expertise + generative AI collaboration (not replacement)
- Pushes open architecture for handling large-scale infrastructure data in the cloud

**Relevance to us:** Demchak's work on digital twins for infrastructure corridors is directly parallel to our Geneva-Villeneuve corridor analysis. His approach of combining multiple data types (BIM + geospatial + point clouds) into a single experience mirrors our multi-layer data integration. His framing of AI as amplifier of human expertise (not replacement) aligns with our thesis. Bentley's infrastructure focus (vs. Autodesk's building focus) makes their AI strategy particularly relevant to large-scale corridor/urban analysis.

**Links:** [Bentley blog: iLab + generative AI](https://blog.bentley.com/insights/from-ancient-aqueducts-to-generative-ai-bentleys-ilab-builds-the-future-brick-by-digital-brick/) | [Masters of Innovation podcast](https://www.bentley.com/news/the-future-of-architecture-with-industry-expert-greg-demchak-005-masters-of-innovation/)

---

## Summary: What matters for City101

| Tool/Person | Category | Maturity | Most relevant for |
|-------------|----------|----------|-------------------|
| Pascal Editor | Open-source 3D editor | Usable now | Quick browser-based modeling |
| Finch 3D | Generative floor plans | Production | Typology generation, constraint-based design |
| D5 Render | Real-time rendering | Production | Presentation renders from Rhino |
| xFigura | AI ideation sandbox | Early | Collaborative concept exploration |
| Gendo AI | AI rendering | Beta/Production | Fast presentation renders from 2D |
| Motif | Cloud-native CAD | Pre-launch | Industry direction signal |
| Greg Demchak / Bentley | Digital twin + AI R&D | Research | Infrastructure corridor analysis parallel |

The clearest connections to our work: **Finch** (graph-based spatial reasoning), **Motif** (thesis validation -- industry leaders see the same gap), and **Demchak/Bentley** (infrastructure corridor + AI = our exact territory).
