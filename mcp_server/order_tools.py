
from app.tools import lookup_order_status


def get_order_status(order_id: str) -> str:
    """Look up an order by its ID."""
    return lookup_order_status.invoke({
        "order_id": order_id,
    })
