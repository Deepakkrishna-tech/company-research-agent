# Company Research Agent 🕵️

**A Streamlit-based application leveraging Large Language Models (LLMs) and web search capabilities to generate concise company profiles and recent news summaries.**

## Overview

The Company Research Agent is an MVP (Minimum Viable Product) designed to automate the initial stages of company research. By providing a company name and its homepage URL, users can quickly obtain a foundational understanding of the company, including a profile summary derived from its website and a digest of recent news articles. This tool utilizes LangChain for orchestrating LLM interactions, Together AI for language model access, and Tavily for performing targeted web searches for news.

The primary goal is to provide a quick, AI-powered first pass at company intelligence, saving users time and effort in their preliminary research tasks.

## Features

*   **Automated Company Profiling:** Extracts and summarizes key information from a company's homepage.
*   **Recent News Aggregation & Summarization:** Fetches recent news articles related to the company and provides concise summaries.
*   **Consolidated Reporting:** Combines the company profile and news highlights into a single, easy-to-read report.
*   **User-Friendly Interface:** Built with Streamlit for an interactive and straightforward user experience.
*   **Modular Agent-Based Architecture:** Utilizes separate agents for distinct tasks (profile generation, news gathering, report compilation).
*   **Configurable:** Key parameters like LLM models, content length, and search results can be adjusted via a configuration file.
*   **API Key Management:** Securely manages API keys using environment variables.

## Tech Stack

*   **Backend:** Python
*   **Frontend (UI):** Streamlit
*   **LLM Orchestration:** LangChain
*   **Language Model Provider:** Together AI (via `langchain-together`)
*   **Web Search (News):** Tavily API (via `tavily-python`)
*   **Web Content Extraction:** `BeautifulSoup4` (used by `WebBaseLoader` in LangChain)
*   **Environment Management:** `python-dotenv`

## Project Structure

The project is organized into the following key directories and files:

```
company_research_agent_project/
├── .env                            # Local environment variables (API keys - DO NOT COMMIT)
├── .env.example                    # Example for environment variables
├── .gitignore                      # Specifies intentionally untracked files that Git should ignore
├── requirements.txt                # Python dependencies
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration (LLM models, constants)
├── prompts.py                      # All LangChain prompt templates
├── llm_services.py                 # For initializing LLMs and other services
├── utils.py                        # Utility functions (e.g., API key checks, URL normalization)
└── agents/
    ├── __init__.py                 # Makes 'agents' a Python package
    ├── company_profile_agent.py    # Agent for generating company profiles
    ├── news_agent.py               # Agent for fetching and summarizing news
    └── report_generator_agent.py   # Agent for compiling the final report
```

## Setup and Installation

Follow these steps to set up and run the Company Research Agent locally:

### 1. Prerequisites

*   Python 3.9 or higher
*   Git
*   Access to Together AI and Tavily API keys

### 2. Clone the Repository

```bash
git clone https://github.com/Deepakkrishna-tech/company-research-agent.git
cd company-research-agent/company_research_agent_project
```

### 3. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

*   **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 4. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

API keys are required for Together AI (LLM) and Tavily (search).

1.  Create a `.env` file in the `company_research_agent_project` directory by copying the example file:
    ```bash
    # For Windows
    copy .env.example .env

    # For macOS/Linux
    cp .env.example .env
    ```
2.  Open the `.env` file and add your API keys:
    ```env
    TOGETHER_API_KEY="your_together_ai_api_key_here"
    TAVILY_API_KEY="your_tavily_api_key_here"
    ```
    **Note:** Ensure the `.env` file is listed in your `.gitignore` file to prevent accidental commits of your API keys.

## Running the Application

Once the setup is complete, you can run the Streamlit application:

```bash
streamlit run app.py
```

This will typically open the application in your default web browser (e.g., at `http://localhost:8501`).

## Usage

1.  Navigate to the application URL in your browser.
2.  Enter the **Company Name** in the designated input field.
3.  Enter the full **Company URL (Homepage)** (e.g., `https://www.example.com`) in the input field.
4.  Click the "Start Research" button.
5.  The application will process the request, displaying spinners for each stage (company profile, news search, report generation).
6.  Once complete, the Company Overview, Recent News Highlights, and the Full Compiled Report will be displayed.

