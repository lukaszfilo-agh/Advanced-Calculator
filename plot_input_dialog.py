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

import matplotlib
matplotlib.use('QtAgg')

import re

import numpy as np

class PlotInputDialog(QDialog):
    # Class for input dialog
    def __init__(self):
        super().__init__()
        # Calling function to initialize UI
        self.init_ui()

    def init_ui(self):
        # Setting window title
        self.setWindowTitle('Enter Data')
        # Setting window size
        self.resize(500, 500)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Input fields list
        self.input_fields = [
            CustomLineEdit(),  # Function input
            CustomLineEdit(),  # Lower limit input
            CustomLineEdit()   # Upper limit input
        ]

        # Input fields labels
        labels_text = ['f(x):', 'Lower limit:', 'Upper limit:']

        self.input_fields[0].installEventFilter(self)
        self.input_fields[1].installEventFilter(self)
        self.input_fields[2].installEventFilter(self)

        self.input_fields[0].mousePressEvent = lambda e: self.switch_func_keyboard()
        self.input_fields[1].mousePressEvent = lambda e: self.switch_lower_lim_keyboard()
        self.input_fields[2].mousePressEvent = lambda e: self.switch_upper_lim_keyboard()

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
                ['*', '/', 'sin', 'cos'],
                ['+', '-', 'tg', 'ctg'],
                ['.', '^', 'arcsin', 'arccos'],
                ['(', ')', 'arctg', 'log'],
                ['π', 'e', '| |', 'sqrt'],
                ['x', ' ', '<-', 'C']
            ],
            [  # Keyboard for lower limit
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', ' '],
                ['+', '-', '<-', 'C']
            ],
            [  # Keyboard for upper limit
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', ' '],
                ['+', '-', '<-', 'C']
            ]
        ]

        # Button for drawing plot
        button_draw_plot = QPushButton('Draw plot')
        button_draw_plot.clicked.connect(self.accept)
        button_draw_plot.setShortcut(Qt.Key.Key_Return)

        main_layout.addWidget(button_draw_plot)

        # Setting main_layout as dialog layout
        self.setLayout(main_layout)

        self.active_field = 0
        self.update_keyboard()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj in self.input_fields:
            if event.key() == Qt.Key.Key_Tab:
                active_index = self.input_fields.index(obj)
                if active_index == 2:
                    self.active_field = 0
                else:
                    self.active_field = active_index + 1
            self.update_keyboard()
        return super().eventFilter(obj, event)

    def switch_func_keyboard(self):
        self.active_field = 0
        self.update_keyboard()

    def switch_lower_lim_keyboard(self):
        self.active_field = 1
        self.update_keyboard()

    def switch_upper_lim_keyboard(self):
        self.active_field = 2
        self.update_keyboard()

    def on_button_clicked(self):
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

    def update_keyboard(self):
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
                button.clicked.connect(self.on_button_clicked)
                row_layout.addWidget(button)
            self.buttons_layout.addLayout(row_layout)

    def getInputs(self):
        function_str, lim1, lim2 = tuple(input.text() for input in self.input_fields)

        try:
            if len(function_str) == 0 or len(lim1) == 0 or len(lim2) == 0:
                    raise EmptyInputError
        
            # Checking for illegal charaters in function str
            invalid_chars = func_bad_chars(function_str)
            if len(invalid_chars) != 0:
                raise InvalidCharacters(function_str)
            
            # Checking for illegal charaters in lim str
            lim1_invalid_chars = lim_bad_chars(lim1)
            lim2_invalid_chars = lim_bad_chars(lim2)

            if len(lim1_invalid_chars) != 0 or len(lim2_invalid_chars) != 0:
                raise LimError(lim1, lim2, 0)
            
            lim1 = convert_lim_math(lim1)
            lim2 = convert_lim_math(lim2)

            # Conversion of lim1 and lim2
            lim1 = eval(lim1)
            lim2 = eval(lim2)

            # Checking for limit error
            if lim1 > lim2:
                raise LimError(lim1, lim2, 1)
            
            # Creating expression for eval
            function_math = convert_func_math(function_str)

        # Catching errors for empty data
        except EmptyInputError:
            return None, None, None, None
        
        # Catching errors for invalid chars
        except InvalidCharacters:
            return None, None, None, None
        
        # Catching errors for LimErrors
        except LimError:
            return None, None, None, None

        except SyntaxError:
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(f"Syntax error.")
            print("Syntax error")
            result = message_box.exec()
            if result == QMessageBox.StandardButton.Ok:
                print("Error closed")
            return None, None, None, None
        
        return function_math, function_str, lim1, lim2

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


