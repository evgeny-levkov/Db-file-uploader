from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel

class OperationScreen(QWidget):  

    escape = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initlUi()

    def initlUi(self):
        self.loyuot1 = QVBoxLayout()

        self.new = QLabel("Новое окно")
        self.new.setProperty("class", "label5")

        self.loyuot1.addWidget(self.new)

        self.esc_button = QPushButton("назад")
        self.esc_button.setProperty("class", "QPushButton")
        self.esc_button.clicked.connect(self.go_to_screen1)

        self.loyuot1.addWidget(self.esc_button)

        self.setLayout(self.loyuot1)

    def go_to_screen1(self):
        self.escape.emit()