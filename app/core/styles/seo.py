"""
SEO-optimized content writing style.

This style focuses on search engine optimization with clear structure,
keyword emphasis, and scannable content.
"""

from app.core.styles.base import ContentStyle


class SEOStyle(ContentStyle):
    """
    SEO-optimized writing style for maximum search visibility.
    
    This style emphasizes:
    - Search intent alignment
    - Clear, keyword-rich headings
    - Structured, scannable content
    - Strategic keyword placement
    - Strong meta-worthy introductions
    """
    
    def get_instruction(self) -> str:
        """
        Return SEO-focused writing instructions.
        
        Returns:
            str: Detailed SEO writing guidelines.
        """
        return """
🎯 CONTENT STYLE: SEO-OPTIMIZED

hese guidelines affect HOW the content is written.
They do NOT change who is speaking, the authorship, or the identity.
The author's voice and signature must be preserved.

Apply the following SEO writing principles:

STRUCTURE:
- Use clear, descriptive headings with relevant keywords
- Break content into scannable sections (H2, H3 headings)
- Keep paragraphs short (2-4 sentences maximum)
- Use bullet points and numbered lists for easy scanning
- Include a strong, keyword-rich introduction

KEYWORD STRATEGY:
- Naturally incorporate primary and secondary keywords
- Use semantic variations and related terms
- Place keywords in headings, first paragraph, and throughout content
- Avoid keyword stuffing - maintain natural flow

CONTENT APPROACH:
- Focus on search intent and user questions
- Provide comprehensive, authoritative answers
- Include actionable insights and practical examples
- Use clear, direct language
- Add relevant statistics or data when appropriate

READABILITY:
- Write for 8th-grade reading level
- Use active voice
- Keep sentences concise and clear
- Use transition words for smooth flow
- End with a clear conclusion or call-to-action

Remember: Balance SEO optimization with genuine value for readers.
"""
