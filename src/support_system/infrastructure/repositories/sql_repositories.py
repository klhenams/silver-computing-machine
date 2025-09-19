from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from pgvector.sqlalchemy import Vector
from ..database.models import DocumentModel, TicketModel, FAQModel, QueryModel
from ...domain.entities.models import Document, Ticket, FAQ, Query
from ...domain.repositories.interfaces import (
    DocumentRepository, TicketRepository, FAQRepository, QueryRepository
)
import structlog

logger = structlog.get_logger()


class SQLDocumentRepository(DocumentRepository):
    """SQLAlchemy implementation of DocumentRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, model: DocumentModel) -> Document:
        """Convert database model to domain entity."""
        return Document(
            id=model.id,
            title=model.title,
            content=model.content,
            category=model.category,
            tags=model.tags or [],
            embedding=list(model.embedding) if model.embedding else None,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active
        )
    
    def _entity_to_model(self, entity: Document) -> DocumentModel:
        """Convert domain entity to database model."""
        return DocumentModel(
            id=entity.id,
            title=entity.title,
            content=entity.content,
            category=entity.category,
            tags=entity.tags,
            embedding=entity.embedding,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active
        )
    
    async def create(self, document: Document) -> Document:
        """Create a new document."""
        try:
            model = self._entity_to_model(document)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to create document", error=str(e))
            raise
    
    async def get_by_id(self, document_id: str) -> Optional[Document]:
        """Get document by ID."""
        model = self.session.query(DocumentModel).filter(
            DocumentModel.id == document_id,
            DocumentModel.is_active == True
        ).first()
        return self._model_to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[Document]:
        """Get all documents with pagination and optional category filter."""
        query = self.session.query(DocumentModel).filter(DocumentModel.is_active == True)
        
        if category:
            query = query.filter(DocumentModel.category == category)
        
        models = query.offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, document: Document) -> Document:
        """Update an existing document."""
        try:
            model = self.session.query(DocumentModel).filter(
                DocumentModel.id == document.id
            ).first()
            
            if not model:
                raise ValueError(f"Document with id {document.id} not found")
            
            model.title = document.title
            model.content = document.content
            model.category = document.category
            model.tags = document.tags
            model.embedding = document.embedding
            model.updated_at = document.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to update document", error=str(e), document_id=document.id)
            raise
    
    async def delete(self, document_id: str) -> bool:
        """Delete a document."""
        try:
            model = self.session.query(DocumentModel).filter(
                DocumentModel.id == document_id
            ).first()
            
            if not model:
                return False
            
            model.is_active = False
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to delete document", error=str(e), document_id=document_id)
            raise
    
    async def search_by_embedding(self, embedding: List[float], limit: int = 10) -> List[Document]:
        """Search documents by embedding similarity."""
        try:
            models = self.session.query(DocumentModel).filter(
                DocumentModel.is_active == True,
                DocumentModel.embedding.is_not(None)
            ).order_by(
                DocumentModel.embedding.cosine_distance(embedding)
            ).limit(limit).all()
            
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            logger.error("Failed to search documents by embedding", error=str(e))
            return []
    
    async def search_by_text(self, query: str, limit: int = 10) -> List[Document]:
        """Search documents by text."""
        try:
            models = self.session.query(DocumentModel).filter(
                DocumentModel.is_active == True,
                func.concat(DocumentModel.title, ' ', DocumentModel.content).ilike(f'%{query}%')
            ).limit(limit).all()
            
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            logger.error("Failed to search documents by text", error=str(e))
            return []


class SQLTicketRepository(TicketRepository):
    """SQLAlchemy implementation of TicketRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, model: TicketModel) -> Ticket:
        """Convert database model to domain entity."""
        return Ticket(
            id=model.id,
            user_id=model.user_id,
            subject=model.subject,
            description=model.description,
            status=model.status,
            priority=model.priority,
            category=model.category,
            tags=model.tags or [],
            embedding=list(model.embedding) if model.embedding else None,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
    
    def _entity_to_model(self, entity: Ticket) -> TicketModel:
        """Convert domain entity to database model."""
        return TicketModel(
            id=entity.id,
            user_id=entity.user_id,
            subject=entity.subject,
            description=entity.description,
            status=entity.status,
            priority=entity.priority,
            category=entity.category,
            tags=entity.tags,
            embedding=entity.embedding,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
    
    async def create(self, ticket: Ticket) -> Ticket:
        """Create a new ticket."""
        try:
            model = self._entity_to_model(ticket)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to create ticket", error=str(e))
            raise
    
    async def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        """Get ticket by ID."""
        model = self.session.query(TicketModel).filter(
            TicketModel.id == ticket_id
        ).first()
        return self._model_to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100, status: Optional[str] = None) -> List[Ticket]:
        """Get all tickets with pagination and optional status filter."""
        query = self.session.query(TicketModel)
        
        if status:
            query = query.filter(TicketModel.status == status)
        
        models = query.offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Ticket]:
        """Get tickets by user ID."""
        models = self.session.query(TicketModel).filter(
            TicketModel.user_id == user_id
        ).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, ticket: Ticket) -> Ticket:
        """Update an existing ticket."""
        try:
            model = self.session.query(TicketModel).filter(
                TicketModel.id == ticket.id
            ).first()
            
            if not model:
                raise ValueError(f"Ticket with id {ticket.id} not found")
            
            model.subject = ticket.subject
            model.description = ticket.description
            model.status = ticket.status
            model.priority = ticket.priority
            model.category = ticket.category
            model.tags = ticket.tags
            model.embedding = ticket.embedding
            model.updated_at = ticket.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to update ticket", error=str(e), ticket_id=ticket.id)
            raise
    
    async def delete(self, ticket_id: str) -> bool:
        """Delete a ticket."""
        try:
            result = self.session.query(TicketModel).filter(
                TicketModel.id == ticket_id
            ).delete()
            self.session.commit()
            return result > 0
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to delete ticket", error=str(e), ticket_id=ticket_id)
            raise
    
    async def search_by_embedding(self, embedding: List[float], limit: int = 10) -> List[Ticket]:
        """Search tickets by embedding similarity."""
        try:
            models = self.session.query(TicketModel).filter(
                TicketModel.embedding.is_not(None)
            ).order_by(
                TicketModel.embedding.cosine_distance(embedding)
            ).limit(limit).all()
            
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            logger.error("Failed to search tickets by embedding", error=str(e))
            return []


