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
    # SECTION 4.5: IDENTITY PROFILE (OPTIONAL)
    # ========================================================================
    st.sidebar.subheader(f"👤 {get_text('identity_header', ui_language)}")
    
    # Enable/disable identity personalization
    identity_enabled = st.sidebar.checkbox(
        label=get_text("identity_enable", ui_language),
        value=False,
        help=get_text("identity_enable_help", ui_language),
        key="identity_enabled"
    )
    
    # Initialize identity fields with default values
    identity_type = None
    identity_name = ""
    identity_role = ""
    identity_description = ""
    identity_tone = ""
    identity_values = ""
    
    # Show identity fields when enabled
    if identity_enabled:
        # Initialize default index for identity type
        # Preserve selection across language changes by checking session state
        default_type_index = 0
        if "identity_type" in st.session_state:
            # Get the current value from session state
            current_type = st.session_state.identity_type
            # Check if it matches "person" or "company" keywords
            if "company" in current_type.lower() or "empresa" in current_type.lower() or "société" in current_type.lower() or "azienda" in current_type.lower():
                default_type_index = 1
        
        # Identity type selector
        identity_type = st.sidebar.selectbox(
            label=get_text("identity_type_label", ui_language),
            options=[get_text("identity_type_person", ui_language), get_text("identity_type_company", ui_language)],
            index=default_type_index,
            help=get_text("identity_type_help", ui_language),
            key="identity_type"
        )
        
        # Name input - use session state value as default
        identity_name = st.sidebar.text_input(
            label=get_text("identity_name_label", ui_language),
            value=st.session_state.get("identity_name", ""),
            placeholder=get_text("identity_name_placeholder", ui_language),
            help=get_text("identity_name_help", ui_language),
            key="identity_name"
        )
        
        # Role or Industry input with suggestions
        is_person = identity_type == get_text("identity_type_person", ui_language)
        role_label = get_text("identity_role_label", ui_language) if is_person else get_text("identity_industry_label", ui_language)
        
        # Show suggestions in an expander
        if is_person:
            with st.sidebar.expander(f"💡 {get_text('identity_role_suggestions', ui_language)}"):
                st.caption(f"{get_text('identity_role_ceo', ui_language)} • {get_text('identity_role_marketing', ui_language)} • {get_text('identity_role_engineer', ui_language)} • {get_text('identity_role_scientist', ui_language)} • {get_text('identity_role_product', ui_language)} • {get_text('identity_role_designer', ui_language)} • {get_text('identity_role_writer', ui_language)}")
        else:
            with st.sidebar.expander(f"💡 {get_text('identity_industry_suggestions', ui_language)}"):
                st.caption(f"{get_text('identity_industry_tech', ui_language)} • {get_text('identity_industry_fintech', ui_language)} • {get_text('identity_industry_health', ui_language)} • {get_text('identity_industry_ecommerce', ui_language)} • {get_text('identity_industry_marketing', ui_language)} • {get_text('identity_industry_consulting', ui_language)} • {get_text('identity_industry_education', ui_language)}")
        
        identity_role = st.sidebar.text_input(
            label=role_label,
            value=st.session_state.get("identity_role", ""),
            placeholder=get_text("identity_role_placeholder_person", ui_language) if is_person else get_text("identity_role_placeholder_company", ui_language),
            help=get_text("identity_role_help_person", ui_language) if is_person else get_text("identity_role_help_company", ui_language),
            key="identity_role"
        )
        
        # Description text area
        description_label = get_text("identity_background_label", ui_language) if is_person else get_text("identity_about_label", ui_language)
        
        identity_description = st.sidebar.text_area(
            label=description_label,
            value=st.session_state.get("identity_description", ""),
            placeholder=get_text("identity_background_placeholder", ui_language) if is_person else get_text("identity_about_placeholder", ui_language),
            help=get_text("identity_background_help", ui_language),
            height=100,
            key="identity_description"
        )
        
        # Optional: Tone of voice with dropdown + custom option
        tone_options = [
            get_text("identity_tone_formal", ui_language),
            get_text("identity_tone_approachable", ui_language),
            get_text("identity_tone_conversational", ui_language),
            get_text("identity_tone_technical", ui_language),
            get_text("identity_tone_inspiring", ui_language),
            get_text("identity_tone_empathetic", ui_language),
            get_text("identity_tone_innovative", ui_language),
            get_text("identity_custom", ui_language)
        ]
        
        tone_selection = st.sidebar.selectbox(
            label=get_text("identity_tone_label", ui_language),
            options=[""] + tone_options,  # Empty string for "no selection"
            format_func=lambda x: get_text("identity_select_placeholder", ui_language) if x == "" else x,
            help=get_text("identity_tone_help", ui_language),
            key="identity_tone_select"
        )
        
        # If custom selected or no selection, show text input
        if tone_selection == get_text("identity_custom", ui_language) or tone_selection == "":
            identity_tone = st.sidebar.text_input(
                label=get_text("identity_tone_custom_label", ui_language) if tone_selection == get_text("identity_custom", ui_language) else get_text("identity_tone_custom_placeholder", ui_language),
                value=st.session_state.get("identity_tone_custom", ""),
                placeholder="e.g., witty and educational",
                key="identity_tone_custom"
            )
        else:
            identity_tone = tone_selection
        
        # Optional: Core values with dropdown + custom option
        values_options = [
            get_text("identity_values_innovation", ui_language),
            get_text("identity_values_customer", ui_language),
            get_text("identity_values_sustainability", ui_language),
            get_text("identity_values_excellence", ui_language),
            get_text("identity_values_creativity", ui_language),
            get_text("identity_values_trust", ui_language),
            get_text("identity_values_diversity", ui_language),
            get_text("identity_custom", ui_language)
        ]
        
        values_selection = st.sidebar.selectbox(
            label=get_text("identity_values_label", ui_language),
            options=[""] + values_options,  # Empty string for "no selection"
            format_func=lambda x: get_text("identity_select_placeholder", ui_language) if x == "" else x,
            help=get_text("identity_values_help", ui_language),
            key="identity_values_select"
        )
        
        # If custom selected or no selection, show text input
        if values_selection == get_text("identity_custom", ui_language) or values_selection == "":
            identity_values = st.sidebar.text_input(
                label=get_text("identity_values_custom_label", ui_language) if values_selection == get_text("identity_custom", ui_language) else get_text("identity_values_custom_placeholder", ui_language),
                value=st.session_state.get("identity_values_custom", ""),
                placeholder="e.g., speed, simplicity, customer focus",
                key="identity_values_custom"
            )
        else:
            identity_values = values_selection
    
    # Add spacing
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 4.7: CONTENT WRITING STYLE
    # ========================================================================
    st.sidebar.subheader(f"✍️ {get_text('style_selector_header', ui_language)}")
    
    # Style options mapping
    style_options = {
        "default": get_text("style_default", ui_language),
        "seo": get_text("style_seo", ui_language),
        "divulgative": get_text("style_divulgative", ui_language),
        "kids": get_text("style_kids", ui_language)
    }
    
    # Get display labels
    style_display_options = list(style_options.values())
    
    # Create reverse mapping
    display_to_style = {v: k for k, v in style_options.items()}
    
    style_display = st.sidebar.selectbox(
        label=get_text("style_selector_label", ui_language),
        options=style_display_options,
        index=0,  # Default to "Default"
        help=get_text("style_selector_help", ui_language),
        key="style_select"
    )
    
    # Map display value back to internal style key
    selected_style = display_to_style.get(style_display, "default")
    
    # Show style description
    style_descriptions = {
        "default": get_text("style_default_desc", ui_language),
        "seo": get_text("style_seo_desc", ui_language),
        "divulgative": get_text("style_divulgative_desc", ui_language),
        "kids": get_text("style_kids_desc", ui_language)
    }
    
    st.sidebar.caption(f"ℹ️ {style_descriptions[selected_style]}")
    
    # Add spacing
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 5: LLM PROVIDER SELECTION
    # ========================================================================
    st.sidebar.subheader(get_text("provider_header", ui_language))
    
    # Provider options with clear labels
    provider_options = {
        "groq": get_text("provider_groq", ui_language),
        "ollama": get_text("provider_ollama", ui_language)
    }
    
    # Get display labels for the selectbox
    provider_display_options = list(provider_options.values())
    
    # Create reverse mapping for getting the key from display value
    display_to_key = {v: k for k, v in provider_options.items()}
    
    provider_display = st.sidebar.selectbox(
        label=get_text("provider_label", ui_language),
        options=provider_display_options,
        index=0,  # Default to Groq (Cloud)
        help=get_text("provider_help", ui_language),
        key="provider_select"
    )
    
    # Map displayed provider back to internal key
    llm_provider = display_to_key.get(provider_display, "groq")
    
    # Add spacing before the generate button
    st.sidebar.divider()
    
    # ========================================================================
    # SECTION 4.8: IMAGE GENERATION (OPTIONAL)
    # ========================================================================
    st.sidebar.subheader("🖼️ Images (optional)")
    
    # --- Blog Images ---
    blog_images_enabled = st.sidebar.checkbox(
        label="Enable images for blog content",
        value=False,
        help="Add relevant images to your blog post to enhance visual appeal",
        key="blog_images_enabled"
    )
    
    # Initialize default values
    blog_image_provider = "external"
    blog_num_images = 2
    
    # Show blog image controls when enabled
    if blog_images_enabled:
        blog_image_provider = st.sidebar.radio(
            label="Image provider",
            options=["external", "replicate", "huggingface"],
            format_func=lambda x: {
                "external": "📸 Stock photos (Unsplash / Pexels)",
                "replicate": "🎨 AI-generated images (Replicate)",
                "huggingface": "🤖 AI-generated images (HuggingFace – experimental)"
            }[x],
            help="Choose the source for your images",
            key="blog_image_provider"
        )
        
        # Show helpful text based on selected provider
        if blog_image_provider == "external":
            st.sidebar.caption("ℹ️ High-quality stock photos with proper attribution")
        elif blog_image_provider == "replicate":
            st.sidebar.caption("ℹ️ AI-generated unique images (requires Replicate API key)")
        else:  # huggingface
            st.sidebar.caption("⚠️ Experimental - API may be unstable")
        
        blog_num_images = st.sidebar.slider(
            label="Number of images",
            min_value=1,
            max_value=5,
            value=2,
            help="How many images to include in the blog post",
            key="blog_num_images"
        )
    
    st.sidebar.markdown("")  # Small spacing
    
    # --- Social Media Images ---
    social_images_enabled = st.sidebar.checkbox(
        label="Include image in social posts",
        value=False,
        help="Add an image to accompany your social media posts",
        key="social_images_enabled"
    )
    
    # Initialize default value
    social_image_provider = "external"
    
    # Show social image controls when enabled
    if social_images_enabled:
        social_image_provider = st.sidebar.radio(
            label="Image provider",
            options=["external", "replicate", "huggingface"],
            format_func=lambda x: {
                "external": "📸 Stock photos (Unsplash / Pexels)",
                "replicate": "🎨 AI-generated images (Replicate)",
                "huggingface": "🤖 AI-generated images (HuggingFace – experimental)"
            }[x],
            help="Choose the source for social media images",
            key="social_image_provider"
        )
        
        # Show helpful text based on selected provider
        if social_image_provider == "external":
            st.sidebar.caption("ℹ️ Eye-catching stock photos optimized for social media")
        elif social_image_provider == "replicate":
            st.sidebar.caption("ℹ️ Custom AI-generated visuals (requires Replicate API key)")
        else:  # huggingface
            st.sidebar.caption("⚠️ Experimental - API may be unstable")
    
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
        "style": selected_style,  # Content writing style
        "llm_provider": llm_provider,
        "generate_clicked": generate_clicked,
        # Identity profile fields
        "identity_enabled": identity_enabled,
        "identity_type": identity_type,
        "identity_name": identity_name,
        "identity_role": identity_role,
        "identity_description": identity_description,
        "identity_tone": identity_tone,
        "identity_values": identity_values,
        # Image generation fields
        "blog_images_enabled": blog_images_enabled,
        "blog_image_provider": blog_image_provider,
        "blog_num_images": blog_num_images,
        "social_images_enabled": social_images_enabled,
        "social_image_provider": social_image_provider
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
