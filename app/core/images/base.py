"""
Abstract base class for image providers.

This module defines the interface that all image provider implementations
must follow. It ensures consistency across different image generation and
retrieval services.
"""

from abc import ABC, abstractmethod
from typing import Optional
import logging

from app.core.images.models import ImageAsset

logger = logging.getLogger(__name__)


class ImageProvider(ABC):
    """
    Abstract interface for image generation and retrieval services.
    
    This base class defines the contract that all image providers must
    implement. It supports both AI-generated images (like Stable Diffusion)
    and external image sources (like Unsplash, Pexels).
    
    Implementations should handle:
    - Configuration and authentication
    - API communication
    - Error handling and retries
    - Response parsing and validation
    
    The interface is intentionally minimal to support diverse providers
    while maintaining a consistent API for consumers.
    """
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        placement: Optional[str] = None,
        **kwargs
    ) -> ImageAsset:
        """
        Generate or retrieve an image based on a text prompt.
        
        This method should either generate a new image using AI models
        or search for an existing image from external sources, depending
        on the provider implementation.
        
        Args:
            prompt: Text description or search query for the image.
                   Should be clear and descriptive.
                   Example: "modern office workspace with natural lighting"
            
            placement: Optional hint for where the image will be used.
                      Common values: "cover", "section", "inline"
                      Providers may adjust image dimensions or style based on this.
            
            **kwargs: Additional provider-specific parameters.
                     Examples:
                     - width, height: Image dimensions
                     - style: Art style or image type
                     - num_results: Number of candidates to consider
        
        Returns:
            ImageAsset: The generated or retrieved image asset with all metadata.
        
        Raises:
            ValueError: If the prompt is invalid or empty.
            ConnectionError: If the provider service is unreachable.
            Exception: For other provider-specific errors.
        
        Example:
            >>> provider = SomeImageProvider()
            >>> asset = provider.generate(
            ...     prompt="sunset over mountains",
            ...     placement="cover",
            ...     width=1200,
            ...     height=630
            ... )
            >>> print(asset.source)
            "https://example.com/generated/img_123.jpg"
        """
        pass
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate that the provider is properly configured and accessible.
        
        This method checks that:
        - Required credentials/API keys are present
        - The service endpoint is reachable
        - The provider is ready to handle requests
        
        This should be called before attempting to generate images to
        provide early feedback about configuration issues.
        
        Returns:
            bool: True if provider is properly configured and ready,
                  False otherwise.
        
        Example:
            >>> provider = SomeImageProvider()
            >>> if provider.validate():
            ...     asset = provider.generate("test image")
            ... else:
            ...     print("Provider not configured correctly")
        """
        pass
    
    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        Get the name of this provider.
        
        Returns:
            str: Provider name (e.g., "huggingface", "external").
        
        Example:
            >>> provider = SomeImageProvider()
            >>> print(provider.provider_name)
            "huggingface"
        """
        pass
    
    def supports_generation(self) -> bool:
        """
        Check if this provider supports AI-based image generation.
        
        Returns:
            bool: True if provider can generate images, False if it only searches.
        """
        # Default implementation - subclasses should override if needed
        return True
    
    def supports_search(self) -> bool:
        """
        Check if this provider supports searching existing images.
        
        Returns:
            bool: True if provider can search images, False if it only generates.
        """
        # Default implementation - subclasses should override if needed
        return False
