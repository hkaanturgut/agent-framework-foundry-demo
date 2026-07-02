# 25-minute demo runbook

Session: *"Agent development got faster — Microsoft Agent Framework + Foundry Toolkit."*
Goal: show that the **orchestration building blocks are now stable** and the **local
dev loop in VS Code is GA**. One story ("Contoso Outdoors Launch Desk"), five patterns.

> Golden rule: **run `python smoke_test.py` before you walk on stage.** If Wi-Fi dies,
> switch `.env` to `MODEL_BACKEND=github` (or your pre-recorded terminal) and keep going.

---

## Timeline

| Time | Section | You do / say | Command |
|------|---------|--------------|---------|
| 0:00–2:00 | **Hook** | "Last year agents were demos. This year they're building blocks." Set up Contoso Outdoors. | slide 1–3 |
| 2:00–5:00 | **What shipped** | MAF = Semantic Kernel + AutoGen, GA orchestration. Foundry Toolkit GA. | slide 4–6 |
| 5:00–8:00 | **Foundry Toolkit loop** | Live in VS Code: Model Catalog → Playground → Agent Builder → *Generate code*. | see below |
| 8:00–10:00 | **00 single agent** | The generated agent, running from code. | `make single` |
| 10:00–12:30 | **01 sequential** | Blog pipeline Outliner→Writer→Editor. "Deterministic handoff." | `make sequential` |
| 12:30–15:00 | **02 concurrent** | SEO ∥ Legal ∥ Brand fan-out/fan-in. "Same agents, different shape." | `make concurrent` |
| 15:00–17:30 | **03 handoff** | Support triage routes to a specialist. "The model picks the path." | `make handoff` |
| 17:30–19:30 | **05 magentic** | Manager plans Researcher + Analyst. "Open-ended, plan-driven." | `make magentic` |
| 19:30–22:00 | **06 HITL + tracing** | Approval gate on `publish_blog`; show the trace in the toolkit. | `make hitl` |
| 22:00–24:00 | **Wrap** | Five patterns, one API. Eval + trace in-editor. Repo is the handout. | slide 17–19 |
| 24:00–25:00 | **CTA / Q&A** | `aka.ms/foundrytk`, star the repo, questions. | slide 19 |

*(04 group chat is the cut-for-time spare — drop it first if you're running long,
or swap it in for magentic if the room prefers a lighter example.)*

---

## The VS Code portion (5:00–8:00)

1. **Model Catalog** — filter to `gpt-4o-mini`, one sentence on multi-provider.
2. **Playground** — paste `foundry-toolkit/agent-builder-prompt.md`, send one prompt.
3. **Agent Builder** — same prompt → **Generate code**. "That's `demos/00_single_agent.py`."
4. (If time) **Tracing** — start the local collector; you'll return to it at 19:30.

Keep it to ~3 minutes. The point is *"test → build → generate code, without leaving the editor."*

---

## Per-demo talking points

- **00 single agent** — baseline: `Agent(name, instructions, tools)`. Everything else is composition.
- **01 sequential** — `SequentialBuilder(participants=[...])`. Output of one is input to the next. Deterministic.
- **02 concurrent** — `ConcurrentBuilder(...)`. *Same three agents could be reviewers in parallel.* Fan-out, aggregate.
- **03 handoff** — `HandoffBuilder` + `.add_handoff(...)`. The **model** decides who takes the ticket. Note `require_per_service_call_history_persistence=True`.
- **05 magentic** — `MagenticBuilder(manager_agent=...)`. Manager writes a plan and delegates. Best for open-ended tasks.
- **06 HITL** — `@tool(approval_mode="always_require")`. The workflow **pauses** and emits a `request_info` event; you approve; it resumes. This is the "safe autonomy" slide.

---

## If something breaks

- **Auth/network error** → set `MODEL_BACKEND=github` in `.env`, rerun. (Have a PAT ready.)
- **A run hangs** → Ctrl-C; say "non-determinism is why we have tracing + eval," pivot to the toolkit panels.
- **Total failure** → walk the code in the editor; the narrative stands on the source alone.
- Every demo prints clean, projector-readable banners via `src/contoso/pretty.py`.

See `docs/TROUBLESHOOTING.md` for specifics.
