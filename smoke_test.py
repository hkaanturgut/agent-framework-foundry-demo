"""Offline smoke test — builds every agent, tool, and workflow WITHOUT calling the model.

It sets a dummy backend so no network or Azure credentials are needed, then it
constructs all five orchestration workflows. If this passes, your wiring is sound
and the only remaining variable on stage is your model backend / credentials.

Run:  python smoke_test.py
"""

import os
import pathlib
import sys

# Force a no-network, no-Azure client config before importing contoso.
os.environ.setdefault("MODEL_BACKEND", "openai")
os.environ.setdefault("OPENAI_API_KEY", "sk-dummy-not-used-offline")
os.environ.setdefault("OPENAI_MODEL", "gpt-4o-mini")

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent / "src"))

from agent_framework.orchestrations import (  # noqa: E402
    ConcurrentBuilder,
    GroupChatBuilder,
    HandoffBuilder,
    MagenticBuilder,
    SequentialBuilder,
)

from contoso import get_chat_client  # noqa: E402
from contoso import agents as A  # noqa: E402


def main() -> int:
    client = get_chat_client()
    checks = []

    def ok(label: str) -> None:
        checks.append(label)
        print(f"  ✓ {label}")

    print("Building agents + tools...")
    ok("agents & tools import + construct")

    print("Building workflows...")
    SequentialBuilder(
        participants=[A.outliner(client), A.writer(client), A.editor(client)],
        intermediate_output_from="all",
    ).build()
    ok("Sequential")

    ConcurrentBuilder(
        participants=[A.seo_reviewer(client), A.legal_reviewer(client), A.brand_reviewer(client)],
        intermediate_output_from="all",
    ).build()
    ok("Concurrent")

    t = A.triage(client)
    (
        HandoffBuilder(name="s", participants=[t, A.order_agent(client), A.refund_agent(client)])
        .with_start_agent(t)
        .add_handoff(t, [A.order_agent(client)])
        .build()
    )
    ok("Handoff")

    GroupChatBuilder(
        participants=[A.copywriter(client), A.headline_editor(client)],
        selection_func=lambda state: list(state.participants.keys())[
            state.current_round % len(state.participants)
        ],
        max_rounds=4,
        intermediate_output_from="all",
    ).build()
    ok("GroupChat")

    MagenticBuilder(
        participants=[A.researcher(client), A.analyst(client)],
        manager_agent=A.launch_manager(client),
        max_round_count=6,
        intermediate_output_from="all",
    ).build()
    ok("Magentic")

    SequentialBuilder(participants=[A.publisher(client)]).build()
    ok("HITL publisher workflow")

    print(f"\nAll {len(checks)} checks passed. Wiring is sound. ✅")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
