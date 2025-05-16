# company_research_agent_project/agents/news_agent.py

import streamlit as st
from langchain.chains import LLMChain
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate # Import PromptTemplate
from prompts import NEWS_SUMMARY_PROMPT
from config import TAVILY_MAX_RESULTS, MAX_ARTICLE_CONTENT_LENGTH

@st.cache_data(show_spinner=False) # show_spinner=False is fine if app.py handles spinners
def run_news_agent(_llm, company_name: str): # Renamed llm to _llm
    """
    Searches for news about a company using Tavily and summarizes relevant articles using an LLM.
    """
    # print(f"News Agent: Searching for news about {company_name} using Tavily...") # Use print for server-side logs

    try:
        tavily_search = TavilySearchResults(max_results=TAVILY_MAX_RESULTS)
        # Note: TavilySearchResults can sometimes return a string error message directly
        # or a list of dictionaries. Robust handling might be needed if API errors are common.
        search_results_raw = tavily_search.invoke(company_name)

        if isinstance(search_results_raw, str): # Handle cases where Tavily returns an error string
            # st.warning(f"Tavily search for {company_name} returned an error: {search_results_raw}")
            return f"Could not retrieve news for {company_name} from Tavily: {search_results_raw}"

        if not search_results_raw:
            # st.warning(f"No news found for {company_name} via Tavily.") # Better handled in app.py
            return "No recent news highlights found for this company."

        summaries = []
        
        # Ensure NEWS_SUMMARY_PROMPT is a PromptTemplate instance
        if isinstance(NEWS_SUMMARY_PROMPT, str):
            prompt_template_to_use = PromptTemplate.from_template(NEWS_SUMMARY_PROMPT)
        elif isinstance(NEWS_SUMMARY_PROMPT, PromptTemplate):
            prompt_template_to_use = NEWS_SUMMARY_PROMPT
        else:
            # st.error("NEWS_SUMMARY_PROMPT is not a valid string or PromptTemplate instance.") # Better handled in app.py
            return "Failed to generate news summaries due to invalid prompt configuration."

        news_summary_chain = LLMChain(llm=_llm, prompt=prompt_template_to_use) # Use _llm

        for result_item in search_results_raw:
            # Tavily results are typically dictionaries
            if isinstance(result_item, dict) and result_item.get("content") and result_item.get("url"):
                # print(f"News Agent: Summarizing news: {result_item.get('title', result_item['url'])}") # Server-side log
                article_content = result_item["content"]
                
                if len(article_content) > MAX_ARTICLE_CONTENT_LENGTH:
                    article_content = article_content[:MAX_ARTICLE_CONTENT_LENGTH] + "..."
                
                summary_input = {
                    "company_name": company_name, 
                    "article_content": article_content
                }
                summary_output = news_summary_chain.invoke(summary_input)
                summary = summary_output.get('text', str(summary_output)) # Fallback if 'text' key is missing
                
                summaries.append(f"- {summary} (Source: {result_item['url']})")
        
        return "\n".join(summaries) if summaries else "No relevant news summaries could be generated from the found articles."
    
    except Exception as e:
        # st.error(f"Error in News Agent for {company_name}: {e}") # Better handled in app.py
        # For debugging:
        # import traceback
        # print(f"Error in News Agent for {company_name}: {e}\n{traceback.format_exc()}")
        return f"Failed to generate news highlights for {company_name} due to an error: {str(e)}"