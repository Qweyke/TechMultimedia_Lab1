import sys

import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib.axes import Axes
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from mpl_toolkits.mplot3d import Axes3D

from funcs import func_1, func_2, func_3
from gui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # Window resize as half of screen space
        self.setWindowTitle("Qweyke Plotter")
        self.setMinimumSize(800, 600)
        self.resize(int(QApplication.primaryScreen().geometry().width() * 0.7),
                    int(QApplication.primaryScreen().geometry().height() * 0.7))

        # Creation of 3D chart widget
        self.figure = plt.figure()
        self.plot_area_1 = self.figure.add_subplot(121, projection="3d")
        self.plot_area_2 = self.figure.add_subplot(122)

        # Link QT widget and matplotlib canvas
        self.figure_canvas = FigureCanvasQTAgg(self.figure)
        plot_layout = QVBoxLayout()
        plot_layout.setContentsMargins(0, 0, 0, 0)
        plot_layout.setSpacing(0)
        plot_layout.addWidget(self.figure_canvas)
        self.gui.plot_wdgt.setLayout(plot_layout)

        start = 0
        end = 10
        step = 2

        self.gui.plot_btn.pressed.connect(lambda: self.plot_series(func_1, start, end, step))
        self.gui.plot_btn.pressed.connect(lambda: self.plot_func(self.plot_area_2, func_1, start, end, step))

    def plot_series(self, func, start, end, step):
        num_steps = int((end - start) / step)
        for i in range(num_steps):
            self.plot_cone(self.plot_area_1, func(start), "blue", 1, step_num=i)
            start += step

    def plot_cone(self, plot_area: Axes3D, cone_height: float, color: str, density: float, step_num: int = 0):
        CONE_BASE_RADIUS = 1
        SHIFT_FOR_START_IN_0 = 1

        # Cone's base antialiasing
        PRECISE = 10

        # Center shift for each cone in diagram
        X_SHIFT = CONE_BASE_RADIUS * step_num

        # Polar coord creation
        radius_list = np.linspace(0, CONE_BASE_RADIUS, PRECISE)
        theta_in_radians_list = np.linspace(0, 2 * np.pi, PRECISE)

        # Polar coord meshgrid (2 matrix for all combs of theta and r)
        r_matrix, theta_matrix = np.meshgrid(radius_list, theta_in_radians_list)

        x_coord_list = r_matrix * np.cos(theta_matrix) + SHIFT_FOR_START_IN_0 + X_SHIFT
        y_coord_list = r_matrix * np.sin(theta_matrix)

        z_coord_list = cone_height - (cone_height / CONE_BASE_RADIUS) * r_matrix

        # Plot a surface from all matrices
        plot_area.plot_surface(x_coord_list, y_coord_list, z_coord_list, color=color, alpha=density)

        # # Compute the z-limits based on actual data, not just cone_height
        # z_min = np.min(z_coord_list)
        z_max = np.max(z_coord_list)
        #
        # # Ensure z-limits are not the same, prevent singular transformation
        # if z_min == z_max:
        #     z_max += 1  # Slightly adjust z_max to avoid identical values
        #
        # # Set the limits to the same for all axes
        # max_val = max(np.max(x_coord_list), np.max(y_coord_list), z_max)
        max_val = np.max(x_coord_list)
        if np.any(x_coord_list < 0):
            min_x_limit = -max_val
        else:
            min_x_limit = 0

        #
        plot_area.set_xlim(min_x_limit, max_val)
        plot_area.set_ylim(-max_val, max_val)
        plot_area.set_zlim(-max_val, max_val)

        plot_area.set_xlabel('X')
        plot_area.set_ylabel('Y')
        plot_area.set_zlabel('Z')

        plot_area.view_init(elev=10, azim=95)  # elev is elevation angle, azim is azimuth angle

        self.figure_canvas.draw()

    def plot_func(self, plot_area: Axes, func, start, end, step):
        x_list = np.arange(start, end, step)
        y_list = func(x_list)

        plot_area.set_xlabel('x')
        plot_area.set_ylabel('y')
        plot_area.plot(x_list, y_list)

        self.figure_canvas.draw()


app = QApplication(sys.argv)
window = MainWindow()

window.show()
sys.exit(app.exec())
