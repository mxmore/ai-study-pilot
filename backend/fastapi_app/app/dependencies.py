from collections.abc import AsyncGenerator

from .services.question_service import QuestionService
from .services.study_plan_service import StudyPlanService
from .services.document_service import DocumentService


async def get_question_service() -> AsyncGenerator[QuestionService, None]:
    service = QuestionService()
    try:
        yield service
    finally:
        await service.dispose()


async def get_study_plan_service() -> AsyncGenerator[StudyPlanService, None]:
    service = StudyPlanService()
    try:
        yield service
    finally:
        await service.dispose()


async def get_document_service() -> AsyncGenerator[DocumentService, None]:
    service = DocumentService()
    try:
        yield service
    finally:
        await service.dispose()
