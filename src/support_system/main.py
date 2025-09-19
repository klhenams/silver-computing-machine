from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import structlog
from contextlib import asynccontextmanager

from .infrastructure.config import settings
from .infrastructure.container import container
from .infrastructure.database.models import get_database_config
from .presentation.api import documents, tickets, faqs, queries
from .application.interfaces.services import DocumentService, TicketService, FAQService, QueryService

# Configure logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up Support System API")
    
    # Create database tables
    try:
        db_config = get_database_config()
        db_config.create_tables()
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down Support System API")


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency overrides for API routes
def get_database_session() -> Session:
    """Get database session dependency."""
    return next(container.get_database_session())


def get_document_service(session: Session = Depends(get_database_session)) -> DocumentService:
    """Get document service dependency."""
    return container.get_document_service(session)


def get_ticket_service(session: Session = Depends(get_database_session)) -> TicketService:
    """Get ticket service dependency."""
    return container.get_ticket_service(session)


def get_faq_service(session: Session = Depends(get_database_session)) -> FAQService:
    """Get FAQ service dependency."""
    return container.get_faq_service(session)


def get_query_service(session: Session = Depends(get_database_session)) -> QueryService:
    """Get query service dependency."""
    return container.get_query_service(session)


# Override the dependencies in the routers
documents.get_document_service = get_document_service
tickets.get_ticket_service = get_ticket_service
faqs.get_faq_service = get_faq_service
queries.get_query_service = get_query_service

# Include routers
app.include_router(documents.router, prefix="/api/v1")
app.include_router(tickets.router, prefix="/api/v1")
app.include_router(faqs.router, prefix="/api/v1")
app.include_router(queries.router, prefix="/api/v1")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Support System API",
        "version": settings.api_version,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    import time
    timestamper = structlog.processors.TimeStamper(fmt="iso")
    timestamp_dict = timestamper(None, None, {"timestamp": time.time()})
    return {
        "status": "healthy",
        "version": settings.api_version,
        "timestamp": timestamp_dict.get("timestamp")
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level=settings.log_level.lower()
    )