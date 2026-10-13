"""Install handler — thin adapter over InstallService for the GUI."""

from __future__ import annotations

from pathlib import Path

from hdtpi.services.install_service import InstallResult, InstallService


class InstallHandler:
    """Keeps the UI dumb: it asks, the service decides."""

    def __init__(self, service: InstallService | None = None) -> None:
        self._service = service or InstallService()

    def preview(self, pack: Path, target: Path) -> str:
        plan = self._service.plan(pack, target)
        import io

        buf = io.StringIO()
        plan.render(buf)
        return buf.getvalue()

    def run(self, pack: Path, target: Path, *, backup: bool = False) -> InstallResult:
        plan = self._service.plan(pack, target)
        return self._service.apply(plan, backup=backup)