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

# Widget for plot display


class MplCanvas(FigureCanvas):
    # c
    def __init__(self, parent=None, width=11, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PlotWindow(QWidget):
    def __init__(self, menu_window):
        super().__init__()
        # Setting parent window
        self.parent = menu_window
        # Setting name of window
        self.setWindowTitle("Plot Window")
        # Rezisizing window
        self.resize(600, 600)
        # Centering window
        self.center()

        # Create canvas for plot
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.grid(True)

        # Create toolbar, passing canvas as first parament, parent (self, the PlotWindow) as second.
        canvas_toolbar = NavigationToolbar(self.canvas, self)

        # Create button for inserting data
        data_button = QPushButton("Insert fuction")
        data_button.clicked.connect(self.get_function)

        # Create button for clearing plot
        clear_button = QPushButton("Clear plot")
        clear_button.clicked.connect(self.clear_plot)

        # Create button for going back to menu
        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.back_to_menu)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Creating bottom layout for buttons
        bottom_layout = QHBoxLayout()

        # Adding widgets to main layout
        main_layout.addWidget(canvas_toolbar)
        main_layout.addWidget(self.canvas)

        # Adding buttons to bottom widget
        bottom_layout.addWidget(
            data_button, alignment=Qt.AlignmentFlag.AlignLeft)
        bottom_layout.addWidget(
            clear_button, alignment=Qt.AlignmentFlag.AlignCenter)
        bottom_layout.addWidget(
            back_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Adding bottom layout to main layout
        main_layout.addLayout(bottom_layout)

        # Setting layout for window
        self.setLayout(main_layout)

    def back_to_menu(self):
        self.close()
        self.parent.show()
        print('Back to menu')

    def clear_plot(self):
        self.canvas.axes.cla()
        self.canvas.axes.grid(True)
        self.canvas.draw()

    def get_function(self):
        print('Get data for plot')
        function_str, done1 = QtWidgets.QInputDialog.getText(
            self, 'Function', 'Enter funcion:')
        lim1, done2 = QtWidgets.QInputDialog.getDouble(
            self, 'Lower limit', 'Enter lower limit:')
        lim2, done3 = QtWidgets.QInputDialog.getDouble(
            self, 'Upper limit', 'Enter upper limit:')
        if done1 and done2 and done3:
            try:
                if lim1 > lim2:
                    raise(ValueError)
                xvals = np.arange(lim1, lim2, 0.01)
                function_str_math = "lambda x: "
                function_str_math += convert_to_math(function_str)
                fx = eval(function_str_math)
                yvals = fx(xvals)
                self.canvas.axes.plot(xvals, yvals)
                self.canvas.axes.grid(True)
                self.canvas.axes.set_title(f'$f(x) = {function_str}$')
                self.canvas.axes.axhline(0, color='black', linewidth=1)
                self.canvas.axes.axvline(0, color='black', linewidth=1)
                self.canvas.draw()
            except:
                self.error_window(function_str, lim1, lim2)

    # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def error_window(self, str, lim1, lim2):
        message_box = QMessageBox()
        if lim1 > lim2:
            message_box.setText(f"Lower limit is greater than upper limit.")
            print("Error limits")
        else:
            message_box.setText(
                f"Data enetered:\nf(x)={str}\nlim1={lim1}\nlim2={lim2}")
            print("Error data")
        message_box.setWindowTitle("ERROR")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Action after clicking ok
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")


def convert_to_math(expression):
    # Change 'sin' to 'np.sin'
    expression = re.sub(r'\bsin\b', 'np.sin', expression)
    # Change 'x' to '*x'
    expression = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expression)
    # Change '^' to '**'
    expression = expression.replace('^', '**')
    # Adding multiplication sing in 'x(' or ')x'
    expression = re.sub(r'(\d)(\()', r'\1*\2', expression)
    expression = re.sub(r'(\))([a-zA-Z])', r'\1*\2', expression)
    return expression


def main():
    calcApp = QApplication(sys.argv)
    MainW = CalcMainWindow()
    MainW.show()
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
