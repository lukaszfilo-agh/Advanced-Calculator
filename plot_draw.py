from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QLabel,
    QMessageBox
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
        # Getting function
        function_str, done1 = QtWidgets.QInputDialog.getText(
            self, 'Function', 'f(x):')

        try:
            # Checking for illegal charaters
            invalid_chars = func_bad_chars(function_str)
            if len(invalid_chars) != 0:
                raise InvalidCharacters

            # Getting lower limit
            lim1, done2 = QtWidgets.QInputDialog.getDouble(
                self, 'Lower limit', 'Enter lower limit:')

            # Getting upper limit
            lim2, done3 = QtWidgets.QInputDialog.getDouble(
                self, 'Upper limit', 'Enter upper limit:')

            # Checking for limit error
            if lim1 > lim2:
                raise LimError

            # Drawing plot with entered data
            if done1 and done2 and done3:

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
    result = re.findall(r'(?!(?:sin|cos|e\^|\b\d|x+\b|\b[\(\)\+\-\*\/\^]\b|x))\b\S+\b', expression)
    
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
