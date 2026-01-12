"""
LLM Factory for creating LLM provider instances.

This module implements the Factory pattern to centralize LLM instantiation logic.
It provides a clean interface for obtaining LLM instances without coupling
the rest of the application to specific provider implementations.
"""

from typing import Optional

from app.llms.base import BaseLLM
from app.llms.groq_llm import GroqLLM
from app.llms.ollama_llm import OllamaLLM


class LLMFactory:
    """
    Factory class for creating LLM provider instances.
    
    This factory is responsible for instantiating the correct LLM provider
    based on a string identifier. It encapsulates all provider-specific
    instantiation logic, making it the single source of truth for LLM creation.
    
    Supported providers:
    - "groq": Groq cloud API (fast inference)
    - "ollama": Ollama local inference (privacy, no API costs)
    
    Example:
        >>> factory = LLMFactory()
        >>> llm = factory.create_llm(provider="groq")
        >>> # Use llm for content generation...
    """
    
    # Define supported providers for validation
    SUPPORTED_PROVIDERS = ["groq", "ollama"]
    
    @staticmethod
    def create_llm(
        provider: str,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None,
        **kwargs
    ) -> BaseLLM:
        """
        Create and return an LLM instance for the specified provider.
        
        This is the main factory method that handles provider selection and
        instantiation. It ensures that only valid providers are used and
        provides clear error messages for unsupported providers.
        
        Args:
            provider: Name of the LLM provider to use. Must be one of:
                     - "groq": Use Groq cloud API
                     - "ollama": Use Ollama local inference
            api_key: Optional API key for cloud providers (not used by Ollama).
            model_name: Optional model name override.
            **kwargs: Additional provider-specific configuration options.
        
        Returns:
            BaseLLM: An instance of the requested LLM provider.
        
        Raises:
            ValueError: If the provider is not supported.
        
        Example:
            >>> # Create a Groq LLM
            >>> groq_llm = LLMFactory.create_llm("groq")
            >>> 
            >>> # Create an Ollama LLM with custom model
            >>> ollama_llm = LLMFactory.create_llm(
            ...     provider="ollama",
            ...     model_name="mistral"
            ... )
        """
        # Normalize provider name to lowercase for case-insensitive matching
        provider = provider.lower().strip()
        
        # Validate provider
        if provider not in LLMFactory.SUPPORTED_PROVIDERS:
            raise ValueError(
                f"Unsupported LLM provider: '{provider}'. "
                f"Supported providers are: {', '.join(LLMFactory.SUPPORTED_PROVIDERS)}"
            )
        
        # Instantiate the appropriate provider
        if provider == "groq":
            return GroqLLM(api_key=api_key, model_name=model_name)
        
        elif provider == "ollama":
            # Extract Ollama-specific parameters
            base_url = kwargs.get("base_url")
            return OllamaLLM(
                model_name=model_name,
                base_url=base_url
            )
        
        # This should never be reached due to validation above,
        # but included for completeness
        raise ValueError(f"Provider '{provider}' not implemented")
    
    @staticmethod
    def get_supported_providers() -> list[str]:
        """
        Get a list of all supported LLM providers.
        
        Returns:
            list[str]: List of supported provider names.
        
        Example:
            >>> providers = LLMFactory.get_supported_providers()
            >>> print(providers)
            ['groq', 'ollama']
        """
        return LLMFactory.SUPPORTED_PROVIDERS.copy()
    
    @staticmethod
    def is_provider_supported(provider: str) -> bool:
        """
        Check if a provider is supported by the factory.
        
        Args:
            provider: Name of the provider to check.
        
        Returns:
            bool: True if the provider is supported, False otherwise.
        
        Example:
            >>> if LLMFactory.is_provider_supported("groq"):
            ...     print("Groq is supported!")
        """
        return provider.lower().strip() in LLMFactory.SUPPORTED_PROVIDERS
