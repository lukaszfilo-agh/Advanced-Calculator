import sympy as sp
import numpy as np
import re
import warnings
from integ_help_window import IntegralsHelpWindow
from typing import Union, List
from scipy.integrate import quad, IntegrationWarning
from sympy.calculus.singularities import singularities
from sympy.calculus.util import continuous_domain
from sympy import Interval
from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QMessageBox
)

warnings.filterwarnings("error")


class IntegralsWindow(QDialog):
    # Class for input dialog
    def __init__(self, main_window) -> None:
        super().__init__()

        # Initializing parent:
        self.parent = main_window

        # Calling function to initialize UI
        self.init_ui()

    def init_ui(self) -> None:
        # Setting window title
        self.setWindowTitle('Integrals window')
        # Setting window size
        self.resize(500, 500)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Input fields list:
        self.input_fields = [
            CustomLineEdit(),  # Function input
            CustomLineEdit(),  # Lower limit input
            CustomLineEdit()  # Upper limit input
        ]

        # Input fields labels:
        labels_text = ['f(x):', 'Lower limit:', 'Upper limit:']
        self.input_fields[0].installEventFilter(self)
        self.input_fields[1].installEventFilter(self)
        self.input_fields[2].installEventFilter(self)

        self.input_fields[0].mousePressEvent = lambda e: self.__switch_func_keyboard()
        self.input_fields[1].mousePressEvent = lambda e: self.__switch_lower_lim_keyboard()
        self.input_fields[2].mousePressEvent = lambda e: self.__switch_upper_lim_keyboard()

        for i in range(len(self.input_fields)):
            label = QLabel(labels_text[i])
            main_layout.addWidget(label)
            main_layout.addWidget(self.input_fields[i])

        # Layout for keyboard buttons:
        self.buttons_layout = QVBoxLayout()
        main_layout.addLayout(self.buttons_layout)

        # Creating keyboards:
        self.keyboards = [
            [  # Keyboard for function:
                ['*', '/', 'sin', 'cos'],
                ['+', '-', 'tg', 'ctg'],
                ['.', '^', 'arcsin', 'arccos'],
                ['(', ')', 'arctg', 'log'],
                ['π', 'e', '| |', 'sqrt'],
                ['x', ' ', '<-', 'C']
            ],
            [  # Keyboard for lower limit:
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', '∞'],
                ['+', '-', '<-', 'C']
            ],
            [  # Keyboard for upper limit:
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', '∞'],
                ['+', '-', '<-', 'C']
            ]
        ]

        # Button for calculating:
        button_calculate = QPushButton('Calculate')
        button_calculate.clicked.connect(self.__calc)
        button_calculate.setShortcut(Qt.Key.Key_Return)

        main_layout.addWidget(button_calculate)

        # Button for returning to main window:
        back_button = QPushButton('Back to main window')
        back_button.clicked.connect(self.__back_to_menu)

        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Button for help window:
        help_button = QPushButton('Help')
        help_button.clicked.connect(self.__help_window)

        main_layout.addWidget(help_button, alignment=Qt.AlignmentFlag.AlignRight)

        # Setting main_layout as dialog layout:
        self.setLayout(main_layout)

        self.active_field = 0
        self.__update_keyboard()

    # Managing moving through input fields:
    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj in self.input_fields:
            if event.key() == Qt.Key.Key_Tab:
                active_index = self.input_fields.index(obj)
                if active_index == 2:
                    self.active_field = 0
                else:
                    self.active_field = active_index + 1
            self.__update_keyboard()
        return super().eventFilter(obj, event)

    def __switch_func_keyboard(self) -> None:
        self.active_field = 0
        self.__update_keyboard()

    def __switch_lower_lim_keyboard(self) -> None:
        self.active_field = 1
        self.__update_keyboard()

    def __switch_upper_lim_keyboard(self) -> None:
        self.active_field = 2
        self.__update_keyboard()

    def __on_button_clicked(self) -> None:
        clicked_button = self.sender()
        text = clicked_button.text()

        if text == 'C':
            self.input_fields[self.active_field].clear()
        elif text == '<-':
            current_text = self.input_fields[self.active_field].text()
            new_text = current_text[:-1]
            self.input_fields[self.active_field].setText(new_text)
        elif text == ' ':
            pass
        else:
            current_text = self.input_fields[self.active_field].text()
            new_text = current_text + text
            self.input_fields[self.active_field].setText(new_text)

    def __update_keyboard(self) -> None:
        # Deleting buttons
        for i in reversed(range(self.buttons_layout.count())):
            layout = self.buttons_layout.itemAt(i).layout()
            if layout is not None:
                for j in reversed(range(layout.count())):
                    layout.itemAt(j).widget().deleteLater()
                self.buttons_layout.removeItem(layout)

        # Adding buttons
        for row in self.keyboards[self.active_field]:
            row_layout = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text)
                button.setFixedSize(100, 40)
                button.clicked.connect(self.__on_button_clicked)
                row_layout.addWidget(button)
            self.buttons_layout.addLayout(row_layout)

    # Function for going back to main menu
    def __back_to_menu(self) -> None:
        self.close()
        self.parent.show()

    # Function for displaying help window:
    def __help_window(self) -> None:
        self.__help_window = IntegralsHelpWindow()
        self.__help_window.show()

    # Getting inputs to calculate:
    def __calc(self) -> None:
        function_str, lim1, lim2 = tuple(input.text() for input in self.input_fields)

        try:
            if len(function_str) == 0:
                raise EmptyInputError

            # Checking for illegal charaters in function str
            invalid_chars = func_bad_chars(function_str)
            if len(invalid_chars) != 0:
                raise InvalidCharacters(function_str)

            # Creating expression for eval:
            function_math = convert_func_math(function_str)

            # Checking for illegal charaters in lim str
            lim1_invalid_chars = lim_bad_chars(lim1)
            lim2_invalid_chars = lim_bad_chars(lim2)

            if len(lim1_invalid_chars) != 0 or len(lim2_invalid_chars) != 0:
                raise LimError(lim1, lim2, 0)

            # If both lim are empty then we move to indefinite integrals:
            if lim1 == "" and lim2 == "":
                self.__calc_indefinite_integrals(function_math)

            # Else - definite integrals:
            else:
                # Check for missing input:
                if (lim1 == "" and lim2 != "") or (lim2 == "" and lim1 != ""):
                    raise EmptyInputError

                # Checking for illegal characters in function str:
                invalid_chars = func_bad_chars(function_str)
                if len(invalid_chars) != 0:
                    raise InvalidCharacters(function_str)

                # Checking for illegal characters in lim str:
                lim1_invalid_chars = lim_bad_chars(lim1)
                lim2_invalid_chars = lim_bad_chars(lim2)

                if len(lim1_invalid_chars) != 0 or len(lim2_invalid_chars) != 0:
                    raise LimError(lim1, lim2, 0)

                # Converting lim to math expressions:
                lim1 = convert_lim_math(lim1)
                lim2 = convert_lim_math(lim2)

                # Evaluating lim:
                lim1 = eval(lim1)
                lim2 = eval(lim2)

                self.__calc_definite_integrals(function_math, lim1, lim2)
        except EmptyInputError:
            return
        except InvalidCharacters:
            return
        except LimError:
            return

    # Calculating indefinite integrals:
    def __calc_indefinite_integrals(self, func: str) -> None:
        try:
            # Symbolic variable:
            x = sp.symbols('x', real=True)

            # Evaluating function:
            func_math = eval(func)

            # Getting result for display:
            res = str(sp.simplify(sp.integrate(func_math, x))) + " + C"

            # No result in elementary function:
            if res[0] in ["⌠", "I"]:
                message_box = QMessageBox()
                message_box.setWindowTitle("NOT ABLE TO SOLVE")
                message_box.setText("Not able to find primary funtion.")
                message_box.exec()
                print(res)
            else:
                # Substituting representation so that functions match keyboard names:
                res = substitute_sympy_representation(res)
                message_box = QMessageBox()
                message_box.setWindowTitle("SOLUTION")
                message_box.setText(f"Primary function to your integral:\n\n{res}")
                message_box.exec()
        # Catch zero division error:
        except ZeroDivisionError:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(f"Division by zero!!!")
            message_box.exec()
            # Clearing the input:
            for line_edit in self.input_fields:
                line_edit.setText("")
        # Catching all other exceptions
        except Exception as e:
            print('different exception')
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(
                f"ERROR \n f(x) = {re.sub('sp.','', func)} \n {func}")
            message_box.exec()
            print(print(e))

            # Clearing the input:
            for line_edit in self.input_fields:
                line_edit.setText("")

    # Calcualting definite integrals:
    def __calc_definite_integrals(self, func: str, lim1: Union[float, int], lim2: Union[float, int]) -> None:
        try:

            res = 0 # If lims are equal - we do not need to evaluate.
            # We need to evaluate:
            if lim1 != lim2:
                # Creating lambda function:
                def f(x): return eval(func)

                # We have symmetry in lim:
                if lim1 == -lim2:
                    # Symbolic variable:
                    x = sp.symbols('x', real=True)

                    # Evaluating function using sympy:
                    func_sympy = eval(func)

                    # Check if function is odd:
                    if func_sympy == -func_sympy.subs(x, -x):
                        # We keep 0 as a result
                        pass
                    # Check if function is even:
                    elif func_sympy == func_sympy.subs(x, -x):
                        # Choose larger lim - we can now calculate our integral as
                        # 2 * I(0, lim) instead of I(lim1, lim2):
                        lim = lim2 if lim2 > lim1 else lim1

                        # Remember the sign for changed limits:
                        sign = 1
                        if lim2 < lim1:
                            sign *= -1

                        # Find function singularities:
                        sing = singularities(func_sympy, x)

                        # Getting domain of our function:
                        domain = continuous_domain(func_sympy, x, sp.Reals)

                        # If we have singularities or integral interval is not in function continuous domain:
                        if sing or not domain.intersect(Interval(0, lim2)) == Interval(0, lim2):
                            # Try using sympy.integrate:
                            res = str(2 * sign * sp.integrate(func_sympy, (x, 0, lim)))

                            # No result found:
                            if res[0] in ["⌠", "I"]:
                                message_box = QMessageBox()
                                message_box.setWindowTitle("NOT ABLE TO SOLVE")
                                message_box.setText("Not able to find solution")
                                message_box.exec()
                                return
                            else:
                                # Substituting representation so that functions match keyboard names:
                                res = substitute_sympy_representation(res)
                        # Else - use scipy:
                        else:
                            res, _ = quad(f, 0, lim2)
                            res *= 2 * sign
                    else:
                        # Symbolic variable:
                        x = sp.symbols('x', real=True)

                        # Evaluating function using sympy:
                        func_sympy = eval(func)

                        # Getting domain of our function:
                        domain = continuous_domain(func_sympy, x, sp.Reals)

                        # Integral interval is in function continous domain - we may use scipy (no complex):
                        if domain.intersect(Interval(lim1, lim2)) == Interval(lim1, lim2):
                            # Calculating numerically:
                            res, _ = quad(f, lim1, lim2)

                        # Use sympy to calculate result - complex solution:
                        else:
                            res = str(sp.integrate(func_sympy, (x, lim1, lim2)))

                            # No result found:
                            if res[0] in ["⌠", "I"]:
                                message_box = QMessageBox()
                                message_box.setWindowTitle("NOT ABLE TO SOLVE")
                                message_box.setText("Not able to find solution")
                                message_box.exec()
                                return
                            else:
                                # Substituting representation so that functions match keyboard names:
                                res = substitute_sympy_representation(res)
                else:
                    # Symbolic variable:
                    x = sp.symbols('x', real=True)

                    # Evaluating function using sympy:
                    func_sympy = eval(func)

                    # Get function continuous domain:
                    domain = continuous_domain(func_sympy, x, sp.Reals)

                    # Integral interval is in function continous domain - we may use scipy (no complex):
                    if domain.intersect(Interval(lim1, lim2)) == Interval(lim1, lim2):
                        # Calculating numerically:
                        res, _ = quad(f, lim1, lim2)

                    # Use sympy to calculate result - complex solution:
                    else:
                        res = str(sp.integrate(func_sympy, (x, lim1, lim2)))

                        # No result found:
                        if res[0] in ["⌠", "I"]:
                            message_box = QMessageBox()
                            message_box.setWindowTitle("NOT ABLE TO SOLVE")
                            message_box.setText("Not able to find solution")
                            message_box.exec()
                            return
                        else:
                            # Substituting representation so that functions match keyboard names:
                            res = substitute_sympy_representation(res)
            if res == "nan" or res == sp.nan:
                message_box = QMessageBox()
                message_box.setWindowTitle("NOT ABLE TO SOLVE")
                message_box.setText("Not able to find solution")
                message_box.exec()
                return
            message_box = QMessageBox()
            message_box.setWindowTitle("SOLUTION")
            message_box.setText(f"Integral of your function:\n{res}")
            message_box.exec()
        except ZeroDivisionError:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(f"Division by zero!!!")
            message_box.exec()
        except IntegrationWarning:
            message_box = QMessageBox()
            message_box.setWindowTitle("SOLUTION")
            message_box.setText(f"Integral is not divergent")
            message_box.exec()
        except ValueError:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(f"Domain error")
            message_box.exec()
        except TypeError:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(f"Complex domain results are not supported.")
            message_box.exec()
        except Exception as e:
            print('different exception')
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(f"ERROR \n f(x) = {re.sub('sp.', '', func)} \n")
            message_box.exec()
            print(e)

            # Clearing the input:
            for line_edit in self.input_fields:
                line_edit.setText("")


