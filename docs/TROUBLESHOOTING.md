# Troubleshooting

## Fast triage

```bash
python smoke_test.py     # builds every workflow offline — no model call
```
If this passes, your **wiring** is fine and any failure is auth/network/model-side.

---

## Auth & backend

**`DefaultAzureCredential`/`AzureCliCredential` failed / not logged in**
→ `az login`. For Azure OpenAI you can instead set `AZURE_OPENAI_API_KEY` in `.env`.

**`404` / `DeploymentNotFound` (Azure OpenAI)**
→ `AZURE_OPENAI_CHAT_DEPLOYMENT` must be the **deployment name**, not the model name.
Confirm `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_API_VERSION` (e.g. `2024-10-21`).

**`401 Unauthorized` (GitHub Models)**
→ `GITHUB_TOKEN` missing/expired, or model id wrong. Use e.g. `openai/gpt-4o-mini`.

**Rate limited / `429`**
→ You're on a small quota. Wait, lower request volume, or switch `MODEL_BACKEND=github`.

**No network / Wi-Fi died on stage**
→ Switch `.env` to `MODEL_BACKEND=github` with a pre-made PAT, or narrate from the code.
The demos are intentionally readable without running.

---

## Handoff demo (03)

**`ValueError` when building the handoff workflow**
→ Every participant agent must be created with `require_history_persistence=True`
(maps to `require_per_service_call_history_persistence`). The support-desk factories in
`agents.py` already set this — keep it if you edit them.

---

## Group chat demo (04)

**`ValueError`: group chat needs an orchestrator/selection**
→ `GroupChatBuilder` requires one of `orchestrator_agent=`, `orchestrator=`, or
`selection_func=`. This demo supplies a `selection_func`; don't remove it.

**Chat never stops**
→ Ensure a `termination_condition`/`max_rounds` is set and the editor persona can emit
the stop token (`SHIP IT:`). Lower `max_rounds` if it runs long on stage.

---

## HITL demo (06)

**It runs the tool without asking**
→ The tool must be declared `@tool(approval_mode="always_require")` (see `tools.py`).
Run with `--yes`/`--no` to script the answer for a clean stage demo.

**Hangs waiting for input**
→ It's waiting on the approval `request_info`. Answer the prompt, or pass `--yes`.

---

## Tracing

**No spans in the Foundry Toolkit**
→ Set `ENABLE_TRACING=true`, and **start the Tracing collector in VS Code first**
(it listens on `4317`). Then run the demo. See `foundry-toolkit/README.md`.

---

## Imports / environment

**`ModuleNotFoundError: agent_framework`**
→ Activate the venv (`source .venv/bin/activate`) and `pip install -r requirements.txt`.

**`ImportError` for a builder or `tool`**
→ You're on a different SDK version. This repo targets **`agent-framework==1.10.0`**;
the API moved during beta. Reinstall the pinned version.

**Python too old**
→ Need 3.10+. Check with `python --version`.

---

## Deck

**Regenerate the slides**
→ `pip install -r requirements-dev.txt && python deck/build_deck.py`
(writes `deck/Build2026-Recap-Agents.pptx`).
