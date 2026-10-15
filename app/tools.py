
from uuid import uuid4

from langchain_core.tools import tool


# Mock order database for development.
ORDERS = {
    "ORD1001": {
        "status": "Shipped",
        "estimated_delivery": "2026-10-18",
    },
    "ORD1002": {
        "status": "Processing",
        "estimated_delivery": "Not yet available",
    },
    "ORD1003": {
        "status": "Delivered",
        "estimated_delivery": "2026-10-12",
    },
}

# Temporary storage. Tickets disappear when the process restarts.
TICKETS = {}


@tool
def lookup_order_status(order_id: str) -> str:
    """Look up the status and estimated delivery of an order using its order ID."""
    normalized_id = order_id.strip().upper()
    order = ORDERS.get(normalized_id)

    if order is None:
        return (
            f"No order found for {normalized_id}. "
            "Ask the customer to verify their order ID."
        )

    return (
        f"Order ID: {normalized_id}\n"
        f"Status: {order['status']}\n"
        f"Estimated delivery: {order['estimated_delivery']}"
    )


@tool
def create_support_ticket(
    issue: str,
    order_id: str = "",
) -> str:
    """Create a support ticket when a customer requests follow-up or needs human help."""
    clean_issue = issue.strip()

    if not clean_issue:
        return "Cannot create a ticket without an issue description."

    ticket_id = f"TKT-{uuid4().hex[:8].upper()}"

    ticket = {
        "ticket_id": ticket_id,
        "issue": clean_issue,
        "order_id": order_id.strip().upper() or None,
        "status": "Open",
    }

    TICKETS[ticket_id] = ticket

    return (
        f"Support ticket created successfully.\n"
        f"Ticket ID: {ticket_id}\n"
        f"Status: Open"
    )
