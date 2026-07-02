# Foundry Toolkit for VS Code — focused demo guide

This guide is the core of the simplified session.  
Everything below is optimized for a **toolkit-only** live demo.

Install: **`aka.ms/foundrytk`**  
Overview: https://code.visualstudio.com/docs/intelligentapps/overview

---

## The 6-step loop to show

| # | Feature | What to do live | Repo tie-in |
|---|---|---|---|
| 1 | **Model Catalog** | Pick a model you already have access to | `.env` backend/model |
| 2 | **Playground** | Paste and test prompt variations | `agent-builder-prompt.md` |
| 3 | **Agent Builder** | Generate agent scaffold from prompt | `demos/00_single_agent.py` |
| 4 | **Agent Inspector** | Run and inspect turns/debug flow | toolkit runtime view |
| 5 | **Tracing** | Show spans from a real run | `src/contoso/tracing.py` |
| 6 | **Evaluation** | Load small dataset and discuss quality gates | `evaluation/dataset.jsonl` |

---

## Live walkthrough (quick)

1. Open Foundry Toolkit in VS Code.
2. Choose a model in **Model Catalog**.
3. Open **Playground** and paste `agent-builder-prompt.md`.
4. Build from prompt in **Agent Builder**.
5. Run baseline sample:
   ```bash
   make single
   ```
6. Turn on tracing:
   - set `ENABLE_TRACING=true` in `.env`
   - run `make single` again
   - show spans in Tracing panel
7. Open **Evaluation**, load `evaluation/dataset.jsonl`, explain scoring.

---

## Tracing wiring (repo side)

This repo streams OpenTelemetry to Foundry Toolkit's local collector:

```python
from agent_framework.observability import configure_otel_providers
configure_otel_providers(vs_code_extension_port=4317)
```

Code location: `src/contoso/tracing.py`

---

## Files in this folder

- `agent-builder-prompt.md` — prompt to paste into Playground/Builder
- `evaluation/dataset.jsonl` — tiny evaluation data for demo
- `evaluation/README.md` — evaluation usage notes

