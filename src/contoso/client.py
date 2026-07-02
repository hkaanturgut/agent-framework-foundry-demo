"""Build a backend-agnostic chat client and a small ``make_agent`` helper.

Every demo calls :func:`get_chat_client` once and reuses it for all agents.
Switching backends is a ``.env`` change — no code edits required.

Verified against **agent-framework 1.10.0**:
- Azure OpenAI is a *mode* of ``OpenAIChatClient`` (pass ``azure_endpoint`` +
  ``api_version``). There is no separate ``AzureOpenAIChatClient`` class in this
  release.
- Foundry uses ``agent_framework.foundry.FoundryChatClient``.
- GitHub Models / OpenAI-compatible endpoints use ``OpenAIChatClient(base_url=...)``.
"""

from __future__ import annotations

from typing import Any

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient

from .config import (
    AZURE_OPENAI,
    FOUNDRY,
    GITHUB,
    OPENAI,
    Settings,
    get_settings,
)


def get_chat_client(settings: Settings | None = None) -> Any:
    """Return a chat client for the configured backend.

    The return type is intentionally ``Any`` because different backends return
    different concrete client classes; all of them satisfy the interface the
    agents and orchestration builders expect.
    """

    settings = settings or get_settings()

    if settings.backend == AZURE_OPENAI:
        if not settings.azure_endpoint:
            raise RuntimeError(
                "AZURE_OPENAI_ENDPOINT is not set. Copy .env.example to .env and fill it in, "
                "or switch MODEL_BACKEND=github for a zero-Azure fallback."
            )
        # Prefer an API key if provided; otherwise use Entra ID (az login / VS Code).
        if settings.azure_api_key:
            return OpenAIChatClient(
                model=settings.model,
                azure_endpoint=settings.azure_endpoint,
                api_version=settings.azure_api_version,
                api_key=settings.azure_api_key,
            )
        from azure.identity import AzureCliCredential

        return OpenAIChatClient(
            model=settings.model,
            azure_endpoint=settings.azure_endpoint,
            api_version=settings.azure_api_version,
            credential=AzureCliCredential(),
        )

    if settings.backend == FOUNDRY:
        from agent_framework.foundry import FoundryChatClient
        from azure.identity import AzureCliCredential

        if not settings.foundry_project_endpoint:
            raise RuntimeError("FOUNDRY_PROJECT_ENDPOINT is not set.")
        return FoundryChatClient(
            project_endpoint=settings.foundry_project_endpoint,
            model=settings.model,
            credential=AzureCliCredential(),
        )

    if settings.backend in (GITHUB, OPENAI):
        if not settings.api_key:
            key_name = "GITHUB_TOKEN" if settings.backend == GITHUB else "OPENAI_API_KEY"
            raise RuntimeError(f"{key_name} is not set for MODEL_BACKEND={settings.backend}.")
        kwargs: dict[str, Any] = {"model": settings.model, "api_key": settings.api_key}
        if settings.base_url:
            kwargs["base_url"] = settings.base_url
        return OpenAIChatClient(**kwargs)

    raise ValueError(f"Unsupported backend: {settings.backend}")


def make_agent(
    client: Any,
    name: str,
    instructions: str,
    *,
    description: str | None = None,
    tools: Any = None,
    require_history_persistence: bool = False,
) -> Agent:
    """Create an :class:`agent_framework.Agent` bound to ``client``.

    A thin convenience wrapper so demo scripts read as a list of roles rather
    than a wall of constructor arguments.

    ``require_history_persistence`` maps to the Agent's
    ``require_per_service_call_history_persistence`` flag, which the **Handoff**
    orchestration requires on every participant so local history stays consistent
    across handoff tool-call short-circuits.
    """

    return Agent(
        client=client,
        name=name,
        description=description,
        instructions=instructions,
        tools=tools,
        require_per_service_call_history_persistence=require_history_persistence,
    )
