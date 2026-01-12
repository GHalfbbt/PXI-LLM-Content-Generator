"""
Base abstract class for content writing styles.

This module defines the interface that all content styles must implement.
Styles define HOW content is written (tone, structure, vocabulary),
independently of the platform.
"""

from abc import ABC, abstractmethod


class ContentStyle(ABC):
    """
    Abstract base class for content writing styles.
    
    A style defines the writing approach, tone, structure, and vocabulary
    to be used when generating content. Styles are platform-independent
    and can be applied to blog posts, social media posts, or any other
    content type.
    """
    
    @abstractmethod
    def get_instruction(self) -> str:
        """
        Return the style instruction to be injected into the prompt.
        
        This instruction guides the LLM on HOW to write the content,
        including tone, structure, vocabulary choices, and formatting.
        
        Returns:
            str: A clear, detailed instruction block for the LLM.
        
        Example:
            >>> style = SEOStyle()
            >>> instruction = style.get_instruction()
            >>> print(instruction)
            "Write in an SEO-optimized style with clear headings..."
        """
        pass
