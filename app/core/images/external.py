"""
External image source provider.

This module implements image retrieval from external stock photo APIs
like Unsplash and Pexels. It performs keyword-based searches and returns
image URLs with proper attribution.
"""

import os
import requests
from typing import Optional, List, Dict, Any
import uuid
import logging

from app.core.images.base import ImageProvider
from app.core.images.models import ImageAsset

logger = logging.getLogger(__name__)


class ExternalImageProvider(ImageProvider):
    """
    Image provider for external stock photo APIs.
    
    This provider searches for existing images from stock photo services
    like Unsplash and Pexels. It does not generate images, only retrieves
    URLs to existing photos based on keyword searches.
    
    Configuration:
        UNSPLASH_ACCESS_KEY: API key for Unsplash (optional)
                            Get one at: https://unsplash.com/developers
        
        PEXELS_API_KEY: API key for Pexels (optional)
                       Get one at: https://www.pexels.com/api/
        
        Note: At least one API key should be configured. If both are available,
              Unsplash will be tried first, then Pexels as fallback.
    
    Features:
        - Keyword-based image search
        - High-quality stock photos
        - Proper attribution and licensing
        - Automatic fallback between providers
    
    Example:
        >>> provider = ExternalImageProvider(preferred_provider="unsplash")
        >>> if provider.validate():
        ...     asset = provider.generate("mountain landscape")
        ...     print(asset.source)  # HTTPS URL to image
        ...     print(asset.attribution)  # Photo credit
    """
    
    def __init__(self, preferred_provider: Optional[str] = None):
        """
        Initialize the external image provider with environment config.
        
        Args:
            preferred_provider: Optional preferred provider ("unsplash" or "pexels").
                              If not specified or unavailable, will try both with fallback.
        """
        self.unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")
        self.pexels_key = os.getenv("PEXELS_API_KEY")
        self.preferred_provider = preferred_provider
    
    def validate(self) -> bool:
        """
        Validate that at least one external provider is configured.
        
        Returns:
            bool: True if at least one API key is set, False otherwise.
        """
        if not self.unsplash_key and not self.pexels_key:
            logger.warning("No external image API keys configured")
            logger.info("Set UNSPLASH_ACCESS_KEY or PEXELS_API_KEY to enable image search")
            return False
        
        return True
    
    def generate(
        self,
        prompt: str,
        placement: Optional[str] = None,
        **kwargs
    ) -> ImageAsset:
        """
        Search for an image from external sources.
        
        Args:
            prompt: Search keywords for finding images.
            placement: Optional placement hint (may affect image selection).
            **kwargs: Additional parameters:
                     - orientation: "landscape", "portrait", "squarish"
                     - per_page: Number of results to fetch
        
        Returns:
            ImageAsset: Retrieved image with URL and attribution.
        
        Raises:
            ValueError: If prompt is empty or no providers configured.
            ConnectionError: If all API requests fail.
        """
        # Validate input
        if not prompt or not prompt.strip():
            raise ValueError("Image search prompt cannot be empty")
        
        # Validate configuration
        if not self.validate():
            raise ValueError(
                "External image provider not configured. "
                "Please set UNSPLASH_ACCESS_KEY or PEXELS_API_KEY."
            )
        
        # If a specific provider is preferred and available, use it
        if self.preferred_provider == "unsplash" and self.unsplash_key:
            try:
                result = self._search_unsplash(prompt, placement, **kwargs)
                # Explicitly set provider in attribution for clarity
                if "unsplash" not in result.attribution.lower():
                    result.attribution = f"Imagen de Unsplash: {result.attribution}"
                return result
            except Exception as e:
                logger.warning(f"Unsplash search failed: {str(e)}")
                if not self.pexels_key:  # No fallback available
                    raise ConnectionError(f"Failed to retrieve image from Unsplash: {str(e)}")
                logger.info("Falling back to Pexels")
        
        if self.preferred_provider == "pexels" and self.pexels_key:
            try:
                result = self._search_pexels(prompt, placement, **kwargs)
                # Explicitly set provider in attribution for clarity
                if "pexels" not in result.attribution.lower():
                    result.attribution = f"Imagen de Pexels: {result.attribution}"
                return result
            except Exception as e:
                logger.warning(f"Pexels search failed: {str(e)}")
                if not self.unsplash_key:  # No fallback available
                    raise ConnectionError(f"Failed to retrieve image from Pexels: {str(e)}")
                logger.info("Falling back to Unsplash")
        
        # No preference specified or preferred provider unavailable, try both
        # Try Unsplash first
        if self.unsplash_key:
            try:
                result = self._search_unsplash(prompt, placement, **kwargs)
                if "unsplash" not in result.attribution.lower():
                    result.attribution = f"Imagen de Unsplash: {result.attribution}"
                return result
            except Exception as e:
                logger.warning(f"Unsplash search failed: {str(e)}")
                # Continue to try Pexels
        
        # Try Pexels as fallback
        if self.pexels_key:
            try:
                result = self._search_pexels(prompt, placement, **kwargs)
                if "pexels" not in result.attribution.lower():
                    result.attribution = f"Imagen de Pexels: {result.attribution}"
                return result
            except Exception as e:
                logger.warning(f"Pexels search failed: {str(e)}")
                raise ConnectionError(
                    "Failed to retrieve images from all external providers"
                )
        
        raise ConnectionError("No external image providers available")
    
    def _search_unsplash(
        self,
        prompt: str,
        placement: Optional[str] = None,
        **kwargs
    ) -> ImageAsset:
        """
        Search for images on Unsplash.
        
        Args:
            prompt: Search query.
            placement: Placement hint.
            **kwargs: Additional search parameters.
        
        Returns:
            ImageAsset: First matching image from Unsplash.
        """
        url = "https://api.unsplash.com/search/photos"
        
        headers = {
            "Authorization": f"Client-ID {self.unsplash_key}"
        }
        
        params = {
            "query": prompt,
            "per_page": kwargs.get("per_page", 1),
            "orientation": kwargs.get("orientation", "landscape")
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("results"):
            raise ValueError(f"No images found for query: {prompt}")
        
        # Get first result
        photo = data["results"][0]
        
        # Create ImageAsset
        asset = ImageAsset(
            id=f"unsplash_{photo['id']}",
            prompt=prompt,
            provider="external",
            source=photo["urls"]["regular"],
            placement=placement,
            alt_text=photo.get("alt_description") or photo.get("description") or prompt,
            attribution=(
                f"Photo by {photo['user']['name']} on Unsplash "
                f"({photo['links']['html']})"
            )
        )
        
        return asset
    
    def _search_pexels(
        self,
        prompt: str,
        placement: Optional[str] = None,
        **kwargs
    ) -> ImageAsset:
        """
        Search for images on Pexels.
        
        Args:
            prompt: Search query.
            placement: Placement hint.
            **kwargs: Additional search parameters.
        
        Returns:
            ImageAsset: First matching image from Pexels.
        """
        url = "https://api.pexels.com/v1/search"
        
        headers = {
            "Authorization": self.pexels_key
        }
        
        params = {
            "query": prompt,
            "per_page": kwargs.get("per_page", 1),
            "orientation": kwargs.get("orientation", "landscape")
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data.get("photos"):
            raise ValueError(f"No images found for query: {prompt}")
        
        # Get first result
        photo = data["photos"][0]
        
        # Create ImageAsset
        asset = ImageAsset(
            id=f"pexels_{photo['id']}",
            prompt=prompt,
            provider="external",
            source=photo["src"]["large"],
            placement=placement,
            alt_text=photo.get("alt") or prompt,
            attribution=(
                f"Photo by {photo['photographer']} on Pexels "
                f"({photo['url']})"
            )
        )
        
        return asset
    
    @property
    def provider_name(self) -> str:
        """Return the provider name."""
        return "external"
    
    def supports_generation(self) -> bool:
        """This provider does not support AI image generation."""
        return False
    
    def supports_search(self) -> bool:
        """This provider supports image search."""
        return True
