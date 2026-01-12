"""
Identity prompt utilities for content generation.

This module centralizes the identity prompt structure and provides
utilities for working with identity context in prompt templates.

Purpose:
- Centralize identity context formatting in one place
- Make it easy for chains and adapters to inject identity
- Keep identity logic separate from platform-specific prompts
"""


def get_identity_instruction() -> str:
    """
    Get the standard instruction text for identity-aware content generation.
    
    This instruction is appended to prompts when identity context is provided,
    ensuring the LLM understands how to use the identity information.
    
    Returns:
        str: Standard instruction text for identity-aware generation.
    
    Example:
        >>> instruction = get_identity_instruction()
        >>> print(instruction)
        All content should reflect this identity's voice, expertise, and values.
    """
    return "All content should reflect this identity's voice, expertise, and values."


def format_identity_header(identity_type: str, name: str) -> str:
    """
    Format a header line for identity context.
    
    Args:
        identity_type: Type of identity ("person" or "company")
        name: Name of the person or company
    
    Returns:
        str: Formatted header line
    
    Example:
        >>> header = format_identity_header("person", "Dr. Jane Smith")
        >>> print(header)
        You are generating content on behalf of Dr. Jane Smith (Person).
    """
    return f"You are generating content on behalf of {name} ({identity_type.capitalize()})."


# ============================================================================
# IDENTITY CONTEXT INTEGRATION GUIDELINES
# ============================================================================

"""
How to use identity in your prompts:

1. In content generation chains:
   - Accept Optional[IdentityProfile] parameter
   - Use build_identity_context() to convert to text
   - Prepend identity context to your existing prompt
   
2. In prompt templates:
   - Keep identity context separate from platform rules
   - Don't hardcode identity in templates
   - Let chains inject identity dynamically
   
3. Best practices:
   - Identity context goes FIRST (before any other instructions)
   - Separate identity context from main prompt with blank line
   - Keep identity formatting consistent across all prompts
   
Example integration:
    
    from app.core.identity import IdentityProfile, build_identity_context
    
    def generate_content(topic: str, identity: Optional[IdentityProfile] = None):
        # Build base prompt
        prompt = get_my_prompt_template()
        
        # If identity provided, prepend context
        if identity:
            identity_ctx = build_identity_context(identity)
            full_prompt = identity_ctx + "\\n\\n" + prompt
        else:
            full_prompt = prompt
        
        # Continue with generation...
"""
