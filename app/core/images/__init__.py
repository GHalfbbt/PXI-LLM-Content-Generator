"""
Image generation and retrieval module.

This module provides a complete system for enriching generated content with images.
It supports both AI-generated images (via Hugging Face) and stock photo retrieval
(via Unsplash/Pexels).

Public API:
    - ImageAsset: Data model for image metadata
    - ImageProvider: Abstract interface for image providers
    - ImageProviderFactory: Factory for creating provider instances
    - generate_images_for_content: Main function for content enrichment
    - generate_single_image: Simple function for single image generation

Usage Example:
    >>> from app.core.images import generate_images_for_content
    >>> 
    >>> content = "# AI in Healthcare\\n\\nArtificial intelligence..."
    >>> images = generate_images_for_content(
    ...     content=content,
    ...     num_images=2,
    ...     provider="external"
    ... )
    >>> 
    >>> for img in images:
    ...     print(f"{img.placement}: {img.source}")
"""

from app.core.images.models import ImageAsset
from app.core.images.base import ImageProvider
from app.core.images.factory import ImageProviderFactory
from app.core.images.huggingface import HuggingFaceImageProvider
from app.core.images.external import ExternalImageProvider

# Import orchestration functions from chains
from app.core.chains.image_chain import (
    generate_images_for_content,
    generate_single_image,
    get_available_providers,
    validate_provider
)

__all__ = [
    # Data models
    "ImageAsset",
    
    # Base classes
    "ImageProvider",
    
    # Concrete providers
    "HuggingFaceImageProvider",
    "ExternalImageProvider",
    
    # Factory
    "ImageProviderFactory",
    
    # Orchestration functions
    "generate_images_for_content",
    "generate_single_image",
    "get_available_providers",
    "validate_provider",
]
