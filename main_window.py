from math import sqrt, floor
from typing import Optional, Dict, Callable
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

        # Display widget:
        self.__display_field: Optional[QWidget] = None

        # Operations widget:
        self.__operations_field: Optional[QWidget] = None

        # Str val of display:
        self.__str_val = ""

        # Name, size of window:
        self.setWindowTitle("Advanced Calculator")
        self.setFixedSize(WINDOW_WIDTH + 10, WINDOW_HEIGHT - 200)

        # Center window:
        self.center()

        # Dark, black:
        # self.setStyleSheet("background-color: #181818")

        # Layouts:
        final_layout = QVBoxLayout()
        field_layout = QVBoxLayout()

        # Creating font:
        font = QFont("Calibri", 14)

        # Label for results display:
        self.__display_field = QLabel("0")

        # Label for displaying operations:
        self.__operations_field = QLabel("")

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
            button_percent = QPushButton("%", self)
            button_percent.setFont(font)
            button_CE = QPushButton("CE", self)
            button_CE.setFont(font)
            button_C = QPushButton("C", self)
            button_C.setFont(font)
            button_rem = QPushButton("<-", self)
            button_rem.setFont(font)

            first_line = [button_percent, button_CE, button_C, button_rem]

            # Second line:
            button_measurable = QPushButton("1/x", self)
            button_measurable.setFont(font)
            button_squared = QPushButton("x**2", self)
            button_squared.setFont(font)
            button_sq_root = QPushButton("sqrt(x)", self)
            button_sq_root.setFont(font)
            button_div = QPushButton("/", self)
            button_div.setFont(font)

            second_line = [button_measurable, button_squared, button_sq_root, button_div]

            # Third line:
            button_7 = QPushButton("7", self)
            button_7.setFont(font)
            button_8 = QPushButton("8", self)
            button_8.setFont(font)
            button_9 = QPushButton("9", self)
            button_9.setFont(font)
            button_x = QPushButton("x", self)
            button_x.setFont(font)

            third_line = [button_7, button_8, button_9, button_x]

            # Forth line:
            button_4 = QPushButton("4", self)
            button_4.setFont(font)
            button_5 = QPushButton("5", self)
            button_5.setFont(font)
            button_6 = QPushButton("6", self)
            button_6.setFont(font)
            button_minus = QPushButton("-", self)
            button_minus.setFont(font)

            forth_line = [button_4, button_5, button_6, button_minus]

            # Fifth line:
            button_1 = QPushButton("1", self)
            button_1.setFont(font)
            button_2 = QPushButton("2", self)
            button_2.setFont(font)
            button_3 = QPushButton("3", self)
            button_3.setFont(font)
            button_plus = QPushButton("+", self)
            button_plus.setFont(font)

            fifth_line = [button_1, button_2, button_3, button_plus]

            # Sixth line:
            button_plus_minus = QPushButton("+/-", self)
            button_plus_minus.setFont(font)
            button_0 = QPushButton("0", self)
            button_0.setFont(font)
            button_dot = QPushButton(".", self)
            button_dot.setFont(font)
            button_eq = QPushButton("=", self)
            button_eq.setFont(font)

            sixth_line = [button_plus_minus, button_0, button_dot, button_eq]

            # Getting all buttons:
            buttons = first_line + second_line + third_line + forth_line + fifth_line + sixth_line

            # Connecting buttons to operations manager:
            for button in buttons:
                button.clicked.connect(self.__manage_clicks)

            # Gathering all lines and lines layouts:
            all_lines = [first_line, second_line, third_line, forth_line, fifth_line, sixth_line]
            all_layouts = [buttons_layout1, buttons_layout2, buttons_layout3, buttons_layout4, buttons_layout5, buttons_layout6]

            for i in range(len(all_lines)):
                for j in range(4):
                    all_layouts[i].addWidget(all_lines[i][j])
                general_layout.addLayout(all_layouts[i])
            return general_layout
        buttons_layout = get_buttons_layout()

        font.setPointSize(45)
        self.__display_field.setFont(font)

        font.setPointSize(8)
        self.__operations_field.setFont(font)

        # White:
        #field.setStyleSheet("color: #FFFFFF")
        # Black:
        #field.setStyleSheet("background-color: #181818")

        # Toolbar
        toolbar = QToolBar("Main toolbar")
        toolbar.setMovable(False)

        # Creating sample buttons and adding to toolbar:
        def create_sample_buttons() -> None:

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

            # Adding buttons to toolbar
            toolbar.addAction(sample_button)
            toolbar.addAction(plot_calc_button)
            toolbar.addAction(exit_button)
        create_sample_buttons()

        # Setting up final layout:
        field_layout.addWidget(self.__operations_field, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        field_layout.addWidget(self.__display_field, alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        final_layout.addLayout(field_layout)
        final_layout.addLayout(buttons_layout)

        # Parent of GUI elements
        central_widget = QWidget()
        central_widget.setLayout(final_layout)

        # Adding to window:
        self.setCentralWidget(central_widget)
        self.addToolBar(toolbar)

        # Create statusbar:
        self.setStatusBar(QStatusBar(self))

    # Function to manage clicks:
    def __manage_clicks(self) -> None:
        # Get a button which is a sender of this information:
        sender = self.sender()

        # Delete text - set to 0: - WORKS
        if sender.text() in ["C", "CE"]:
            self.__str_val = ""
            self.__display_field.setText("0")
            self.__operations_field = ""
        # Remove digits: - WORKS
        elif sender.text() == "<-":
            # if we can go back - there is something to delete and there is no special sign:
            if len(self.__str_val) > 0 and self.__str_val[-1] not in ["/", "x", "-", "+"]:
                self.__str_val = str(eval(self.__str_val) // 10)
                # if we get zeros we simply display 0 and reset our counter:
                if self.__str_val in ["0", "0.0"]:
                    self.__display_field.setText("0")
                    self.__str_val = ""
                # Otherwise we count normally:
                else:
                    self.__display_field.setText(self.__str_val)

        # Evaluate:
        elif sender.text() == "=":
            # if something was entered - it's not the basic 0 in the display:
            if self.__str_val != "":
                try:
                    # We evaluate the str_val:
                    print(self.__str_val)
                    count_val = eval(self.__str_val)
                    print(count_val)
                    # We check if there was a division and rest i 0, then we omit it:
                    if isinstance(count_val, float) and abs(count_val) > 1 and count_val % int(count_val) == 0.0:
                        count_val = int(count_val)
                    # We keep the value for later calculations:
                    self.__str_val = f"{count_val}"
                    print(self.__str_val)
                    # We display the result:
                    self.__display_field.setText(self.__str_val)
                # In case of division by zero:
                except ZeroDivisionError:
                    self.__display_field.setText("Err")
                    self.__str_val = ""
        else:
            # Check for max display length:
            if len(self.__display_field.text()) < 13:
                # Adding digits: - WORKS
                if sender.text() in [str(i) for i in range(0, 10)]:
                    if sender.text() != "0" or (sender.text() == "0" and self.__display_field.text()[0] != "0"):
                        self.__str_val += sender.text()
                        self.__display_field.setText(self.__str_val)
                elif sender.text() in ["/", "x", "-", "+"]:
                    if 12 > len(self.__str_val) > 0 and self.__str_val[-1] not in ["/", "*", "-", "+"]:
                        if sender.text() == "x":
                            self.__str_val += "*"
                        else:
                            self.__str_val += sender.text()
                        self.__display_field.setText(self.__str_val)
            # We have overloaded the display:
            # else:
            #     if sender.text() in ["/", "x", "-", "+"]:
            #         if self.__str_val[-1] not in ["/", "*", "-", "+"]:
            #             if sender.text() == "x":
            #                 self.__str_val += "*"
            #             else:
            #                 self.__str_val += sender.text()
                # elif sender.text() in [str(i) for i in range(0, 10)]:
                #     self.__str_val += sender.text()

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