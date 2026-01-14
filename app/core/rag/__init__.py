"""
RAG (Retrieval-Augmented Generation) core module.

This module provides a complete RAG pipeline for scientific content:
- Document loading from arXiv
- Text splitting and chunking
- Embedding generation
- Vector storage with ChromaDB
- Retrieval and RAG chain orchestration

All components are modular, reusable, and platform-agnostic.
"""

from app.core.rag.config import RAGConfig

__all__ = ["RAGConfig"]
