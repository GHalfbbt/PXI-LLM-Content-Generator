"""
Streamlit sidebar UI components for content generation inputs.

This module defines the sidebar interface where users input parameters
for blog content generation (topic, audience, tone, language).
"""

import streamlit as st
from typing import Dict, Any


# ============================================================================
# SIDEBAR CONFIGURATION OPTIONS
# ============================================================================

# Available tone options for content generation
TONE_OPTIONS = [
    "Professional",
    "Casual",
    "Friendly",
    "Technical"
]

# Available language options for content generation
LANGUAGE_OPTIONS = [
    "English",
    "Spanish",
    "French",
    "Italian"
]


# ============================================================================
# SIDEBAR RENDERING
# ============================================================================

def render_sidebar() -> Dict[str, Any]:
    """
    Render the Streamlit sidebar with all input controls for content generation.
    
    This function creates and displays all the necessary input fields in the
    Streamlit sidebar, including topic, audience, tone, and language selection.
    It also provides a generate button to trigger content generation.
    
    The sidebar is organized into logical sections with clear labels and
    helpful descriptions to guide the user through the content generation process.
    
    Returns:
        dict: A dictionary containing all user inputs and generation state:
            - 'topic' (str): The blog post topic entered by the user
            - 'audience' (str): The target audience for the content
            - 'tone' (str): The selected tone/style for writing
            - 'language' (str): The language for content generation
            - 'generate_clicked' (bool): True if the generate button was clicked
    
    Example:
        >>> inputs = render_sidebar()
        >>> if inputs['generate_clicked']:
        ...     content = generate_blog_content(
        ...         topic=inputs['topic'],
        ...         audience=inputs['audience'],
        ...         tone=inputs['tone'],
        ...         language=inputs['language']
        ...     )
    """
    # Display sidebar header
    st.sidebar.title("🎯 Content Configuration")
    st.sidebar.markdown("Configure the parameters for your blog post generation.")
    
    # Add a visual separator
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 1: TOPIC INPUT
    # ========================================================================
    st.sidebar.subheader("📝 Topic")
    topic = st.sidebar.text_input(
        label="Blog Topic",
        placeholder="e.g., The Future of Artificial Intelligence",
        help="Enter the main subject or theme for your blog post",
        key="topic_input"
    )
    
    # ========================================================================
    # SECTION 2: AUDIENCE INPUT
    # ========================================================================
    st.sidebar.subheader("👥 Target Audience")
    audience = st.sidebar.text_input(
        label="Target Audience",
        placeholder="e.g., software developers, general public",
        help="Specify who will be reading this content",
        key="audience_input"
    )
    
    # Add spacing between sections
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 3: TONE SELECTION
    # ========================================================================
    st.sidebar.subheader("🎨 Writing Style")
    tone = st.sidebar.selectbox(
        label="Tone",
        options=TONE_OPTIONS,
        index=0,  # Default to "Professional"
        help="Choose the writing tone that best fits your audience and purpose",
        key="tone_select"
    )
    
    # Provide brief descriptions for each tone option
    tone_descriptions = {
        "Professional": "Formal, business-appropriate language",
        "Casual": "Relaxed, conversational style",
        "Friendly": "Warm, approachable, and personable",
        "Technical": "Detailed, precise, with technical terminology"
    }
    
    # Display the description for the selected tone
    st.sidebar.caption(f"ℹ️ {tone_descriptions[tone]}")
    
    # ========================================================================
    # SECTION 4: LANGUAGE SELECTION
    # ========================================================================
    st.sidebar.subheader("🌍 Language")
    language = st.sidebar.selectbox(
        label="Content Language",
        options=LANGUAGE_OPTIONS,
        index=0,  # Default to "English"
        help="Select the language for content generation",
        key="language_select"
    )
    
    # Add spacing before the generate button
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 5: GENERATION CONTROLS
    # ========================================================================
    st.sidebar.subheader("🚀 Generate")
    
    # Display a note about required fields
    st.sidebar.caption("⚠️ Make sure to fill in the topic and audience fields")
    
    # Create the generate button
    # This button triggers the content generation process
    generate_clicked = st.sidebar.button(
        label="Generate Blog Post",
        type="primary",  # Makes the button more prominent
        use_container_width=True,  # Button spans full width of sidebar
        key="generate_button"
    )
    
    # ========================================================================
    # RETURN ALL INPUT VALUES
    # ========================================================================
    # Package all inputs into a dictionary for easy access by the main app
    return {
        "topic": topic,
        "audience": audience,
        "tone": tone,
        "language": language,
        "generate_clicked": generate_clicked
    }


# ============================================================================
# ADDITIONAL SIDEBAR COMPONENTS (OPTIONAL)
# ============================================================================

def render_sidebar_footer() -> None:
    """
    Render additional information in the sidebar footer.
    
    This function can be used to display additional information such as
    app version, credits, or helpful links at the bottom of the sidebar.
    """
    st.sidebar.divider()
    st.sidebar.caption("---")
    st.sidebar.caption("💡 **Tip:** Be specific with your topic and audience for better results!")
