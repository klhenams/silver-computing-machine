from typing import Generator
from sqlalchemy.orm import Session
from ..infrastructure.database.models import get_database_config
from ..infrastructure.external_services.huggingface import HuggingFaceEmbeddingService, HuggingFaceLLMService
from ..infrastructure.repositories.sql_repositories import (
    SQLDocumentRepository, SQLTicketRepository, SQLFAQRepository, SQLQueryRepository
)
from ..application.use_cases.services import (
    DocumentServiceImpl, TicketServiceImpl, FAQServiceImpl, QueryServiceImpl
)
from ..application.interfaces.services import DocumentService, TicketService, FAQService, QueryService
from ..domain.services.interfaces import EmbeddingService, LLMService
from ..domain.repositories.interfaces import DocumentRepository, TicketRepository, FAQRepository, QueryRepository


class Container:
    """Dependency injection container."""
    
    def __init__(self):
        self.db_config = get_database_config()
        self._embedding_service = None
        self._llm_service = None
    
    def get_database_session(self) -> Generator[Session, None, None]:
        """Get database session."""
        session = next(self.db_config.get_session())
        try:
            yield session
        finally:
            session.close()
    
    def get_embedding_service(self) -> EmbeddingService:
        """Get embedding service."""
        if self._embedding_service is None:
            self._embedding_service = HuggingFaceEmbeddingService()
        return self._embedding_service
    
    def get_llm_service(self) -> LLMService:
        """Get LLM service."""
        if self._llm_service is None:
            self._llm_service = HuggingFaceLLMService()
        return self._llm_service
    
    def get_document_repository(self, session: Session) -> DocumentRepository:
        """Get document repository."""
        return SQLDocumentRepository(session)
    
    def get_ticket_repository(self, session: Session) -> TicketRepository:
        """Get ticket repository."""
        return SQLTicketRepository(session)
    
    def get_faq_repository(self, session: Session) -> FAQRepository:
        """Get FAQ repository."""
        return SQLFAQRepository(session)
    
    def get_query_repository(self, session: Session) -> QueryRepository:
        """Get query repository."""
        return SQLQueryRepository(session)
    
    def get_document_service(self, session: Session) -> DocumentService:
        """Get document service."""
        document_repo = self.get_document_repository(session)
        embedding_service = self.get_embedding_service()
        return DocumentServiceImpl(document_repo, embedding_service)
    
    def get_ticket_service(self, session: Session) -> TicketService:
        """Get ticket service."""
        ticket_repo = self.get_ticket_repository(session)
        embedding_service = self.get_embedding_service()
        return TicketServiceImpl(ticket_repo, embedding_service)
    
    def get_faq_service(self, session: Session) -> FAQService:
        """Get FAQ service."""
        faq_repo = self.get_faq_repository(session)
        embedding_service = self.get_embedding_service()
        return FAQServiceImpl(faq_repo, embedding_service)
    
    def get_query_service(self, session: Session) -> QueryService:
        """Get query service."""
        query_repo = self.get_query_repository(session)
        document_repo = self.get_document_repository(session)
        faq_repo = self.get_faq_repository(session)
        ticket_repo = self.get_ticket_repository(session)
        embedding_service = self.get_embedding_service()
        llm_service = self.get_llm_service()
        
        return QueryServiceImpl(
            query_repo,
            document_repo,
            faq_repo,
            ticket_repo,
            embedding_service,
            llm_service
        )


# Global container instance
container = Container()