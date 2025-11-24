from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Profile:
    """
    Crawling + scoring configuration for a single run.
    For the web UI, this is built in memory from form input.
    """

    name: str
    start_urls: List[str]
    max_depth: int
    same_domain_only: bool
    required_keywords: List[str]
    bonus_keywords: List[str]
    min_score: int
    max_pages: int
    request_delay_seconds: float
    allowed_domains: Optional[List[str]]


@dataclass
class CrawlerSettings:
    timeout: int = 10
    user_agent: str = (
        "InsightsCrawler/1.0 (+https://github.com/Justin17388/devops-portfolio-justin)"
    )
