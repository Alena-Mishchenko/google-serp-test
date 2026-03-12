import os
import requests

API_KEY = os.getenv("SERPAPI_KEY")


def fetch_google_results(query: str):
    if not API_KEY:
        raise RuntimeError("API key is missing: SERPAPI_KEY is not set.")
    if not query:
        return []

    url = "https://serpapi.com/search.json"

    params = {
        "q": query,
        "engine": "google",
        "api_key": API_KEY,
        "hl": "cs",
        "gl": "cz",
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    organic = data.get("organic_results", [])

    return [
        {
            "title": item.get("title"),
            "link": item.get("link"),
            "snippet": item.get("snippet"),
        }
        for item in organic
    ]
