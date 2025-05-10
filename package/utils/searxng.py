import requests
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from urllib.parse import urlencode

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
    suggestions: List[str]

def search_searxng(query: str, opts: Optional[SearxngSearchOptions] = None) -> SearxngSearchResponse:
    base_url = f"{get_searxng_api_endpoint()}/search?format=json"
    params = {'q': query}

    if opts:
        for key, value in opts.model_dump(exclude_none=True).items():
            if isinstance(value, list):
                params[key] = ','.join(value)
            else:
                params[key] = str(value)

    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    return SearxngSearchResponse(results=data['results'], suggestions=data.get('suggestions', []))
