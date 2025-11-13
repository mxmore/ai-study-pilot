from __future__ import annotations

from datetime import date
from typing import Any

from pydantic import BaseModel, Field


class PlanItem(BaseModel):
    id: str
    knowledge_code: str
    due_at: date
    status: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class StudyPlanResponse(BaseModel):
    id: str
    title: str
    description: str | None
    cadence: str
    items: list[PlanItem]


class StudyPlanCreateRequest(BaseModel):
    user_id: str
    title: str
    description: str | None = None
    start_date: date
    cadence: str = "daily"
    knowledge_codes: list[str] = Field(default_factory=list)
