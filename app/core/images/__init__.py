"""
Image generation and retrieval module.

This module provides a complete system for enriching generated content with images.
It supports both AI-generated images (via Hugging Face) and stock photo retrieval
(via Unsplash/Pexels).

Public API:
    - ImageAsset: Data model for image metadata
    - ImageProvider: Abstract interface for image providers
    - ImageProviderFactory: Factory for creating provider instances
    - Image integration utilities

For orchestration functions, import from app.core.chains.image_chain:
    - generate_images_for_content
    - generate_single_image
    - get_available_providers
    - validate_provider

Usage Example:
    >>> from app.core.images import ImageAsset, ImageProviderFactory
    >>> from app.core.chains.image_chain import generate_images_for_content
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

# Import integration utilities (no circular dependency)
from app.core.images.integrator import (
    inject_images_into_blog,
    prepare_social_image,
    extract_first_image_from_content,
    remove_images_from_content
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
    
    # Integration utilities
    "inject_images_into_blog",
    "prepare_social_image",
    "extract_first_image_from_content",
    "remove_images_from_content",
]