# Continuing with FAQ and Query repositories...
class SQLFAQRepository(FAQRepository):
    """SQLAlchemy implementation of FAQRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, model: FAQModel) -> FAQ:
        """Convert database model to domain entity."""
        return FAQ(
            id=model.id,
            question=model.question,
            answer=model.answer,
            category=model.category,
            tags=model.tags or [],
            embedding=list(model.embedding) if model.embedding else None,
            view_count=model.view_count,
            helpful_count=model.helpful_count,
            created_at=model.created_at,
            updated_at=model.updated_at,
            is_active=model.is_active
        )
    
    def _entity_to_model(self, entity: FAQ) -> FAQModel:
        """Convert domain entity to database model."""
        return FAQModel(
            id=entity.id,
            question=entity.question,
            answer=entity.answer,
            category=entity.category,
            tags=entity.tags,
            embedding=entity.embedding,
            view_count=entity.view_count,
            helpful_count=entity.helpful_count,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            is_active=entity.is_active
        )
    
    async def create(self, faq: FAQ) -> FAQ:
        """Create a new FAQ."""
        try:
            model = self._entity_to_model(faq)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to create FAQ", error=str(e))
            raise
    
    async def get_by_id(self, faq_id: str) -> Optional[FAQ]:
        """Get FAQ by ID."""
        model = self.session.query(FAQModel).filter(
            FAQModel.id == faq_id,
            FAQModel.is_active == True
        ).first()
        return self._model_to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100, category: Optional[str] = None) -> List[FAQ]:
        """Get all FAQs with pagination and optional category filter."""
        query = self.session.query(FAQModel).filter(FAQModel.is_active == True)
        
        if category:
            query = query.filter(FAQModel.category == category)
        
        models = query.offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, faq: FAQ) -> FAQ:
        """Update an existing FAQ."""
        try:
            model = self.session.query(FAQModel).filter(
                FAQModel.id == faq.id
            ).first()
            
            if not model:
                raise ValueError(f"FAQ with id {faq.id} not found")
            
            model.question = faq.question
            model.answer = faq.answer
            model.category = faq.category
            model.tags = faq.tags
            model.embedding = faq.embedding
            model.view_count = faq.view_count
            model.helpful_count = faq.helpful_count
            model.updated_at = faq.updated_at
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to update FAQ", error=str(e), faq_id=faq.id)
            raise
    
    async def delete(self, faq_id: str) -> bool:
        """Delete a FAQ."""
        try:
            model = self.session.query(FAQModel).filter(
                FAQModel.id == faq_id
            ).first()
            
            if not model:
                return False
            
            model.is_active = False
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to delete FAQ", error=str(e), faq_id=faq_id)
            raise
    
    async def search_by_embedding(self, embedding: List[float], limit: int = 10) -> List[FAQ]:
        """Search FAQs by embedding similarity."""
        try:
            models = self.session.query(FAQModel).filter(
                FAQModel.is_active == True,
                FAQModel.embedding.is_not(None)
            ).order_by(
                FAQModel.embedding.cosine_distance(embedding)
            ).limit(limit).all()
            
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            logger.error("Failed to search FAQs by embedding", error=str(e))
            return []
    
    async def search_by_text(self, query: str, limit: int = 10) -> List[FAQ]:
        """Search FAQs by text."""
        try:
            models = self.session.query(FAQModel).filter(
                FAQModel.is_active == True,
                func.concat(FAQModel.question, ' ', FAQModel.answer).ilike(f'%{query}%')
            ).limit(limit).all()
            
            return [self._model_to_entity(model) for model in models]
        except Exception as e:
            logger.error("Failed to search FAQs by text", error=str(e))
            return []
    
    async def get_popular(self, limit: int = 10) -> List[FAQ]:
        """Get most popular FAQs by view count."""
        models = self.session.query(FAQModel).filter(
            FAQModel.is_active == True
        ).order_by(desc(FAQModel.view_count)).limit(limit).all()
        return [self._model_to_entity(model) for model in models]


class SQLQueryRepository(QueryRepository):
    """SQLAlchemy implementation of QueryRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def _model_to_entity(self, model: QueryModel) -> Query:
        """Convert database model to domain entity."""
        return Query(
            id=model.id,
            user_id=model.user_id,
            query_text=model.query_text,
            embedding=list(model.embedding) if model.embedding else None,
            response=model.response,
            sources=model.sources or [],
            confidence_score=model.confidence_score,
            feedback_rating=model.feedback_rating,
            created_at=model.created_at
        )
    
    def _entity_to_model(self, entity: Query) -> QueryModel:
        """Convert domain entity to database model."""
        return QueryModel(
            id=entity.id,
            user_id=entity.user_id,
            query_text=entity.query_text,
            embedding=entity.embedding,
            response=entity.response,
            sources=entity.sources,
            confidence_score=entity.confidence_score,
            feedback_rating=entity.feedback_rating,
            created_at=entity.created_at
        )
    
    async def create(self, query: Query) -> Query:
        """Create a new query."""
        try:
            model = self._entity_to_model(query)
            self.session.add(model)
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to create query", error=str(e))
            raise
    
    async def get_by_id(self, query_id: str) -> Optional[Query]:
        """Get query by ID."""
        model = self.session.query(QueryModel).filter(
            QueryModel.id == query_id
        ).first()
        return self._model_to_entity(model) if model else None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Query]:
        """Get all queries with pagination."""
        models = self.session.query(QueryModel).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Query]:
        """Get queries by user ID."""
        models = self.session.query(QueryModel).filter(
            QueryModel.user_id == user_id
        ).offset(skip).limit(limit).all()
        return [self._model_to_entity(model) for model in models]
    
    async def update(self, query: Query) -> Query:
        """Update an existing query."""
        try:
            model = self.session.query(QueryModel).filter(
                QueryModel.id == query.id
            ).first()
            
            if not model:
                raise ValueError(f"Query with id {query.id} not found")
            
            model.response = query.response
            model.sources = query.sources
            model.confidence_score = query.confidence_score
            model.feedback_rating = query.feedback_rating
            
            self.session.commit()
            self.session.refresh(model)
            return self._model_to_entity(model)
        except Exception as e:
            self.session.rollback()
            logger.error("Failed to update query", error=str(e), query_id=query.id)
            raise
    
    async def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get query analytics for the specified number of days."""
        try:
            from datetime import datetime, timedelta
            start_date = datetime.utcnow() - timedelta(days=days)
            
            total_queries = self.session.query(QueryModel).filter(
                QueryModel.created_at >= start_date
            ).count()
            
            avg_rating = self.session.query(func.avg(QueryModel.feedback_rating)).filter(
                QueryModel.created_at >= start_date,
                QueryModel.feedback_rating.is_not(None)
            ).scalar() or 0
            
            queries_with_feedback = self.session.query(QueryModel).filter(
                QueryModel.created_at >= start_date,
                QueryModel.feedback_rating.is_not(None)
            ).count()
            
            return {
                "total_queries": total_queries,
                "average_rating": round(float(avg_rating), 2),
                "queries_with_feedback": queries_with_feedback,
                "feedback_rate": round(queries_with_feedback / total_queries * 100, 2) if total_queries > 0 else 0,
                "period_days": days
            }
        except Exception as e:
            logger.error("Failed to get query analytics", error=str(e))
            return {
                "total_queries": 0,
                "average_rating": 0,
                "queries_with_feedback": 0,
                "feedback_rate": 0,
                "period_days": days
            }