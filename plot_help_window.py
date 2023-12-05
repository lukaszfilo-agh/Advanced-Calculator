from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)

# Class for help window for plot
class PlotHelpWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Setting name of window
        self.setWindowTitle("Help")
        # Rezisizing window
        self.resize(300, 300)
        # Centering window
        self.center()

        # Setting text for help window
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
