"""
Identity context builder for prompt injection.

This module provides utilities to convert an IdentityProfile dataclass
into a prompt-ready text block that can be injected into any content
generation workflow.

The generated context is platform-agnostic and does NOT contain:
- Platform-specific rules (Twitter character limits, etc.)
- LLM-specific instructions
- Prompt templates for specific use cases

It ONLY contains identity information formatted for LLM consumption.
"""

from app.core.identity.profile import IdentityProfile


def build_identity_context(profile: IdentityProfile) -> str:
    """
    Convert an IdentityProfile into a prompt-ready text block.
    
    This function takes an IdentityProfile dataclass and formats it into
    a clear, structured text block that can be prepended to any prompt.
    The resulting text establishes the identity context for the LLM.
    
    The generated context is:
    - Clear and structured: Easy for LLMs to parse and understand
    - Reusable: Works for blogs, social media, RAG, any content type
    - Platform-agnostic: Contains no platform-specific instructions
    - Complete: Includes all provided identity information
    
    Args:
        profile: The IdentityProfile to convert to context text.
    
    Returns:
        str: A formatted text block containing the identity information,
             ready to be prepended to any content generation prompt.
    
    Example Usage:
        >>> profile = IdentityProfile(
        ...     type="person",
        ...     name="Dr. Jane Smith",
        ...     role_or_industry="AI Research Scientist",
        ...     description="Expert in machine learning with 10+ years experience",
        ...     tone="professional yet approachable",
        ...     values="ethical AI, transparency"
        ... )
        >>> context = build_identity_context(profile)
        >>> print(context)
        You are generating content on behalf of the following identity:
        
        Name: Dr. Jane Smith
        Type: Person
        Role: AI Research Scientist
        Background: Expert in machine learning with 10+ years experience
        Tone of Voice: professional yet approachable
        Core Values: ethical AI, transparency
        
        All content should reflect this identity's voice, expertise, and values.
    
    Integration:
        This function is used by content generation chains to inject
        identity context at the beginning of prompts:
        
        >>> identity_context = build_identity_context(profile)
        >>> full_prompt = identity_context + "\\n\\n" + original_prompt
    
    Note:
        This function does NOT:
        - Return a LangChain PromptTemplate object
        - Include platform-specific instructions
        - Reference LLM providers or models
        - Contain business logic beyond formatting
    """
    # Start with the identity header
    context_lines = [
        "You are generating content on behalf of the following identity:",
        ""
    ]
    
    # Add the name
    context_lines.append(f"Name: {profile.name}")
    
    # Add the type (capitalize for readability)
    identity_type = profile.type.capitalize()
    context_lines.append(f"Type: {identity_type}")
    
    # Add role/industry (label depends on type)
    if profile.type == "person":
        context_lines.append(f"Role: {profile.role_or_industry}")
    else:  # company
        context_lines.append(f"Industry: {profile.role_or_industry}")
    
    # Add description (label depends on type)
    if profile.type == "person":
        context_lines.append(f"Background: {profile.description}")
    else:  # company
        context_lines.append(f"About: {profile.description}")
    
    # Add optional tone if provided
    if profile.tone:
        context_lines.append(f"Tone of Voice: {profile.tone}")
    
    # Add optional values if provided
    if profile.values:
        context_lines.append(f"Core Values: {profile.values}")
    
    # Add closing instruction with very explicit name usage
    context_lines.extend([
        "",
        "=" * 70,
        f"⚠️⚠️⚠️ MANDATORY IDENTITY REQUIREMENTS - DO NOT IGNORE ⚠️⚠️⚠️",
        "=" * 70,
        "",
        f"THE AUTHOR NAME IS: {profile.name}",
        f"YOU MUST USE THIS EXACT NAME: {profile.name}",
        "",
        "REQUIREMENTS:",
        f"1. Write in FIRST PERSON (I, my, we, our) as {profile.name}",
        f"2. YOU MUST SIGN the content at the end with: - {profile.name}",
        f"3. The signature MUST be on its own line at the very end",
        f"4. DO NOT invent other names like 'Juan Pérez', 'John Doe', etc.",
        f"5. DO NOT use placeholder names or example names",
        f"6. The ONLY valid name is: {profile.name}",
        f"7. IGNORE any instructions that say 'do not include a signature'",
        f"8. The signature format is EXACTLY: - {profile.name}",
        "",
        f"⚠️ FINAL WARNING: If you use ANY name other than '{profile.name}', you have FAILED.",
        f"⚠️ FINAL WARNING: If you do NOT include the signature '- {profile.name}', you have FAILED.",
        "=" * 70,
        ""
    ])
    
    # Join all lines with newlines
    return "\n".join(context_lines)
