from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class EmbeddingService(ABC):
    """Abstract service for generating embeddings."""

    @abstractmethod
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        pass

    @abstractmethod
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        pass


class LLMService(ABC):
    """Abstract service for LLM operations."""

    @abstractmethod
    async def generate_response(
        self,
        query: str,
        context: List[str],
        max_length: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate response using LLM with given context."""
        pass

    @abstractmethod
    async def summarize_text(self, text: str, max_length: int = 150) -> str:
        """Summarize the given text."""
        pass

    @abstractmethod
    async def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from the given text."""
        pass


class VectorSearchService(ABC):
    """Abstract service for vector similarity search."""

    @abstractmethod
    async def find_similar_documents(
        self,
        query_embedding: List[float],
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Find similar documents based on embedding similarity."""
        pass

    @abstractmethod
    async def find_similar_tickets(
        self,
        query_embedding: List[float],
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Find similar tickets based on embedding similarity."""
        pass

    @abstractmethod
    async def find_similar_faqs(
        self,
        query_embedding: List[float],
        limit: int = 10,
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """Find similar FAQs based on embedding similarity."""
        pass