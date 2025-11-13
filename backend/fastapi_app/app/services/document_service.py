from __future__ import annotations

from ..models.document import DocumentResponse, DocumentIngestionRequest


class DocumentService:
    """Service facade around document catalog and ingestion orchestration."""

    def __init__(self) -> None:
        self._documents: dict[str, DocumentResponse] = {
            "doc-1": DocumentResponse(
                id="doc-1",
                title="Linear Equations Guide",
                summary="Step-by-step strategies to solve single variable equations.",
                knowledge_codes=["ALG-001"],
                tags=["algebra", "fundamentals"],
                storage_key="documents/algebra/linear-equations.pdf",
            )
        }

    async def list_documents(self, knowledge_code: str | None = None) -> list[DocumentResponse]:
        docs = list(self._documents.values())
        if knowledge_code:
            docs = [doc for doc in docs if knowledge_code in doc.knowledge_codes]
        return docs

    async def request_ingestion(self, payload: DocumentIngestionRequest) -> dict[str, str]:
        # Publish ingestion request to queue (stubbed)
        _ = payload
        return {"status": "queued"}

    async def dispose(self) -> None:
        return None
