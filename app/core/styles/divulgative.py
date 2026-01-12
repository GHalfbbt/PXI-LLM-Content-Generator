"""
Divulgative (educational/explanatory) content writing style.

This style focuses on making complex topics accessible through
clear explanations and educational approach.
"""

from app.core.styles.base import ContentStyle


class DivulgativeStyle(ContentStyle):
    """
    Divulgative writing style for educational content.
    
    This style emphasizes:
    - Clear, accessible explanations
    - Avoiding jargon or explaining technical terms
    - Educational approach
    - Building understanding step-by-step
    """
    
    def get_instruction(self) -> str:
        """
        Return divulgative writing instructions.
        
        Returns:
            str: Detailed educational writing guidelines.
        """
        return """
📚  WRITING GUIDELINES — DIVULGATIVE (EDUCATIONAL STYLE)

These guidelines affect HOW the content is explained.
They do NOT change who is speaking or the authorship of the content.

Apply the following divulgative writing principles:

LANGUAGE:
- Use clear, accessible language
- Avoid technical jargon whenever possible
- When technical terms are necessary, explain them immediately
- Write as if teaching someone new to the topic
- Use analogies and examples to clarify concepts

STRUCTURE:
- Build understanding progressively (simple to complex)
- Start with foundational concepts before advanced ideas
- Use clear topic sentences to introduce each section
- Provide context and background information
- Summarize key points regularly

EXPLANATION APPROACH:
- Break down complex ideas into simpler components
- Use the "what, why, how" framework
- Include real-world examples and practical applications
- Anticipate and answer reader questions
- Connect new concepts to familiar ideas

TONE:
- Informative but conversational
- Patient and encouraging
- Enthusiastic about sharing knowledge
- Respectful of reader's learning journey
- Avoid condescension or oversimplification

Remember: The goal is to educate and empower readers with clear understanding.
"""
