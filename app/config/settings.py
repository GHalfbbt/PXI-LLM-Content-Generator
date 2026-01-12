"""
Configuration settings for the LLM Content Generator application.

This module centralizes all configuration values including API keys,
model settings, and environment variables.
"""

import os
from typing import Optional


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
    Validate that all required configuration values are present.
    
    Raises:
        ValueError: If any required configuration value is missing.
    """
    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY environment variable is not set. "
            "Please set it before running the application."
        )
