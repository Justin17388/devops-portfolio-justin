from typing import List

from ddgs import DDGS


def search_duckduckgo(query: str, max_results: int = 10) -> List[str]:
    """
    Use the `ddgs` package to turn a text query into a list of URLs.

    This is a metasearch library that can hit multiple backends (google, brave, etc.),
    so it's more robust than scraping HTML directly.
    """
    urls: List[str] = []

    # You can tweak backend, region, safesearch if needed.
    # We'll keep it simple and rely on defaults + max_results.
    with DDGS() as ddgs:
        for result in ddgs.text(query, max_results=max_results):
            # Depending on backend, results may use 'href' or 'url'
            href = result.get("href") or result.get("url")
            if href and href.startswith("http"):
                urls.append(href)

    print(f"[INSIGHTS] DDGS search query={query!r}, collected {len(urls)} URLs")
    for i, u in enumerate(urls, start=1):
        print(f"  {i}. {u}")

    return urls
