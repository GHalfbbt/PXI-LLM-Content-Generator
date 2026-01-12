"""
Instagram adapter for platform-specific content generation.

This module implements the Instagram adapter that transforms blog content
into emotional, visually-focused captions.
"""

from typing import Dict
from langchain_core.prompts import PromptTemplate

from app.core.social.base import SocialAdapter
from app.core.prompts.instagram import get_instagram_prompt


class InstagramAdapter(SocialAdapter):
    """
    Instagram platform adapter.
    
    Transforms blog content into Instagram-optimized captions with
    emotional storytelling and visual appeal.
    
    Platform characteristics:
    - Visual-first platform
    - Emotional and authentic tone
    - Story-driven content
    - Heavy hashtag usage for discovery
    
    Example:
        >>> adapter = InstagramAdapter()
        >>> prompt = adapter.get_prompt()
        >>> constraints = adapter.get_constraints()
    """
    
    platform = "instagram"
    
    def get_prompt(self) -> PromptTemplate:
        """
        Return the Instagram-specific prompt template.
        
        This prompt is optimized for emotional storytelling and
        mobile-friendly formatting with visual context.
        
        Returns:
            PromptTemplate: Instagram prompt template from prompts module.
        """
        return get_instagram_prompt()
    
    def get_constraints(self) -> Dict[str, any]:
        """
        Return Instagram platform constraints and guidelines.
        
        Returns:
            Dict[str, any]: Dictionary containing:
                - max_length: Maximum caption length (2,200)
                - tone: Emotional and storytelling
                - hashtags: Recommended count (5-10)
                - emojis: Usage guidelines (encouraged)
                - call_to_action: Type (strong)
        """
        return {
            "max_length": 2200,
            "recommended_length": 1500,
            "tone": "emotional_storytelling",
            "hashtags": {
                "min": 5,
                "max": 10,
                "placement": "end_grouped"
            },
            "emojis": "encouraged_natural",
            "call_to_action": "strong",
            "line_breaks": "required_mobile_friendly",
            "hook": "stop_scrolling",
            "authenticity": "high"
        }
