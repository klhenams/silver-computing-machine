from typing import Optional, List
from datetime import datetime, timezone
from dataclasses import dataclass, field
import uuid


@dataclass
class Document:
    """Domain entity representing a support document."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    title: str = ""
    content: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    def update_content(self, title: str, content: str, category: str, tags: List[str]) -> None:
        """Update document content and metadata."""
        self.title = title
        self.content = content
        self.category = category
        self.tags = tags
        self.updated_at = datetime.now(timezone.utc)
        self.embedding = None  # Reset embedding when content changes

    def set_embedding(self, embedding: List[float]) -> None:
        """Set the document embedding vector."""
        self.embedding = embedding


@dataclass
class Ticket:
    """Domain entity representing a support ticket."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    subject: str = ""
    description: str = ""
    status: str = "open"  # open, in_progress, resolved, closed
    priority: str = "medium"  # low, medium, high, urgent
    category: str = ""
    tags: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def update_status(self, status: str) -> None:
        """Update ticket status."""
        valid_statuses = ["open", "in_progress", "resolved", "closed"]
        if status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.status = status
        self.updated_at = datetime.now(timezone.utc)

    def update_priority(self, priority: str) -> None:
        """Update ticket priority."""
        valid_priorities = ["low", "medium", "high", "urgent"]
        if priority not in valid_priorities:
            raise ValueError(f"Invalid priority. Must be one of: {valid_priorities}")
        self.priority = priority
        self.updated_at = datetime.now(timezone.utc)

    def set_embedding(self, embedding: List[float]) -> None:
        """Set the ticket embedding vector."""
        self.embedding = embedding


@dataclass
class FAQ:
    """Domain entity representing a frequently asked question."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    question: str = ""
    answer: str = ""
    category: str = ""
    tags: List[str] = field(default_factory=list)
    embedding: Optional[List[float]] = None
    view_count: int = 0
    helpful_count: int = 0
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    def increment_views(self) -> None:
        """Increment the view count."""
        self.view_count += 1

    def increment_helpful(self) -> None:
        """Increment the helpful count."""
        self.helpful_count += 1

    def update_content(self, question: str, answer: str, category: str, tags: List[str]) -> None:
        """Update FAQ content."""
        self.question = question
        self.answer = answer
        self.category = category
        self.tags = tags
        self.updated_at = datetime.now(timezone.utc)
        self.embedding = None  # Reset embedding when content changes

    def set_embedding(self, embedding: List[float]) -> None:
        """Set the FAQ embedding vector."""
        self.embedding = embedding


@dataclass
class Query:
    """Domain entity representing a user query."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None
    query_text: str = ""
    embedding: Optional[List[float]] = None
    response: Optional[str] = None
    sources: List[str] = field(default_factory=list)
    confidence_score: Optional[float] = None
    feedback_rating: Optional[int] = None  # 1-5 rating
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def set_response(self, response: str, sources: List[str], confidence_score: float) -> None:
        """Set the query response and metadata."""
        self.response = response
        self.sources = sources
        self.confidence_score = confidence_score

    def set_feedback(self, rating: int) -> None:
        """Set user feedback rating."""
        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5")
        self.feedback_rating = rating

    def set_embedding(self, embedding: List[float]) -> None:
        """Set the query embedding vector."""
        self.embedding = embedding