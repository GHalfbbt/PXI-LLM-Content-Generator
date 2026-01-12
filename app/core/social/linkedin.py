"""
LinkedIn adapter for platform-specific content generation.

This module implements the LinkedIn adapter that transforms blog content
into professional, engaging LinkedIn posts.
"""

from typing import Dict
from langchain_core.prompts import PromptTemplate

from app.core.social.base import SocialAdapter
from app.core.prompts.linkedin import get_linkedin_prompt


class LinkedInAdapter(SocialAdapter):
    """
    LinkedIn platform adapter.
    
    Transforms blog content into LinkedIn-optimized posts following
    professional networking platform best practices.
    
    Platform characteristics:
    - Professional audience
    - Career and industry focus
    - Longer-form content acceptable
    - Hashtag usage important for discovery
    
    Example:
        >>> adapter = LinkedInAdapter()
        >>> prompt = adapter.get_prompt()
        >>> constraints = adapter.get_constraints()
    """
    
    platform = "linkedin"
    
    def get_prompt(self) -> PromptTemplate:
        """
        Return the LinkedIn-specific prompt template.
        
        This prompt is optimized for professional networking content
        with appropriate tone and formatting rules.
        
        Returns:
            PromptTemplate: LinkedIn prompt template from prompts module.
        """
        return get_linkedin_prompt()
    
    def get_constraints(self) -> Dict[str, any]:
        """
        Return LinkedIn platform constraints and guidelines.
        
        Returns:
            Dict[str, any]: Dictionary containing:
                - max_length: Maximum character count (~1,300)
                - tone: Professional yet human
                - hashtags: Recommended count (3-5)
                - call_to_action: Type (soft)
                - line_breaks: Recommended usage
        """
        return {
            "max_length": 1300,
            "recommended_length": 1000,
            "tone": "professional_human",
            "hashtags": {
                "min": 3,
                "max": 5,
                "placement": "end"
            },
            "call_to_action": "soft",
            "emojis": "minimal",
            "line_breaks": "encouraged",
            "focus": "professional_insights"
        }
