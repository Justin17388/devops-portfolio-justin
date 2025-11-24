import asyncio
import time
from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse
from urllib import robotparser

import aiohttp
from bs4 import BeautifulSoup

from .config import Profile, CrawlerSettings
from .scoring import score_text
from .storage import PageResult


@dataclass
class AsyncCrawlState:
    visited: Set[str]
    queue: Deque[Tuple[str, int]]  # (url, depth)
    pages_processed: int


class AsyncInsightsCrawler:
    """
    Asynchronous crawler for Turbo mode.
    Still:
    - Respects robots.txt (fetched via aiohttp)
    - Applies per-domain delay
    - Honors max_depth, max_pages, allowed_domains
    """

    def __init__(
        self,
        profile: Profile,
        settings: Optional[CrawlerSettings] = None,
        max_concurrency: int = 10,
    ) -> None:
        self.profile = profile
        self.settings = settings or CrawlerSettings()
        self._robots_cache: Dict[str, Optional[robotparser.RobotFileParser]] = {}
        self._last_request_time: Dict[str, float] = {}
        self._state = AsyncCrawlState(visited=set(), queue=deque(), pages_processed=0)
        self._sem = asyncio.Semaphore(max_concurrency)

    def _domain_allowed(self, url: str) -> bool:
        if not self.profile.allowed_domains:
            return True
        netloc = urlparse(url).netloc
        return any(netloc.endswith(domain) for domain in self.profile.allowed_domains)

    def _same_domain(self, base: str, url: str) -> bool:
        base_netloc = urlparse(base).netloc
        target_netloc = urlparse(url).netloc
        return base_netloc == target_netloc

    async def _get_robots(
        self, session: aiohttp.ClientSession, url: str
    ) -> Optional[robotparser.RobotFileParser]:
        netloc = urlparse(url).netloc
        if netloc in self._robots_cache:
            return self._robots_cache[netloc]

        rp = robotparser.RobotFileParser()
        for scheme in ("https", "http"):
            robots_url = f"{scheme}://{netloc}/robots.txt"
            try:
                async with session.get(
                    robots_url, headers={"User-Agent": self.settings.user_agent}
                ) as resp:
                    if resp.status == 200:
                        text = await resp.text()
                        rp.parse(text.splitlines())
                        self._robots_cache[netloc] = rp
                        return rp
            except Exception:
                continue

        self._robots_cache[netloc] = None
        return None

    async def _allowed_by_robots(
        self, session: aiohttp.ClientSession, url: str
    ) -> bool:
        rp = await self._get_robots(session, url)
        if rp is None:
            return True
        return rp.can_fetch(self.settings.user_agent, url)

    async def _apply_rate_limit(self, url: str) -> None:
        netloc = urlparse(url).netloc
        last = self._last_request_time.get(netloc)
        delay = self.profile.request_delay_seconds
        if last is not None and delay > 0:
            elapsed = time.perf_counter() - last
            if elapsed < delay:
                await asyncio.sleep(delay - elapsed)

    @staticmethod
    def _extract_links(html: str, base_url: str) -> List[str]:
        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []
        for a in soup.find_all("a", href=True):
            href = a["href"]
            absolute = urljoin(base_url, href)
            links.append(absolute)
        return links

    @staticmethod
    def _extract_title_and_text(html: str) -> Tuple[str, str]:
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""
        text = soup.get_text(separator=" ", strip=True)
        return title, text

    async def _fetch_and_process(
        self,
        session: aiohttp.ClientSession,
        url: str,
        depth: int,
        results: List[PageResult],
    ) -> None:
        if self._state.pages_processed >= self.profile.max_pages:
            return

        if url in self._state.visited:
            return
        self._state.visited.add(url)

        if depth > self.profile.max_depth:
            return

        if not self._domain_allowed(url):
            return

        async with self._sem:
            if not await self._allowed_by_robots(session, url):
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
                self._state.pages_processed += 1
                return

            try:
                await self._apply_rate_limit(url)
                start = time.perf_counter()
                async with session.get(url, timeout=self.settings.timeout) as resp:
                    content_type = resp.headers.get("Content-Type", "")
                    html = await resp.text() if "text/html" in content_type else ""
                    elapsed_ms = (time.perf_counter() - start) * 1000.0
                    self._last_request_time[urlparse(url).netloc] = time.perf_counter()
                    status_code = resp.status
            except Exception as exc:
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
                self._state.pages_processed += 1
                return

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
            self._state.pages_processed += 1

            if status_code == 200 and html:
                for link in self._extract_links(html, url):
                    if self.profile.same_domain_only and not self._same_domain(
                        url, link
                    ):
                        continue
                    if not self._domain_allowed(link):
                        continue
                    if link not in self._state.visited:
                        self._state.queue.append((link, depth + 1))

    async def crawl_async(self) -> List[PageResult]:
        results: List[PageResult] = []

        for url in self.profile.start_urls:
            self._state.queue.append((url, 0))

        async with aiohttp.ClientSession(
            headers={"User-Agent": self.settings.user_agent}
        ) as session:
            while (
                self._state.queue
                and self._state.pages_processed < self.profile.max_pages
            ):
                url, depth = self._state.queue.popleft()
                await self._fetch_and_process(session, url, depth, results)

        return results
