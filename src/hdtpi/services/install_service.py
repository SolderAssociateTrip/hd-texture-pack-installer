"""InstallService — plans and applies HD texture packs into a game install."""

from __future__ import annotations

import logging
import shutil
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

from hdtpi.adapters.filesystem import safe_join
from hdtpi.config.settings import Settings
from hdtpi.models.install_plan import InstallPlan, PlannedWrite
from hdtpi.parsers.registry import parser_for
from hdtpi.services.extract_service import ExtractService
from hdtpi.utils.hashing import sha256_file

log = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class InstallResult:
    files_written: int
    bytes_written: int
    backed_up: int


class InstallService:
    """Coordinates extraction, planning, and apply.

    Concurrency: apply() fans out file copies across a bounded thread pool.
    All writes go through ``safe_join`` so a malicious manifest cannot
    escape ``target_root``.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self._settings = settings or Settings.load()
        self._extract = ExtractService(self._settings)

    def plan(self, pack_path: Path, target_root: Path) -> InstallPlan:
        """Resolve a pack into an ordered list of writes. No disk mutation."""
        staging = self._extract.extract(pack_path)
        manifest = parser_for(pack_path)(staging / "manifest.hdtp")

        writes: list[PlannedWrite] = []
        conflicts: list[Path] = []
        for entry in manifest.entries:
            src = safe_join(staging, entry.source)
            dst = safe_join(target_root, entry.target)
            overwrites = dst.exists()
            if overwrites:
                conflicts.append(dst)
            writes.append(
                PlannedWrite(
                    source=src,
                    target=dst,
                    size_bytes=src.stat().st_size if src.exists() else 0,
                    overwrites=overwrites,
                )
            )
        return InstallPlan(
            pack_id=manifest.pack_id,
            target_root=target_root,
            writes=tuple(writes),
            conflicts=tuple(conflicts),
        )

    def apply(self, plan: InstallPlan, *, backup: bool = False) -> InstallResult:
        """Execute an install plan. Writes files, optionally backing up."""
        written = 0
        total = 0
        backed = 0

        def _one(write: PlannedWrite) -> tuple[int, int, int]:
            if not write.source.exists():
                log.warning("missing source, skipping: %s", write.source)
                return (0, 0, 0)
            write.target.parent.mkdir(parents=True, exist_ok=True)
            local_backed = 0
            if backup and write.overwrites:
                bak = self._settings.backup_dir / write.target.name
                bak.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(write.target, bak)
                local_backed = 1
            shutil.copy2(write.source, write.target)
            size = write.target.stat().st_size
            if self._settings.verify_hashes:
                _ = sha256_file(write.target)
            return (1, size, local_backed)

        with ThreadPoolExecutor(max_workers=self._settings.max_workers) as pool:
            for files, size, bkd in pool.map(_one, plan.writes):
                written += files
                total += size
                backed += bkd

        return InstallResult(files_written=written, bytes_written=total, backed_up=backed)