import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient

MCP_SERVER_URL = "http://127.0.0.1:8001/mcp"

async def get_mcp_tools():
    client = MultiServerMCPClient({
        "customer_support": {
            "transport": "streamable_http",
            "url": MCP_SERVER_URL,
        }
    })
    return await client.get_tools()

async def main():
    tools = await get_mcp_tools()

    print("Tools discovered from MCP server:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description}")

if __name__ == "__main__":
    asyncio.run(main())