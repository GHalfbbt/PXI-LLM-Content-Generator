"""
Ollama LLM integration using LangChain.

This module implements the BaseLLM interface for Ollama,
which provides local LLM inference without requiring cloud APIs.
"""

from typing import Optional
from langchain_ollama import ChatOllama

from app.llms.base import BaseLLM
import os


class OllamaLLM(BaseLLM):
    """
    Ollama LLM implementation using LangChain's ChatOllama.
    
    This class wraps Ollama for local LLM inference, allowing users to run
    models on their own hardware without cloud dependencies. It follows the
    BaseLLM interface to ensure consistency with other LLM providers.
    
    Ollama must be installed and running locally for this to work.
    Installation: https://ollama.ai/
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize the Ollama LLM with configuration.
        
        Args:
            api_key: Not used for Ollama (local), kept for interface consistency.
            model_name: Name of the Ollama model to use (e.g., 'llama3.2', 'mistral').
                       Defaults to 'llama3.2' if not provided.
            base_url: Base URL for Ollama server. Defaults to 'http://localhost:11434'.
        """
        # Ollama doesn't require an API key (local), but we maintain the interface
        super().__init__(api_key=None, model_name=model_name)
        
        # Set model name with fallback to environment or default
        self.model_name = (
            model_name or 
            os.getenv("OLLAMA_MODEL_NAME", "llama3.2")
        )
        
        # Set base URL with fallback to environment or default
        self.base_url = (
            base_url or 
            os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        )
    
    def get_llm(
        self,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> ChatOllama:
        """
        Create and return a configured ChatOllama instance.
        
        This method instantiates a LangChain ChatOllama object configured with
        the specified parameters for local inference.
        
        Args:
            temperature: Controls randomness in generation (0.0 = deterministic, 1.0 = creative).
                        Default: 0.7 (balanced creativity).
            max_tokens: Maximum number of tokens to generate in the response.
                       Default: 2048 tokens (~1500 words).
        
        Returns:
            ChatOllama: A configured Ollama chat model instance ready for use with LangChain.
        
        Raises:
            ConnectionError: If Ollama server is not running or not accessible.
        
        Example:
            >>> ollama = OllamaLLM(model_name="llama3.2")
            >>> llm = ollama.get_llm(temperature=0.7, max_tokens=2048)
            >>> response = llm.invoke("Write a short story")
        """
        # Create and configure the ChatOllama instance
        llm = ChatOllama(
            model=self.model_name,
            base_url=self.base_url,
            temperature=temperature,
            num_predict=max_tokens,  # Ollama uses 'num_predict' instead of 'max_tokens'
        )
        
        return llm
    
    def validate(self) -> bool:
        """
        Validate that Ollama is properly configured.
        
        This method only checks configuration, NOT connectivity.
        Actual connectivity errors are handled gracefully at runtime.
        
        Checks:
        1. Base URL is configured
        2. Model name is configured
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        
        Note:
            This method does NOT make network calls or test connectivity.
            Runtime errors (Ollama not running, model not downloaded) are
            handled by try/except blocks in the calling code.
        
        Example:
            >>> ollama = OllamaLLM()
            >>> if ollama.validate():
            ...     llm = ollama.get_llm()
            ... else:
            ...     print("Ollama configuration is invalid")
        """
        # Only validate configuration, not connectivity
        if not self.model_name:
            return False
        
        if not self.base_url:
            return False
        
        return True
    
    def __repr__(self) -> str:
        """
        String representation of the OllamaLLM instance.
        
        Returns:
            str: A string describing this Ollama LLM configuration.
        """
        return f"OllamaLLM(model='{self.model_name}', base_url='{self.base_url}')"
