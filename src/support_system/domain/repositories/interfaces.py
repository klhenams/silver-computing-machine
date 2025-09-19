from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from ..entities.models import Document, Ticket, FAQ, Query


class DocumentRepository(ABC):
    """Abstract repository for document operations."""

    @abstractmethod
    async def create(self, document: Document) -> Document:
        """Create a new document."""
        pass

    @abstractmethod
    async def get_by_id(self, document_id: str) -> Optional[Document]:
        """Get document by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Document]:
        """Get all documents with pagination and optional category filter."""
        pass

    @abstractmethod
    async def update(self, document: Document) -> Document:
        """Update an existing document."""
        pass

    @abstractmethod
    async def delete(self, document_id: str) -> bool:
        """Delete a document."""
        pass

    @abstractmethod
    async def search_by_embedding(self, embedding: List[float], limit: int = 10) -> List[Document]:
        """Search documents by embedding similarity."""
        pass

    @abstractmethod
    async def search_by_text(self, query: str, limit: int = 10) -> List[Document]:
        """Search documents by text."""
        pass


class TicketRepository(ABC):
    """Abstract repository for ticket operations."""

    @abstractmethod
    async def create(self, ticket: Ticket) -> Ticket:
        """Create a new ticket."""
        pass

    @abstractmethod
    async def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Get ticket by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Ticket]:
        """Get all tickets with pagination and optional status filter."""
        pass

    @abstractmethod
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Ticket]:
        """Get tickets by user ID."""
        pass

    @abstractmethod
    async def update(self, ticket: Ticket) -> Ticket:
        """Update an existing ticket."""
        pass

    @abstractmethod
    async def delete(self, ticket_id: str) -> bool:
        """Delete a ticket."""
        pass

    @abstractmethod
    async def search_by_embedding(self, embedding: List[float], limit: int = 10) -> List[Ticket]:
        """Search tickets by embedding similarity."""
        pass


class FAQRepository(ABC):
    """Abstract repository for FAQ operations."""

    @abstractmethod
    async def create(self, faq: FAQ) -> FAQ:
        """Create a new FAQ."""
        pass

    @abstractmethod
    async def get_by_id(self, faq_id: str) -> Optional[FAQ]:
        """Get FAQ by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[FAQ]:
        """Get all FAQs with pagination and optional category filter."""
        pass

    @abstractmethod
    async def update(self, faq: FAQ) -> FAQ:
        """Update an existing FAQ."""
        pass

    @abstractmethod
    async def delete(self, faq_id: str) -> bool:
        """Delete a FAQ."""
        pass

    @abstractmethod
    async def search_by_embedding(self, embedding: List[float], limit: int = 10) -> List[FAQ]:
        """Search FAQs by embedding similarity."""
        pass

    @abstractmethod
    async def search_by_text(self, query: str, limit: int = 10) -> List[FAQ]:
        """Search FAQs by text."""
        pass

    @abstractmethod
    async def get_popular(self, limit: int = 10) -> List[FAQ]:
        """Get most popular FAQs by view count."""
        pass


class QueryRepository(ABC):
    """Abstract repository for query operations."""

    @abstractmethod
    async def create(self, query: Query) -> Query:
        """Create a new query."""
        pass

    @abstractmethod
    async def get_by_id(self, query_id: str) -> Optional[Query]:
        """Get query by ID."""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Query]:
        """Get all queries with pagination."""
        pass

    @abstractmethod
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Query]:
        """Get queries by user ID."""
        pass

    @abstractmethod
    async def update(self, query: Query) -> Query:
        """Update an existing query."""
        pass

    @abstractmethod
    async def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get query analytics for the specified number of days."""
        pass