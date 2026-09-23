from __future__ import annotations

from collections import deque
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse, urldefrag
from typing import Iterable

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


@dataclass
class PageRecord:
    url: str
    level: int
    title: str
    status: int | None
    parent: str | None
    links: list[str]
    error: str | None = None

    def to_dict(self):
        return asdict(self)


def normalize_url(base: str, href: str) -> str | None:
    if not href:
        return None
    href = href.strip()
    if href.startswith(("mailto:", "tel:", "javascript:", "data:")):
        return None
    absolute = urljoin(base, href)
    absolute, _ = urldefrag(absolute)
    p = urlparse(absolute)
    if p.scheme not in {"http", "https"}:
        return None
    return absolute


def same_host(url: str, host: str) -> bool:
    return urlparse(url).netloc.lower() == host.lower()


class SCrawler:
    def __init__(self, max_depth: int = 5, same_domain: bool = True, timeout_ms: int = 15000):
        if max_depth < 0:
            raise ValueError("max_depth must be >= 0")
        self.max_depth = max_depth
        self.same_domain = same_domain
        self.timeout_ms = timeout_ms

    def crawl(self, start_url: str) -> dict:
        parsed = urlparse(start_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("start_url must be an absolute http(s) URL")

        host = parsed.netloc
        start_url = urldefrag(start_url)[0]
        frontier = deque([(start_url, 0, None)])
        queued = {start_url}
        visited: set[str] = set()
        pages: list[PageRecord] = []

        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page()

            while frontier:
                url, level, parent = frontier.popleft()
                if url in visited:
                    continue
                visited.add(url)

                status = None
                title = ""
                links: list[str] = []
                error = None

                try:
                    response = page.goto(url, wait_until="domcontentloaded", timeout=self.timeout_ms)
                    status = response.status if response else None
                    html = page.content()
                    title = page.title()
                    soup = BeautifulSoup(html, "html.parser")

                    discovered: list[str] = []
                    for a in soup.find_all("a", href=True):
                        normalized = normalize_url(url, a.get("href"))
                        if not normalized:
                            continue
                        if self.same_domain and not same_host(normalized, host):
                            continue
                        if normalized not in discovered:
                            discovered.append(normalized)
                    links = discovered

                    if level < self.max_depth:
                        for child in discovered:
                            if child not in visited and child not in queued:
                                frontier.append((child, level + 1, url))
                                queued.add(child)
                except Exception as exc:
                    error = f"{type(exc).__name__}: {exc}"

                pages.append(PageRecord(
                    url=url,
                    level=level,
                    title=title,
                    status=status,
                    parent=parent,
                    links=links,
                    error=error,
                ))

            browser.close()

        return {
            "start_url": start_url,
            "max_depth": self.max_depth,
            "same_domain": self.same_domain,
            "pages": [p.to_dict() for p in pages],
            "stats": {
                "visited": len(pages),
                "errors": sum(1 for p in pages if p.error),
                "levels_reached": max((p.level for p in pages), default=0),
            },
        }
