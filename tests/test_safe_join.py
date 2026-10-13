"""Tests for the path-safety adapter."""

from __future__ import annotations

from pathlib import Path

import pytest

from hdtpi.adapters.filesystem import UnsafePathError, safe_join


def test_join_inside_root_ok(tmp_path: Path) -> None:
    result = safe_join(tmp_path, "textures/characters/hero.dds")
    assert result.is_relative_to(tmp_path.resolve())


def test_traversal_rejected(tmp_path: Path) -> None:
    with pytest.raises(UnsafePathError):
        safe_join(tmp_path, "../../windows/system32/evil.dll")


def test_absolute_member_rejected(tmp_path: Path) -> None:
    with pytest.raises(UnsafePathError):
        safe_join(tmp_path, "C:/Windows/System32/drivers/etc/hosts")