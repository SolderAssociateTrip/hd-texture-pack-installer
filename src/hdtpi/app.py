"""GUI bootstrap. Wires the Qt window to the service layer."""

from __future__ import annotations

import sys

from PySide6.QtWidgets import QApplication

from hdtpi.ui.main_window import MainWindow
from hdtpi.utils.logging import configure_logging


def run() -> int:
    configure_logging(verbose=False)
    app = QApplication(sys.argv)
    app.setApplicationName("HD Texture Pack Installer")
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(run())