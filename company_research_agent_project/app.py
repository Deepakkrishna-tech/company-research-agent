# company_research_agent_project/app.py

import sys
import os

# Add the project root to the Python path
# This allows us to use absolute imports from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
from utils import load_env_vars, ensure_api_keys, normalize_url # These are now found via PROJECT_ROOT
from llm_services import get_llm
from agents import ( # This will use the updated agents/__init__.py
    run_company_profile_agent,
    run_news_agent,
    run_report_generation_agent
)

# --- Page Configuration ---
st.set_page_config(page_title="Company Research Agent MVP", layout="wide")

# --- Load Environment Variables and Check API Keys ---
load_env_vars() # Load .env file if present

def main():
    st.title("Company Research Agent 🕵️")
    st.caption("Generates company profile research and news summary.")

    if not ensure_api_keys(): # This will st.stop() if keys are missing
        return

    try:
        llm = get_llm()
    except Exception as e:
        st.error(f"Failed to initialize the Language Model: {e}")
        st.error("Please check your TOGETHER_API_KEY and network connection.")
        st.stop()

    with st.sidebar:
        st.header("Research Parameters")
        company_name_input = st.text_input("Company Name *", placeholder="e.g., OpenAI")
        company_url_input = st.text_input("Company URL (Homepage)", placeholder="e.g., https://openai.com")
        
        start_research_button = st.button("Start Research", type="primary", use_container_width=True)
        st.markdown("---")
        st.header("About")
        st.info(
            "This is an MVP of a Company Research Agent using LangChain, Together AI, and Tavily. "
            "It provides a basic company overview and recent news highlights."
        )

    if start_research_button:
        if not company_name_input:
            st.error("Company Name is required.")
            st.stop()
        
        normalized_company_url = normalize_url(company_url_input) if company_url_input else ""

        st.subheader(f"Research Report for: {company_name_input}")
        
        profile_summary = "Company profile requires a valid URL and could not be generated."
        if normalized_company_url:
            with st.spinner(f"🕵️ Gathering company profile for {company_name_input}... (from {normalized_company_url})"):
                profile_summary = run_company_profile_agent(llm, normalized_company_url)
            st.success("Company Profile agent finished.")
        else:
            st.warning("Skipping company profile generation as no URL was provided.") # Changed to warning
        
        with st.spinner(f"📰 Searching for news about {company_name_input}..."):
            news_summaries = run_news_agent(llm, company_name_input)
        st.success("News Agent finished.")

        with st.spinner("📝 Generating final report..."):
            final_report = run_report_generation_agent(llm, company_name_input, profile_summary, news_summaries)
        st.success("Report generation finished!")
        st.balloons()

        st.markdown("---")
        st.markdown("### Company Overview")
        st.markdown(profile_summary if profile_summary else "Not generated or URL not provided.")
        
        st.markdown("### Recent News Highlights")
        st.markdown(news_summaries if news_summaries else "No news found or generated.")
        
        st.markdown("---")
        st.markdown("### Full Compiled Report")
        st.markdown(final_report)

    # REMOVE OR COMMENT OUT THE FOLLOWING SECTION:
    # with st.expander("Future Enhancements & Notes (Developer View)"):
    #     st.markdown("""
    #     **MVP Evaluation:**
    #     1. Manual Review: Accuracy, relevance, coherence for 5-10 diverse companies.
    #     2. Robustness: Invalid URLs, no news, long content.

    #     **Upscaling Measures & Next Steps:**
    #     1.  **Enhanced Company Profile:** Sitemap crawling, JS site handling (Playwright/Selenium), targeted extraction.
    #     2.  **Advanced News Agent:** More results, date filtering, sentiment analysis, re-ranking.
    #     3.  **New Agents:** Industry Analysis, Competitor ID, Financials, SWOT.
    #     4.  **Improved Report Gen:** More sections, user selection, PDF/Markdown export.
    #     5.  **Robustness:** Granular error handling, retries (`tenacity`).
    #     6.  **Performance:** Async operations for long tasks if deployed beyond basic Streamlit.
    #     7.  **LangChain Agents:** Convert functions to full LangChain Agents for complex tool use/decision-making.
    #     8.  **UI/UX:** Granular progress, clickable sources, better input validation.
    #     9.  **Config:** Externalize more settings (e.g., `config.yaml`).
    #     10. **Persistence:** Save reports, vector stores for knowledge base.
    #     11. **Evaluation Framework:** LangSmith, golden datasets, automated metrics.
    #     12. **Code Structure:** Continue refining modules as complexity grows.
    #     """)

if __name__ == "__main__":
    main()