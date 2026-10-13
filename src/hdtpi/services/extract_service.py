"""ExtractService — safely unpacks pack archives into staging."""

from __future__ import annotations

import logging
import zipfile
from pathlib import Path

from hdtpi.adapters.filesystem import safe_join
from hdtpi.config.settings import Settings

log = logging.getLogger(__name__)


class ExtractService:
    """Extracts .hdtp / .zip packs into a per-pack staging directory.

    Rejects any archive member whose resolved path escapes the staging
    root (zip-slip defense).
    """

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def extract(self, pack_path: Path) -> Path:
        if pack_path.is_dir():
            return pack_path

        staging = self._settings.staging_dir / pack_path.stem
        staging.mkdir(parents=True, exist_ok=True)

        with zipfile.ZipFile(pack_path) as zf:
            for member in zf.namelist():
                dest = safe_join(staging, member)
                if member.endswith("/"):
                    dest.mkdir(parents=True, exist_ok=True)
                    continue
                dest.parent.mkdir(parents=True, exist_ok=True)
                with zf.open(member) as src, dest.open("wb") as out:
                    out.write(src.read())
        log.info("extracted %s -> %s", pack_path.name, staging)
        return staging