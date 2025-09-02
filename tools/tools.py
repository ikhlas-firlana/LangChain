import conf
from langchain_community.tools.tavily_search import TavilySearchResults

from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool


def get_profile_url_tavily(name: str, max_results_to_check: int = 2) -> str:
    """Search for linkedin or Twitter page"""
    print(f"--- Tool: get_profile_url_tavily ---")
    print(f"--- Searching for LinkedIn profile of: {name} ---")

    search = TavilySearchResults(max_results=max_results_to_check)
    res = search.run(f"{name}")
    print(f"--- Tool: Response ---")
    print(res)
    return res[0]["url"]


def get_profile_url_linkedin_from_google(name: str) -> str:
    print(f"--- Tool: get_profile_url_linkedin_from_google ---")
    print(f"--- Searching for LinkedIn profile of: {name} ---")
    """
        Finds the LinkedIn profile URL for a given name and optional company
        using a targeted Google Search.

        Returns the first result found.
        """
    # Instantiate the search tool
    search_google = GoogleSearchAPIWrapper()

    # Craft a precise query
    query = f'site:linkedin.com/in/ "{name}"'
    print(f"Executing search query: {query}")

    # Run the search tool
    # The result is typically a list of snippets and links.
    # We will parse it to find the most likely URL.
    results = search_google.results(query, num_results=1)

    if not results:
        return "No LinkedIn profile found."
    print(results)

    # The 'results' method returns a list of dictionaries.
    # We extract the link from the first result.
    first_result = results[0]
    if "link" in first_result:
        return first_result["link"]
    else:
        return "Could not extract a link from the search result."
