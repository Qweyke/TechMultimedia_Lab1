import sys

from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QApplication
from sympy import symbols, sympify, lambdify

from chart_widget import ChartWidget
from gui import Ui_MainWindow


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Create chart widget, insert it to GUI widget's space
        self._chart_widget = ChartWidget(parent=self.ui.plot_wdgt)
        layout = QVBoxLayout(self.ui.plot_wdgt)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._chart_widget)

        # Connect btns
        self.ui.plot_btn.clicked.connect(self._plot_func)
        self.ui.clear_btn.clicked.connect(self._chart_widget.clear_canvas)

    def _plot_func(self):
        x = symbols('x')
        expr = sympify(self.ui.func_lineEdit.text())
        f = lambdify(x, expr, modules=['math'])

        self._chart_widget.draw_function_test(f, self.ui.from_spinBox.value(), self.ui.to_spinBox.value())

        # if self.ui.cones_checkBox.isChecked():
        #     self._chart_widget.draw_function_cones(f, self.ui.from_spinBox.value(), self.ui.to_spinBox.value(),
        #                                            step=self.ui.step_spinBox.value())
        # else:
        #     self._chart_widget.draw_function(f, self.ui.from_spinBox.value(), self.ui.to_spinBox.value(),
        #                                      step=self.ui.step_spinBox.value())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec())
