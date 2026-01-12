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
    st.error(f"⚠️ Configuration Error: {str(e)}")
    st.stop()


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

# Configure the Streamlit page settings
# This must be the first Streamlit command in the script
st.set_page_config(
    page_title="AI Content Generator",
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
    # HEADER SECTION
    # ========================================================================
    
    # Display the main application header
    st.title("✍️ AI Content Generator")
    st.markdown(
        "Generate high-quality blog posts using AI. "
        "Configure your content parameters in the sidebar and click generate."
    )
    
    # Add a visual separator
    st.divider()
    
    # ========================================================================
    # SIDEBAR - INPUT COLLECTION
    # ========================================================================
    
    # Render the sidebar and collect user inputs
    # This returns a dictionary with all input values and button state
    inputs = render_sidebar()
    
    # Optionally render sidebar footer with tips
    render_sidebar_footer()
    
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
            st.warning("⚠️ Please enter a topic for your blog post.")
            return
        
        if not inputs["audience"].strip():
            st.warning("⚠️ Please specify your target audience.")
            return
        
        # ====================================================================
        # LOADING STATE
        # ====================================================================
        
        # Display loading indicator while content is being generated
        # This provides visual feedback to the user
        with st.spinner("🤖 Generating your blog post... This may take a few moments."):
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
                    language=inputs["language"]
                )
                
                # ============================================================
                # SUCCESS STATE
                # ============================================================
                
                # Store the generated content in session state
                # This allows the content to persist across reruns
                st.session_state["last_generated_content"] = generated_content
                
                # Display success message
                st.success("✅ Blog post generated successfully!")
                
                # Render the generated content
                render_output(generated_content)
            
            except Exception as e:
                # ============================================================
                # ERROR STATE
                # ============================================================
                
                # Display user-friendly error message
                # Avoid exposing technical details that might confuse users
                render_error(str(e))
    
    else:
        # ====================================================================
        # EMPTY STATE OR DISPLAY PREVIOUS CONTENT
        # ====================================================================
        
        # Check if there's previously generated content in session state
        if "last_generated_content" in st.session_state:
            # Display the last generated content
            # This allows users to see their previous generation
            st.info("ℹ️ Showing previously generated content. Modify inputs and click Generate to create new content.")
            render_output(st.session_state["last_generated_content"])
        else:
            # No content has been generated yet
            # Display a friendly empty state with instructions
            render_empty_state()


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Entry point for the Streamlit application.
    
    This block is executed when the script is run directly.
    It simply calls the main() function to start the application.
    
    To run the application:
        streamlit run app/main.py
    """
    main()
