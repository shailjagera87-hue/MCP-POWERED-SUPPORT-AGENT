
from app.tools import (
    ORDERS,
    TICKETS,
    lookup_order_status,
    create_support_ticket,
)


def test_lookup_existing_order():
    result = lookup_order_status.invoke({"order_id": "ORD1001"})

    assert "Shipped" in result
    assert "ORD1001" in result


def test_lookup_order_case_insensitive():
    result = lookup_order_status.invoke({"order_id": "ord1001"})

    assert "Shipped" in result


def test_lookup_unknown_order():
    result = lookup_order_status.invoke({"order_id": "UNKNOWN123"})

    assert "No order found" in result


def test_create_ticket():
    result = create_support_ticket.invoke({
        "issue": "Package arrived damaged",
        "order_id": "ORD1001",
    })

    assert "Support ticket created successfully" in result
    assert "Ticket ID:" in result
    assert len(TICKETS) > 0


def test_create_ticket_without_order_id():
    result = create_support_ticket.invoke({
        "issue": "I need help with my account",
    })

    assert "Support ticket created successfully" in result


def test_empty_ticket_issue():
    result = create_support_ticket.invoke({
        "issue": "   ",
    })

    assert "Cannot create a ticket" in result
