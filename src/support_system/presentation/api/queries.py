from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from ...application.interfaces.services import QueryService
from ...application.dtos.models import QueryCreateDTO, QueryFeedbackDTO
from ..schemas.api_models import (
    QueryRequest, QueryResponse, QueryFeedbackRequest, AnalyticsResponse, ErrorResponse
)
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/queries", tags=["queries"])


def get_query_service() -> QueryService:
    """Dependency to get query service."""
    # This will be implemented in the main app with proper DI
    pass


@router.post("/", response_model=QueryResponse, status_code=201)
async def process_query(
    request: QueryRequest,
    service: QueryService = Depends(get_query_service)
):
    """Process a user query and generate response."""
    try:
        dto = QueryCreateDTO(
            query_text=request.query_text,
            user_id=request.user_id
        )
        result = await service.process_query(dto)
        return QueryResponse(**result.dict())
    except Exception as e:
        logger.error("Failed to process query", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to process query")


@router.get("/{query_id}", response_model=QueryResponse)
async def get_query(
    query_id: str,
    service: QueryService = Depends(get_query_service)
):
    """Get a query by ID."""
    try:
        result = await service.get_query(query_id)
        return QueryResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to get query", error=str(e), query_id=query_id)
        raise HTTPException(status_code=500, detail="Failed to get query")


@router.get("/", response_model=List[QueryResponse])
async def get_queries(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: QueryService = Depends(get_query_service)
):
    """Get all queries with pagination."""
    try:
        results = await service.get_queries(skip, limit)
        return [QueryResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get queries", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get queries")


@router.get("/user/{user_id}", response_model=List[QueryResponse])
async def get_user_queries(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: QueryService = Depends(get_query_service)
):
    """Get queries by user ID."""
    try:
        results = await service.get_user_queries(user_id, skip, limit)
        return [QueryResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get user queries", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail="Failed to get user queries")


@router.post("/{query_id}/feedback", status_code=204)
async def provide_feedback(
    query_id: str,
    request: QueryFeedbackRequest,
    service: QueryService = Depends(get_query_service)
):
    """Provide feedback for a query response."""
    try:
        dto = QueryFeedbackDTO(rating=request.rating)
        success = await service.provide_feedback(query_id, dto)
        if not success:
            raise HTTPException(status_code=404, detail="Query not found")
    except Exception as e:
        logger.error("Failed to provide feedback", error=str(e), query_id=query_id)
        raise HTTPException(status_code=500, detail="Failed to provide feedback")


@router.get("/analytics/", response_model=AnalyticsResponse)
async def get_analytics(
    days: int = Query(30, ge=1, le=365),
    service: QueryService = Depends(get_query_service)
):
    """Get query analytics."""
    try:
        result = await service.get_analytics(days)
        return AnalyticsResponse(**result)
    except Exception as e:
        logger.error("Failed to get analytics", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get analytics")