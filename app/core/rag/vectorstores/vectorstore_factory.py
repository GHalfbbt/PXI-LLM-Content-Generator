"""
Vector store factory for RAG pipeline.

Manages ChromaDB vector store with persistence.
"""

from typing import List, Optional
import logging
from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain.embeddings.base import Embeddings

from app.core.rag.config import RAGConfig
from app.core.rag.embeddings import EmbeddingFactory

logger = logging.getLogger(__name__)


class VectorStoreFactory:
    """
    Factory for creating and managing ChromaDB vector stores.
    
    Handles vector store creation, persistence, and loading.
    """
    
    @staticmethod
    def create_vectorstore_from_documents(
        documents: List[Document],
        embeddings: Optional[Embeddings] = None,
        collection_name: str = None,
        persist_directory: str = None
    ) -> Chroma:
        """
        Create a new ChromaDB vector store from documents.
        
        Args:
            documents: List of documents to embed and store
            embeddings: Embeddings instance to use
                       If None, uses default from EmbeddingFactory
            collection_name: Name for the Chroma collection
                           If None, uses RAGConfig.CHROMA_COLLECTION_NAME
            persist_directory: Directory to persist vectors
                             If None, uses RAGConfig.CHROMA_PERSIST_DIR
        
        Returns:
            Chroma: Configured and persisted vector store
        
        Raises:
            ValueError: If documents list is empty
        
        Example:
            >>> docs = load_arxiv_documents("AI")
            >>> chunks = split_documents(docs)
            >>> vectorstore = VectorStoreFactory.create_vectorstore_from_documents(chunks)
        """
        if not documents:
            raise ValueError("Documents list cannot be empty")
        
        if embeddings is None:
            embeddings = EmbeddingFactory.get_default_embeddings()
        
        if collection_name is None:
            collection_name = RAGConfig.CHROMA_COLLECTION_NAME
        
        if persist_directory is None:
            persist_directory = str(RAGConfig.get_chroma_persist_dir())
        
        logger.info(f"Creating vector store with {len(documents)} documents")
        logger.info(f"Collection: {collection_name}, Persist dir: {persist_directory}")
        
        # Create vector store with persistence
        vectorstore = Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name=collection_name,
            persist_directory=persist_directory
        )
        
        logger.info("Vector store created and persisted successfully")
        return vectorstore
    
    @staticmethod
    def load_existing_vectorstore(
        embeddings: Optional[Embeddings] = None,
        collection_name: str = None,
        persist_directory: str = None
    ) -> Chroma:
        """
        Load an existing ChromaDB vector store from disk.
        
        Args:
            embeddings: Embeddings instance to use
                       If None, uses default from EmbeddingFactory
            collection_name: Name of the Chroma collection to load
                           If None, uses RAGConfig.CHROMA_COLLECTION_NAME
            persist_directory: Directory where vectors are persisted
                             If None, uses RAGConfig.CHROMA_PERSIST_DIR
        
        Returns:
            Chroma: Loaded vector store
        
        Raises:
            ValueError: If vector store doesn't exist
        
        Example:
            >>> vectorstore = VectorStoreFactory.load_existing_vectorstore()
            >>> results = vectorstore.similarity_search("quantum computing")
        """
        if embeddings is None:
            embeddings = EmbeddingFactory.get_default_embeddings()
        
        if collection_name is None:
            collection_name = RAGConfig.CHROMA_COLLECTION_NAME
        
        if persist_directory is None:
            persist_directory = str(RAGConfig.get_chroma_persist_dir())
        
        logger.info(f"Loading existing vector store from {persist_directory}")
        
        try:
            vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=embeddings,
                persist_directory=persist_directory
            )
            
            logger.info("Vector store loaded successfully")
            return vectorstore
        
        except Exception as e:
            logger.error(f"Failed to load vector store: {str(e)}")
            raise ValueError(f"Vector store not found or corrupted: {str(e)}")
    
    @staticmethod
    def vectorstore_exists(
        collection_name: str = None,
        persist_directory: str = None
    ) -> bool:
        """
        Check if a vector store exists on disk.
        
        Args:
            collection_name: Name of the collection to check
            persist_directory: Directory to check
        
        Returns:
            bool: True if vector store exists, False otherwise
        """
        if persist_directory is None:
            persist_directory = str(RAGConfig.get_chroma_persist_dir())
        
        from pathlib import Path
        persist_path = Path(persist_directory)
        
        return persist_path.exists() and any(persist_path.iterdir())
