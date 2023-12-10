import sys
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QApplication
)

from PyQt6.QtCore import Qt

import numpy as np

from matrix_input_dialog import MatrixInputDialog


class MatrixWindow(QWidget):
    # Class for matrix operations
    def __init__(self, menu_window):
        super().__init__()
        self.parent = menu_window

        # Creating variables for matrices
        self.matrix1 = None
        self.matrix2 = None

        # Setting name of window
        self.setWindowTitle("Matrix Calculator")
        # Rezisizing window
        self.resize(500, 600)
        # Centering window
        self.center()

        # Button for inserting data matrix 1
        matrix1_button = QPushButton("Insert Matrix 1")
        matrix1_button.clicked.connect(self.matrix1_input)

        # Button for inserting data matrix 2
        matrix2_button = QPushButton("Insert Matrix 2")
        matrix2_button.clicked.connect(self.matrix2_input)

        # Creating top layout for buttons
        data_buttons_layout = QHBoxLayout()

        # Adding buttons to top widget
        data_buttons_layout.addWidget(matrix1_button)
        data_buttons_layout.addWidget(matrix2_button)

        # Creating labels for matrices
        matrix1_label = QLabel('Matrix 1')
        matrix2_label = QLabel('Matrix 2')
        matrix_result_label = QLabel('Result')

        # Adding matrix1 display
        self.matrix1_text = QTextEdit()
        self.matrix1_text.setReadOnly(True)

        # Adding matrix1 display
        self.matrix2_text = QTextEdit()
        self.matrix2_text.setReadOnly(True)

        # Adding result display
        self.matrix_result_text = QTextEdit()
        self.matrix_result_text.setReadOnly(True)

        # Creating layout for matrix show
        matrix_layout = QHBoxLayout()
        
        # Creating layout for matrix 1
        matrix1_layout = QVBoxLayout()

        # Adding label and matrix to layout
        matrix1_layout.addWidget(matrix1_label, alignment=Qt.AlignmentFlag.AlignCenter)
        matrix1_layout.addWidget(self.matrix1_text)

        # Creating layout for matrix 2
        matrix2_layout = QVBoxLayout()

        # Adding label and matrix to layout
        matrix2_layout.addWidget(matrix2_label, alignment=Qt.AlignmentFlag.AlignCenter)
        matrix2_layout.addWidget(self.matrix2_text)
        
        # Ading matrices layout to matrices layout
        matrix_layout.addLayout(matrix1_layout)
        matrix_layout.addLayout(matrix2_layout)

        # Create button for going back to menu
        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.back_to_menu)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Adding matrix show to main layout
        main_layout.addLayout(matrix_layout)

        # Adding top widget to main layout
        main_layout.addLayout(data_buttons_layout)

        # Creating buttons for operators
        add_button = QPushButton('Add')
        subtract_button = QPushButton('Subtract')
        multiply_button = QPushButton('Multipy')
        transpose_button = QPushButton('Transpose')
        invert_button = QPushButton('Invert')

        # Creating layout for operators
        operators_layout_c1 = QVBoxLayout()

        # Adding operator buttons to layout
        operators_layout_c1.addWidget(add_button)
        operators_layout_c1.addWidget(subtract_button)
        operators_layout_c1.addWidget(multiply_button)
        operators_layout_c1.addWidget(transpose_button)
        operators_layout_c1.addWidget(invert_button)

        # Creating layout for result matrix
        result_layout = QVBoxLayout()

        # Adding result matrix to layout
        result_layout.addWidget(matrix_result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.matrix_result_text)

        # Creating layout for result matrix and operators
        res_operators_layout = QHBoxLayout()
        res_operators_layout.addLayout(result_layout)
        res_operators_layout.addLayout(operators_layout_c1)

        # Adding result and operators to main layout
        main_layout.addLayout(res_operators_layout)

        # Adding back button to main layout
        main_layout.addWidget(back_button)

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
        self.matrix2_text.setPlainText(str(self.matrix2))
    
    # Function for going back to main menu
    def back_to_menu(self):
        self.close()
        self.parent.show()

    # Method for centering windows
    def center(self):
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


# def main():
#     app = QApplication(sys.argv)
#     window = MatrixWindow(None)
#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()
