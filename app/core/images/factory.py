"""
Factory for creating image provider instances.

This module provides centralized access to different image providers,
following the factory pattern. It allows easy switching between providers
and ensures consistent instantiation.
"""

from typing import List

from app.core.images.base import ImageProvider
from app.core.images.huggingface import HuggingFaceImageProvider
from app.core.images.external import ExternalImageProvider
from app.core.images.replicate import ReplicateImageProvider


class ImageProviderFactory:
    """
    Factory for creating image provider instances.
    
    This factory centralizes the creation of image providers and provides
    utility methods for discovering available providers. It follows the
    factory pattern to decouple provider selection from usage.
    
    Supported Providers:
        - "huggingface": AI-powered image generation via Hugging Face
        - "external": Stock photo search via Unsplash/Pexels
        - "replicate": AI-powered image generation via Replicate
    
    Usage Example:
        >>> provider = ImageProviderFactory.create_provider("replicate")
        >>> if provider.validate():
        ...     asset = provider.generate("beautiful sunset")
    """
    
    # Registry of available providers
    _PROVIDERS = {
        "huggingface": HuggingFaceImageProvider,
        "external": ExternalImageProvider,  # Fallback for compatibility
        "unsplash": ExternalImageProvider,
        "pexels": ExternalImageProvider,
        "replicate": ReplicateImageProvider,
    }
    
    @staticmethod
    def create_provider(provider_name: str) -> ImageProvider:
        """
        Create an instance of the specified image provider.
        
        Args:
            provider_name: Name of the provider to create.
                          Must be one of: "huggingface", "external", "unsplash", "pexels", "replicate"
        
        Returns:
            ImageProvider: Initialized provider instance.
        
        Raises:
            ValueError: If provider_name is not supported.
        
        Example:
            >>> provider = ImageProviderFactory.create_provider("replicate")
            >>> print(provider.provider_name)
            "replicate"
        """
        provider_name = provider_name.lower().strip()
        
        if provider_name not in ImageProviderFactory._PROVIDERS:
            supported = ", ".join(ImageProviderFactory._PROVIDERS.keys())
            raise ValueError(
                f"Unsupported image provider: '{provider_name}'. "
                f"Supported providers are: {supported}"
            )
        
        provider_class = ImageProviderFactory._PROVIDERS[provider_name]
        
        # For external providers, pass the preferred provider name
        if provider_name in ["unsplash", "pexels"]:
            return provider_class(preferred_provider=provider_name)
        
        return provider_class()
    
    @staticmethod
    def get_supported_providers() -> List[str]:
        """
        Get a list of all supported provider names.
        
        Returns:
            List[str]: List of provider identifiers.
        
        Example:
            >>> providers = ImageProviderFactory.get_supported_providers()
            >>> print(providers)
            ['huggingface', 'external', 'replicate']
        """
        return list(ImageProviderFactory._PROVIDERS.keys())
    
    @staticmethod
    def is_provider_supported(provider_name: str) -> bool:
        """
        Check if a provider name is supported.
        
        Args:
            provider_name: Provider name to check.
        
        Returns:
            bool: True if supported, False otherwise.
        
        Example:
            >>> ImageProviderFactory.is_provider_supported("huggingface")
            True
            >>> ImageProviderFactory.is_provider_supported("dalle")
            False
        """
        return provider_name.lower().strip() in ImageProviderFactory._PROVIDERS
    
    @staticmethod
    def get_available_providers() -> List[str]:
        """
        Get a list of providers that are actually configured and ready to use.
        
        This checks each provider's validate() method to determine which
        providers have the necessary API keys and configuration.
        
        Returns:
            List[str]: List of provider names that passed validation.
        
        Example:
            >>> available = ImageProviderFactory.get_available_providers()
            >>> if "huggingface" in available:
            ...     print("HuggingFace is ready to use")
        """
        available = []
        
        for provider_name in ImageProviderFactory._PROVIDERS.keys():
            try:
                provider = ImageProviderFactory.create_provider(provider_name)
                if provider.validate():
                    available.append(provider_name)
            except Exception:
                # If provider creation or validation fails, skip it
                continue
        
        return available
