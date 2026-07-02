"""One-line OpenTelemetry setup that streams traces to the Foundry Toolkit.

The Foundry Toolkit for VS Code runs a local OTLP collector. Calling
``configure_otel_providers(vs_code_extension_port=4317)`` points Agent Framework's
built-in instrumentation at it, so every agent run, tool call, and workflow step
shows up in the toolkit's **Tracing** view — great for a live "look inside the
agents" moment.

Enable it by setting ``ENABLE_TRACING=true`` in ``.env``.
"""

from __future__ import annotations

from .config import get_settings


def enable_tracing() -> bool:
    """Turn on tracing if ``ENABLE_TRACING=true``. Returns whether it was enabled."""

    settings = get_settings()
    if not settings.enable_tracing:
        return False

    try:
        from agent_framework.observability import configure_otel_providers
    except ImportError:
        print("[tracing] agent_framework.observability not available; skipping.")
        return False

    # vs_code_extension_port wires traces to the Foundry Toolkit local collector.
    configure_otel_providers(vs_code_extension_port=4317, enable_console_exporters=False)
    print("[tracing] OpenTelemetry enabled -> Foundry Toolkit (localhost:4317)")
    return True