# Class for custom line edit with keyboard filtering
class CustomLineEdit(QLineEdit):
    def __init__(self) -> None:
        super().__init__()

    def keyPressEvent(self, event) -> None:
        allowed_keys = [Qt.Key.Key_Backspace,
                        Qt.Key.Key_Left,
                        Qt.Key.Key_Right,
                        Qt.Key.Key_X,
                        Qt.Key.Key_Minus,
                        Qt.Key.Key_Plus,
                        Qt.Key.Key_Period,
                        Qt.Key.Key_Asterisk,
                        Qt.Key.Key_E,
                        47,  # '/'
                        94,  # '^'
                        40,  # '('
                        41,  # ')'
                        124  # '|'
                        ]
        print(event.key())
        if event.text().isdigit() or event.key() in allowed_keys:
            super().keyPressEvent(event)


class EmptyInputError(Exception):
    "Raised when data input is NULL"

    def __init__(self) -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        message_box.setText(f"Input cannot be empty.")
        message_box.exec()


class InvalidCharacters(Exception):
    "Raised when the input can't be evaluated"

    def __init__(self, str) -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        message_box.setText(f"You have entered invalid input: {str}.")
        message_box.exec()


class LimError(Exception):
    "Raised when limit error is detected"

    def __init__(self, lim1, lim2, flag) -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        if flag == 0:
            message_box.setText(f"Limit error. {lim1}, {lim2}")
        elif flag == 1:
            message_box.setText(f"Lower limit is greater than upper limit.")
        message_box.exec()


