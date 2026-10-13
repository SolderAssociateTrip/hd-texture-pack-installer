"""Install plan — the resolved set of writes before anything touches disk."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TextIO


@dataclass(frozen=True, slots=True)
class PlannedWrite:
    source: Path
    target: Path
    size_bytes: int
    overwrites: bool


@dataclass(frozen=True, slots=True)
class InstallPlan:
    """An ordered list of writes plus metadata for a dry-run render."""

    pack_id: str
    target_root: Path
    writes: tuple[PlannedWrite, ...]
    conflicts: tuple[Path, ...] = ()

    @property
    def total_bytes(self) -> int:
        return sum(w.size_bytes for w in self.writes)

    def render(self, out: TextIO = sys.stdout) -> None:
        out.write(f"pack: {self.pack_id}\n")
        out.write(f"target: {self.target_root}\n")
        out.write(f"writes: {len(self.writes)} ({self.total_bytes} bytes)\n")
        for write in self.writes:
            flag = "OVERWRITE" if write.overwrites else "NEW"
            out.write(f"  [{flag}] {write.target.relative_to(self.target_root)}\n")
        if self.conflicts:
            out.write(f"conflicts: {len(self.conflicts)}\n")