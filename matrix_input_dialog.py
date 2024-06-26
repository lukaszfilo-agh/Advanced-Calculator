import numpy as np
import re
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QGridLayout,
    QDialog,
    QPushButton,
    QMessageBox
)
from PyQt6.QtCore import Qt


class MatrixInputDialog(QDialog):
    # Class for matrix input dialog
    def __init__(self) -> None:
        super().__init__()
        # Calling function to initialize UI
        self.init_ui()

    def init_ui(self) -> None:
        # Setting window title
        self.setWindowTitle('Enter Matrix')
        # Setting window size
        self.setFixedSize(400, 400)

        # Create label and input for rows
        rows_label = QLabel('Enter number of rows:')
        self.rows_input = RowColLineEdit()

        # Create layout for rows input
        rows_input_layout = QHBoxLayout()
        rows_input_layout.addWidget(rows_label)
        rows_input_layout.addWidget(self.rows_input)

        # Create label and input for columns
        cols_label = QLabel('Enter number of columns:')
        self.cols_input = RowColLineEdit()

        # Create button for saving size of matrix
        next_button = QPushButton('Proceed')
        next_button.clicked.connect(self.__update_matrix)

        # Create accept button
        done_button = QPushButton('Save')
        done_button.clicked.connect(self.accept)
        done_button.setShortcut(Qt.Key.Key_Return)

        # Create layout for columns input
        cols_input_layout = QHBoxLayout()
        cols_input_layout.addWidget(cols_label)
        cols_input_layout.addWidget(self.cols_input)

        # Creating lists for matrix labels and inputs
        self.matrix_labels = []
        self.matrix_inputs = []
        self.conv_matrix = []

        # Creating layout for showing matrix
        self.matrix_layout = QGridLayout()

        # Creating main layout
        main_layout = QVBoxLayout()

        # Adding layouts for rows and cols input
        main_layout.addLayout(rows_input_layout)
        main_layout.addLayout(cols_input_layout)

        # Adding proceed button to main layout
        main_layout.addWidget(next_button)

        # Adding matrix layout to main layout
        main_layout.addLayout(self.matrix_layout)

        # Adding save button to main layout
        main_layout.addWidget(done_button)

        # Setting layout for window
        self.setLayout(main_layout)

    def __update_matrix(self) -> None:
        try:
            if self.rows_input.text() == '' or self.cols_input.text() == '':
                raise EmptyInputError
            rows = int(self.rows_input.text())
            cols = int(self.cols_input.text())

            # Clear previous matrix widgets
            for i in reversed(range(self.matrix_layout.count())):
                self.matrix_layout.itemAt(i).widget().setParent(None)
            self.matrix_labels = []
            self.matrix_inputs = []

            # Create and display new matrix widgets
            for i in range(rows):
                row_labels = []
                row_inputs = []
                for j in range(cols):
                    # label = QLabel(f"[{i}][{j}]:")
                    input_field = MatrixInputLineEdit()
                    # self.matrix_layout.addWidget(label, i, j * 2)
                    self.matrix_layout.addWidget(input_field, i, j * 2 + 1)
                    # row_labels.append(label)
                    row_inputs.append(input_field)
                self.matrix_labels.append(row_labels)
                self.matrix_inputs.append(row_inputs)

        except EmptyInputError:
            return

        except ValueError:
            print('value error')

    def __read_matrix(self) -> None:
        for i, row_inputs in enumerate(self.matrix_inputs):
            row_values = []
            for j, input_field in enumerate(row_inputs):
                value = input_field.text()
                try:
                    if value == '':
                        raise EmptyInputError
                    res = re.findall(r'i', value)
                    if len(res) != 0:
                        value = value.replace('i', 'j')
                        value = complex(value)
                    else:
                        value = float(value)
                except EmptyInputError:
                    self.conv_matrix = None
                    return
                row_values.append(value)
            self.conv_matrix.append(row_values)

    def getInputs(self):
        self.__read_matrix()
        if self.conv_matrix is None:
            return None
        else:
            return np.array(self.conv_matrix)


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


class RowColLineEdit(QLineEdit):
    # Class for custom line edit with keyboard filtering for Rows and Cols
    def __init__(self) -> None:
        super().__init__()

    def keyPressEvent(self, event) -> None:
        allowed_keys = [Qt.Key.Key_Backspace,
                        Qt.Key.Key_Left,
                        Qt.Key.Key_Right
                        ]
        print(event.key())
        if event.text().isdigit() or event.key() in allowed_keys:
            super().keyPressEvent(event)


class MatrixInputLineEdit(QLineEdit):
    # Class for custom line edit with keyboard filtering for matrix input
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        allowed_keys = [Qt.Key.Key_Backspace,
                        Qt.Key.Key_Left,
                        Qt.Key.Key_Right,
                        Qt.Key.Key_I,
                        Qt.Key.Key_Minus,
                        46  # '.'
                        ]
        print(event.key())
        if event.text().isdigit() or event.key() in allowed_keys:
            super().keyPressEvent(event)
