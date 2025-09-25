from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ...application.interfaces.services import FAQService
from ...application.dtos.models import FAQCreateDTO, FAQUpdateDTO, SearchRequestDTO
from ..schemas.api_models import (
    FAQCreateRequest, FAQUpdateRequest, FAQResponse,
    SearchRequest, SearchResponse, ErrorResponse
)
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/faqs", tags=["faqs"])


def get_faq_service() -> FAQService:
    """Dependency to get FAQ service."""
    # This will be overridden in main.py with proper DI
    raise HTTPException(status_code=500, detail="FAQ service not configured")


@router.post("/", response_model=FAQResponse, status_code=201)
async def create_faq(
    request: FAQCreateRequest,
    service: FAQService = Depends(get_faq_service)
):
    """Create a new FAQ."""
    try:
        dto = FAQCreateDTO(
            question=request.question,
            answer=request.answer,
            category=request.category,
            tags=request.tags
        )
        result = await service.create_faq(dto)
        return FAQResponse(**result.dict())
    except Exception as e:
        logger.error("Failed to create FAQ", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create FAQ")


@router.get("/{faq_id}", response_model=FAQResponse)
async def get_faq(
    faq_id: str,
    service: FAQService = Depends(get_faq_service)
):
    """Get a FAQ by ID."""
    try:
        result = await service.get_faq(faq_id)
        # Increment view count
        await service.increment_faq_views(faq_id)
        return FAQResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to get FAQ", error=str(e), faq_id=faq_id)
        raise HTTPException(status_code=500, detail="Failed to get FAQ")


@router.get("/", response_model=List[FAQResponse])
async def get_faqs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = Query(None),
    service: FAQService = Depends(get_faq_service)
):
    """Get all FAQs with pagination."""
    try:
        results = await service.get_faqs(skip, limit, category)
        return [FAQResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get FAQs", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get FAQs")


@router.get("/popular/", response_model=List[FAQResponse])
async def get_popular_faqs(
    limit: int = Query(10, ge=1, le=50),
    service: FAQService = Depends(get_faq_service)
):
    """Get popular FAQs."""
    try:
        results = await service.get_popular_faqs(limit)
        return [FAQResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get popular FAQs", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get popular FAQs")


@router.put("/{faq_id}", response_model=FAQResponse)
async def update_faq(
    faq_id: str,
    request: FAQUpdateRequest,
    service: FAQService = Depends(get_faq_service)
):
    """Update a FAQ."""
    try:
        dto = FAQUpdateDTO(
            question=request.question,
            answer=request.answer,
            category=request.category,
            tags=request.tags
        )
        result = await service.update_faq(faq_id, dto)
        return FAQResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to update FAQ", error=str(e), faq_id=faq_id)
        raise HTTPException(status_code=500, detail="Failed to update FAQ")


@router.delete("/{faq_id}", status_code=204)
async def delete_faq(
    faq_id: str,
    service: FAQService = Depends(get_faq_service)
):
    """Delete a FAQ."""
    try:
        success = await service.delete_faq(faq_id)
        if not success:
            raise HTTPException(status_code=404, detail="FAQ not found")
    except Exception as e:
        logger.error("Failed to delete FAQ", error=str(e), faq_id=faq_id)
        raise HTTPException(status_code=500, detail="Failed to delete FAQ")


@router.post("/search", response_model=SearchResponse)
async def search_faqs(
    request: SearchRequest,
    service: FAQService = Depends(get_faq_service)
):
    """Search FAQs."""
    try:
        dto = SearchRequestDTO(
            query=request.query,
            limit=request.limit,
            category=request.category
        )
        result = await service.search_faqs(dto)
        return SearchResponse(**result.dict())
    except Exception as e:
        logger.error("Failed to search FAQs", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to search FAQs")


@router.post("/{faq_id}/helpful", status_code=204)
async def mark_faq_helpful(
    faq_id: str,
    service: FAQService = Depends(get_faq_service)
):
    """Mark FAQ as helpful."""
    try:
        success = await service.increment_faq_helpful(faq_id)
        if not success:
            raise HTTPException(status_code=404, detail="FAQ not found")
    except Exception as e:
        logger.error("Failed to mark FAQ as helpful", error=str(e), faq_id=faq_id)
        raise HTTPException(status_code=500, detail="Failed to mark FAQ as helpful")