from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QMessageBox,
    QDialog, 
    QLineEdit, 
    QDialogButtonBox, 
    QFormLayout
)
from PyQt6.QtCore import QRegularExpression, Qt, QEvent
from PyQt6.QtGui import QRegularExpressionValidator, QKeyEvent, QShortcut, QKeySequence
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)

import re

import matplotlib
matplotlib.use('QtAgg')

# Class for widged plot display
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=11, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


# Class for window with plots
class PlotWindow(QWidget):
    def __init__(self, menu_window):
        super().__init__()
        # Setting parent window
        self.parent = menu_window
        # Creating Help window
        self.help_window = Help_Plot()
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
        data_button.clicked.connect(self.draw_plot)

        # Create button for clearing plot
        clear_button = QPushButton("Clear plot")
        clear_button.clicked.connect(self.clear_plot)

        # Create button for showing help
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.show_help)

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
        bottom_layout.addWidget(data_button)
        bottom_layout.addWidget(clear_button)
        bottom_layout.addWidget(help_button)
        bottom_layout.addWidget(back_button)

        # Adding bottom layout to main layout
        main_layout.addLayout(bottom_layout)

        # Setting layout for window
        self.setLayout(main_layout)


    # Function for going back to main menu
    def back_to_menu(self):
        self.close()
        self.parent.show()

    # Function for clearing plot window
    def clear_plot(self):
        self.canvas.axes.cla()
        self.canvas.axes.grid(True)
        self.canvas.draw()

    # Function for drawing plots
    def draw_plot(self):
        # Creating dialog for data input
        dialog_data = InputDialog()
        
        # Getting data from input
        dialog_data.exec()
        function_str, lim1, lim2 = dialog_data.getInputs()

        try:
            if len(function_str) == 0 or len(lim1) == 0 or len(lim2) == 0:
                raise InputError

            # Checking for illegal charaters
            invalid_chars = func_bad_chars(function_str)
            if len(invalid_chars) != 0:
                raise InvalidCharacters
            
            # Conversion of lim1 and lim2
            lim1 = float(lim1)
            lim2 = float(lim2)

            # Checking for limit error
            if lim1 > lim2:
                raise LimError

        # Catching errors for empty data
        except InputError:
            self.error_window('Entered data cannot be empty')
            return

        # Catching errors for invalid chars
        except InvalidCharacters:
            self.error_window(invalid_chars)
            return

        # Catching errors for LimErrors
        except LimError:
            self.error_window(lim1=lim1, lim2=lim2)
            return

        # Catching errors and displaying error window
        except:
            self.error_window(function_str, lim1, lim2)
            return

        # Creating vector with x values
        xvals = np.arange(lim1, lim2, 0.01)

        # Creating expression for eval
        function_math = convert_func_math(function_str)
        
        # Defining lambda function
        def fx(x): return eval(function_math)

        try:
            # Calculating values for function
            yvals = fx(xvals)

        except:
            self.error_window('Error while calc:\n' + function_math, lim1, lim2)
            return

        # Drawing plot
        self.canvas.axes.plot(xvals, yvals)
        # Showing grid
        self.canvas.axes.grid(True)
        # Setting title
        self.canvas.axes.set_title(f'$f(x) = {function_str}$')
        # Adding bolded x and y axis
        if lim2 > 0 and lim1 < 0:
            self.canvas.axes.axhline(0, color='black', linewidth=1)
            self.canvas.axes.axvline(0, color='black', linewidth=1)
        # Setting lims for x axis
        # self.canvas.axes.set_xlim((lim1, lim2))
        # self.canvas.axes.set_ylim((fx(lim1), fx(lim2)))
        # Displaying plot
        self.canvas.draw()

    # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def error_window(self, str='', lim1=0, lim2=0):
        message_box = QMessageBox()
        if lim1 > lim2:
            message_box.setText(f"Lower limit is greater than upper limit.")
            print("Error limits")
        elif lim1 != 0:
            message_box.setText(
                f"Data enetered:\nf(x)={str}\nlim1={lim1}\nlim2={lim2}")
            print("Error data")
        else:
            message_box.setText(f"You have entered invalid input: {str}.")
            print("Invalid chars")
        message_box.setWindowTitle("ERROR")
        message_box.setStandardButtons(QMessageBox.StandardButton.Ok)

        # Action after clicking ok
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")

    def show_help(self):
        self.help_window.show()

