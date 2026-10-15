
from typing import Literal

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.config import settings
from app.vector_store import load_vector_store
import os

MCP_SERVER_URL = settings.mcp_server_url




SYSTEM_PROMPT = """
You are a helpful customer support agent.

Your responsibilities:
1. Answer customer questions using the provided knowledge-base context.
2. Use the available MCP tools to look up order status or create support tickets.
3. Never invent order information, delivery dates, or ticket IDs.
4. If an order ID is missing, ask the customer for it before looking up an order.
5. Create a support ticket when the customer requests human assistance or
   when their issue needs follow-up.
6. If the knowledge base does not contain enough information, say so honestly.
7. Be professional, clear, concise, and friendly.

Knowledge-base context:
{context}
"""


async def get_mcp_tools():
    """Connect to the MCP server and retrieve its tools."""
    client = MultiServerMCPClient(
        {
            "customer_support": {
                "transport": "streamable_http",
                "url": MCP_SERVER_URL,
            }
        }
    )
    return await client.get_tools()


def retrieve_context(question: str, k: int = 4) -> str:
    """Retrieve relevant knowledge-base documents from FAISS."""
    store = load_vector_store()
    results = store.similarity_search_with_relevance_scores(
        question,
        k=k,
    )

    relevant_chunks = [
        doc.page_content
        for doc, score in results
        if score > 0.2
    ]

    if not relevant_chunks:
        return "No relevant knowledge-base information was found."

    return "\n\n---\n\n".join(relevant_chunks)


async def ask_support(question: str) -> str:
    """Run the customer support agent using Groq, LangGraph, and MCP."""
    question = question.strip()
    if not question:
        raise ValueError("Question cannot be empty.")

    # Discover the tools exposed by the running MCP server.
    tools = await get_mcp_tools()

    # Initialize the Groq model with tool-calling support.
    llm = ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
    ).bind_tools(tools)

    # Retrieve relevant context from the local FAISS index.
    context = retrieve_context(question)

    system_message = SystemMessage(
        content=SYSTEM_PROMPT.format(context=context)
    )

    # Define the graph's model node.
    async def call_model(state: MessagesState):
        messages = [system_message, *state["messages"]]
        response = await llm.ainvoke(messages)
        return {"messages": [response]}

    # Execute MCP tool calls requested by the model.
    tool_node = ToolNode(tools)

    # Build the LangGraph workflow.
    builder = StateGraph(MessagesState)
    builder.add_node("assistant", call_model)
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "assistant")
    builder.add_conditional_edges(
        "assistant",
        tools_condition,
        {
            "tools": "tools",
            END: END,
        },
    )
    builder.add_edge("tools", "assistant")

    graph = builder.compile()

    # Run the graph until the model produces a final answer.
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=question)]}
    )

    # Return the latest assistant response as text.
    for message in reversed(result["messages"]):
        if (
            getattr(message, "type", None) == "ai"
            and not getattr(message, "tool_calls", None)
        ):
            content = message.content
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                text_parts = [
                    item["text"]
                    for item in content
                    if isinstance(item, dict)
                    and item.get("type") == "text"
                ]
                if text_parts:
                    return "\n".join(text_parts)

    return "I'm sorry, I couldn't generate a response. Please try again."
