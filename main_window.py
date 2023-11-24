from typing import Optional
import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QWidget,
    QPushButton,
    QToolBar,
    QStatusBar, QTextEdit
)

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600


# Subclass QMainWindow application main window
class CalcMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Other windows needed in the future:
        self.plot_window: Optional[QWidget] = None

        # Number that will be displayed; math operations will be performed on it:
        self.__display_value: float = 0

        # Name, size of window:
        self.setWindowTitle("Advanced Calculator")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT - 200)

        # Center window
        self.center()

        # Dark, black:
        #self.setStyleSheet("background-color: #181818")

        # Creating font:
        font = QFont("Calibri", 14)

        # Helper to get buttons layout:
        def get_buttons_layout() -> QVBoxLayout:

            # Create layouts:
            general_layout = QVBoxLayout()
            buttons_layout1 = QHBoxLayout()
            buttons_layout2 = QHBoxLayout()
            buttons_layout3 = QHBoxLayout()
            buttons_layout4 = QHBoxLayout()
            buttons_layout5 = QHBoxLayout()
            buttons_layout6 = QHBoxLayout()

            # First line:
            button_percent = QPushButton("%")
            button_percent.setFont(font)
            button_CE = QPushButton("CE")
            button_CE.setFont(font)
            button_C = QPushButton("C")
            button_C.setFont(font)
            button_rem = QPushButton("<-")
            button_rem.setFont(font)

            first_line = [button_percent, button_CE, button_C, button_rem]

            # Second line:
            button_measurable = QPushButton("1/x")
            button_measurable.setFont(font)
            button_squared = QPushButton("x**2")
            button_squared.setFont(font)
            button_sq_root = QPushButton("sqrt(x)")
            button_sq_root.setFont(font)
            button_div = QPushButton("/")
            button_div.setFont(font)

            second_line = [button_measurable, button_squared, button_sq_root, button_div]

            # Third line:
            button_7 = QPushButton("7")
            button_7.setFont(font)
            button_8 = QPushButton("8")
            button_8.setFont(font)
            button_9 = QPushButton("9")
            button_9.setFont(font)
            button_x = QPushButton("x")
            button_x.setFont(font)

            third_line = [button_7, button_8, button_9, button_x]

            # Forth line:
            button_4 = QPushButton("4")
            button_4.setFont(font)
            button_5 = QPushButton("5")
            button_5.setFont(font)
            button_6 = QPushButton("6")
            button_6.setFont(font)
            button_minus = QPushButton("-")
            button_minus.setFont(font)

            forth_line = [button_4, button_5, button_6, button_minus]

            # Fifth line:
            button_1 = QPushButton("1")
            button_1.setFont(font)
            button_2 = QPushButton("2")
            button_2.setFont(font)
            button_3 = QPushButton("3")
            button_3.setFont(font)
            button_plus = QPushButton("+")
            button_plus.setFont(font)

            fifth_line = [button_1, button_2, button_3, button_plus]

            # Sixth line:
            button_plus_minus = QPushButton("+/-")
            button_plus_minus.setFont(font)
            button_0 = QPushButton("0")
            button_0.setFont(font)
            button_dot = QPushButton(".")
            button_dot.setFont(font)
            button_eq = QPushButton("=")
            button_eq.setFont(font)

            sixth_line = [button_plus_minus, button_0, button_dot, button_eq]

            # Gathering all lines and lines layouts:
            all_lines = [first_line, second_line, third_line, forth_line, fifth_line, sixth_line]
            all_layouts = [buttons_layout1, buttons_layout2, buttons_layout3, buttons_layout4, buttons_layout5, buttons_layout6]

            for i in range(len(all_lines)):
                for j in range(4):
                    all_layouts[i].addWidget(all_lines[i][j])
                general_layout.addLayout(all_layouts[i])
            return general_layout

        # Layouts:
        final_layout = QVBoxLayout()
        field_layout = QVBoxLayout()
        buttons_layout = get_buttons_layout()

        font.setPointSize(45)

        # Label for results display:
        field = QLabel(f"{self.__display_value}")
        field.setFont(font)

        # White:
        #field.setStyleSheet("color: #FFFFFF")
        # Black:
        #field.setStyleSheet("background-color: #181818")


        # Sample button:
        sample_button = QAction("&Sample button", self)
        sample_button.setStatusTip("This is Sample button")
        sample_button.triggered.connect(self.sample_button_click)

        # Plot calc button:
        plot_calc_button = QAction("&Draw plot", self)
        plot_calc_button.setStatusTip("Open plot calc")
        plot_calc_button.triggered.connect(self.draw_plot_window)

        # Exit Button:
        exit_button = QAction("&Quit", self)
        exit_button.setStatusTip("Quit app")
        exit_button.triggered.connect(QApplication.instance().quit)

        # Toolbar
        toolbar = QToolBar("Main toolbar")
        toolbar.setMovable(False)

        # Adding buttons to toolbar
        toolbar.addAction(sample_button)
        toolbar.addAction(plot_calc_button)
        toolbar.addAction(exit_button)

        # Setting up final layout:
        field_layout.addWidget(field, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        final_layout.addLayout(field_layout)
        final_layout.addLayout(buttons_layout)

        # Parent of GUI elements
        central_widget = QWidget()
        central_widget.setLayout(final_layout)

        # Adding to window:
        self.setCentralWidget(central_widget)
        self.addToolBar(toolbar)

        # Create statusbar
        self.setStatusBar(QStatusBar(self))

    def draw_plot_window(self):
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
    MainW = CalcMainWindow()
    MainW.show()
    sys.exit(calcApp.exec())


if __name__ == "__main__":
    main()
