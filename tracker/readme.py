from __future__ import annotations

import re
from pathlib import Path
from typing import Any

START_MARKER = "<!-- LATEST_PAPERS:START -->"
END_MARKER = "<!-- LATEST_PAPERS:END -->"

_MARKER_PATTERN = re.compile(re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER), re.DOTALL)


def render_table(papers: list[dict[str, Any]], limit: int = 10) -> str:
    rows = sorted(papers, key=lambda p: p.get("date", ""), reverse=True)[:limit]

    lines = ["| Date | Source | Category | Title |", "| --- | --- | --- | --- |"]
    for paper in rows:
        category = paper.get("category") or "-"
        source = paper["source"].capitalize()
        lines.append(
            f"| {paper['date']} | {source} | {category} | "
            f"[{paper['title']}]({paper['url']}) |"
        )
    return "\n".join(lines)


def update_readme(readme_path: Path, table_md: str) -> bool:
    text = readme_path.read_text()
    if not _MARKER_PATTERN.search(text):
        raise RuntimeError(f"README markers {START_MARKER}/{END_MARKER} not found")

    new_text = _MARKER_PATTERN.sub(f"{START_MARKER}\n{table_md}\n{END_MARKER}", text)
    if new_text == text:
        return False

    readme_path.write_text(new_text)
    return True
