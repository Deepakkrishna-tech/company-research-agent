# company_research_agent_project/agents/company_profile_agent.py

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate # Import PromptTemplate
from prompts import COMPANY_PROFILE_PROMPT
from config import MAX_WEBSITE_CONTENT_LENGTH

@st.cache_data(show_spinner=False) # show_spinner=False is fine if app.py handles spinners
def run_company_profile_agent(_llm, company_url: str): # Renamed llm to _llm
    """
    Fetches content from a company URL, truncates it, and generates a profile summary using an LLM.
    """
    # UI feedback like st.write is generally better handled in app.py with st.spinner,
    # especially for cached functions, as they only run on a cache miss.
    # However, if this is intended as a log that only appears when processing happens, it's okay.
    # print(f"Company Profile Agent: Fetching content from {company_url}...") # Use print for server-side logs

    try:
        loader = WebBaseLoader(
            web_paths=[company_url],
            continue_on_failure=True, # Good practice
        )
        docs = loader.load()

        if not docs or not docs[0].page_content:
            # st.warning(f"Could not retrieve significant content from {company_url}.") # Better handled in app.py
            return f"No detailed company profile information could be retrieved from {company_url}. The page might be empty, protected, or require JavaScript."

        content = docs[0].page_content
        
        if len(content) > MAX_WEBSITE_CONTENT_LENGTH:
            content = content[:MAX_WEBSITE_CONTENT_LENGTH]
            # st.caption(f"Note: Website content was truncated to {MAX_WEBSITE_CONTENT_LENGTH} characters for processing.")
            # This kind of note is also better surfaced in app.py if needed, or logged.
            # For now, we'll assume the truncation is an internal detail.
            # If you want to inform the user, return this info as part of the result or a separate status.

        # Ensure COMPANY_PROFILE_PROMPT is a PromptTemplate instance
        if isinstance(COMPANY_PROFILE_PROMPT, str):
            prompt_template_to_use = PromptTemplate.from_template(COMPANY_PROFILE_PROMPT)
        elif isinstance(COMPANY_PROFILE_PROMPT, PromptTemplate):
            prompt_template_to_use = COMPANY_PROFILE_PROMPT
        else:
            # st.error("COMPANY_PROFILE_PROMPT is not a valid string or PromptTemplate instance.") # Better handled in app.py
            return "Failed to generate company profile due to invalid prompt configuration."

        profile_chain = LLMChain(llm=_llm, prompt=prompt_template_to_use) # Use _llm
        
        input_data = {"company_url": company_url, "website_content": content}
        summary_output = profile_chain.invoke(input_data)
        
        # LLMChain output is a dictionary, typically with the result under the 'text' key.
        summary = summary_output.get('text')

        if summary is None:
            # st.warning(f"Profile generation for {company_url} did not produce a 'text' field. Raw: {summary_output}")
            summary = str(summary_output) # Fallback

        return summary

    except Exception as e:
        # st.error(f"Error in Company Profile Agent for {company_url}: {e}") # Better handled in app.py
        # For debugging, you might want to log the full traceback
        # import traceback
        # print(f"Error in Company Profile Agent for {company_url}: {e}\n{traceback.format_exc()}")
        return f"Failed to generate company profile for {company_url} due to an error: {str(e)}"