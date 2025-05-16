# company_research_agent_project/agents/report_generator_agent.py

import streamlit as st
from langchain.chains import LLMChain
from langchain_core.prompts import PromptTemplate # Ensure this is the base class for your prompt
from prompts import FINAL_REPORT_PROMPT # Assuming FINAL_REPORT_PROMPT is a PromptTemplate instance or a string

# This decorator is added if you want to cache the results of this function.
# If you add it, the 'llm' parameter should be prefixed with an underscore.
@st.cache_data 
def run_report_generation_agent(_llm, company_name: str, profile_summary: str, news_summaries: str): # Renamed llm to _llm
    """
    Generates a final report by combining company profile and news summaries using an LLM.
    """
    # st.write(f"Compiling final report for {company_name}...") # UI feedback like this is better handled in app.py with st.spinner

    try:
        # Ensure FINAL_REPORT_PROMPT is a PromptTemplate instance
        # If FINAL_REPORT_PROMPT from prompts.py is a string, it needs to be converted.
        if isinstance(FINAL_REPORT_PROMPT, str):
            prompt_template_to_use = PromptTemplate.from_template(FINAL_REPORT_PROMPT)
        elif isinstance(FINAL_REPORT_PROMPT, PromptTemplate):
            prompt_template_to_use = FINAL_REPORT_PROMPT
        else:
            st.error("FINAL_REPORT_PROMPT is not a valid string or PromptTemplate instance.")
            return "Failed to generate final report due to invalid prompt configuration."

        report_chain = LLMChain(llm=_llm, prompt=prompt_template_to_use) # Use _llm
        
        input_data = {
            "company_name": company_name,
            "profile_summary": profile_summary if profile_summary else "No profile summary available.",
            "news_summaries": news_summaries if news_summaries else "No news summaries available."
        }
        
        report_output = report_chain.invoke(input_data)
        
        # LLMChain output is a dictionary, typically with the result under the 'text' key.
        final_report = report_output.get('text')
        
        if final_report is None:
            st.warning(
                f"Report generation for {company_name} did not produce a 'text' field in the output. "
                f"Raw output: {report_output}"
            )
            # Fallback to converting the entire output to string if 'text' key is missing.
            final_report = str(report_output) 

        return final_report
        
    except Exception as e:
        st.error(f"Error in Report Generation Agent for {company_name}: {e}")
        # For debugging, you might want to log the full traceback
        # import traceback
        # print(traceback.format_exc())
        return f"Failed to generate final report for {company_name} due to an error."