"""Parser registry — maps pack extensions to parser callables."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

from hdtpi.models.pack_manifest import PackManifest

ParserFn = Callable[[Path], PackManifest]

_REGISTRY: dict[str, ParserFn] = {}


def register(ext: str) -> Callable[[ParserFn], ParserFn]:
    def _wrap(fn: ParserFn) -> ParserFn:
        _REGISTRY[ext.lower()] = fn
        return fn

    return _wrap


def parser_for(path: Path) -> ParserFn:
    ext = path.suffix.lower()
    try:
        return _REGISTRY[ext]
    except KeyError as exc:
        raise LookupError(f"no parser registered for extension {ext!r}") from exc