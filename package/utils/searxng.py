import requests
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from urllib.parse import urlencode, urlparse

# Equivalent to `getSearxngApiEndpoint()` in TypeScript
def get_searxng_api_endpoint() -> str:
    return "http://localhost:8080"  # Or your Docker container address


class SearxngSearchOptions(BaseModel):
    categories: Optional[List[str]] = None
    engines: Optional[List[str]] = None
    language: Optional[str] = None
    pageno: Optional[int] = None


class SearxngSearchResult(BaseModel):
    title: str
    url: str
    img_src: Optional[str] = None
    thumbnail_src: Optional[str] = None
    thumbnail: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    iframe_src: Optional[str] = None


class SearxngSearchResponse(BaseModel):
    results: List[SearxngSearchResult]
    # suggestions: List[str]


def get_searxng_query(query, whitelist: List[str] = None):
    if whitelist:
        whitelist = [f"site:{wl}" for wl in whitelist]
        query = f"{query} ({' OR '.join(whitelist)})"
    return query


def search_searxng(query: str, whitelist: List[str] = None, opts: Optional[SearxngSearchOptions] = None) -> SearxngSearchResponse:
    """this function will be fixed in the logic later, since current logis in for loop quite messy"""
    base_url = f"{get_searxng_api_endpoint()}/search?format=json"
    params = {'q': get_searxng_query(query, whitelist)}

    if opts:
        for key, value in opts.model_dump(exclude_none=True).items():
            if isinstance(value, list):
                params[key] = ','.join(value)
            else:
                params[key] = str(value)

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()
    results = []
    suggestions = []
    for result in data["results"]:
        url = result.get("url", None)
        if url and url.startswith("https"):
            parsed_url = urlparse(url)
            domain = parsed_url.netloc
        if domain.startswith("www."):
            domain = domain[4:]
        if whitelist:
            # if any(domain == wl or domain.endswith(f".{wl}") for wl in whitelist):
            if any(wl in domain for wl in whitelist):
                results.append(result)
        else:
            results.append(result)
    return SearxngSearchResponse(results=results)
