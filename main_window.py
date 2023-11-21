import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QGridLayout,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
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


def main():
    calcApp = QApplication(sys.argv)
    MainW = CalcMainWindow()
    MainW.show()
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
