# Contoso Launch Desk

### Foundry Toolkit for VS Code — focused demo repo

> Built for **Microsoft Build 2026 Recap — Toronto**.  
> This version is intentionally simplified for a **Foundry Toolkit-only** session.

[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-GA-brightgreen)](https://code.visualstudio.com/docs/intelligentapps/overview)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## What this repo is for

This repo helps you explain to people who missed Build 2026:

1. **What Foundry Toolkit for VS Code is** (and why GA matters)
2. **How the in-editor dev loop works** end-to-end:
   - Model Catalog
   - Playground
   - Agent Builder
   - Agent Inspector
   - Tracing
   - Evaluation
3. **How to run a practical demo quickly** with minimal moving parts

The previous multi-pattern orchestration deep dive is still in the repo as optional appendix material, but your main talk can now stay entirely toolkit-centered.

---

## 25-minute session flow (toolkit-only)

Use **[docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)** for the minute-by-minute script.

High-level structure:

- 0–5 min: what Foundry Toolkit is and what changed (GA)
- 5–16 min: live VS Code loop (catalog → playground → builder → inspector)
- 16–22 min: tracing + evaluation
- 22–25 min: recap + links + Q&A

---

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Set your backend in `.env`:

- `MODEL_BACKEND=foundry` (preferred for this session)
- `MODEL_BACKEND=azure-openai` (also fine)
- `MODEL_BACKEND=github` (stage fallback)

Sanity check:

```bash
python smoke_test.py
```

---

## Minimal live-demo path

1. Open VS Code with the **Foundry Toolkit** extension installed (`aka.ms/foundrytk`).
2. Use **Model Catalog** to choose a model.
3. Use **Playground** with `foundry-toolkit/agent-builder-prompt.md`.
4. Use **Agent Builder** and generate code.
5. Run the generated/baseline sample:
   ```bash
   make single
   ```
6. Turn on tracing:
   - Set `ENABLE_TRACING=true` in `.env`
   - Open Tracing panel in toolkit
   - Run:
     ```bash
     make single
     ```
7. Show evaluation with:
   - `foundry-toolkit/evaluation/dataset.jsonl`
   - `foundry-toolkit/evaluation/README.md`

Detailed click-paths are in **[foundry-toolkit/README.md](foundry-toolkit/README.md)**.

---

## What to open on stage

- **Runbook:** [docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)
- **Toolkit guide:** [foundry-toolkit/README.md](foundry-toolkit/README.md)
- **Slides:** `deck/Build2026-Recap-Agents.pptx`

Regenerate slides:

```bash
make deck
```

---

## Optional appendix (if asked)

These are preserved, but not required for the simplified talk:

- Multi-agent pattern demos (`demos/01` to `demos/06`)
- MAF-focused architecture docs
- Terraform/AVM Foundry package under `infra/terraform/`

---

## Links

- Foundry Toolkit for VS Code: https://code.visualstudio.com/docs/intelligentapps/overview
- Install shortcut: `aka.ms/foundrytk`
- Azure AI Foundry docs: https://learn.microsoft.com/azure/foundry/

