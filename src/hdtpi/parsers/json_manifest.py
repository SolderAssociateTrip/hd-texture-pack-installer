"""Parser for .hdtp JSON manifests."""

from __future__ import annotations

import json
from pathlib import Path

from hdtpi.models.pack_manifest import PackManifest, TextureEntry
from hdtpi.parsers.registry import register


@register(".hdtp")
def parse_json_manifest(path: Path) -> PackManifest:
    """Parse a JSON manifest. Raises ValueError on schema violations."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if "pack_id" not in raw or "entries" not in raw:
        raise ValueError("manifest missing required keys: pack_id, entries")

    entries = tuple(
        TextureEntry(
            source=e["source"],
            target=e["target"],
            resolution=e.get("resolution", "unknown"),
            category=e.get("category", "uncategorized"),
        )
        for e in raw["entries"]
    )
    return PackManifest(
        pack_id=raw["pack_id"],
        name=raw.get("name", raw["pack_id"]),
        version=raw.get("version", "0.0.0"),
        game=raw.get("game", "unknown"),
        target_root=raw.get("target_root", "."),
        entries=entries,
        requires=tuple(raw.get("requires", [])),
    )