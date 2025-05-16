# company_research_agent_project/llm_services.py

import os
from langchain_together.chat_models import ChatTogether
from dotenv import load_dotenv
from config import DEFAULT_LLM_MODEL, LLM_TEMPERATURE, LLM_MAX_TOKENS # Changed from .config

# Load environment variables from .env file at the module level
load_dotenv()

_llm_instance = None
_llm_config_params = {} # To store the params used for the cached instance

def get_llm(model_name: str = None, temperature: float = None, max_tokens: int = None):
    global _llm_instance, _llm_config_params
    
    together_api_key = os.getenv("TOGETHER_API_KEY")
    if not together_api_key:
        # It's better to raise an error here so the calling code (e.g., app.py)
        # can catch it and display a user-friendly message.
        # Printing here might get lost if not run from a visible console.
        raise ValueError("TOGETHER_API_KEY not found in environment variables. Please set it in your .env file.")

    # Determine current parameters, falling back to defaults from config.py
    current_model = model_name or DEFAULT_LLM_MODEL
    current_temp = temperature if temperature is not None else LLM_TEMPERATURE
    current_max_tokens = max_tokens or LLM_MAX_TOKENS

    # Create a dictionary of current parameters for easy comparison
    current_params = {
        "model": current_model,
        "temperature": current_temp,
        "max_tokens": current_max_tokens,
        "together_api_key": together_api_key # API key is also part of the config
    }

    # Check if a cached instance exists and if its configuration matches current parameters
    if _llm_instance and _llm_config_params == current_params:
        # print("Returning cached LLM instance.") # Optional: for debugging
        return _llm_instance

    # print("Initializing new LLM instance...") # Optional: for debugging
    try:
        new_llm_instance = ChatTogether(
            model=current_model,
            temperature=current_temp,
            max_tokens=current_max_tokens,
            together_api_key=together_api_key
        )
        _llm_instance = new_llm_instance
        _llm_config_params = current_params # Cache the params used for this instance
        # print(f"LLM Initialized with: model={current_model}, temp={current_temp}, tokens={current_max_tokens}") # Optional
        return _llm_instance
    except Exception as e:
        # Log the error or handle it more gracefully
        # Re-raising allows the caller (app.py) to handle UI updates
        print(f"Error during ChatTogether initialization: {e}") # Keep for server-side logs
        _llm_instance = None # Ensure instance is None if initialization fails
        _llm_config_params = {} # Clear cached params
        raise RuntimeError(f"Failed to initialize the Language Model: {e}") # Re-raise for app.py to catch