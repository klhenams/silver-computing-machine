from sqlalchemy import create_engine, Column, String, Text, DateTime, Boolean, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from pgvector.sqlalchemy import Vector
import uuid
from datetime import datetime
from typing import Optional


Base = declarative_base()


class DocumentModel(Base):
    """SQLAlchemy model for documents."""
    
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(ARRAY(String), default=list)
    embedding = Column(Vector(384))  # Assuming 384-dimensional embeddings
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class TicketModel(Base):
    """SQLAlchemy model for tickets."""
    
    __tablename__ = "tickets"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False)
    subject = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    status = Column(String(20), default="open")
    priority = Column(String(20), default="medium")
    category = Column(String(50), nullable=False)
    tags = Column(ARRAY(String), default=list)
    embedding = Column(Vector(384))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FAQModel(Base):
    """SQLAlchemy model for FAQs."""
    
    __tablename__ = "faqs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(String(500), nullable=False)
    answer = Column(Text, nullable=False)
    category = Column(String(50), nullable=False)
    tags = Column(ARRAY(String), default=list)
    embedding = Column(Vector(384))
    view_count = Column(Integer, default=0)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class QueryModel(Base):
    """SQLAlchemy model for queries."""
    
    __tablename__ = "queries"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=True)
    query_text = Column(Text, nullable=False)
    embedding = Column(Vector(384))
    response = Column(Text, nullable=True)
    sources = Column(ARRAY(String), default=list)
    confidence_score = Column(Float, nullable=True)
    feedback_rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class DatabaseConfig:
    """Database configuration and session management."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get database session."""
        session = self.SessionLocal()
        try:
            yield session
        finally:
            session.close()


# Database dependency
def get_database_config() -> DatabaseConfig:
    """Get database configuration from environment."""
    import os
    database_url = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/support_system"
    )
    return DatabaseConfig(database_url)