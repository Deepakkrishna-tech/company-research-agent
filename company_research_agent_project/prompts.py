# company_research_agent_project/prompts.py

from langchain.prompts import PromptTemplate

COMPANY_PROFILE_PROMPT_TEMPLATE = """
Based on the following content from the company's website ({company_url}), provide a concise overview of the company.
Focus on:
1. What the company does (its main products/services).
2. Its stated mission or primary goal, if apparent.
3. Its target audience or industry, if clear.

Keep the overview to 3-4 concise paragraphs.

Website Content:
{website_content}

Concise Company Overview:
"""
COMPANY_PROFILE_PROMPT = PromptTemplate(
    input_variables=["company_url", "website_content"],
    template=COMPANY_PROFILE_PROMPT_TEMPLATE,
)

NEWS_SUMMARY_PROMPT_TEMPLATE = """
You are a helpful assistant. Based on the following news article content, provide a 1-2 sentence summary.
Focus on the key takeaway of the article regarding the company {company_name}.

Article Content:
{article_content}

Summary:
"""
NEWS_SUMMARY_PROMPT = PromptTemplate(
    input_variables=["company_name", "article_content"],
    template=NEWS_SUMMARY_PROMPT_TEMPLATE,
)

FINAL_REPORT_PROMPT_TEMPLATE = """
You are a research assistant. Compile a brief company research report for {company_name} using the information provided.
Structure the report with the following sections:
1. Company Overview
2. Recent News Highlights

Use a professional and informative tone. Ensure the report flows well.

Provided Information:
--- Company Overview ---
{profile_summary}

--- Recent News ---
{news_summaries}

---
Company Research Report for {company_name}:
"""
FINAL_REPORT_PROMPT = PromptTemplate(
    input_variables=["company_name", "profile_summary", "news_summaries"],
    template=FINAL_REPORT_PROMPT_TEMPLATE,
)