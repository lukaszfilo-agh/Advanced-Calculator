import sys

import re

import matplotlib
matplotlib.use('QtAgg')

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import numpy as np

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
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
    QLabel
)

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

# Class for plot display
class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PlotWindow(QWidget):
    def __init__(self, menu_window):
        super().__init__()
        self.parent = menu_window
        self.setWindowTitle("Plot Window")
        self.resize(600, 600)
        self.center()

        self.main_layout = QVBoxLayout()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.grid(True)
        self.main_layout.addWidget(self.canvas)

        bottom_layout = QHBoxLayout()

        data_button = QPushButton("Insert data")
        data_button.clicked.connect(self.get_data)
        bottom_layout.addWidget(data_button, alignment=Qt.AlignmentFlag.AlignLeft)

        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.back_to_menu)
        bottom_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(bottom_layout)
        self.setLayout(self.main_layout)

    def back_to_menu(self):
        self.close()
        self.parent.show()
        print('Back to menu')

    def get_data(self):
        print('Get data for plot')
        function_str, done1 = QtWidgets.QInputDialog.getText(
             self, 'Function', 'Enter funcion:')
        lim1, done2 = QtWidgets.QInputDialog.getInt(
           self, 'Lower limit', 'Enter lower limit:')
        lim2, done3 = QtWidgets.QInputDialog.getInt(
           self, 'Upper limit', 'Enter upper limit:')
        if done1 and done2 and done3:
            xvals = np.arange(lim1, lim2, 0.01)
            function_str = convert_to_math(function_str)
            fx = lambda x: eval(function_str)
            yvals = fx(xvals)
            self.canvas.axes.cla()
            self.canvas.axes.plot(xvals, yvals)
            self.canvas.axes.grid(True)
            self.canvas.draw()
    
    # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

def convert_to_math(zapis):
    # Zamiana 'x' na '*x'
    zapis = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', zapis)
    # Zamiana '^' na '**'
    zapis = zapis.replace('^', '**')
    # Dodanie znaku mnożenia w przypadku 'x(' lub ')x'
    zapis = re.sub(r'([a-zA-Z])(\()', r'\1*\2', zapis)
    zapis = re.sub(r'(\))([a-zA-Z])', r'\1*\2', zapis)

    return zapis

def main():
    calcApp = QApplication(sys.argv)
    MainW = CalcMainWindow()
    MainW.show()
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
