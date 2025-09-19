from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from ...application.interfaces.services import TicketService
from ...application.dtos.models import TicketCreateDTO, TicketUpdateDTO
from ..schemas.api_models import (
    TicketCreateRequest, TicketUpdateRequest, TicketResponse, ErrorResponse
)
import structlog

logger = structlog.get_logger()

router = APIRouter(prefix="/tickets", tags=["tickets"])


def get_ticket_service() -> TicketService:
    """Dependency to get ticket service."""
    # This will be implemented in the main app with proper DI
    pass


@router.post("/", response_model=TicketResponse, status_code=201)
async def create_ticket(
    request: TicketCreateRequest,
    service: TicketService = Depends(get_ticket_service)
):
    """Create a new ticket."""
    try:
        dto = TicketCreateDTO(
            user_id=request.user_id,
            subject=request.subject,
            description=request.description,
            priority=request.priority,
            category=request.category,
            tags=request.tags
        )
        result = await service.create_ticket(dto)
        return TicketResponse(**result.dict())
    except Exception as e:
        logger.error("Failed to create ticket", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create ticket")


@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(
    ticket_id: str,
    service: TicketService = Depends(get_ticket_service)
):
    """Get a ticket by ID."""
    try:
        result = await service.get_ticket(ticket_id)
        return TicketResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to get ticket", error=str(e), ticket_id=ticket_id)
        raise HTTPException(status_code=500, detail="Failed to get ticket")


@router.get("/", response_model=List[TicketResponse])
async def get_tickets(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = Query(None),
    service: TicketService = Depends(get_ticket_service)
):
    """Get all tickets with pagination."""
    try:
        results = await service.get_tickets(skip, limit, status)
        return [TicketResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get tickets", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to get tickets")


@router.get("/user/{user_id}", response_model=List[TicketResponse])
async def get_user_tickets(
    user_id: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    service: TicketService = Depends(get_ticket_service)
):
    """Get tickets by user ID."""
    try:
        results = await service.get_user_tickets(user_id, skip, limit)
        return [TicketResponse(**result.dict()) for result in results]
    except Exception as e:
        logger.error("Failed to get user tickets", error=str(e), user_id=user_id)
        raise HTTPException(status_code=500, detail="Failed to get user tickets")


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: str,
    request: TicketUpdateRequest,
    service: TicketService = Depends(get_ticket_service)
):
    """Update a ticket."""
    try:
        dto = TicketUpdateDTO(
            subject=request.subject,
            description=request.description,
            status=request.status,
            priority=request.priority,
            category=request.category,
            tags=request.tags
        )
        result = await service.update_ticket(ticket_id, dto)
        return TicketResponse(**result.dict())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error("Failed to update ticket", error=str(e), ticket_id=ticket_id)
        raise HTTPException(status_code=500, detail="Failed to update ticket")


@router.delete("/{ticket_id}", status_code=204)
async def delete_ticket(
    ticket_id: str,
    service: TicketService = Depends(get_ticket_service)
):
    """Delete a ticket."""
    try:
        success = await service.delete_ticket(ticket_id)
        if not success:
            raise HTTPException(status_code=404, detail="Ticket not found")
    except Exception as e:
        logger.error("Failed to delete ticket", error=str(e), ticket_id=ticket_id)
        raise HTTPException(status_code=500, detail="Failed to delete ticket")