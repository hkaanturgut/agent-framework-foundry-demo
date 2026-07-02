# Setup

## 1. Prerequisites

- **Python 3.10+** (3.13 recommended)
- **VS Code** + **Foundry Toolkit** extension → install from `aka.ms/foundrytk`
- One model backend (pick one):
  - **Azure OpenAI** (primary for this talk) — a deployment such as `gpt-4o-mini`
  - **Microsoft Foundry** project endpoint
  - **GitHub Models** (free, zero-Azure fallback) — a GitHub PAT
  - **OpenAI** or any OpenAI-compatible endpoint

## 2. Install

```bash
# from the repo root
python -m venv .venv && source .venv/bin/activate      # or: uv venv .venv
pip install -r requirements.txt                        # or: uv pip install -r requirements.txt
cp .env.example .env
```

(Optional, only to regenerate the slides: `pip install -r requirements-dev.txt`.)

## 3. Configure `.env`

Open `.env` and set `MODEL_BACKEND` plus the matching values.

### Azure OpenAI (recommended for the talk)

```dotenv
MODEL_BACKEND=azure-openai
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-10-21
# Auth: either set a key, or leave it blank and use Entra ID:
# AZURE_OPENAI_API_KEY=...
```

For Entra ID auth (no key in the file), sign in first:

```bash
az login
```

### Microsoft Foundry

```dotenv
MODEL_BACKEND=foundry
FOUNDRY_PROJECT_ENDPOINT=https://<resource>.services.ai.azure.com/api/projects/<project>
FOUNDRY_MODEL=gpt-4o-mini
```
(Uses `az login` / `DefaultAzureCredential`.)

### GitHub Models — the bulletproof stage fallback

```dotenv
MODEL_BACKEND=github
GITHUB_TOKEN=ghp_...
GITHUB_MODEL=openai/gpt-4o-mini
```

## 4. Verify (offline — no network needed)

```bash
python smoke_test.py
```

You should see all workflow builders construct successfully. This proves the wiring
without spending a token — run it right before you go on stage.

## 5. Run a demo

```bash
python demos/01_sequential.py
# or: make sequential
```

## 6. (Optional) Enable tracing into the Foundry Toolkit

```dotenv
ENABLE_TRACING=true
```
Then open **Foundry Toolkit → Tracing** in VS Code and start the local collector
before running a demo. See `foundry-toolkit/README.md`.
