import sys
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit
)


import numpy as np

from matrix_input_dialog import MatrixInputDialog


class MatrixWindow(QWidget):
    # Class for matrix operations
    def __init__(self, menu_window):
        super().__init__()
        self.parent = menu_window

        self.matrix1 = None
        self.matrix2 = None

        # Setting name of window
        self.setWindowTitle("Matrix Calculator")
        # Rezisizing window
        self.resize(600, 600)

        # Button for inserting data matrix 1
        matrix1_button = QPushButton("Insert Matrix 1")
        matrix1_button.clicked.connect(self.matrix1_input)

        # Button for inserting data matrix 2
        matrix2_button = QPushButton("Insert Matrix 2")
        matrix2_button.clicked.connect(self.matrix2_input)

        # Creating top layout for buttons
        top_layout = QHBoxLayout()

        # Adding buttons to top widget
        top_layout.addWidget(matrix1_button)
        top_layout.addWidget(matrix2_button)

        # Adding matrix1 display
        self.matrix1_text = QTextEdit()
        self.matrix1_text.setReadOnly(True)

        # Adding matrix1 display
        self.matrix2_text = QTextEdit()
        self.matrix2_text.setReadOnly(True)

        # Creating layout for matrix show
        matrix_layout = QHBoxLayout()

        # Ading matrices to layout
        matrix_layout.addWidget(self.matrix1_text)
        matrix_layout.addWidget(self.matrix2_text)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Adding top widget to main layout
        main_layout.addLayout(top_layout)

        # Adding matrix show to main layout
        main_layout.addLayout(matrix_layout)

        # Setting main layout of window
        self.setLayout(main_layout)

    def matrix1_input(self):
        # Creating dialog for data input
        matrix_data = MatrixInputDialog()

        # Getting data from input
        matrix_data.exec()
        self.matrix1 = matrix_data.getInputs()

        # Updating matrix1 show widget
        self.matrix1_text.setPlainText(str(self.matrix1))

    def matrix2_input(self):
        # Creating dialog for data input
        matrix_data = MatrixInputDialog()

        # Getting data from input
        matrix_data.exec()
        self.matrix2 = matrix_data.getInputs()

        # Updating matrix1 show widget
        self.matrix2_text.setPlainText(str(self.matrix1))


# def main():
#     app = QApplication(sys.argv)
#     window = MatrixWindow(None)
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()
