"""
Content generation chain using LangChain.

This module orchestrates the content generation pipeline by combining
the prompt template with the LLM provider to create a complete chain
that generates blog posts based on user inputs.
"""

from typing import Optional

from app.core.prompts.blog import get_blog_prompt
from app.core.identity import IdentityProfile, build_identity_context
from app.llms.factory import LLMFactory
from app.config import settings


# ============================================================================
# CONTENT GENERATION CHAIN
# ============================================================================

def generate_blog_content(
    topic: str,
    audience: str,
    tone: str,
    language: str,
    llm_provider: str = "groq",
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None,
    identity: Optional[IdentityProfile] = None
) -> str:
    """
    Generate blog content using LangChain with selected LLM provider.
    
    This function is the main entry point for blog content generation.
    It creates a chain by combining the blog prompt template with the
    selected LLM provider (Groq or Ollama), then executes the chain 
    with the provided parameters.
    
    The generation process:
    1. Initialize the selected LLM provider using the factory
    2. Load the blog prompt template
    3. Optionally inject identity context if provided
    4. Create a LangChain chain linking prompt and LLM
    5. Execute the chain with user-provided inputs
    6. Return the generated blog post content
    
    Args:
        topic (str): The main subject or theme of the blog post.
                    Example: "The Future of Artificial Intelligence"
        audience (str): Target audience for the content.
                       Example: "software developers", "general public", "business executives"
        tone (str): Desired writing tone for the content.
                   Example: "professional", "casual", "friendly", "technical"
        language (str): Language in which to generate the content.
                       Example: "English", "Spanish", "French"
        llm_provider (str): LLM provider to use ("groq" or "ollama").
                           Defaults to "groq" for cloud-based generation.
        temperature (float, optional): Controls randomness in generation.
                                      Range: 0.0 (deterministic) to 1.0 (creative).
                                      Defaults to settings.DEFAULT_TEMPERATURE (0.7).
        max_tokens (int, optional): Maximum number of tokens to generate.
                                   Defaults to settings.DEFAULT_MAX_TOKENS (2048).
        identity (IdentityProfile, optional): Identity information to personalize content.
                                             If provided, content reflects this identity's voice.
    
    Returns:
        str: The generated blog post content, ready for publication.
    
    Raises:
        ValueError: If required configuration (API keys) is missing.
        Exception: If content generation fails due to API errors or other issues.
    
    Example:
        >>> content = generate_blog_content(
        ...     topic="Python Best Practices",
        ...     audience="intermediate developers",
        ...     tone="professional and educational",
        ...     language="English"
        ... )
        >>> print(content)
    """
    # Use default values from settings if not provided
    if temperature is None:
        temperature = settings.DEFAULT_TEMPERATURE
    if max_tokens is None:
        max_tokens = settings.DEFAULT_MAX_TOKENS
    
    # Step 1: Initialize the selected LLM provider using the factory
    # The factory handles instantiation of Groq or Ollama based on provider
    llm_instance = LLMFactory.create_llm(llm_provider)
    
    # Step 2: Validate that the LLM is properly configured before proceeding
    if not llm_instance.validate():
        raise ValueError(
            f"{llm_provider.upper()} LLM is not properly configured. "
            f"Please check your environment variables and configuration."
        )
    
    # Step 3: Get the configured LLM instance with specified parameters
    # This creates the actual LLM instance ready for inference
    llm = llm_instance.get_llm(
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Step 4: Load the blog prompt template
    # This template defines how the LLM should structure the blog post
    prompt = get_blog_prompt()
    
    # Step 5: Inject identity context if provided
    # Identity context is prepended to the prompt to personalize content
    if identity:
        identity_context = build_identity_context(identity)
        # Modify the prompt template to include identity context
        # We prepend identity to the template's template string
        from langchain_core.prompts import PromptTemplate
        original_template = prompt.template
        enhanced_template = identity_context + "\n\n" + original_template
        prompt = PromptTemplate(
            template=enhanced_template,
            input_variables=prompt.input_variables
        )
    
    # Step 6: Create the LangChain chain using LCEL (LangChain Expression Language)
    # Modern LangChain uses the pipe operator (|) to chain components
    # This creates a pipeline: prompt -> LLM -> output parser
    chain = prompt | llm
    
    # Step 7: Execute the chain with user inputs
    # The chain will format the prompt with the provided variables
    # and send it to the LLM for content generation
    try:
        result = chain.invoke({
            "topic": topic,
            "audience": audience,
            "tone": tone,
            "language": language
        })
        
        # Extract the content from the response
        # The result is an AIMessage object, we need the content string
        if hasattr(result, 'content'):
            content = result.content
        else:
            content = str(result)
        
        # Return the generated content as a string
        # The result is the complete blog post ready for display/publication
        return content.strip()
    
    except Exception as e:
        # Catch and re-raise with more context if generation fails
        raise Exception(f"Failed to generate blog content: {str(e)}") from e
