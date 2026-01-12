"""
Twitter (X) post generation prompt template.

This module defines the prompt template for transforming blog content
into concise, impactful Twitter posts.
"""

from langchain_core.prompts import PromptTemplate


def get_twitter_prompt() -> PromptTemplate:
    """
    Create and return the Twitter post generation prompt template.
    
    This prompt transforms blog content into Twitter-optimized posts
    following platform constraints and best practices.
    
    Platform-specific rules enforced by this prompt:
    - Maximum 280 characters (strict limit)
    - Strong, attention-grabbing hook
    - 1-2 relevant hashtags maximum
    - Concise and punchy language
    - No unnecessary emojis
    - Direct value proposition
    
    Returns:
        PromptTemplate: Configured prompt template for Twitter posts.
    
    Example:
        >>> prompt = get_twitter_prompt()
        >>> chain = prompt | llm
        >>> result = chain.invoke({"blog_content": "..."})
    """
    
    template = """You are an expert Twitter (X) content creator specializing in concise, high-impact tweets.

Your task is to transform the following blog article into a compelling Twitter post that maximizes engagement within character limits.

BLOG ARTICLE:
{blog_content}

TWITTER POST REQUIREMENTS:
1. Maximum length: 280 characters (STRICT LIMIT - count every character)
2. Start with a powerful hook that demands attention
3. Distill the blog's core insight into one punchy statement
4. Use 1-2 relevant hashtags maximum (include in character count)
5. No emojis unless absolutely necessary for context
6. Every word must add value - be ruthlessly concise
7. Can use line breaks for impact if needed
8. Make it quotable and shareable
9. Maintain accuracy to the blog's main point

CHARACTER COUNT VALIDATION:
- Your response must be ≤ 280 characters total
- Count spaces, hashtags, and punctuation
- If the response is longer than 280 characters, you MUST rewrite it.
- Repeat the rewriting process until the final output is ≤ 280 characters.
- Do not output anything longer than 280 characters.

OUTPUT FORMAT:
- Write the tweet directly
- Do not include meta-commentary or explanations
- Do not add "Here's the tweet" or similar phrases
- Just the tweet content itself

Generate the Twitter post now:"""
    
    return PromptTemplate.from_template(template)
