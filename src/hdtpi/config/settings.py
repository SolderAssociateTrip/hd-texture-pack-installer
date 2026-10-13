"""Runtime settings loaded from TOML, env vars, and sane defaults."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - py3.11+ only
    import tomli as tomllib  # type: ignore[no-redef]


@dataclass(slots=True)
class Settings:
    """Resolved runtime configuration.

    Attributes:
        staging_dir: Where packs are extracted before apply.
        backup_dir: Where overwritten originals are copied.
        cache_dir: Manifest + hash cache root.
        max_workers: Executor pool size for parallel extraction.
        verify_hashes: Recompute SHA-256 of every written file.
    """

    staging_dir: Path
    backup_dir: Path
    cache_dir: Path
    max_workers: int = 4
    verify_hashes: bool = True
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def load(cls, config_path: Path | None = None) -> "Settings":
        data: dict[str, object] = {}
        if config_path and config_path.exists():
            with config_path.open("rb") as fh:
                data = tomllib.load(fh)

        base = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "hdtpi"
        return cls(
            staging_dir=Path(str(data.get("staging_dir", base / "staging"))),
            backup_dir=Path(str(data.get("backup_dir", base / "backups"))),
            cache_dir=Path(str(data.get("cache_dir", base / "cache"))),
            max_workers=int(os.environ.get("HDTPI_WORKERS", data.get("max_workers", 4))),
            verify_hashes=bool(data.get("verify_hashes", True)),
        )