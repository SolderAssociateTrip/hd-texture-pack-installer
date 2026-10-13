"""Tests for InstallService planning."""

from __future__ import annotations

import json
from pathlib import Path

from hdtpi.config.settings import Settings
from hdtpi.services.install_service import InstallService


def _make_pack(root: Path) -> Path:
    pack = root / "pack"
    pack.mkdir()
    (pack / "manifest.hdtp").write_text(
        json.dumps(
            {
                "pack_id": "hd-terrain-4k",
                "name": "HD Terrain 4K",
                "version": "1.2.0",
                "game": "Skyward",
                "target_root": ".",
                "entries": [
                    {"source": "tex/grass.dds", "target": "Data/tex/grass.dds", "resolution": "4096x4096", "category": "terrain"},
                    {"source": "tex/rock.dds", "target": "Data/tex/rock.dds", "resolution": "4096x4096", "category": "terrain"},
                ],
            }
        ),
        encoding="utf-8",
    )
    (pack / "tex").mkdir()
    (pack / "tex" / "grass.dds").write_bytes(b"\x00" * 16)
    (pack / "tex" / "rock.dds").write_bytes(b"\x00" * 16)
    return pack


def test_plan_lists_writes(tmp_path: Path) -> None:
    settings = Settings(
        staging_dir=tmp_path / "staging",
        backup_dir=tmp_path / "backup",
        cache_dir=tmp_path / "cache",
    )
    service = InstallService(settings)
    pack = _make_pack(tmp_path)
    target = tmp_path / "game"
    target.mkdir()

    plan = service.plan(pack, target)
    assert plan.pack_id == "hd-terrain-4k"
    assert len(plan.writes) == 2
    assert plan.conflicts == ()


def test_apply_writes_files(tmp_path: Path) -> None:
    settings = Settings(
        staging_dir=tmp_path / "staging",
        backup_dir=tmp_path / "backup",
        cache_dir=tmp_path / "cache",
    )
    service = InstallService(settings)
    pack = _make_pack(tmp_path)
    target = tmp_path / "game"
    target.mkdir()

    plan = service.plan(pack, target)
    result = service.apply(plan, backup=True)
    assert result.files_written == 2
    assert (target / "Data" / "tex" / "grass.dds").exists()
    assert (target / "Data" / "tex" / "rock.dds").exists()
</thinking>