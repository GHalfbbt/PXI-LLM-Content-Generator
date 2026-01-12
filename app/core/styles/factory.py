"""
Factory for creating content writing style instances.

This module provides a centralized way to create and retrieve
content style objects based on style identifiers.
"""

from app.core.styles.base import ContentStyle
from app.core.styles.seo import SEOStyle
from app.core.styles.divulgative import DivulgativeStyle
from app.core.styles.kids import KidsStyle


class DefaultStyle(ContentStyle):
    """
    Default style with no special instructions.
    
    This style returns an empty instruction, allowing the base prompt
    to determine the writing style without additional constraints.
    """
    
    def get_instruction(self) -> str:
        """
        Return empty instruction for default style.
        
        Returns:
            str: Empty string (no style modification).
        """
        return ""


class StyleFactory:
    """
    Factory class for creating content style instances.
    
    This factory manages the available content styles and provides
    a simple interface for retrieving style objects by name.
    
    Supported styles:
    - "default": No style modification (empty instruction)
    - "seo": SEO-optimized content
    - "divulgative": Educational/explanatory content
    - "kids": Kid-friendly content (ages 6-10)
    """
    
    # Mapping of style names to style classes
    _STYLE_MAP = {
        "default": DefaultStyle,
        "seo": SEOStyle,
        "divulgative": DivulgativeStyle,
        "kids": KidsStyle,
    }
    
    @classmethod
    def create_style(cls, style_name: str) -> ContentStyle:
        """
        Create and return a content style instance.
        
        Args:
            style_name: Name of the style to create.
                       Must be one of: "default", "seo", "divulgative", "kids"
        
        Returns:
            ContentStyle: Instance of the requested style.
        
        Raises:
            ValueError: If style_name is not supported.
        
        Example:
            >>> style = StyleFactory.create_style("seo")
            >>> instruction = style.get_instruction()
        """
        style_name = style_name.lower().strip()
        
        if style_name not in cls._STYLE_MAP:
            supported = ", ".join(f"'{s}'" for s in cls._STYLE_MAP.keys())
            raise ValueError(
                f"Unsupported content style: '{style_name}'. "
                f"Supported styles are: {supported}"
            )
        
        style_class = cls._STYLE_MAP[style_name]
        return style_class()
    
    @classmethod
    def get_supported_styles(cls) -> list[str]:
        """
        Get a list of all supported style names.
        
        Returns:
            list[str]: List of supported style identifiers.
        
        Example:
            >>> styles = StyleFactory.get_supported_styles()
            >>> print(styles)
            ['default', 'seo', 'divulgative', 'kids']
        """
        return list(cls._STYLE_MAP.keys())
    
    @classmethod
    def is_style_supported(cls, style_name: str) -> bool:
        """
        Check if a style name is supported.
        
        Args:
            style_name: Style name to check.
        
        Returns:
            bool: True if style is supported, False otherwise.
        
        Example:
            >>> StyleFactory.is_style_supported("seo")
            True
            >>> StyleFactory.is_style_supported("academic")
            False
        """
        return style_name.lower().strip() in cls._STYLE_MAP
