import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout,
                             QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt


class Calculator:
    """
    The Model: Handles the core logic of the calculator.
    """
    def __init__(self):
        """
        Initializes the Calculator object with an empty expression.
        """
        self.expression = ""

    def add_to_expression(self, char: str):
        """
        Adds a new character (e.g., digit, operator) to the current expression.

        Args:
            char (str): A single character to append to the expression.
        """
        self.expression += char

    def remove_last_character(self):
        """
        Removes the last character from the current expression.
        """
        self.expression = self.expression[:-1]

    def clear_expression(self):
        """
        Clears the entire expression, setting it back to an empty string.
        """
        self.expression = ""

    def calculate(self):
        """
        Evaluates the current mathematical expression and returns the result.

        Returns:
            A numeric result (int or float) if the expression is valid.
            A string error message if the expression is invalid or malformed (e.g., division by zero).
        """
        try:
            result = eval(self.expression)
            return result
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception:
            return "Error: Invalid expression"

    def get_expression(self):
        """
        Returns the current mathematical expression stored in expression.

        Returns:
            str: The current expression as a string.
        """
        return self.expression


class CalculatorWindow(QMainWindow):
    """
    The Controller: Manages the GUI (View) and interacts with the Model (Calculator).
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setGeometry(100, 100, 300, 400)

        self.calculator = Calculator()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.input_field = QLineEdit()
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setReadOnly(True)
        self.input_field.setFont(self.input_field.font())  # Ensure font is initialized
        font = self.input_field.font()
        font.setPointSize(20)
        self.input_field.setFont(font)
        self.layout.addWidget(self.input_field)

        self.buttons_layout = QGridLayout()

        # Define button labels
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        row = 1
        col = 0
        for button_text in buttons:
            button = QPushButton(button_text)
            button.setFixedSize(70, 70)
            button.setFont(font)
            button.clicked.connect(self.on_button_click)
            self.buttons_layout.addWidget(button, row, col)
            col += 1
            if col > 3:
                col = 0
                row += 1

        self.clear_button = QPushButton("C")
        self.clear_button.setFixedSize(70, 70)
        self.clear_button.setFont(font)
        self.clear_button.clicked.connect(self.clear_input)
        self.buttons_layout.addWidget(self.clear_button, 0, 0, 1, 1)

        self.backspace_button = QPushButton("<-")
        self.backspace_button.setFixedSize(70, 70)
        self.backspace_button.setFont(font)
        self.backspace_button.clicked.connect(self.backspace)
        self.buttons_layout.addWidget(self.backspace_button, 0, 1, 1, 1)

        # Empty space for layout consistency
        empty_button = QWidget()
        empty_button.setFixedSize(70, 70)
        self.buttons_layout.addWidget(empty_button, 0, 2, 1, 1)

        empty_button_2 = QWidget()
        empty_button_2.setFixedSize(70, 70)
        self.buttons_layout.addWidget(empty_button_2, 0, 3, 1, 1)


        self.layout.addLayout(self.buttons_layout)
        self.central_widget.setLayout(self.layout)

    def on_button_click(self):
        sender = self.sender()
        button_text = sender.text()

        if button_text == "=":
            result = self.calculator.calculate()
            self.input_field.setText(str(result))
            self.calculator.expression = str(result) # Update model with result for potential further calculations
        else:
            self.calculator.add_to_expression(button_text)
            self.input_field.setText(self.calculator.get_expression())

    def clear_input(self):
        self.calculator.clear_expression()
        self.input_field.clear()

    def backspace(self):
        self.calculator.remove_last_character()
        self.input_field.setText(self.calculator.get_expression())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.show()
    sys.exit(app.exec_())