import numpy as np
import re
import matplotlib
from plot_help_window import PlotHelpWindow
from plot_input_dialog import PlotInputDialog
from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QWidget,
    QMessageBox
)

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
    NavigationToolbar2QT as NavigationToolbar
)
matplotlib.use('QtAgg')


# TODO repair function eg 1/x
# TODO sin(x-pi)
# TODO buttons from keyboards adding at back of inputfield
# TODO add eg. x=5
# TODO sqrt(-1)
# TODO write HELP

# TODO lims for multiple plots ???
# TODO add log ???
# TODO remove >< from function keyboard but it works in stragne way


class MplCanvas(FigureCanvas):
    # Class for widged plot display
    def __init__(self, parent=None, width=11, height=4, dpi=100) -> None:
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class PlotWindow(QWidget):
    # Class for window with plots
    def __init__(self, menu_window) -> None:
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
        self.__center()

        # Create canvas for plot
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.canvas.axes.grid(True)

        # Create toolbar, passing canvas as first parament, parent (self, the PlotWindow) as second.
        canvas_toolbar = NavigationToolbar(self.canvas, self)

        # Create button for inserting data
        data_button = QPushButton("Insert fuction")
        data_button.clicked.connect(self.__draw_plot)

        # Create button for clearing plot
        clear_button = QPushButton("Clear plot")
        clear_button.clicked.connect(self.__clear_plot)

        # Create button for showing help
        help_button = QPushButton("Help")
        help_button.clicked.connect(self.__show_help)

        # Create button for going back to menu
        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.__back_to_menu)

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
    def __back_to_menu(self) -> None:
        self.close()
        self.parent.show()

    # Function for clearing plot window
    def __clear_plot(self) -> None:
        self.canvas.axes.cla()
        self.canvas.axes.grid(True)
        self.canvas.draw()

    # Function for drawing plots
    def __draw_plot(self) -> None:
        # Creating dialog for data input
        dialog_data = PlotInputDialog()

        # Getting data from input
        dialog_data.exec()
        function_math, function_str, lim1, lim2 = dialog_data.get_inputs()

        if function_math is None:
            return

        try:
            # Creating vector with x values
            xvals = np.arange(lim1, lim2, 0.01)

            # Defining lambda function
            def fx(x): return eval(function_math)

            # Calculating values for function
            yvals = fx(xvals)

            # Checking for infs in yvals
            if np.isinf(yvals).any():
                raise InfNanError

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
        if lim2 > 0 > lim1:
            self.canvas.axes.axhline(0, color='black', linewidth=1)
            self.canvas.axes.axvline(0, color='black', linewidth=1)

        # Setting lims for x axis
        # self.canvas.axes.set_xlim((lim1, lim2))

        # Setting lims for y axis
        # self.canvas.axes.set_ylim((ylim_min, ylim_max))

        # Displaying plot
        self.canvas.draw()

    # Method for centering windows
    def __center(self) -> None:
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def __show_help(self) -> None:
        self.help_window.show()


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
