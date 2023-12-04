import math
import sys
from typing import Optional, Union
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

from plot_draw import PlotWindow

# Window size:
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

# Max number of digits in display:
MAX_DIGITS = 13


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
            buttons_layout7 = QHBoxLayout()

            # First line:
            button_pi = QPushButton("π", self)
            button_pi.setFont(font)
            button_e = QPushButton("e", self)
            button_e.setFont(font)
            button_CE = QPushButton("CE", self)
            button_CE.setFont(font)
            button_C = QPushButton("C", self)
            button_C.setFont(font)
            button_rem = QPushButton("<-", self)
            button_rem.setFont(font)

            first_line = [button_pi, button_e, button_CE, button_C, button_rem]

            # Second line:
            button_ln = QPushButton("ln", self)
            button_ln.setFont(font)
            button_exp = QPushButton("e^x", self)
            button_exp.setFont(font)
            button_fac = QPushButton("n!", self)
            button_fac.setFont(font)
            button_abs = QPushButton("|x|", self)
            button_abs.setFont(font)
            button_mod = QPushButton("mod", self)
            button_mod.setFont(font)

            second_line = [button_ln, button_exp, button_fac, button_abs, button_mod]

            # Third line:
            button_log = QPushButton("log", self)
            button_log.setFont(font)
            button_measurable = QPushButton("1/x", self)
            button_measurable.setFont(font)
            button_squared = QPushButton("x**2", self)
            button_squared.setFont(font)
            button_sq_root = QPushButton("sqrt(x)", self)
            button_sq_root.setFont(font)
            button_div = QPushButton("/", self)
            button_div.setFont(font)

            third_line = [button_log, button_measurable, button_squared, button_sq_root, button_div]

            # Forth line:
            button_x_y = QPushButton("x^y", self)
            button_x_y.setFont(font)
            button_7 = QPushButton("7", self)
            button_7.setFont(font)
            button_8 = QPushButton("8", self)
            button_8.setFont(font)
            button_9 = QPushButton("9", self)
            button_9.setFont(font)
            button_x = QPushButton("x", self)
            button_x.setFont(font)

            forth_line = [button_x_y, button_7, button_8, button_9, button_x]

            # Fifth line:
            button_x_sqrt_y = QPushButton("x_sqrt(y)", self)
            button_x_sqrt_y.setFont(font)
            button_4 = QPushButton("4", self)
            button_4.setFont(font)
            button_5 = QPushButton("5", self)
            button_5.setFont(font)
            button_6 = QPushButton("6", self)
            button_6.setFont(font)
            button_minus = QPushButton("-", self)
            button_minus.setFont(font)

            fifth_line = [button_x_sqrt_y, button_4, button_5, button_6, button_minus]

            # Sixth line:
            button_10x = QPushButton("10^x", self)
            button_10x.setFont(font)
            button_1 = QPushButton("1", self)
            button_1.setFont(font)
            button_2 = QPushButton("2", self)
            button_2.setFont(font)
            button_3 = QPushButton("3", self)
            button_3.setFont(font)
            button_plus = QPushButton("+", self)
            button_plus.setFont(font)

            sixth_line = [button_10x, button_1, button_2, button_3, button_plus]

            # Seventh line:
            button_logy_x = QPushButton("logy(x)", self)
            button_logy_x.setFont(font)
            button_plus_minus = QPushButton("+/-", self)
            button_plus_minus.setFont(font)
            button_0 = QPushButton("0", self)
            button_0.setFont(font)
            button_dot = QPushButton(".", self)
            button_dot.setFont(font)
            button_eq = QPushButton("=", self)
            button_eq.setFont(font)

            seventh_line = [button_logy_x, button_plus_minus, button_0, button_dot, button_eq]

            # Getting all buttons:
            buttons = first_line + second_line + third_line + forth_line + fifth_line + sixth_line + seventh_line

            # Connecting buttons to operations manager and adding shortcuts:
            for button in buttons:
                button.clicked.connect(self.__manage_clicks)
                if button.text() in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
                                     "+", "-", "=", "/", "x", "<-", "C", "."]:
                    if button.text() == "x":
                        button.setShortcut("*")
                    elif button.text() == "<-":
                        button.setShortcut(Qt.Key.Key_Backspace)
                    elif button.text() == "=":
                        button.setShortcut(Qt.Key.Key_Return)
                    elif button.text() == "C":
                        button.setShortcut(Qt.Key.Key_Delete)
                    else:
                        button.setShortcut(button.text())
            # Gathering all lines and lines layouts:
            all_lines = [first_line, second_line, third_line, forth_line, fifth_line, sixth_line, seventh_line]
            all_layouts = [buttons_layout1, buttons_layout2, buttons_layout3, buttons_layout4, buttons_layout5,
                           buttons_layout6, buttons_layout7]

            for i in range(len(all_lines)):
                for j in range(5):
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
            sample_button.triggered.connect(self.__sample_button_click)

            # Plot calc button:
            plot_calc_button = QAction("&Draw plot", self)
            plot_calc_button.setStatusTip("Open plot calc")
            plot_calc_button.triggered.connect(self.__draw_plot_window)

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
                rounding_to = MAX_DIGITS - idx_dot_point - 1

                return round(num, rounding_to)
            # if we have str - e format value:
            idx_dot_point = num.index(".")

            # Rounding to max possible digits including e format length:
            rounding_to = MAX_DIGITS - idx_dot_point - 1 - len(e)

            return str(round(float(num), rounding_to))

        # Helper function which rounds if there are too many digits in display after adding minus:
        def terminate_too_many_digits(num: int) -> int:
            rounding_to = MAX_DIGITS
            return round(num, rounding_to)

        # Helper function which changes number to string e notation:
        def change_format_for_large_nums(num: Union[int, float]) -> str:
            return "{:e}".format(num)

        # Helper function to get e format:
        def get_e_format(num: Union[int, float]) -> str:
            e_format = ""

            # Fixing overflow after evaluation:
            if len(str(num)) >= MAX_DIGITS:

                # Block too small e:
                if 1e-8 < num < 1e11:
                    return ""

                e_format = change_format_for_large_nums(num)

                # if we take too much display space with e format:
                if len(e_format) >= MAX_DIGITS:
                    # We get the position of e - beginning of our format:
                    e_ind = e_format.index("e")

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
            if isinstance(value, float) and len(str(value)) >= MAX_DIGITS:
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

        # Helper function to handle overflow error:
        def handle_overflow_err() -> None:
            self.__operations_field.setText("")
            self.__display_field.setText("INF")
            self.__str_val = ""
            self.__str_val_operations = ""

        # Helper function managing unary functions on buttons:
        def manage_unary_operators(button_name: str) -> None:
            operation = None
            if button_name == "1/x":
                operation = lambda x: 1 / x
            elif button_name == "x**2":
                operation = lambda x: x ** 2
            elif button_name == "sqrt(x)":
                operation = lambda x: math.sqrt(x)
            elif button_name == "|x|":
                operation = lambda x: abs(x)
            elif button_name == "n!":
                operation = lambda x: math.gamma(x + 1)
            elif button_name == "e^x":
                operation = lambda x: math.exp(x)
            elif button_name == "ln":
                operation = lambda x: math.log(x)
            elif button_name == "log":
                operation = lambda x: math.log10(x)
            elif button_name == "10^x":
                operation = lambda x: 10 ** x

            # We have entered digits but have yet to perform any operation:
            if self.__str_val != "" and self.__str_val_operations == "":
                # Check for solo dot point:
                manage_solo_dot()
                # We do not need to eval str_val:
                val = 0
                # We don't have a dot point:
                if "." not in self.__str_val:
                    val = int(self.__str_val)
                else:
                    val = float(self.__str_val)

                if button_name == "10^x" and float(self.__str_val) > 1e6:
                    handle_overflow_err()
                    return

                val = operation(val)

                # Protecting against unnecessary parsing:
                val = manage_immediate_dot_point_after_eval(val)

                # if we have floating point, get rid of too many digits after dot point:
                if isinstance(val, float) and len(str(val)) >= MAX_DIGITS:
                    val = terminate_too_many_digits_after_dot(val)

                # We'll keep the e format information in case there is one:
                e_format = get_e_format(val)

                # If we erased display, we don't change its view:
                if self.__display_field.text() != "":
                    # Update str_val in order to place it on display:
                    self.__str_val = str(val)
                else:
                    self.__str_val = ""

                # But if we have e_format we enter it on display:
                if e_format != "":
                    self.__display_field.setText(e_format)
                # Else - we enter the same value as in str_val:
                else:
                    self.__display_field.setText(self.__str_val)

                # We keep evaluated value in str_val_operations and add new bin_op:
                self.__str_val_operations = str(val)

                # But if we have e_format we enter it on operations display with bin_op:
                if e_format != "":
                    self.__operations_field.setText(e_format)
                # Else - we enter the same value as in str_val_operations:
                else:
                    self.__operations_field.setText(self.__str_val_operations)

                # Keep value reset:
                self.__str_val = ""

            # We performed operations, but we don't have any following operator:
            elif self.__str_val_operations != "" and (self.__str_val_operations[-1] not in ["/", "*", "-", "+", "%"]
                                                      and self.__str_val_operations[-2:] != "**"):
                if button_name == "10^x" and float(self.__str_val_operations) > 1e6:
                    handle_overflow_err()
                    return
                # Evaluate:
                eval_str = eval(self.__str_val_operations)
                eval_str = operation(eval_str)

                # Protecting against unnecessary parsing:
                eval_str = manage_immediate_dot_point_after_eval(eval_str)

                # if we have floating point, get rid of too many digits after dot point:
                if isinstance(eval_str, float) and len(str(eval_str)) >= MAX_DIGITS:
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
            elif self.__str_val_operations != "" and (self.__str_val_operations[-2:] == "**" or
                                                      self.__str_val_operations[-1] in ["/", "*", "-", "+", "%"]):
                # We haven't entered any digits -
                # evaluate 1/x on str_val and perform operation with given op (enter result in str_val):
                if self.__str_val == "":
                    if button_name == "10^x" and float(self.__str_val_operations[:-1]) > 1e6:
                        handle_overflow_err()
                        return
                        # Evaluate - only the number:
                    if self.__str_val_operations[-2:] == "**":
                        eval_str = eval(self.__str_val_operations[:-2])
                    else:
                        eval_str = eval(self.__str_val_operations[:-1])
                    eval_str = operation(eval_str)

                    # Protecting against unnecessary parsing:
                    eval_str = manage_immediate_dot_point_after_eval(eval_str)

                    # if we have floating point, get rid of too many digits after dot point:
                    if isinstance(eval_str, float) and len(str(eval_str)) >= MAX_DIGITS:
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
                    if button_name == "10^x" and float(self.__str_val) > 1e6:
                        handle_overflow_err()
                        return
                    # Check for solo dot point:
                    manage_solo_dot()
                    # Evaluate str_val
                    eval_str = eval(self.__str_val)
                    eval_str = operation(eval_str)

                    # Protection against adding dot point even when it's not necessary:
                    eval_str = manage_immediate_dot_point_after_eval(eval_str)

                    # if we have floating point, get rid of too many digits after dot point:
                    if isinstance(eval_str, float) and len(str(eval_str)) >= MAX_DIGITS:
                        eval_str = terminate_too_many_digits_after_dot(eval_str)

                    # Get e format:
                    e_format = get_e_format(eval_str)

                    # Keep the value:
                    self.__str_val = str(eval_str)

                    if e_format != "":
                        self.__display_field.setText(e_format)
                    else:
                        self.__display_field.setText(self.__str_val)

        # Helper function to manage solely dot appearance before evaluation:
        def manage_solo_dot() -> None:
            if self.__str_val[-1] == ".":
                self.__str_val = self.__str_val[:-1]
                self.__display_field.setText(self.__str_val)

        # Function managing appearing of dot point always after "/" and sqrt(x) even if it's not needed:
        def manage_immediate_dot_point_after_eval(num: Union[int, float]) -> Union[int, float]:
            if isinstance(num, float):
                if int(num) == num:
                    return int(num)
            return num

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
                if self.__str_val_operations != "" and (self.__str_val_operations[-1] in ["/", "*", "-", "+", "%"] or
                                                        self.__str_val_operations[-2:] == "**"):
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
                    self.__str_val = self.__str_val[:-1]
                    # Update display:
                    self.__display_field.setText(self.__str_val)
                    # If we got to plain zero we reset our str_val and start over:
                    if self.__str_val == "0":
                        self.__str_val = ""
        # Evaluating with "=":
        elif sender.text() == "=":
            # If there is an operator in str_val_operations:
            if len(self.__str_val_operations) > 0 and (self.__str_val_operations[-1] in ["/", "*", "-", "+", "%"] or
                                                       self.__str_val_operations[-2:] == "**"):
                # Get binary operator:
                bin_op = self.__str_val_operations[-1]
                if self.__str_val_operations[-2:] == "**":
                    bin_op = "**"
                try:
                    # We have 1 value - perform evaluation on itself:
                    if self.__str_val == "":
                        # We add the same number to our evaluation:
                        if self.__str_val_operations[-2:] == "**":
                            self.__str_val_operations += self.__str_val_operations[:-2]
                        else:
                            self.__str_val_operations += self.__str_val_operations[:-1]
                        eval_str = eval(self.__str_val_operations)

                        if bin_op in ["/", "%", "**"]:
                            # Protection against adding dot point even when it's not necessary:
                            eval_str = manage_immediate_dot_point_after_eval(eval_str)
                        set_displays_after_op_eq(eval_str)
                    # We have 2 values, evaluate regularly:
                    else:
                        # Check for solo dot point:
                        manage_solo_dot()
                        # We str_val number to operation:
                        self.__str_val_operations += self.__str_val
                        eval_str = eval(self.__str_val_operations)
                        if bin_op in ["/", "%", "**"]:
                            # Protection against adding dot point even when it's not necessary:
                            eval_str = manage_immediate_dot_point_after_eval(eval_str)
                        set_displays_after_op_eq(eval_str)

                except ZeroDivisionError:
                    handle_zero_division_err()
                except OverflowError:
                    handle_overflow_err()
            # Else - we simply keep the number (nothing to evaluate on):
            else:
                pass
        # Digits in sender:
        elif sender.text() in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            # Protect against adding a number into display when
            # we have str_val_operations, but we don't have an operator:
            if len(self.__str_val_operations) > 0 and (self.__str_val_operations[-1] not in ["/", "*", "-", "+", "%"] and
                                                       self.__str_val_operations[-2:] != "**"):
                pass
            # Check for max display length - don't allow to add more digits if we don't have more space:
            elif (len(self.__str_val) < MAX_DIGITS) or self.__display_field.text() in \
                    ["ZERO DIVISION", "INVALID INPUT", "INF"]:
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
        elif sender.text() in ["/", "x", "-", "+", "mod", "x^y"]:
            # We get the binary op:
            bin_op = sender.text()
            if sender.text() == "x":
                bin_op = "*"
            elif sender.text() == "mod":
                bin_op = "%"
            elif sender.text() == "x^y":
                bin_op = "**"
            # If there is nothing in operations:
            if len(self.__str_val_operations) == 0:
                # We have something to draw to operations field:
                if len(self.__str_val) > 0:
                    # Check for solo dot point:
                    manage_solo_dot()
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
                    if self.__str_val_operations[-1] in ["/", "*", "-", "+", "%"] or \
                            self.__str_val_operations[-2:] == "**":

                        # We swap binary operators from str_val_operations:
                        if self.__str_val_operations[-2:] == "**":
                            self.__str_val_operations = self.__str_val_operations[:-2] + bin_op
                        else:
                            self.__str_val_operations = self.__str_val_operations[:-1] + bin_op
                        # if there's no e format:
                        if "e" not in self.__operations_field.text():
                            self.__operations_field.setText(self.__str_val_operations)
                        else:
                            # We swap text from operations field:
                            if self.__operations_field.text()[-2:] == "**":
                                self.__operations_field.setText(self.__operations_field.text()[:-2] + bin_op)
                            else:
                                self.__operations_field.setText(self.__operations_field.text()[:-1] + bin_op)
                    # No operator - add it:
                    else:
                        # Trying for 0 division error:
                        try:
                            # Evaluate value in str_val_operations - to check if we need e format:
                            eval_str = eval(self.__str_val_operations)

                            # if we have floating point, get rid of too many digits after dot point:
                            if isinstance(eval_str, float) and len(str(eval_str)) >= MAX_DIGITS:
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
                        except OverflowError:
                            handle_overflow_err()
                # Else - we evaluate (we have 1 operator and str_val):
                else:
                    # Trying for 0 division error:
                    try:
                        # Check for solo dot point:
                        manage_solo_dot()
                        # We get the value from str_val to our operations_val and evaluate:
                        self.__str_val_operations += self.__str_val
                        eval_str = eval(self.__str_val_operations)

                        # Protection against adding dot point even when it's not necessary:
                        eval_str = manage_immediate_dot_point_after_eval(eval_str)

                        # if we have floating point, get rid of too many digits after dot point:
                        if isinstance(eval_str, float) and len(str(eval_str)) >= MAX_DIGITS:
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
                    except OverflowError:
                        handle_overflow_err()
        # Unary operators:
        elif sender.text() in ["1/x", "x**2", "sqrt(x)", "|x|", "n!", "e^x", "ln", "log", "10^x"]:
            # Protect against trying to do operation over string:
            if self.__display_field.text() not in ["ZERO DIVISION", "INVALID INPUT", "INF"]:
                # Trying for zero division and sqrt of negative values:
                try:
                    manage_unary_operators(sender.text())
                except ZeroDivisionError:
                    handle_zero_division_err()
                except ValueError:
                    handle_value_err()
                except OverflowError:
                    handle_overflow_err()
        # +/- in sender:
        elif sender.text() == "+/-":
            # If we entered a value:
            if self.__str_val != "":
                # We change its sign:
                if self.__str_val[0] == "-":
                    self.__str_val = self.__str_val[1:]
                else:
                    self.__str_val = "-" + self.__str_val
                    val = 0
                    dot = ""
                    # If there's no dot:
                    if "." not in self.__str_val:
                        # We get int:
                        val = int(self.__str_val)

                        # If we have too many digits in display, we terminate them:
                        if len(str(val)) > MAX_DIGITS:
                            val = terminate_too_many_digits(val)
                            val //= 10
                    # Else - there's dot:
                    else:
                        # Dot is last, with no following elements:
                        if self.__str_val[-1] == ".":
                            # We get number without dot (int) - store dot in another variable:
                            val = int(self.__str_val[:-1])
                            dot = "."
                        else:
                            # We get float:
                            val = float(self.__str_val)

                            # If we have too many digits in display (excluding dot)
                            if len(str(val)) >= MAX_DIGITS + 1:
                                val = terminate_too_many_digits_after_dot(val)

                    # Set str_val + dot (if there was one):
                    self.__str_val = str(val) + dot
                # Display:
                self.__display_field.setText(self.__str_val)
            # We haven't entered a value:
            else:
                # We have operations value:
                if self.__str_val_operations != "":
                    bin_op = ""
                    e_format = ""
                    # If there's an operator:
                    if self.__str_val_operations[-2:] == "**":
                        bin_op = "**"
                        self.__str_val_operations = self.__str_val_operations[:-2]
                    elif self.__str_val_operations[-1] in ["/", "*", "-", "+", "%"]:
                        # We remember it in bin_op variable, but delete it from str_val_operations:
                        bin_op = self.__str_val_operations[-1]
                        self.__str_val_operations = self.__str_val_operations[:-1]
                    # We change its sign:
                    if self.__str_val_operations[0] == "-":
                        self.__str_val_operations = self.__str_val_operations[1:]
                        if "." not in self.__str_val_operations and "e-" not in self.__str_val_operations:
                            # We get int:
                            val = int(self.__str_val_operations)
                            # If we have too many digits in display, we terminate them:
                            if len(str(val)) >= MAX_DIGITS + 1:
                                val = terminate_too_many_digits(val)

                            # Getting e format:
                            e_format = get_e_format(val)
                        # Else - there's dot:
                        else:
                            # We get float:
                            val = float(self.__str_val_operations)

                            # If we have too many digits in display (excluding dot)
                            if len(str(val)) >= MAX_DIGITS:
                                val = terminate_too_many_digits_after_dot(val)
                            # Getting e format:
                            e_format = get_e_format(val)
                        # Set str_val_operations and add bin_op if there's one:
                        self.__str_val_operations = self.__str_val_operations + bin_op
                    else:
                        self.__str_val_operations = "-" + self.__str_val_operations
                        # If there's no dot:
                        if "." not in self.__str_val_operations and "e-" not in self.__str_val_operations:
                            # We get int:
                            val = int(self.__str_val_operations)

                            # If we have too many digits in display, we terminate them:
                            if len(str(val)) >= MAX_DIGITS + 1:
                                val = terminate_too_many_digits(val)

                            # Getting e format:
                            e_format = get_e_format(val)
                        # Else - there's dot:
                        else:
                            # We get float:
                            val = float(self.__str_val_operations)

                            # If we have too many digits in display (excluding dot)
                            if len(str(val)) >= MAX_DIGITS:
                                val = terminate_too_many_digits_after_dot(val)
                            # Getting e format:
                            e_format = get_e_format(val)
                        # Set str_val_operations and add operator (if there's one):
                        self.__str_val_operations = str(val) + bin_op

                    # We have e format:
                    if e_format != "":
                        self.__display_field.setText(e_format)
                        self.__operations_field.setText(e_format if bin_op == "" else e_format + bin_op)
                    # Else - no e format:
                    else:
                        # Display (set display field without operator if there's one):
                        if bin_op == "":
                            self.__display_field.setText(self.__str_val_operations)
                        else:
                            if bin_op == "**":
                                self.__display_field.setText(self.__str_val_operations[:-2])
                            else:
                                self.__display_field.setText(self.__str_val_operations[:-1])
                        self.__operations_field.setText(self.__str_val_operations)
        # . in sender:
        elif sender.text() == ".":
            # if we entered a value and: there is no dot already, we won't exceed display after adding dot, we don't have e format in display:
            if self.__str_val != "" and "." not in self.__str_val and len(
                    self.__str_val) <= MAX_DIGITS - 2 and "e" not in self.__display_field.text():
                self.__str_val += "."
                self.__display_field.setText(self.__str_val)
        # Pi or e in sender:
        elif sender.text() in ["π", "e"]:
            val = math.e
            if sender.text() == "π":
                val = math.pi
            val = terminate_too_many_digits_after_dot(val)
            if self.__str_val_operations == "" or (
                    self.__str_val_operations != "" and (self.__str_val_operations[-1] in ["/", "*", "-", "+", "%"] or
                                                         self.__str_val_operations[-2:] == "**")):
                self.__str_val = str(val)
                self.__display_field.setText(self.__str_val)
            elif self.__str_val_operations != "" and (self.__str_val_operations[-1] not in ["/", "x", "-", "+", "%"] and
                                                      self.__str_val_operations[-2:] != "**"):
                self.__str_val_operations = str(val)
                self.__display_field.setText(self.__str_val_operations)
                self.__operations_field.setText(self.__str_val_operations)

    def __draw_plot_window(self):
        self.plot_window = PlotWindow(self)
        self.plot_window.show()
        self.hide()
        print('Plotter opened')

    def __sample_button_click(self, s):
        print('button clicked')

    def quit_app(self):
        QApplication.instance().quit

    # Method for centering windows
    def __center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


# Running main program:
def run() -> None:
    calc_app = QApplication(sys.argv)
    main_w = CalcMainWindow()
    main_w.show()
    sys.exit(calc_app.exec())
