"""
arXiv document loader.

Loads scientific papers metadata from arXiv without downloading PDFs.
"""

from typing import List
import logging
import arxiv
from langchain_core.documents import Document

from app.core.rag.config import RAGConfig

logger = logging.getLogger(__name__)


def load_arxiv_documents(
    query: str,
    max_docs: int = None
) -> List[Document]:
    """
    Load document metadata from arXiv based on search query (no PDF download).
    
    Args:
        query: Search query for arXiv (e.g., "quantum computing")
        max_docs: Maximum number of documents to load
                 If None, uses RAGConfig.ARXIV_MAX_DOCS
    
    Returns:
        List[Document]: List of documents with metadata (title, authors, abstract, URL)
    
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
        # Use arxiv API directly to get metadata only (no PDF download)
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_docs,
            sort_by=arxiv.SortCriterion.Relevance
        )
        
        documents = []
        for result in client.results(search):
            # Create document with abstract as content and metadata
            doc = Document(
                page_content=result.summary,  # Use abstract as content
                metadata={
                    "title": result.title,
                    "authors": ", ".join([author.name for author in result.authors]),
                    "published": result.published.strftime("%Y-%m-%d"),
                    "source": result.entry_id,  # arXiv URL
                    "arxiv_id": result.entry_id.split("/")[-1]
                }
            )
            documents.append(doc)
        
        logger.info(f"Successfully loaded {len(documents)} documents from arXiv (metadata only)")
        return documents
    
    except Exception as e:
        logger.error(f"Failed to load documents from arXiv: {str(e)}")
        raise Exception(f"arXiv loader error: {str(e)}")
