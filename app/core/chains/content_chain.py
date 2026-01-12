"""
Content generation chain using LangChain.

This module orchestrates the content generation pipeline by combining
the prompt template with the LLM provider to create a complete chain
that generates blog posts based on user inputs.
"""

from typing import Optional
from langchain.chains import LLMChain

from app.core.prompts.blog import get_blog_prompt
from app.llms.groq_llm import GroqLLM
from app.config import settings


# ============================================================================
# CONTENT GENERATION CHAIN
# ============================================================================

def generate_blog_content(
    topic: str,
    audience: str,
    tone: str,
    language: str,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> str:
    """
    Generate blog content using LangChain LLMChain with Groq LLM.
    
    This function is the main entry point for blog content generation.
    It creates a chain by combining the blog prompt template with the
    Groq LLM provider, then executes the chain with the provided parameters.
    
    The generation process:
    1. Initialize the Groq LLM with configuration settings
    2. Load the blog prompt template
    3. Create a LangChain LLMChain linking prompt and LLM
    4. Execute the chain with user-provided inputs
    5. Return the generated blog post content
    
    Args:
        topic (str): The main subject or theme of the blog post.
                    Example: "The Future of Artificial Intelligence"
        audience (str): Target audience for the content.
                       Example: "software developers", "general public", "business executives"
        tone (str): Desired writing tone for the content.
                   Example: "professional", "casual", "friendly", "technical"
        language (str): Language in which to generate the content.
                       Example: "English", "Spanish", "French"
        temperature (float, optional): Controls randomness in generation.
                                      Range: 0.0 (deterministic) to 1.0 (creative).
                                      Defaults to settings.DEFAULT_TEMPERATURE (0.7).
        max_tokens (int, optional): Maximum number of tokens to generate.
                                   Defaults to settings.DEFAULT_MAX_TOKENS (2048).
    
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
    
    # Step 1: Initialize the Groq LLM provider with configuration
    # The GroqLLM class will automatically read API key and model from settings
    groq_llm = GroqLLM()
    
    # Step 2: Validate that the LLM is properly configured before proceeding
    if not groq_llm.validate():
        raise ValueError(
            "Groq LLM is not properly configured. "
            "Please check your GROQ_API_KEY environment variable."
        )
    
    # Step 3: Get the configured LLM instance with specified parameters
    # This creates the actual ChatGroq instance ready for inference
    llm = groq_llm.get_llm(
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Step 4: Load the blog prompt template
    # This template defines how the LLM should structure the blog post
    prompt = get_blog_prompt()
    
    # Step 5: Create the LangChain LLMChain
    # This chain connects the prompt template with the LLM,
    # allowing us to pass variables and get generated content
    chain = LLMChain(
        llm=llm,
        prompt=prompt,
        verbose=False  # Set to True for debugging to see the full prompt
    )
    
    # Step 6: Execute the chain with user inputs
    # The chain will format the prompt with the provided variables
    # and send it to the LLM for content generation
    try:
        result = chain.run(
            topic=topic,
            audience=audience,
            tone=tone,
            language=language
        )
        
        # Return the generated content as a string
        # The result is the complete blog post ready for display/publication
        return result.strip()
    
    except Exception as e:
        # Catch and re-raise with more context if generation fails
        raise Exception(f"Failed to generate blog content: {str(e)}") from e


# ============================================================================
# CHAIN FACTORY (FOR FUTURE EXTENSIBILITY)
# ============================================================================

def create_blog_chain(temperature: float = 0.7, max_tokens: int = 2048) -> LLMChain:
    """
    Factory function to create a reusable blog content generation chain.
    
    This function creates and returns a configured LLMChain that can be
    reused multiple times without reinitializing the LLM each time.
    Useful for batch processing or when generating multiple blog posts.
    
    Args:
        temperature (float): Controls randomness in generation. Default 0.7.
        max_tokens (int): Maximum tokens to generate. Default 2048.
    
    Returns:
        LLMChain: Configured chain ready for content generation.
    
    Example:
        >>> chain = create_blog_chain(temperature=0.8)
        >>> content1 = chain.run(topic="AI", audience="developers", ...)
        >>> content2 = chain.run(topic="ML", audience="students", ...)
    """
    # Initialize and validate the Groq LLM
    groq_llm = GroqLLM()
    if not groq_llm.validate():
        raise ValueError("Groq LLM is not properly configured.")
    
    # Get the LLM instance
    llm = groq_llm.get_llm(temperature=temperature, max_tokens=max_tokens)
    
    # Get the prompt template
    prompt = get_blog_prompt()
    
    # Create and return the chain
    return LLMChain(llm=llm, prompt=prompt, verbose=False)
