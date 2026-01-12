"""
Social Adapter Factory for creating platform-specific adapters.

This module implements the Factory pattern to centralize social media
adapter instantiation logic, providing a clean interface without coupling
the application to specific adapter implementations.
"""

from typing import List

from app.core.social.base import SocialAdapter
from app.core.social.linkedin import LinkedInAdapter
from app.core.social.twitter import TwitterAdapter
from app.core.social.instagram import InstagramAdapter


class SocialAdapterFactory:
    """
    Factory class for creating social media platform adapters.
    
    This factory is responsible for instantiating the correct adapter
    based on a platform identifier. It encapsulates all platform-specific
    instantiation logic, making it the single source of truth for adapter creation.
    
    Supported platforms:
    - "linkedin": LinkedIn professional networking
    - "twitter": Twitter (X) microblogging
    - "instagram": Instagram visual storytelling
    
    Example:
        >>> factory = SocialAdapterFactory()
        >>> adapter = factory.create_adapter("linkedin")
        >>> prompt = adapter.get_prompt()
    """
    
    # Define supported platforms for validation
    SUPPORTED_PLATFORMS = ["linkedin", "twitter", "instagram"]
    
    @staticmethod
    def create_adapter(platform: str) -> SocialAdapter:
        """
        Create and return a social media adapter for the specified platform.
        
        This is the main factory method that handles platform selection and
        instantiation. It ensures that only valid platforms are used and
        provides clear error messages for unsupported platforms.
        
        Args:
            platform: Name of the social media platform. Must be one of:
                     - "linkedin": Professional networking platform
                     - "twitter": Microblogging platform (X)
                     - "instagram": Visual content platform
        
        Returns:
            SocialAdapter: An instance of the requested platform adapter.
        
        Raises:
            ValueError: If the platform is not supported.
        
        Example:
            >>> # Create a LinkedIn adapter
            >>> linkedin = SocialAdapterFactory.create_adapter("linkedin")
            >>> 
            >>> # Create a Twitter adapter
            >>> twitter = SocialAdapterFactory.create_adapter("twitter")
        """
        # Normalize platform name to lowercase for case-insensitive matching
        platform = platform.lower().strip()
        
        # Validate platform
        if platform not in SocialAdapterFactory.SUPPORTED_PLATFORMS:
            raise ValueError(
                f"Unsupported social media platform: '{platform}'. "
                f"Supported platforms are: {', '.join(SocialAdapterFactory.SUPPORTED_PLATFORMS)}"
            )
        
        # Instantiate the appropriate adapter
        if platform == "linkedin":
            return LinkedInAdapter()
        
        elif platform == "twitter":
            return TwitterAdapter()
        
        elif platform == "instagram":
            return InstagramAdapter()
        
        # This should never be reached due to validation above,
        # but included for completeness
        raise ValueError(f"Platform '{platform}' not implemented")
    
    @staticmethod
    def get_supported_platforms() -> List[str]:
        """
        Get a list of all supported social media platforms.
        
        Returns:
            List[str]: List of supported platform names.
        
        Example:
            >>> platforms = SocialAdapterFactory.get_supported_platforms()
            >>> print(platforms)
            ['linkedin', 'twitter', 'instagram']
        """
        return SocialAdapterFactory.SUPPORTED_PLATFORMS.copy()
    
    @staticmethod
    def is_platform_supported(platform: str) -> bool:
        """
        Check if a social media platform is supported by the factory.
        
        Args:
            platform: Platform name to check.
        
        Returns:
            bool: True if platform is supported, False otherwise.
        
        Example:
            >>> SocialAdapterFactory.is_platform_supported("linkedin")
            True
            >>> SocialAdapterFactory.is_platform_supported("facebook")
            False
        """
        return platform.lower().strip() in SocialAdapterFactory.SUPPORTED_PLATFORMS
