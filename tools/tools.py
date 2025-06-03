from langchain_community.tools.tavily_search import TavilySearchResults

from conf import TAVILY_TOKEN


def get_profile_url_tavily(name: str, max_results_to_check: int = 2) -> str:
    """Search for linkedin or Twitter page"""
    print(f"--- Tool: get_profile_url_tavily ---")
    print(f"--- Searching for LinkedIn profile of: {name} ---")

    search = TavilySearchResults(max_results=max_results_to_check)
    res = search.run(f"{name}")
    print(f"--- Tool: Response ---")
    print(res)
    return res[0]["url"]
