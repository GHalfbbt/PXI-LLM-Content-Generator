"""
Content output rendering components for Streamlit.

This module handles the display of generated blog content in the main
area of the Streamlit application. It provides functions to render
content with proper formatting and user-friendly presentation.
"""

import streamlit as st
from typing import Optional


# ============================================================================
# OUTPUT RENDERING
# ============================================================================

def render_output(content: Optional[str]) -> None:
    """
    Render the generated blog content in the main Streamlit area.
    
    This function displays the generated content in a clean, readable format
    using Streamlit components. It handles empty or None content gracefully
    by not rendering anything in those cases.
    
    The content is displayed with:
    - A clear section header indicating successful generation
    - The full content in a text area for easy reading and copying
    - Proper formatting and visual hierarchy
    
    Args:
        content (str, optional): The generated blog post content to display.
                                 If None or empty, nothing will be rendered.
    
    Returns:
        None: This function only renders UI components and doesn't return a value.
    
    Example:
        >>> generated_content = generate_blog_content(...)
        >>> render_output(generated_content)
    """
    # Early return if content is None or empty
    # This prevents rendering empty sections in the UI
    if not content:
        return
    
    # ========================================================================
    # CONTENT DISPLAY SECTION
    # ========================================================================
    
    # Display a success header to indicate content generation completed
    st.subheader("✅ Generated Blog Post")
    
    # Add a brief description or instruction
    st.markdown("Your blog post has been generated successfully. You can read it below or copy it for use.")
    
    # Display the generated content in a text area
    # The text_area component provides:
    # - Scrollable viewing for long content
    # - Built-in copy functionality
    # - Good readability with proper text wrapping
    st.text_area(
        label="Generated Content",
        value=content,
        height=500,  # Set a comfortable height for reading
        disabled=True,  # Make read-only to prevent accidental edits
        label_visibility="collapsed",  # Hide the label since we have a subheader
        key="output_content"
    )
    
    # ========================================================================
    # ADDITIONAL ACTIONS (OPTIONAL)
    # ========================================================================
    
    # Create columns for action buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    
    # Add a copy button hint (the text_area has built-in copy functionality)
    with col1:
        st.caption("📋 Use the text area controls to copy")
    
    # Display character and word count as metadata
    with col2:
        word_count = len(content.split())
        char_count = len(content)
        st.caption(f"📊 {word_count} words · {char_count} characters")


# ============================================================================
# LOADING STATE RENDERING
# ============================================================================

def render_loading_state() -> None:
    """
    Display a loading state while content is being generated.
    
    This function shows a spinner and informative message to provide
    visual feedback to the user during the content generation process.
    Use this function before calling the generation chain to improve UX.
    
    Returns:
        None: This function only renders UI components.
    
    Example:
        >>> render_loading_state()
        >>> content = generate_blog_content(...)
    """
    with st.spinner("🤖 Generating your blog post... This may take a few moments."):
        st.info("The AI is crafting your content based on your specifications.")


# ============================================================================
# ERROR STATE RENDERING
# ============================================================================

def render_error(error_message: str) -> None:
    """
    Display an error message in a user-friendly format.
    
    This function presents error information in a clear, non-technical way
    to help users understand what went wrong and how to fix it.
    
    Args:
        error_message (str): The error message to display.
    
    Returns:
        None: This function only renders UI components.
    
    Example:
        >>> try:
        ...     content = generate_blog_content(...)
        >>> except Exception as e:
        ...     render_error(str(e))
    """
    st.error("❌ Content Generation Failed")
    st.markdown("An error occurred while generating your blog post:")
    st.code(error_message, language=None)
    st.markdown("**Suggestions:**")
    st.markdown("- Check your internet connection")
    st.markdown("- Verify your API key is correctly set in the `.env` file")
    st.markdown("- Try again with different parameters")


# ============================================================================
# EMPTY STATE RENDERING
# ============================================================================

def render_empty_state() -> None:
    """
    Display a friendly empty state when no content has been generated yet.
    
    This function provides guidance to users when they first open the app
    or after clearing previous results. It helps users understand how to
    get started with content generation.
    
    Returns:
        None: This function only renders UI components.
    
    Example:
        >>> if not content_generated:
        ...     render_empty_state()
    """
    # Create a visually appealing empty state
    st.markdown("---")
    
    # Center the empty state message
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🚀 Welcome to AI Content Generator!")
        st.markdown("To get started:")
        st.markdown("1. Fill in the **Topic** and **Target Audience** in the sidebar")
        st.markdown("2. Select your preferred **Tone** and **Language**")
        st.markdown("3. Click the **Generate Blog Post** button")
        st.markdown("")
        st.info("💡 **Tip:** The more specific you are with your inputs, the better the generated content will be!")
