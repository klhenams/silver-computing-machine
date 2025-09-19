from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..dtos.models import (
    DocumentCreateDTO, DocumentUpdateDTO, DocumentResponseDTO,
    TicketCreateDTO, TicketUpdateDTO, TicketResponseDTO,
    FAQCreateDTO, FAQUpdateDTO, FAQResponseDTO,
    QueryCreateDTO, QueryResponseDTO, QueryFeedbackDTO,
    SearchRequestDTO, SearchResponseDTO
)


class DocumentService(ABC):
    """Abstract service for document operations."""

    @abstractmethod
    async def create_document(self, dto: DocumentCreateDTO) -> DocumentResponseDTO:
        """Create a new document."""
        pass

    @abstractmethod
    async def get_document(self, document_id: str) -> DocumentResponseDTO:
        """Get document by ID."""
        pass

    @abstractmethod
    async def get_documents(self, skip: int = 0, limit: int = 100, category: str = None) -> List[DocumentResponseDTO]:
        """Get all documents with pagination."""
        pass

    @abstractmethod
    async def update_document(self, document_id: str, dto: DocumentUpdateDTO) -> DocumentResponseDTO:
        """Update an existing document."""
        pass

    @abstractmethod
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document."""
        pass

    @abstractmethod
    async def search_documents(self, request: SearchRequestDTO) -> SearchResponseDTO:
        """Search documents."""
        pass


class TicketService(ABC):
    """Abstract service for ticket operations."""

    @abstractmethod
    async def create_ticket(self, dto: TicketCreateDTO) -> TicketResponseDTO:
        """Create a new ticket."""
        pass

    @abstractmethod
    async def get_ticket(self, ticket_id: str) -> TicketResponseDTO:
        """Get ticket by ID."""
        pass

    @abstractmethod
    async def get_tickets(self, skip: int = 0, limit: int = 100, status: str = None) -> List[TicketResponseDTO]:
        """Get all tickets with pagination."""
        pass

    @abstractmethod
    async def get_user_tickets(self, user_id: str, skip: int = 0, limit: int = 100) -> List[TicketResponseDTO]:
        """Get tickets by user ID."""
        pass

    @abstractmethod
    async def update_ticket(self, ticket_id: str, dto: TicketUpdateDTO) -> TicketResponseDTO:
        """Update an existing ticket."""
        pass

    @abstractmethod
    async def delete_ticket(self, ticket_id: str) -> bool:
        """Delete a ticket."""
        pass


class FAQService(ABC):
    """Abstract service for FAQ operations."""

    @abstractmethod
    async def create_faq(self, dto: FAQCreateDTO) -> FAQResponseDTO:
        """Create a new FAQ."""
        pass

    @abstractmethod
    async def get_faq(self, faq_id: str) -> FAQResponseDTO:
        """Get FAQ by ID."""
        pass

    @abstractmethod
    async def get_faqs(self, skip: int = 0, limit: int = 100, category: str = None) -> List[FAQResponseDTO]:
        """Get all FAQs with pagination."""
        pass

    @abstractmethod
    async def update_faq(self, faq_id: str, dto: FAQUpdateDTO) -> FAQResponseDTO:
        """Update an existing FAQ."""
        pass

    @abstractmethod
    async def delete_faq(self, faq_id: str) -> bool:
        """Delete a FAQ."""
        pass

    @abstractmethod
    async def search_faqs(self, request: SearchRequestDTO) -> SearchResponseDTO:
        """Search FAQs."""
        pass

    @abstractmethod
    async def get_popular_faqs(self, limit: int = 10) -> List[FAQResponseDTO]:
        """Get popular FAQs."""
        pass

    @abstractmethod
    async def increment_faq_views(self, faq_id: str) -> bool:
        """Increment FAQ view count."""
        pass

    @abstractmethod
    async def increment_faq_helpful(self, faq_id: str) -> bool:
        """Increment FAQ helpful count."""
        pass


class QueryService(ABC):
    """Abstract service for query operations."""

    @abstractmethod
    async def process_query(self, dto: QueryCreateDTO) -> QueryResponseDTO:
        """Process a user query and generate response."""
        pass

    @abstractmethod
    async def get_query(self, query_id: str) -> QueryResponseDTO:
        """Get query by ID."""
        pass

    @abstractmethod
    async def get_queries(self, skip: int = 0, limit: int = 100) -> List[QueryResponseDTO]:
        """Get all queries with pagination."""
        pass

    @abstractmethod
    async def get_user_queries(self, user_id: str, skip: int = 0, limit: int = 100) -> List[QueryResponseDTO]:
        """Get queries by user ID."""
        pass

    @abstractmethod
    async def provide_feedback(self, query_id: str, feedback: QueryFeedbackDTO) -> bool:
        """Provide feedback for a query response."""
        pass

    @abstractmethod
    async def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get query analytics."""
        pass