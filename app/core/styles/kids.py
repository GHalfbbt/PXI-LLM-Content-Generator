"""
Kid-friendly content writing style.

This style uses very simple language and explanations suitable
for children aged 6-10 years old.
"""

from app.core.styles.base import ContentStyle


class KidsStyle(ContentStyle):
    """
    Kid-friendly writing style for young readers (ages 6-10).
    
    This style emphasizes:
    - Very simple vocabulary
    - Short, clear sentences
    - Friendly, playful tone
    - Concrete examples and familiar concepts
    """
    
    def get_instruction(self) -> str:
        """
        Return kid-friendly writing instructions.
        
        Returns:
            str: Detailed guidelines for writing for children.
        """
        return """
🎈 CONTENT STYLE: KID-FRIENDLY (AGES 6-10)

hese guidelines affect HOW the content is written.
They do NOT change who is speaking, the authorship, or the identity.
The author's voice and signature must be preserved.

Apply the following kid-friendly writing principles:

LANGUAGE:
- Use very simple, everyday words
- Avoid complex vocabulary and technical terms
- If you must use a big word, explain it right away in simple terms
- Use short, clear sentences (10-15 words maximum)
- One idea per sentence

TONE:
- Friendly and warm, like talking to a friend
- Enthusiastic and positive
- Encouraging and supportive
- Playful when appropriate
- Use "you" to speak directly to the reader

EXPLANATIONS:
- Explain everything as if to a curious 8-year-old
- Use comparisons to things kids know (toys, animals, school, family)
- Break down concepts into the simplest possible pieces
- Use concrete examples, not abstract ideas
- Ask questions to engage the reader

STRUCTURE:
- Very short paragraphs (2-3 sentences)
- Use simple lists with clear points
- Include fun facts or interesting details
- Use transition words like "first," "next," "then," "finally"
- Start with something exciting or relatable

THINGS TO AVOID:
- Long, complicated sentences
- Adult concepts without explanation
- Boring or dry language
- Scary or negative examples
- Assuming prior knowledge

Remember: Make it fun, clear, and easy to understand for young minds!
"""
