import sys

from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect, QPoint
from PySide6.QtGui import QPainter, QPen, Qt, QColor, QPolygon, QBrush, QWheelEvent
from PySide6.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout
from sympy import symbols, sympify, lambdify

from gui import Ui_MainWindow

AXIS_DX_RATIO = 0.06  # left indent
AXIS_DY_RATIO = 0.05  # right indent

COLS_RATIO = 0.05
ROWS_RATIO = 0.05


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self._chart_widget = ChartWidget(parent=self.ui.plot_wdgt)

        layout = QVBoxLayout(self.ui.plot_wdgt)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._chart_widget)

        self.ui.plot_btn.clicked.connect(self._plot_func)
        self.ui.clear_btn.clicked.connect(self._chart_widget.clear_canvas)
        self.ui.center_btn.clicked.connect(self._chart_widget.draw_central_dot)

    def _plot_func(self):
        x = symbols('x')
        expr = sympify(self.ui.func_lineEdit.text())
        f = lambdify(x, expr, modules=['math'])

        if not self.ui.cones_checkBox.isChecked():
            self._chart_widget.draw_function(f, self.ui.from_spinBox.value(), self.ui.to_spinBox.value(),
                                             step=self.ui.step_spinBox.value())
        else:
            self._chart_widget.draw_function_cones(f, self.ui.from_spinBox.value(), self.ui.to_spinBox.value(),
                                                   step=self.ui.step_spinBox.value())


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._pixmap = QPixmap()
        self._axis_area = QRect()

        self._scale = 1.0  # current zoom level
        self._logical_range_x = 10  # default visible range in logical units (positive + negative)
        self._logical_range_y = 10

        self._center_coord_x = 0
        self._center_coord_y = 0

    def paintEvent(self, event, /):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._pixmap)
        painter.end()

    def resizeEvent(self, event):
        self._pixmap = QPixmap(self.width(), self.height())
        self._pixmap.fill(QColor(224, 224, 224))
        self._draw_coord_grid()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y()
        zoom_factor = 1.1

        if delta > 0:
            self._scale *= zoom_factor
        else:
            self._scale /= zoom_factor

        self._pixmap.fill(QColor(224, 224, 224))
        self._draw_coord_grid()
        self.update()

    def clear_canvas(self):
        self._pixmap.fill(QColor(224, 224, 224))
        self._draw_coord_grid()

    def _to_pyside_coords(self, x, y):
        px = self._center_coord_x + (x / self._logical_range_x) * (self._axis_area.width() / 2) * self._scale
        py = self._center_coord_y - (y / self._logical_range_y) * (self._axis_area.height() / 2) * self._scale
        return int(px), int(py)

    def _to_cartesian_coords(self, px, py):
        x = ((px - self._center_coord_x) / (self._axis_area.width() / 2)) * self._logical_range_x / self._scale
        y = ((self._center_coord_y - py) / (self._axis_area.height() / 2)) * self._logical_range_y / self._scale
        return x, y

    def draw_central_dot(self):
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._axis_area)
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        painter.setPen(pen)
        x, y = self._to_pyside_coords(0, 0)
        painter.drawPoint(x, y)
        painter.end()
        self.update()

    def draw_function(self, func, x_start, x_end, step=0.1):
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._axis_area)
        pen = QPen(Qt.blue, 2)
        painter.setPen(pen)

        x = x_start
        prev = None
        while x <= x_end:
            try:
                y = func(x)
                px, py = self._to_pyside_coords(x, y)
                if prev:
                    painter.drawLine(prev[0], prev[1], px, py)
                prev = (px, py)
            except:
                pass
            x += step

        painter.end()
        self.update()

    def draw_function_cones(self, func, x_start, x_end, color=QColor(80, 160, 255), step=0.1):
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._axis_area)

        cone_width = 1.0
        x = x_start
        while x <= x_end:
            try:
                y = func(x)
                qt_top_x, qt_top_y = self._to_pyside_coords(x, y)
                qt_left_x, qt_left_y = self._to_pyside_coords(x - cone_width / 2, 0)
                qt_right_x, qt_right_y = self._to_pyside_coords(x + cone_width / 2, 0)

                top_point = QPoint(qt_top_x, qt_top_y)
                left_point = QPoint(qt_left_x, qt_left_y)
                right_point = QPoint(qt_right_x, qt_right_y)

                cone = QPolygon([top_point, left_point, right_point])
                painter.setBrush(QBrush(color))
                painter.setPen(QPen(QColor(0, 0, 0), 0.5))
                painter.drawPolygon(cone)

                # Преобразуем центр и радиусы
                cx, cy = self._to_pyside_coords(x, 0)
                rx = abs(left_point.x() - right_point.x()) // 2
                ry = int(0.1 * abs(y) * self._scale * (self._axis_area.height() / (2 * self._logical_range_y)))

                # QRect, in ellipse
                rect = QRect(cx - rx, cy - ry, 2 * rx, 2 * ry)

                # Left side
                painter.setPen(Qt.NoPen)
                painter.setBrush(QBrush(color.darker(150)))
                painter.drawPie(rect, 180 * 16, 90 * 16)  # from 180° to 270° left

                # Right side
                # painter.setPen(QPen(QColor(0, 0, 0), 0.5))
                painter.setBrush(QBrush(color))
                painter.drawPie(rect, 270 * 16, 90 * 16)

                # Draw shadow
                shadow = QPolygon([top_point, left_point, QPoint(top_point.x(), left_point.y())])
                painter.setBrush(QBrush(color.darker(150)))
                painter.drawPolygon(shadow)



            except Exception as e:
                print(f"Error at x={x}: {e}")
            x += step

        painter.end()
        self.update()

    def _draw_coord_grid(self):
        painter = QPainter(self._pixmap)
        border_pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(border_pen)

        # draw chart border (viewport)
        x_indent = int(self.width() * AXIS_DX_RATIO)
        y_indent = int(self.height() * AXIS_DY_RATIO)

        x_indent_ratio = 0.3
        y_indent_ratio = 0.1

        self._axis_area = QRect(
            x_indent,
            int(y_indent * y_indent_ratio),
            self.width() - x_indent - int(x_indent * x_indent_ratio),
            self.height() - y_indent
        )
        painter.drawRect(self._axis_area)

        # center in screen coords
        self._center_coord_x = self._axis_area.left() + int(self._axis_area.width() / 2)
        self._center_coord_y = self._axis_area.top() + int(self._axis_area.height() / 2)

        # base cell size before scaling in pixels
        base_cell_x = 40  # arbitrary default unit size
        base_cell_y = 40

        self._cell_scale_x = base_cell_x * self._scale
        self._cell_scale_y = base_cell_y * self._scale

        grid_pen = QPen(Qt.black, 1, Qt.DotLine)
        painter.setPen(grid_pen)
        font_metrics = painter.fontMetrics()

        # draw vertical grid lines (infinite to left/right)
        x = self._center_coord_x
        while x <= self._axis_area.right():
            painter.drawLine(int(x), self._axis_area.top(), int(x), self._axis_area.bottom())
            cart_x, _ = self._to_cartesian_coords(x, 0)
            text = f"{cart_x:.1f}"
            w = font_metrics.horizontalAdvance(text)
            painter.drawText(int(x - w / 2), self._axis_area.bottom() + font_metrics.height(), text)
            x += self._cell_scale_x

        x = self._center_coord_x - self._cell_scale_x
        while x >= self._axis_area.left():
            painter.drawLine(int(x), self._axis_area.top(), int(x), self._axis_area.bottom())
            cart_x, _ = self._to_cartesian_coords(x, 0)
            text = f"{cart_x:.1f}"
            w = font_metrics.horizontalAdvance(text)
            painter.drawText(int(x - w / 2), self._axis_area.bottom() + font_metrics.height(), text)
            x -= self._cell_scale_x

        # draw horizontal grid lines (infinite up/down)
        y = self._center_coord_y
        while y <= self._axis_area.bottom():
            painter.drawLine(self._axis_area.left(), int(y), self._axis_area.right(), int(y))
            _, cart_y = self._to_cartesian_coords(0, y)
            text = f"{cart_y:.1f}"
            w = font_metrics.horizontalAdvance(text)
            painter.drawText(self._axis_area.left() - w - 5, int(y + font_metrics.ascent() / 2), text)
            y += self._cell_scale_y

        y = self._center_coord_y - self._cell_scale_y
        while y >= self._axis_area.top():
            painter.drawLine(self._axis_area.left(), int(y), self._axis_area.right(), int(y))
            _, cart_y = self._to_cartesian_coords(0, y)
            text = f"{cart_y:.1f}"
            w = font_metrics.horizontalAdvance(text)
            painter.drawText(self._axis_area.left() - w - 5, int(y + font_metrics.ascent() / 2), text)
            y -= self._cell_scale_y

        painter.end()
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
