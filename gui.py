# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'canvas.ui'
##
## Created by: Qt User Interface Compiler version 6.8.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGridLayout, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.func_box = QComboBox(self.centralwidget)
        self.func_box.setObjectName(u"func_box")

        self.gridLayout.addWidget(self.func_box, 1, 2, 1, 1)

        self.plot_btn = QPushButton(self.centralwidget)
        self.plot_btn.setObjectName(u"plot_btn")

        self.gridLayout.addWidget(self.plot_btn, 0, 2, 1, 1)

        self.plot_wdgt = QWidget(self.centralwidget)
        self.plot_wdgt.setObjectName(u"plot_wdgt")

        self.gridLayout.addWidget(self.plot_wdgt, 0, 1, 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(whatsthis)
        self.func_box.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Choose a function to plot</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(whatsthis)
        self.plot_btn.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to plot chosen function</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.plot_btn.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
    # retranslateUi

