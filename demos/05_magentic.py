"""Demo 05 — MAGENTIC orchestration: the launch brief.

Pattern: a *manager* agent dynamically plans and coordinates specialists — it
balances the structure of a workflow with the flexibility of open-ended reasoning.
    LaunchManager  ─plans▶  { Researcher, Analyst }  ─synthesizes▶  brief

This is the most "autonomous" building block. ``max_round_count`` / ``max_stall_count``
keep the manager's inner loop bounded.

Tip: set ``enable_plan_review=True`` (see 06) to require a human to approve the
manager's plan before work starts — human-in-the-loop for open-ended tasks.

Run:  python demos/05_magentic.py
"""

import asyncio

import _bootstrap  # noqa: F401

from agent_framework.orchestrations import MagenticBuilder

from contoso import get_chat_client
from contoso.agents import analyst, launch_manager, researcher
from contoso.pretty import run_workflow
from contoso.tracing import enable_tracing


async def main() -> None:
    enable_tracing()
    client = get_chat_client()

    workflow = MagenticBuilder(
        participants=[researcher(client), analyst(client)],
        manager_agent=launch_manager(client),
        max_round_count=8,
        max_stall_count=2,
        max_reset_count=1,
        intermediate_output_from="all",
    ).build()

    await run_workflow(
        workflow,
        (
            "Produce a go-to-market launch brief for the Summit 35L ultralight backpack, "
            "targeting weekend backpackers. Include positioning, target segments, three key "
            "messages, and top risks."
        ),
        title="05 — Magentic: Manager coordinates Researcher + Analyst",
    )


if __name__ == "__main__":
    asyncio.run(main())