## Configuration

Key operational parameters can be adjusted in the `config.py` file:

*   `DEFAULT_LLM_MODEL`: Specifies the default Together AI model to be used.
*   `LLM_TEMPERATURE`: Controls the randomness/creativity of the LLM responses.
*   `LLM_MAX_TOKENS`: Sets the maximum number of tokens the LLM can generate.
*   `MAX_WEBSITE_CONTENT_LENGTH`: Maximum characters to extract from a website for profiling.
*   `MAX_ARTICLE_CONTENT_LENGTH`: Maximum characters from a news article to use for summarization.
*   `TAVILY_MAX_RESULTS`: Number of news articles to fetch from Tavily.

## Agents

The core logic is divided into specialized agents:

*   **Company Profile Agent (`company_profile_agent.py`):**
    *   Takes a company URL as input.
    *   Uses `WebBaseLoader` to fetch the content of the company's homepage.
    *   Truncates the content to a manageable size (`MAX_WEBSITE_CONTENT_LENGTH`).
    *   Utilizes an LLM chain with a specific prompt (`COMPANY_PROFILE_PROMPT`) to generate a concise company profile.
*   **News Agent (`news_agent.py`):**
    *   Takes a company name as input.
    *   Uses the `TavilySearchResults` tool to find recent news articles related to the company.
    *   For each relevant article, it truncates the content (`MAX_ARTICLE_CONTENT_LENGTH`).
    *   Employs an LLM chain with a specific prompt (`NEWS_SUMMARY_PROMPT`) to summarize the article.
    *   Compiles a list of these summaries.
*   **Report Generator Agent (`report_generator_agent.py`):**
    *   Takes the company name, the generated profile summary, and the news summaries as input.
    *   Uses an LLM chain with a final prompt (`FINAL_REPORT_PROMPT`) to synthesize all the information into a coherent final report.

## Future Enhancements

While this is an MVP, potential future enhancements include:

*   **Enhanced Company Profile:** Deeper website crawling (sitemaps), handling JavaScript-heavy sites, more targeted information extraction.
*   **Advanced News Agent:** Increased number of results, date range filtering, sentiment analysis, re-ranking of news based on relevance.
*   **New Agent Types:**
    *   Industry Analysis Agent
    *   Competitor Identification Agent
    *   Basic Financials Summary Agent (if public data is accessible)
    *   SWOT Analysis Agent
*   **Improved Report Generation:** More structured report sections, user selection of report components, export options (PDF, Markdown).
*   **Robustness & Error Handling:** More granular error handling, implementation of retries (e.g., using `tenacity`) for API calls.
*   **Performance:** Asynchronous operations for long-running tasks, especially if deployed beyond basic Streamlit.
*   **UI/UX Improvements:** More granular progress indicators, clickable source links in news summaries, enhanced input validation.
*   **Configuration Management:** Externalizing more settings into a `config.yaml` or similar.
*   **Persistence:** Options to save generated reports, potentially build a knowledge base using vector stores.
*   **Evaluation Framework:** Implementing a framework for evaluating the quality of generated reports (e.g., using LangSmith or custom metrics).

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to contribute to the development, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to good coding practices and includes relevant documentation or comments.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file (if you choose to add one) for details.
*(Recommendation: Create a `LICENSE.md` file with the MIT License text if you want to use it).*

---

