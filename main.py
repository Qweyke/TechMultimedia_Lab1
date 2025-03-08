"""pyside6-uic gui.py -o canvas.ui"""

import sys

import matplotlib.pyplot as plt
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg

from funcs import calculate_func, Function
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
        self.subplot1 = self.figure.add_subplot(121, projection="3d")
        self.subplot2 = self.figure.add_subplot(122, projection="3d")

        x_list = np.linspace(0, 10, 100)
        y_list = np.linspace(0, 10, 100)
        z_list = calculate_func(Function.sin_mult, 1, 1000, 100)

        self.subplot1.scatter(x_list, y_list, z_list)
        self.subplot2.scatter(x_list, y_list, z_list)

        self.figure_canvas = FigureCanvasQTAgg(self.figure)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.figure_canvas)

        self.gui.plot_wdgt.setLayout(layout)

    #     self.gui.plot_btn.clicked.connect(lambda: self. plot_func(Function.sin_mult, 10))
    #
    # def plot_func(self, func_type, start, end, step):
    #     print(calculate_func(func_type, start, end, step))


app = QApplication(sys.argv)
window = MainWindow()

window.show()
sys.exit(app.exec())
