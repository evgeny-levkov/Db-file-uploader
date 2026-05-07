from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox
from Ui.connectWindow import ConnectionScreen
from Ui.operationWindow import OperationScreen
from Service.db_service import DbService
from Service.worker import Worker
from PyQt6.QtCore import QThread
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
        self.operationScreen.load.connect(self.handle_load)
        
        self.service = None
        self.worker = None
        self.config = None
        self.thread: QThread = None

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
            self.config = config
            self.service = DbService(config)
            if self.service.test_connection():
                self.stacked_widget.setCurrentIndex(1)
            else:
                QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
        except:
            QMessageBox.critical(self, "Ошибка", "Критическая ошибка")


    def handle_escape(self):
        self.stacked_widget.setCurrentIndex(0)


    def handle_load(self, data):
        
        if self.worker is None:
            self.thread = QThread()
            self.worker = Worker(data[0], data[1], self.config)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.do_work)
            self.thread.start()
            self.worker.finished.connect(self.finished_work)
        else:
            return False


    def finished_work(self, success):
        if success:
            QMessageBox.information(self, "Успех" ,"Вставка прошла успешно")
        else:
            QMessageBox.critical(self, "Ошибка" ,"Ошибка при вставке")
        self.thread.quit()
        self.thread.wait()
        self.worker = None
        self.thread = None



    @staticmethod
    def load_stylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""