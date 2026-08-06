from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QButtonGroup,
    QFrame,
    QHBoxLayout,
    QPushButton,
)

_MODES: list[tuple[str | None, str, str]] = [
    (
        "select",
        "Select",
        "Select and move objects\nWhy: Adjust obstacle positions to see flow changes",
    ),
    (
        "circle",
        "Circle",
        "Draw circular obstacles\n"
        "Why: Study flow around cylinders (classic vortex shedding)",
    ),
    (
        "rect",
        "Rect",
        "Draw rectangular obstacles\nWhy: Study flow separation and drag",
    ),
    (
        "polygon",
        "Poly",
        "Draw custom polygon shapes\nWhy: Create complex geometries like airfoils",
    ),
    (
        "probe",
        "Probe",
        "Place measurement probe\n"
        "Why: Track velocity/pressure at specific points over time",
    ),
]


class ToolStrip(QFrame):
    """Minimal canvas overlay tool strip for viewport drawing modes."""

    tool_selected = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("toolStrip")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 2, 6, 2)
        layout.setSpacing(4)

        self._buttons: list[QPushButton] = []
        self._freehand_btn: QPushButton | None = None
        self._group = QButtonGroup(self)
        self._group.setExclusive(True)
        first_btn: QPushButton | None = None
        for mode, label, tooltip in _MODES:
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setToolTip(tooltip)
            btn.clicked.connect(lambda checked, m=mode, b=btn: self._select(m, b))
            layout.addWidget(btn)
            self._group.addButton(btn)
            self._buttons.append(btn)
            if first_btn is None:
                first_btn = btn
            if mode == "polygon":
                self._freehand_btn = btn
        layout.addStretch(1)
        if first_btn is not None:
            first_btn.setChecked(True)

    def _select(self, mode: str | None, btn: QPushButton) -> None:
        if not btn.isChecked():
            btn.setChecked(True)
        self.tool_selected.emit(mode)

    def set_mode(self, mode: str | None) -> None:
        for btn, (m, _, _) in zip(self._buttons, _MODES, strict=False):
            btn.setChecked(m == mode)

    def set_polygon_visible(self, visible: bool) -> None:
        if self._freehand_btn is not None:
            self._freehand_btn.setVisible(visible)

    def polygon_btn(self) -> QPushButton | None:
        return self._freehand_btn
