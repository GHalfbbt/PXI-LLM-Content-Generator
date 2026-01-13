"""
Image asset data models.

This module defines the core data structures for representing image assets
in the content generation system. Images can be generated via AI models or
retrieved from external sources.
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class ImageAsset:
    """
    Represents an image asset for content enrichment.
    
    An ImageAsset encapsulates all the information needed to identify,
    retrieve, and use an image within generated content. It supports both
    AI-generated images and externally sourced images.
    
    Attributes:
        id: Unique identifier for this image asset.
            Can be a UUID, filename, or external URL hash.
            Example: "img_123456", "unsplash_abc123"
        
        prompt: The text prompt or search query used to obtain this image.
                For AI generation: "a futuristic city at sunset, digital art"
                For external search: "artificial intelligence technology"
        
        provider: The service or system that provided this image.
                 Supported values: "huggingface", "external", "local"
                 This helps track image sources and attribution.
        
        source: The location where the image can be accessed.
                Can be:
                - URL: "https://example.com/image.jpg"
                - Local path: "images/generated/img_123.png"
                - Data URI: "data:image/png;base64,..."
        
        placement: Optional hint for where this image should appear in content.
                   Common values: "cover", "section", "inline", "gallery"
                   If None, placement is determined by the consumer.
        
        alt_text: Optional accessibility description for the image.
                 Used for screen readers and when images fail to load.
                 If None, the prompt can be used as fallback.
        
        attribution: Optional credit line for the image source.
                    Example: "Photo by John Doe on Unsplash"
                    Required for some external sources, optional for generated.
    
    Usage Examples:
        
        Example 1 - AI-generated image:
        >>> asset = ImageAsset(
        ...     id="gen_789abc",
        ...     prompt="modern office workspace with natural light",
        ...     provider="huggingface",
        ...     source="/static/generated/office_789abc.png",
        ...     placement="cover",
        ...     alt_text="A bright modern office with large windows"
        ... )
        
        Example 2 - External API image:
        >>> asset = ImageAsset(
        ...     id="unsplash_xyz123",
        ...     prompt="artificial intelligence",
        ...     provider="external",
        ...     source="https://images.unsplash.com/photo-xyz123",
        ...     placement="section",
        ...     alt_text="Abstract visualization of AI neural network",
        ...     attribution="Photo by Jane Smith on Unsplash"
        ... )
        
        Example 3 - Local file:
        >>> asset = ImageAsset(
        ...     id="local_logo",
        ...     prompt="company logo",
        ...     provider="local",
        ...     source="assets/logo.png",
        ...     placement="inline"
        ... )
    """
    
    id: str
    prompt: str
    provider: Literal["huggingface", "external", "local"]
    source: str
    placement: Optional[str] = None
    alt_text: Optional[str] = None
    attribution: Optional[str] = None
    
    def __post_init__(self):
        """Validate the image asset after initialization."""
        if not self.id:
            raise ValueError("ImageAsset id cannot be empty")
        if not self.prompt:
            raise ValueError("ImageAsset prompt cannot be empty")
        if not self.source:
            raise ValueError("ImageAsset source cannot be empty")
        if self.provider not in ["huggingface", "external", "local"]:
            raise ValueError(
                f"Invalid provider '{self.provider}'. "
                f"Must be 'huggingface', 'external', or 'local'"
            )
    
    def is_url(self) -> bool:
        """
        Check if the source is a URL.
        
        Returns:
            bool: True if source is an HTTP(S) URL, False otherwise.
        """
        return self.source.startswith(("http://", "https://"))
    
    def is_local_path(self) -> bool:
        """
        Check if the source is a local file path.
        
        Returns:
            bool: True if source is a local path, False otherwise.
        """
        return not self.is_url() and not self.source.startswith("data:")
    
    def is_data_uri(self) -> bool:
        """
        Check if the source is a data URI.
        
        Returns:
            bool: True if source is a data URI, False otherwise.
        """
        return self.source.startswith("data:")
    
    def get_display_name(self) -> str:
        """
        Get a human-readable display name for this image.
        
        Returns:
            str: A friendly name for displaying to users.
        """
        if self.placement:
            return f"{self.placement.capitalize()} image: {self.prompt[:50]}"
        return f"Image: {self.prompt[:50]}"
