import requests


def scrape_linkedin_profile(linked_profile_url: str, mock: bool = False):
    """
    scrape information from linkedIn profiles
    :param linked_profile_url:
    :param mock:
    """
    mock_url = "https://gist.githubusercontent.com/ikhlas-firlana/e9da243b26e5a48cd577d5d9c933283f/raw" \
               "/bad5481d33aacde3435e7d97e64f6bfe66f6b55e/linkedin-ikhlas-apify.json"
    data = None
    if mock:
        response = requests.get(mock_url, timeout=10)
        data = response.json()[0]

    return data
