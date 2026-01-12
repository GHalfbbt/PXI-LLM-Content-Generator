"""
Identity management module for personalized content generation.

This module provides tools to inject identity information (person or company)
into all generated content in a clean, reusable, and platform-agnostic way.
"""

from app.core.identity.profile import IdentityProfile
from app.core.identity.context import build_identity_context

__all__ = [
    "IdentityProfile",
    "build_identity_context",
]
