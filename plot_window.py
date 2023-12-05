from plot_help_window import PlotHelpWindow
from plot_input_dialog import PlotInputDialog
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox
)
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)

import re

import matplotlib
matplotlib.use('QtAgg')


# TODO repair function eg 1/x
# TODO sin(x-pi)
# TODO buttons from keyboards adding at back of inputfield
# TODO add eg. x=5
# TODO sqrt(-1)

# TODO lims for multiple plots ???
# TODO add log ???
# TODO remove >< from function keyboard but it works in stragne way

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
        self.help_window = PlotHelpWindow()
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
        dialog_data = PlotInputDialog()

        # Getting data from input
        dialog_data.exec()
        function_str, lim1, lim2 = dialog_data.getInputs()

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

            # Creating vector with x values
            # xvals = np.arange(lim1 - 100, lim2 + 100, 0.01)
            xvals = np.arange(lim1, lim2, 0.01)
            xvals_lim = np.arange(lim1, lim2, 0.01)

            # Creating expression for eval
            function_math = convert_func_math(function_str)

            # Defining lambda function
            def fx(x): return eval(function_math)

            # Calculating values for function
            yvals = fx(xvals)
            print(yvals)
            y_n = yvals[0]
            yvals_lim = fx(xvals_lim)

            # Checking for infs in yvals
            if np.isinf(yvals).any():
                raise InfNanError

        # Catching errors for empty data
        except EmptyInputError:
            return

        # Catching errors for invalid chars
        except InvalidCharacters:
            return

        # Catching errors for LimErrors
        except LimError:
            return

        # Catching errors for INF in yvals
        except InfNanError:
            return

        # Catching all other exceptions
        except Exception as e:
            print('different exception')
            message_box = QMessageBox()
            message_box.setWindowTitle("ERROR")
            message_box.setText(
                f"ERROR \n Str: {function_str} \n Math: {function_math} \n Lim1: {lim1} \n Lim2: {lim2} \n EXCEPTION: {e}")
            print(f"EXCEPTION: {e}")
            result = message_box.exec()
            if result == QMessageBox.StandardButton.Ok:
                print("Error closed")
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
        # ylim_min = np.min(yvals_lim)
        # ylim_max = np.max(yvals_lim)
        # self.canvas.axes.set_ylim((ylim_min, ylim_max))
        # Displaying plot
        self.canvas.draw()

    # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_help(self):
        self.help_window.show()


def func_bad_chars(expression):
    result = re.findall(
        r'(?!(?:sin|arcsin|cos|arccos|tg|arctg|ctg|arctg|sqrt|e\^|\d+|[\(\)\+\-\*\/\^]|\dx|x))\b\S+\b', expression)
    return result


def convert_func_math(expression):
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


def lim_bad_chars(expression):
    result = re.findall(r'[^0-9eπ\-]', expression)
    return result


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

class InfNanError(Exception):
    "Raised when yvals are INF or nan"

    def __init__(self) -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        message_box.setText(f"Values of fuction are inf, -inf or nan.")
        print("inf or -inf")
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")


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
