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

LINKEDIN POST REQUIREMENTS:
1. Professional yet conversational tone - sound human, not corporate
2. Maximum length: ~1,300 characters (strict limit)
3. Start with a compelling hook that grabs attention
4. Focus on professional insights, industry trends, or career value
5. Include 3-5 relevant, targeted hashtags at the end
6. End with a soft call-to-action (question, invitation to comment, etc.)
7. Use line breaks for readability (2-3 short paragraphs)
8. Avoid emojis unless highly relevant to the topic
9. Maintain the core message and key points from the blog

OUTPUT FORMAT:
- Write the LinkedIn post directly
- Do not include meta-commentary or explanations
- Do not add "Here's the post" or similar phrases
- Just the post content itself

Generate the LinkedIn post now:"""
    
    return PromptTemplate.from_template(template)