# Helper function to substitute sympy functions representations for keyboard ones:
def substitute_sympy_representation(sympy_repr: str) -> str:
    # Creating variables for easier function names substitutions:
    funcs_to_subs = ["exp", "asin", "acos", "atan", "tan"]
    subs = ["e^", "arcsin", "arccos", "arctg", "tg"]
    match_funcs_to_subs = {func: sub for func, sub in zip(funcs_to_subs, subs)}

    # Iterating through all possible function occurences:
    for func in funcs_to_subs:
        if func in sympy_repr:
            sub = match_funcs_to_subs[func]
            # Regular expression to swap func() to according sub:
            regex = re.compile(fr'{func}\(([^)]+)\)')

            # Helper function to substitute:
            def sub_with_brackets(match) -> str:
                brackets = match.group(1)
                return f'{sub}({brackets})'

            # Substitution:
            sympy_repr = regex.sub(sub_with_brackets, sympy_repr)

    # Creating variables for easier symbols substitutions:
    symbols_to_sub = ["pi", "E", "**"]
    subs = ["π", "e", "^"]
    match_symbols_to_subs = {symbol: sub for symbol, sub in zip(symbols_to_sub, subs)}
    for symbol in symbols_to_sub:
        if symbol in sympy_repr:
            sub = match_symbols_to_subs[symbol]
            sympy_repr = sympy_repr.replace(symbol, sub)
    return sympy_repr


