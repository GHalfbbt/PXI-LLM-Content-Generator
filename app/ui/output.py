"""
Content output rendering components for Streamlit.

This module handles the display of generated blog content in the main
area of the Streamlit application. It provides functions to render
content with proper formatting and user-friendly presentation.
Supports multiple UI languages.
"""

import streamlit as st
from typing import Optional, List, Dict, Any

from app.utils.i18n import get_text


# ============================================================================
# OUTPUT RENDERING
# ============================================================================

def render_output(content: Optional[str], ui_language: str = "English") -> None:
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
        ui_language (str): The UI language for translations. Default is "English".
    
    Returns:
        None: This function only renders UI components and doesn't return a value.
    
    Example:
        >>> generated_content = generate_blog_content(...)
        >>> render_output(generated_content, "Español")
    """
    # Early return if content is None or empty
    # This prevents rendering empty sections in the UI
    if not content:
        return
    
    # ========================================================================
    # CONTENT DISPLAY SECTION
    # ========================================================================
    
    # Display a success header to indicate content generation completed
    st.subheader(get_text("output_header", ui_language))
    
    # Add a brief description or instruction
    st.markdown(get_text("output_description", ui_language))
    
    # Create tabs for different viewing modes
    tab1, tab2 = st.tabs(["📄 Preview", "📋 Markdown"])
    
    with tab1:
        # Display the content with rendered markdown (including images)
        # Check if content has images (markdown image syntax)
        if "![" in content and "](" in content:
            st.info("✨ Content includes images. They are displayed below.")
        
        # Apply custom CSS for better heading spacing
        st.markdown("""
        <style>
        /* Better heading spacing and visual hierarchy */
        .main h1 {
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
            padding-top: 0.5rem !important;
            border-top: 3px solid #3B82F6;
        }
        .main h2 {
            margin-top: 1.5rem !important;
            margin-bottom: 0.75rem !important;
            padding-top: 0.5rem !important;
            border-top: 2px solid #60A5FA;
        }
        .main h3 {
            margin-top: 1rem !important;
            margin-bottom: 0.5rem !important;
        }
        .main p {
            margin-bottom: 1rem !important;
            line-height: 1.6 !important;
        }
        .main ul, .main ol {
            margin-bottom: 1rem !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Render the markdown content with images
        st.markdown(content, unsafe_allow_html=True)
    
    with tab2:
        # Display the raw markdown in a text area for easy copying
        # The text_area component provides:
        # - Scrollable viewing for long content
        # - Built-in copy functionality
        # - Good readability with proper text wrapping
        st.text_area(
            label=get_text("output_label", ui_language),
            value=content,
            height=500,  # Set a comfortable height for reading
            label_visibility="collapsed",  # Hide the label since we have a subheader
            key="output_content"
        )
    
    # ========================================================================
    # ADDITIONAL ACTIONS AND STATISTICS - OUTSIDE TABS
    # ========================================================================
    
    # Add spacing and divider AFTER tabs
    st.markdown("")
    st.divider()
    
    # Display statistics and copy hint in columns
    word_count = len(content.split())
    char_count = len(content)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.info(f"📊 **Statistics:** {word_count:,} words · {char_count:,} characters", icon="📊")
    
    with col2:
        st.success("💡 **Copy text:** Use the 'Markdown' tab above", icon="📋")


# ============================================================================
# SCIENTIFIC SOURCES RENDERING (RAG)
# ============================================================================

def render_scientific_sources(sources: List[Dict[str, str]], ui_language: str = "English") -> None:
    """
    Render the scientific sources used by RAG in a user-friendly format.
    
    This function displays arXiv papers that were used to ground the content
    generation in scientific research. It provides transparency and allows
    users to verify the sources of information.
    
    Only displayed when RAG is enabled and sources are available.
    
    Args:
        sources (List[Dict]): List of source documents with metadata:
                             - title: Paper title
                             - authors: Paper authors
                             - published: Publication date
                             - source: arXiv URL
        ui_language (str): The UI language for translations. Default is "English".
    
    Returns:
        None: This function only renders UI components.
    
    Example:
        >>> sources = [
        ...     {"title": "Quantum Computing", "authors": "Smith, J.", 
        ...      "published": "2024-01-15", "source": "https://arxiv.org/abs/2401.12345"}
        ... ]
        >>> render_scientific_sources(sources, "English")
    """
    # Early return if no sources
    if not sources:
        return
    
    # Display section header
    st.markdown("")
    st.divider()
    st.subheader("📚 Scientific Sources (arXiv)")
    st.markdown("This content is grounded in the following scientific research papers:")
    
    # Display each source in an expandable section
    for idx, source in enumerate(sources, 1):
        with st.expander(f"📄 **{idx}. {source.get('title', 'Untitled')}**", expanded=False):
            # Authors
            authors = source.get('authors', 'Unknown')
            if authors and authors != 'Unknown':
                # Handle list of authors
                if isinstance(authors, list):
                    authors_str = ", ".join(authors)
                else:
                    authors_str = authors
                st.markdown(f"**👥 Authors:** {authors_str}")
            
            # Publication date
            published = source.get('published', 'Unknown')
            if published and published != 'Unknown':
                st.markdown(f"**📅 Published:** {published}")
            
            # arXiv link with button style
            arxiv_url = source.get('source', '#')
            if arxiv_url and arxiv_url != '#':
                st.markdown(f"**🔗 Read on arXiv:** [View Paper]({arxiv_url})")
                st.link_button("📖 Open in arXiv", arxiv_url, use_container_width=True)
                st.markdown(f"[🔗 View on arXiv]({arxiv_url})")
    
    # Add info message
    st.info("ℹ️ These papers were used by the AI to provide scientifically accurate and evidence-based content.", icon="✅")


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

def render_error(error_message: str, ui_language: str = "English") -> None:
    """
    Display an error message in a user-friendly format.
    
    This function presents error information in a clear, non-technical way
    to help users understand what went wrong and how to fix it.
    
    Args:
        error_message (str): The error message to display.
        ui_language (str): The UI language for translations. Default is "English".
    
    Returns:
        None: This function only renders UI components.
    
    Example:
        >>> try:
        ...     content = generate_blog_content(...)
        >>> except Exception as e:
        ...     render_error(str(e), "Français")
    """
    st.error(get_text("error_title", ui_language))
    st.markdown(get_text("error_description", ui_language))
    st.code(error_message, language=None)
    st.markdown(get_text("error_suggestions_title", ui_language))
    st.markdown(get_text("error_suggestion1", ui_language))
    st.markdown(get_text("error_suggestion2", ui_language))
    st.markdown(get_text("error_suggestion3", ui_language))


# ============================================================================
# EMPTY STATE RENDERING
# ============================================================================

def render_empty_state(ui_language: str = "English") -> None:
    """
    Display a friendly empty state when no content has been generated yet.
    
    This function provides guidance to users when they first open the app
    or after clearing previous results. It helps users understand how to
    get started with content generation.
    
    Args:
        ui_language (str): The UI language for translations. Default is "English".
    
    Returns:
        None: This function only renders UI components.
    
    Example:
        >>> if not content_generated:
        ...     render_empty_state("Italiano")
    """
    # Create a visually appealing empty state
    st.markdown("---")
    
    # Center the empty state message
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(get_text("empty_welcome", ui_language))
        st.markdown(get_text("empty_instructions", ui_language))
        st.markdown(get_text("empty_step1", ui_language))
        st.markdown(get_text("empty_step2", ui_language))
        st.markdown(get_text("empty_step3", ui_language))
        st.markdown("")
        st.info(get_text("empty_tip", ui_language))
