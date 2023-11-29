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
from PyQt6 import QtWidgets
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
        try:
            dialog_data = InputDialog()
            dialog_data.exec()

            function_str, lim1, lim2 = dialog_data.getInputs()

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

            # Creating vector with x values
            xvals = np.arange(lim1, lim2, 0.01)

            # Creating expression for eval
            function_math = convert_func_math(function_str)

            # Defining lambda function
            def fx(x): return eval(function_math)

            # Calculating values for function
            yvals = fx(xvals)

            # Drawing plot
            self.canvas.axes.plot(xvals, yvals)
            # Showing grid
            self.canvas.axes.grid(True)
            # Setting title
            self.canvas.axes.set_title(f'$f(x) = {function_str}$')
            # Adding bolded x and y axis
            self.canvas.axes.axhline(0, color='black', linewidth=1)
            self.canvas.axes.axvline(0, color='black', linewidth=1)
            # Displaying plot
            self.canvas.draw()

        except InputError:
            self.error_window('Entered data cannot be empty')

        # Catching errors for invalid chars
        except InvalidCharacters:
            self.error_window(invalid_chars)

        # Catching errors for LimErrors
        except LimError:
            self.error_window(lim1=lim1, lim2=lim2)

        # Catching errors and displaying error window
        except:
            self.error_window(function_str, lim1, lim2)

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

class InputDialog(QDialog):
    def __init__(self):
        super().__init__()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel, self)
        layout = QFormLayout(self)
        # labels = ['f(x):', 'Lower limit:', 'Upper limit:']
        # self.inputs = []
        # for lab in labels:
        #     self.inputs.append(QLineEdit(self))
        #     layout.addRow(lab, self.inputs[-1])
        
        self.inputs = [QLineEdit(self), QLineEdit(self), QLineEdit(self)]
        layout.addRow('f(x): ', self.inputs[0])
        layout.addRow('Lower limit: ', self.inputs[1])
        layout.addRow('Upper limit: ', self.inputs[2])

        layout.addWidget(buttonBox)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
    
    def getInputs(self):
        return tuple(input.text() for input in self.inputs)

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
