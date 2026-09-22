from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class Paper:
    source: str
    title: str
    url: str
    date: str  # ISO 8601, e.g. "2026-08-10"
    category: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
