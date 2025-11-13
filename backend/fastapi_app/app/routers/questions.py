from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..services.question_service import QuestionService
from ..models.question import AdaptiveQuestionRequest, QuestionResponse, QuestionReviewRequest
from ..dependencies import get_question_service

router = APIRouter(prefix="/questions", tags=["questions"])


@router.get("/", response_model=list[QuestionResponse])
async def list_questions(
    service: Annotated[QuestionService, Depends(get_question_service)],
    knowledge_code: str | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
) -> list[QuestionResponse]:
    """Fetch questions optionally filtered by a knowledge point code."""
    return await service.list_questions(knowledge_code=knowledge_code, limit=limit)


@router.post("/adaptive", response_model=QuestionResponse)
async def generate_adaptive_question(
    payload: AdaptiveQuestionRequest,
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> QuestionResponse:
    """Generate the next adaptive question for a learner."""
    return await service.generate_adaptive_question(payload)


@router.post("/{question_id}/review")
async def submit_question_review(
    question_id: str,
    payload: QuestionReviewRequest,
    service: Annotated[QuestionService, Depends(get_question_service)],
) -> dict[str, str]:
    await service.submit_review(question_id=question_id, payload=payload)
    return {"status": "received"}
