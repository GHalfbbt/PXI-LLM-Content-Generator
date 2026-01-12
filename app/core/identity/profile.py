"""
Identity profile data structure for personalized content generation.

This module defines the IdentityProfile dataclass, which represents
the identity information of a person or company that content is being
generated for or on behalf of.

The IdentityProfile is WHO is speaking - not HOW or WHERE the content
is generated. It is designed to be platform-agnostic and reusable across
all content generation workflows (blogs, social media, RAG, etc.).
"""

from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class IdentityProfile:
    """
    Represents the identity of a person or company for content generation.
    
    This dataclass encapsulates all the information needed to personalize
    content generation by injecting identity context into prompts. It allows
    the generated content to reflect the voice, values, and characteristics
    of a specific person or organization.
    
    The IdentityProfile is designed to be:
    - Platform-agnostic: Works for blogs, social media, RAG, etc.
    - Reusable: Can be shared across multiple content generation requests
    - Optional: Content generation works with or without identity
    - Clean: Simple data structure with no business logic
    
    Attributes:
        type: Whether this is a "person" or "company" identity.
              This helps tailor the content generation approach.
        
        name: The full name of the person or company.
              Examples: "Jane Smith", "Acme Corporation"
        
        role_or_industry: For persons, their role or job title.
                         For companies, their industry or sector.
                         Examples: "Senior Data Scientist", "FinTech", "Healthcare"
        
        description: A brief description of the person or company.
                    This should capture their background, expertise, or mission.
                    Examples: "10+ years in AI/ML with focus on NLP",
                             "Leading provider of cloud-based solutions"
        
        tone: Optional. The preferred tone of voice for content.
              Examples: "friendly and approachable", "professional and formal",
                       "technical and precise", "inspiring and motivational"
              If None, the content generation will use default tone settings.
        
        values: Optional. Core values or principles to reflect in content.
               Examples: "innovation, transparency, user-first",
                        "sustainability, ethical AI, inclusivity"
               If None, no specific values will be emphasized.
    
    Usage Examples:
        
        Example 1 - Personal identity:
        >>> profile = IdentityProfile(
        ...     type="person",
        ...     name="Dr. Sarah Johnson",
        ...     role_or_industry="AI Research Scientist",
        ...     description="PhD in Computer Science, specializing in neural networks "
        ...                 "with 15 years of experience in deep learning research.",
        ...     tone="technical yet accessible",
        ...     values="open science, ethical AI, reproducible research"
        ... )
        
        Example 2 - Company identity:
        >>> profile = IdentityProfile(
        ...     type="company",
        ...     name="TechFlow Solutions",
        ...     role_or_industry="SaaS / Enterprise Software",
        ...     description="Cloud-native platform helping enterprises streamline "
        ...                 "their digital transformation journey.",
        ...     tone="professional and solution-oriented",
        ...     values="customer success, innovation, reliability"
        ... )
        
        Example 3 - Minimal identity (no optional fields):
        >>> profile = IdentityProfile(
        ...     type="person",
        ...     name="Alex Chen",
        ...     role_or_industry="Software Engineer",
        ...     description="Full-stack developer passionate about clean code."
        ... )
    
    Integration:
        The IdentityProfile is converted to prompt context using the
        build_identity_context() function from app.core.identity.context.
        This context is then injected into content generation chains.
    
    Note:
        This dataclass contains NO business logic, prompt formatting,
        or LLM integration. It is purely a data structure. All identity
        context formatting happens in the identity.context module.
    """
    
    type: Literal["person", "company"]
    name: str
    role_or_industry: str
    description: str
    tone: Optional[str] = None
    values: Optional[str] = None
    
    def __post_init__(self):
        """
        Validate the identity profile fields after initialization.
        
        Raises:
            ValueError: If required fields are empty or invalid.
        """
        if not self.name or not self.name.strip():
            raise ValueError("Identity name cannot be empty")
        
        if not self.role_or_industry or not self.role_or_industry.strip():
            raise ValueError("Identity role_or_industry cannot be empty")
        
        if not self.description or not self.description.strip():
            raise ValueError("Identity description cannot be empty")
        
        if self.type not in ("person", "company"):
            raise ValueError(f"Identity type must be 'person' or 'company', got: {self.type}")
