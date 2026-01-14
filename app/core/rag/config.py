"""
RAG configuration module.

Centralizes all RAG-related configuration with environment variable support.
"""

import os
from pathlib import Path


class RAGConfig:
    """
    Configuration for RAG components.
    
    All settings can be overridden via environment variables.
    """
    
    # Text splitting configuration
    CHUNK_SIZE: int = int(os.getenv("RAG_CHUNK_SIZE", "1000"))
    CHUNK_OVERLAP: int = int(os.getenv("RAG_CHUNK_OVERLAP", "200"))
    
    # Embedding configuration
    EMBEDDING_MODEL: str = os.getenv(
        "RAG_EMBEDDING_MODEL",
        "sentence-transformers/all-MiniLM-L6-v2"
    )
    
    # Vector store configuration
    CHROMA_PERSIST_DIR: str = os.getenv(
        "RAG_CHROMA_DIR",
        str(Path(__file__).parent.parent.parent / "storage" / "chroma")
    )
    CHROMA_COLLECTION_NAME: str = os.getenv(
        "RAG_CHROMA_COLLECTION",
        "scientific_rag"
    )
    
    # Retriever configuration
    RETRIEVER_SEARCH_TYPE: str = os.getenv("RAG_SEARCH_TYPE", "similarity")
    RETRIEVER_K: int = int(os.getenv("RAG_RETRIEVER_K", "4"))
    
    # ArXiv loader configuration
    ARXIV_MAX_DOCS: int = int(os.getenv("RAG_ARXIV_MAX_DOCS", "5"))
    
    @classmethod
    def get_chroma_persist_dir(cls) -> Path:
        """
        Get ChromaDB persist directory as Path object.
        
        Creates directory if it doesn't exist.
        
        Returns:
            Path: ChromaDB persist directory
        """
        persist_dir = Path(cls.CHROMA_PERSIST_DIR)
        persist_dir.mkdir(parents=True, exist_ok=True)
        return persist_dir
