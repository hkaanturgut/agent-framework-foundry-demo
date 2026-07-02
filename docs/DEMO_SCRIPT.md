# 25-minute runbook — Foundry Toolkit for VS Code only

Session title (recommended):  
**"Build agents faster with Foundry Toolkit for VS Code (GA)"**

Goal: show a practical, low-risk workflow in VS Code that attendees can repeat the same day.

---

## Pre-demo checklist (run before you leave)

```bash
source .venv/bin/activate
python smoke_test.py
make single
```

In VS Code:
1. Foundry Toolkit extension installed (`aka.ms/foundrytk`)
2. Signed in and connected to your Azure/Foundry resources
3. Tracing panel opens successfully
4. Evaluation panel can load `foundry-toolkit/evaluation/dataset.jsonl`

---

## Timeline

| Time | Section | What you do | Artifact |
|---|---|---|---|
| 0:00–2:00 | Hook | "You can now do the full agent dev loop in VS Code." | slides 1–2 |
| 2:00–5:00 | What shipped | Foundry Toolkit is GA, and why that matters for speed. | slides 3–4 |
| 5:00–8:00 | Model Catalog | Pick model and explain provider flexibility. | Toolkit UI |
| 8:00–11:00 | Playground | Paste prompt, tune temperature, run fast iterations. | `foundry-toolkit/agent-builder-prompt.md` |
| 11:00–14:00 | Agent Builder | Generate agent from prompt and explain code handoff. | Toolkit UI + `demos/00_single_agent.py` |
| 14:00–17:00 | Agent Inspector | Run and inspect agent turns/breakpoints. | Toolkit UI |
| 17:00–20:00 | Tracing | Enable tracing and show spans for a real run. | Toolkit UI + `make single` |
| 20:00–22:00 | Evaluation | Load dataset and explain quality gates. | `foundry-toolkit/evaluation/dataset.jsonl` |
| 22:00–25:00 | Wrap/Q&A | Recap loop + links + next steps. | final slides |

---

## Live steps (exact order)

1. **Model Catalog**
   - Open Foundry Toolkit
   - Choose a chat model you already have access to
   - One sentence: "You can swap models/providers without leaving the editor."

2. **Playground**
   - Paste prompt from `foundry-toolkit/agent-builder-prompt.md`
   - Run 1-2 prompt variants
   - Mention: "We validate behavior here before writing more code."

3. **Agent Builder**
   - Build agent from the tested prompt
   - Show generated scaffold
   - Tie it back to `demos/00_single_agent.py`

4. **Run baseline sample**
   ```bash
   make single
   ```

5. **Tracing**
   - Ensure tracing collector is active in toolkit
   - Set `ENABLE_TRACING=true` in `.env`
   - Run again:
     ```bash
     make single
     ```
   - Walk through spans and explain observability value

6. **Evaluation**
   - Open evaluation workflow in toolkit
   - Load `foundry-toolkit/evaluation/dataset.jsonl`
   - Explain pass/fail gating and iterative improvement

---

## Talk track cues (short)

- **Catalog:** model choice is now a product decision, not plumbing.
- **Playground:** fastest place to test intent and tone.
- **Builder:** shortest path from idea to runnable code.
- **Inspector:** debugging agents is visual now.
- **Tracing:** you can explain every step, not just output.
- **Evaluation:** quality is measurable, not subjective.

---

## If something fails live

- **Toolkit sign-in/resource issue**: switch to code + screenshots; keep narrative on workflow.
- **Model deployment issue**: use your fallback backend (`MODEL_BACKEND=github`) and continue.
- **Tracing unavailable**: continue with Inspector + Evaluation; mention tracing is optional in local loop.
- **Network instability**: run only `make single` and focus on generated code + process.

---

## Backup plan (ultra-simple)

If time is tight or environment is unstable:
1. Playground only (3 min)
2. Agent Builder only (4 min)
3. `make single` run (2 min)
4. One tracing screenshot + one evaluation screenshot (2 min)

You still deliver the full message: **discover → test → generate → inspect → evaluate**.

