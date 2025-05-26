from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QRadialGradient
from PySide6.QtCore import Qt, QPoint

import math


class PlotCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.func = math.sin
        self.zoom = 1.0  # масштаб по умолчанию
        self.offset_x = 0
        self.offset_y = 0
        self.last_mouse_pos = None

    def set_function(self, func):
        self.func = func
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.last_mouse_pos = event.position().toPoint()

    def mouseMoveEvent(self, event):
        if self.last_mouse_pos:
            delta = event.position().toPoint() - self.last_mouse_pos
            self.offset_x += delta.x()
            self.offset_y += delta.y()
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        if delta > 0:
            self.zoom *= 1.1
        else:
            self.zoom /= 1.1
        self.zoom = max(0.2, min(5.0, self.zoom))  # Ограничения масштаба
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), QColor(255, 255, 255))

        width = self.width()
        height = self.height()
        center_y = height * 3 // 4  # "земля", где стоят конусы

        a, b = -10, 10
        base_n = 20
        n = int(base_n * self.zoom)
        n = max(10, min(1000, n))  # ограничение

        step = (b - a) / (n - 1)
        spacing = self.zoom * (self.width() * 0.8 / base_n)  # базовый spacing
        base_x = self.width() * 0.1
        scale_y = self.zoom * 30

        self.draw_grid_and_axes(painter, a, b, n, center_y, scale_y)

        for i in range(n):
            x_val = a + i * step
            y_val = self.func(x_val)

            px = int(base_x + i * spacing * (base_n / n) + self.offset_x)
            py_base = center_y + self.offset_y
            self.draw_cone3d(painter, px, py_base, y_val, scale_y=scale_y)

    def draw_grid_and_axes(self, painter, a, b, n, center_y, scale_y):
        # Параметры сетки
        grid_pen = QPen(QColor(200, 200, 200), 1, Qt.SolidLine)
        axis_pen = QPen(QColor(0, 0, 0), 2)

        painter.setPen(grid_pen)

        width = self.width()
        height = self.height()

        # Вертикальные линии (оси X)
        for i in range(n):
            x_pos = int(self.width() * 0.1 + i * self.zoom * (self.width() * 0.8 / n) + self.offset_x)
            painter.drawLine(x_pos, 0, x_pos, height)

        # Горизонтальные линии (оси Y)
        y_range = 5
        y_steps = 10
        for i in range(y_steps + 1):
            y_val = -y_range + i * (2 * y_range / y_steps)
            y_pos = int(center_y - y_val * scale_y + self.offset_y)
            painter.drawLine(0, y_pos, width, y_pos)

        # Оси
        painter.setPen(axis_pen)
        # Ось X (y = 0)
        painter.drawLine(0, center_y + self.offset_y, width, center_y + self.offset_y)
        # Ось Y (x = 0)
        zero_x_pos = self.width() // 2 + self.offset_x
        painter.drawLine(zero_x_pos, 0, zero_x_pos, height)

        # Подписи X
        painter.setPen(QPen(Qt.black))
        font = painter.font()
        font.setPointSize(8)
        painter.setFont(font)

        step = (b - a) / (n - 1)
        for i in range(n):
            x_val = a + i * step
            x_pos = int(self.width() * 0.1 + i * self.zoom * (self.width() * 0.8 / n) + self.offset_x)
            painter.drawText(x_pos - 15, center_y + 18 + self.offset_y, f"{x_val:.1f}")

        # Подписи Y
        for i in range(y_steps + 1):
            y_val = -y_range + i * (2 * y_range / y_steps)
            y_pos = int(center_y - y_val * scale_y + self.offset_y)
            painter.drawText(5, y_pos + 4, f"{y_val:.2f}")

    def draw_cone(self, painter, x, y):
        base_radius_x = 10
        base_radius_y = 4
        cone_height = 30

        top_x = x
        top_y = y - cone_height

        # Основание
        painter.setBrush(QBrush(QColor(160, 160, 160)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPoint(x, y), base_radius_x, base_radius_y)

        # Боковые линии
        painter.setPen(QPen(Qt.black))
        painter.drawLine(x - base_radius_x, y, top_x, top_y)
        painter.drawLine(x + base_radius_x, y, top_x, top_y)

        # Треугольник (тело конуса)
        path = QPainterPath()
        path.moveTo(x - base_radius_x, y)
        path.lineTo(x + base_radius_x, y)
        path.lineTo(top_x, top_y)
        path.closeSubpath()
        painter.fillPath(path, QBrush(QColor(200, 100, 100)))

    def draw_cone3d(self, painter, x: int, base_y: int, height: float, scale_y=30):
        cone_height = height * scale_y
        top_y = base_y - cone_height

        base_radius_x = 14
        base_radius_y = 6

        # Основание (с тенью — radial gradient)
        ellipse_gradient = QRadialGradient(x, base_y, base_radius_x)
        ellipse_gradient.setColorAt(0.0, QColor(200, 200, 255))
        ellipse_gradient.setColorAt(1.0, QColor(120, 120, 160))
        painter.setBrush(ellipse_gradient)
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QPoint(x, base_y), base_radius_x, base_radius_y)

        # Левая половина конуса — с изгибом внутрь
        path_left = QPainterPath()
        path_left.moveTo(x, top_y)
        path_left.cubicTo(x - base_radius_x * 0.7, base_y - cone_height * 0.5,
                          x - base_radius_x, base_y - cone_height * 0.2,
                          x - base_radius_x, base_y)
        path_left.lineTo(x, base_y)
        path_left.closeSubpath()
        painter.fillPath(path_left, QBrush(QColor(150, 180, 250)))

        # Правая половина — чуть темнее, тоже изогнутая
        path_right = QPainterPath()
        path_right.moveTo(x, top_y)
        path_right.cubicTo(x + base_radius_x * 0.7, base_y - cone_height * 0.5,
                           x + base_radius_x, base_y - cone_height * 0.2,
                           x + base_radius_x, base_y)
        path_right.lineTo(x, base_y)
        path_right.closeSubpath()
        painter.fillPath(path_right, QBrush(QColor(80, 110, 180)))

        # Контур — линия к вершине
        painter.setPen(QPen(QColor(50, 50, 80), 1))
        painter.drawLine(x - base_radius_x, base_y, x, top_y)
        painter.drawLine(x + base_radius_x, base_y, x, top_y)
