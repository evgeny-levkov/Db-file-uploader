from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from Ui.connectWindow import ConnectionScreen
from Ui.operationWindow import OperationScreen
from Service.db_service import DbService
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.connectionScreen = ConnectionScreen()
        self.operationScreen = OperationScreen()

        self.stacked_widget.addWidget(self.connectionScreen)
        self.stacked_widget.addWidget(self.operationScreen)

        self.connectionScreen.success.connect(self.handle_success)
        self.operationScreen.escape.connect(self.handle_escape)

        self.initializeUI() 


    def initializeUI(self):
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


    def handle_success(self, config):
        if config is None:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
            return
        
        try:
            service = DbService(config)
            if service.test_connection():
                self.stacked_widget.setCurrentIndex(1)
                QMessageBox.information(self, "Успех", "Подключение к БД прошло успешно")
            else:
                QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
        except:
            QMessageBox.critical(self, "Критическая ошибка")

    def handle_escape(self):
        self.stacked_widget.setCurrentIndex(0)


    @staticmethod
    def load_stylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""