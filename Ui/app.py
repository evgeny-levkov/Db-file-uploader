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

        self.connectionviewmodel.success.connect(self.HandleSuccess)
        self.operationScreen.escape.connect(self.HandleEscape)        

        self.InitializeUI() 


    def InitializeUI(self):
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


    def HandleSuccess(self, sucess):
        if sucess == "Ошибка подключения к БД":
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")

        elif sucess == "Критическая ошибка":
            QMessageBox.critical(self, "Ошибка", "Критическая ошибка")

        elif sucess == None:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")

        else:
            self.operationScreen.upload_button.setEnabled(True)
            self.operationScreen.load_progress.setVisible(False)
            self.operationviewmodel.service = sucess
            self.stacked_widget.setCurrentIndex(1)


    def HandleEscape(self):
        self.stacked_widget.setCurrentIndex(0)


    @staticmethod
    def LoadStylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""