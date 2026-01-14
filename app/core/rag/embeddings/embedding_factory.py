"""
Embedding factory for RAG pipeline.

Creates embedding instances with configurable models.
"""

import logging
from langchain_community.embeddings import HuggingFaceEmbeddings

from app.core.rag.config import RAGConfig

logger = logging.getLogger(__name__)


class EmbeddingFactory:
    """
    Factory for creating embedding instances.
    
    Provides centralized embedding configuration with support
    for different embedding models.
    """
    
    @staticmethod
    def create_embeddings(model_name: str = None) -> HuggingFaceEmbeddings:
        """
        Create HuggingFace embeddings instance.
        
        Args:
            model_name: Name of the HuggingFace model to use
                       If None, uses RAGConfig.EMBEDDING_MODEL
        
        Returns:
            HuggingFaceEmbeddings: Configured embeddings instance
        
        Example:
            >>> embeddings = EmbeddingFactory.create_embeddings()
            >>> vector = embeddings.embed_query("hello world")
        """
        if model_name is None:
            model_name = RAGConfig.EMBEDDING_MODEL
        
        logger.info(f"Creating embeddings with model: {model_name}")
        
        embeddings = HuggingFaceEmbeddings(
            model_name=model_name,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        return embeddings
    
    @staticmethod
    def get_default_embeddings() -> HuggingFaceEmbeddings:
        """
        Get default embeddings instance.
        
        Returns:
            HuggingFaceEmbeddings: Default configured embeddings
        """
        return EmbeddingFactory.create_embeddings()
