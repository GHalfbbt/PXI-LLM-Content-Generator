"""
Retriever factory for RAG pipeline.

Creates retriever instances from vector stores.
"""

import logging
from langchain_core.vectorstores import VectorStore
from langchain_core.retrievers import BaseRetriever

from app.core.rag.config import RAGConfig

logger = logging.getLogger(__name__)


class RetrieverFactory:
    """
    Factory for creating retriever instances from vector stores.
    """
    
    @staticmethod
    def create_retriever(
        vectorstore: VectorStore,
        search_type: str = None,
        k: int = None
    ) -> BaseRetriever:
        """
        Create a retriever from a vector store.
        
        Args:
            vectorstore: Vector store to create retriever from
            search_type: Type of search to perform
                        If None, uses RAGConfig.RETRIEVER_SEARCH_TYPE
                        Options: "similarity", "mmr", "similarity_score_threshold"
            k: Number of documents to retrieve
               If None, uses RAGConfig.RETRIEVER_K
        
        Returns:
            BaseRetriever: Configured retriever instance
        
        Example:
            >>> vectorstore = VectorStoreFactory.load_existing_vectorstore()
            >>> retriever = RetrieverFactory.create_retriever(vectorstore, k=4)
            >>> docs = retriever.get_relevant_documents("quantum computing")
        """
        if search_type is None:
            search_type = RAGConfig.RETRIEVER_SEARCH_TYPE
        
        if k is None:
            k = RAGConfig.RETRIEVER_K
        
        logger.info(f"Creating retriever with search_type={search_type}, k={k}")
        
        retriever = vectorstore.as_retriever(
            search_type=search_type,
            search_kwargs={"k": k}
        )
        
        return retriever
    
    @staticmethod
    def create_default_retriever(vectorstore: VectorStore) -> BaseRetriever:
        """
        Create a retriever with default configuration.
        
        Args:
            vectorstore: Vector store to create retriever from
        
        Returns:
            BaseRetriever: Retriever with default settings
        """
        return RetrieverFactory.create_retriever(vectorstore)
