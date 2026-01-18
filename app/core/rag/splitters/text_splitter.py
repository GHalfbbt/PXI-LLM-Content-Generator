"""
Text splitting for RAG pipeline.

Splits documents into smaller chunks while preserving metadata.
"""

from typing import List
import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from app.core.rag.config import RAGConfig

logger = logging.getLogger(__name__)


def split_documents(
    documents: List[Document],
    chunk_size: int = None,
    chunk_overlap: int = None
) -> List[Document]:
    """
    Split documents into smaller chunks.
    
    Uses RecursiveCharacterTextSplitter to intelligently split text
    at natural boundaries while preserving metadata.
    
    Args:
        documents: List of documents to split
        chunk_size: Size of each chunk in characters
                   If None, uses RAGConfig.CHUNK_SIZE
        chunk_overlap: Overlap between chunks
                      If None, uses RAGConfig.CHUNK_OVERLAP
    
    Returns:
        List[Document]: List of document chunks with preserved metadata
    
    Raises:
        ValueError: If documents list is empty
    
    Example:
        >>> docs = load_arxiv_documents("AI")
        >>> chunks = split_documents(docs, chunk_size=500)
        >>> print(len(chunks))
    """
    if not documents:
        raise ValueError("Documents list cannot be empty")
    
    if chunk_size is None:
        chunk_size = RAGConfig.CHUNK_SIZE
    
    if chunk_overlap is None:
        chunk_overlap = RAGConfig.CHUNK_OVERLAP
    
    logger.info(f"Splitting {len(documents)} documents with chunk_size={chunk_size}, overlap={chunk_overlap}")
    
    # Initialize text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )
    
    # Split documents
    split_docs = text_splitter.split_documents(documents)
    
    logger.info(f"Split into {len(split_docs)} chunks")
    return split_docs
