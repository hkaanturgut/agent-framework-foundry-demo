"""Demo 04 — GROUP CHAT orchestration: the headline brainstorm.

Pattern: agents share one conversation and take turns — great for debate, review,
or brainstorming until they converge.
    Copywriter  ⇄  HeadlineEditor   (round-robin, until 'SHIP IT')

A round-robin selector alternates speakers; the editor ends the chat when a
headline is good enough. ``max_rounds`` is a safety backstop.

Run:  python demos/04_group_chat.py
"""

import asyncio
from typing import Any

import _bootstrap  # noqa: F401

from agent_framework.orchestrations import GroupChatBuilder

from contoso import get_chat_client
from contoso.agents import copywriter, headline_editor
from contoso.pretty import run_workflow, to_text
from contoso.tracing import enable_tracing


def round_robin(state: Any) -> str:
    """Pick the next speaker by rotating through the participants."""
    names = list(state.participants.keys())
    return names[state.current_round % len(names)]


def shipped(conversation) -> bool:
    """Stop as soon as the editor says 'SHIP IT'."""
    if not conversation:
        return False
    return "ship it" in to_text(conversation[-1]).lower()


async def main() -> None:
    enable_tracing()
    client = get_chat_client()

    workflow = GroupChatBuilder(
        participants=[copywriter(client), headline_editor(client)],
        selection_func=round_robin,
        termination_condition=shipped,
        max_rounds=6,
        intermediate_output_from="all",
    ).build()

    await run_workflow(
        workflow,
        "Brainstorm a launch headline for the new Summit 35L ultralight backpack.",
        title="04 — Group Chat: Copywriter ⇄ Editor",
    )


if __name__ == "__main__":
    asyncio.run(main())
