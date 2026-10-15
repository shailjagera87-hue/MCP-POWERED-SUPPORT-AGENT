
from mcp.server.fastmcp import FastMCP

from mcp_server.order_tools import get_order_status
from mcp_server.ticket_tools import open_support_ticket

mcp = FastMCP("Customer Support MCP Server")


@mcp.tool()
def lookup_order(order_id: str) -> str:
    """Get the status and estimated delivery date for an order."""
    return get_order_status(order_id)


@mcp.tool()
def create_ticket(issue: str, order_id: str = "") -> str:
    """Create a support ticket when a customer needs human assistance."""
    return open_support_ticket(issue, order_id)


if __name__ == "__main__":
    mcp.settings.host = "127.0.0.1"
    mcp.settings.port = 8001
    mcp.run(transport="streamable-http")
