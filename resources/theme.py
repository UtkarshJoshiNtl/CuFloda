"""
S-Stream Professional Visual Design System (GitHub Dark Theme)
Tokens:
- bg-base: #0d1117
- bg-panel: #161b22
- bg-elevated: #21262d
- border: #30363d
- text-primary: #e6edf3
- text-secondary: #8b949e
- text-muted: #484f58
- accent-blue: #58a6ff
- accent-green: #3fb950
- accent-yellow: #d29922
- accent-red: #f85149
"""

APP_STYLESHEET = """
QMainWindow {
    background: #0d1117;
    color: #e6edf3;
}
QWidget {
    color: #e6edf3;
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
        sans-serif;
}
QSplitter::handle {
    background: #30363d;
    width: 2px;
    height: 2px;
}
QSplitter::handle:hover {
    background: #58a6ff;
}
QToolBar {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    padding: 4px 8px;
    spacing: 6px;
}
QToolBar QPushButton {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 12px;
    font-weight: 500;
}
QToolBar QPushButton:hover {
    background: #30363d;
    border-color: #8b949e;
}
QToolBar QPushButton:pressed {
    background: #1f6feb;
}
QToolBar QPushButton:checked {
    background: #1f6feb;
    border-color: #58a6ff;
    color: #ffffff;
}
QMenuBar {
    background: #0d1117;
    color: #e6edf3;
    border-bottom: 1px solid #30363d;
    padding: 2px 6px;
    font-size: 12px;
}
QMenuBar::item {
    padding: 4px 8px;
    background: transparent;
    border-radius: 4px;
}
QMenuBar::item:selected {
    background: #21262d;
    color: #58a6ff;
}
QMenu {
    background: #161b22;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 6px;
    padding: 4px;
}
QMenu::item {
    padding: 6px 24px 6px 16px;
    border-radius: 4px;
    font-size: 12px;
}
QMenu::item:selected {
    background: #1f6feb;
    color: #ffffff;
}
QMenu::separator {
    height: 1px;
    background: #30363d;
    margin: 4px 8px;
}
QStatusBar {
    background: #161b22;
    color: #8b949e;
    border-top: 1px solid #30363d;
    font-size: 11px;
    font-family: "JetBrains Mono", monospace;
}
QLabel {
    color: #e6edf3;
    background: transparent;
}
QGroupBox {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 6px;
    margin-top: 14px;
    padding: 10px 8px 8px 8px;
    font-weight: 600;
    color: #e6edf3;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 2px 6px;
    color: #8b949e;
    font-size: 10px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
}
QComboBox {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 4px 8px;
    font-size: 12px;
}
QComboBox:hover {
    border-color: #8b949e;
}
QComboBox::drop-down {
    border: none;
    width: 20px;
}
QComboBox QAbstractItemView {
    background: #161b22;
    color: #e6edf3;
    selection-background-color: #1f6feb;
    border: 1px solid #30363d;
}
QListWidget, QTreeWidget {
    background: #0d1117;
    color: #e6edf3;
    border: 1px solid #30363d;
    border-radius: 4px;
    outline: none;
    font-size: 12px;
}
QListWidget::item, QTreeWidget::item {
    padding: 5px 8px;
    border-radius: 3px;
}
QListWidget::item:selected, QTreeWidget::item:selected {
    background: #1f6feb;
    color: #ffffff;
}
QListWidget::item:hover:!selected, QTreeWidget::item:hover:!selected {
    background: #21262d;
}
QDoubleSpinBox, QSpinBox {
    background: #0d1117;
    color: #58a6ff;
    font-family: "JetBrains Mono", monospace;
    border: 1px solid #30363d;
    border-radius: 4px;
    padding: 3px 6px;
    font-size: 12px;
}
QDoubleSpinBox:focus, QSpinBox:focus {
    border-color: #58a6ff;
}
QSlider::groove:horizontal {
    height: 4px;
    background: #21262d;
    border-radius: 2px;
}
QSlider::sub-page:horizontal {
    background: #58a6ff;
    border-radius: 2px;
}
QSlider::handle:horizontal {
    background: #e6edf3;
    border: 1px solid #58a6ff;
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}
QSlider::handle:horizontal:hover {
    background: #ffffff;
    border-color: #79c0ff;
}
QScrollBar:vertical {
    background: #0d1117;
    width: 8px;
    border: none;
}
QScrollBar::handle:vertical {
    background: #30363d;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::handle:vertical:hover { background: #8b949e; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar:horizontal {
    background: #0d1117;
    height: 8px;
    border: none;
}
QScrollBar::handle:horizontal {
    background: #30363d;
    border-radius: 4px;
    min-width: 24px;
}
QScrollBar::handle:horizontal:hover { background: #8b949e; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QPushButton {
    background: #21262d;
    color: #e6edf3;
    border: 1px solid #30363d;
    padding: 5px 12px;
    border-radius: 4px;
    font-size: 12px;
}
QPushButton:hover {
    background: #30363d;
    border-color: #8b949e;
}
QPushButton:pressed {
    background: #1f6feb;
}
"""
