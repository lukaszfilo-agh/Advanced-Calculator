from PyQt6.QtWidgets import (
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QDialog,
    QLineEdit
)

from PyQt6.QtCore import Qt, QEvent

import matplotlib
matplotlib.use('QtAgg')

# Class for input dialog
class PlotInputDialog(QDialog):
    def __init__(self):
        super().__init__()
        # Calling function to initialize UI
        self.init_ui()

    def init_ui(self):
        # Setting window title
        self.setWindowTitle('Enter Data')
        # Setting window size
        self.resize(500, 500)

        # Creating main layout
        main_layout = QVBoxLayout()

        # Input fields list
        self.input_fields = [
            CustomLineEdit(),  # Function input
            CustomLineEdit(),  # Lower limit input
            CustomLineEdit()  # Upper limit input
        ]

        # Input fields labels
        labels_text = ['f(x):', 'Lower limit:', 'Upper limit:']

        self.input_fields[0].installEventFilter(self)
        self.input_fields[1].installEventFilter(self)
        self.input_fields[2].installEventFilter(self)

        self.input_fields[0].mousePressEvent = lambda e: self.switch_func_keyboard()
        self.input_fields[1].mousePressEvent = lambda e: self.switch_lower_lim_keyboard()
        self.input_fields[2].mousePressEvent = lambda e: self.switch_upper_lim_keyboard()

        for i in range(len(self.input_fields)):
            label = QLabel(labels_text[i])
            main_layout.addWidget(label)
            main_layout.addWidget(self.input_fields[i])

        # Layout for keyboard buttons
        self.buttons_layout = QVBoxLayout()
        main_layout.addLayout(self.buttons_layout)

        # Creating keyboards
        self.keyboards = [
            [  # Keyboard for function
                ['*', '/', 'sin()', 'cos()'],
                ['+', '-', 'tg()', 'ctg()'],
                ['.', '^', 'arcsin()', 'arccos()'],
                ['(', ')', 'arctg()', ' '],
                ['π', 'e', '| |', 'sqrt()'],
                ['x', ' ', '<-', 'C']
            ],
            [  # Keyboard for lower limit
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', ' '],
                ['+', '-', '<-', 'C']
            ],
            [  # Keyboard for upper limit
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                [' ', ' ', ' ', ' '],
                ['π', 'e', '.', ' '],
                ['+', '-', '<-', 'C']
            ]
        ]

        # Button for drawing plot
        button_draw_plot = QPushButton('Draw plot')
        button_draw_plot.clicked.connect(self.accept)
        button_draw_plot.setShortcut(Qt.Key.Key_Return)

        main_layout.addWidget(button_draw_plot)

        # Setting main_layout as dialog layout
        self.setLayout(main_layout)

        self.active_field = 0
        self.update_keyboard()

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.KeyPress and obj in self.input_fields:
            if event.key() == Qt.Key.Key_Tab:
                active_index = self.input_fields.index(obj)
                if active_index == 2:
                    self.active_field = 0
                else:
                    self.active_field = active_index + 1
            self.update_keyboard()
        return super().eventFilter(obj, event)

    def switch_func_keyboard(self):
        self.active_field = 0
        self.update_keyboard()

    def switch_lower_lim_keyboard(self):
        self.active_field = 1
        self.update_keyboard()

    def switch_upper_lim_keyboard(self):
        self.active_field = 2
        self.update_keyboard()

    def on_button_clicked(self):
        clicked_button = self.sender()
        text = clicked_button.text()

        if text == 'C':
            self.input_fields[self.active_field].clear()
        elif text == '<-':
            current_text = self.input_fields[self.active_field].text()
            new_text = current_text[:-1]
            self.input_fields[self.active_field].setText(new_text)
        elif text == ' ':
            pass
        else:
            current_text = self.input_fields[self.active_field].text()
            new_text = current_text + text
            self.input_fields[self.active_field].setText(new_text)

    def update_keyboard(self):
        # Deleting buttons
        for i in reversed(range(self.buttons_layout.count())):
            layout = self.buttons_layout.itemAt(i).layout()
            if layout is not None:
                for j in reversed(range(layout.count())):
                    layout.itemAt(j).widget().deleteLater()
                self.buttons_layout.removeItem(layout)

        # Adding buttons
        for row in self.keyboards[self.active_field]:
            row_layout = QHBoxLayout()
            for button_text in row:
                button = QPushButton(button_text)
                button.setFixedSize(100, 40)
                button.clicked.connect(self.on_button_clicked)
                row_layout.addWidget(button)
            self.buttons_layout.addLayout(row_layout)

    def getInputs(self):
        return tuple(input.text() for input in self.input_fields)

# Class for custom line edit with keyboard filtering
class CustomLineEdit(QLineEdit):
    def __init__(self):
        super().__init__()

    def keyPressEvent(self, event):
        allowed_keys = [Qt.Key.Key_Backspace,
                        Qt.Key.Key_Left,
                        Qt.Key.Key_Right,
                        Qt.Key.Key_X,
                        Qt.Key.Key_Minus,
                        Qt.Key.Key_Plus,
                        47,  # '/'
                        94,  # '^'
                        40,  # '('
                        41  # ')'
                        ]
        print(event.key())
        if event.text().isdigit() or event.key() in allowed_keys:
            super().keyPressEvent(event)
