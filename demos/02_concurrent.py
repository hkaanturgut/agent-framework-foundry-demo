"""Demo 02 — CONCURRENT orchestration: the parallel review board.

Pattern: agents run in parallel on the same input, then results are aggregated.
    ┌─▶ SEO ─┐
    ├─▶ Legal┤─▶ (aggregated)
    └─▶ Brand┘

Use it when tasks are independent and you want to cut latency: three reviewers
look at the same copy at once instead of waiting in line.

Run:  python demos/02_concurrent.py
"""

import asyncio

import _bootstrap  # noqa: F401

from agent_framework.orchestrations import ConcurrentBuilder

from contoso import get_chat_client
from contoso.agents import brand_reviewer, legal_reviewer, seo_reviewer
from contoso.pretty import run_workflow
from contoso.tracing import enable_tracing

COPY = (
    "The all-new Summit backpack is the BEST pack ever made — guaranteed to make every "
    "hike perfect. Ultralight 35L, weatherproof, and built for adventure."
)


async def main() -> None:
    enable_tracing()
    client = get_chat_client()

    workflow = ConcurrentBuilder(
        participants=[seo_reviewer(client), legal_reviewer(client), brand_reviewer(client)],
        intermediate_output_from="all",
    ).build()

    await run_workflow(
        workflow,
        f"Review this marketing copy from three angles:\n\n{COPY}",
        title="02 — Concurrent: SEO ∥ Legal ∥ Brand",
    )


if __name__ == "__main__":
    asyncio.run(main())
