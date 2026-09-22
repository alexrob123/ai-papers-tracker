from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_known_papers(path: Path) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_known_papers(path: Path, papers: dict[str, dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ordered = dict(
        sorted(papers.items(), key=lambda kv: kv[1].get("date", ""), reverse=True)
    )
    path.write_text(json.dumps(ordered, indent=2) + "\n")
