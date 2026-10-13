"""Validation report model."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from typing import TextIO


@dataclass(frozen=True, slots=True)
class Issue:
    level: str  # "error" | "warning"
    code: str
    message: str


@dataclass(frozen=True, slots=True)
class ValidationReport:
    pack_id: str
    issues: tuple[Issue, ...] = ()

    @property
    def ok(self) -> bool:
        return not any(i.level == "error" for i in self.issues)

    def render(self, out: TextIO = sys.stdout) -> None:
        out.write(f"pack: {self.pack_id} -> {'OK' if self.ok else 'FAILED'}\n")
        for issue in self.issues:
            out.write(f"  {issue.level.upper():7} {issue.code}: {issue.message}\n")