# Architecture

## Layout

```
foundry-toolkit-vscode-demo/
├── src/contoso/            # reusable library — the "story" lives here
│   ├── config.py           # .env → Settings, resolves the backend
│   ├── client.py           # get_chat_client() + make_agent()  (backend-agnostic)
│   ├── tools.py            # read-only tools + approval-gated tools
│   ├── agents.py           # every agent persona (factory functions)
│   ├── pretty.py           # banners + run_workflow() output rendering
│   └── tracing.py          # one-call OTLP → Foundry Toolkit
├── demos/                  # one file per orchestration pattern (short, projector-friendly)
│   ├── 00_single_agent.py … 06_hitl_approval.py
│   └── _bootstrap.py       # puts src/ on sys.path
├── foundry-toolkit/        # what to click in VS Code + eval dataset
├── docs/                   # SETUP, DEMO_SCRIPT, ARCHITECTURE, TROUBLESHOOTING
├── deck/                   # python-pptx generator + generated .pptx
└── smoke_test.py           # offline: builds every workflow, calls no model
```

## Design principle

**Personas and plumbing live in `src/contoso/`; the demo files show only the pattern.**
Each demo is ~20–40 lines so that on a projector the *orchestration shape* is the star,
not boilerplate. Swap the backend in `.env` and every demo follows.

## The two layers that matter

### 1. `client.py` — backend-agnostic entry point

`get_chat_client()` reads `Settings.backend` and returns the right client:

| backend | class |
|---------|-------|
| `azure-openai` | `agent_framework.openai.OpenAIChatClient(azure_endpoint=…, api_version=…, credential/api_key)` |
| `foundry` | `agent_framework.foundry.FoundryChatClient(project_endpoint=…, credential)` |
| `github` | `OpenAIChatClient(base_url=…models.github.ai…, api_key=GITHUB_TOKEN)` |
| `openai` | `OpenAIChatClient(api_key=…)` |

`make_agent(client, name, instructions, tools=…, require_history_persistence=…)` wraps
`agent_framework.Agent(...)` and maps `require_history_persistence` →
`require_per_service_call_history_persistence` (needed by the Handoff builder).

### 2. `agents.py` + the orchestration builders

The demos compose personas with builders from `agent_framework.orchestrations`:

| Demo | Builder | Shape |
|------|---------|-------|
| 01 | `SequentialBuilder(participants=[outliner, writer, editor])` | pipeline |
| 02 | `ConcurrentBuilder(participants=[seo, legal, brand])` | fan-out / aggregate |
| 03 | `HandoffBuilder(...).with_start_agent(triage).add_handoff(...)` | model-routed |
| 04 | `GroupChatBuilder(participants=[…], selection_func=…)` | round-robin chat |
| 05 | `MagenticBuilder(participants=[…], manager_agent=launch_manager)` | plan-and-delegate |
| 06 | single `publisher` agent + `@tool(approval_mode="always_require")` | HITL approval |

## Human-in-the-loop flow (demo 06)

```
publisher.run("write & publish …")
        │  agent decides to call publish_blog (approval_mode="always_require")
        ▼
workflow emits a  request_info  event   ← execution PAUSES here
        │  ev.data is a function_approval_request (has .function_call, .to_function_approval_response)
        ▼
you approve/deny → workflow.run(responses={ev.request_id: response})
        ▼
tool actually runs (or is skipped) → final output
```

The same `request_info` primitive powers Magentic **plan review** (`enable_plan_review=True`).

## Observability

`tracing.enable_tracing()` calls
`agent_framework.observability.configure_otel_providers(vs_code_extension_port=4317)`,
streaming OpenTelemetry spans to the Foundry Toolkit's local collector. Toggle with
`ENABLE_TRACING=true`. This is what makes the multi-agent steps visible in VS Code.

## Version pinning

`requirements.txt` pins `agent-framework==1.10.0` on purpose — the SDK is in fast beta
and had breaking renames during 2026 (e.g. `ai_function` → `tool`). Pinning keeps the
talk reproducible.
