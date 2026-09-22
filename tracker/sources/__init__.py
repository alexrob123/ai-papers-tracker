from __future__ import annotations

from collections.abc import Callable

from ..models import Paper
from . import anthropic

SOURCES: dict[str, Callable[[], list[Paper]]] = {
    anthropic.NAME: anthropic.fetch,
}
