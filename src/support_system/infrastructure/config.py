from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings."""
    
    # Database
    database_url: str = "postgresql://postgres:password@localhost:5432/support_system"
    
    # API
    api_title: str = "Support System API"
    api_description: str = "Modern support system with LLMs and vector databases"
    api_version: str = "1.0.0"
    debug: bool = False
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Hugging Face
    huggingface_api_key: Optional[str] = None
    huggingface_model: str = "microsoft/DialoGPT-large"
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    # Vector Search
    similarity_threshold: float = 0.7
    max_search_results: int = 10
    
    # LLM
    max_response_length: int = 500
    temperature: float = 0.7
    max_context_length: int = 2000
    
    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()