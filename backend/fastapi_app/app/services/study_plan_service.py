from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from ..models.study_plan import StudyPlanCreateRequest, StudyPlanResponse, PlanItem


class StudyPlanService:
    """Service orchestrating study plan CRUD and SRS scheduling."""

    def __init__(self) -> None:
        self._plans: dict[str, StudyPlanResponse] = {}

    async def create_plan(self, payload: StudyPlanCreateRequest) -> StudyPlanResponse:
        base_id = f"plan-{len(self._plans) + 1}"
        items = [
            PlanItem(
                id=f"{base_id}-item-{index}",
                knowledge_code=code,
                due_at=payload.start_date + timedelta(days=index),
                status="pending",
            )
            for index, code in enumerate(payload.knowledge_codes)
        ]
        plan = StudyPlanResponse(
            id=base_id,
            title=payload.title,
            description=payload.description,
            cadence=payload.cadence,
            items=items,
        )
        self._plans[base_id] = plan
        return plan

    async def list_plans(self, user_id: str) -> list[StudyPlanResponse]:
        _ = user_id
        return list(self._plans.values())

    async def get_daily_schedule(self, user_id: str, target_date: date) -> list[PlanItem]:
        _ = user_id
        result: list[PlanItem] = []
        for plan in self._plans.values():
            for item in plan.items:
                if item.due_at == target_date:
                    result.append(item)
        return result

    async def dispose(self) -> None:
        return None