def func_bad_chars(expression: str) -> List[str]:
    result = re.findall(
        r'(?!(?:sin|arcsin|cos|arccos|tg|arctg|ctg|arctg|sqrt|log|e\^|\d+|[\(\)\+\-\*\/\^]|\dx|x|π))\b\S+\b', expression)
    return result


def lim_bad_chars(expression: str) -> List[str]:
    result = re.findall(r'[^0-9eπ∞.\-]', expression)
    return result


def convert_lim_math(expression: str) -> str:

    # Change 'lx' to 'l*x'
    expression = re.sub(r'(\w)(x)', r'\1*\2', expression)

    # Change 'π' to '*π'
    expression = re.sub(r'(\d)(π)', r'\1*\2', expression)

    # Change 'e' to '*e'
    expression = re.sub(r'(\d)(e)', r'\1*\2', expression)

    # Change 'π' to 'np.pi'
    expression = re.sub(r'π', 'np.pi', expression)

    # Change 'e' to 'sp.e'
    expression = re.sub(r'e', 'np.e', expression)

    # Change '∞' to 'inf'
    expression = re.sub(r'∞', 'np.inf', expression)

    # Change '\w np.' to '\w*sp.'
    expression = re.sub(r'(\w)(np)', r'\1*\2', expression)

    return expression


