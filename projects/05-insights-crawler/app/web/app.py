from __future__ import annotations

import asyncio
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

from flask import Flask, render_template, request, send_file

from insights.config import Profile, CrawlerSettings
from insights.crawler import InsightsCrawler
from insights.crawler_async import AsyncInsightsCrawler
from insights.search_bootstrap import search_duckduckgo
from insights.storage import PageResult, ResultStore

app = Flask(__name__)

# Where we store the latest CSV for download
LATEST_OUTPUT = Path("output/latest-results.csv")


def _parse_csv_list(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    return [item.strip() for item in raw.split(",") if item.strip()]


def _derive_allowed_domains_from_urls(urls: List[str]) -> List[str]:
    domains: List[str] = []
    for u in urls:
        netloc = urlparse(u).netloc
        if netloc and netloc not in domains:
            domains.append(netloc)
    return domains


@app.route("/", methods=["GET", "POST"])
def index():
    results: Optional[List[PageResult]] = None
    error: Optional[str] = None

    if request.method == "POST":
        mode = request.form.get("mode", "urls")  # "urls" or "search"
        use_turbo = request.form.get("turbo") == "on"

        # Raw form values
        start_urls = _parse_csv_list(request.form.get("start_urls"))
        allowed_domains = _parse_csv_list(request.form.get("allowed_domains"))
        required_keywords = _parse_csv_list(request.form.get("required_keywords"))
        bonus_keywords = _parse_csv_list(request.form.get("bonus_keywords"))
        search_keywords = request.form.get("search_keywords", "") or ""

        try:
            max_depth = int(request.form.get("max_depth") or 1)
            max_pages = int(request.form.get("max_pages") or 50)
            min_score = int(request.form.get("min_score") or 2)
            request_delay_seconds = float(
                request.form.get("request_delay_seconds") or 1.0
            )
            same_domain_only = request.form.get("same_domain_only") == "on"
            max_search_results = int(request.form.get("max_search_results") or 10)
        except ValueError:
            error = "Numeric fields must contain valid numbers."
            return render_template(
                "index.html",
                results=None,
                error=error,
            )

        # --- Search bootstrap mode: keywords -> URLs via ddgs ---
        if mode == "search":
            if not search_keywords and not (required_keywords or bonus_keywords):
                error = "In search mode, please provide search keywords or required/bonus keywords."
                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                )

            query = search_keywords or " ".join(required_keywords + bonus_keywords)
            try:
                start_urls = search_duckduckgo(
                    query=query, max_results=max_search_results
                )
                print(
                    f"[INSIGHTS] Using search query={query!r}, start_urls from search: {start_urls}"
                )
            except Exception as exc:  # noqa: BLE001
                error = f"Error during search bootstrap: {exc}"
                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                )

            if not start_urls:
                error = "No results found from search. Try different keywords."
                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                )

            # If user didn't specify allowed_domains, derive from search results
            if not allowed_domains:
                allowed_domains = _derive_allowed_domains_from_urls(start_urls)

        # --- Validate we have something to crawl ---
        if not start_urls:
            error = "Please provide at least one start URL or use search mode."
            return render_template(
                "index.html",
                results=None,
                error=error,
            )

        profile = Profile(
            name="ad-hoc-search",
            start_urls=start_urls,
            max_depth=max_depth,
            same_domain_only=same_domain_only,
            required_keywords=required_keywords,
            bonus_keywords=bonus_keywords,
            min_score=min_score,
            max_pages=max_pages,
            request_delay_seconds=request_delay_seconds,
            allowed_domains=allowed_domains or None,
        )

        settings = CrawlerSettings()

        try:
            if use_turbo:
                crawler_async = AsyncInsightsCrawler(
                    profile, settings=settings, max_concurrency=10
                )
                results = asyncio.run(crawler_async.crawl_async())
            else:
                crawler = InsightsCrawler(profile, settings=settings)
                results = crawler.crawl()

            # Filter by min_score (so low-scoring pages can be dropped)
            results = [
                r
                for r in results
                if r.score >= profile.min_score or r.skipped_by_robots or r.error
            ]

            # Save CSV for download
            store = ResultStore(LATEST_OUTPUT)
            store.save_csv(results)
        except Exception as exc:  # noqa: BLE001
            error = f"Error during crawl: {exc}"
            results = None

    return render_template(
        "index.html",
        results=results,
        error=error,
    )


@app.route("/download")
def download():
    if not LATEST_OUTPUT.exists():
        return "No results available to download yet.", 404
    return send_file(
        LATEST_OUTPUT,
        as_attachment=True,
        download_name="insights-results.csv",
    )
