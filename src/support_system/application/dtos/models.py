from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentCreateDTO(BaseModel):
    """DTO for creating a document."""
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)


class DocumentUpdateDTO(BaseModel):
    """DTO for updating a document."""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = None


class DocumentResponseDTO(BaseModel):
    """DTO for document response."""
    id: str
    title: str
    content: str
    category: str
    tags: List[str]
    created_at: datetime
    updated_at: datetime
    is_active: bool


class TicketCreateDTO(BaseModel):
    """DTO for creating a ticket."""
    user_id: str = Field(..., min_length=1)
    subject: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1)
    priority: str = Field(default="medium", pattern="^(low|medium|high|urgent)$")
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)


class TicketUpdateDTO(BaseModel):
    """DTO for updating a ticket."""
    subject: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1)
    status: Optional[str] = Field(None, pattern="^(open|in_progress|resolved|closed)$")
    priority: Optional[str] = Field(None, pattern="^(low|medium|high|urgent)$")
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = None


class TicketResponseDTO(BaseModel):
    """DTO for ticket response."""
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


class FAQCreateDTO(BaseModel):
    """DTO for creating a FAQ."""
    question: str = Field(..., min_length=1, max_length=500)
    answer: str = Field(..., min_length=1)
    category: str = Field(..., min_length=1, max_length=50)
    tags: List[str] = Field(default_factory=list)


class FAQUpdateDTO(BaseModel):
    """DTO for updating a FAQ."""
    question: Optional[str] = Field(None, min_length=1, max_length=500)
    answer: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    tags: Optional[List[str]] = None


class FAQResponseDTO(BaseModel):
    """DTO for FAQ response."""
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


class QueryCreateDTO(BaseModel):
    """DTO for creating a query."""
    query_text: str = Field(..., min_length=1, max_length=1000)
    user_id: Optional[str] = None


class QueryResponseDTO(BaseModel):
    """DTO for query response."""
    id: str
    user_id: Optional[str]
    query_text: str
    response: Optional[str]
    sources: List[str]
    confidence_score: Optional[float]
    created_at: datetime


class QueryFeedbackDTO(BaseModel):
    """DTO for query feedback."""
    rating: int = Field(..., ge=1, le=5)


class SearchRequestDTO(BaseModel):
    """DTO for search requests."""
    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=10, ge=1, le=50)
    category: Optional[str] = None


class SearchResponseDTO(BaseModel):
    """DTO for search response."""
    query: str
    results: List[dict]
    total_results: int
    execution_time_ms: float