"""CLI entrypoint. Thin: parse args, dispatch to services, print result."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from hdtpi.services.install_service import InstallService
from hdtpi.services.validate_service import ValidateService
from hdtpi.utils.logging import configure_logging


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hdtpi",
        description="Install and apply HD texture packs into game installs.",
    )
    parser.add_argument("--verbose", "-v", action="store_true", help="debug logging")
    sub = parser.add_subparsers(dest="command", required=True)

    install = sub.add_parser("install", help="install a texture pack")
    install.add_argument("pack", type=Path, help="path to .hdtp pack or directory")
    install.add_argument("--target", type=Path, required=True, help="game install root")
    install.add_argument("--dry-run", action="store_true", help="plan only, no writes")
    install.add_argument("--backup", action="store_true", help="backup overwritten files")

    validate = sub.add_parser("validate", help="validate a pack manifest")
    validate.add_argument("pack", type=Path)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)

    if args.command == "install":
        service = InstallService()
        plan = service.plan(pack_path=args.pack, target_root=args.target)
        if args.dry_run:
            plan.render(sys.stdout)
            return 0
        result = service.apply(plan, backup=args.backup)
        print(f"installed {result.files_written} files, {result.bytes_written} bytes")
        return 0

    if args.command == "validate":
        service = ValidateService()
        report = service.validate(args.pack)
        report.render(sys.stdout)
        return 0 if report.ok else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())