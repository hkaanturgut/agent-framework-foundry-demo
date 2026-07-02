"""Demo 00 — a single agent (the baseline).

Story: "Before orchestration, an agent is just a model + instructions + tools."
This is also the thing you first build in the Foundry Toolkit **Agent Builder** /
test in the **Playground** before you ever write code.

Run:  python demos/00_single_agent.py
"""

import asyncio

import _bootstrap  # noqa: F401  (adds src/ to sys.path)

from contoso import get_chat_client, get_settings
from contoso.agents import writer
from contoso.pretty import banner
from contoso.tracing import enable_tracing


async def main() -> None:
    enable_tracing()
    print(get_settings().describe())

    client = get_chat_client()
    agent = writer(client)

    banner("00 — Single agent")
    prompt = "Write a friendly 2-sentence blurb for the Summit backpack (35L, ultralight)."
    print(f"Prompt: {prompt}\n")

    response = await agent.run(prompt)
    print(response.text)


if __name__ == "__main__":
    asyncio.run(main())