This README provides a comprehensive guide to understanding, setting up, and using the Company Research Agent.
```

**Next Steps for you:**

1.  **Create `README.md`**: Copy the content above into a new file named `README.md` in the root of your `company_research_agent` directory (the one that contains `company_research_agent_project/` and `.git/`).
2.  **(Optional but Recommended) Add a `LICENSE.md`**: If you want to use the MIT license (or another), create a `LICENSE.md` file in the root of your `company_research_agent` directory and paste the license text into it. You can easily find MIT license text online.
3.  **Add, Commit, and Push the README (and License) to GitHub**:
    ```bash
    git add README.md
    # If you added a license file:
    # git add LICENSE.md
    git commit -m "Add comprehensive README and project documentation"
    git push origin main
    ```

This will make your GitHub repository much more informative and welcoming to anyone who visits it.// filepath: c:\Users\Deepak\Documents\company_research_agent\README.md
# Company Research Agent 🕵️

**A Streamlit-based application leveraging Large Language Models (LLMs) and web search capabilities to generate concise company profiles and recent news summaries.**

## Overview

The Company Research Agent is an MVP (Minimum Viable Product) designed to automate the initial stages of company research. By providing a company name and its homepage URL, users can quickly obtain a foundational understanding of the company, including a profile summary derived from its website and a digest of recent news articles. This tool utilizes LangChain for orchestrating LLM interactions, Together AI for language model access, and Tavily for performing targeted web searches for news.

The primary goal is to provide a quick, AI-powered first pass at company intelligence, saving users time and effort in their preliminary research tasks.

## Features

*   **Automated Company Profiling:** Extracts and summarizes key information from a company's homepage.
*   **Recent News Aggregation & Summarization:** Fetches recent news articles related to the company and provides concise summaries.
*   **Consolidated Reporting:** Combines the company profile and news highlights into a single, easy-to-read report.
*   **User-Friendly Interface:** Built with Streamlit for an interactive and straightforward user experience.
*   **Modular Agent-Based Architecture:** Utilizes separate agents for distinct tasks (profile generation, news gathering, report compilation).
*   **Configurable:** Key parameters like LLM models, content length, and search results can be adjusted via a configuration file.
*   **API Key Management:** Securely manages API keys using environment variables.

## Tech Stack

*   **Backend:** Python
*   **Frontend (UI):** Streamlit
*   **LLM Orchestration:** LangChain
*   **Language Model Provider:** Together AI (via `langchain-together`)
*   **Web Search (News):** Tavily API (via `tavily-python`)
*   **Web Content Extraction:** `BeautifulSoup4` (used by `WebBaseLoader` in LangChain)
*   **Environment Management:** `python-dotenv`

## Project Structure

The project is organized into the following key directories and files:

```
company_research_agent_project/
├── .env                            # Local environment variables (API keys - DO NOT COMMIT)
├── .env.example                    # Example for environment variables
├── .gitignore                      # Specifies intentionally untracked files that Git should ignore
├── requirements.txt                # Python dependencies
├── app.py                          # Main Streamlit application
├── config.py                       # Configuration (LLM models, constants)
├── prompts.py                      # All LangChain prompt templates
├── llm_services.py                 # For initializing LLMs and other services
├── utils.py                        # Utility functions (e.g., API key checks, URL normalization)
└── agents/
    ├── __init__.py                 # Makes 'agents' a Python package
    ├── company_profile_agent.py    # Agent for generating company profiles
    ├── news_agent.py               # Agent for fetching and summarizing news
    └── report_generator_agent.py   # Agent for compiling the final report
```

## Setup and Installation

Follow these steps to set up and run the Company Research Agent locally:

### 1. Prerequisites

*   Python 3.9 or higher
*   Git
*   Access to Together AI and Tavily API keys

### 2. Clone the Repository

```bash
git clone https://github.com/Deepakkrishna-tech/company-research-agent.git
cd company-research-agent/company_research_agent_project
```

### 3. Create and Activate a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

*   **Windows:**
    ```bash
    python -m venv venv
    .\venv\Scripts\activate
    ```
*   **macOS/Linux:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

### 4. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

API keys are required for Together AI (LLM) and Tavily (search).

1.  Create a `.env` file in the `company_research_agent_project` directory by copying the example file:
    ```bash
    # For Windows
    copy .env.example .env

    # For macOS/Linux
    cp .env.example .env
    ```
2.  Open the `.env` file and add your API keys:
    ```env
    TOGETHER_API_KEY="your_together_ai_api_key_here"
    TAVILY_API_KEY="your_tavily_api_key_here"
    ```
    **Note:** Ensure the `.env` file is listed in your `.gitignore` file to prevent accidental commits of your API keys.

## Running the Application

Once the setup is complete, you can run the Streamlit application:

```bash
streamlit run app.py
```

This will typically open the application in your default web browser (e.g., at `http://localhost:8501`).

