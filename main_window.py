from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QToolBar,
    QStatusBar,
    QLabel,
    QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QSize
from PyQt6 import QtCore, QtWidgets
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar

)
import sys

import re

import matplotlib
matplotlib.use('QtAgg')

from plot_draw import PlotWindow

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# Subclass QMainWindow application main window


class CalcMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.plot_window = None

        # Name of window
        self.setWindowTitle("Advanced Calculator")

        # Size of window
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Center window
        self.center()

        # Select box layout
        self.generalLayout = QVBoxLayout()

        # Parent of GUI elements
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        # Sample button
        sample_button = QAction("&Sample button", self)
        sample_button.setStatusTip("This is Sample button")
        sample_button.triggered.connect(self.sample_button_click)

        # Plot calc button
        plot_calc_button = QAction("&Draw plot", self)
        plot_calc_button.setStatusTip("Open plot calc")
        plot_calc_button.triggered.connect(self.draw_plot_window)

        # Exit Button
        exit_button = QAction("&Quit", self)
        exit_button.setStatusTip("Quit app")
        exit_button.triggered.connect(QApplication.instance().quit)

        # Toolbar
        toolbar = QToolBar("Main toolbar")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        # Adding buttons to toolbar
        toolbar.addAction(sample_button)
        toolbar.addAction(plot_calc_button)
        toolbar.addAction(exit_button)

        # Create statusbar
        self.setStatusBar(QStatusBar(self))

    def draw_plot_window(self):
        self.plot_window = PlotWindow(self)
        self.plot_window.show()
        self.hide()
        print('Plotter opened')

    def sample_button_click(self, s):
        print('button clicked')

    def quit_app(self):
        QApplication.instance().quit

    # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())



def main():
    calcApp = QApplication(sys.argv)
    # calcApp.setAttribute(Qt.ApplicationAttribute.AA_DontUseNativeDialogs, True)
    MainW = CalcMainWindow()
    MainW.show()
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
