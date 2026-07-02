"""Contoso Outdoors Launch Desk — shared helpers for the MAF + Foundry Toolkit demo.

This package holds the *reusable* pieces so each demo script under ``demos/`` stays
short and readable on a projector:

- ``config``  — load ``.env`` and resolve which model backend to use.
- ``client``  — build a backend-agnostic chat client (Azure OpenAI / Foundry / GitHub / OpenAI).
- ``agents``  — factory functions that create the agents used across the demos.
- ``tools``   — function tools, including approval-gated (human-in-the-loop) ones.
- ``tracing`` — one-line OpenTelemetry setup that streams traces to the Foundry Toolkit.
- ``pretty``  — small printing helpers so workflow output reads well in a terminal.
"""

from .client import get_chat_client, make_agent
from .config import Settings, get_settings

__all__ = ["Settings", "get_settings", "get_chat_client", "make_agent"]
