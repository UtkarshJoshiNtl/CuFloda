from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QFrame,
    QScrollArea,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

_HEADER_QSS = """
QToolButton {
    background: transparent;
    border: none;
    border-bottom: 1px solid #30363d;
    color: #e6edf3;
    font-weight: 700;
    font-size: 11px;
    letter-spacing: 0.8px;
    padding: 7px 8px;
    text-align: left;
}
QToolButton:hover {
    background: #21262d;
    color: #58a6ff;
}
QToolButton:checked {
    color: #58a6ff;
}
"""

_SECTION_QSS = (
    "QFrame#sidebarSection { background: #161b22; "
    "border: 1px solid #30363d; border-radius: 6px; }"
)


class SidebarSection(QFrame):
    """Collapsible accordion section (header button + body)."""

    toggled = Signal(str, bool)

    def __init__(
        self,
        key: str,
        title: str,
        content: QWidget,
        expanded: bool = True,
        parent=None,
    ):
        super().__init__(parent)
        self.key = key
        self.setObjectName("sidebarSection")
        self.setStyleSheet(_SECTION_QSS)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self._header = QToolButton()
        self._header.setText(title)
        self._header.setCheckable(True)
        self._header.setChecked(expanded)
        self._header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self._header.setStyleSheet(_HEADER_QSS)
        self._header.clicked.connect(self._on_header_clicked)
        layout.addWidget(self._header)

        self._body = QWidget()
        body_layout = QVBoxLayout(self._body)
        body_layout.setContentsMargins(4, 4, 4, 4)
        body_layout.setSpacing(4)
        body_layout.addWidget(content)
        self._body.setVisible(expanded)
        layout.addWidget(self._body)

        self._set_arrow(expanded)

    def _set_arrow(self, expanded: bool) -> None:
        self._header.setArrowType(
            Qt.ArrowType.DownArrow if expanded else Qt.ArrowType.RightArrow
        )

    def _on_header_clicked(self) -> None:
        self.set_expanded(self._header.isChecked())

    def set_expanded(self, expanded: bool) -> None:
        if expanded == self._body.isVisible():
            return
        self._header.setChecked(expanded)
        self._body.setVisible(expanded)
        self._set_arrow(expanded)
        self.toggled.emit(self.key, expanded)

    def expand(self) -> None:
        self.set_expanded(True)

    def collapse(self) -> None:
        self.set_expanded(False)

    def is_expanded(self) -> bool:
        return self._body.isVisible()


class Sidebar(QScrollArea):
    """Vertical accordion container for SidebarSections."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._container = QWidget()
        self._layout = QVBoxLayout(self._container)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.setSpacing(6)
        self.setWidget(self._container)
        self._sections: dict[str, SidebarSection] = {}

    def add_section(self, section: SidebarSection, stretch: int = 0) -> None:
        self._sections[section.key] = section
        self._layout.addWidget(section, stretch)

    def section(self, key: str) -> SidebarSection | None:
        return self._sections.get(key)

    def expand_section(self, key: str) -> None:
        section = self._sections.get(key)
        if section is not None:
            section.set_expanded(True)
