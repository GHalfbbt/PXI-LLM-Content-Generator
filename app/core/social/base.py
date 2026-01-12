"""
Base interface for social media adapters.

This module defines the abstract base class that all platform-specific
adapters must implement, ensuring consistency across platforms.
"""

from abc import ABC, abstractmethod
from typing import Dict
from langchain_core.prompts import PromptTemplate


class SocialAdapter(ABC):
    """
    Abstract base class for social media platform adapters.
    
    Each platform adapter must extend this class and implement methods
    for retrieving the platform-specific prompt and constraints.
    
    Attributes:
        platform (str): The name of the social media platform.
    """
    
    platform: str
    
    @abstractmethod
    def get_prompt(self) -> PromptTemplate:
        """
        Return the LangChain prompt template for this platform.
        
        The prompt must be designed to transform blog content into
        platform-optimized social media posts following specific rules.
        
        Returns:
            PromptTemplate: A LangChain prompt template configured for the platform.
        
        Example:
            >>> adapter = LinkedInAdapter()
            >>> prompt = adapter.get_prompt()
            >>> # Use prompt in LCEL chain
        """
        pass
    
    @abstractmethod
    def get_constraints(self) -> Dict[str, any]:
        """
        Return platform-specific constraints and formatting rules.
        
        Constraints may include character limits, hashtag counts,
        tone guidelines, and other platform-specific requirements.
        
        Returns:
            Dict[str, any]: A dictionary containing platform constraints.
        
        Example:
            >>> adapter = TwitterAdapter()
            >>> constraints = adapter.get_constraints()
            >>> print(constraints['max_length'])
            280
        """
        pass
    
    def __repr__(self) -> str:
        """
        String representation of the adapter.
        
        Returns:
            str: A string identifying the adapter platform.
        """
        return f"{self.__class__.__name__}(platform='{self.platform}')"
