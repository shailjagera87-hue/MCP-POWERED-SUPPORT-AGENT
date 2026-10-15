
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from app.config import settings


def get_groq_model() -> ChatGroq:
    return ChatGroq(
        model=settings.groq_model,
        api_key=settings.groq_api_key,
        temperature=0,
    )


def test_groq_connection() -> None:
    model = get_groq_model()

    response = model.invoke([
        SystemMessage(
            content="You are a helpful customer support assistant."
        ),
        HumanMessage(
            content="Reply with exactly: Groq connection successful."
        ),
    ])

    print(response.content)


if __name__ == "__main__":
    test_groq_connection()
