from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from agents import function_tool

CUSTOM_SEARCH_ENGINE_ID = "42389273c2ea947a1" 

@function_tool
def general_web_search(query: str) -> str:
    """
    Performs a web search to find recent news, sentiment, and broad market trends.
    
    Args:
        query: The search query to execute (e.g., 'latest market sentiment Consumer Staples 2025').
    
    Returns:
        A string summary of the top search results or an error message.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "ERROR: GOOGLE_API_KEY is not set in environment variables."
        
    try:
        service = build("customsearch", "v1", developerKey=api_key)
        result = service.cse().list(
            q=query,
            cx=CUSTOM_SEARCH_ENGINE_ID,
            num=5  
        ).execute()
    
    except HttpError as e:
        return f"ERROR: Google Search API returned an HTTP error. Check daily quota. Error: {e}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred during search execution: {e}"

    search_results_markdown = ""
    items = result.get('items', [])
    
    if not items:
        return f"Search for '{query}' returned no relevant results."

    for i, item in enumerate(items, 1):
        title = item.get('title', 'No Title')
        snippet = item.get('snippet', 'No Snippet')
        search_results_markdown += (
            f"Result {i}. Title: {title}. Snippet: {snippet}\n"
        )
        
    return (
        f"General web search completed. Summarized results for '{query}':\n\n"
        f"{search_results_markdown}"
    )