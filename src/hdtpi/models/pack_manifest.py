"""Pack manifest model — the declarative contract every texture pack ships."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TextureEntry:
    """A single texture file declared by a pack.

    Attributes:
        source: Relative path inside the pack archive.
        target: Relative path inside the game install root.
        resolution: Declared output resolution, e.g. "2048x2048".
        category: Loose tag such as "characters", "terrain", "ui".
    """

    source: str
    target: str
    resolution: str
    category: str = "uncategorized"


@dataclass(frozen=True, slots=True)
class PackManifest:
    """Parsed manifest for one HD texture pack."""

    pack_id: str
    name: str
    version: str
    game: str
    target_root: str
    entries: tuple[TextureEntry, ...] = field(default_factory=tuple)
    requires: tuple[str, ...] = field(default_factory=tuple)

    @property
    def entry_count(self) -> int:
        return len(self.entries)

    def by_category(self) -> dict[str, list[TextureEntry]]:
        grouped: dict[str, list[TextureEntry]] = {}
        for entry in self.entries:
            grouped.setdefault(entry.category, []).append(entry)
        return grouped