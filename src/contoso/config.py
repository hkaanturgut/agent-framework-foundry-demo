"""Configuration: load ``.env`` and resolve the active model backend.

The whole demo is designed to be **backend-swappable via ``.env``** so you can:

- present on Azure OpenAI / Foundry (the on-brand choice for an Azure event), and
- fall back instantly to GitHub Models or OpenAI if Wi-Fi / a deployment misbehaves
  on stage — just change ``MODEL_BACKEND`` and re-run.

Nothing here talks to the network; it only reads environment variables.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # dotenv is optional; env vars still work without it.
    load_dotenv = None

# Load the repo-root .env once on import (if python-dotenv is installed).
_REPO_ROOT = Path(__file__).resolve().parents[2]
if load_dotenv is not None:
    load_dotenv(_REPO_ROOT / ".env")


# Supported backends. "azure-openai" is the default for this talk.
AZURE_OPENAI = "azure-openai"
FOUNDRY = "foundry"
GITHUB = "github"
OPENAI = "openai"


@dataclass
class Settings:
    """Resolved settings for the active backend."""

    backend: str
    model: str
    # Azure OpenAI
    azure_endpoint: str | None = None
    azure_api_version: str | None = None
    azure_api_key: str | None = None
    # Foundry
    foundry_project_endpoint: str | None = None
    # GitHub Models / OpenAI-compatible
    base_url: str | None = None
    api_key: str | None = None
    # Observability
    enable_tracing: bool = False

    def describe(self) -> str:
        target = {
            AZURE_OPENAI: self.azure_endpoint,
            FOUNDRY: self.foundry_project_endpoint,
            GITHUB: self.base_url,
            OPENAI: self.base_url or "https://api.openai.com/v1",
        }.get(self.backend, "?")
        return f"backend={self.backend} model={self.model} target={target}"


def _bool(value: str | None) -> bool:
    return (value or "").strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    """Read environment variables and return a validated :class:`Settings`."""

    backend = os.getenv("MODEL_BACKEND", AZURE_OPENAI).strip().lower()
    enable_tracing = _bool(os.getenv("ENABLE_TRACING"))

    if backend == AZURE_OPENAI:
        return Settings(
            backend=backend,
            model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o-mini"),
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            azure_api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
            azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            enable_tracing=enable_tracing,
        )
    if backend == FOUNDRY:
        return Settings(
            backend=backend,
            model=os.getenv("FOUNDRY_MODEL", "gpt-4o-mini"),
            foundry_project_endpoint=os.getenv("FOUNDRY_PROJECT_ENDPOINT"),
            enable_tracing=enable_tracing,
        )
    if backend == GITHUB:
        return Settings(
            backend=backend,
            model=os.getenv("GITHUB_MODEL", "openai/gpt-4o-mini"),
            base_url=os.getenv("GITHUB_MODELS_ENDPOINT", "https://models.github.ai/inference"),
            api_key=os.getenv("GITHUB_TOKEN"),
            enable_tracing=enable_tracing,
        )
    if backend == OPENAI:
        return Settings(
            backend=backend,
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            base_url=os.getenv("OPENAI_BASE_URL"),
            api_key=os.getenv("OPENAI_API_KEY"),
            enable_tracing=enable_tracing,
        )

    raise ValueError(
        f"Unknown MODEL_BACKEND={backend!r}. "
        f"Use one of: {AZURE_OPENAI}, {FOUNDRY}, {GITHUB}, {OPENAI}."
    )
