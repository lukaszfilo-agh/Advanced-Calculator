from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
)
from PyQt6.QtCore import Qt


# Class for displaying integrals results:
class IntegralsResultWindow(QWidget):
    def __init__(self, res: str) -> None:
        super().__init__()

        # Setting name of window
        self.setWindowTitle("SOLUTION")

        # Setting fixed width - so that title is visible:
        self.setFixedWidth(250)

        # Setting text for help window
        help_text = QLabel(f"{res}")

        help_text.setWordWrap(True)

        # Create button for closing window
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Adding pieces to layout
        main_layout.addWidget(help_text)
        main_layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Setting layout for window
        self.setLayout(main_layout)

        # Centering window
        self.__center()

    # Method for centering windows
    def __center(self) -> None:
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())