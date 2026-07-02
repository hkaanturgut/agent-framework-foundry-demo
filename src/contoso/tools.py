"""Function tools for the Contoso Outdoors agents.

Two kinds are shown on purpose:

- **Read-only tools** (``check_inventory``, ``lookup_order``) run automatically.
- **Write / high-impact tools** (``submit_refund``, ``publish_blog``) are marked
  ``approval_mode="always_require"`` so Agent Framework pauses and asks a human
  before executing them. This is the enterprise "human-in-the-loop" story.

The data here is fake — the point is to show tool-calling and approval gates,
not to model a real catalog.
"""

from __future__ import annotations

from typing import Annotated

from agent_framework import tool
from pydantic import Field

# A tiny fake catalog / order book so tool calls return believable data.
_INVENTORY = {
    "trailblazer-tent": 42,
    "summit-backpack": 7,
    "riverrun-kayak": 0,
    "alpine-jacket": 128,
}
_ORDERS = {
    "A1001": {"item": "summit-backpack", "status": "delivered", "total": 189.00},
    "A1002": {"item": "riverrun-kayak", "status": "in-transit", "total": 749.00},
    "A1003": {"item": "alpine-jacket", "status": "delivered", "total": 219.00},
}


@tool
def check_inventory(
    sku: Annotated[str, Field(description="Product SKU, e.g. 'summit-backpack'.")],
) -> str:
    """Return how many units of a SKU are in stock (read-only)."""
    qty = _INVENTORY.get(sku.lower())
    if qty is None:
        return f"SKU '{sku}' not found."
    return f"{sku}: {qty} in stock" + (" (BACKORDER)" if qty == 0 else "")


@tool
def lookup_order(
    order_id: Annotated[str, Field(description="Order id, e.g. 'A1002'.")],
) -> str:
    """Look up the status and total of an order (read-only)."""
    order = _ORDERS.get(order_id.upper())
    if not order:
        return f"Order '{order_id}' not found."
    return f"Order {order_id}: {order['item']}, status={order['status']}, total=${order['total']:.2f}"


@tool(approval_mode="always_require")
def submit_refund(
    order_id: Annotated[str, Field(description="Order id to refund.")],
    amount: Annotated[float, Field(description="Refund amount in USD.")],
    reason: Annotated[str, Field(description="Short reason for the refund.")],
) -> str:
    """Issue a refund. Requires human approval before it runs."""
    return f"REFUND ISSUED: ${amount:.2f} for order {order_id} ({reason})."


@tool(approval_mode="always_require")
def publish_blog(
    title: Annotated[str, Field(description="Blog post title.")],
    body: Annotated[str, Field(description="Full markdown body of the post.")],
) -> str:
    """Publish a blog post to the live site. Requires human approval before it runs."""
    return f"PUBLISHED: '{title}' ({len(body)} chars) is now live on contoso-outdoors.com/blog."
