# Foundry Toolkit for VS Code — Simple Demo Repo

This repo is intentionally minimal.

Use it to demo only four things:
1. Install the extension
2. Deploy a base model
3. Create a prompt agent
4. Use Playgrounds

---

## Session scope (what you will show)

This is a **Foundry Toolkit for VS Code only** session.  
No deep orchestration code, no complex infra walkthrough, no framework internals.

---

## Prerequisites

1. **VS Code** installed
2. **Azure subscription** with access to Azure AI Foundry
3. **Foundry project** (existing or newly created in portal)
4. Ability to sign in to Azure from VS Code

Toolkit install link: **`aka.ms/foundrytk`**  
Docs: https://code.visualstudio.com/docs/intelligentapps/overview

---

## Step-by-step demo guide

## 1) Install the Foundry Toolkit extension

In VS Code:
1. Open **Extensions**
2. Search for **Foundry Toolkit**
3. Install extension id: `teamsdevapp.vscode-ai-toolkit`

Optional CLI install:
```bash
code --install-extension teamsdevapp.vscode-ai-toolkit
```

---

## 2) Sign in and connect your Foundry project

1. Open the **Foundry Toolkit** panel in VS Code
2. Sign in to Azure
3. Select your subscription
4. Select your Foundry resource and project

Expected result: your project appears under Toolkit resources.

---

## 3) Deploy a base model (Model Catalog)

1. Open **Model Catalog** in Toolkit
2. Choose a base chat model (example: `gpt-5.4-mini`)
3. Click **Deploy**
4. Select your project and region
5. Keep defaults for first demo (or smallest allowed capacity)
6. Wait for deployment status = **Succeeded**

Tip: if your preferred model is unavailable in your subscription/region, pick any supported chat model and continue.

---

## 4) Playground demo (copy/paste prompts)

Open Playground and set:
- Temperature: `0.5` (start stable)
- Max tokens: `300`

Use this **system prompt**:

```text
You are Contoso Assistant, a concise and practical AI helper for a retail outdoor brand.
Rules:
- Be clear and short.
- Use bullet points when useful.
- If data is missing, state assumptions explicitly.
- Never invent product availability or pricing.
```

Use these **user prompts** in sequence:

```text
Prompt 1 (baseline):
Write a 4-bullet launch summary for our new Summit 35L backpack.

Prompt 2 (tone):
Rewrite this for first-time hikers in simple language.

Prompt 3 (constraint):
Give me a 2-line website hero copy and one CTA button text.

Prompt 4 (guardrail check):
Tell me exact inventory count and tomorrow's discount percentage.
```

What to explain while running:
- Prompt quality before coding
- Fast iteration loop
- Guardrail behavior on unknown data

More prompt sets: `foundry-toolkit/playground-prompts.md`

---

## 5) Create a Prompt Agent (Agent Builder)

1. Open **Agent Builder** in Toolkit
2. Create new agent: `contoso-prompt-agent`
3. Paste the same system prompt (or use `foundry-toolkit/agent-builder-prompt.md`)
4. Select your deployed model
5. Save agent configuration
6. Run test prompts from the builder test panel

Suggested test prompts:
- `Draft a 3-point product positioning for Summit 35L.`
- `Give me a customer support reply for a delayed shipment.`
- `Summarize this product in one sentence for social media.`

---

## 6) Show Playground + Agent side by side

In the live demo:
1. Run a prompt in Playground
2. Run same prompt in Prompt Agent test panel
3. Explain difference:
   - Playground = fast experimentation
   - Prompt Agent = reusable behavior/config for app workflows

---

## 7) (Optional) Wrap-up talking points

- Foundry Toolkit brings the full inner loop into VS Code
- Team can move from idea to tested prompt agent quickly
- Model deployment + prompt iteration + reusable agent are all in one tool

---

## Recommended 25-minute timing

- 0–4 min: install + sign-in + project selection
- 4–10 min: deploy model from catalog
- 10–18 min: playground prompt iterations
- 18–24 min: create and test prompt agent
- 24–25 min: recap + Q&A

---

## Files in this repo

- `README.md` — full demo script (this file)
- `foundry-toolkit/agent-builder-prompt.md` — primary prompt agent template
- `foundry-toolkit/playground-prompts.md` — extra prompt sets for live testing

