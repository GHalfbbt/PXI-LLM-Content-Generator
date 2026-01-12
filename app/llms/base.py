"""
Base interface for Language Model integrations.

This module defines the abstract base class that all LLM implementations
must follow. It ensures a consistent interface across different LLM providers
(Groq, Ollama, etc.).
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseLLM(ABC):
    """
    Abstract base class for all LLM implementations.
    
    This class defines the interface that all LLM providers must implement.
    It ensures consistency and allows easy swapping between different providers.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the LLM with optional API key and model name.
        
        Args:
            api_key: API key for the LLM provider (if required).
            model_name: Name of the specific model to use.
        """
        self.api_key = api_key
        self.model_name = model_name
    
    @abstractmethod
    def get_llm(self, temperature: float = 0.7, max_tokens: int = 2048):
        """
        Return the configured LLM instance ready for use with LangChain.
        
        This method must be implemented by each LLM provider to return
        a LangChain-compatible LLM object configured with the specified parameters.
        
        Args:
            temperature: Controls randomness in generation (0.0 = deterministic, 1.0 = creative).
            max_tokens: Maximum number of tokens to generate.
            
        Returns:
            A LangChain-compatible LLM instance.
            
        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """
        raise NotImplementedError("Subclasses must implement get_llm()")
    
    @abstractmethod
    def validate(self) -> bool:
        """
        Validate that the LLM is properly configured and accessible.
        
        This method should check if all required credentials are present
        and if the LLM provider is reachable.
        
        Returns:
            True if the LLM is properly configured and accessible, False otherwise.
            
        Raises:
            NotImplementedError: If the subclass doesn't implement this method.
        """
        raise NotImplementedError("Subclasses must implement validate()")
