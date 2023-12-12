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

from scipy import linalg

from matrix_input_dialog import MatrixInputDialog


class MatrixWindow(QWidget):
    # Class for matrix operations
    def __init__(self, menu_window):
        super().__init__()
        self.parent = menu_window

        # Creating variables for matrices
        self.matrix1 = None
        self.matrix2 = None

        self.matrix_result = None

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

        # Adding data buttons insert to main layout
        main_layout.addLayout(data_buttons_layout)

        # Creating layout for operators
        operators_layout_c1 = QVBoxLayout()
        operators_layout_c2 = QVBoxLayout()

        # Creating buttons for operators Column 1
        add_button = QPushButton('Add')
        add_button.clicked.connect(self.add_matrices)

        subtract_button = QPushButton('Subtract')
        subtract_button.clicked.connect(self.subtract_matrices)

        multiply_button = QPushButton('Multipy')
        multiply_button.clicked.connect(self.multipy_matrices)

        transpose_button = QPushButton('Transpose')
        transpose_button.clicked.connect(self.matrix1_transpose)

        invert_button = QPushButton('Invert')
        invert_button.clicked.connect(self.matrix1_invert)

        # Adding operator buttons column 1 to layout
        operators_layout_c1.addWidget(add_button)
        operators_layout_c1.addWidget(subtract_button)
        operators_layout_c1.addWidget(multiply_button)
        operators_layout_c1.addWidget(transpose_button)
        operators_layout_c1.addWidget(invert_button)

        # Creating buttons for operators Column 2
        eigval_button = QPushButton('Eigenvalues')
        eigval_button.clicked.connect(self.matrix1_eigvals)

        eigvect_button = QPushButton('Eigenvectors')
        eigvect_button.clicked.connect(self.matrix1_eigvect)

        jordan_decomp = QPushButton('Jordan')
        jordan_decomp.clicked.connect(self.matrix1_jordan)

        ph_1 = QPushButton('PH1')
        ph_1.clicked.connect(self.ph1_func)

        ph_2 = QPushButton('PH2')
        ph_2.clicked.connect(self.ph2_func)

        # Adding operator buttons column 2 to layout
        operators_layout_c2.addWidget(eigval_button)
        operators_layout_c2.addWidget(eigvect_button)
        operators_layout_c2.addWidget(jordan_decomp)
        operators_layout_c2.addWidget(ph_1)
        operators_layout_c2.addWidget(ph_2)

        # Creating layout for result matrix
        result_layout = QVBoxLayout()

        # Adding result matrix to layout
        result_layout.addWidget(matrix_result_label, alignment=Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.matrix_result_text)

        # Creating layout for result matrix and operators
        res_operators_layout = QHBoxLayout()
        res_operators_layout.addLayout(result_layout)
        res_operators_layout.addLayout(operators_layout_c1)
        res_operators_layout.addLayout(operators_layout_c2)

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

    def add_matrices(self):
        self.matrix_result = self.matrix1 + self.matrix2
        self.result_show()

    def subtract_matrices(self):
        self.matrix_result = self.matrix1 - self.matrix2
        self.result_show()

    def multipy_matrices(self):
        self.matrix_result = self.matrix1 @ self.matrix2
        self.result_show()

    def matrix1_transpose(self):
        self.matrix_result = np.transpose(self.matrix1)
        self.matrix2_text.setPlainText('Matrix 1 transposed')
        self.result_show()

    def matrix1_invert(self):
        self.matrix_result = linalg.inv(self.matrix1)
        self.matrix2_text.setPlainText('Matrix 1 inverted')
        self.result_show()

    def matrix1_eigvals(self):
        self.matrix_result, _ = linalg.eig(self.matrix1)
        self.matrix2_text.setPlainText('Matrix 1 Eigvals')
        self.result_show()

    def matrix1_eigvect(self):
        _, self.matrix_result = linalg.eig(self.matrix1)
        self.matrix2_text.setPlainText('Matrix 1 Eigvects')
        self.result_show()

    def matrix1_jordan(self):
        pass

    def ph1_func(self):
        pass

    def ph2_func(self):
        pass

    def result_show(self):
        self.matrix_result_text.setPlainText(str(self.matrix_result))
    
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


def main():
    app = QApplication(sys.argv)
    window = MatrixWindow(None)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