def convert_func_math(expression: str) -> str:

    # Change 'e^x' to 'sp.exp(x)'
    expression = re.sub(r'e\^(.*)', r'sp.exp(\1)', expression)

    # Change '||' to 'sp.Abs(x):
    expression = re.sub(r'\|(.*)\|', r'sp.Abs(\1)', expression)

    # Change 2l to 2*l:
    expression = re.sub(r'(\d)(\w)', r'\1*\2', expression)

    # Change xl to x*l
    expression = re.sub(r'(x)(\w)', r'\1*\2', expression)

    # Change 'sqrt()' to sp.sqrt():
    expression = re.sub(r'\bsqrt\b', 'sp.sqrt', expression)

    # Change 'log()' to 'sp.log()':
    expression = re.sub(r'\blog\b', 'sp.log', expression)

    # Change 'sin' to 'sp.sin'
    expression = re.sub(r'\bsin\b', 'sp.sin', expression)

    # Change 'arcsin' to 'sp.arcsin'
    expression = re.sub(r'\barcsin\b', 'sp.asin', expression)

    # Change 'cos' to 'sp.cos'
    expression = re.sub(r'\bcos\b', 'sp.cos', expression)

    # Change 'arccos' to 'sp.arccos'
    expression = re.sub(r'\barccos\b', 'sp.acos', expression)

    # Change 'tg' to 'sp.tan'
    expression = re.sub(r'\btg\b', 'sp.tan', expression)

    # Change 'arctg' to 'sp.arctan'
    expression = re.sub(r'\barctg\b', 'sp.atan', expression)

    # Change 'ctg' to '1/sp.tan'
    expression = re.sub(r'\bctg\b', '1/sp.tan', expression)

    # Change 'x' to '*x'
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)

    # Change 'lx' to 'l*x'
    expression = re.sub(r'(\w)(x)', r'\1*\2', expression)

    # Change '^' to '**'
    expression = expression.replace('^', '**')

    # Change ')(' to ')*('
    expression = expression.replace(')(', ')*(')

    # Adding multiplication sign in 'x(' or ')x'
    expression = re.sub(r'([1-9x])(\()', r'\1*\2', expression)
    expression = re.sub(r'(\))([1-9x])', r'\1*\2', expression)

    # Change 'π' to 'sp.pi'
    expression = re.sub(r'π', 'sp.pi', expression)

    # Change 'e' to 'sp.E'
    expression = re.sub(r'e', 'sp.E', expression)

    # Change '\d sp.' to '\d*sp.'
    expression = re.sub(r'(\d)(sp)', r'\1*\2', expression)

    # Change '\w np.' to '\w*sp.'
    expression = re.sub(r'(\w)(sp)', r'\1*\2', expression)

    # Change 'xsp' to 'x * sp'
    expression = re.sub(r'(x)(sp)', r'\1*\2', expression)

    return expression