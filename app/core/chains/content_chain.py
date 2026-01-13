"""
Content generation chain using LangChain.

This module orchestrates the content generation pipeline by combining
the prompt template with the LLM provider to create a complete chain
that generates blog posts based on user inputs.
"""

from typing import Optional
import logging

from app.core.prompts.blog import get_blog_prompt
from app.core.identity import IdentityProfile, build_identity_context
from app.core.styles import StyleFactory
from app.llms.factory import LLMFactory
from app.config import settings

logger = logging.getLogger(__name__)


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
    identity: Optional[IdentityProfile] = None,
    style: str = "default",
    include_images: bool = False,
    image_provider: str = "external",
    num_images: int = 2
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
        style (str, optional): Content writing style to apply.
                              Options: "default", "seo", "divulgative", "kids".
                              Defaults to "default" (no style modification).
                              If provided, content reflects this identity's voice.
        include_images (bool, optional): Whether to generate and inject images.
                                        Defaults to False.
        image_provider (str, optional): Image provider to use ("huggingface", "external").
                                       Defaults to "external".
        num_images (int, optional): Number of images to generate.
                                   Defaults to 2 (1 cover + 1 section).
    
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
    # This template defines the structure and requirements for blog generation
    prompt = get_blog_prompt()
    
    # Step 5: Build the complete prompt with optional enhancements
    # The injection order is: Identity (if provided) -> Style (if not default) -> Base prompt
    template_parts = []
    
    # First: Add identity context if provided (highest priority)
    if identity:
        identity_context = build_identity_context(identity)
        template_parts.append(identity_context)
    
    # Second: Add style instruction if not default
    if style != "default":
        try:
            style_instance = StyleFactory.create_style(style)
            style_instruction = style_instance.get_instruction()
            if style_instruction:  # Only add if non-empty
                template_parts.append(style_instruction)
        except ValueError as e:
            # If invalid style, log warning but continue with default
            # This prevents breaking generation due to invalid style
            logger.warning(f"{str(e)}. Using default style.")
    
    # Third: Add the base prompt template
    template_parts.append(prompt.template)
    
    # Combine all parts with double newlines for clear separation
    enhanced_template = "\n\n".join(template_parts)
    
    # Create new prompt with enhanced template
    from langchain_core.prompts import PromptTemplate
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
        
        # Clean the generated content
        content = content.strip()
        
        # Step 8: Optionally generate and inject images
        if include_images:
            try:
                from app.core.chains.image_chain import generate_images_for_content
                from app.core.images.integrator import inject_images_into_blog
                
                # Generate images based on content
                images = generate_images_for_content(
                    content=content,
                    num_images=num_images,
                    provider=image_provider,
                    include_cover=True
                )
                
                # Inject images into content
                if images:
                    content = inject_images_into_blog(content, images)
                    logger.info(f"Injected {len(images)} images into blog content")
                else:
                    logger.warning("No images generated, returning content without images")
            
            except Exception as img_error:
                # Log error but don't fail the entire generation
                logger.error(f"Failed to generate/inject images: {str(img_error)}")
                # Return content without images
        
        # Return the generated content (with or without images)
        return content
    
    except Exception as e:
        # Catch and re-raise with more context if generation fails
        raise Exception(f"Failed to generate blog content: {str(e)}") from e
