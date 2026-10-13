"""ValidateService — checks a pack manifest for structural and safety issues."""

from __future__ import annotations

from pathlib import Path

from hdtpi.models.validation_report import Issue, ValidationReport
from hdtpi.parsers.registry import parser_for


class ValidateService:
    """Runs a fixed rule set against a parsed manifest."""

    def validate(self, pack_path: Path) -> ValidationReport:
        issues: list[Issue] = []
        try:
            manifest = parser_for(pack_path)(pack_path)
        except Exception as exc:  # noqa: BLE001 - report, don't crash
            return ValidationReport(
                pack_id=pack_path.stem,
                issues=(Issue("error", "PARSE_FAIL", str(exc)),),
            )

        if manifest.entry_count == 0:
            issues.append(Issue("error", "EMPTY_PACK", "manifest declares zero textures"))

        for entry in manifest.entries:
            if entry.target.startswith(("/", "\\")) or ".." in Path(entry.target).parts:
                issues.append(
                    Issue("error", "UNSAFE_TARGET", f"absolute or escaping target: {entry.target}")
                )
            if entry.resolution == "unknown":
                issues.append(
                    Issue("warning", "NO_RESOLUTION", f"{entry.source} has no resolution tag")
                )

        return ValidationReport(pack_id=manifest.pack_id, issues=tuple(issues))