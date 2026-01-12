"""
Content writing styles module.

This module provides different writing styles that define HOW content
is written (tone, structure, vocabulary), independently of platform.

Available styles:
- Default: No style modification
- SEO: Search engine optimized
- Divulgative: Educational/explanatory
- Kids: Kid-friendly (ages 6-10)

Usage:
    from app.core.styles import StyleFactory
    
    style = StyleFactory.create_style("seo")
    instruction = style.get_instruction()
"""

from app.core.styles.base import ContentStyle
from app.core.styles.factory import StyleFactory
from app.core.styles.seo import SEOStyle
from app.core.styles.divulgative import DivulgativeStyle
from app.core.styles.kids import KidsStyle

__all__ = [
    "ContentStyle",
    "StyleFactory",
    "SEOStyle",
    "DivulgativeStyle",
    "KidsStyle",
]
