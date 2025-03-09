"""pyside6-uic gui.py -o canvas.ui"""

import sys

import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from mpl_toolkits.mplot3d import Axes3D

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

        self.figure = plt.figure()
        self.plot_area_1 = self.figure.add_subplot(111, projection="3d")

        self.plot_cone(self.plot_area_1, 5, "red", 1)

        self.figure_canvas = FigureCanvasQTAgg(self.figure)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.figure_canvas)

        self.gui.plot_wdgt.setLayout(layout)

    def plot_cone(self, plot_area: Axes3D, cone_height: float, color: str, density: float):
        CIRCLE_BASE_RADIUS = 1
        PRECISE = 100

        # Polar coord creation
        radius_list = np.linspace(0, CIRCLE_BASE_RADIUS, PRECISE)
        theta_in_radians_list = np.linspace(0, 2 * np.pi, PRECISE)

        # Polar coord meshgrid (2 matrix for all combs of theta and r)
        r_matrix, theta_matrix = np.meshgrid(radius_list, theta_in_radians_list)

        x_coord_list = r_matrix * np.cos(theta_matrix)
        y_coord_list = r_matrix * np.sin(theta_matrix)
        z_coord_list = cone_height - (cone_height / CIRCLE_BASE_RADIUS) * r_matrix

        plot_area.plot_surface(x_coord_list, y_coord_list, z_coord_list, color=color, alpha=density)


app = QApplication(sys.argv)
window = MainWindow()

window.show()
sys.exit(app.exec())
