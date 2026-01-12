"""
Streamlit sidebar UI components for content generation inputs.

This module defines the sidebar interface where users input parameters
for blog content generation (topic, audience, tone, language).
Supports multiple UI languages for better user experience.
"""

import streamlit as st
from typing import Dict, Any

from app.utils.i18n import get_text, get_available_languages


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

# Mapping for language display to actual value
LANGUAGE_MAP = {
    "English": "English",
    "Inglés": "English",
    "Anglais": "English",
    "Inglese": "English",
    "Spanish": "Spanish",
    "Español": "Spanish",
    "Espagnol": "Spanish",
    "Spagnolo": "Spanish",
    "French": "French",
    "Francés": "French",
    "Français": "French",
    "Francese": "French",
    "Italian": "Italian",
    "Italiano": "Italian",
    "Italien": "Italian"
}


# ============================================================================
# SIDEBAR RENDERING
# ============================================================================

def render_sidebar() -> Dict[str, Any]:
    """
    Render the Streamlit sidebar with all input controls for content generation.
    
    This function creates and displays all the necessary input fields in the
    Streamlit sidebar, including UI language selector, topic, audience, tone,
    and content language selection. It also provides a generate button to
    trigger content generation.
    
    The sidebar is organized into logical sections with clear labels and
    helpful descriptions to guide the user through the content generation process.
    All text is internationalized based on the selected UI language.
    
    Returns:
        dict: A dictionary containing all user inputs and generation state:
            - 'ui_language' (str): The selected UI language
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
    # ========================================================================
    # SECTION 0: UI LANGUAGE SELECTION
    # ========================================================================
    # Initialize session state for UI language if not exists
    if "ui_language" not in st.session_state:
        st.session_state.ui_language = "English"
    
    # UI language selector at the top of sidebar
    ui_language = st.sidebar.selectbox(
        label=get_text("ui_language_label", st.session_state.ui_language),
        options=get_available_languages(),
        index=get_available_languages().index(st.session_state.ui_language),
        help=get_text("ui_language_help", st.session_state.ui_language),
        key="ui_language_select"
    )
    
    # Update session state if language changed
    st.session_state.ui_language = ui_language
    
    st.sidebar.divider()
    
    # Display sidebar header using selected language
    st.sidebar.title(get_text("sidebar_title", ui_language))
    st.sidebar.markdown(get_text("sidebar_subtitle", ui_language))
    
    # Add a visual separator
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 1: TOPIC INPUT
    # ========================================================================
    st.sidebar.subheader(get_text("topic_header", ui_language))
    topic = st.sidebar.text_input(
        label=get_text("topic_label", ui_language),
        placeholder=get_text("topic_placeholder", ui_language),
        help=get_text("topic_help", ui_language),
        key="topic_input"
    )
    
    # ========================================================================
    # SECTION 2: AUDIENCE INPUT
    # ========================================================================
    st.sidebar.subheader(get_text("audience_header", ui_language))
    audience = st.sidebar.text_input(
        label=get_text("audience_label", ui_language),
        placeholder=get_text("audience_placeholder", ui_language),
        help=get_text("audience_help", ui_language),
        key="audience_input"
    )
    
    # Add spacing between sections
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 3: TONE SELECTION
    # ========================================================================
    st.sidebar.subheader(get_text("style_header", ui_language))
    tone = st.sidebar.selectbox(
        label=get_text("tone_label", ui_language),
        options=TONE_OPTIONS,
        index=0,  # Default to "Professional"
        help=get_text("tone_help", ui_language),
        key="tone_select"
    )
    
    # Provide brief descriptions for each tone option
    tone_descriptions = {
        "Professional": get_text("tone_professional", ui_language),
        "Casual": get_text("tone_casual", ui_language),
        "Friendly": get_text("tone_friendly", ui_language),
        "Technical": get_text("tone_technical", ui_language)
    }
    
    # Display the description for the selected tone
    st.sidebar.caption(f"ℹ️ {tone_descriptions[tone]}")
    
    # ========================================================================
    # SECTION 4: CONTENT LANGUAGE SELECTION
    # ========================================================================
    st.sidebar.subheader(get_text("language_header", ui_language))
    
    # Get translated language options
    language_options_translated = [
        get_text("lang_english", ui_language),
        get_text("lang_spanish", ui_language),
        get_text("lang_french", ui_language),
        get_text("lang_italian", ui_language)
    ]
    
    language_display = st.sidebar.selectbox(
        label=get_text("content_language_label", ui_language),
        options=language_options_translated,
        index=0,  # Default to "English"
        help=get_text("content_language_help", ui_language),
        key="language_select"
    )
    
    # Map displayed language back to English name for API
    language = LANGUAGE_MAP.get(language_display, "English")
    
    # Add spacing before the generate button
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 5: GENERATION CONTROLS
    # ========================================================================
    st.sidebar.subheader(get_text("generate_header", ui_language))
    
    # Display a note about required fields
    st.sidebar.caption(get_text("generate_note", ui_language))
    
    # Create the generate button
    # This button triggers the content generation process
    generate_clicked = st.sidebar.button(
        label=get_text("generate_button", ui_language),
        type="primary",  # Makes the button more prominent
        use_container_width=True,  # Button spans full width of sidebar
        key="generate_button"
    )
    
    # ========================================================================
    # RETURN ALL INPUT VALUES
    # ========================================================================
    # Package all inputs into a dictionary for easy access by the main app
    return {
        "ui_language": ui_language,
        "topic": topic,
        "audience": audience,
        "tone": tone,
        "language": language,
        "generate_clicked": generate_clicked
    }


# ============================================================================
# ADDITIONAL SIDEBAR COMPONENTS (OPTIONAL)
# ============================================================================

def render_sidebar_footer(ui_language: str = "English") -> None:
    """
    Render additional information in the sidebar footer.
    
    This function displays helpful tips at the bottom of the sidebar
    in the user's selected language.
    
    Args:
        ui_language (str): The UI language for translations. Default is "English".
    """
    st.sidebar.divider()
    st.sidebar.caption("---")
    st.sidebar.caption(get_text("footer_tip", ui_language))
