"""Agent factory functions for the Contoso Outdoors Launch Desk.

Each function takes a chat ``client`` and returns a configured ``Agent``. Keeping
the personas here (instead of inline in every demo) means the demo scripts stay
short and the *orchestration pattern* is what stands out on screen.
"""

from __future__ import annotations

from typing import Any

from .client import make_agent
from .tools import check_inventory, lookup_order, publish_blog, submit_refund

# ── Content pipeline (Sequential) ─────────────────────────────────────────────


def outliner(client: Any):
    return make_agent(
        client,
        name="Outliner",
        description="Turns a topic into a tight blog outline.",
        instructions=(
            "You are a content strategist for Contoso Outdoors, an outdoor gear brand. "
            "Given a topic, produce a punchy blog outline: a working title plus 3-5 "
            "section headings with a one-line note each. Be concise."
        ),
    )


def writer(client: Any):
    return make_agent(
        client,
        name="Writer",
        description="Writes the draft from the outline.",
        instructions=(
            "You are a copywriter for Contoso Outdoors. Expand the provided outline into "
            "an engaging first draft (~200 words). Friendly, active voice, concrete."
        ),
    )


def editor(client: Any):
    return make_agent(
        client,
        name="Editor",
        description="Polishes the draft into the final version.",
        instructions=(
            "You are a senior editor. Tighten the draft, fix flow and grammar, and return "
            "the final publish-ready post. Return only the finished post."
        ),
    )


# ── Parallel review board (Concurrent) ────────────────────────────────────────


def seo_reviewer(client: Any):
    return make_agent(
        client,
        name="SEO",
        description="Reviews copy for search performance.",
        instructions=(
            "You are an SEO specialist. Review the copy and return 3 concrete, prioritized "
            "SEO improvements (keywords, headings, meta). Bullet points only."
        ),
    )


def legal_reviewer(client: Any):
    return make_agent(
        client,
        name="Legal",
        description="Flags compliance and claims risk.",
        instructions=(
            "You are a compliance reviewer. Flag any unsupported claims, risky superlatives, "
            "or missing disclaimers in the copy. Bullet points only. If clean, say so."
        ),
    )


def brand_reviewer(client: Any):
    return make_agent(
        client,
        name="Brand",
        description="Checks tone and brand voice.",
        instructions=(
            "You are a brand voice guardian for Contoso Outdoors (adventurous, warm, "
            "no hype). Return 3 tone/voice notes as bullet points."
        ),
    )


# ── Support desk (Handoff) ────────────────────────────────────────────────────


def triage(client: Any):
    return make_agent(
        client,
        name="triage_agent",
        description="Frontline support that routes to a specialist.",
        instructions=(
            "You are frontline support triage for Contoso Outdoors. Read the customer "
            "message and hand off to the right specialist: order questions -> order_agent, "
            "returns -> returns_agent, refunds -> refund_agent. Do not solve it yourself; route it."
        ),
        require_history_persistence=True,
    )


def order_agent(client: Any):
    return make_agent(
        client,
        name="order_agent",
        description="Handles order status and shipping questions.",
        instructions=(
            "You handle order status and shipping questions. Use lookup_order when an order "
            "id is provided. End your reply with 'Case complete.' when resolved."
        ),
        tools=[lookup_order],
        require_history_persistence=True,
    )


def returns_agent(client: Any):
    return make_agent(
        client,
        name="returns_agent",
        description="Handles product returns.",
        instructions=(
            "You handle product returns. Explain the return steps clearly. If the customer "
            "then wants their money back, hand off to refund_agent. End with 'Case complete.' when done."
        ),
        require_history_persistence=True,
    )


def refund_agent(client: Any):
    return make_agent(
        client,
        name="refund_agent",
        description="Processes refunds (with human approval).",
        instructions=(
            "You process refunds. Look up the order with lookup_order, then call submit_refund. "
            "submit_refund requires human approval before it runs. End with 'Case complete.' when done."
        ),
        tools=[lookup_order, submit_refund],
        require_history_persistence=True,
    )


# ── Headline brainstorm (Group Chat) ──────────────────────────────────────────


def copywriter(client: Any):
    return make_agent(
        client,
        name="Copywriter",
        description="Proposes bold headlines.",
        instructions=(
            "You are a bold copywriter. Propose ONE punchy headline per turn for the product, "
            "then briefly react to the editor's feedback and improve it next turn."
        ),
    )


def headline_editor(client: Any):
    return make_agent(
        client,
        name="HeadlineEditor",
        description="Critiques and sharpens headlines.",
        instructions=(
            "You are a sharp editor. Critique the copywriter's headline in one line and suggest "
            "how to make it tighter. When a headline is genuinely great, reply exactly: 'SHIP IT: <headline>'."
        ),
    )


# ── Launch brief (Magentic) ───────────────────────────────────────────────────


def researcher(client: Any):
    return make_agent(
        client,
        name="Researcher",
        description="Gathers facts and market context.",
        instructions=(
            "You are a market researcher. Gather relevant facts, comparisons, and customer "
            "angles for the requested product/topic. No fabrication; note assumptions."
        ),
    )


def analyst(client: Any):
    return make_agent(
        client,
        name="Analyst",
        description="Turns research into a structured recommendation.",
        instructions=(
            "You are a go-to-market analyst. Turn research into a structured launch brief: "
            "positioning, target segments, 3 key messages, and risks. Use short sections."
        ),
    )


def launch_manager(client: Any):
    return make_agent(
        client,
        name="LaunchManager",
        description="Coordinates the researcher and analyst to produce the brief.",
        instructions=(
            "You coordinate a small team (Researcher, Analyst) to produce a launch brief. "
            "Plan the steps, delegate, and synthesize a final brief."
        ),
    )


# ── Single agent with an approval-gated tool (HITL) ───────────────────────────


def publisher(client: Any):
    return make_agent(
        client,
        name="Publisher",
        description="Writes and publishes blog posts (publish requires approval).",
        instructions=(
            "You are the Contoso Outdoors publisher. Write a short blog post for the requested "
            "topic, then call publish_blog to publish it. publish_blog requires human approval."
        ),
        tools=[publish_blog, check_inventory],
    )
