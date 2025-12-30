# Contributing to NexusStudio

First off, thank you for considering contributing to NexusStudio. We are building the most advanced open-source post-production AI on the planet.

Because this project combines **High-Performance Python**, **Systems Programming (Rust)**, and **Modern Web Tech**, we adhere to strict engineering standards to keep the system stable and "Titanium-Grade."

## 🧪 The "Titanium" Code Standards

We do not write "scripts." We write **Systems**.

### 1. The Zero-Cost Rule
**Constraint:** Any feature you add **MUST** run on either:
1.  The Local CPU (Simulated on a 2018 MacBook Air or average Windows Laptop).
2.  A Free Tier API.
*   *Rejection Criteria:* Do not submit PRs that require paid OpenAI credits or CUDA-only dependencies.

### 2. Architecture & Patterns
*   **Backend (Cortex):** We use **Dependency Injection**. Do not hardcode API clients. Use the `LLMFactory` in `core/llm_factory.py`.
*   **Type Safety:** Python code must be fully typed. Use `mypy` before pushing.
*   **Async First:** Network-bound operations (API calls) must be `async`. CPU-bound operations (FFmpeg/CV) must run in a `ThreadPoolExecutor` to avoid blocking the event loop.

### 3. The Commit Style
We use **Conventional Commits**.
*   `feat: add Kalman Filter to camera logic`
*   `fix: resolve whisper quantization memory leak`
*   `perf: optimize chroma vector search`
*   `docs: update API key instructions`

## 🛠️ Development Workflow

### Monorepo Structure
*   `apps/cortex`: The Python Brain.
*   `apps/canvas`: The Tauri Frontend.
*   `shared`: JSON schemas shared between Python and Rust.

### Setting up for Dev
1.  **Dependency Management:** We use `uv` exclusively. Do not use `pip` directly.
    *   To add a lib: `uv add library_name`
2.  **Linting:**
    *   Python: `ruff check .`
    *   TypeScript: `pnpm lint`

## 🐛 Reporting Bugs
1.  **Check the logs:** NexusStudio logs extensively to the console. Please include the stack trace.
2.  **State the Hardware:** Since we are CPU-optimized, tell us your CPU model and RAM.

## 🧠 Major Design Decisions (RFCs)
If you want to change the "Cinematic Damping Algorithm" or the "Agent Swarm Topology," please open an **Issue** tagged `RFC` (Request for Comments) first. These are core math/logic components and require architectural discussion.

---

**"We build the tools that build the stories."**