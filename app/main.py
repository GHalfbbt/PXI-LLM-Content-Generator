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
    # HEADER SECTION
    # ========================================================================
    
    # Display the main application header using selected language
    st.title(get_text("page_title", ui_language))
    st.markdown(get_text("page_subtitle", ui_language))
    
    # Optionally render sidebar footer with tips
    render_sidebar_footer(ui_language)
    
    # ========================================================================
    # STATE MANAGEMENT & CONTENT GENERATION
    # ========================================================================
    
    # Check if the generate button was clicked
    if inputs["generate_clicked"]:
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
                    llm_provider=inputs["llm_provider"]
                )
                
                # ============================================================
                # SUCCESS STATE
                # ============================================================
                
                # Store the generated content in session state
                # This allows the content to persist across reruns
                st.session_state["last_generated_content"] = generated_content
                
                # Display success message
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
                
                # Detect Ollama-specific errors
                if inputs["llm_provider"] == "ollama" and any(
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


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    main()
