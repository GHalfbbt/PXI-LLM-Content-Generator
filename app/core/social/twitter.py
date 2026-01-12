"""
Twitter (X) adapter for platform-specific content generation.

This module implements the Twitter adapter that transforms blog content
into concise, impactful tweets.
"""

from typing import Dict
from langchain_core.prompts import PromptTemplate

from app.core.social.base import SocialAdapter
from app.core.prompts.twitter import get_twitter_prompt


class TwitterAdapter(SocialAdapter):
    """
    Twitter (X) platform adapter.
    
    Transforms blog content into Twitter-optimized posts with strict
    character limits and high-impact messaging.
    
    Platform characteristics:
    - Extreme brevity required (280 characters)
    - Fast-paced, attention-grabbing
    - Minimal hashtags
    - Direct value proposition
    
    Example:
        >>> adapter = TwitterAdapter()
        >>> prompt = adapter.get_prompt()
        >>> constraints = adapter.get_constraints()
    """
    
    platform = "twitter"
    
    def get_prompt(self) -> PromptTemplate:
        """
        Return the Twitter-specific prompt template.
        
        This prompt is optimized for extreme conciseness and impact
        within Twitter's character constraints.
        
        Returns:
            PromptTemplate: Twitter prompt template from prompts module.
        """
        return get_twitter_prompt()
    
    def get_constraints(self) -> Dict[str, any]:
        """
        Return Twitter platform constraints and guidelines.
        
        Returns:
            Dict[str, any]: Dictionary containing:
                - max_length: Strict 280 character limit
                - tone: Concise and punchy
                - hashtags: Maximum count (1-2)
                - emojis: Usage guidelines (minimal)
                - hook: Requirement (strong)
        """
        return {
            "max_length": 280,
            "strict_limit": True,
            "tone": "concise_punchy",
            "hashtags": {
                "min": 1,
                "max": 2,
                "placement": "integrated"
            },
            "emojis": "minimal_or_none",
            "hook": "required_strong",
            "value": "immediate",
            "line_breaks": "optional_for_impact"
        }
