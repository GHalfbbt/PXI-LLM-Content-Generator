"""
Image integration module for content enrichment.

This module provides utilities to inject images into generated content
using appropriate formatting for different content types (markdown for blogs,
metadata for social posts).
"""

import re
from typing import List, Optional, Tuple
import logging

from app.core.images.models import ImageAsset

logger = logging.getLogger(__name__)


def inject_images_into_blog(
    content: str,
    images: List[ImageAsset]
) -> str:
    """
    Inject images into blog content using Markdown syntax.
    
    This function intelligently places images within blog content:
    - Cover images: After the main title (# heading)
    - Section images: After section headers (## headings)
    - Preserves original content structure
    
    Args:
        content: The original blog content in Markdown format.
        images: List of ImageAsset objects to inject.
    
    Returns:
        str: Blog content with images injected in Markdown format.
    
    Example:
        >>> content = "# My Blog\\n\\nIntro text\\n\\n## Section 1\\n\\nContent..."
        >>> images = [ImageAsset(..., placement="cover"), ImageAsset(..., placement="section")]
        >>> enriched = inject_images_into_blog(content, images)
    """
    if not images:
        return content
    
    lines = content.split('\n')
    result_lines = []
    
    # Track which images have been used
    cover_image = _find_image_by_placement(images, "cover")
    section_images = [img for img in images if img.placement == "section"]
    section_image_index = 0
    
    # Track if we've added the cover image
    cover_added = False
    
    for i, line in enumerate(lines):
        result_lines.append(line)
        
        # Check if this is a title (# heading) and we have a cover image
        if not cover_added and cover_image and re.match(r'^#\s+', line):
            # Add cover image after title
            result_lines.append('')
            result_lines.append(_create_markdown_image(cover_image))
            result_lines.append('')
            cover_added = True
        
        # Check if this is a section header (## or ### heading)
        elif re.match(r'^#{2,3}\s+', line):
            # Add section image if available
            if section_image_index < len(section_images):
                result_lines.append('')
                result_lines.append(_create_markdown_image(section_images[section_image_index]))
                result_lines.append('')
                section_image_index += 1
    
    return '\n'.join(result_lines)


def prepare_social_image(
    post_text: str,
    image: Optional[ImageAsset] = None
) -> Tuple[str, Optional[ImageAsset]]:
    """
    Prepare social media post with optional image metadata.
    
    For social media, we do NOT embed images in the text.
    Instead, we return the text and image metadata separately.
    The platform-specific implementation will handle image attachment.
    
    Args:
        post_text: The generated social media post text.
        image: Optional ImageAsset to attach to the post.
    
    Returns:
        Tuple[str, Optional[ImageAsset]]: Post text and image metadata.
    
    Example:
        >>> text = "Check out this amazing article!"
        >>> image = ImageAsset(...)
        >>> post, img = prepare_social_image(text, image)
        >>> # Post remains unchanged, image returned as metadata
    """
    # Social posts should not have Markdown images embedded
    # Return text as-is and image as separate metadata
    return post_text, image


def extract_first_image_from_content(content: str) -> Optional[str]:
    """
    Extract the URL of the first image from Markdown content.
    
    This is useful for creating social media previews from blog posts.
    
    Args:
        content: Markdown content that may contain images.
    
    Returns:
        Optional[str]: URL of the first image found, or None.
    
    Example:
        >>> content = "# Title\\n\\n![alt](https://example.com/img.jpg)\\n\\nText..."
        >>> url = extract_first_image_from_content(content)
        >>> print(url)
        "https://example.com/img.jpg"
    """
    # Match markdown image syntax: ![alt](url)
    pattern = r'!\[.*?\]\((.*?)\)'
    match = re.search(pattern, content)
    
    if match:
        return match.group(1)
    
    return None


def remove_images_from_content(content: str) -> str:
    """
    Remove all Markdown images from content.
    
    Useful when you need plain text without images.
    
    Args:
        content: Markdown content with images.
    
    Returns:
        str: Content with all images removed.
    
    Example:
        >>> content = "Text\\n\\n![alt](url)\\n\\nMore text"
        >>> clean = remove_images_from_content(content)
        >>> print(clean)
        "Text\\n\\nMore text"
    """
    # Remove markdown images
    pattern = r'!\[.*?\]\(.*?\)'
    content = re.sub(pattern, '', content)
    
    # Clean up excessive blank lines
    content = re.sub(r'\n{3,}', '\n\n', content)
    
    return content.strip()


# ============================================================================
# PRIVATE HELPER FUNCTIONS
# ============================================================================

def _find_image_by_placement(images: List[ImageAsset], placement: str) -> Optional[ImageAsset]:
    """
    Find the first image with a specific placement.
    
    Args:
        images: List of ImageAsset objects.
        placement: Placement type to search for.
    
    Returns:
        Optional[ImageAsset]: First matching image, or None.
    """
    for image in images:
        if image.placement == placement:
            return image
    return None


def _create_markdown_image(image: ImageAsset) -> str:
    """
    Create a Markdown image tag from an ImageAsset.
    
    Args:
        image: ImageAsset to convert to Markdown.
    
    Returns:
        str: Markdown image syntax.
    
    Example:
        ![Alt text](image_url)
    """
    alt_text = image.alt_text or image.prompt or "Image"
    
    # Escape special characters in alt text
    alt_text = alt_text.replace('[', '\\[').replace(']', '\\]')
    
    return f"![{alt_text}]({image.source})"


def count_images_in_content(content: str) -> int:
    """
    Count the number of Markdown images in content.
    
    Args:
        content: Markdown content.
    
    Returns:
        int: Number of images found.
    """
    pattern = r'!\[.*?\]\(.*?\)'
    matches = re.findall(pattern, content)
    return len(matches)


def validate_image_integration(content: str, expected_count: int) -> bool:
    """
    Validate that the expected number of images were integrated.
    
    Args:
        content: Enriched content.
        expected_count: Number of images expected.
    
    Returns:
        bool: True if count matches, False otherwise.
    """
    actual_count = count_images_in_content(content)
    
    if actual_count != expected_count:
        logger.warning(
            f"Image integration mismatch: expected {expected_count}, "
            f"found {actual_count}"
        )
        return False
    
    return True
