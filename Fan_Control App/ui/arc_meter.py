# arc_meter.py
from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QPen
from PySide6.QtCore import Qt, QRectF, QPointF
import math

class ArcMeter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._value = 0  # Range: 0–100
        self.setMinimumSize(150, 150)

    def setValue(self, value):
        self._value = max(0, min(100, value))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        rect = QRectF(10, 10, self.width() - 20, self.height() - 20)
        center = rect.center()
        radius = rect.width() / 2

        # Draw arc
        pen = QPen(Qt.gray, 6)
        painter.setPen(pen)
        painter.drawArc(rect, 135 * 16, 270 * 16)

        # Draw needle
        angle_deg = 135 + 270 * (self._value / 100)
        angle_rad = math.radians(angle_deg)
        needle_length = radius - 10
        needle_x = center.x() + needle_length * math.cos(angle_rad)
        needle_y = center.y() - needle_length * math.sin(angle_rad)

        pen = QPen(Qt.red, 4)
        painter.setPen(pen)
        painter.drawLine(center, QPointF(needle_x, needle_y))

        # Optional: draw current value
        painter.setPen(Qt.black)
        painter.drawText(self.rect(), Qt.AlignCenter, f"{self._value:.0f}")



