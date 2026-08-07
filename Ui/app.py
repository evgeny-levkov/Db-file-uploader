from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from Ui.ConnectWindow import ConnectionScreen
from Ui.OperationWindow import OperationScreen
from Viewmodel.ConnectionViewModel import ConnectionViewModel
from Viewmodel.OperationViewModel import OperationViewModel
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.connectionviewmodel = ConnectionViewModel()
        self.connectionScreen = ConnectionScreen(self.connectionviewmodel)
        self.operationviewmodel = OperationViewModel()
        self.operationScreen = OperationScreen(self.operationviewmodel)
        self.stacked_widget.addWidget(self.connectionScreen)
        self.stacked_widget.addWidget(self.operationScreen)
        self.connectionviewmodel.success.connect(self.handle_success)
        self.operationScreen.escape.connect(self.handle_escape)
        self.initialize_ui()

    def initialize_ui(self):
        self.setGeometry(300, 200, 1200, 1000)
        self.setWindowTitle("App")

        # настройка окна
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(palette)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.stacked_widget)
        self.setLayout(windowLayout)
        self.stacked_widget.setCurrentIndex(0)

        self.show()

    def handle_success(self, success):
        if success == "Ошибка подключения к БД":
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
        elif success == "Критическая ошибка":
            QMessageBox.critical(self, "Ошибка", "Критическая ошибка")
        elif success is None:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
        else:
            self.operationScreen.upload_button.setEnabled(True)
            self.operationScreen.load_progress.setVisible(False)
            self.operationviewmodel.service = success
            self.stacked_widget.setCurrentIndex(1)

    def handle_escape(self):
        self.stacked_widget.setCurrentIndex(0)

    @staticmethod
    def load_stylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""