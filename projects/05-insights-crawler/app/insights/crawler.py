import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

from .config import Profile, CrawlerSettings
from .scoring import score_text
from .storage import PageResult


@dataclass
class CrawlState:
    visited: Set[str]
    queue: Deque[Tuple[str, int]]  # (url, depth)
    pages_processed: int


class InsightsCrawler:
    """
    Synchronous, ethical crawler:
    - Respects robots.txt
    - Applies per-domain delay
    - Honors allowed_domains, max_depth, max_pages
    """

    def __init__(
        self, profile: Profile, settings: Optional[CrawlerSettings] = None
    ) -> None:
        self.profile = profile
        self.settings = settings or CrawlerSettings()
        self._robots_cache: Dict[str, Optional[robotparser.RobotFileParser]] = {}
        self._last_request_time: Dict[str, float] = {}

    def _domain_allowed(self, url: str) -> bool:
        if not self.profile.allowed_domains:
            return True
        netloc = urlparse(url).netloc
        return any(netloc.endswith(domain) for domain in self.profile.allowed_domains)

    def _same_domain(self, base: str, url: str) -> bool:
        base_netloc = urlparse(base).netloc
        target_netloc = urlparse(url).netloc
        return base_netloc == target_netloc

    def _get_robots(self, url: str) -> Optional[robotparser.RobotFileParser]:
        netloc = urlparse(url).netloc
        if netloc in self._robots_cache:
            return self._robots_cache[netloc]

        robots_url_https = f"https://{netloc}/robots.txt"
        robots_url_http = f"http://{netloc}/robots.txt"
        rp = robotparser.RobotFileParser()

        for robots_url in (robots_url_https, robots_url_http):
            try:
                rp.set_url(robots_url)
                rp.read()
                self._robots_cache[netloc] = rp
                return rp
            except Exception:
                continue

        self._robots_cache[netloc] = None
        return None

    def _allowed_by_robots(self, url: str) -> bool:
        rp = self._get_robots(url)
        if rp is None:
            return True
        return rp.can_fetch(self.settings.user_agent, url)

    def _apply_rate_limit(self, url: str) -> None:
        netloc = urlparse(url).netloc
        last = self._last_request_time.get(netloc)
        delay = self.profile.request_delay_seconds
        if last is not None and delay > 0:
            elapsed = time.perf_counter() - last
            if elapsed < delay:
                time.sleep(delay - elapsed)

    def _extract_links(self, html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            absolute = urljoin(base_url, href)
            links.append(absolute)
        return links

    def _extract_title_and_text(self, html: str) -> Tuple[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        text = soup.get_text(separator=" ", strip=True)
        return title, text

    def crawl(self) -> List[PageResult]:
        state = CrawlState(
            visited=set(),
            queue=deque(),
            pages_processed=0,
        )

        for url in self.profile.start_urls:
            state.queue.append((url, 0))

        results: List[PageResult] = []

        with tqdm(desc=f"Crawling profile: {self.profile.name}", unit="page") as pbar:
            while state.queue and state.pages_processed < self.profile.max_pages:
                url, depth = state.queue.popleft()

                if url in state.visited:
                    continue
                state.visited.add(url)

                if depth > self.profile.max_depth:
                    continue

                if not self._domain_allowed(url):
                    continue

                if not self._allowed_by_robots(url):
                    results.append(
                        PageResult(
                            url=url,
                            title="",
                            status_code=None,
                            elapsed_ms=None,
                            score=0.0,
                            matched_required=[],
                            matched_bonus=[],
                            snippet="",
                            skipped_by_robots=True,
                            error=None,
                        )
                    )
                    state.pages_processed += 1
                    pbar.update(1)
                    continue

                try:
                    self._apply_rate_limit(url)
                    start = time.perf_counter()
                    resp = requests.get(
                        url,
                        timeout=self.settings.timeout,
                        headers={"User-Agent": self.settings.user_agent},
                    )
                    elapsed_ms = (time.perf_counter() - start) * 1000.0
                    self._last_request_time[urlparse(url).netloc] = time.perf_counter()

                    status_code = resp.status_code
                    content_type = resp.headers.get("Content-Type", "")
                    html = resp.text if "text/html" in content_type else ""
                except Exception as exc:  # noqa: BLE001
                    results.append(
                        PageResult(
                            url=url,
                            title="",
                            status_code=None,
                            elapsed_ms=None,
                            score=0.0,
                            matched_required=[],
                            matched_bonus=[],
                            snippet="",
                            skipped_by_robots=False,
                            error=str(exc),
                        )
                    )
                    state.pages_processed += 1
                    pbar.update(1)
                    continue

                title, text = self._extract_title_and_text(html) if html else ("", "")
                score_res = score_text(text, self.profile)
                snippet = text[:300] if text else ""

                results.append(
                    PageResult(
                        url=url,
                        title=title,
                        status_code=status_code,
                        elapsed_ms=elapsed_ms,
                        score=score_res.score,
                        matched_required=score_res.matched_required,
                        matched_bonus=score_res.matched_bonus,
                        snippet=snippet,
                        skipped_by_robots=False,
                        error=None,
                    )
                )

                state.pages_processed += 1
                pbar.update(1)

                if status_code == 200 and html:
                    for link in self._extract_links(html, url):
                        if self.profile.same_domain_only and not self._same_domain(
                            url, link
                        ):
                            continue
                        if not self._domain_allowed(link):
                            continue
                        if link not in state.visited:
                            state.queue.append((link, depth + 1))

        return results
