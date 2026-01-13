"""
Image generation orchestration chain.

This module orchestrates the end-to-end process of enriching content with images:
1. Analyze content to extract topics
2. Generate appropriate image prompts
3. Call image providers to obtain images
4. Return structured image assets

No UI logic or LLM logic should be here - pure orchestration.
"""

from typing import List, Optional
import logging

from app.core.images.models import ImageAsset
from app.core.images.factory import ImageProviderFactory
from app.core.images.context import generate_prompts_for_content, generate_image_prompt

logger = logging.getLogger(__name__)


def generate_images_for_content(
    content: str,
    num_images: int = 1,
    provider: str = "external",
    include_cover: bool = True,
    style: Optional[str] = None
) -> List[ImageAsset]:
    """
    Generate or retrieve images to enrich content.
    
    This function orchestrates the complete workflow:
    1. Extract topics from content
    2. Generate appropriate image prompts
    3. Use specified provider to obtain images
    4. Return list of ImageAsset objects
    
    Args:
        content: The text content to generate images for.
        num_images: Number of images to generate.
        provider: Image provider to use ("huggingface", "external").
        include_cover: Whether to include a cover image.
        style: Optional visual style hint ("professional", "creative", "minimal").
    
    Returns:
        List[ImageAsset]: List of generated/retrieved images with metadata.
    
    Raises:
        ValueError: If provider is not supported or content is empty.
        Exception: If image generation fails.
    
    Example:
        >>> content = "# AI in Healthcare\\n\\nAI is transforming medicine..."
        >>> assets = generate_images_for_content(
        ...     content=content,
        ...     num_images=2,
        ...     provider="external"
        ... )
        >>> for asset in assets:
        ...     print(f"{asset.placement}: {asset.source}")
    """
    # Validate input
    if not content or not content.strip():
        raise ValueError("Content cannot be empty")
    
    # Validate provider
    if not ImageProviderFactory.is_provider_supported(provider):
        supported = ", ".join(ImageProviderFactory.get_supported_providers())
        raise ValueError(
            f"Unsupported image provider: '{provider}'. "
            f"Supported providers: {supported}"
        )
    
    # Create provider instance
    image_provider = ImageProviderFactory.create_provider(provider)
    
    # Validate provider is configured
    if not image_provider.validate():
        raise ValueError(
            f"Image provider '{provider}' is not properly configured. "
            f"Please check required environment variables and API keys."
        )
    
    # Generate prompts from content
    prompt_data = generate_prompts_for_content(
        content=content,
        num_images=num_images,
        include_cover=include_cover
    )
    
    # Generate images for each prompt
    images = []
    
    for prompt_dict in prompt_data:
        try:
            # Generate/retrieve image
            asset = image_provider.generate(
                prompt=prompt_dict["prompt"],
                placement=prompt_dict["placement"]
            )
            
            # Override alt_text with our suggestion if provider didn't set it
            if not asset.alt_text:
                asset.alt_text = prompt_dict["alt_text"]
            
            images.append(asset)
        
        except Exception as e:
            # Log error but continue with other images
            logger.error(f"Failed to generate image for prompt '{prompt_dict['prompt']}': {str(e)}")
            # Optionally continue or raise depending on strictness
            continue
    
    return images


def generate_single_image(
    prompt: str,
    provider: str = "external",
    placement: str = "cover",
    **kwargs
) -> ImageAsset:
    """
    Generate a single image from a direct prompt.
    
    This is a simpler interface for generating one image without content analysis.
    
    Args:
        prompt: Direct image prompt or search query.
        provider: Image provider to use.
        placement: Where the image will be used.
        **kwargs: Additional provider-specific parameters.
    
    Returns:
        ImageAsset: The generated/retrieved image.
    
    Raises:
        ValueError: If provider is not supported or prompt is empty.
        Exception: If image generation fails.
    
    Example:
        >>> asset = generate_single_image(
        ...     prompt="futuristic city at night",
        ...     provider="huggingface",
        ...     placement="cover"
        ... )
        >>> print(asset.source)
    """
    # Validate input
    if not prompt or not prompt.strip():
        raise ValueError("Image prompt cannot be empty")
    
    # Validate provider
    if not ImageProviderFactory.is_provider_supported(provider):
        supported = ", ".join(ImageProviderFactory.get_supported_providers())
        raise ValueError(
            f"Unsupported image provider: '{provider}'. "
            f"Supported providers: {supported}"
        )
    
    # Create provider instance
    image_provider = ImageProviderFactory.create_provider(provider)
    
    # Validate provider is configured
    if not image_provider.validate():
        raise ValueError(
            f"Image provider '{provider}' is not properly configured. "
            f"Please check required environment variables and API keys."
        )
    
    # Generate image
    asset = image_provider.generate(
        prompt=prompt,
        placement=placement,
        **kwargs
    )
    
    return asset


def get_available_providers() -> List[str]:
    """
    Get list of image providers that are currently available and configured.
    
    This checks each provider's configuration and returns only those that
    are ready to use.
    
    Returns:
        List[str]: List of available provider names.
    
    Example:
        >>> available = get_available_providers()
        >>> if available:
        ...     print(f"Available providers: {', '.join(available)}")
        ... else:
        ...     print("No image providers configured")
    """
    return ImageProviderFactory.get_available_providers()


def validate_provider(provider: str) -> bool:
    """
    Check if a specific provider is available and properly configured.
    
    Args:
        provider: Provider name to validate.
    
    Returns:
        bool: True if provider is available and ready, False otherwise.
    
    Example:
        >>> if validate_provider("huggingface"):
        ...     print("HuggingFace is ready")
        ... else:
        ...     print("HuggingFace not configured")
    """
    try:
        image_provider = ImageProviderFactory.create_provider(provider)
        return image_provider.validate()
    except Exception:
        return False
