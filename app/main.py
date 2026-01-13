"""
Main Streamlit application for AI-powered content generation.

This is the entry point for the content generation platform.
It orchestrates the UI components and coordinates the content generation
workflow without containing business logic.
"""

import streamlit as st
from dotenv import load_dotenv

# Import UI components
from app.ui.sidebar import render_sidebar, render_sidebar_footer
from app.ui.output import (
    render_output,
    render_empty_state,
    render_error
)

# Import content generation functionality
from app.core.chains.content_chain import generate_blog_content
from app.core.chains.social_chain import generate_social_post

# Import identity profile for personalization
from app.core.identity import IdentityProfile

# Import configuration for validation
from app.config import settings

# Import i18n for translations
from app.utils.i18n import get_text


# ============================================================================
# APPLICATION INITIALIZATION
# ============================================================================

# Load environment variables from .env file
# This must be done before any other imports that use env variables
load_dotenv()

# Validate configuration on startup
# This ensures API keys and required settings are present
try:
    settings.validate_config()
except ValueError as e:
    st.error(get_text("config_error", "English", error=str(e)))
    st.stop()


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Configure the Streamlit page settings
# This must be the first Streamlit command in the script
st.set_page_config(
    page_title=get_text("page_title", "English"),
    page_icon="✍️",
    layout="wide",  # Use wide layout for better content display
    initial_sidebar_state="expanded",  # Show sidebar by default
    menu_items={
        "Get Help": None,
        "Report a bug": None,
        "About": "AI-powered content generation platform using LLMs"
    }
)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main() -> None:
    """
    Main application function that orchestrates the entire workflow.
    
    This function coordinates all the components of the application:
    1. Renders the page header
    2. Displays the sidebar with input controls
    3. Handles user input validation
    4. Manages application state (empty, loading, success, error)
    5. Triggers content generation when requested
    6. Displays the generated content or appropriate messages
    
    The function maintains a clear separation of concerns by only
    orchestrating UI and calling other modules for business logic.
    """
    # ========================================================================
    # CUSTOM STYLING
    # ========================================================================
    
    # Apply custom CSS for better visual design
    st.markdown("""
        <style>
        /* Main background with soft blue gradient - cover full page */
        .main {
            background: linear-gradient(135deg, #a8d0ff 0%, #7eb8ff 100%);
            background-attachment: fixed;
            padding: 0 !important;
            min-height: 100vh;
        }
        
        /* Hide Streamlit header */
        header[data-testid="stHeader"] {
            background: linear-gradient(135deg, #a8d0ff 0%, #7eb8ff 100%);
            border-bottom: none;
        }
        
        /* Content container with soft blue gradient - seamless integration */
        .block-container {
            background: linear-gradient(135deg, #a8d0ff 0%, #7eb8ff 100%);
            border-radius: 0;
            padding: 2rem;
            padding-top: 1rem !important;
            padding-bottom: 2rem !important;
            margin: 0 !important;
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            box-shadow: none;
            min-height: 100vh;
        }
        
        /* Remove white space at bottom */
        .appview-container {
            background: linear-gradient(135deg, #a8d0ff 0%, #7eb8ff 100%);
        }
        
        /* Streamlit footer integration */
        footer {
            background: linear-gradient(135deg, #a8d0ff 0%, #7eb8ff 100%);
            visibility: hidden;
        }
        
        /* Main header styling - dark blue solid */
        h1 {
            color: #1E3A8A;
            font-weight: 800;
            padding-top: 0rem;
            padding-bottom: 0.5rem;
            margin-top: 0rem;
            font-size: 3rem;
        }
        
        /* Subtitle styling - dark text for light blue background */
        .stMarkdown p {
            color: #1E40AF;
            font-size: 1.2rem;
            line-height: 1.6;
            font-weight: 500;
        }
        
        /* Success message styling - blue-green */
        .stSuccess {
            background: linear-gradient(135deg, #84FAB0 0%, #8FD3F4 100%);
            border-left: 6px solid #3B82F6;
            border-radius: 0.75rem;
            padding: 1rem;
            color: #1E3A8A;
            font-weight: 600;
        }
        
        /* Warning message styling - blue-yellow */
        .stWarning {
            background: linear-gradient(135deg, #FFE259 0%, #FFA751 100%);
            border-left: 6px solid #F59E0B;
            border-radius: 0.75rem;
            padding: 1rem;
            color: #78350F;
            font-weight: 600;
        }
        
        /* Info message styling - light blue */
        .stInfo {
            background: linear-gradient(135deg, #A1C4FD 0%, #C2E9FB 100%);
            border-left: 6px solid #3B82F6;
            border-radius: 0.75rem;
            padding: 1rem;
            color: #1E3A8A;
            font-weight: 600;
        }
        
        /* Button styling - red gradient */
        .stButton > button {
            background: linear-gradient(90deg, #EF4444 0%, #DC2626 100%);
            color: white;
            font-weight: 600;
            border: none;
            padding: 0.5rem 2rem;
            border-radius: 0.5rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background: linear-gradient(90deg, #DC2626 0%, #B91C1C 100%);
            box-shadow: 0 4px 6px rgba(239, 68, 68, 0.4);
        }
        
        /* Sidebar styling - soft blue gradient with increased width */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #3B82F6 0%, #2563EB 100%);
            width: 24rem !important;
            min-width: 24rem !important;
        }
        
        [data-testid="stSidebar"] > div {
            background-color: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(10px);
            width: 24rem !important;
        }
        
        /* Compact sidebar spacing - more aggressive */
        [data-testid="stSidebar"] .block-container {
            padding-top: 0.5rem;
            padding-bottom: 0.5rem;
        }
        
        /* Reduce spacing between sidebar elements - ultra compact */
        [data-testid="stSidebar"] .stSelectbox,
        [data-testid="stSidebar"] .stTextInput {
            margin-bottom: 0.1rem;
            margin-top: 0rem;
        }
        
        /* Ultra compact dividers */
        [data-testid="stSidebar"] hr {
            margin-top: 0.15rem;
            margin-bottom: 0.15rem;
        }
        
        /* Very compact headers and subheaders in sidebar */
        [data-testid="stSidebar"] h1 {
            font-size: 1.4rem;
            margin-bottom: 0rem;
            margin-top: 0rem;
            padding-bottom: 0rem;
            line-height: 1.3;
        }
        
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            font-size: 1rem;
            margin-bottom: 0rem;
            margin-top: 0.15rem;
            padding-bottom: 0rem;
            line-height: 1.2;
        }
        
        /* Minimize caption spacing */
        [data-testid="stSidebar"] .stCaption {
            margin-top: 0rem;
            margin-bottom: 0rem;
            font-size: 0.75rem;
            line-height: 1.1;
        }
        
        /* Compact markdown in sidebar */
        [data-testid="stSidebar"] .stMarkdown {
            margin-bottom: 0.1rem;
            margin-top: 0rem;
        }
        
        /* Reduce label spacing */
        [data-testid="stSidebar"] label {
            margin-bottom: 0rem;
        }
        
        /* Sidebar text in white for visibility */
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] .stMarkdown,
        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p {
            color: white !important;
        }
        
        /* Text area styling - blue gradient border and light background */
        .stTextArea textarea {
            border: 3px solid transparent;
            background-image: linear-gradient(white, white), linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
            background-origin: border-box;
            background-clip: padding-box, border-box;
            border-radius: 1rem;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            transition: all 0.3s ease;
            color: #1F2937;
            font-weight: 500;
        }
        
        .stTextArea textarea:focus {
            box-shadow: 0 0 0 4px rgba(79, 172, 254, 0.3);
        }
        
        /* Subheaders with dark blue */
        h2, h3 {
            color: #1E3A8A;
            font-weight: 700;
        }
        
        /* Remove separate background from output section - unified design */
        .element-container:has(.stTextArea) {
            padding: 0;
            background: transparent;
        }
        
        /* Disable spellcheck underline on output text area */
        textarea[aria-label="Generated Content"] {
            spellcheck: false;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # SIDEBAR - INPUT COLLECTION
    # ========================================================================
    
    # Render the sidebar and collect user inputs
    # This returns a dictionary with all input values and button state
    inputs = render_sidebar()
    
    # Get the selected UI language
    ui_language = inputs.get("ui_language", "English")
    
    # ========================================================================
    # IDENTITY PROFILE CREATION
    # ========================================================================
    
    # Create identity profile if enabled and valid
    identity = None
    
    if inputs.get("identity_enabled", False):
        # Validate required identity fields
        identity_name = inputs.get("identity_name", "").strip()
        identity_role = inputs.get("identity_role", "").strip()
        identity_description = inputs.get("identity_description", "").strip()
        
        if identity_name and identity_role and identity_description:
            try:
                # Map translated type back to English for internal use
                type_mapping = {
                    get_text("identity_type_person", inputs["ui_language"]): "person",
                    get_text("identity_type_company", inputs["ui_language"]): "company"
                }
                identity_type_internal = type_mapping.get(inputs.get("identity_type", ""), "person")
                
                # Create IdentityProfile instance
                identity = IdentityProfile(
                    type=identity_type_internal,  # "person" or "company"
                    name=identity_name,
                    role_or_industry=identity_role,
                    description=identity_description,
                    tone=inputs.get("identity_tone", "").strip() or None,
                    values=inputs.get("identity_values", "").strip() or None
                )
                
                # Check if identity has changed - if so, clear previous content
                old_identity = st.session_state.get("identity_profile")
                if old_identity and (
                    old_identity.name != identity.name or
                    old_identity.type != identity.type or
                    old_identity.role_or_industry != identity.role_or_industry
                ):
                    st.sidebar.info(f"🔄 Identity changed: {old_identity.name} → {identity.name}")
                    # Clear previous content since identity changed
                    if "last_generated_content" in st.session_state:
                        del st.session_state["last_generated_content"]
                    if "social_posts" in st.session_state:
                        del st.session_state["social_posts"]
                
                # Store in session state for persistence
                st.session_state["identity_profile"] = identity
                
            except ValueError as e:
                # Display validation error to user
                st.sidebar.error(f"❌ Identity validation error: {str(e)}")
                identity = None
        elif identity_name or identity_role or identity_description:
            # Partial input - show warning
            st.sidebar.warning("⚠️ Please fill in all required identity fields (Name, Role/Industry, Description)")
    else:
        # Identity disabled - clear from session state
        if "identity_profile" in st.session_state:
            del st.session_state["identity_profile"]
    
    # Add identity to inputs for passing to render functions
    inputs["identity"] = identity
    # Add identity to inputs for passing to render functions
    inputs["identity"] = identity
    
    # ========================================================================
    # HEADER SECTION
    # ========================================================================
    
    # Display the main application header using selected language
    st.title(get_text("page_title", ui_language))
    st.markdown(get_text("page_subtitle", ui_language))
    
    # Optionally render sidebar footer with tips
    render_sidebar_footer(ui_language)
    
    # TABBED INTERFACE - BLOG & SOCIAL MEDIA
    # ========================================================================
    
    # Create tabs for blog and social media content
    tab_blog, tab_social = st.tabs([
        get_text("tab_blog", ui_language),
        get_text("tab_social", ui_language)
    ])
    
    # ========================================================================
    # TAB 1: BLOG CONTENT GENERATION
    # ========================================================================
    
    with tab_blog:
        render_blog_generation_ui(inputs, ui_language)
    
    # ========================================================================
    # TAB 2: SOCIAL MEDIA GENERATION
    # ========================================================================
    
    with tab_social:
        render_social_media_ui(inputs, ui_language)


def render_blog_generation_ui(inputs: dict, ui_language: str) -> None:
    """
    Render the blog content generation UI.
    
    This function handles the blog generation workflow including
    validation, generation, and output display.
    
    Args:
        inputs: Dictionary containing user inputs from sidebar.
        ui_language: Selected UI language for translations.
    """
    # ========================================================================
    # ========================================================================
    # STATE MANAGEMENT & CONTENT GENERATION
    # ========================================================================
    
    # Create a key for current generation parameters
    # This helps detect when parameters change and auto-regenerate
    current_params = {
        "topic": inputs["topic"],
        "audience": inputs["audience"],
        "tone": inputs["tone"],
        "language": inputs["language"],
        "llm_provider": inputs["llm_provider"],
        "style": inputs.get("style", "default"),
        "identity_name": inputs.get("identity").name if inputs.get("identity") else None,
        "identity_role": inputs.get("identity").role_or_industry if inputs.get("identity") else None
    }
    
    # Check if parameters have changed since last generation
    params_changed = False
    if "last_generation_params" in st.session_state:
        params_changed = st.session_state["last_generation_params"] != current_params
    
    # Check if the generate button was clicked OR if key parameters changed
    should_generate = inputs["generate_clicked"] or (
        params_changed and 
        "last_generated_content" in st.session_state and
        inputs["topic"].strip() and 
        inputs["audience"].strip()
    )
    
    if should_generate:
        # ====================================================================
        # INPUT VALIDATION
        # ====================================================================
        
        # Validate that required fields are not empty
        # Topic and audience are mandatory for meaningful content generation
        if not inputs["topic"].strip():
            st.warning(get_text("validation_topic", ui_language))
            return
        
        if not inputs["audience"].strip():
            st.warning(get_text("validation_audience", ui_language))
            return
        
        # ====================================================================
        # LOADING STATE
        # ====================================================================
        
        # Display loading indicator while content is being generated
        # This provides visual feedback to the user
        with st.spinner(get_text("generating_spinner", ui_language)):
            try:
                # ============================================================
                # CONTENT GENERATION
                # ============================================================
                
                # Call the content generation chain with user inputs
                # This is where the actual AI content generation happens
                generated_content = generate_blog_content(
                    topic=inputs["topic"],
                    audience=inputs["audience"],
                    tone=inputs["tone"],
                    language=inputs["language"],
                    llm_provider=inputs["llm_provider"],
                    identity=inputs.get("identity"),  # Pass identity if available
                    style=inputs.get("style", "default"),  # Pass content writing style
                    include_images=inputs.get("blog_images_enabled", False),  # Image generation
                    image_provider=inputs.get("blog_image_provider", "external"),
                    num_images=inputs.get("blog_num_images", 2)
                )
                
                # ============================================================
                # SUCCESS STATE
                # ============================================================
                
                # Store the generated content in session state
                # This allows the content to persist across reruns
                st.session_state["last_generated_content"] = generated_content
                
                # Store the generation parameters used
                # This allows detecting changes for auto-regeneration
                st.session_state["last_generation_params"] = current_params
                
                # Display success message (only if explicitly clicked generate button)
                if inputs["generate_clicked"]:
                    st.success(get_text("success_message", ui_language))
                
                # Render the generated content
                render_output(generated_content, ui_language)
            
            except ValueError as ve:
                # ============================================================
                # CONFIGURATION ERROR (LLM not available/configured)
                # ============================================================
                
                render_error(str(ve), ui_language)
            
            except Exception as e:
                # ============================================================
                # RUNTIME ERROR (Connectivity, model issues, etc.)
                # ============================================================
                
                error_msg = str(e).lower()
                
                # Detect image provider errors
                if inputs.get("blog_images_enabled", False) and any(
                    keyword in error_msg for keyword in [
                        "image",
                        "unsplash",
                        "pexels",
                        "huggingface",
                        "replicate",
                        "api key",
                        "access key"
                    ]
                ):
                    st.warning(
                        f"⚠️ Image generation failed: {str(e)}\n\n"
                        "The blog content was generated successfully, but images could not be added. "
                        "Please check your API keys or try a different image provider."
                    )
                    # Continue without showing full error - content is still valid
                
                # Detect Ollama-specific errors
                elif inputs["llm_provider"] == "ollama" and any(
                    keyword in error_msg for keyword in [
                        "connection refused",
                        "connection error",
                        "failed to connect",
                        "could not connect",
                        "ollama",
                        "localhost:11434",
                        "connect econnrefused"
                    ]
                ):
                    st.error(get_text("ollama_error", ui_language))
                    st.info(get_text("ollama_help", ui_language))
                else:
                    # Generic error handling
                    render_error(str(e), ui_language)
    
    else:
        # ====================================================================
        # EMPTY STATE OR DISPLAY PREVIOUS CONTENT
        # ====================================================================
        
        # Check if there's previously generated content in session state
        if "last_generated_content" in st.session_state:
            # Display the last generated content
            # This allows users to see their previous generation
            st.info(get_text("previous_content_info", ui_language))
            render_output(st.session_state["last_generated_content"], ui_language)
        else:
            # No content has been generated yet
            # Display a friendly empty state with instructions
            render_empty_state(ui_language)


def render_social_media_ui(inputs: dict, ui_language: str) -> None:
    """
    Render the social media content generation UI.
    
    This function allows users to transform existing blog content
    into platform-specific social media posts.
    
    Args:
        inputs: Dictionary containing user inputs from sidebar.
        ui_language: Selected UI language for translations.
    """
    # ========================================================================
    # CHECK FOR EXISTING BLOG CONTENT
    # ========================================================================
    
    # Social media generation requires a blog post as source
    if "last_generated_content" not in st.session_state:
        # Display empty state with instructions
        st.info(f"📝 {get_text('social_no_content', ui_language)}")
        st.markdown(f"""
        ### {get_text('social_subtitle', ui_language).replace('.', ':')}
        {get_text('social_instruction_1', ui_language)}
        {get_text('social_instruction_2', ui_language)}
        {get_text('social_instruction_3', ui_language)}
        """)
        return
    
    # ========================================================================
    # SOCIAL MEDIA CONFIGURATION
    # ========================================================================
    
    st.markdown(f"### {get_text('social_title', ui_language)}")
    st.markdown(get_text('social_subtitle', ui_language))
    
    # Platform selection
    col1, col2 = st.columns([2, 1])
    
    with col1:
        selected_platforms = st.multiselect(
            f"📱 {get_text('social_platform_label', ui_language)}",
            options=["linkedin", "twitter", "instagram"],
            default=["linkedin"],
            help="Choose which social media platforms to generate content for"
        )
    
    with col2:
        # LLM provider selection for social posts
        social_llm_provider = st.selectbox(
            "🤖 LLM Provider",
            options=["groq", "ollama"],
            index=0,
            help="Select the LLM provider for social content generation"
        )
    
    # Generate button
    generate_social = st.button(
        "🚀 Generate Social Posts",
        type="primary",
        use_container_width=True,
        disabled=len(selected_platforms) == 0
    )
    
    # ========================================================================
    # SOCIAL POST GENERATION
    # ========================================================================
    
    if generate_social:
        if not selected_platforms:
            st.warning("⚠️ Please select at least one platform.")
            return
        
        # Get blog content from session state
        blog_content = st.session_state["last_generated_content"]
        
        # Get identity if available
        identity_obj = inputs.get("identity")
        
        # Display progress
        with st.spinner(f"🤖 Generating posts for {len(selected_platforms)} platform(s)..."):
            # Clear previous results and generate fresh posts
            st.session_state["social_posts"] = {}
            
            # Generate posts for each platform
            for platform in selected_platforms:
                try:
                    # Generate platform-specific post
                    social_post_result = generate_social_post(
                        blog_content=blog_content,
                        platform=platform,
                        language=inputs["language"],  # Pass the content language
                        llm_provider=social_llm_provider,
                        identity=identity_obj,  # Pass identity if available
                        style=inputs.get("style", "default"),  # Pass content writing style
                        include_image=inputs.get("social_images_enabled", False),  # Image generation
                        image_provider=inputs.get("social_image_provider", "external")
                    )
                    
                    # Extract text from result dictionary
                    # generate_social_post now returns {"text": str, "image": ImageAsset, "platform": str}
                    social_post_text = social_post_result.get("text", social_post_result) if isinstance(social_post_result, dict) else social_post_result
                    
                    # Store successful result
                    st.session_state["social_posts"][platform] = {
                        "content": social_post_text,
                        "status": "success",
                        "provider": social_llm_provider
                    }
                    
                except Exception as e:
                    # Check if error is image-related
                    error_msg = str(e).lower()
                    is_image_error = any(
                        keyword in error_msg for keyword in [
                            "image",
                            "unsplash",
                            "pexels",
                            "huggingface",
                            "replicate"
                        ]
                    )
                    
                    if is_image_error and inputs.get("social_images_enabled", False):
                        # Image error - generate post without image
                        st.warning(f"⚠️ Image generation failed for {platform}. Continuing without image...")
                        try:
                            # Retry without image
                            social_post_result = generate_social_post(
                                blog_content=blog_content,
                                platform=platform,
                                language=inputs["language"],
                                llm_provider=social_llm_provider,
                                identity=identity_obj,
                                style=inputs.get("style", "default"),
                                include_image=False  # Disable images
                            )
                            social_post_text = social_post_result.get("text", social_post_result) if isinstance(social_post_result, dict) else social_post_result
                            
                            st.session_state["social_posts"][platform] = {
                                "content": social_post_text,
                                "status": "success",
                                "provider": social_llm_provider,
                                "image_warning": str(e)
                            }
                            continue
                        except:
                            pass  # Fall through to regular error handling
                    
                    # Store error for this platform
                    st.session_state["social_posts"][platform] = {
                        "content": None,
                        "status": "error",
                        "error": str(e),
                        "provider": social_llm_provider
                    }
        
        # Show completion message
        successful = sum(
            1 for p in st.session_state["social_posts"].values()
            if p["status"] == "success"
        )
        st.success(f"✅ Generated {successful}/{len(selected_platforms)} social posts successfully!")
    
    # ========================================================================
    # DISPLAY SOCIAL POSTS
    # ========================================================================
    
    # Display results if they exist
    if "social_posts" in st.session_state and st.session_state["social_posts"]:
        st.markdown("---")
        st.markdown("### 📤 Generated Social Posts")
        
        # Platform emojis and names
        platform_info = {
            "linkedin": {"emoji": "💼", "name": "LinkedIn", "color": "#0077B5"},
            "twitter": {"emoji": "🐦", "name": "Twitter", "color": "#1DA1F2"},
            "instagram": {"emoji": "📸", "name": "Instagram", "color": "#E4405F"}
        }
        
        # Display each platform's result
        for platform, result in st.session_state["social_posts"].items():
            info = platform_info.get(platform, {"emoji": "📱", "name": platform.capitalize()})
            
            # Platform header
            st.markdown(f"#### {info['emoji']} {info['name']}")
            
            if result["status"] == "success":
                # Success - display the post
                content = result["content"]
                char_count = len(content)
                
                # Show character count with color coding
                if platform == "twitter" and char_count > 280:
                    st.warning(f"⚠️ {char_count} characters (exceeds Twitter limit of 280)")
                else:
                    st.caption(f"✓ {char_count} characters · Generated with {result['provider'].upper()}")
                
                # Display content in text area for easy copying
                st.text_area(
                    label=f"{info['name']} Post",
                    value=content,
                    height=200,
                    key=f"social_output_{platform}",
                    label_visibility="collapsed"
                )
                
            else:
                # Error - display error message
                st.error(f"❌ Failed to generate {info['name']} post")
                with st.expander("View Error Details"):
                    st.code(result.get("error", "Unknown error"))
            
            st.markdown("")  # Spacing


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
