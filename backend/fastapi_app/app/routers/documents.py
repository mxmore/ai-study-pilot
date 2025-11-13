from typing import Annotated

from fastapi import APIRouter, Depends, Query

from ..models.document import DocumentResponse, DocumentIngestionRequest
from ..services.document_service import DocumentService
from ..dependencies import get_document_service

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("/", response_model=list[DocumentResponse])
async def list_documents(
    knowledge_code: str | None = Query(None),
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> list[DocumentResponse]:
    return await service.list_documents(knowledge_code=knowledge_code)


@router.post("/ingest")
async def queue_document_ingestion(
    payload: DocumentIngestionRequest,
    service: Annotated[DocumentService, Depends(get_document_service)],
) -> dict[str, str]:
    return await service.request_ingestion(payload)
