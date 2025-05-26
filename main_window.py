from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout
from gui import Ui_MainWindow
import sys
import math

from test import PlotCanvas


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plot = PlotCanvas(self.ui.plot_wdgt)
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.plot)
        self.ui.plot_wdgt.setLayout(layout)

        self.ui.func_box.addItems(["sin(x)", "cos(x)", "x^2"])

        self.ui.plot_btn.clicked.connect(self.plot_graph)

    def plot_graph(self):
        text = self.ui.func_box.currentText()
        if text == "sin(x)":
            self.plot.set_function(math.sin)
        elif text == "cos(x)":
            self.plot.set_function(math.cos)
        elif text == "x^2":
            self.plot.set_function(lambda x: 0.05 * x ** 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
