import math
from typing import Optional, Union
import sys
from PyQt6.QtCore import Qt
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
    QStatusBar
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

        # Overflow display widget:
        self.__operations_field: Optional[QWidget] = None

        # Str val of display:
        self.__str_val = ""

        # Str val of overflow:
        self.__str_val_operations = ""

        # Name, size of window:
        self.setWindowTitle("Advanced Calculator")
        self.setFixedSize(WINDOW_WIDTH + 10, WINDOW_HEIGHT - 200)

        # Center window:
        self.__center()

        # Dark, black:
        # self.setStyleSheet("background-color: #181818")

        # Layouts:
        final_layout = QVBoxLayout()
        field_layout = QVBoxLayout()

        # Creating font:
        font = QFont("Calibri", 14)

        # Label for results display:
        self.__display_field = QLabel("")

        # Label for overflow management:
        self.__operations_field = QLabel("")

        # Helper to get buttons layout and connect them to action management function:
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
            all_layouts = [buttons_layout1, buttons_layout2, buttons_layout3, buttons_layout4, buttons_layout5,
                           buttons_layout6]

            for i in range(len(all_lines)):
                for j in range(4):
                    all_layouts[i].addWidget(all_lines[i][j])
                general_layout.addLayout(all_layouts[i])
            return general_layout

        buttons_layout = get_buttons_layout()

        font.setPointSize(45)
        self.__display_field.setFont(font)

        font.setPointSize(12)
        self.__operations_field.setFont(font)

        # White:
        # field.setStyleSheet("color: #FFFFFF")
        # Black:
        # field.setStyleSheet("background-color: #181818")

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
        field_layout.addWidget(self.__operations_field,
                               alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        field_layout.addWidget(self.__display_field,
                               alignment=Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
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

        # Helper function which rounds if there are too many digits after evaluation:
        def terminate_too_many_digits_after_dot(num: Union[float, str], e: str = None) -> Union[float, str]:

            # if we have float - only evaluated value:
            if isinstance(num, float):
                # Index of dot point:
                idx_dot_point = str(num).index(".")

                # Rounding to max possible digits:
                rounding_to = 13 - idx_dot_point - 1

                return round(num, rounding_to)
            # if we have str - e format value:
            idx_dot_point = num.index(".")

            # Rounding to max possible digits including e format length:
            rounding_to = 13 - idx_dot_point - 1 - len(e)

            return str(round(float(num), rounding_to))

        # Helper function which changes number to string e notation:
        def change_format_for_large_nums(num: Union[int, float]) -> str:
            return "{:e}".format(num)

        # Helper function to get e format:
        def get_e_format(num: float) -> str:
            e_format = ""

            # Fixing overflow after evaluation, we block immediate e format application to small numbers:
            if len(str(num)) >= 13 and abs(num) > 1:

                e_format = change_format_for_large_nums(num)

                # if we take too much display space with e format:
                if len(e_format) >= 13:
                    # We get the position of e - beginning of our format:
                    e_ind = e_format.index("e")

                    # Block situation of appearing e+00 - round with no e:
                    if e_format[e_ind + 1] == "0":
                        e_format = terminate_too_many_digits_after_dot(float(e_format))
                    # Else if there is something different then 0 after e:
                    else:
                        # We separate number for e:
                        num = e_format[:e_ind]
                        e = e_format[e_ind:]

                        # We round accordingly:
                        num = terminate_too_many_digits_after_dot(num, e)

                        # We connect rounded number with format:
                        e_format = num + e
            return e_format

        # Helper function which reoccurs in different cases of "=" operator:
        def set_displays_after_op_eq(value: float) -> None:
            # if we have floating point, get rid of too many digits after dot point:
            if isinstance(value, float) and len(str(value)) >= 13:
                value = terminate_too_many_digits_after_dot(value)

            # We'll keep the e format information in case there is one:
            e_format = get_e_format(value)

            # We keep evaluated value in str_val for further operations:
            self.__str_val = str(value)

            # But if we have e_format we enter it on display:
            if e_format != "":
                self.__display_field.setText(e_format)
            # Else - we enter the same value as in str_val:
            else:
                self.__display_field.setText(self.__str_val)

            # We keep evaluated value in str_val_operations for further operations:
            self.__str_val_operations = str(value)
            print(self.__str_val_operations)
            # But if we have e_format we enter it on operations display:
            if e_format != "":
                self.__operations_field.setText(e_format)
            # Else - we enter the same value as in str_val_operations:
            else:
                self.__operations_field.setText(self.__str_val_operations)

            # Reset str_val for further evaluation:
            self.__str_val = ""

        # Helper function to handle zero division error:
        def handle_zero_division_err() -> None:
            self.__operations_field.setText("")
            self.__display_field.setText("ZERO DIVISION")
            self.__str_val = ""
            self.__str_val_operations = ""

        # Helper function to handle value error:
        def handle_value_err() -> None:
            self.__operations_field.setText("")
            self.__display_field.setText("INVALID INPUT")
            self.__str_val = ""
            self.__str_val_operations = ""

        # Helper function managing 3 button clicks based on their function:
        def manage_1_over_x_sq_sqrt(button_name: str) -> None:
            operation = None
            if button_name == "1/x":
                operation = lambda x: 1/x
            elif button_name == "x**2":
                operation = lambda x: x**2
            elif button_name == "sqrt(x)":
                operation = lambda x: math.sqrt(x)

            # We have entered digits but have yet to perform any operation:
            if self.__str_val != "" and self.__str_val_operations == "":
                # We do not need to eval str_val:
                float_val = float(self.__str_val)
                float_val = operation(float_val)

                # if we have floating point, get rid of too many digits after dot point:
                if isinstance(float_val, float) and len(str(float_val)) >= 13:
                    float_val = terminate_too_many_digits_after_dot(float_val)

                # We'll keep the e format information in case there is one:
                e_format = get_e_format(float_val)

                # If we erased display, we don't change its view:
                if self.__display_field.text() != "":
                    # Update str_val in order to place it on display:
                    self.__str_val = str(float_val)
                else:
                    self.__str_val = ""

                # But if we have e_format we enter it on display:
                if e_format != "":
                    if e_format[-2:] != "00":
                        self.__display_field.setText(e_format)
                    else:
                        self.__display_field.setText(self.__str_val)
                # Else - we enter the same value as in str_val:
                else:
                    self.__display_field.setText(self.__str_val)

                # We keep evaluated value in str_val_operations and add new bin_op:
                self.__str_val_operations = str(float_val)

                # But if we have e_format we enter it on operations display with bin_op:
                if e_format != "":
                    self.__operations_field.setText(e_format)
                # Else - we enter the same value as in str_val_operations:
                else:
                    self.__operations_field.setText(self.__str_val_operations)

                # Keep value reset:
                self.__str_val = ""

            # We performed operations, but we don't have any following operator:
            elif self.__str_val_operations != 0 and self.__str_val_operations[-1] not in ["/", "*", "-", "+"]:
                # Evaluate:
                eval_str = eval(self.__str_val_operations)
                eval_str = operation(eval_str)

                # if we have floating point, get rid of too many digits after dot point:
                if isinstance(eval_str, float) and len(str(eval_str)) >= 13:
                    eval_str = terminate_too_many_digits_after_dot(eval_str)

                # We'll keep the e format information in case there is one:
                e_format = get_e_format(eval_str)

                # We keep evaluated value in str_val for further operations:
                self.__str_val = str(eval_str)

                # But if we have e_format we enter it on display:
                if e_format != "":
                    self.__display_field.setText(e_format)
                # Else - we enter the same value as in str_val:
                else:
                    self.__display_field.setText(self.__str_val)

                # We keep evaluated value in str_val_operations with bin_op for further operations:
                self.__str_val_operations = str(eval_str)

                # But if we have e_format we enter it on operations display with bin_op:
                if e_format != "":
                    self.__operations_field.setText(e_format)
                # Else - we enter the same value as in str_val_operations:
                else:
                    self.__operations_field.setText(self.__str_val_operations)

                # Setting str_val to "":
                self.__str_val = ""

            # We have str_val operations:
            elif self.__str_val_operations != 0 and self.__str_val_operations[-1] in ["/", "*", "-", "+"]:
                # We haven't entered any digits -
                # evaluate 1/x on str_val and perform operation with given op (enter result in str_val):
                if self.__str_val == "":
                    # Evaluate - only the number:
                    eval_str = eval(self.__str_val_operations[:-1])
                    eval_str = operation(eval_str)

                    # if we have floating point, get rid of too many digits after dot point:
                    if isinstance(eval_str, float) and len(str(eval_str)) >= 13:
                        eval_str = terminate_too_many_digits_after_dot(eval_str)

                    # Get e format:
                    e_format = get_e_format(eval_str)

                    # We keep evaluated value in str_val for further operations:
                    self.__str_val = str(eval_str)

                    if e_format != "":
                        self.__display_field.setText(e_format)
                    else:
                        self.__display_field.setText(self.__str_val)
                    # Str_val_operations remains as it was:
                # Else we have str_val - perform 1/x on it:
                else:
                    # Evaluate str_val
                    eval_str = eval(self.__str_val)
                    eval_str = operation(eval_str)

                    # if we have floating point, get rid of too many digits after dot point:
                    if isinstance(eval_str, float) and len(str(eval_str)) >= 13:
                        eval_str = terminate_too_many_digits_after_dot(eval_str)

                    # We don't track e format - we enter str_val so it's in range.

                    # Keep the value:
                    self.__str_val = str(eval_str)

                    # Display it:
                    self.__display_field.setText(self.__str_val)

        # Get a button which is a sender of this information:
        sender = self.sender()

        # Delete buttons:
        if sender.text() in ["C", "CE"]:
            # We get rid of all output:
            if sender.text() == "C":
                self.__str_val_operations = ""
                self.__operations_field.setText("")
                self.__str_val = ""
                self.__display_field.setText("")
            elif sender.text() == "CE":
                # Prevent situations in which we were able to delete main display
                # when there was operation field and no operator - resulted in inf:
                if self.__str_val_operations != "" and self.__str_val_operations[-1] in ["/", "*", "-", "+"]:
                    self.__str_val = ""
                    self.__display_field.setText("")
                # if its empty we can remove freely:
                elif self.__str_val_operations == "":
                    self.__str_val = ""
                    self.__display_field.setText("")
        # Remove digits:
        elif sender.text() == "<-":
            # Don't allow removal when we have e format:
            if "e" not in self.__display_field.text():
                # if there is something to delete:
                if len(self.__str_val) > 0:
                    eval_str = eval(self.__str_val)
                    # If we have a dot point:
                    if isinstance(eval_str, float):
                        # We simply override our string by removing the last char:
                        self.__str_val = self.__str_val[:-1]
                        # If we are at a situation that there's only dot point left, with nothing after it,
                        # we override again:
                        if self.__str_val[-1] == ".":
                            self.__str_val = self.__str_val[:-1]
                    # If we have int, we can just divide using "//" to get rid of the last digit:
                    else:
                        self.__str_val = str(eval(self.__str_val) // 10)
                    # Update display:
                    self.__display_field.setText(self.__str_val)
                    # If we got to plain zero we reset our str_val and start over:
                    if self.__str_val == "0":
                        self.__str_val = ""
        # Evaluating with "=":
        elif sender.text() == "=":
            # If there is an operator in str_val_operations:
            if len(self.__str_val_operations) > 0 and self.__str_val_operations[-1] in ["/", "*", "-", "+"]:
                try:
                    # We have 1 value - perform evaluation on itself:
                    if self.__str_val == "":
                        # We addd the same number to our evaluation:
                        self.__str_val_operations += self.__str_val_operations[:-1]
                        eval_str = eval(self.__str_val_operations)
                        set_displays_after_op_eq(eval_str)
                    # We have 2 values, evaluate regularly:
                    else:
                        # We str_val number to operation:
                        self.__str_val_operations += self.__str_val
                        eval_str = eval(self.__str_val_operations)
                        set_displays_after_op_eq(eval_str)

                except ZeroDivisionError:
                    handle_zero_division_err()
            # Else - we simply keep the number (nothing to evaluate on):
            else:
                pass
        # Digits in sender:
        elif sender.text() in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            # Protect against adding a number into display when
            # we have str_val_operations, but we don't have an operator:
            if len(self.__str_val_operations) > 0 and self.__str_val_operations[-1] not in ["/", "*", "-", "+"]:
                pass
            # Check for max display length - don't allow to add more digits if we don't have more space:
            elif (len(self.__str_val) < 13) or self.__display_field.text() in ["ZERO DIVISION", "INVALID INPUT"]:
                # If sender is not "0":
                if sender.text() != "0":
                    # If str_val is already at "0":
                    if self.__str_val == "0":
                        # We keep swap it, not append:
                        self.__str_val = sender.text()
                    # Else:
                    else:
                        # We append:
                        self.__str_val += sender.text()
                # If sender is "0":
                else:
                    # If there is nothing in str_val or no 0 at the beginning
                    # or 0 at the beginning, but we have a dot point:
                    if len(self.__str_val) == 0 or self.__str_val[0] != "0" or (
                            self.__str_val[0] == "0" and "." in self.__str_val):
                        # We append:
                        self.__str_val += sender.text()
                # Change value at display:
                self.__display_field.setText(self.__str_val)
        # Binary operators in sender:
        elif sender.text() in ["/", "x", "-", "+"]:
            # We get the binary op:
            bin_op = sender.text()
            if sender.text() == "x":
                bin_op = "*"
            # If there is nothing in operations:
            if len(self.__str_val_operations) == 0:
                # We have something to draw to operations field:
                if len(self.__str_val) > 0:
                    # We take input from str_val and add binary operator:
                    self.__str_val_operations += self.__str_val + bin_op
                    self.__operations_field.setText(self.__str_val_operations)

                    # We artificially set str_val to "" so that it won't be evaluated until we enter another value:
                    self.__str_val = ""
            # If there is something in operations field:
            else:
                # Str_val is empty - it wasn't overriden after entering bin_op:
                if self.__str_val == "":
                    # We have an operator - override:
                    if self.__str_val_operations[-1] in ["/", "*", "-", "+"]:
                        # We swap binary operators from str_val_operations:
                        self.__str_val_operations = self.__str_val_operations[:-1] + bin_op
                        # if there's no e format:
                        if "e" not in self.__operations_field.text():
                            self.__operations_field.setText(self.__str_val_operations)
                        else:
                            # We swap text from operations field:
                            self.__operations_field.setText(self.__operations_field.text()[:-1] + bin_op)
                    # No operator - add it:
                    else:
                        # Trying for 0 division error:
                        try:
                            # Evaluate value in str_val_operations - to check if we need e format:
                            eval_str = eval(self.__str_val_operations)

                            # if we have floating point, get rid of too many digits after dot point:
                            if isinstance(eval_str, float) and len(str(eval_str)) >= 13:
                                eval_str = terminate_too_many_digits_after_dot(eval_str)

                            # We'll keep the e format information in case there is one:
                            e_format = get_e_format(eval_str)

                            # If we erased display, we don't change its view:
                            if self.__display_field.text() != "":
                                # Update str_val in order to place it on display:
                                self.__str_val = str(eval_str)
                            else:
                                self.__str_val = ""

                            # But if we have e_format we enter it on display:
                            if e_format != "":
                                self.__display_field.setText(e_format)
                            # Else - we enter the same value as in str_val:
                            else:
                                self.__display_field.setText(self.__str_val)

                            # We keep evaluated value in str_val_operations and add new bin_op:
                            self.__str_val_operations += bin_op

                            # But if we have e_format we enter it on operations display with bin_op:
                            if e_format != "":
                                self.__operations_field.setText(e_format + bin_op)
                            # Else - we enter the same value as in str_val_operations:
                            else:
                                self.__operations_field.setText(self.__str_val_operations)

                            # Keep value reset:
                            self.__str_val = ""

                        except ZeroDivisionError:
                            handle_zero_division_err()
                # Else - we evaluate (we have 1 operator and str_val):
                else:
                    # Trying for 0 division error:
                    try:
                        # We get the value from str_val to our operations_val and evaluate:
                        self.__str_val_operations += self.__str_val
                        eval_str = eval(self.__str_val_operations)

                        # if we have floating point, get rid of too many digits after dot point:
                        if isinstance(eval_str, float) and len(str(eval_str)) >= 13:
                            eval_str = terminate_too_many_digits_after_dot(eval_str)

                        # We'll keep the e format information in case there is one:
                        e_format = get_e_format(eval_str)

                        # We keep evaluated value in str_val for further operations:
                        self.__str_val = str(eval_str)

                        # But if we have e_format we enter it on display:
                        if e_format != "":
                            self.__display_field.setText(e_format)
                        # Else - we enter the same value as in str_val:
                        else:
                            self.__display_field.setText(self.__str_val)

                        # We keep evaluated value in str_val_operations with bin_op for further operations:
                        self.__str_val_operations = str(eval_str) + bin_op

                        # But if we have e_format we enter it on operations display with bin_op:
                        if e_format != "":
                            self.__operations_field.setText(e_format + bin_op)
                        # Else - we enter the same value as in str_val_operations:
                        else:
                            self.__operations_field.setText(self.__str_val_operations)

                        # Setting str_val to "":
                        self.__str_val = ""
                    except ZeroDivisionError:
                        handle_zero_division_err()
        # Other buttons:
        elif sender.text() == "%":
            pass
        # 1/x, x**2, sqrt(x) in sender:
        elif sender.text() in ["1/x", "x**2", "sqrt(x)"]:
            # Protect against trying to do operation over string:
            if self.__display_field.text() not in ["ZERO DIVISION", "INVALID INPUT"]:
                # Trying for zero division and sqrt of negative values:
                try:
                    manage_1_over_x_sq_sqrt(sender.text())
                except ZeroDivisionError:
                    handle_zero_division_err()
                except ValueError:
                    handle_value_err()
        elif sender.text() == "+/-":
            pass

    def draw_plot_window(self):
        print('Plotter opened')

    def sample_button_click(self, s):
        print('button clicked')

    def quit_app(self):
        QApplication.instance().quit

    # Method for centering windows
    def __center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


def main():
    calc_app = QApplication(sys.argv)
    main_w = CalcMainWindow()
    main_w.show()
    sys.exit(calc_app.exec())


if __name__ == "__main__":
    main()
