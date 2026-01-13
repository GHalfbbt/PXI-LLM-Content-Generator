"""
Context extraction for image generation.

This module provides functions to derive meaningful image prompts from
generated content. It analyzes text to extract topics, themes, and concepts
that can be used to generate or search for relevant images.

No API calls are made here - this is pure text analysis.
"""

import re
from typing import List, Optional, Dict


def extract_main_topic(content: str, max_words: int = 5) -> str:
    """
    Extract the main topic from content text.
    
    This function attempts to identify the primary subject or theme of the
    content by analyzing the first few paragraphs and extracting key phrases.
    
    Args:
        content: The full text content to analyze.
        max_words: Maximum number of words in the extracted topic.
    
    Returns:
        str: A concise topic phrase suitable for image search/generation.
             Example: "artificial intelligence future"
    
    Example:
        >>> content = "# The Future of AI\\n\\nArtificial intelligence is..."
        >>> topic = extract_main_topic(content)
        >>> print(topic)
        "artificial intelligence future"
    """
    if not content or not content.strip():
        return "abstract concept"
    
    # Remove markdown formatting
    clean_content = _remove_markdown(content)
    
    # Try to extract from title (first line or H1)
    lines = clean_content.split('\n')
    title = lines[0].strip() if lines else ""
    
    if title:
        # Clean and truncate title
        words = title.split()[:max_words]
        return ' '.join(words).lower()
    
    # Fallback: extract from first paragraph
    paragraphs = [p.strip() for p in clean_content.split('\n\n') if p.strip()]
    if paragraphs:
        first_para = paragraphs[0]
        words = first_para.split()[:max_words]
        return ' '.join(words).lower()
    
    return "abstract concept"


def extract_section_topics(content: str) -> List[str]:
    """
    Extract topics for each major section in the content.
    
    This function identifies section headers (H2, H3) and extracts them
    as individual topics. This is useful for generating section-specific images.
    
    Args:
        content: The full text content with markdown formatting.
    
    Returns:
        List[str]: List of section topics, one per major section.
    
    Example:
        >>> content = "# Main\\n\\n## AI Ethics\\n...\\n## Future Trends\\n..."
        >>> topics = extract_section_topics(content)
        >>> print(topics)
        ['ai ethics', 'future trends']
    """
    topics = []
    
    # Find markdown headers (## or ###)
    header_pattern = r'^#{2,3}\s+(.+)$'
    
    for line in content.split('\n'):
        match = re.match(header_pattern, line.strip())
        if match:
            topic = match.group(1).strip().lower()
            # Remove markdown formatting from topic
            topic = _remove_markdown(topic)
            topics.append(topic)
    
    return topics


def generate_image_prompt(
    content: str,
    placement: str = "cover",
    style: Optional[str] = None
) -> str:
    """
    Generate a descriptive image prompt from content.
    
    This function creates a detailed prompt suitable for AI image generation
    or stock photo search, based on the content's topic and the desired
    placement.
    
    Args:
        content: The text content to analyze.
        placement: Where the image will be placed ("cover", "section", "inline").
                  This affects the prompt style and details.
        style: Optional visual style hint ("professional", "creative", "minimal").
    
    Returns:
        str: A detailed image generation prompt.
    
    Example:
        >>> content = "# AI in Healthcare\\n\\nArtificial intelligence..."
        >>> prompt = generate_image_prompt(content, placement="cover")
        >>> print(prompt)
        "modern healthcare technology with artificial intelligence, professional..."
    """
    # Extract main topic
    topic = extract_main_topic(content, max_words=4)
    
    # Build prompt based on placement
    if placement == "cover":
        # Cover images should be broad and eye-catching
        base_prompt = f"modern {topic}, professional photography"
        
        if style == "creative":
            base_prompt += ", artistic composition, vibrant colors"
        elif style == "minimal":
            base_prompt += ", minimalist design, clean background"
        else:
            base_prompt += ", high quality, detailed"
    
    elif placement == "section":
        # Section images should be more specific
        base_prompt = f"{topic}, illustration"
        
        if style == "creative":
            base_prompt += ", colorful, engaging"
        elif style == "minimal":
            base_prompt += ", simple, clean lines"
        else:
            base_prompt += ", clear, professional"
    
    else:  # inline or other
        # Inline images should be simple and focused
        base_prompt = f"{topic}, icon or symbol"
        
        if style == "creative":
            base_prompt += ", creative design"
        elif style == "minimal":
            base_prompt += ", minimal style"
        else:
            base_prompt += ", professional"
    
    return base_prompt


def generate_prompts_for_content(
    content: str,
    num_images: int = 1,
    include_cover: bool = True
) -> List[Dict[str, str]]:
    """
    Generate multiple image prompts for a piece of content.
    
    This function analyzes content and generates appropriate prompts for
    multiple images - typically a cover image plus section images.
    
    Args:
        content: The full text content.
        num_images: Total number of image prompts to generate.
        include_cover: Whether to include a cover image prompt.
    
    Returns:
        List[Dict[str, str]]: List of prompt dictionaries with keys:
                              - "prompt": The image generation prompt
                              - "placement": Where to place the image
                              - "alt_text": Suggested alt text
    
    Example:
        >>> content = "# AI Guide\\n\\n## Ethics\\n...\\n## Future\\n..."
        >>> prompts = generate_prompts_for_content(content, num_images=3)
        >>> for p in prompts:
        ...     print(f"{p['placement']}: {p['prompt']}")
        cover: modern ai guide, professional photography
        section: ethics, illustration
        section: future, illustration
    """
    prompts = []
    
    # Generate cover image prompt if requested
    if include_cover:
        main_topic = extract_main_topic(content)
        cover_prompt = generate_image_prompt(content, placement="cover")
        
        prompts.append({
            "prompt": cover_prompt,
            "placement": "cover",
            "alt_text": f"Cover image for {main_topic}"
        })
    
    # Generate section image prompts
    section_topics = extract_section_topics(content)
    remaining_slots = num_images - len(prompts)
    
    for i, topic in enumerate(section_topics[:remaining_slots]):
        section_prompt = f"{topic}, professional illustration, clear and engaging"
        
        prompts.append({
            "prompt": section_prompt,
            "placement": "section",
            "alt_text": f"Illustration for {topic}"
        })
    
    # If we still need more prompts, use the main topic
    while len(prompts) < num_images:
        main_topic = extract_main_topic(content)
        generic_prompt = f"{main_topic}, visual representation"
        
        prompts.append({
            "prompt": generic_prompt,
            "placement": "inline",
            "alt_text": f"Image related to {main_topic}"
        })
    
    return prompts[:num_images]


def _remove_markdown(text: str) -> str:
    """
    Remove markdown formatting from text.
    
    Args:
        text: Text with markdown formatting.
    
    Returns:
        str: Plain text without markdown.
    """
    # Remove headers
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    
    # Remove bold and italic
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'__(.+?)__', r'\1', text)
    text = re.sub(r'_(.+?)_', r'\1', text)
    
    # Remove links but keep text
    text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
    
    # Remove inline code
    text = re.sub(r'`(.+?)`', r'\1', text)
    
    return text.strip()
