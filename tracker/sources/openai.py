from __future__ import annotations

import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

import requests

from ..models import Paper

NAME = "openai"
FEED_URL = "https://openai.com/news/rss.xml"
USER_AGENT = "ai-papers-tracker/1.0 (personal research tracker; https://github.com/alexrob123/ai-papers-tracker)"

# openai.com/research/index/ sits behind a Cloudflare JS challenge and can't
# be scraped directly (plain requests get a 403 "challenge" response), so
# this reads OpenAI's public news RSS feed instead, filtered down to the
# topic tags shown on that page (the feed also carries non-research
# categories like "Product" or "Company" news, which are dropped).
#
# Add or remove a category to change which topics get tracked; its value
# is the reference type ("Post", "Paper", ...) shown for that category.
TRACKED_CATEGORIES = {
    "Research": "Post",
    "Publication": "Post",
    "Security": "Post",
}


def fetch() -> list[Paper]:
    response = requests.get(FEED_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    papers: list[Paper] = []
    for item in root.iter("item"):
        category = item.findtext("category") or ""
        paper_type = TRACKED_CATEGORIES.get(category)
        if paper_type is None:
            continue

        title = item.findtext("title")
        url = item.findtext("link")
        pub_date = item.findtext("pubDate")
        if not title or not url or not pub_date:
            continue

        papers.append(
            Paper(
                source=NAME,
                title=title.strip(),
                url=url.strip(),
                date=parsedate_to_datetime(pub_date).date().isoformat(),
                type=paper_type,
                category=category,
            )
        )

    return papers
