from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    id: str
    title: str
    summary: str | None = None
    knowledge_codes: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    storage_key: str
    metadata: dict[str, Any] = Field(default_factory=dict)


class DocumentIngestionRequest(BaseModel):
    source_uri: str
    knowledge_codes: list[str]
    tags: list[str] = Field(default_factory=list)
    priority: int = Field(default=5, ge=1, le=10)
