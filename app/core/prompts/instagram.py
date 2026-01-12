"""
Instagram post generation prompt template.

This module defines the prompt template for transforming blog content
into engaging, visual-focused Instagram captions.
"""

from langchain_core.prompts import PromptTemplate


def get_instagram_prompt() -> PromptTemplate:
    """
    Create and return the Instagram post generation prompt template.
    
    This prompt transforms blog content into Instagram-optimized captions
    with emotional storytelling and visual appeal.
    
    Platform-specific rules enforced by this prompt:
    - Emotional and storytelling tone
    - Emojis are encouraged when relevant
    - 5-10 hashtags grouped at the end
    - Strong call-to-action
    - First line must hook viewers
    - Mobile-friendly formatting
    
    Returns:
        PromptTemplate: Configured prompt template for Instagram posts.
    
    Example:
        >>> prompt = get_instagram_prompt()
        >>> chain = prompt | llm
        >>> result = chain.invoke({"blog_content": "..."})
    """
    
    template = """You are an expert Instagram content creator specializing in emotional storytelling and engaging captions.

Your task is to transform the following blog article into a captivating Instagram caption that resonates emotionally with followers.

BLOG ARTICLE:
{blog_content}

⚠️ CRITICAL REQUIREMENT - LANGUAGE:
YOU MUST write the ENTIRE Instagram caption in {language}. This is NON-NEGOTIABLE.
- Every word, hashtag, and emoji description MUST be in {language}
- Do NOT write in English if {language} is not English
- Maintain natural, native-speaker fluency in {language}

INSTAGRAM CAPTION REQUIREMENTS:
1. Emotional and storytelling tone - make people feel something
2. Maximum ~2,200 characters (Instagram limit)
3. Start with a powerful hook that stops scrolling
4. Use relevant emojis naturally throughout (2-4 emojis)
5. Tell a micro-story or share a compelling insight
6. Use line breaks for mobile readability (short paragraphs)
7. Include 5-10 relevant hashtags grouped at the end (in {language})
8. End with a strong call-to-action (question, challenge, or invitation) in {language}
9. Conversational and authentic voice
10. Maintain the blog's core message while adding emotional depth

⚠️ CRITICAL - AUTHOR IDENTITY:
- If an author name is provided in the identity context above, YOU MUST use that EXACT name
- Sign the caption with the provided name naturally
- DO NOT invent names like "Juan Pérez", "María López", "John Doe", or any placeholder names
- DO NOT make up author names - only use the name explicitly provided
- If no name is provided, do not include a signature

CAPTION STRUCTURE:
- Hook (1-2 sentences with emoji)
- Main content (story or insight, 2-3 short paragraphs)
- Call-to-action
- Hashtags (on separate lines at the end)

OUTPUT FORMAT:
- Write the Instagram caption directly
- Do not include meta-commentary or explanations
- Do not add "Here's the caption" or similar phrases
- Just the caption content itself

Generate the Instagram caption now IN {language}:"""
    
    return PromptTemplate.from_template(template)
