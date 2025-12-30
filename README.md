# NexusStudio  Titanium

<div align="center">

![NexusStudio Status](https://img.shields.io/badge/Status-Phase_1_Ingestion-blue?style=for-the-badge&logo=python)
![Architecture](https://img.shields.io/badge/Architecture-Neuro_Symbolic-purple?style=for-the-badge)
![Cost](https://img.shields.io/badge/Cloud_Cost-%240.00-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

**The CPU-First, Zero-Cost Autonomous Post-Production Facility.**

[Explore the Docs] • [Report Bug] • [Request Feature]

</div>

---

## ⚡ The Manifesto

**NexusStudio** is not just a video editor; it is a **Hierarchical Multi-Agent Swarm** designed to automate the entire post-production workflow of long-form video content.

Unlike other AI video tools that require $10,000 GPUs or expensive cloud credits, NexusStudio is built on the **"Titanium" Philosophy**:
1.  **Zero Cost:** Leveraging the Free Tiers of Enterprise APIs (Gemini Flash, Groq, OpenRouter).
2.  **Local First:** Heavy computer vision tasks (Face Mesh, Depth, Rendering) run locally on the CPU using highly optimized math.
3.  **Neuro-Symbolic:** Combining the creativity of LLMs with the deterministic precision of Code and Signal Processing.

---

## 🏗 Architecture

NexusStudio operates as a Monorepo containing two distinct organisms:

### 🧠 The Cortex (Backend)
*   **Language:** Python 3.11
*   **Framework:** FastAPI + LangGraph
*   **The "Brain":** Google Gemini 1.5 Flash (Context: 1M Tokens)
*   **The "Reflex":** Groq (Llama 3 70B) for sub-second decision making.
*   **The "Eye":** MediaPipe + DepthAnything (Quantized ONNX).
*   **Memory:** SQLite (Metadata) + ChromaDB (Vector Search).

### 🎨 The Canvas (Frontend)
*   **Language:** Rust (Tauri v2) + TypeScript
*   **UI:** Next.js 15 + React Flow + Shadcn/UI
*   **Concept:** Node-based Non-Linear Editor (NLE). No timelines; just intelligence nodes.

---

## 🚀 Features (The "Impossible" List)

### 1. The Cognitive Crop Engine 🎥
Standard auto-croppers make viewers nauseous. NexusStudio uses a **Probabilistic Kalman Filter** with "Cinematic Damping."
*   **Dead Zone Logic:** The camera acts like a tripod, only panning when the subject explicitly exits the frame.
*   **Speaker Diarization:** The camera automatically cuts to whoever is speaking (or to a reaction shot).

### 2. The Dopamine Psychologist Agent 🧠
An AI agent (Llama 3) that reads the script specifically to find psychological hooks.
*   **Scores:** Curiosity Gap, Negativity Bias, Status Seeking.
*   **Action:** Re-writes the video title *before* the video is cut to ensure alignment.

### 3. Zero-Cost B-Roll 🎞️
*   **Federated Search:** Agents scour Pexels, Unsplash, and Wikimedia.
*   **CPU Verification:** A tiny MobileNet model verifies the image content locally before adding it to the timeline.

---

## 🗺️ Roadmap & Status

We are currently in **PHASE 1**.

- [x] **Phase 0: The Infrastructure** (Universal API Keyring, Multi-Provider Switchboard).
- [x] **Phase 1: The Cortex** (Ingestion, CPU-Optimized Whisper Transcription, SQL Schema).
- [ ] **Phase 2: The Eye** (MediaPipe Integration, Cinematic Damping Algorithm).
- [ ] **Phase 3: The Director** (LangGraph Swarm, Debate Loop between Agents).
- [ ] **Phase 4: The Canvas** (Tauri + React Flow UI Implementation).
- [ ] **Phase 5: The Polish** (FFmpeg Filtergraphs, Karaoke Subtitles).

---

## 🛠️ Installation (Titanium Grade)

We use modern tooling. Ensure you have `uv` (Python) and `pnpm` (Node) installed.

### Prerequisites
*   **FFmpeg** (Must be in your System PATH).
*   **Rust** (For Tauri).
*   **Python 3.11+**.

### 1. Clone the Monorepo
```bash
git clone https://github.com/yourusername/NexusStudio.git
cd NexusStudio
```

### 2. The Armory (Environment Setup)
Create a `.env` file in `apps/cortex/`. You need at least one Key.
```ini
GOOGLE_API_KEY="AIza..."
GROQ_API_KEY="gsk_..."
PRIMARY_BRAIN_PROVIDER="google"
```

### 3. Ignite the Cortex
```bash
cd apps/cortex
uv sync
uv run python main.py
```

---

## 🤝 Contributing

We welcome engineers who believe in the **Local-First** future.
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our "Titanium" code standards.

---

**Built with 🖤 and heavy optimization.**

