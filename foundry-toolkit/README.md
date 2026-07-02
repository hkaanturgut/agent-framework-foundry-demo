# Foundry Toolkit for VS Code — demo guide

The **Foundry Toolkit for Visual Studio Code** (formerly *AI Toolkit for VS Code*,
now **GA**) is the other half of this talk. It gives you the full local AI dev loop
inside the editor. This folder tells you exactly what to click during the session.

Install: **`aka.ms/foundrytk`** · Docs: https://code.visualstudio.com/docs/intelligentapps/overview

---

## The 60-second dev loop to demo

| # | Toolkit feature | What to show | Ties to the code |
|---|-----------------|--------------|------------------|
| 1 | **Model Catalog** | Browse models (OpenAI, Anthropic, Google, GitHub, Foundry, ONNX, Ollama). Pick `gpt-4o-mini`. | the model in `.env` |
| 2 | **Playground** | Paste the Writer instructions, chat, tweak temperature. "Test before you code." | `agents.writer` |
| 3 | **Agent Builder** | Turn that prompt into an agent + generate code; attach an MCP tool. | `demos/00_single_agent.py` |
| 4 | **Agent Inspector** | Run an agent locally, visualize the run, set a breakpoint. | any demo |
| 5 | **Tracing** | Turn on `ENABLE_TRACING=true` and run a workflow — watch spans appear. | `contoso/tracing.py` |
| 6 | **Evaluation** | Load `evaluation/dataset.jsonl`, run built-in evaluators (relevance/coherence). | `evaluation/` |

> On stage, you don't need all six. The strong ones are **Agent Builder** (build → code),
> **Agent Inspector** (visualize a run), and **Tracing** (see the multi-agent steps live).

---

## Wiring traces into the toolkit

Agent Framework has built-in OpenTelemetry. This repo streams it to the toolkit's local
OTLP collector with one call (see `src/contoso/tracing.py`):

```python
from agent_framework.observability import configure_otel_providers
configure_otel_providers(vs_code_extension_port=4317)   # -> Foundry Toolkit
```

Steps to demo tracing:
1. In VS Code, open the **Foundry Toolkit** view → **Tracing** and start the local collector.
2. Set `ENABLE_TRACING=true` in `.env`.
3. Run a multi-agent demo, e.g. `python demos/05_magentic.py`.
4. Switch to the Tracing panel — each agent turn, tool call, and workflow step is a span.

---

## Files here

- **`agent-builder-prompt.md`** — a ready-to-paste prompt for the Agent Builder / Playground.
- **`evaluation/dataset.jsonl`** — a tiny evaluation set for the Model Evaluation feature.
- **`evaluation/README.md`** — how to run the evaluation.
