from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QWidget,
)

_STYLES = {
    "bar": "QFrame#transportBar { background: #161b22; "
    "border-top: 1px solid #30363d; }",
    "play": (
        "QPushButton { background: #2ea043; color: #ffffff; border: none; "
        "border-radius: 5px; padding: 5px 16px; font-weight: 700; }"
        "QPushButton:hover { background: #3fb950; }"
        "QPushButton:pressed { background: #238636; }"
    ),
    "pause": (
        "QPushButton { background: #1f6feb; color: #ffffff; border: none; "
        "border-radius: 5px; padding: 5px 16px; font-weight: 700; }"
        "QPushButton:hover { background: #58a6ff; }"
        "QPushButton:pressed { background: #1f6feb; }"
    ),
    "control": (
        "QPushButton { background: #21262d; color: #e6edf3; "
        "border: 1px solid #30363d; border-radius: 5px; padding: 5px 12px; }"
        "QPushButton:hover { background: #30363d; }"
    ),
    "step": "color: #8b949e; font-family: 'JetBrains Mono', monospace; "
    "font-size: 11px;",
    "fps": "color: #58a6ff; font-family: 'JetBrains Mono', monospace; "
    "font-size: 11px;",
}

_SPEEDS = (
    ("×0.25", 0.25),
    ("×0.5", 0.5),
    ("×1", 1.0),
    ("×2", 2.0),
    ("×4", 4.0),
)


class TransportBar(QWidget):
    """Full-width bottom transport controls: play/step/reset, timeline,
    playback speed, and FPS readout."""

    play_toggled = Signal(bool)
    step_requested = Signal()
    reset_requested = Signal()
    speed_changed = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("transportBar")
        self.setStyleSheet(_STYLES["bar"])

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 6, 10, 6)
        layout.setSpacing(8)

        self.play_btn = QPushButton("Pause")
        self.play_btn.setFixedWidth(84)
        self.play_btn.setToolTip("Play or pause the simulation (Space)")
        self.play_btn.setStyleSheet(_STYLES["play"])
        self.play_btn.clicked.connect(lambda: self.play_toggled.emit(True))
        layout.addWidget(self.play_btn)

        self.step_btn = QPushButton("Step")
        self.step_btn.setToolTip("Advance one simulation step (.)")
        self.step_btn.setStyleSheet(_STYLES["control"])
        self.step_btn.clicked.connect(self.step_requested)
        layout.addWidget(self.step_btn)

        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setToolTip("Clear and restart from initial conditions (R)")
        self.reset_btn.setStyleSheet(_STYLES["control"])
        self.reset_btn.clicked.connect(self.reset_requested)
        layout.addWidget(self.reset_btn)

        layout.addSpacing(8)

        self.timeline_slider = QSlider(Qt.Orientation.Horizontal)
        self.timeline_slider.setRange(0, 0)
        self.timeline_slider.setValue(0)
        self.timeline_slider.setToolTip("Scrub simulation timeline back and forth")
        layout.addWidget(self.timeline_slider, 1)

        self.step_label = QLabel("Step 0")
        self.step_label.setStyleSheet(_STYLES["step"])
        self.step_label.setMinimumWidth(64)
        layout.addWidget(self.step_label)

        self.speed_combo = QComboBox()
        for label, factor in _SPEEDS:
            self.speed_combo.addItem(label, factor)
        self.speed_combo.setCurrentIndex(2)
        self.speed_combo.setToolTip("Playback speed")
        self.speed_combo.currentIndexChanged.connect(self._emit_speed)
        layout.addWidget(self.speed_combo)

        self.fps_label = QLabel("FPS: -")
        self.fps_label.setStyleSheet(_STYLES["fps"])
        layout.addWidget(self.fps_label)

    def _emit_speed(self, index: int) -> None:
        self.speed_changed.emit(float(self.speed_combo.itemData(index)))

    def set_play_state(self, playing: bool) -> None:
        self.play_btn.setText("Pause" if playing else "Play")
        self.play_btn.setStyleSheet(_STYLES["play"] if playing else _STYLES["pause"])

    def set_fps(self, fps: float) -> None:
        self.fps_label.setText(f"FPS: {fps:.0f}")

    def set_step_label(self, text: str) -> None:
        self.step_label.setText(text)
