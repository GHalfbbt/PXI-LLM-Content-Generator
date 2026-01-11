"""
Groq LLM integration using LangChain.

This module implements the BaseLLM interface for the Groq API,
which provides fast inference for open-source LLMs.
"""

from typing import Optional
from langchain_groq import ChatGroq

from app.llms.base import BaseLLM
from app.config import settings


class GroqLLM(BaseLLM):
    """
    Groq LLM implementation using LangChain's ChatGroq.
    
    This class wraps the Groq API to provide fast inference for content generation
    using high-performance open-source models provided by Groq. It follows the BaseLLM interface to ensure
    consistency with other LLM providers.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """
        Initialize the Groq LLM with API credentials and model selection.
        
        Args:
            api_key: Groq API key. If not provided, reads from settings/environment.
            model_name: Name of the Groq model to use. 
        """
        # Use provided values or fall back to configuration settings
        super().__init__(
            api_key=api_key or settings.GROQ_API_KEY,
            model_name=model_name or settings.GROQ_MODEL_NAME
        )
    
    def get_llm(
        self,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> ChatGroq:
        """
        Create and return a configured ChatGroq instance.
        
        This method instantiates a LangChain ChatGroq object configured with
        the specified parameters for content generation.
        
        Args:
            temperature: Controls randomness (0.0 = deterministic, 1.0 = creative).
                        Default is 0.7 for balanced creativity.
            max_tokens: Maximum number of tokens to generate in the response.
                       Default is 2048 tokens.
        
        Returns:
            ChatGroq: A configured LangChain ChatGroq instance ready for use.
        
        Raises:
            ValueError: If API key is missing or invalid.
        """
        # Validate that we have an API key before attempting to create the LLM
        if not self.api_key:
            raise ValueError(
                "Groq API key is required. Set GROQ_API_KEY environment variable "
                "or provide it during initialization."
            )
        
        # Create and configure the ChatGroq instance with specified parameters
        llm = ChatGroq(
            api_key=self.api_key,
            model_name=self.model_name,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        return llm
    
    def validate(self) -> bool:
        """
        Validate that the Groq LLM is properly configured.
        
        This method checks if the API key is present and valid. It performs
        a basic validation without making an actual API call.
        
        Returns:
            bool: True if the LLM appears to be properly configured, False otherwise.
        """
        # Check if API key exists and is not empty
        if not self.api_key or len(self.api_key.strip()) == 0:
            return False
        
        # Check if model name is specified
        if not self.model_name:
            return False
        
        # Basic validation passed
        return True
    
    def __repr__(self) -> str:
        """
        Return a string representation of the GroqLLM instance.
        
        Returns:
            str: String representation showing the model name (API key hidden for security).
        """
        # Hide API key for security, only show model name
        api_key_preview = f"{self.api_key[:8]}..." if self.api_key else "None"
        return f"GroqLLM(model={self.model_name}, api_key={api_key_preview})"
