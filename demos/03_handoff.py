"""Demo 03 — HANDOFF orchestration: the support desk.

Pattern: a triage agent transfers control to the right specialist based on context.
    triage ─▶ order_agent
           ─▶ returns_agent ─▶ refund_agent
           ─▶ refund_agent

Use it to route to specialists instead of stuffing everything into one giant
prompt. Here we ask an order-status question, so triage hands off to order_agent,
which uses the ``lookup_order`` tool and closes the case.

Run:  python demos/03_handoff.py
"""

import asyncio

import _bootstrap  # noqa: F401

from agent_framework.orchestrations import HandoffBuilder

from contoso import get_chat_client
from contoso.agents import order_agent, refund_agent, returns_agent, triage
from contoso.pretty import to_text
from contoso.tracing import enable_tracing


def case_is_closed(conversation) -> bool:
    """Terminate once a specialist signs off with 'Case complete.'."""
    if not conversation:
        return False
    return "case complete." in to_text(conversation[-1]).lower()


async def main() -> None:
    enable_tracing()
    client = get_chat_client()

    triage_agent = triage(client)
    orders = order_agent(client)
    returns = returns_agent(client)
    refunds = refund_agent(client)

    workflow = (
        HandoffBuilder(
            name="contoso_support",
            participants=[triage_agent, orders, returns, refunds],
            termination_condition=case_is_closed,
        )
        .with_start_agent(triage_agent)
        .add_handoff(triage_agent, [orders, returns, refunds])
        .add_handoff(returns, [refunds])
        .add_handoff(orders, [triage_agent])
        .build()
    )

    task = "Hi, where is my order A1002? It was supposed to arrive last week."
    print("Customer:", task, "\n")

    result = await workflow.run(task)
    for step in result.get_intermediate_outputs():
        text = to_text(step).strip()
        if text:
            print(text, "\n")
    print("═══ RESOLUTION ═══")
    for out in result.get_outputs():
        print(to_text(out).strip())


if __name__ == "__main__":
    asyncio.run(main())
