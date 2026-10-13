"""Filesystem adapter — the only place path joins are trusted."""

from __future__ import annotations

from pathlib import Path


class UnsafePathError(ValueError):
    """Raised when a resolved path escapes its declared root."""


def safe_join(root: Path, member: str) -> Path:
    """Join ``member`` under ``root``, rejecting traversal.

    Raises UnsafePathError if the resolved path is not a descendant of root.
    """
    root_resolved = root.resolve()
    candidate = (root_resolved / member).resolve()
    if root_resolved != candidate and root_resolved not in candidate.parents:
        raise UnsafePathError(f"{member!r} escapes {root_resolved}")
    return candidate