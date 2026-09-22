from __future__ import annotations

import datetime as dt

import requests
from bs4 import BeautifulSoup

from ..models import Paper

NAME = "anthropic"
TYPE = "Post"  # anthropic.com/research is a blog-style listing of posts
URL = "https://www.anthropic.com/research"
USER_AGENT = "ai-papers-tracker/1.0 (personal research tracker; https://github.com/alexrob123/ai-papers-tracker)"


def _parse_date(text: str) -> str:
    return dt.datetime.strptime(text.strip(), "%b %d, %Y").date().isoformat()


def fetch() -> list[Paper]:
    """Fetch the publication list from anthropic.com/research.

    The page's CSS module class names are content-hashed (e.g.
    "PublicationList-module-scss-module__KxYrHG__listItem"), so entries are
    matched by the stable suffix of each class rather than the full name.
    """
    response = requests.get(URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    papers: dict[str, Paper] = {}
    for link in soup.select('a[class*="listItem"]'):
        href = link.get("href", "")
        if not href.startswith("/research/") or href.startswith("/research/team/"):
            continue

        time_el = link.select_one("time")
        title_el = link.select_one('span[class*="title"]')
        category_el = link.select_one('span[class*="subject"]')
        if time_el is None or title_el is None:
            continue

        url = f"https://www.anthropic.com{href}"
        papers[url] = Paper(
            source=NAME,
            title=title_el.get_text(strip=True),
            url=url,
            date=_parse_date(time_el.get_text(strip=True)),
            type=TYPE,
            category=category_el.get_text(strip=True) if category_el else None,
        )

    return list(papers.values())
