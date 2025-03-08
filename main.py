from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
import sys

from gui import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # Window creation and resize as half of screen space
        self.setWindowTitle("Qweyke Charter")
        self.setMinimumSize(800, 600)
        self.resize(int(QApplication.primaryScreen().geometry().width() * 0.5),
                      int(QApplication.primaryScreen().geometry().height() * 0.5))

        self.gui.plot_btn.connect()

app = QApplication(sys.argv)
window = MainWindow()

window.show()
sys.exit(app.exec())
