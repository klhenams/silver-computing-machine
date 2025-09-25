from typing import List, Dict, Any
import time
from ...domain.entities.models import Document, Ticket, FAQ, Query
from ...domain.repositories.interfaces import DocumentRepository, TicketRepository, FAQRepository, QueryRepository
from ...domain.services.interfaces import EmbeddingService, LLMService
from ..dtos.models import (
    DocumentCreateDTO, DocumentUpdateDTO, DocumentResponseDTO,
    TicketCreateDTO, TicketUpdateDTO, TicketResponseDTO,
    FAQCreateDTO, FAQUpdateDTO, FAQResponseDTO,
    QueryCreateDTO, QueryResponseDTO, QueryFeedbackDTO,
    SearchRequestDTO, SearchResponseDTO
)
from ..interfaces.services import DocumentService, TicketService, FAQService, QueryService
import structlog

logger = structlog.get_logger()


class DocumentServiceImpl(DocumentService):
    """Implementation of DocumentService."""
    
    def __init__(
        self,
        document_repo: DocumentRepository,
        embedding_service: EmbeddingService
    ):
        self.document_repo = document_repo
        self.embedding_service = embedding_service
    
    def _entity_to_dto(self, entity: Document) -> DocumentResponseDTO:
        """Convert entity to response DTO."""
        return DocumentResponseDTO(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            category=entity.category,
            tags=entity.tags,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active
        )
    
    async def create_document(self, dto: DocumentCreateDTO) -> DocumentResponseDTO:
        """Create a new document."""
        document = Document()
        document.update_content(dto.title, dto.content, dto.category, dto.tags)
        
        # Generate embedding
        text_for_embedding = f"{dto.title} {dto.content}"
        embedding = await self.embedding_service.generate_embedding(text_for_embedding)
        document.set_embedding(embedding)
        
        created_document = await self.document_repo.create(document)
        return self._entity_to_dto(created_document)
    
    async def get_document(self, document_id: str) -> DocumentResponseDTO:
        """Get document by ID."""
        document = await self.document_repo.get_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found")
        return self._entity_to_dto(document)
    
    async def get_documents(
        self, skip: int = 0, limit: int = 100, category: str = None
    ) -> List[DocumentResponseDTO]:
        """Get all documents with pagination."""
        documents = await self.document_repo.get_all(skip, limit, category)
        return [self._entity_to_dto(doc) for doc in documents]
    
    async def update_document(
        self, document_id: str, dto: DocumentUpdateDTO
    ) -> DocumentResponseDTO:
        """Update an existing document."""
        document = await self.document_repo.get_by_id(document_id)
        if not document:
            raise ValueError(f"Document with id {document_id} not found")
        
        # Update only provided fields
        if dto.title is not None:
            document.title = dto.title
        if dto.content is not None:
            document.content = dto.content
        if dto.category is not None:
            document.category = dto.category
        if dto.tags is not None:
            document.tags = dto.tags
        
        # Regenerate embedding if content changed
        if dto.title is not None or dto.content is not None:
            text_for_embedding = f"{document.title} {document.content}"
            embedding = await self.embedding_service.generate_embedding(text_for_embedding)
            document.set_embedding(embedding)
        
        updated_document = await self.document_repo.update(document)
        return self._entity_to_dto(updated_document)
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete a document."""
        return await self.document_repo.delete(document_id)
    
    async def search_documents(self, request: SearchRequestDTO) -> SearchResponseDTO:
        """Search documents."""
        start_time = time.time()
        
        # Generate embedding for the query
        query_embedding = await self.embedding_service.generate_embedding(request.query)
        
        # Search by embedding similarity
        similar_docs = await self.document_repo.search_by_embedding(
            query_embedding, request.limit
        )
        
        # Also search by text as fallback
        text_docs = await self.document_repo.search_by_text(request.query, request.limit)
        
        # Combine and deduplicate results
        all_docs = {doc.id: doc for doc in similar_docs + text_docs}
        
        # Filter by category if specified
        if request.category:
            all_docs = {
                doc_id: doc for doc_id, doc in all_docs.items() 
                if doc.category == request.category
            }
        
        results = [
            {
                "id": doc.id,
                "title": doc.title,
                "content": doc.content[:200] + "..." if len(doc.content) > 200 else doc.content,
                "category": doc.category,
                "tags": doc.tags
            }
            for doc in list(all_docs.values())[:request.limit]
        ]
        
        execution_time = (time.time() - start_time) * 1000
        
        return SearchResponseDTO(
            query=request.query,
            results=results,
            total_results=len(results),
            execution_time_ms=execution_time
        )


class TicketServiceImpl(TicketService):
    """Implementation of TicketService."""
    
    def __init__(
        self,
        ticket_repo: TicketRepository,
        embedding_service: EmbeddingService
    ):
        self.ticket_repo = ticket_repo
        self.embedding_service = embedding_service
    
    def _entity_to_dto(self, entity: Ticket) -> TicketResponseDTO:
        """Convert entity to response DTO."""
        return TicketResponseDTO(
            id=entity.id,
            user_id=entity.user_id,
            subject=entity.subject,
            description=entity.description,
            status=entity.status,
            priority=entity.priority,
            category=entity.category,
            tags=entity.tags,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    async def create_ticket(self, dto: TicketCreateDTO) -> TicketResponseDTO:
        """Create a new ticket."""
        ticket = Ticket(
            user_id=dto.user_id,
            subject=dto.subject,
            description=dto.description,
            priority=dto.priority,
            category=dto.category,
            tags=dto.tags
        )
        
        # Generate embedding
        text_for_embedding = f"{dto.subject} {dto.description}"
        embedding = await self.embedding_service.generate_embedding(text_for_embedding)
        ticket.set_embedding(embedding)
        
        created_ticket = await self.ticket_repo.create(ticket)
        return self._entity_to_dto(created_ticket)
    
    async def get_ticket(self, ticket_id: str) -> TicketResponseDTO:
        """Get ticket by ID."""
        ticket = await self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket with id {ticket_id} not found")
        return self._entity_to_dto(ticket)
    
    async def get_tickets(
        self, skip: int = 0, limit: int = 100, status: str = None
    ) -> List[TicketResponseDTO]:
        """Get all tickets with pagination."""
        tickets = await self.ticket_repo.get_all(skip, limit, status)
        return [self._entity_to_dto(ticket) for ticket in tickets]
    
    async def get_user_tickets(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[TicketResponseDTO]:
        """Get tickets by user ID."""
        tickets = await self.ticket_repo.get_by_user(user_id, skip, limit)
        return [self._entity_to_dto(ticket) for ticket in tickets]
    
    async def update_ticket(
        self, ticket_id: str, dto: TicketUpdateDTO
    ) -> TicketResponseDTO:
        """Update an existing ticket."""
        ticket = await self.ticket_repo.get_by_id(ticket_id)
        if not ticket:
            raise ValueError(f"Ticket with id {ticket_id} not found")
        
        # Update only provided fields
        if dto.subject is not None:
            ticket.subject = dto.subject
        if dto.description is not None:
            ticket.description = dto.description
        if dto.status is not None:
            ticket.update_status(dto.status)
        if dto.priority is not None:
            ticket.update_priority(dto.priority)
        if dto.category is not None:
            ticket.category = dto.category
        if dto.tags is not None:
            ticket.tags = dto.tags
        
        # Regenerate embedding if content changed
        if dto.subject is not None or dto.description is not None:
            text_for_embedding = f"{ticket.subject} {ticket.description}"
            embedding = await self.embedding_service.generate_embedding(text_for_embedding)
            ticket.set_embedding(embedding)
        
        updated_ticket = await self.ticket_repo.update(ticket)
        return self._entity_to_dto(updated_ticket)
    
    async def delete_ticket(self, ticket_id: str) -> bool:
        """Delete a ticket."""
        return await self.ticket_repo.delete(ticket_id)


class FAQServiceImpl(FAQService):
    """Implementation of FAQService."""
    
    def __init__(
        self,
        faq_repo: FAQRepository,
        embedding_service: EmbeddingService
    ):
        self.faq_repo = faq_repo
        self.embedding_service = embedding_service
    
    def _entity_to_dto(self, entity: FAQ) -> FAQResponseDTO:
        """Convert entity to response DTO."""
        return FAQResponseDTO(
            id=entity.id,
            question=entity.question,
            answer=entity.answer,
            category=entity.category,
            tags=entity.tags,
            view_count=entity.view_count,
            helpful_count=entity.helpful_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active
        )
    
    async def create_faq(self, dto: FAQCreateDTO) -> FAQResponseDTO:
        """Create a new FAQ."""
        faq = FAQ()
        faq.update_content(dto.question, dto.answer, dto.category, dto.tags)
        
        # Generate embedding
        text_for_embedding = f"{dto.question} {dto.answer}"
        embedding = await self.embedding_service.generate_embedding(text_for_embedding)
        faq.set_embedding(embedding)
        
        created_faq = await self.faq_repo.create(faq)
        return self._entity_to_dto(created_faq)
    
    async def get_faq(self, faq_id: str) -> FAQResponseDTO:
        """Get FAQ by ID."""
        faq = await self.faq_repo.get_by_id(faq_id)
        if not faq:
            raise ValueError(f"FAQ with id {faq_id} not found")
        return self._entity_to_dto(faq)
    
    async def get_faqs(
        self, skip: int = 0, limit: int = 100, category: str = None
    ) -> List[FAQResponseDTO]:
        """Get all FAQs with pagination."""
        faqs = await self.faq_repo.get_all(skip, limit, category)
        return [self._entity_to_dto(faq) for faq in faqs]
    
    async def update_faq(self, faq_id: str, dto: FAQUpdateDTO) -> FAQResponseDTO:
        """Update an existing FAQ."""
        faq = await self.faq_repo.get_by_id(faq_id)
        if not faq:
            raise ValueError(f"FAQ with id {faq_id} not found")
        
        # Update only provided fields
        if dto.question is not None:
            faq.question = dto.question
        if dto.answer is not None:
            faq.answer = dto.answer
        if dto.category is not None:
            faq.category = dto.category
        if dto.tags is not None:
            faq.tags = dto.tags
        
        # Regenerate embedding if content changed
        if dto.question is not None or dto.answer is not None:
            text_for_embedding = f"{faq.question} {faq.answer}"
            embedding = await self.embedding_service.generate_embedding(text_for_embedding)
            faq.set_embedding(embedding)
        
        updated_faq = await self.faq_repo.update(faq)
        return self._entity_to_dto(updated_faq)
    
    async def delete_faq(self, faq_id: str) -> bool:
        """Delete a FAQ."""
        return await self.faq_repo.delete(faq_id)
    
    async def search_faqs(self, request: SearchRequestDTO) -> SearchResponseDTO:
        """Search FAQs."""
        start_time = time.time()
        
        # Generate embedding for the query
        query_embedding = await self.embedding_service.generate_embedding(request.query)
        
        # Search by embedding similarity
        similar_faqs = await self.faq_repo.search_by_embedding(
            query_embedding, request.limit * 2  # Get more results for filtering
        )
        
        # Also search by text as fallback
        text_faqs = await self.faq_repo.search_by_text(request.query, request.limit * 2)
        
        # Combine and deduplicate results
        all_faqs = {faq.id: faq for faq in similar_faqs + text_faqs}
        
        # Filter by category if specified, but only if we have relevant results
        if request.category and all_faqs:
            all_faqs = {
                faq_id: faq for faq_id, faq in all_faqs.items() 
                if faq.category == request.category
            }
        
        # If no relevant results found and category is specified, don't return random FAQs
        if not all_faqs and request.category:
            all_faqs = {}
        
        results = [
            {
                "id": faq.id,
                "question": faq.question,
                "answer": faq.answer[:200] + "..." if len(faq.answer) > 200 else faq.answer,
                "category": faq.category,
                "tags": faq.tags,
                "view_count": faq.view_count,
                "helpful_count": faq.helpful_count
            }
            for faq in list(all_faqs.values())[:request.limit]
        ]
        
        execution_time = (time.time() - start_time) * 1000
        
        return SearchResponseDTO(
            query=request.query,
            results=results,
            total_results=len(results),
            execution_time_ms=execution_time
        )
    
    async def get_popular_faqs(self, limit: int = 10) -> List[FAQResponseDTO]:
        """Get popular FAQs."""
        faqs = await self.faq_repo.get_popular(limit)
        return [self._entity_to_dto(faq) for faq in faqs]
    
    async def increment_faq_views(self, faq_id: str) -> bool:
        """Increment FAQ view count."""
        faq = await self.faq_repo.get_by_id(faq_id)
        if not faq:
            return False
        
        faq.increment_views()
        await self.faq_repo.update(faq)
        return True
    
    async def increment_faq_helpful(self, faq_id: str) -> bool:
        """Increment FAQ helpful count."""
        faq = await self.faq_repo.get_by_id(faq_id)
        if not faq:
            return False
        
        faq.increment_helpful()
        await self.faq_repo.update(faq)
        return True


class QueryServiceImpl(QueryService):
    """Implementation of QueryService."""
    
    def __init__(
        self,
        query_repo: QueryRepository,
        document_repo: DocumentRepository,
        faq_repo: FAQRepository,
        ticket_repo: TicketRepository,
        embedding_service: EmbeddingService,
        llm_service: LLMService
    ):
        self.query_repo = query_repo
        self.document_repo = document_repo
        self.faq_repo = faq_repo
        self.ticket_repo = ticket_repo
        self.embedding_service = embedding_service
        self.llm_service = llm_service
    
    def _entity_to_dto(self, entity: Query) -> QueryResponseDTO:
        """Convert entity to response DTO."""
        return QueryResponseDTO(
            id=entity.id,
            user_id=entity.user_id,
            query_text=entity.query_text,
            response=entity.response,
            sources=entity.sources,
            confidence_score=entity.confidence_score,
            created_at=entity.created_at
        )
    
    async def process_query(self, dto: QueryCreateDTO) -> QueryResponseDTO:
        """Process a user query and generate response."""
        query = Query(
            user_id=dto.user_id,
            query_text=dto.query_text
        )
        
        # Generate embedding for the query
        query_embedding = await self.embedding_service.generate_embedding(dto.query_text)
        query.set_embedding(query_embedding)
        
        # Search for relevant content
        documents = await self.document_repo.search_by_embedding(query_embedding, 3)
        faqs = await self.faq_repo.search_by_embedding(query_embedding, 3)
        tickets = await self.ticket_repo.search_by_embedding(query_embedding, 2)
        
        # Prepare context for LLM
        context = []
        sources = []
        
        for doc in documents:
            context.append(f"Document: {doc.title}\n{doc.content}")
            sources.append(f"doc:{doc.id}")
        
        for faq in faqs:
            context.append(f"FAQ: {faq.question}\nAnswer: {faq.answer}")
            sources.append(f"faq:{faq.id}")
        
        for ticket in tickets:
            context.append(f"Ticket: {ticket.subject}\n{ticket.description}")
            sources.append(f"ticket:{ticket.id}")
        
        # Generate response using LLM
        if context:
            response = await self.llm_service.generate_response(
                dto.query_text, context
            )
            confidence_score = 0.8  # You could implement actual confidence scoring
        else:
            response = "I couldn't find relevant information to answer your question. Please try rephrasing or contact support directly."
            confidence_score = 0.1
        
        query.set_response(response, sources, confidence_score)
        
        # Save query to database
        created_query = await self.query_repo.create(query)
        return self._entity_to_dto(created_query)
    
    async def get_query(self, query_id: str) -> QueryResponseDTO:
        """Get query by ID."""
        query = await self.query_repo.get_by_id(query_id)
        if not query:
            raise ValueError(f"Query with id {query_id} not found")
        return self._entity_to_dto(query)
    
    async def get_queries(self, skip: int = 0, limit: int = 100) -> List[QueryResponseDTO]:
        """Get all queries with pagination."""
        queries = await self.query_repo.get_all(skip, limit)
        return [self._entity_to_dto(query) for query in queries]
    
    async def get_user_queries(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[QueryResponseDTO]:
        """Get queries by user ID."""
        queries = await self.query_repo.get_by_user(user_id, skip, limit)
        return [self._entity_to_dto(query) for query in queries]
    
    async def provide_feedback(self, query_id: str, feedback: QueryFeedbackDTO) -> bool:
        """Provide feedback for a query response."""
        query = await self.query_repo.get_by_id(query_id)
        if not query:
            return False
        
        query.set_feedback(feedback.rating)
        await self.query_repo.update(query)
        return True
    
    async def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get query analytics."""
        return await self.query_repo.get_analytics(days)