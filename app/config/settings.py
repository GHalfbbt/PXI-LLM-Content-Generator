"""
Configuration settings for the LLM Content Generator application.

This module centralizes all configuration values including API keys,
model settings, and environment variables.
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
# This ensures that env vars are available when this module is imported
load_dotenv()


# ============================================================================
# LLM PROVIDER SETTINGS
# ============================================================================

# Groq API configuration - using high-performance open-source models provided by Groq
GROQ_API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
GROQ_MODEL_NAME: str = os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

# Default temperature for text generation (0.0 = deterministic, 1.0 = creative)
DEFAULT_TEMPERATURE: float = 0.7

# Maximum number of tokens to generate in a single completion
DEFAULT_MAX_TOKENS: int = 2048


# ============================================================================
# APPLICATION SETTINGS
# ============================================================================

# Application title displayed in the UI
APP_TITLE: str = "AI Content Generator"

# Supported content platforms
SUPPORTED_PLATFORMS: list[str] = ["blog", "linkedin", "twitter", "instagram"]


# ============================================================================
# VALIDATION
# ============================================================================

def validate_config() -> None:
    """
    Validate that at least one LLM provider is properly configured.
    
    Checks that either Groq (cloud) or Ollama (local) is available.
    At least one provider must be configured for the application to work.
    
    Raises:
        ValueError: If no LLM provider is properly configured.
    """
    # Check if Groq is configured
    groq_available = bool(GROQ_API_KEY)
    
    # Check if Ollama is configured (it's always available if installed locally)
    ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL_NAME", "llama3.2")
    ollama_available = bool(ollama_base_url and ollama_model)
    
    # At least one provider must be available
    if not groq_available and not ollama_available:
        raise ValueError(
            "No LLM provider is configured. "
            "Please configure either Groq (set GROQ_API_KEY) or Ollama (ensure it's installed and running)."
        )
    
    # Log which providers are available (optional, for debugging)
    available_providers = []
    if groq_available:
        available_providers.append("Groq")
    if ollama_available:
        available_providers.append("Ollama")
    
    # Note: We don't raise an error here, just log which providers are available
    # The UI will show both options, and runtime errors will be handled gracefully
