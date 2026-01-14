"""
arXiv document loader.

Loads scientific papers from arXiv with clean metadata.
"""

from typing import List
import logging
from langchain_community.document_loaders import ArxivLoader
from langchain.schema import Document

from app.core.rag.config import RAGConfig

logger = logging.getLogger(__name__)


def load_arxiv_documents(
    query: str,
    max_docs: int = None
) -> List[Document]:
    """
    Load documents from arXiv based on search query.
    
    Args:
        query: Search query for arXiv (e.g., "quantum computing")
        max_docs: Maximum number of documents to load
                 If None, uses RAGConfig.ARXIV_MAX_DOCS
    
    Returns:
        List[Document]: List of documents with cleaned metadata
    
    Raises:
        ValueError: If query is empty
        Exception: If arXiv API fails
    
    Example:
        >>> docs = load_arxiv_documents("machine learning", max_docs=3)
        >>> print(docs[0].metadata["title"])
    """
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")
    
    if max_docs is None:
        max_docs = RAGConfig.ARXIV_MAX_DOCS
    
    logger.info(f"Loading {max_docs} documents from arXiv for query: '{query}'")
    
    try:
        # Initialize arXiv loader
        loader = ArxivLoader(
            query=query,
            load_max_docs=max_docs
        )
        
        # Load documents
        documents = loader.load()
        
        # Clean and standardize metadata
        for doc in documents:
            # Ensure required metadata fields
            doc.metadata["source"] = "arxiv"
            
            # Keep only relevant metadata
            cleaned_metadata = {
                "title": doc.metadata.get("Title", "Unknown"),
                "authors": doc.metadata.get("Authors", "Unknown"),
                "published": doc.metadata.get("Published", "Unknown"),
                "source": "arxiv"
            }
            
            doc.metadata = cleaned_metadata
        
        logger.info(f"Successfully loaded {len(documents)} documents from arXiv")
        return documents
    
    except Exception as e:
        logger.error(f"Failed to load documents from arXiv: {str(e)}")
        raise Exception(f"arXiv loader error: {str(e)}")
