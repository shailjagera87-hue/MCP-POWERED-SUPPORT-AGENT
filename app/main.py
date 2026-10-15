
from fastapi import FastAPI, HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.graph import ask_support

app = FastAPI(title="Customer Support Agent")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Question cannot be empty or whitespace only.",
        )

    try:
        answer = await ask_support(question)
        return ChatResponse(answer=answer)
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="The support agent could not process your request.",
        )

