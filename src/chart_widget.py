from PIL.ImageQt import QPixmap
from PySide6.QtCore import QRect
from PySide6.QtGui import QPainter, QPen, Qt, QColor
from PySide6.QtWidgets import QWidget

BASE_CELL_SIZE = 40


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create canvas and rectangle for plotting
        self._pixmap = QPixmap(self.width(), self.height())
        self._plotting_rect = QRect()

        # Qt's real pixel coords
        self._qt_center_x = None
        self._qt_center_y = None

        self._cell_size_x = BASE_CELL_SIZE
        self._cell_size_y = BASE_CELL_SIZE

        self._cell_scale_ratio_x = 1
        self._cell_scale_ratio_y = 1

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._pixmap)
        painter.end()

    def resizeEvent(self, event):
        self.clear_canvas()

    def clear_canvas(self):
        self._pixmap.fill(QColor(224, 224, 224))
        self._draw_coord_grid()

    def _to_qt_coordinates(self, logic_x, logic_y) -> tuple[int, int]:
        pixel_x = self._qt_center_x + (logic_x * self._cell_size_x)
        pixel_y = self._qt_center_y - (logic_y * self._cell_size_y)
        return int(pixel_x), int(pixel_y)

    def _to_logic_coordinates(self, pixel_x, pixel_y) -> tuple[float, float]:
        logic_x = pixel_x / self._cell_size_x
        logic_y = pixel_y / self._cell_size_y
        return logic_x, logic_y

    def draw_function_test(self, func, left_x: float, right_x: float, step: float = 1, line_thickness: int = 2):
        print("Func")

        def calculate_cell_size():
            # Calculate cell x-size
            points_num = right_x - left_x
            self._cell_size_x = self._plotting_rect.width() / points_num / step

            # Calculate cell y-size
            y_sorted = sorted(y_vals_list)
            y_top_value = y_sorted[int(len(y_sorted) * 0.9) - 1]
            y_bottom_value = y_sorted[0]
            self._cell_size_y = self._plotting_rect.height() / (y_top_value - y_bottom_value)

        # Create painter and restrict its action to plotting_rect area
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._plotting_rect)
        pen = QPen(Qt.blue, line_thickness, Qt.SolidLine)
        painter.setPen(pen)

        x = left_x
        y_vals_list = []

        while x <= right_x:
            try:
                y_vals_list.append(func(x))
            except Exception as ex:
                print(f"Error at x={x}: {ex}")

            x += step

        calculate_cell_size()
        self._draw_coord_grid()

        prev = None
        while x <= right_x:
            try:
                y = func(x)
                pixel_x, pixel_y = self._to_qt_coordinates(x, y)

                painter.drawLine(prev[0], prev[1], pixel_x, pixel_y)
                prev = (pixel_x, pixel_y)

            except Exception as ex:
                print(f"Error at x={x}: {ex}")

            x += step

        painter.end()
        self.update()

    def _draw_coord_grid(self):
        print("Grid")
        painter = QPainter(self._pixmap)
        thickness = 4
        border_pen = QPen(Qt.black, thickness, Qt.SolidLine)
        painter.setPen(border_pen)

        # Create area for chart plotting (axis rectangle for plotting)
        start_x = int(self.width() * 0.05)
        start_y = int(self.height() * 0.05)
        self._plotting_rect = QRect(
            start_x,
            start_y,
            self.width() - start_x * 2,
            self.height() - start_y * 2
        )
        painter.drawRect(self._plotting_rect)
        painter.end()

        # Calculate current center coordinates
        self._qt_center_x = self._plotting_rect.left() + int(self._plotting_rect.width() / 2)
        self._qt_center_y = self._plotting_rect.top() + int(self._plotting_rect.height() / 2)

        # Prepare to draw grid lines
        grid_pen = QPen(Qt.black, 1, Qt.DotLine)
        painter.setPen(grid_pen)
        font_metrics = painter.fontMetrics()

        # Draw (vertical or 'x') grid lines
        x = self._plotting_rect.left()
        while x <= self._plotting_rect.right():
            painter.drawLine(int(x), self._plotting_rect.top(), int(x), self._plotting_rect.bottom())

            # Draw cell's legend
            logic_x, _ = self._to_logic_coordinates(x, 0)
            text = f"{logic_x:.1f}"
            text_width = font_metrics.horizontalAdvance(text)
            text_x = int(x - text_width / 2)
            text_y = int(self._plotting_rect.bottom() + font_metrics.height() + (self._plotting_rect.height() * 0.05))
            painter.drawText(text_x, text_y, text)

            # Advance further
            x += self._cell_size_x

        # Draw (horizontal or 'y') grid lines
        y = self._plotting_rect.bottom()
        while y >= self._plotting_rect.top():
            painter.drawLine(self._plotting_rect.left(), int(y), self._plotting_rect.right(), int(y))

            # Draw cell's legend
            _, logic_y = self._to_logic_coordinates(0, y)
            text = f"{logic_y:.1f}"
            text_width = font_metrics.horizontalAdvance(text)
            text_x = int(self._plotting_rect.left() - text_width - (self._plotting_rect.width() * 0.05))
            text_y = int(self._plotting_rect.bottom() - y + (font_metrics.ascent() / 2))
            painter.drawText(text_x, text_y, text)

            # Advance further
            y += self._cell_size_y

        painter.end()
        self.update()

    def draw_central_dot(self):
        painter = QPainter(self._pixmap)
        painter.setClipRect(self._plotting_rect)
        pen = QPen(Qt.red, 5, Qt.SolidLine)
        painter.setPen(pen)
        x, y = self._to_qt_coordinates(0, 0)
        painter.drawPoint(x, y)
        painter.end()
        self.update()

    # def draw_function(self, func, x_start, x_end, step=0.1):
    #     self._last_func = partial(self.draw_function, func, x_start, x_end, step)
    #
    #     painter = QPainter(self._pixmap)
    #     painter.setClipRect(self._plotting_rect)
    #     pen = QPen(Qt.blue, 2)
    #     painter.setPen(pen)
    #
    #     x = x_start
    #     prev = None
    #     while x <= x_end:
    #         try:
    #             y = func(x)
    #             px, py = self._to_pyside_coords(x, y)
    #             if math.isfinite(y):
    #                 if prev is not None:
    #                     if abs(prev[1] - py) < self.height():
    #                         painter.drawLine(prev[0], prev[1], px, py)
    #                 prev = (px, py)
    #             else:
    #                 prev = None
    #
    #         except (ZeroDivisionError, ValueError, OverflowError):
    #             prev = None
    #
    #         except Exception as ex:
    #             print(f"Error at x={x}: {ex}")
    #
    #         x += step
    #
    #     painter.end()
    #     self.update()

    # def draw_function_cones(self, func, x_start, x_end, color=QColor(80, 160, 255), step=0.1):
    #     self._last_func = partial(self.draw_function_cones, func, x_start, x_end, color, step)
    #
    #     painter = QPainter(self._pixmap)
    #     painter.setClipRect(self._plotting_rect)
    #
    #     cone_width = 1.0
    #     x = x_start
    #     prev_y = None
    #     max_y_jump = (self._logical_range_y * 0.3)
    #     while x <= x_end:
    #         try:
    #             y = func(x)
    #
    #             if not math.isfinite(y):
    #                 prev_y = None
    #                 x += step
    #                 continue
    #
    #             if prev_y is not None and abs(y - prev_y) > max_y_jump:
    #                 prev_y = y
    #                 x += step
    #                 continue
    #
    #             qt_top_x, qt_top_y = self._to_pyside_coords(x, y)
    #             qt_left_x, qt_left_y = self._to_pyside_coords(x - cone_width / 2, 0)
    #             qt_right_x, qt_right_y = self._to_pyside_coords(x + cone_width / 2, 0)
    #
    #             top_point = QPoint(qt_top_x, qt_top_y)
    #             left_point = QPoint(qt_left_x, qt_left_y)
    #             right_point = QPoint(qt_right_x, qt_right_y)
    #
    #             cone = QPolygon([top_point, left_point, right_point])
    #             painter.setBrush(QBrush(color))
    #             painter.setPen(QPen(QColor(0, 0, 0), 0.5))
    #             painter.drawPolygon(cone)
    #
    #             # Преобразуем центр и радиусы
    #             cx, cy = self._to_pyside_coords(x, 0)
    #             rx = abs(left_point.x() - right_point.x()) // 2
    #             ry = int(0.1 * abs(y) * self._scale * (self._plotting_rect.height() / (2 * self._logical_range_y)))
    #
    #             # QRect, in ellipse
    #             rect = QRect(cx - rx, cy - ry, 2 * rx, 2 * ry)
    #
    #             # Left side
    #             painter.setPen(Qt.NoPen)
    #             painter.setBrush(QBrush(color.darker(150)))
    #             painter.drawPie(rect, 180 * 16, 90 * 16)  # from 180° to 270° left
    #
    #             # Right side
    #             painter.setBrush(QBrush(color))
    #             painter.drawPie(rect, 270 * 16, 90 * 16)
    #
    #             # Draw shadow
    #             shadow = QPolygon([top_point, left_point, QPoint(top_point.x(), left_point.y())])
    #             painter.setBrush(QBrush(color.darker(150)))
    #             painter.drawPolygon(shadow)
    #
    #         except (ZeroDivisionError, ValueError, OverflowError):
    #             prev_y = None
    #         except Exception as e:
    #             print(f"Error at x={x}: {e}")
    #
    #         x += step
    #
    #     painter.end()
    #     self.update()
