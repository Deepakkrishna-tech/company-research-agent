# company_research_agent_project/config.py

# LLM Configuration
DEFAULT_LLM_MODEL = "mistralai/Mistral-7B-Instruct-v0.3"
# You can add other models here and allow selection in the UI later
# E.g., LLAMA_3_8B_INSTRUCT = "meta-llama/Llama-3-8b-chat-hf"

LLM_TEMPERATURE = 0.2
LLM_MAX_TOKENS = 1024

# Content Processing
MAX_WEBSITE_CONTENT_LENGTH = 8000 # Max characters from website to feed to LLM
MAX_ARTICLE_CONTENT_LENGTH = 4000 # Max characters from news article for summarization

# Tavily Search
TAVILY_MAX_RESULTS = 3