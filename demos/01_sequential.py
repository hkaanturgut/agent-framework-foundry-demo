"""Demo 01 — SEQUENTIAL orchestration: the blog pipeline.

Pattern: agents run one after another; each builds on the previous output.
    Outliner ─▶ Writer ─▶ Editor

This is the "assembly line" building block. Notice how little code the pattern
takes: ``SequentialBuilder(participants=[...]).build()``.

Run:  python demos/01_sequential.py
"""

import asyncio

import _bootstrap  # noqa: F401

from agent_framework.orchestrations import SequentialBuilder

from contoso import get_chat_client
from contoso.agents import editor, outliner, writer
from contoso.pretty import run_workflow
from contoso.tracing import enable_tracing


async def main() -> None:
    enable_tracing()
    client = get_chat_client()

    workflow = SequentialBuilder(
        participants=[outliner(client), writer(client), editor(client)],
        intermediate_output_from="all",  # so we can show each stage on screen
    ).build()

    await run_workflow(
        workflow,
        "How to choose your first 3-season backpacking tent.",
        title="01 — Sequential: Outliner ▶ Writer ▶ Editor",
    )


if __name__ == "__main__":
    asyncio.run(main())
