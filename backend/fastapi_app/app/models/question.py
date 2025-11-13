from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class Option(BaseModel):
    label: str
    value: str


class AdaptiveQuestionRequest(BaseModel):
    user_id: str = Field(..., description="Learner requesting the question")
    knowledge_code: str | None = Field(None, description="Target knowledge focus")
    difficulty: float | None = Field(None, ge=0.0, le=1.0)


class QuestionResponse(BaseModel):
    id: str
    prompt: str
    question_type: str
    options: list[Option] | None = None
    solution: str | None = None
    difficulty: float | None = None
    knowledge_codes: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class QuestionReviewRequest(BaseModel):
    rating: int = Field(..., ge=1, le=5)
    feedback: str | None = None
    flag_issue: bool = False
