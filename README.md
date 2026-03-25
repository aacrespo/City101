# City101 — Still on the Line

An AI-native architectural design system for the 101km Geneva–Villeneuve corridor. Built at EPFL as part of the Sentient Cities studio (AR-302k, Studio Huang).

## What this is

This repository contains three layers of work, each validating the one above it:

### 1. Design Methodology

A way of working where architects collaborate with AI agents as team members — not as tools that generate on command, but as participants that hold context, accumulate knowledge, and coordinate across tasks. The methodology treats the repository itself as the shared workspace: a kitchen where the recipes are parametric scripts, the ingredients are a construction knowledge base, and the chefs are specialized agents that can work in parallel.

### 2. Workflow Orchestration System

The infrastructure that makes the methodology real. This includes:

- **Agent skills and roles** — five specialist agents (analyst, cartographer, modeler, visualizer, builder) with distinct capabilities and context
- **Session management** — context injection, session save/restore, a lockboard for task coordination between team members (human and AI)
- **Multi-agent 3D modeling** — modified MCP servers for Rhino and Blender, a router for multi-instance coordination, and an agent team workflow tested with 7 concurrent agents producing 709 objects
- **Construction knowledge base** — a 4-layer system (SQLite, curated markdown, parametric scripts, 35K+ chunk RAG) grounding every modeling decision in real material properties, Swiss norms, and construction logic

### 3. Typology Generator *(in development)*

Software that generates architectural typologies for a given site along the corridor — pick points on the map, get Rhino scripts grounded in site context and construction knowledge, with customizable parameters and 24-hour usage animation.

## Tech Stack

Python, Rhino (via MCP), Blender (via MCP), SQLite, Qdrant, Gemini Embeddings, Claude Code, MapLibre GL, Leaflet, QGIS — all coordinates in Swiss LV95 (EPSG:2056).

## Status

Under active development. Midterm presentation March 30, 2026.

## Authors

**Andrea Abril Crespo Salas** and **Henna Rafik**
With Claude as third team member.

EPFL BA6 Architecture — Media x Design Laboratory (LDM), Sentient Cities studio.

## License

AGPL-3.0 — see [LICENSE](LICENSE).
