from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


# Request schemas
class DocumentCreateRequest(BaseModel):
    """Request schema for creating a document."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)


class DocumentUpdateRequest(BaseModel):
    """Request schema for updating a document."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = None


class TicketCreateRequest(BaseModel):
    """Request schema for creating a ticket."""
    user_id: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)


class TicketUpdateRequest(BaseModel):
    """Request schema for updating a ticket."""
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[str] = Field(None, pattern="^(open|in_progress|resolved|closed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = None


class FAQCreateRequest(BaseModel):
    """Request schema for creating a FAQ."""
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)


class FAQUpdateRequest(BaseModel):
    """Request schema for updating a FAQ."""
    question: Optional[str] = Field(None, min_length=1, max_length=500)
    answer: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = None


class QueryRequest(BaseModel):
    """Request schema for creating a query."""
    query_text: str = Field(..., min_length=1, max_length=1000)
    user_id: Optional[str] = None


class QueryFeedbackRequest(BaseModel):
    """Request schema for query feedback."""
    rating: int = Field(..., ge=1, le=5)


class SearchRequest(BaseModel):
    """Request schema for search."""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
    category: Optional[str] = None


# Response schemas
class DocumentResponse(BaseModel):
    """Response schema for document."""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool


class TicketResponse(BaseModel):
    """Response schema for ticket."""
    id: str
    user_id: str
    subject: str
    description: str
    status: str
    priority: str
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime


class FAQResponse(BaseModel):
    """Response schema for FAQ."""
    id: str
    question: str
    answer: str
    category: str
    tags: List[str]
    view_count: int
    helpful_count: int
    created_at: datetime
    updated_at: datetime
    is_active: bool


class QueryResponse(BaseModel):
    """Response schema for query."""
    id: str
    user_id: Optional[str]
    query_text: str
    response: Optional[str]
    sources: List[str]
    confidence_score: Optional[float]
    created_at: datetime


class SearchResponse(BaseModel):
    """Response schema for search."""
    query: str
    results: List[dict]
    total_results: int
    execution_time_ms: float


class AnalyticsResponse(BaseModel):
    """Response schema for analytics."""
    total_queries: int
    average_rating: float
    queries_with_feedback: int
    feedback_rate: float
    period_days: int


# Error schemas
class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    error_code: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    """Validation error response schema."""
    detail: str
    errors: List[dict]