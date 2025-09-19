from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ...application.interfaces.services import DocumentService
from ...application.dtos.models import DocumentCreateDTO, DocumentUpdateDTO, SearchRequestDTO
from ..schemas.api_models import (
    DocumentCreateRequest, DocumentUpdateRequest, DocumentResponse,
    SearchRequest, SearchResponse, ErrorResponse
)
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/documents", tags=["documents"])


def get_document_service() -> DocumentService:
    """Dependency to get document service."""
    # This will be implemented in the main app with proper DI
    pass


@router.post("/", response_model=DocumentResponse, status_code=201)
async def create_document(
    request: DocumentCreateRequest,
    service: DocumentService = Depends(get_document_service)
):
    """Create a new document."""
    try:
        dto = DocumentCreateDTO(
            title=request.title,
            content=request.content,
            category=request.category,
            tags=request.tags
        )
        result = await service.create_document(dto)
        return DocumentResponse(**result.dict())
    except Exception as e:
        logger.error("Failed to create document", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create document")


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service)
):
    """Get a document by ID."""
    try:
        result = await service.get_document(document_id)
        return DocumentResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to get document", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to get document")


@router.get("/", response_model=List[DocumentResponse])
async def get_documents(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    service: DocumentService = Depends(get_document_service)
):
    """Get all documents with pagination."""
    try:
        results = await service.get_documents(skip, limit, category)
        return [DocumentResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get documents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get documents")


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    request: DocumentUpdateRequest,
    service: DocumentService = Depends(get_document_service)
):
    """Update a document."""
    try:
        dto = DocumentUpdateDTO(
            title=request.title,
            content=request.content,
            category=request.category,
            tags=request.tags
        )
        result = await service.update_document(document_id, dto)
        return DocumentResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to update document", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to update document")


@router.delete("/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service)
):
    """Delete a document."""
    try:
        success = await service.delete_document(document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logger.error("Failed to delete document", error=str(e), document_id=document_id)
        raise HTTPException(status_code=500, detail="Failed to delete document")


@router.post("/search", response_model=SearchResponse)
async def search_documents(
    request: SearchRequest,
    service: DocumentService = Depends(get_document_service)
):
    """Search documents."""
    try:
        dto = SearchRequestDTO(
            query=request.query,
            limit=request.limit,
            category=request.category
        )
        result = await service.search_documents(dto)
        return SearchResponse(**result.dict())
    except Exception as e:
        logger.error("Failed to search documents", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search documents")