# Class for input dialog
class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Calling function to initialize UI
        self.init_ui()

    def init_ui(self):
        # Setting window title
        self.setWindowTitle('Wprowadź wzór funkcji')
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
                ['1', '2', '3', '*', '/', 'sin( )', 'cos( )'],
                ['4', '5', '6', '+', '-', 'tg( )', 'ctg( )'],
                ['7', '8', '9', '=', '^', 'arcsin( )', 'arccos()'],
                ['0', 'x', '( )', '| |', 'e', 'arctg( )', 'arcctg( )'],
                ['<', '>', '<-', 'C']
            ],
            [  # Keyboard for lower limit
                ['1', '2', '3', '4'],
                ['5', '6', '7', '8'],
                ['9', '0', '.', '-'],
                ['pi', '<-', '->', 'C']
            ],
            [  # Keyboard for upper limit
                ['1', '2', '3', '4'],
                ['5', '6', '7', '8'],
                ['9', '0', '.', '-'],
                ['pi', '<-', '->', 'C']
            ]
        ]

        # Creating buttons for changing input fields
        button_func_field = QPushButton('Function')
        button_func_field.clicked.connect(self.switch_func_keyboard)
        button_lower_limit_field = QPushButton('Lower limit')
        button_lower_limit_field.clicked.connect(self.switch_lower_lim_keyboard)
        button_upper_limit_field = QPushButton('Upper limit')
        button_upper_limit_field.clicked.connect(self.switch_upper_lim_keyboard)
        
        # Creating Layout for buttons
        input_field_buttons = QHBoxLayout()
        
        # Adding buttons to layout
        input_field_buttons.addWidget(button_func_field)
        input_field_buttons.addWidget(button_lower_limit_field)
        input_field_buttons.addWidget(button_upper_limit_field)

        main_layout.addLayout(input_field_buttons)

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
        elif text == 'OK':
            expression = self.input_fields[self.active_field].text()
            print(f'Wprowadzona wartość pola {self.active_field + 1}: {expression}')
            self.active_field = (self.active_field + 1) % len(self.input_fields)
            self.update_keyboard()
        elif text == '=':
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
        return tuple(input.text() for input in self.input_fields)

class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()
    
    def check_active_field(self):
        active_widget = self.focusWidget()
        print(active_widget)
        return active_widget

    def keyPressEvent(self, event):
        # self.check_active_field()
        allowed_keys = [Qt.Key.Key_Backspace, 
                        Qt.Key.Key_Left, 
                        Qt.Key.Key_Right, 
                        Qt.Key.Key_X, 
                        Qt.Key.Key_Minus, 
                        Qt.Key.Key_Plus]
        if event.text().isdigit() or event.key() in allowed_keys:
            super().keyPressEvent(event)


class Help_Plot(QWidget):
    def __init__(self):
        super().__init__()
        # Setting name of window
        self.setWindowTitle("Help")
        # Rezisizing window
        self.resize(300, 300)
        # Centering window
        self.center()

        help_text = QLabel("HELP HELP HELP")

        # Create button for closing window
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Adding pieces to layout
        main_layout.addWidget(help_text)
        main_layout.addWidget(close_button)

        # Setting layout for window
        self.setLayout(main_layout)

        # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


def func_bad_chars(expression):
    result = re.findall(r'(?!(?:sin|cos|tan|tg|e\^|\d+|[\(\)\+\-\*\/\^]|\dx|x))\b\S+\b', expression)
    return result


def convert_func_math(expression):
    # Change 'e^x' to 'np.exp(x)'
    expression = re.sub(r'e\^(.*)', r'np.exp(\1)', expression)

    # Change 'e^x' to 'np.exp(x)'
    expression = re.sub(r'\|(.*)\|', r'np.abs(\1)', expression)

    # Change 'sin' to 'np.sin'
    expression = re.sub(r'\bsin\b', 'np.sin', expression)

    # Change 'cos' to 'np.cos'
    expression = re.sub(r'\bcos\b', 'np.cos', expression)

    # Change 'tan or tg' to 'np.tan'
    expression = re.sub(r'\btan\b', 'np.tan', expression)
    expression = re.sub(r'\btg\b', 'np.tan', expression)

    # Change 'x' to '*x'
    expression = re.sub(r'(\d)(x)', r'\1*\2', expression)

    # Change '^' to '**'
    expression = expression.replace('^', '**')

    # Change ')(' to ')*('
    expression = expression.replace(')(', ')*(')

    # Adding multiplication sing in 'x(' or ')x'
    expression = re.sub(r'([1-9x])(\()', r'\1*\2', expression)
    expression = re.sub(r'(\))([1-9x])', r'\1*\2', expression)

    return expression

def convert_lim_math(expression):
    expression = re.sub(r'\bpi\b', 'np.pi', expression)
    return expression

def lim_bad_chars(expression):
    result = re.findall(
        r'^(?![\dpi]+?$).*', expression)
    return result

class InvalidCharacters(Exception):
    "Raised when the input can't be evaluated"
    pass


class LimError(Exception):
    "Raised when lim1 > lim2"
    pass

class InputError(Exception):
    "Raised when data input is NULL"
    pass
