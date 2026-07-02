"""Demo 06 — HUMAN-IN-THE-LOOP: approval-gated tools.

Every orchestration building block supports human-in-the-loop. The simplest form:
a tool marked ``approval_mode="always_require"`` pauses the run and asks a human
before it executes. Here the Publisher agent writes a post and then tries to call
``publish_blog`` — which we must approve.

How it works (verified against agent-framework 1.10):
    result = await workflow.run(task)
    for ev in result.get_request_info_events():        # approvals surface as request_info
        req = ev.data                                  # a 'function_approval_request'
        responses[ev.request_id] = req.to_function_approval_response(approved=...)
    result = await workflow.run(responses=responses)   # resume with the decision

Run:  python demos/06_hitl_approval.py            (interactive)
      python demos/06_hitl_approval.py --yes      (auto-approve, e.g. for a dry run)
      python demos/06_hitl_approval.py --no        (auto-reject)
"""

import asyncio
import sys

import _bootstrap  # noqa: F401

from agent_framework.orchestrations import SequentialBuilder

from contoso import get_chat_client
from contoso.agents import publisher
from contoso.pretty import banner, to_text
from contoso.tracing import enable_tracing


def decide(tool_name: str, args: str) -> bool:
    if "--yes" in sys.argv:
        print(f"[auto-approve] {tool_name}")
        return True
    if "--no" in sys.argv:
        print(f"[auto-reject] {tool_name}")
        return False
    answer = input(f"\n[APPROVAL NEEDED] Run '{tool_name}' with {args}? (y/n): ")
    return answer.strip().lower() == "y"


async def main() -> None:
    enable_tracing()
    client = get_chat_client()

    workflow = SequentialBuilder(participants=[publisher(client)]).build()

    banner("06 — Human-in-the-loop: publish requires approval")
    task = "Write a short blog post announcing the Summit 35L backpack, then publish it."
    print(f"Task: {task}\n")

    result = await workflow.run(task)
    pending = result.get_request_info_events()

    while pending:
        responses = {}
        for ev in pending:
            req = ev.data
            fn = getattr(req, "function_call", None)
            tool_name = getattr(fn, "name", "tool")
            args = getattr(fn, "arguments", "") or ""
            approved = decide(tool_name, str(args)[:120])
            responses[ev.request_id] = req.to_function_approval_response(approved=approved)
        result = await workflow.run(responses=responses)
        pending = result.get_request_info_events()

    print("\n═══ RESULT ═══")
    for out in result.get_outputs():
        print(to_text(out).strip())


if __name__ == "__main__":
    asyncio.run(main())
