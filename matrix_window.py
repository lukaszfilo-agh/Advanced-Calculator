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
        self.matrix_A = None
        self.matrix_B = None
        self.matrix_R = None

        # Setting name of window
        self.setWindowTitle("Matrix Calculator")
        # Rezisizing window
        self.setFixedSize(600, 600)
        # Centering window
        self.center()

        # Creating top layout for buttons
        data_buttons_layout = QHBoxLayout()

        # Button for inserting data matrix A
        matrix_A_button = QPushButton("Insert Matrix A")
        matrix_A_button.clicked.connect(self.matrix_A_input)

        # Button for inserting data matrix B
        matrix_B_button = QPushButton("Insert Matrix B")
        matrix_B_button.clicked.connect(self.matrix_B_input)

        # Adding buttons to top widget
        data_buttons_layout.addWidget(matrix_A_button)
        data_buttons_layout.addWidget(matrix_B_button)

        # Creating labels for matrices
        matrix_A_label = QLabel('Matrix A')
        matrix_B_label = QLabel('Matrix B')
        matrix_result_label = QLabel('Result')

        # Adding matrix_A display
        self.matrix_A_text = QTextEdit()
        self.matrix_A_text.setReadOnly(True)

        # Adding matrix_A display
        self.matrix_B_text = QTextEdit()
        self.matrix_B_text.setReadOnly(True)

        # Adding result display
        self.matrix_result_text = QTextEdit()
        self.matrix_result_text.setReadOnly(True)

        # Creating layout for matrix show
        matrices_layout = QHBoxLayout()

        # Creating layout for matrix A
        matrix_A_layout = QVBoxLayout()

        # Adding label and matrix to layout
        matrix_A_layout.addWidget(
            matrix_A_label, alignment=Qt.AlignmentFlag.AlignCenter)
        matrix_A_layout.addWidget(self.matrix_A_text)

        # Creating layout for matrix B
        matrix_B_layout = QVBoxLayout()

        # Adding label and matrix to layout
        matrix_B_layout.addWidget(
            matrix_B_label, alignment=Qt.AlignmentFlag.AlignCenter)
        matrix_B_layout.addWidget(self.matrix_B_text)

        # Creating layout for operators between Two Matrices
        operators_AB = QVBoxLayout()

        # Adding buttons for operators between Two Matrices
        add_button = QPushButton('A + B')
        add_button.clicked.connect(self.add_matrices)

        subtract_button = QPushButton('A - B')
        subtract_button.clicked.connect(self.subtract_matrices)

        multiply_button = QPushButton('A * B')
        multiply_button.clicked.connect(self.multipy_matrices)

        # Adding operators to Layout
        operators_AB.addWidget(add_button)
        operators_AB.addWidget(subtract_button)
        operators_AB.addWidget(multiply_button)

        # Ading matrices layout and operators to matrices layout
        matrices_layout.addLayout(matrix_A_layout)
        matrices_layout.addLayout(operators_AB)
        matrices_layout.addLayout(matrix_B_layout)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Adding matrix show to main layout
        main_layout.addLayout(matrices_layout)

        # Adding data buttons insert to main layout
        main_layout.addLayout(data_buttons_layout)

        # Creating layout for operators for matrix A
        operators_layout_MA = QVBoxLayout()

        # Creating buttons for operators matrix A
        transpose_button_MA = QPushButton('Transpose A')
        transpose_button_MA.clicked.connect(self.matrix_A_transpose)

        det_button_MA = QPushButton('Determinant A')
        det_button_MA.clicked.connect(self.matrix_A_det)

        invert_button_MA = QPushButton('Invert A')
        invert_button_MA.clicked.connect(self.matrix_A_invert)

        eigval_button_MA = QPushButton('Eigenvalues A')
        eigval_button_MA.clicked.connect(self.matrix_A_eigvals)

        eigvect_button_MA = QPushButton('Eigenvectors A')
        eigvect_button_MA.clicked.connect(self.matrix_A_eigvect)

        jordan_decomp_MA = QPushButton('Jordan A')
        jordan_decomp_MA.clicked.connect(self.matrix_A_jordan)

        # Adding operator buttons for matrix A
        operators_layout_MA.addWidget(transpose_button_MA)
        operators_layout_MA.addWidget(det_button_MA)
        operators_layout_MA.addWidget(invert_button_MA)
        operators_layout_MA.addWidget(eigval_button_MA)
        operators_layout_MA.addWidget(eigvect_button_MA)
        operators_layout_MA.addWidget(jordan_decomp_MA)

        # Creating layout for operators for matrix B
        operators_layout_MB = QVBoxLayout()

        # Creating buttons for operators matrix B
        transpose_button_MB = QPushButton('Transpose B')
        transpose_button_MB.clicked.connect(self.matrix_B_transpose)

        det_button_MB = QPushButton('Determinant B')
        det_button_MB.clicked.connect(self.matrix_B_det)

        invert_button_MB = QPushButton('Invert B')
        invert_button_MB.clicked.connect(self.matrix_B_invert)

        eigval_button_MB = QPushButton('Eigenvalues B')
        eigval_button_MB.clicked.connect(self.matrix_B_eigvals)

        eigvect_button_MB = QPushButton('Eigenvectors B')
        eigvect_button_MB.clicked.connect(self.matrix_B_eigvect)

        jordan_decomp_MB = QPushButton('Jordan B')
        jordan_decomp_MB.clicked.connect(self.matrix_B_jordan)

        # A dding operator buttons for matrix B
        operators_layout_MB.addWidget(transpose_button_MB)
        operators_layout_MB.addWidget(det_button_MB)
        operators_layout_MB.addWidget(invert_button_MB)
        operators_layout_MB.addWidget(eigval_button_MB)
        operators_layout_MB.addWidget(eigvect_button_MB)
        operators_layout_MB.addWidget(jordan_decomp_MB)

        # Creating layout for result matrix
        result_layout = QVBoxLayout()

        # Adding result matrix to layout
        result_layout.addWidget(matrix_result_label,
                                alignment=Qt.AlignmentFlag.AlignCenter)
        result_layout.addWidget(self.matrix_result_text)

        # Creating layout for result matrix and operators
        res_operators_layout = QHBoxLayout()
        res_operators_layout.addLayout(operators_layout_MA)
        res_operators_layout.addLayout(result_layout)
        res_operators_layout.addLayout(operators_layout_MB)

        # Adding result and operators to main layout
        main_layout.addLayout(res_operators_layout)

        # Create button for going back to menu
        back_button = QPushButton("Back to Main Window")
        back_button.clicked.connect(self.back_to_menu)

        # Adding back button to main layout
        main_layout.addWidget(back_button)

        # Setting main layout of window
        self.setLayout(main_layout)

    def matrix_A_input(self):
        # Creating dialog for data input
        matrix_data = MatrixInputDialog()

        # Getting data from input
        matrix_data.exec()
        self.matrix_A = matrix_data.getInputs()

        # Updating matrix_A show widget
        self.matrix_A_text.setPlainText(str(self.matrix_A))

    def matrix_B_input(self):
        # Creating dialog for data input
        matrix_data = MatrixInputDialog()

        # Getting data from input
        matrix_data.exec()
        self.matrix_B = matrix_data.getInputs()

        # Updating matrix_A show widget
        self.matrix_B_text.setPlainText(str(self.matrix_B))

    def add_matrices(self):
        self.matrix_R = self.matrix_A + self.matrix_B
        self.result_show('A + B')

    def subtract_matrices(self):
        self.matrix_R = self.matrix_A - self.matrix_B
        self.result_show('A - B')

    def multipy_matrices(self):
        self.matrix_R = self.matrix_A @ self.matrix_B
        self.result_show('A * B')

    def matrix_A_det(self):
        self.matrix_R = linalg.det(self.matrix_A)
        self.result_show('Determinant A')

    def matrix_A_transpose(self):
        self.matrix_R = np.transpose(self.matrix_A)
        self.result_show('Transpose A')

    def matrix_A_invert(self):
        self.matrix_R = linalg.inv(self.matrix_A)
        self.result_show('Invert A')

    def matrix_A_eigvals(self):
        self.matrix_R, _ = linalg.eig(self.matrix_A)
        self.result_show('Eigenvalues A')

    def matrix_A_eigvect(self):
        _, self.matrix_R = linalg.eig(self.matrix_A)
        self.result_show('Eigenvectors A')

    def matrix_A_jordan(self):
        eigvals, eigvects = linalg.eig(self.matrix_A)
        jordan = np.diag(eigvals)
        p = eigvects
        pinv = linalg.inv(eigvects)
        self.matrix_result_text.setPlainText('Matrix A Jordan\n' + 'P' + '\n' + str(
            p) + '\n' + 'J' + '\n' + str(jordan) + '\n' + 'P_inv' + '\n' + str(pinv))

    def matrix_B_det(self):
        self.matrix_R = linalg.det(self.matrix_B)
        self.result_show('Determinant B')

    def matrix_B_transpose(self):
        self.matrix_R = np.transpose(self.matrix_B)
        self.result_show('Transpose B')

    def matrix_B_invert(self):
        self.matrix_R = linalg.inv(self.matrix_B)
        self.result_show('Invert B')

    def matrix_B_eigvals(self):
        self.matrix_R, _ = linalg.eig(self.matrix_B)
        self.result_show('Eigenvalues B')

    def matrix_B_eigvect(self):
        _, self.matrix_R = linalg.eig(self.matrix_B)
        self.result_show('Eigenvectors B')

    def matrix_B_jordan(self):
        eigvals, eigvects = linalg.eig(self.matrix_B)
        jordan = np.diag(eigvals)
        p = eigvects
        pinv = linalg.inv(eigvects)
        self.matrix_result_text.setPlainText('Matrix B Jordan\n' + 'P' + '\n' + str(
            p) + '\n' + 'J' + '\n' + str(jordan) + '\n' + 'P_inv' + '\n' + str(pinv))

    def result_show(self, msg):
        self.matrix_result_text.setPlainText(msg + '\n' + str(self.matrix_R))

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

