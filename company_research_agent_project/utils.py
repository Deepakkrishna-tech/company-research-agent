# company_research_agent_project/utils.py

import os
import streamlit as st
from dotenv import load_dotenv

def load_env_vars():
    """Loads environment variables from .env file."""
    load_dotenv()

def ensure_api_keys():
    """
    Checks for necessary API keys from environment variables.
    Displays warnings in Streamlit and stops execution if not found.
    """
    required_keys = ["TOGETHER_API_KEY", "TAVILY_API_KEY"]
    missing_keys = [key for key in required_keys if key not in os.environ or not os.environ[key]]

    if missing_keys:
        for key in missing_keys:
            st.error(f"{key} not set. Please set it as an environment variable or in a .env file.")
        st.info("Create a '.env' file in the project root (next to app.py) and add your keys like this:\n"
                "TOGETHER_API_KEY=\"YOUR_KEY_HERE\"\n"
                "TAVILY_API_KEY=\"YOUR_KEY_HERE\"")
        st.warning("The application will not function correctly without these API keys.")
        st.stop()
    return True

def normalize_url(url: str) -> str:
    """Adds https:// if scheme is missing from the URL."""
    if url and not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url