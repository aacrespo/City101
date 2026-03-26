# Relay-Lock Configurator: App Tooling Landscape Research

**Date:** 2026-03-18
**Context:** Current prototype is a 1,572-line single HTML file (`city101_prototypology.html`) using Leaflet, D3, and vanilla JS. Question: what's the smartest path from this prototype to a real app?

---

## 1. GOOGLE AI STUDIO — What It Actually Is

**One sentence:** Google AI Studio is a prompt-testing and API-prototyping console for Gemini models, not an app builder.

**Details:**
- It's the front door to the **Gemini API** — you test prompts, manage API keys, monitor usage, and prototype AI features
- It recently added a "Build mode" (sometimes called "vibe coding") that can generate code, but this is for prototyping AI-powered features, not for building and deploying full web applications
- The workflow is: prototype a prompt in AI Studio, click "Get code," then go build your app elsewhere
- Current models include Gemini 3.1 Pro, Gemini 3 Flash, and Gemini 3.1 Flash-Lite
- Capabilities: function calling, structured output, code execution, grounding with Google Search, long context (millions of tokens)

**Fit for this project: PARTIAL — but not how you might think.**
- NOT useful as an app builder (it's not Bolt.new or v0)
- IS useful for the Phase 2 "AI-powered community research" feature — you could use Gemini API (free tier: generous for prototyping) as an alternative to Claude API for the AI site-analysis feature
- The Gemini API free tier is more generous than Claude API for experimentation
- **Bottom line:** Google AI Studio is where you'd go to prototype the AI features of your app, not to build the app itself

**Cost:** Free for prototyping. Gemini API has a free tier; paid usage is pay-per-token.

---

## 2. AI APP BUILDERS — Can They Build This?

### v0 by Vercel
- **What:** AI-powered app generator that produces React/Next.js code from prompts, deployed to Vercel
- **Fit: PARTIAL** — Good for generating UI components (the spec card, slider panels, dashboard layout). Cannot handle the domain-specific scoring engine, Leaflet integration, Rhino script generation, or custom GeoJSON logic without heavy manual work
- **Key advantage:** Generates real React code you can export and continue developing
- **Key limitation:** Context window limits mean it loses track of complex multi-feature apps; "maximum context limit reached" is a documented issue
- **Cost:** Credit-based, free tier available, ~$20/mo for Pro

### Bolt.new
- **What:** AI app builder with backend infrastructure (databases, auth, hosting) included
- **Fit: PARTIAL** — Best of the AI builders for full-stack needs. Could scaffold the app structure and basic UI. Claims to handle projects "1,000 times larger than before"
- **Key advantage:** Backend infrastructure included (Bolt Cloud) — databases, auth, hosting, custom domains all built in. Closest to a one-stop shop
- **Key limitation:** Domain-specific logic (scoring algorithms, GeoJSON processing, Rhino script templates) will still need manual coding. AI-generated code often needs significant cleanup
- **Cost:** Free (300K tokens/day), Pro $25/mo (10M tokens/mo)

### Lovable
- **What:** AI app builder that generates React + Supabase full-stack apps from descriptions
- **Fit: PARTIAL** — Generates clean React code with Supabase backend. Good for standard web apps
- **Key advantage:** GitHub sync + one-click deploy. Clean React output
- **Key limitation:** Same as others — domain-specific geospatial/architectural features need manual coding. Credit system limits iteration
- **Cost:** Free tier, Pro $25/mo (100 credits/mo)

### Replit Agent
- **What:** AI coding agent inside Replit's online IDE that can build and deploy full-stack apps
- **Fit: PARTIAL** — Can scaffold a full app with database, but same limitations for domain-specific logic
- **Key advantage:** Integrated IDE + deployment. You can manually edit what the AI generates
- **Key limitation:** Performance can be slow. Less control over code architecture. Deployment tied to Replit
- **Cost:** Free tier available, Core plan ~$20/mo

### Claude Artifacts
- **What:** Single-file interactive apps generated in Claude conversations (HTML or React)
- **Fit: YES for prototyping, NO for production** — This is essentially what you already did to build the current prototype
- **Key advantage:** Fast iteration, supports Three.js (r128), D3, Leaflet-compatible HTML
- **Key limitation:** Single-file only, no backend, no persistent storage, Three.js version is old (r128), no deployment
- **Cost:** Included with Claude subscription

### Verdict on AI App Builders

**None of them can build the Relay-Lock Configurator end-to-end.** They're useful for:
- Scaffolding the initial app structure (v0 or Bolt.new)
- Generating UI components (spec cards, sliders, dashboard layouts)
- Setting up basic backend (Bolt.new or Lovable + Supabase)

But the scoring engine, GeoJSON-based site analysis, Rhino script generation, and custom map interactions will need human coding regardless. The risk is spending time fighting the AI builder's assumptions instead of just writing the code.

**Recommended use:** Use v0 or Bolt.new to generate the initial React scaffold and UI components, then take over manually for the domain logic. Or just keep building with Claude Code, which gives you more control.

---

## 3. FRONTEND FRAMEWORKS

### Vanilla JS (current approach)
- **What:** Plain HTML/CSS/JavaScript, no framework
- **Fit: YES for now, limits you later**
- **Advantage:** Zero build step, zero dependencies, works on GitHub Pages, you already have 1,572 lines working
- **Limitation:** At ~3,000+ lines, single-file apps become unmaintainable. No component reuse. State management is manual and error-prone. Adding features like the scoring engine + spec cards + 3D preview in one file will be painful
- **Cost:** Free

### Svelte / SvelteKit
- **What:** Compiler-based UI framework — components compile to minimal JS at build time
- **Fit: BEST OPTION for this project**
- **Advantage:** Closest to vanilla HTML/CSS/JS (uses standard web languages, not JSX). Smallest learning curve from where you are now. Excellent reactivity (sliders updating scores updating map markers — all automatic). Tiny bundle size. SvelteKit adds routing and optional SSR
- **Limitation:** Smaller ecosystem than React (fewer pre-built components). Some Leaflet wrappers exist but aren't as mature
- **Cost:** Free, open source (MIT)

### Vue.js
- **What:** Progressive JavaScript framework with gentle learning curve
- **Fit: GOOD**
- **Advantage:** Approachable for non-JS-specialists. Template syntax is closer to HTML than React's JSX. Single-file components (HTML + CSS + JS in one .vue file) map well to architectural thinking. Good Leaflet ecosystem (vue-leaflet)
- **Limitation:** Slightly more boilerplate than Svelte. Two API styles (Options vs Composition) can be confusing for beginners
- **Cost:** Free, open source (MIT)

### React / Next.js
- **What:** The dominant UI library (React) and its full-stack framework (Next.js, currently v16)
- **Fit: OVERKILL for Phase 1, reasonable for Phase 2**
- **Advantage:** Largest ecosystem. Most AI tools generate React code. Best library support for maps (react-leaflet, react-map-gl, @react-three/fiber). If you ever need SSR, API routes, or image optimization, Next.js has it built in
- **Limitation:** Steepest learning curve. JSX is unfamiliar if you come from HTML. React's mental model (hooks, state, effects, re-renders) requires real investment to learn. Overkill for a tool that's essentially one interactive page
- **Cost:** Free, open source (MIT). Next.js deployment free on Vercel hobby tier

### Recommendation for This Project

**Phase 1 (12 days to midterm):** Stay on vanilla JS. Your 1,572-line prototype works. Polish it, don't rewrite it.

**Phase 2 (April-May, real app):** Migrate to **Svelte + SvelteKit**. Reasons:
1. Closest to what you already know (HTML/CSS/JS, not JSX)
2. Built-in reactivity makes the scoring engine trivial (change a slider -> score updates -> map updates -> spec card updates, all automatically)
3. Tiny output = fast load times
4. SvelteKit can deploy as static site (GitHub Pages) or with server functions (Vercel/Netlify) — grows with you
5. The Svelte compiler catches errors at build time

If AI-generated components matter to you (using v0, Bolt.new), then **React/Next.js** is pragmatically better because that's what every AI tool generates. It's a tradeoff: easier AI scaffolding vs easier manual coding.

---

## 4. LOW-CODE / NO-CODE PLATFORMS

### Streamlit
- **What:** Python framework for building data apps with minimal frontend code
- **Fit: NO**
- **Why not:** Python-only (your existing code is JS). UI is widget-based — you can't build custom map interactions, spec cards, or the scoring visualization you have. No custom CSS control. Your prototype already looks better than anything Streamlit can produce
- **Cost:** Free (open source), free cloud hosting for public apps

### Gradio
- **What:** Python framework for ML model demos with 40+ built-in components
- **Fit: NO**
- **Why not:** Designed for ML model demos, not interactive design tools. Has a 3D model viewer but no map-based site scoring. Same Python limitation as Streamlit
- **Cost:** Free (open source), free hosting on Hugging Face

### Retool
- **What:** Platform for building internal business tools with drag-and-drop UI + database connectors
- **Fit: NO**
- **Why not:** Designed for internal CRUD apps (admin panels, dashboards). No custom map interactions. Locked into their component system. Not designed for public-facing design tools. Student discount available but the platform mismatch is the real issue
- **Cost:** Free for up to 5 users, paid plans for teams. Student discounts available

### Anvil
- **What:** Full-stack Python web framework with visual designer
- **Fit: NO**
- **Why not:** Python-only. Visual designer is for standard form-based UIs. Can't reproduce the map-centric, spec-card-generating, Rhino-script-downloading tool you need
- **Cost:** Free tier, paid plans from ~$30/mo

### Verdict on Low-Code/No-Code

**None of these fit.** Your tool is too spatially-specific and visually custom for any low-code platform. The prototype you already have is more sophisticated than what these platforms can produce for this use case. Skip this entire category.

---

## 5. DEPLOYMENT

### GitHub Pages (current plan)
- **What:** Free static site hosting from a GitHub repo
- **Fit: YES for Phase 1**
- **Advantage:** Free, already integrated with your repo, zero config, custom domain support
- **Limitation:** Static files only — no server-side code, no database, no API routes. When you need the Claude API integration, you'll need something else
- **Cost:** Free

### Vercel
- **What:** Frontend deployment platform, creators of Next.js
- **Fit: BEST for Phase 2**
- **Advantage:** Free hobby tier. Serverless functions for API routes (Claude API proxy, scoring backend). Edge network = fast globally. Git push = auto deploy. Preview deployments for every branch. Works with any framework (Svelte, React, Vue)
- **Limitation:** Serverless function limits on free tier (100GB bandwidth, 1M invocations/mo — plenty for a student project)
- **Cost:** Free (Hobby), $20/user/mo (Pro)

### Netlify
- **What:** Similar to Vercel — static + serverless deployment
- **Fit: GOOD alternative to Vercel**
- **Advantage:** Similar feature set to Vercel. Serverless functions. Form handling built in. Free tier
- **Limitation:** Slightly less integrated with framework ecosystems than Vercel. Credit-based system can be confusing
- **Cost:** Free, $9/mo (Personal), $20/member/mo (Pro)

### Railway
- **What:** Full-stack cloud platform for deploying apps with databases and backends
- **Fit: GOOD for Phase 2 if you need a real database**
- **Advantage:** Easy database setup (Postgres). Full backend deployment. Pay only for what you use. Hard spending limits (unique feature — won't surprise you with a bill)
- **Limitation:** More complex than Vercel/Netlify for a frontend-heavy app. Overkill unless you need persistent server processes
- **Cost:** Free tier, pay-as-you-go after

### Fly.io
- **What:** Cloud platform for running full applications globally
- **Fit: OVERKILL**
- **Advantage:** Global edge deployment, great for latency-sensitive apps
- **Limitation:** More ops work than Vercel/Netlify. Designed for always-on servers, not serverless functions
- **Cost:** Pay for CPU/memory consumption

### Recommendation

**Phase 1:** GitHub Pages. It's free, it works, you're already set up.

**Phase 2:** Vercel. One command to deploy. Serverless functions handle the Claude API proxy (you don't want API keys in client-side code). Free tier is more than enough. If you end up needing a database (multi-user features, saved configurations), add Supabase (free tier: 500MB, 50K monthly active users) — it pairs with any deployment platform.

---

## 6. 3D / SPATIAL LIBRARIES

### Three.js
- **What:** The dominant JavaScript 3D graphics library using WebGL
- **Fit: YES — best for the 3D lock preview**
- **Advantage:** Can load architectural models (glTF, OBJ, FBX). Huge ecosystem. Well-documented. Can render your lock geometry directly. @react-three/fiber (R3F) if you go React. threlte if you go Svelte
- **Limitation:** Learning curve for 3D programming. You'll need to convert Rhino geometry to glTF for web viewing. Performance with complex models requires optimization
- **Cost:** Free, open source (MIT)

### MapLibre GL JS
- **What:** Open-source fork of Mapbox GL JS for vector tile maps with WebGL rendering
- **Fit: YES — best upgrade path from Leaflet**
- **Advantage:** Vector tiles (smoother zoom, better styling). Built-in 3D terrain and building extrusion. Globe view. WebGL-accelerated. Free and open source (unlike Mapbox). Can show 3D buildings and terrain without Three.js. Leaflet migration guide available
- **Limitation:** Needs a vector tile source (MapTiler free tier: 100K tiles/mo, or self-host). More complex setup than Leaflet. Different API from Leaflet (not a drop-in replacement)
- **Cost:** Free (library). Tile hosting: MapTiler free tier or OpenFreeMap (fully free)

### deck.gl
- **What:** GPU-powered framework for large-scale geospatial data visualization
- **Fit: PARTIAL — good for data-heavy visualizations but overkill for 7 lock sites**
- **Advantage:** GPU-accelerated. Handles millions of points. Beautiful data visualization. Integrates with MapLibre, Google Maps
- **Limitation:** Designed for big data visualization, not architectural detail. Steep learning curve. Overkill for 7 sites with a few hundred data points
- **Cost:** Free, open source (MIT)

### CesiumJS
- **What:** JavaScript library for 3D globes and geospatial visualization
- **Fit: NO — wrong scale**
- **Advantage:** Beautiful 3D globe. 3D Tiles support. Terrain streaming. Great for urban-scale visualization
- **Limitation:** Designed for earth-scale to city-scale, not building-scale. Heavy library. The lock configurator needs building-detail 3D, not globe rendering. Cesium ion (tile hosting) is paid for serious use
- **Cost:** Library free (Apache 2.0). Cesium ion: free tier limited, paid for production

### Rhino.Inside
- **What:** McNeel's embeddable Rhino compute kernel — runs RhinoCommon + Grasshopper headless inside any .NET host (web server, Unity, Revit, custom app). No Rhino GUI needed. The geometry engine becomes a library call
- **Fit: YES — Phase 2/3, server-side geometry generation**
- **Advantage:** Instead of generating `.py` Rhino scripts the user downloads and runs locally, the app could call Rhino.Inside on a server and return actual geometry (glTF, mesh, NURBS). Users wouldn't need a Rhino license. Full RhinoCommon API available: booleans, NURBS, meshing, Grasshopper definitions. Could power a "click site → get 3D lock model in browser" flow. Pairs naturally with Three.js viewer on the frontend
- **Limitation:** Requires a **Rhino.Inside license** (~$995 one-time per deployment, or included with Rhino 8+ commercial license). Server needs .NET runtime. Compute-heavy — needs a real server, not serverless functions. McNeel's compute.rhino3d (their hosted version) exists but is meant for Grasshopper definitions, not arbitrary RhinoCommon code. Setup is non-trivial
- **Licensing:** Rhino.Inside is free for development/testing. Production deployment requires a Rhino license per server instance. EPFL may already have institutional licenses that cover this — worth checking with Sébastien (who approved the LAN Zoo licenses)
- **Architecture:** Client (Svelte + Three.js) → API call with site parameters → Server (Rhino.Inside + lock generation logic) → returns glTF → Three.js renders in browser. The parametric scripts you already have (`output/city101_hub/rhino_scripts/`) could run server-side with minimal adaptation
- **Cost:** Free for dev. ~$995/deployment for production (or covered by institutional license). Server hosting: Railway or a small VM ($5-20/mo)

### Recommendation

**Phase 1 (midterm):** Keep Leaflet. It works. Don't touch the map library 12 days before a deadline.

**Phase 2 — Map upgrade:** Switch to **MapLibre GL JS**. You get vector tiles, smooth zooming, 3D terrain, building extrusion, and better styling — all open source. Use MapTiler's free tier or OpenFreeMap for tiles. Your Swiss data (swissBUILDINGS3D, swissALTI3D) can feed 3D terrain/buildings directly.

**Phase 2 — 3D lock preview:** Add **Three.js** for the in-panel lock model viewer. Export your Rhino lock geometry as glTF, load it in a Three.js viewport embedded in the spec card. This is a contained component — doesn't require rewriting the whole app.

If you go Svelte, use **threlte** (Svelte + Three.js wrapper). If React, use **@react-three/fiber**.

---

## 7. THE SMARTEST PATH: PHASE 1 vs PHASE 2

### Phase 1: Next 12 Days (Midterm)

**Do not rewrite anything.** Your prototype works. The goal is a polished demo, not a production app.

| Action | Tool | Time |
|--------|------|------|
| Polish the existing HTML prototype | Vanilla JS (current) | 2-3 days |
| Add the scoring engine + weight sliders | Vanilla JS | 2-3 days |
| Add spec card generation | Vanilla JS + CSS | 1-2 days |
| Deploy to GitHub Pages | GitHub Pages | 30 min |
| Show a compelling demo at midterm | -- | -- |

**Total tech stack:** Vanilla JS + Leaflet + D3 + GitHub Pages. Cost: $0.

### Phase 2: April-May (Real App)

This is when you migrate from prototype to app. Two realistic paths:

#### Path A: Svelte + Manual Build (Recommended)
1. Set up SvelteKit project
2. Break the 1,572-line HTML into components (Map, ScorePanel, SpecCard, LockPreview, ScriptGenerator)
3. Add MapLibre GL JS (replacing Leaflet)
4. Add Three.js lock preview (via threlte)
5. Add Vercel serverless functions for Claude API proxy
6. Add Supabase if multi-user features needed
7. Deploy on Vercel

**Pros:** Full control, clean architecture, fast performance, you learn real web dev
**Cons:** More manual work, steeper initial setup
**Cost:** $0 (all free tiers)

#### Path B: AI-Scaffolded React + Manual Domain Logic
1. Use v0 or Bolt.new to generate the initial React app structure and UI components
2. Take the generated code, set up a proper Next.js project
3. Manually implement scoring engine, map integration, Rhino script generation
4. Add react-map-gl (MapLibre) and @react-three/fiber (Three.js)
5. Deploy on Vercel

**Pros:** Faster initial scaffold, more pre-built components available, React ecosystem is largest
**Cons:** JSX learning curve, AI-generated code needs cleanup, React mental model is complex
**Cost:** v0/Bolt.new subscription $20-25/mo for 1-2 months, then $0

#### Path C: Enhanced Vanilla JS (Minimum Viable)
1. Split the HTML file into modules using ES modules (no build step needed)
2. Keep Leaflet, add Three.js for 3D preview
3. Add a simple Vercel serverless function for Claude API
4. Stay on GitHub Pages or move to Vercel

**Pros:** Least disruption, no framework to learn
**Cons:** Will hit maintainability ceiling if the app grows significantly
**Cost:** $0

### My Recommendation

**Path A (Svelte)** if you want to learn proper web dev and build something genuinely impressive for your portfolio.

**Path C (Enhanced Vanilla)** if time is tight and you just need it to work.

**Path B (React)** only if you specifically want React on your resume or plan to use AI code generation extensively.

Google AI Studio is not relevant as an app builder. It's relevant only for prototyping the Gemini API if you want a free alternative to Claude API for the AI community-research feature in Phase 2.

---

## Quick Reference Table

| Tool | Category | Fits? | Cost | Notes |
|------|----------|-------|------|-------|
| Google AI Studio | AI API console | For AI features only | Free | Not an app builder |
| v0 (Vercel) | AI app builder | Scaffold only | Free / $20/mo | Generates React code |
| Bolt.new | AI app builder | Scaffold + backend | Free / $25/mo | Most complete AI builder |
| Lovable | AI app builder | Scaffold only | Free / $25/mo | React + Supabase |
| Replit Agent | AI app builder | Scaffold only | Free / $20/mo | Integrated IDE |
| Claude Artifacts | AI prototyping | Already using it | Subscription | Single-file limit |
| Svelte/SvelteKit | Framework | BEST FIT | Free | Easiest from vanilla JS |
| Vue.js | Framework | Good | Free | Gentle learning curve |
| React/Next.js | Framework | Overkill Phase 1 | Free | Largest ecosystem |
| Vanilla JS | No framework | Current, fine for now | Free | Maintainability ceiling |
| Streamlit | Low-code | No | Free | Wrong paradigm |
| Gradio | Low-code | No | Free | ML demos only |
| Retool | Low-code | No | Free tier | Internal tools only |
| GitHub Pages | Deploy | Phase 1 | Free | Static only |
| Vercel | Deploy | Phase 2 | Free | Serverless functions |
| Netlify | Deploy | Phase 2 alt | Free | Similar to Vercel |
| Railway | Deploy | If need DB server | Free tier | Full backend |
| Three.js | 3D | Phase 2 lock preview | Free | Best for building-scale 3D |
| MapLibre GL JS | Maps | Phase 2 map upgrade | Free | 3D terrain + vector tiles |
| Rhino.Inside | Server-side 3D | Phase 2/3 | Free dev / ~$995 prod | Headless Rhino kernel as a service |
| deck.gl | Geospatial | Overkill | Free | Big data viz |
| CesiumJS | 3D globe | No | Free/paid | Wrong scale |
