"""
RAG chain orchestration.

Builds complete RAG chains for question answering using retrieved context.
"""

import logging
from langchain.chains import RetrievalQA
from langchain.schema import BaseRetriever
from langchain.llms.base import BaseLLM

from app.core.rag.prompts import get_rag_prompt

logger = logging.getLogger(__name__)


def build_rag_chain(
    llm: BaseLLM,
    retriever: BaseRetriever
) -> RetrievalQA:
    """
    Build a complete RAG chain for question answering.
    
    Chain structure:
    1. User asks a question
    2. Retriever fetches relevant context from vector store
    3. Context and question are formatted into prompt
    4. LLM generates answer based on context
    
    Args:
        llm: Language model instance (e.g., ChatGroq, ChatOllama)
        retriever: Configured retriever with access to vector store
    
    Returns:
        RetrievalQA: Complete RAG chain ready for use
    
    Raises:
        ValueError: If llm or retriever is None
    
    Example:
        >>> from app.llms.groq_llm import create_groq_llm
        >>> from app.core.rag.vectorstores import VectorStoreFactory
        >>> from app.core.rag.retrievers import RetrieverFactory
        >>> 
        >>> llm = create_groq_llm()
        >>> vectorstore = VectorStoreFactory.load_existing_vectorstore()
        >>> retriever = RetrieverFactory.create_retriever(vectorstore)
        >>> 
        >>> chain = build_rag_chain(llm, retriever)
        >>> result = chain.run("What is quantum entanglement?")
        >>> print(result)
    """
    if llm is None:
        raise ValueError("LLM cannot be None")
    
    if retriever is None:
        raise ValueError("Retriever cannot be None")
    
    logger.info("Building RAG chain")
    
    # Get RAG prompt template
    prompt = get_rag_prompt()
    
    # Build RetrievalQA chain
    rag_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        return_source_documents=False,
        chain_type_kwargs={
            "prompt": prompt
        }
    )
    
    logger.info("RAG chain built successfully")
    return rag_chain
