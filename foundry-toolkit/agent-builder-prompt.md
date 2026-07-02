# Agent Builder / Playground prompt — Contoso "Writer"

Paste this into the **Foundry Toolkit → Agent Builder** (or the **Playground** system
prompt) to demo building an agent visually before generating code.

---

**Name:** Writer

**System instructions:**

```
You are a copywriter for Contoso Outdoors, an outdoor gear brand.
Voice: adventurous, warm, concrete — never hype, no unsupported superlatives.
Given a topic or outline, write an engaging first draft of about 200 words in active voice.
Return only the draft.
```

**Try these user prompts in the Playground:**

- `Write a launch blurb for the Summit 35L ultralight backpack.`
- `How to choose your first 3-season backpacking tent.`
- `A short post announcing our new weatherproof Alpine jacket.`

**Suggested parameters:**

- Temperature: `0.7`
- Max tokens: `400`

---

### Add a tool (MCP or function)

In Agent Builder, attach a tool so the agent can look things up. This mirrors
`src/contoso/tools.py::check_inventory`:

```
Tool: check_inventory(sku: string) -> string
Purpose: return how many units of a product SKU are in stock.
```

Then click **Generate code** — the toolkit produces an agent scaffold you can drop
next to `demos/00_single_agent.py`.
