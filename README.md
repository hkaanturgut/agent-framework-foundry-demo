# Contoso Outdoors Launch Desk

### Microsoft Agent Framework × Foundry Toolkit for VS Code — a live demo repo

> Built for the **Microsoft Build 2026 Recap — Toronto** session
> *"Agent development got faster."* One company, **five orchestration patterns**,
> plus the **in-editor dev loop** that ships them. This README doubles as the handout —
> clone it and you have the whole talk.

[![Agent Framework](https://img.shields.io/badge/agent--framework-1.10.0-blue)](https://pypi.org/project/agent-framework/)
[![Foundry Toolkit](https://img.shields.io/badge/Foundry%20Toolkit-GA-brightgreen)](https://code.visualstudio.com/docs/intelligentapps/overview)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)

---

## What is this actually about?

Two things shipped that make agents feel like *engineering* instead of *demos*:

### 1. Microsoft Agent Framework (MAF)
The single, supported successor to **Semantic Kernel** + **AutoGen**. It gives you an
`Agent` primitive and a set of **stable orchestration building blocks** — reusable ways
to wire multiple agents together:

| Pattern | When you reach for it |
|---------|-----------------------|
| **Sequential** | A pipeline — each agent's output feeds the next (draft → edit → publish). |
| **Concurrent** | Fan out the same input to several agents, then aggregate (parallel review). |
| **Handoff** | The **model** routes work to the right specialist (support triage). |
| **Group Chat** | Several agents converse and converge (brainstorm, debate). |
| **Magentic** | A manager writes a plan and delegates to a team (open-ended tasks). |

All of them support **human-in-the-loop** — the workflow can pause for an approval and resume.

### 2. Foundry Toolkit for VS Code (now GA)
The local AI dev loop, in the editor: **Model Catalog → Playground → Agent Builder →
Agent Inspector → Evaluation → Tracing**. Test a prompt, generate agent code, run it,
watch the traces, and score it — without leaving VS Code. (Formerly "AI Toolkit for VS Code".)
Install: **`aka.ms/foundrytk`**

**The story of this repo:** *build an agent in the toolkit, drop the generated code into
these patterns, and watch it run — traced and evaluated in the same window.*

---

## The demo — "Contoso Outdoors Launch Desk"

One fictional outdoor-gear company. Every pattern is a real desk in that company:

| # | File | Pattern | Scene |
|---|------|---------|-------|
| 00 | `demos/00_single_agent.py` | Single agent | Baseline: one writer agent + a tool. |
| 01 | `demos/01_sequential.py` | **Sequential** | Blog pipeline: Outliner → Writer → Editor. |
| 02 | `demos/02_concurrent.py` | **Concurrent** | Review board: SEO ∥ Legal ∥ Brand → aggregate. |
| 03 | `demos/03_handoff.py` | **Handoff** | Support triage routes to Order / Returns / Refund. |
| 04 | `demos/04_group_chat.py` | **Group Chat** | Headline brainstorm; stops on "SHIP IT". |
| 05 | `demos/05_magentic.py` | **Magentic** | Launch brief: Manager plans Researcher + Analyst. |
| 06 | `demos/06_hitl_approval.py` | **HITL** | `publish_blog` is gated by a human approval. |

Each script is deliberately short (~20–40 lines) so the **pattern** is what shows on the
projector. The personas and plumbing live in `src/contoso/`.

---

## Quickstart

```bash
# 1. install
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # then edit .env (see below)

# 2. prove the wiring — offline, no tokens spent
python smoke_test.py

# 3. run a pattern
python demos/01_sequential.py   # or:  make sequential
```

Pick a backend in `.env` (`MODEL_BACKEND`):

- `azure-openai` — Azure OpenAI deployment (primary for the talk)
- `foundry` — Microsoft Foundry project endpoint
- `github` — **GitHub Models**, free, zero-Azure — the perfect stage fallback
- `openai` — OpenAI or any compatible endpoint

Full details in **[docs/SETUP.md](docs/SETUP.md)**.

```bash
make            # list every shortcut (setup, smoke, single…hitl, deck)
```

---

## Repo map

```
src/contoso/     reusable library: config, client, tools, agents, pretty, tracing
demos/           one file per orchestration pattern (00–06)
foundry-toolkit/ what to click in VS Code + an evaluation dataset
docs/            SETUP · DEMO_SCRIPT (25-min runbook) · ARCHITECTURE · TROUBLESHOOTING
deck/            python-pptx generator + the generated .pptx
smoke_test.py    offline: builds every workflow, calls no model
```

The backend-agnostic core is `src/contoso/client.py` (`get_chat_client()` + `make_agent()`);
personas are in `src/contoso/agents.py`; read-only vs approval-gated tools are in
`src/contoso/tools.py`. See **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)**.

---

## The Foundry Toolkit loop (the VS Code half)

1. **Model Catalog** → pick `gpt-4o-mini`.
2. **Playground** → paste [`foundry-toolkit/agent-builder-prompt.md`](foundry-toolkit/agent-builder-prompt.md), test it.
3. **Agent Builder** → *Generate code* → that's `demos/00_single_agent.py`.
4. **Tracing** → set `ENABLE_TRACING=true`, run a demo, watch the spans. (Code: `src/contoso/tracing.py`.)
5. **Evaluation** → load [`foundry-toolkit/evaluation/dataset.jsonl`](foundry-toolkit/evaluation/dataset.jsonl), score routing accuracy.

Step-by-step: **[foundry-toolkit/README.md](foundry-toolkit/README.md)**.

---

## Presenting this?

- **[docs/DEMO_SCRIPT.md](docs/DEMO_SCRIPT.md)** — a minute-by-minute 25-minute runbook with talking points and fallbacks.
- **`deck/Build2026-Recap-Agents.pptx`** — the slides (regenerate with `make deck`).
- **Golden rule:** run `python smoke_test.py` before you go on stage. If Wi-Fi dies, flip `.env` to `MODEL_BACKEND=github`.

---

## Key API facts (verified against `agent-framework==1.10.0`)

The SDK is in fast beta and had renames during 2026, so this repo **pins the version** and
uses the verified surface:

- Agents: `agent_framework.Agent(name, instructions, client, tools=…)`.
- Azure OpenAI: `agent_framework.openai.OpenAIChatClient(azure_endpoint=…, api_version=…, credential=… | api_key=…)` (there is no separate `AzureOpenAIChatClient`).
- Foundry: `agent_framework.foundry.FoundryChatClient(project_endpoint=…, credential=…)`.
- Tools: `@tool(...)`, approval-gating via `@tool(approval_mode="always_require")`.
- Orchestration builders live in `agent_framework.orchestrations` (`SequentialBuilder`, `ConcurrentBuilder`, `HandoffBuilder`, `GroupChatBuilder`, `MagenticBuilder`).
- Handoff requires each participant with `require_per_service_call_history_persistence=True`.
- HITL: approval-gated tool calls surface as `request_info` events; resume with `workflow.run(responses={request_id: response})`.
- Tracing: `agent_framework.observability.configure_otel_providers(vs_code_extension_port=4317)`.

If you hit an import error, you're probably on a newer SDK — reinstall the pinned version.

---

## Links

- Foundry Toolkit for VS Code — https://code.visualstudio.com/docs/intelligentapps/overview · install `aka.ms/foundrytk`
- Agent Framework — https://pypi.org/project/agent-framework/
- Troubleshooting — [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

*Contoso Outdoors is a fictional brand used for demo purposes.*
