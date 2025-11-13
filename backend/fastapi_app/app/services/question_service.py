from __future__ import annotations

from typing import Any

from ..models.question import AdaptiveQuestionRequest, QuestionResponse, QuestionReviewRequest, Option


class QuestionService:
    """Facade over question retrieval, adaptive selection and evaluation."""

    def __init__(self) -> None:
        # Placeholder in-memory dataset for the MVP scaffold
        self._questions: list[dict[str, Any]] = [
            {
                "id": "q-1",
                "prompt": "What is the solution to 2x + 3 = 11?",
                "question_type": "single_choice",
                "options": [
                    {"label": "A", "value": "2"},
                    {"label": "B", "value": "3"},
                    {"label": "C", "value": "4"},
                    {"label": "D", "value": "5"},
                ],
                "solution": "Subtract 3 from both sides and divide by 2 to find x = 4.",
                "difficulty": 0.45,
                "knowledge_codes": ["ALG-001"],
            },
            {
                "id": "q-2",
                "prompt": "Newton's second law states that F = ma.",
                "question_type": "true_false",
                "options": None,
                "solution": "Force equals mass times acceleration.",
                "difficulty": 0.30,
                "knowledge_codes": ["PHY-101"],
            },
        ]

    async def list_questions(self, knowledge_code: str | None, limit: int) -> list[QuestionResponse]:
        filtered = (
            [q for q in self._questions if knowledge_code in q["knowledge_codes"]]
            if knowledge_code
            else self._questions
        )
        return [QuestionResponse(**self._normalize_question(q)) for q in filtered[:limit]]

    async def generate_adaptive_question(self, payload: AdaptiveQuestionRequest) -> QuestionResponse:
        # Simplified adaptive logic: cycle through questions filtered by knowledge code
        candidates = await self.list_questions(payload.knowledge_code, limit=len(self._questions))
        if not candidates:
            raise ValueError("No questions available for the requested knowledge code")
        index = hash(payload.user_id) % len(candidates)
        return candidates[index]

    async def submit_review(self, question_id: str, payload: QuestionReviewRequest) -> None:
        # Placeholder for persisting review feedback
        _ = (question_id, payload)

    async def dispose(self) -> None:
        """Release service resources such as db sessions."""
        return None

    def _normalize_question(self, question: dict[str, Any]) -> dict[str, Any]:
        options = question.get("options")
        if options:
            question["options"] = [Option(**opt) for opt in options]
        return question