def func_bad_chars(expression):
    result = re.findall(
        r'(?!(?:sin|arcsin|cos|arccos|tg|arctg|ctg|arctg|sqrt|log|e\^|\d+|[\(\)\+\-\*\/\^]|\dx|x|π))\b\S+\b', expression)
    return result

def lim_bad_chars(expression):
    result = re.findall(r'[^0-9eπ\-]', expression)
    return result


def convert_lim_math(expression):
    # Change 'π' to '*π'
    expression = re.sub(r'(\d)(π)', r'\1*\2', expression)

    # Change 'e' to '*e'
    expression = re.sub(r'(\d)(e)', r'\1*\2', expression)

    # Change 'π' to 'np.pi'
    expression = re.sub(r'\bπ\b', 'np.pi', expression)

    # Change 'e' to 'np.e'
    expression = re.sub(r'\be\b', 'np.e', expression)

    return expression

def convert_func_math(expression):
    # Change 'e^x' to 'np.exp(x)'
    expression = re.sub(r'e\^(.*)', r'np.exp(\1)', expression)

    # Change '||' to 'np.abs(x)'
    expression = re.sub(r'\|(.*)\|', r'np.abs(\1)', expression)

    # Change 2l to 2*l
    expression = re.sub(r'(\d)(\w)', r'\1*\2', expression)

    # Change xl to x*l
    expression = re.sub(r'(x)(\w)', r'\1*\2', expression)

    # Change 'sqrt()' to np.sqrt()
    expression = re.sub(r'\bsqrt\b', 'np.sqrt', expression)

    # Change 'log()' to 'np.log()'
    expression = re.sub(r'\blog\b', 'np.log', expression)

    # Change 'sin' to 'np.sin'
    expression = re.sub(r'\bsin\b', 'np.sin', expression)

    # Change 'arcsin' to 'np.arcsin'
    expression = re.sub(r'\barcsin\b', 'np.arcsin', expression)

    # Change 'cos' to 'np.cos'
    expression = re.sub(r'\bcos\b', 'np.cos', expression)

    # Change 'arccos' to 'np.arccos'
    expression = re.sub(r'\barccos\b', 'np.arccos', expression)

    # Change 'tg' to 'np.tan'
    expression = re.sub(r'\btg\b', 'np.tan', expression)

    # Change 'arctg' to 'np.arctan'
    expression = re.sub(r'\barctg\b', 'np.arctan', expression)

    # Change 'ctg' to '1/np.tan'
    expression = re.sub(r'\bctg\b', '1/np.tan', expression)

    # Change 'x' to '*x'
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)

    # Change 'lx' to 'l*x'
    expression = re.sub(r'(\w)(x)', r'\1*\2', expression)

    # Change '^' to '**'
    expression = expression.replace('^', '**')

    # Change ')(' to ')*('
    expression = expression.replace(')(', ')*(')

    # Adding multiplication sing in 'x(' or ')x'
    expression = re.sub(r'([1-9x])(\()', r'\1*\2', expression)
    expression = re.sub(r'(\))([1-9x])', r'\1*\2', expression)

    # Change 'π' to 'np.pi'
    expression = re.sub(r'π', 'np.pi', expression)

    # Change 'e' to 'np.e'
    expression = re.sub(r'e', 'np.e', expression)

    # Change '\d np.' to '\d*np.'
    expression = re.sub(r'(\d)(np)', r'\1*\2', expression)

    # Change '\w np.' to '\w*np.'
    expression = re.sub(r'(\w)(np)', r'\1*\2', expression)

    # Change 'xnp' to 'x * np'
    expression = re.sub(r'(x)(np)', r'\1*\2', expression)

    return expression