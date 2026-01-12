"""
Social media content generation chain using LangChain.

This module orchestrates the transformation of blog content into
platform-specific social media posts using the adapter pattern
and LangChain LCEL composition.
"""

from typing import Optional

from app.core.social.factory import SocialAdapterFactory
from app.core.identity import IdentityProfile, build_identity_context
from app.core.styles import StyleFactory
from app.llms.factory import LLMFactory
from app.config import settings


# ============================================================================
# SOCIAL MEDIA CONTENT GENERATION CHAIN
# ============================================================================

def generate_social_post(
    blog_content: str,
    platform: str,
    language: str = "English",
    llm_provider: str = "groq",
    temperature: float = None,
    max_tokens: int = None,
    identity: Optional[IdentityProfile] = None,
    style: str = "default"
) -> str:
    """
    Generate a platform-specific social media post from a blog article.
    
    This function transforms blog content into optimized social media posts
    for specific platforms (LinkedIn, Twitter, Instagram) using the adapter
    pattern and LangChain LCEL chains.
    
    The generation process:
    1. Validate and instantiate the correct social media adapter
    2. Retrieve platform-specific prompt template
    3. Optionally inject identity context if provided
    4. Initialize the LLM provider via factory
    5. Create LCEL chain (prompt | llm)
    6. Execute chain with blog content and language
    7. Return the generated social post
    
    Args:
        blog_content: The source blog article text to transform.
                     This is the single source of truth.
        platform: Target social media platform. Must be one of:
                 - "linkedin": Professional networking
                 - "twitter": Microblogging (280 chars)
                 - "instagram": Visual storytelling
        language: Language in which to generate the social post.
                 Should match the blog content language for consistency.
                 Defaults to "English".
        llm_provider: LLM provider to use ("groq" or "ollama").
                     Defaults to "groq" for cloud-based generation.
        temperature: Controls randomness in generation (0.0-1.0).
                    Defaults to settings.DEFAULT_TEMPERATURE (0.7).
        max_tokens: Maximum tokens to generate.
                   Defaults to settings.DEFAULT_MAX_TOKENS (2048).
        identity: Identity information to personalize the social post.
        style: Content writing style to apply.
              Options: "default", "seo", "divulgative", "kids".
              Defaults to "default" (no style modification).
                 If provided, the post reflects this identity's voice.
    
    Returns:
        str: The generated social media post, optimized for the target platform.
    
    Raises:
        ValueError: If platform is not supported or LLM provider is invalid.
        Exception: If content generation fails due to API errors.
    
    Example:
        >>> blog = "AI is transforming industries..."
        >>> linkedin_post = generate_social_post(
        ...     blog_content=blog,
        ...     platform="linkedin",
        ...     language="Spanish",
        ...     llm_provider="groq"
        ... )
        >>> print(linkedin_post)
        "🚀 La IA está revolucionando cómo trabajamos..."
    """
    # Use default values from settings if not provided
    if temperature is None:
        temperature = settings.DEFAULT_TEMPERATURE
    if max_tokens is None:
        max_tokens = settings.DEFAULT_MAX_TOKENS
    
    # Step 1: Create the appropriate social media adapter
    # This validates the platform and provides platform-specific prompts
    try:
        adapter = SocialAdapterFactory.create_adapter(platform)
    except ValueError as e:
        raise ValueError(f"Invalid platform: {str(e)}") from e
    
    # Step 2: Get the platform-specific prompt template
    # Each adapter provides its own optimized prompt
    prompt = adapter.get_prompt()
    
    # Step 3: Build the complete prompt with optional enhancements
    # The injection order is: Identity (if provided) -> Style (if not default) -> Platform prompt
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
            print(f"Warning: {str(e)}. Using default style.")
    
    # Third: Add the platform-specific prompt template
    template_parts.append(prompt.template)
    
    # Combine all parts with double newlines for clear separation
    enhanced_template = "\n\n".join(template_parts)
    
    # Create new prompt with enhanced template
    from langchain_core.prompts import PromptTemplate
    prompt = PromptTemplate(
        template=enhanced_template,
        input_variables=["blog_content", "language"]
    )
    
    # Step 4: Initialize the LLM provider using the factory
    # The factory handles Groq/Ollama instantiation and validation
    llm_instance = LLMFactory.create_llm(llm_provider)
    
    # Step 5: Validate that the LLM is properly configured
    if not llm_instance.validate():
        raise ValueError(
            f"{llm_provider.upper()} LLM is not properly configured. "
            f"Please check your environment variables and configuration."
        )
    
    # Step 6: Get the configured LLM instance with specified parameters
    llm = llm_instance.get_llm(
        temperature=temperature,
        max_tokens=max_tokens
    )
    
    # Step 7: Create the LangChain chain using LCEL
    # Modern LangChain uses the pipe operator (|) to chain components
    chain = prompt | llm
    
    # Step 8: Execute the chain with the blog content and language
    try:
        result = chain.invoke({
            "blog_content": blog_content,
            "language": language
        })
        
        # Extract the content from the response
        # The result is an AIMessage object, we need the content string
        if hasattr(result, 'content'):
            content = result.content
        else:
            content = str(result)
        
        # Return the generated social post as a clean string
        return content.strip()
    
    except Exception as e:
        # Catch and re-raise with more context if generation fails
        raise Exception(
            f"Failed to generate {platform} post: {str(e)}"
        ) from e


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_supported_platforms() -> list[str]:
    """
    Get a list of all supported social media platforms.
    
    Returns:
        list[str]: List of supported platform identifiers.
    
    Example:
        >>> platforms = get_supported_platforms()
        >>> print(platforms)
        ['linkedin', 'twitter', 'instagram']
    """
    return SocialAdapterFactory.get_supported_platforms()


def validate_platform(platform: str) -> bool:
    """
    Check if a platform is supported for social media generation.
    
    Args:
        platform: Platform identifier to validate.
    
    Returns:
        bool: True if platform is supported, False otherwise.
    
    Example:
        >>> validate_platform("linkedin")
        True
        >>> validate_platform("facebook")
        False
    """
    return SocialAdapterFactory.is_platform_supported(platform)
