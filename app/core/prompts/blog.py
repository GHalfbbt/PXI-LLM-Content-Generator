"""
Prompt template for blog content generation.

This module defines the base PromptTemplate used to generate
long-form blog content adapted to a specific topic, audience,
tone, and language using LangChain.
"""

from langchain.prompts import PromptTemplate


# ============================================================================
# BLOG CONTENT GENERATION PROMPT
# ============================================================================

def get_blog_prompt() -> PromptTemplate:
    """
    Create and return the PromptTemplate for blog content generation.
    
    This function returns a carefully crafted prompt that instructs the LLM
    to generate high-quality blog posts with proper structure, SEO considerations,
    and audience-appropriate language.

    The generated content will be:
    - Well-structured with clear headings and sections
    - Engaging and informative
    - Adapted to the target audience and tone
    - Written in the specified language
    - Ready to be published as a blog post

    Input Variables:
        topic (str): The main subject or theme of the blog post.
        audience (str): Target audience (e.g., "developers", "beginners", "business professionals").
        tone (str): Writing tone (e.g., "professional", "casual", "friendly", "technical").
        language (str): Language for the content (e.g., "English", "Spanish").

    Returns:
        PromptTemplate: LangChain prompt template configured for blog generation.
    """
    # Define the template string with clear instructions and formatting
    template = """You are a professional content writer and digital marketing expert specializing in creating engaging blog content.

Your task is to write a comprehensive, well-structured blog post based on the following parameters:

📌 CONTENT PARAMETERS:
- Topic: {topic}
- Target Audience: {audience}
- Tone: {tone}
- Language: {language}

📝 WRITING GUIDELINES:
1. Structure: Create a clear hierarchy with an introduction, well-organized body sections, and a conclusion
2. Headings: Use descriptive headings and subheadings to organize content
3. Paragraphs: Keep paragraphs short (3-5 sentences) for better readability
4. Engagement: Write in an engaging style that captures and maintains reader interest
5. Value: Provide actionable insights, practical examples, or useful information
6. Audience Adaptation: Adjust language complexity and terminology to match the target audience
7. Tone Consistency: Maintain the specified tone throughout the entire post
8. Language: Write entirely in {language}

⚠️ IMPORTANT:
- Avoid filler content and generic statements
- Do NOT include meta-commentary like "Here is your blog post" or "I hope this helps"
- Start directly with the blog post content (title or introduction)
- Ensure the content is publication-ready

Now, write the blog post:"""

    # Create and return the PromptTemplate with defined input variables
    return PromptTemplate(
        input_variables=[
            "topic",      # Main subject of the blog post
            "audience",   # Target readers/demographic
            "tone",       # Writing style and voice
            "language",   # Language for content generation
        ],
        template=template
    )
    
