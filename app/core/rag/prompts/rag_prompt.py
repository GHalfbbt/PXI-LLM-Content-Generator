"""
RAG prompt templates for scientific content.

Prompts designed for explaining scientific concepts to general audiences.
"""

from langchain.prompts import PromptTemplate


def get_rag_prompt() -> PromptTemplate:
    """
    Get the RAG prompt template for scientific divulgation.
    
    This prompt instructs the LLM to:
    - Explain scientific concepts clearly to general audiences
    - Use retrieved context as the primary source of information
    - Be accurate but accessible
    - Avoid hallucinations or unsupported claims
    - Cite information conceptually (not with fake citations)
    
    Returns:
        PromptTemplate: Configured prompt template with context and question variables
    
    Example:
        >>> prompt = get_rag_prompt()
        >>> formatted = prompt.format(context="...", question="What is quantum computing?")
    """
    template = """You are a science communicator explaining complex scientific concepts to a general audience.

Use the following scientific information to answer the question. Your goal is to make the content accurate, clear, and accessible to non-experts.

Guidelines:
- Base your answer strictly on the provided context
- Explain technical terms in simple language
- Use analogies or examples when helpful
- Be accurate and honest - if the context doesn't contain the answer, say so
- Do NOT make up information or citations
- Do NOT use academic jargon without explanation
- Keep the tone educational and engaging

Context:
{context}

Question: {question}

Answer:"""
    
    return PromptTemplate(
        template=template,
        input_variables=["context", "question"]
    )
