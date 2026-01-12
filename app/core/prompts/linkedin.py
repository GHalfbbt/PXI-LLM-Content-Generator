"""
LinkedIn post generation prompt template.

This module defines the prompt template for transforming blog content
into professional, engaging LinkedIn posts.
"""

from langchain_core.prompts import PromptTemplate


def get_linkedin_prompt() -> PromptTemplate:
    """
    Create and return the LinkedIn post generation prompt template.
    
    This prompt transforms blog content into LinkedIn-optimized posts
    following platform best practices and constraints.
    
    Platform-specific rules enforced by this prompt:
    - Professional yet human tone
    - Maximum ~1,300 characters
    - 3-5 relevant hashtags
    - Soft call-to-action
    - Engaging hook in first line
    - Industry/professional focus
    
    Returns:
        PromptTemplate: Configured prompt template for LinkedIn posts.
    
    Example:
        >>> prompt = get_linkedin_prompt()
        >>> chain = prompt | llm
        >>> result = chain.invoke({"blog_content": "..."})
    """
    
    template = """You are an expert LinkedIn content strategist specializing in professional social media posts.

Your task is to transform the following blog article into an engaging LinkedIn post that follows platform best practices.

BLOG ARTICLE:
{blog_content}

⚠️ CRITICAL REQUIREMENT - LANGUAGE:
YOU MUST write the ENTIRE LinkedIn post in {language}. This is NON-NEGOTIABLE.
- Every word, hashtag, and call-to-action MUST be in {language}
- Do NOT write in English if {language} is not English
- Maintain natural, native-speaker fluency in {language}

LINKEDIN POST REQUIREMENTS:
1. Professional yet conversational tone - sound human, not corporate
2. Maximum length: ~1,300 characters (strict limit)
3. Start with a compelling hook that grabs attention
4. Focus on professional insights, industry trends, or career value
5. Include 3-5 relevant, targeted hashtags at the end (in {language})
6. End with a soft call-to-action (question, invitation to comment, etc.) in {language}
7. Use line breaks for readability (2-3 short paragraphs)
8. Avoid emojis unless highly relevant to the topic
9. Maintain the core message and key points from the blog

⚠️ CRITICAL - AUTHOR IDENTITY:
- If an author name is provided in the identity context above, YOU MUST use that EXACT name
- Sign the post with the provided name (e.g., "- [Exact Name]")
- DO NOT invent names like "Juan Pérez", "John Doe", or any placeholder names
- DO NOT make up author names - only use the name explicitly provided
- If no name is provided, do not include a signature

OUTPUT FORMAT:
- Write the LinkedIn post directly
- Do not include meta-commentary or explanations
- Do not add "Here's the post" or similar phrases
- Just the post content itself

Generate the LinkedIn post now IN {language}:"""
    
    return PromptTemplate.from_template(template)
