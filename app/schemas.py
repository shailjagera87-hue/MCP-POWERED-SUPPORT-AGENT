
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Customer's support question",
    )


class ChatResponse(BaseModel):
    answer: str
    success: bool = True
