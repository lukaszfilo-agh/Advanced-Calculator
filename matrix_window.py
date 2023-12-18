import sys
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QLabel,
    QApplication,
    QMessageBox
)

from PyQt6.QtCore import Qt

import numpy as np

from scipy import linalg

from matrix_input_dialog import MatrixInputDialog


# TODO Matrix none exception
# TODO print result +-j, delete +

class MatrixWindow(QWidget):
    """
    Class for window with matrix operators
    """
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
        self.matrix_R_text = QTextEdit()
        self.matrix_R_text.setReadOnly(True)

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
        result_layout.addWidget(self.matrix_R_text)

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

    def matrix_A_input(self) -> None:
        """
        Method for inserting data to matrix A
        """
        # Creating dialog for data input
        matrix_data = MatrixInputDialog()

        # Getting data from input
        matrix_data.exec()
        self.matrix_A = matrix_data.getInputs()
        if self.matrix_A is not None:
            # Updating matrix_A show widget
            self.matrix_A_text.setPlainText(str(self.matrix_A))
        else:
            self.matrix_A_text.setPlainText('')

        # Clearing result
        self.matrix_R_text.setPlainText('')

    def matrix_B_input(self) -> None:
        """
        Method for inserting data to matrix B
        """
        # Creating dialog for data input
        matrix_data = MatrixInputDialog()

        # Getting data from input
        matrix_data.exec()
        self.matrix_B = matrix_data.getInputs()

        if self.matrix_B is not None:
            # Updating matrix_A show widget
            self.matrix_B_text.setPlainText(str(self.matrix_B))
        else:
            self.matrix_B_text.setPlainText('')

        # Clearing result
        self.matrix_R_text.setPlainText('')

    def add_matrices(self) -> None:
        """
        Method for adding matrices A and B

        Raises
        ----------
        MatrixNoneError
            If matrix A or B is None

        OperationError
            If matrices are not same size
        """
        try:
            if self.matrix_A is None or self.matrix_B is None:
                raise MatrixNoneError
            if self.matrix_A.shape != self.matrix_B.shape:
                raise OperationError('Matrices must be same size')
            
            self.matrix_R = self.matrix_A + self.matrix_B
            self.result_show('A + B')
            
        except (OperationError, MatrixNoneError):
            return

        

    def subtract_matrices(self) -> None:
        """
        Method for adding matrices A and B

        Raises
        ----------
        MatrixNoneError
            If matrix A or B is None

        OperationError
            If matrices are not same size        
        """
        try:
            if self.matrix_A is None or self.matrix_B is None:
                 raise MatrixNoneError
            if self.matrix_A.shape != self.matrix_B.shape:
                raise OperationError('Matrices must be same size')
            
            self.matrix_R = self.matrix_A - self.matrix_B
            self.result_show('A - B')

        except (OperationError, MatrixNoneError):
            return

    def multipy_matrices(self) -> None:
        """
        Method for multiplying matrices A and B

        Raises
        ----------
        MatrixNoneError
            If matrix A or B is None

        OperationError
            If shapes of matrices don't match
        """
        try:
            if self.matrix_A is None or self.matrix_B is None:
                 raise MatrixNoneError
            if self.matrix_A.shape[1] != self.matrix_B.shape[0]:
                raise OperationError('Shapes of matrices do not match')
            
            self.matrix_R = self.matrix_A @ self.matrix_B
            self.result_show('A * B')

        except (OperationError, MatrixNoneError):
            return
        

    def matrix_A_det(self) -> None:
        """
        Method for calculating determinant of matrix A

        Raises
        ----------
        MatrixNoneError
            If matrix A is None

        OperationError
            If matrix A is not square
        """
        try:
            if self.matrix_A is None:
                raise MatrixNoneError('A')
            if self.matrix_A.shape[0] != self.matrix_A.shape[1]:
                raise OperationError('Matrix is not square')
            self.matrix_R = linalg.det(self.matrix_A)
            self.result_show('Determinant A')

        except (OperationError, MatrixNoneError):
            return
        

    def matrix_A_transpose(self) -> None:
        """
        Method for transposing matrix A

        Raises
        ----------
        MatrixNoneError
            If matrix A is None

        OperationError
            If matrix A is None
        """
        try:
            if self.matrix_A is None:
                raise MatrixNoneError('A')
            self.matrix_R = np.transpose(self.matrix_A)
            self.result_show('Transpose A')

        except MatrixNoneError:
            return
        

    def matrix_A_invert(self) -> None:
        """
        Method for inverting matrix A

        Raises
        ----------
        MatrixNoneError
            If matrix A is None
            
        OperationError
            If matrix A is not square or singular
        """
        try:
            if self.matrix_A is None:
                raise MatrixNoneError('A')
            if self.matrix_A.shape[0] != self.matrix_A.shape[1]:
                raise OperationError('Matrix is not square')
            if linalg.det(self.matrix_A) == 0:
                raise OperationError('Matrix is singular')
            
            self.matrix_R = linalg.inv(self.matrix_A)
            self.result_show('Invert A')

        except (OperationError, MatrixNoneError):
            return
       

    def matrix_A_eigvals(self) -> None:
        """
        Method for calculating eigenvalues of matrix A

        Raises
        ----------
        MatrixNoneError
            If matrix A is None
            
        OperationError
            If matrix A is not square
        """
        try:
            if self.matrix_A is None:
                raise MatrixNoneError('A')
            if self.matrix_A.shape[0] != self.matrix_A.shape[1]:
                raise OperationError('Matrix is not square')
            
            self.matrix_R, _ = linalg.eig(self.matrix_A)
            self.result_show('Eigenvalues A')
            
        except (OperationError, MatrixNoneError):
            return
       

    def matrix_A_eigvect(self) -> None:
        """
        Method for calculating eigenvectors of matrix A

        Raises
        ----------
        MatrixNoneError
            If matrix A is None
            
        OperationError
            If matrix A is not square
        """
        try:
            if self.matrix_A is None:
                raise MatrixNoneError('A')
            if self.matrix_A.shape[0] != self.matrix_A.shape[1]:
                raise OperationError('Matrix is not square')
            
            _, self.matrix_R = linalg.eig(self.matrix_A)
            self.result_show('Eigenvectors A')
            
        except (OperationError, MatrixNoneError):
            return
        

    def matrix_A_jordan(self) -> None:
        eigvals, eigvects = linalg.eig(self.matrix_A)
        jordan = np.diag(eigvals)
        p = eigvects
        pinv = linalg.inv(eigvects)
        self.matrix_R_text.setPlainText('Matrix A Jordan\n' + 'P' + '\n' + str(
            p) + '\n' + 'J' + '\n' + str(jordan) + '\n' + 'P_inv' + '\n' + str(pinv))

    def matrix_B_det(self) -> None:
        try:
            if self.matrix_B.shape[0] != self.matrix_B.shape[1]:
                raise OperationError('Matrix is not square')
        except OperationError:
            return
        self.matrix_R = linalg.det(self.matrix_B)
        self.result_show('Determinant B')

    def matrix_B_transpose(self) -> None:
        self.matrix_R = np.transpose(self.matrix_B)
        self.result_show('Transpose B')

    def matrix_B_invert(self) -> None:
        self.matrix_R = linalg.inv(self.matrix_B)
        self.result_show('Invert B')

    def matrix_B_eigvals(self) -> None:
        self.matrix_R, _ = linalg.eig(self.matrix_B)
        self.result_show('Eigenvalues B')

    def matrix_B_eigvect(self) -> None:
        _, self.matrix_R = linalg.eig(self.matrix_B)
        self.result_show('Eigenvectors B')

    def matrix_B_jordan(self) -> None:
        eigvals, eigvects = linalg.eig(self.matrix_B)
        jordan = np.diag(eigvals)
        p = eigvects
        pinv = linalg.inv(eigvects)
        self.matrix_R_text.setPlainText('Matrix B Jordan\n' + 'P' + '\n' + str(
            p) + '\n' + 'J' + '\n' + str(jordan) + '\n' + 'P_inv' + '\n' + str(pinv))

    def result_show(self, message: str) -> None:
        """
        Method for updating result view

        Parameters
        ----------
        message : str 
            A message that appears above the result.
        """

        m_str = np.array2string(self.matrix_R, formatter={'complexfloat': complex_to_string,
                                                          'float': complex_to_string})
        
        self.matrix_R_text.setPlainText(message + '\n' + m_str)

    def back_to_menu(self) -> None:
        """
        Method for going back to main menu
        """
        self.close()
        self.parent.show()

    def center(self) -> None:
        """
        Method for centering windows
        """
        qr = self.frameGeometry()
        cp = self.screen().availableGeometry().center()

        qr.moveCenter(cp)
        self.move(qr.topLeft())


def complex_to_string(c):
    if c.imag == 0 and c.real != 0:
        return '{0.real:.4f}'.format(c)
    elif c.real == 0 and c.imag != 0:
        return '{0.imag:.4f}j'.format(c)
    elif c.real == 0 and c.imag == 0:
        return '  0 '
    else:
        return '{0.real:.4f}+{0.imag:.4f}j'.format(c)


class OperationError(Exception):
    """
    Class for operation error
    """

    def __init__(self, msg: str) -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        message_box.setText(msg)
        print("Input empty")
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")


class MatrixNoneError(Exception):
    """
    Class for none matrix exception
    """

    def __init__(self, flag: str='AB') -> None:
        super().__init__()
        message_box = QMessageBox()
        message_box.setWindowTitle("ERROR")
        if flag == 'A':
            message_box.setText('Matrix A is None')
        elif flag == 'B':
            message_box.setText('Matrix B is None')
        else:
            message_box.setText('Matrix A or B is None')
        print("Input empty")
        result = message_box.exec()
        if result == QMessageBox.StandardButton.Ok:
            print("Error closed")
