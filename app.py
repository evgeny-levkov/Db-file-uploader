from db_connect import Dbconnect
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QStackedWidget
import sys
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.stacked_widget = QStackedWidget()
        self.connectionScreen = QWidget()
        # self.operationScreen = QWidget() 
        #self.stacked_widget.addWidget(self.connectionScreen)
        #self.stacked_widget.addWidget(self.operationScreen)
        self.initializeUI()
        self.db_connect = None


    def initializeUI(self):
        self.setGeometry(300, 200, 1200, 1000)
        self.setWindowTitle("App")
        self.setUpMainWindow()
        self.show()


    def setUpMainWindow(self):
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(palette)

        #Верхние надписи
        mainLayout = QVBoxLayout()
        upperLayout = QHBoxLayout()

        self.label1 = QLabel("🚇 Финансовые сверки")
        self.label1.setProperty("class", "label1")

        self.label2 = QLabel("· Московский метрополитен")
        self.label2.setProperty("class", "label2")

        self.label3 = QLabel("Загрузка данных, ETL-обработка, формирование отчётов и аналитика")
        self.label3.setProperty("class", "label3")

        upperLayout.setSpacing(5)
        upperLayout.addWidget(self.label1)
        upperLayout.addWidget(self.label2)
        upperLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        mainLayout.addLayout(upperLayout)
        mainLayout.addWidget(self.label3) 

        # Поля для ввода подключения

        mainlowerLoyout = QVBoxLayout()

        lowerLoyout1 = QHBoxLayout()
        lowerLoyout2 = QHBoxLayout()
        lowerLoyout3 = QHBoxLayout()
        lowerLoyout4 = QHBoxLayout()
        lowerLoyout5 = QHBoxLayout()
        lowerLoyout6 = QHBoxLayout()
        lowerLoyout7 = QHBoxLayout()

        self.params = QLabel("🔌 Параметры подключения к PostgreSQL")
        self.params.setProperty("class", "label5")
        mainlowerLoyout.addWidget(self.params)

        self.host = QLabel("Хост / сервер")
        self.host.setProperty("class", "label4")
        self.field_host = QLineEdit()
        lowerLoyout1.addWidget(self.host)
        lowerLoyout2.addWidget(self.field_host)

        self.port = QLabel("Порт")
        self.port.setProperty("class", "label4")
        self.field_port = QLineEdit()
        self.field_host.setProperty("class", "QLineEdit")
        lowerLoyout1.addWidget(self.port)
        lowerLoyout2.addWidget(self.field_port)  

        self.name_db = QLabel("Имя базы днных")
        self.name_db.setProperty("class", "label4")
        self.field_name_db = QLineEdit()
        self.field_name_db.setProperty("class", "QLineEdit")
        lowerLoyout3.addWidget(self.name_db)
        lowerLoyout4.addWidget(self.field_name_db) 

        self.user = QLabel("Пользователь")
        self.user.setProperty("class", "label4")
        self.field_user = QLineEdit()
        self.field_user.setProperty("class", "QLineEdit")
        lowerLoyout3.addWidget(self.user)
        lowerLoyout4.addWidget(self.field_user) 

        self.password = QLabel("Пароль")
        self.password.setProperty("class", "label4")
        self.spacer1 = QWidget()
        self.spacer2 = QWidget()
        self.field_password = QLineEdit()
        self.field_password.setProperty("class", "QLineEdit")
        lowerLoyout5.addWidget(self.password, 1)
        lowerLoyout5.addWidget(self.spacer1, 1)
        lowerLoyout6.addWidget(self.field_password, 1) 
        lowerLoyout6.addWidget(self.spacer2, 1)

        self.connect_button = QPushButton("Проверить подключение")
        self.connect_button.setProperty("class", "QPushButton")
        self.connect_button.clicked.connect(self.connect_db)
        lowerLoyout7.addWidget(QWidget(), 1)
        lowerLoyout7.addWidget(self.connect_button, 2)
        lowerLoyout7.addWidget(QWidget(), 1)       

        mainlowerLoyout.addLayout(lowerLoyout1)
        mainlowerLoyout.addLayout(lowerLoyout2)  
        mainlowerLoyout.addLayout(lowerLoyout3)
        mainlowerLoyout.addLayout(lowerLoyout4) 
        mainlowerLoyout.addLayout(lowerLoyout5)
        mainlowerLoyout.addLayout(lowerLoyout6)
        mainlowerLoyout.addLayout(lowerLoyout7)    
        mainLayout.addLayout(mainlowerLoyout)

        #mainLayout.addWidget(self.connectionButton)
        mainLayout.addStretch()
        self.connectionScreen.setLayout(mainLayout)
        # self.stacked_widget.setCurrentWidget(self.connectionScreen)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.connectionScreen)
        self.setLayout(windowLayout)


    def connect_db(self):
        try:
            self.db_connect = Dbconnect(self.field_user.text(), self.field_password.text(), self.field_host.text(), self.field_port.text(), self.field_name_db.text())
            if self.db_connect.test_connection() is True:
                QMessageBox.information(self, "Успех", "Подключение к БД прошло успешно")
                return
            else:
                QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
                self.db_connection = None

        except:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")


    @staticmethod
    def load_stylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    stylesheet = MainWindow.load_stylesheet("style.css")
    if stylesheet:
        app.setStyleSheet(stylesheet)
        print("✅")
    else:
        print("⚠️")
    
    window = MainWindow()
    sys.exit(app.exec())

sys.dont_write_bytecode = True