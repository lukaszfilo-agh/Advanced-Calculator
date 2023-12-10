from typing import Union
import scipy as sp

from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialog,
    QLineEdit,
    QMessageBox
)

from PyQt6.QtCore import Qt, QEvent

import re


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

        # Input fields list
        self.input_fields = [
            CustomLineEdit(),  # Function input
            CustomLineEdit(),  # Lower limit input
            CustomLineEdit()  # Upper limit input
        ]

        # Input fields labels
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

        # Layout for keyboard buttons
        self.buttons_layout = QVBoxLayout()
        main_layout.addLayout(self.buttons_layout)

        # Creating keyboards
        self.keyboards = [
            [  # Keyboard for function
                ['*', '/', 'sin()', 'cos()'],
                ['+', '-', 'tg()', 'ctg()'],
                ['.', '^', 'arcsin()', 'arccos()'],
                ['(', ')', 'arctg()', ' '],
                ['π', 'e', '| |', 'sqrt()'],
                ['x', ' ', '<-', 'C']
            ],
            [  # Keyboard for lower limit
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', '∞'],
                ['+', '-', '<-', 'C']
            ],
            [  # Keyboard for upper limit
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', '∞'],
                ['+', '-', '<-', 'C']
            ]
        ]

        # Button for drawing plot
        button_calculate = QPushButton('Calculate')
        button_calculate.clicked.connect(self.accept)
        button_calculate.setShortcut(Qt.Key.Key_Return)

        main_layout.addWidget(button_calculate)

        # Button for returning to main window:
        back_button = QPushButton('Back to main window')
        back_button.clicked.connect(self.__back_to_menu)

        main_layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Setting main_layout as dialog layout
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

    # Getting inputs:
    def __get_inputs(self) -> tuple[None, None, None, None]:
        function_str, lim1, lim2 = tuple(input.text() for input in self.input_fields)

        try:
            if len(function_str) == 0:
                raise EmptyInputError

            # Creating expression for eval:
            function_math = convert_func_math(function_str)

            # If only 1 lim is empty we fill it with inf:
            if lim1 == "" and lim2 != "":
                lim1 = "inf"
            elif lim2 == "" and lim1 != "":
                lim2 = "inf"

            # If both lim are empty then we move to indefinite integrals:
            if lim1 == "" and lim2 == "":
                self.__calc_indefinite_integrals(function_math)
            # Else - definite integrals:
            else:
                # Checking for illegal characters in function str:
                invalid_chars = func_bad_chars(function_str)
                if len(invalid_chars) != 0:
                    raise InvalidCharacters(function_str)

                # Checking for illegal characters in lim str:
                lim1_invalid_chars = lim_bad_chars(lim1)
                lim2_invalid_chars = lim_bad_chars(lim2)

                if len(lim1_invalid_chars) != 0 or len(lim2_invalid_chars) != 0:
                    raise LimError(lim1, lim2, 0)

                lim1 = convert_lim_math(lim1)
                lim2 = convert_lim_math(lim2)

                # Evaluating lim1 and lim2:
                if lim1 in ["inf", "-inf"]:
                    lim1 = float(lim1)
                else:
                    lim1 = eval(lim1)

                if lim2 in ["inf", "-inf"]:
                    lim2 = float(lim2)
                else:
                    lim2 = eval(lim2)

                self.__calc_definite_integrals(function_math, lim1, lim2)

        # Catching errors for empty data
        except EmptyInputError:
            return None, None, None, None

        # Catching errors for invalid chars
        except InvalidCharacters:
            return None, None, None, None

        # Catching errors for LimErrors
        except LimError:
            return None, None, None, None

    # Calculating indefinite integrals:
    def __calc_indefinite_integrals(self, func: str) -> None:
        pass

    # Calcualting definite integrals:
    def __calc_definite_integrals(self, func: str, lim1: Union[float, int], lim2: Union[float, int]) -> None:
        pass


# Class for custom line edit with keyboard filtering
class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        allowed_keys = [Qt.Key.Key_Backspace,
                        Qt.Key.Key_Left,
                        Qt.Key.Key_Right,
                        Qt.Key.Key_X,
                        Qt.Key.Key_Minus,
                        Qt.Key.Key_Plus,
                        47,  # '/'
                        94,  # '^'
                        40,  # '('
                        41  # ')'
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
        print("Input empty")
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")


class InvalidCharacters(Exception):
    "Raised when the input can't be evaluated"

    def __init__(self, str) -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        message_box.setText(f"You have entered invalid input: {str}.")
        print("Invalid chars")
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")


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
        print("Error limits")
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")


def func_bad_chars(expression: str) -> str:
    result = re.findall(
        r'(?!(?:sin|arcsin|cos|arccos|tg|arctg|ctg|arctg|sqrt|e\^|\d+|[\(\)\+\-\*\/\^]|\dx|x))\b\S+\b', expression)
    return result


def lim_bad_chars(expression: str) -> str:
    result = re.findall(r'[^0-9eπ∞\-]', expression)
    return result


def convert_lim_math(expression: str) -> str:
    # Change 'π' to '*π'
    expression = re.sub(r'(\d)(π)', r'\1*\2', expression)

    # Change 'e' to '*e'
    expression = re.sub(r'(\d)(e)', r'\1*\2', expression)

    # Change 'π' to 'np.pi'
    expression = re.sub(r'\bπ\b', 'np.pi', expression)

    # Change 'e' to 'np.e'
    expression = re.sub(r'\be\b', 'np.e', expression)

    # Change '∞' to 'inf'
    expression = re.sub(r'\b∞\b', 'inf', expression)

    # Change '-∞' to 'inf'
    expression = re.sub(r'\b-∞\b', '-inf', expression)

    return expression


def convert_func_math(expression: str) -> str:
    # Change 'e^x' to 'np.exp(x)'
    expression = re.sub(r'e\^(.*)', r'np.exp(\1)', expression)

    # Change 'e^x' to 'np.exp(x)'
    expression = re.sub(r'\|(.*)\|', r'np.abs(\1)', expression)

    # Change 'sqrt()' to np.sqrt()
    expression = re.sub(r'sqrt\b', 'np.sqrt', expression)

    # Change 'sin' to 'np.sin'
    expression = re.sub(r'sin\b', 'np.sin', expression)

    # Change 'arcsin' to 'np.arcsin'
    expression = re.sub(r'arcsin\b', 'np.arcsin', expression)

    # Change 'cos' to 'np.cos'
    expression = re.sub(r'cos\b', 'np.cos', expression)

    # Change 'arccos' to 'np.arccos'
    expression = re.sub(r'arccos\b', 'np.arccos', expression)

    # Change 'tg' to 'np.tan'
    expression = re.sub(r'tg\b', 'np.tan', expression)

    # Change 'arctg' to 'np.arctan'
    expression = re.sub(r'arctg\b', 'np.arctan', expression)

    # Change 'ctg' to '1/np.tan'
    expression = re.sub(r'ctg\b', '1/np.tan', expression)

    # Change 'x' to '*x'
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)

    # Change '^' to '**'
    expression = expression.replace('^', '**')

    # Change ')(' to ')*('
    expression = expression.replace(')(', ')*(')

    # Adding multiplication sing in 'x(' or ')x'
    expression = re.sub(r'([1-9x])(\()', r'\1*\2', expression)
    expression = re.sub(r'(\))([1-9x])', r'\1*\2', expression)

    # Change '\d np.' to '\d*np.'
    expression = re.sub(r'(\d)(np)', r'\1*\2', expression)

    return expression