## Usage

1.  Navigate to the application URL in your browser.
2.  Enter the **Company Name** in the designated input field.
3.  Enter the full **Company URL (Homepage)** (e.g., `https://www.example.com`) in the input field.
4.  Click the "Start Research" button.
5.  The application will process the request, displaying spinners for each stage (company profile, news search, report generation).
6.  Once complete, the Company Overview, Recent News Highlights, and the Full Compiled Report will be displayed.

## Configuration

Key operational parameters can be adjusted in the `config.py` file:

*   `DEFAULT_LLM_MODEL`: Specifies the default Together AI model to be used.
*   `LLM_TEMPERATURE`: Controls the randomness/creativity of the LLM responses.
*   `LLM_MAX_TOKENS`: Sets the maximum number of tokens the LLM can generate.
*   `MAX_WEBSITE_CONTENT_LENGTH`: Maximum characters to extract from a website for profiling.
*   `MAX_ARTICLE_CONTENT_LENGTH`: Maximum characters from a news article to use for summarization.
*   `TAVILY_MAX_RESULTS`: Number of news articles to fetch from Tavily.

## Agents

The core logic is divided into specialized agents:

*   **Company Profile Agent (`company_profile_agent.py`):**
    *   Takes a company URL as input.
    *   Uses `WebBaseLoader` to fetch the content of the company's homepage.
    *   Truncates the content to a manageable size (`MAX_WEBSITE_CONTENT_LENGTH`).
    *   Utilizes an LLM chain with a specific prompt (`COMPANY_PROFILE_PROMPT`) to generate a concise company profile.
*   **News Agent (`news_agent.py`):**
    *   Takes a company name as input.
    *   Uses the `TavilySearchResults` tool to find recent news articles related to the company.
    *   For each relevant article, it truncates the content (`MAX_ARTICLE_CONTENT_LENGTH`).
    *   Employs an LLM chain with a specific prompt (`NEWS_SUMMARY_PROMPT`) to summarize the article.
    *   Compiles a list of these summaries.
*   **Report Generator Agent (`report_generator_agent.py`):**
    *   Takes the company name, the generated profile summary, and the news summaries as input.
    *   Uses an LLM chain with a final prompt (`FINAL_REPORT_PROMPT`) to synthesize all the information into a coherent final report.

## Future Enhancements

While this is an MVP, potential future enhancements include:

*   **Enhanced Company Profile:** Deeper website crawling (sitemaps), handling JavaScript-heavy sites, more targeted information extraction.
*   **Advanced News Agent:** Increased number of results, date range filtering, sentiment analysis, re-ranking of news based on relevance.
*   **New Agent Types:**
    *   Industry Analysis Agent
    *   Competitor Identification Agent
    *   Basic Financials Summary Agent (if public data is accessible)
    *   SWOT Analysis Agent
*   **Improved Report Generation:** More structured report sections, user selection of report components, export options (PDF, Markdown).
*   **Robustness & Error Handling:** More granular error handling, implementation of retries (e.g., using `tenacity`) for API calls.
*   **Performance:** Asynchronous operations for long-running tasks, especially if deployed beyond basic Streamlit.
*   **UI/UX Improvements:** More granular progress indicators, clickable source links in news summaries, enhanced input validation.
*   **Configuration Management:** Externalizing more settings into a `config.yaml` or similar.
*   **Persistence:** Options to save generated reports, potentially build a knowledge base using vector stores.
*   **Evaluation Framework:** Implementing a framework for evaluating the quality of generated reports (e.g., using LangSmith or custom metrics).

## Contributing

Contributions are welcome! If you have suggestions for improvements or want to contribute to the development, please feel free to:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

Please ensure your code adheres to good coding practices and includes relevant documentation or comments.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file (if you choose to add one) for details.
*(Recommendation: Create a `LICENSE.md` file with the MIT License text if you want to use it).*

---

This README provides a comprehensive guide to understanding, setting up, and using the Company Research Agent.
```