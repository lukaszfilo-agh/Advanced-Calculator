import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QStatusBar
)

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# Subclass QMainWindow application main window


class CalcMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Name of window
        self.setWindowTitle("Advanced Calculator")

        # Size of window
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)

        # Select box layout
        self.generalLayout = QVBoxLayout()

        # Parent of GUI elements
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)

        # Sample button
        sample_button = QAction("&Sample button", self)
        sample_button.setStatusTip("This is Sample button")
        sample_button.triggered.connect(self.SampleButtonClick)

        # Plot calc button
        plot_calc_button = QAction("&Draw plot", self)
        plot_calc_button.setStatusTip("Open plot calc")
        plot_calc_button.triggered.connect(self.DrawPlotWindow)

        #Exit Button
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


    def DrawPlotWindow(self):
        print('Plotter opened')

    def SampleButtonClick(self, s):
        print('button clicked')
    
    def quitApp(self):
        QApplication.instance().quit

def main():
    calcApp = QApplication(sys.argv)
    MainW = CalcMainWindow()
    MainW.show()
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
