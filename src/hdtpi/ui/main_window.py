"""Main application window."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from hdtpi.handlers.install_handler import InstallHandler


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("HD Texture Pack Installer")
        self.resize(760, 520)
        self._handler = InstallHandler()

        self._pack = QLineEdit(placeholderText="Path to .hdtp pack")
        self._target = QLineEdit(placeholderText="Game install root")
        self._preview = QTextEdit(readOnly=True)
        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self._on_preview)

        row = QHBoxLayout()
        row.addWidget(QLabel("Pack:"))
        row.addWidget(self._pack)
        row.addWidget(QLabel("Target:"))
        row.addWidget(self._target)

        layout = QVBoxLayout(self)
        layout.addLayout(row)
        layout.addWidget(preview_btn)
        layout.addWidget(self._preview)

    def _on_preview(self) -> None:
        from pathlib import Path

        text = self._handler.preview(Path(self._pack.text()), Path(self._target.text()))
        self._preview.setPlainText(text)