from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..models.study_plan import StudyPlanCreateRequest, StudyPlanResponse, PlanItem
from ..services.study_plan_service import StudyPlanService
from ..dependencies import get_study_plan_service

router = APIRouter(prefix="/study-plans", tags=["study_plans"])


@router.get("/", response_model=list[StudyPlanResponse])
async def list_study_plans(
    user_id: str,
    service: Annotated[StudyPlanService, Depends(get_study_plan_service)],
) -> list[StudyPlanResponse]:
    return await service.list_plans(user_id)


@router.post("/", response_model=StudyPlanResponse, status_code=201)
async def create_study_plan(
    payload: StudyPlanCreateRequest,
    service: Annotated[StudyPlanService, Depends(get_study_plan_service)],
) -> StudyPlanResponse:
    return await service.create_plan(payload)


@router.get("/schedule", response_model=list[PlanItem])
async def get_daily_schedule(
    user_id: str,
    target_date: date = Query(default_factory=date.today),
    service: Annotated[StudyPlanService, Depends(get_study_plan_service)],
) -> list[PlanItem]:
    return await service.get_daily_schedule(user_id=user_id, target_date=target_date)
