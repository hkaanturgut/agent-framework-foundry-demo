# Evaluation dataset

`dataset.jsonl` is a tiny set for demoing the Foundry Toolkit **Model Evaluation**
feature. Each row is a support message plus the specialist the triage agent *should*
route to (`ground_truth`) — i.e. a routing-accuracy set for the Handoff demo.

Fields per line:
- `query` — the customer message
- `ground_truth` — the expected specialist (`order_agent` / `returns_agent` / `refund_agent`)
- `context` — a short note (handy for human reviewers)

## Run it in the toolkit

1. Open **Foundry Toolkit → Model Evaluation** in VS Code.
2. Create a new evaluation and select this `dataset.jsonl`.
3. Pick a model (the same one from your `.env`).
4. Choose built-in evaluators — e.g. **relevance**, **coherence**, **similarity** —
   or add a custom evaluator that checks whether the response names `ground_truth`.
5. Run and review the per-row scores.

## Programmatic option

Agent Framework also exposes evaluators via `agent_framework.foundry`
(`FoundryEvals`, `evaluate_foundry_target`, `evaluate_traces`) if you'd rather run
evaluation from code. See the Foundry docs for the current signatures.
