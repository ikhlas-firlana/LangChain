import os

import requests


def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """
    scrape information from linkedin profiles
    :param linkedin_profile_url:
    :param mock:
    """
    # mock_url = "https://gist.githubusercontent.com/ikhlas-firlana/e9da243b26e5a48cd577d5d9c933283f/raw" \
    #            "/bad5481d33aacde3435e7d97e64f6bfe66f6b55e/linkedin-ikhlas-apify.json"
    mock_url = "https://gist.githubusercontent.com/ikhlas-firlana/0f676e9e7d6f80c5ac15cca3b9fdb646/raw" \
               "/384a50ad804b5ed313e36377fb792fdf819e229b/linkedin-ikhlas-proxycurl.json"
    if mock:
        response = requests.get(mock_url, timeout=10)
        return response.json()
    else:
        api_key = os.getenv('PROXYCURL_API')
        headers = {'Authorization': 'Bearer ' + api_key}
        api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
        response = requests.get(
            api_endpoint,
            params={'url': linkedin_profile_url},
            headers=headers
        )
        return response.json()