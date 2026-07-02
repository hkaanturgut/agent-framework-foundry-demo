"""Small printing helpers so orchestration output reads well on a projector.

Kept deliberately defensive: workflow event ``data`` can be a string, an
``AgentResponse``/``Message`` (has ``.text``), or a list of messages. ``to_text``
flattens any of those to something printable.
"""

from __future__ import annotations

from typing import Any

RULE = "\u2500" * 68  # ─


def banner(title: str) -> None:
    print(f"\n{RULE}\n  {title}\n{RULE}")


def to_text(obj: Any) -> str:
    """Best-effort conversion of a workflow output/event payload to text."""

    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    text = getattr(obj, "text", None)
    if isinstance(text, str) and text.strip():
        return text
    if isinstance(obj, (list, tuple)):
        parts = [to_text(item) for item in obj]
        return "\n".join(p for p in parts if p.strip())
    return str(obj)


async def run_workflow(workflow: Any, task: str, *, title: str, show_steps: bool = True) -> Any:
    """Run a workflow to completion and print intermediate + final output.

    Uses the non-streaming ``await workflow.run(task)`` path, which returns a
    ``WorkflowRunResult`` exposing ``get_intermediate_outputs()`` and
    ``get_outputs()``. This is the most robust path for a live demo.
    """

    banner(title)
    print(f"Task: {task}\n")

    result = await workflow.run(task)

    if show_steps:
        steps = result.get_intermediate_outputs()
        for i, step in enumerate(steps, start=1):
            text = to_text(step).strip()
            if text:
                print(f"── step {i} ──\n{text}\n")

    print("═══ FINAL OUTPUT ═══")
    for out in result.get_outputs():
        print(to_text(out).strip())
    print()
    return result
