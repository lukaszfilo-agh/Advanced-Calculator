from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)


# Class for help window for integrals:
class IntegralsHelpWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # Setting name of window
        self.setWindowTitle("Help")

        # Rezisizing window
        self.resize(300, 200)

        # Centering window
        self.__center()

        # Setting text for help window
        help_text = QLabel("Integrals helper:\n"
                            "- note that we tolerate complex solutions, hence: \n"
                            "   *integral of f(x) = 1/x is equal to ln(x) instead of ln(|x|) and so on,\n"
                            "- for proper results: \n"
                            "   *use \"*\" always for multiplication,\n"
                            "   *group operands with brackets, for instance: (x-1)/(sqrt(x)-1),\n"
                            "- you are required to add brackets to functions - functions with no \narguments"
                            " will not be accepted.")

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
    def __center(self) -> None:
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())
