import httpx
import numpy as np
from typing import List, Optional
from sentence_transformers import SentenceTransformer
from ..config import settings
from ...domain.services.interfaces import EmbeddingService, LLMService
import asyncio
import structlog

logger = structlog.get_logger()


class HuggingFaceEmbeddingService(EmbeddingService):
    """Hugging Face embedding service implementation."""
    
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the given text."""
        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None, 
                self.model.encode, 
                text
            )
            # Ensure we return a Python list, not a NumPy array
            if hasattr(embedding, 'tolist'):
                return embedding.tolist()
            else:
                return list(embedding)
        except Exception as e:
            logger.error("Failed to generate embedding", error=str(e), text=text[:100])
            raise
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            loop = asyncio.get_event_loop()
            embeddings = await loop.run_in_executor(
                None, 
                self.model.encode, 
                texts
            )
            # Ensure we return Python lists, not NumPy arrays
            if hasattr(embeddings, 'tolist'):
                return embeddings.tolist()
            else:
                return [list(emb) for emb in embeddings]
        except Exception as e:
            logger.error("Failed to generate batch embeddings", error=str(e), batch_size=len(texts))
            raise


class HuggingFaceLLMService(LLMService):
    """Hugging Face LLM service implementation."""
    
    def __init__(self):
        self.api_key = settings.huggingface_api_key
        self.model = settings.huggingface_model
        self.base_url = "https://api-inference.huggingface.co/models"
    
    async def generate_response(
        self,
        query: str,
        context: List[str],
        max_length: int = 500,
        temperature: float = 0.7
    ) -> str:
        """Generate response using LLM with given context."""
        try:
            # Prepare the prompt with context
            context_text = "\n".join(context[:5])  # Limit context to prevent token overflow
            prompt = f"""Based on the following context, provide a helpful answer to the user's question.

Context:
{context_text}

Question: {query}

Answer:"""

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": max_length,
                    "temperature": temperature,
                    "return_full_text": False
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/{self.model}",
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        generated_text = result[0].get("generated_text", "").strip()
                        return generated_text
                    else:
                        return "I apologize, but I couldn't generate a response at this time."
                else:
                    logger.error("HuggingFace API error", status_code=response.status_code, response=response.text)
                    return "I apologize, but I'm experiencing technical difficulties. Please try again later."
                    
        except Exception as e:
            logger.error("Failed to generate LLM response", error=str(e), query=query[:100])
            return "I apologize, but I couldn't process your request at this time. Please try again later."
    
    async def summarize_text(self, text: str, max_length: int = 150) -> str:
        """Summarize the given text."""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": text,
                "parameters": {
                    "max_length": max_length,
                    "min_length": 30,
                    "do_sample": False
                }
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/facebook/bart-large-cnn",  # Summarization model
                    headers=headers,
                    json=payload
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        return result[0].get("summary_text", text[:max_length])
                    else:
                        return text[:max_length]
                else:
                    logger.error("Summarization API error", status_code=response.status_code)
                    return text[:max_length]
                    
        except Exception as e:
            logger.error("Failed to summarize text", error=str(e))
            return text[:max_length]
    
    async def extract_keywords(self, text: str, max_keywords: int = 10) -> List[str]:
        """Extract keywords from the given text."""
        try:
            # Simple keyword extraction using common words filtering
            # In production, you might want to use a proper NER model
            words = text.lower().split()
            
            # Filter out common stop words
            stop_words = {
                "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", 
                "by", "is", "are", "was", "were", "be", "been", "have", "has", "had", "do", "does",
                "did", "will", "would", "could", "should", "may", "might", "can", "i", "you", "he",
                "she", "it", "we", "they", "this", "that", "these", "those"
            }
            
            keywords = [word.strip(".,!?") for word in words if len(word) > 3 and word not in stop_words]
            
            # Remove duplicates while preserving order
            unique_keywords = []
            seen = set()
            for keyword in keywords:
                if keyword not in seen:
                    unique_keywords.append(keyword)
                    seen.add(keyword)
            
            return unique_keywords[:max_keywords]
            
        except Exception as e:
            logger.error("Failed to extract keywords", error=str(e))
            return []