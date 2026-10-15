
from app.tools import create_support_ticket


def open_support_ticket(
    issue: str,
    order_id: str = "",
) -> str:
    """Create a support ticket for a customer issue."""
    return create_support_ticket.invoke({
        "issue": issue,
        "order_id": order_id,
    })
