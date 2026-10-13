"""Windows adapter — locates game install roots via the registry."""

from __future__ import annotations

import sys
from pathlib import Path

if sys.platform == "win32":  # pragma: no cover - platform gate
    import winreg  # type: ignore[import-not-found]


def find_game_root(game_key: str) -> Path | None:
    """Look up a game install root under HKLM\\SOFTWARE\\...\\Games.

    Returns None when the key is absent or the platform is not Windows.
    """
    if sys.platform != "win32":
        return None
    try:
        with winreg.OpenKey(  # type: ignore[name-defined]
            winreg.HKEY_LOCAL_MACHINE,  # type: ignore[name-defined]
            rf"SOFTWARE\HDTexturePacks\Games\{game_key}",
        ) as key:
            value, _ = winreg.QueryValueEx(key, "InstallPath")  # type: ignore[name-defined]
            return Path(value)
    except FileNotFoundError:
        return None