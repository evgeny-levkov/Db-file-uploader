from Service.db_service import DbService
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QStackedWidget
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.connectionScreen = QWidget()
        self.operationScreen = QWidget()

        self.stacked_widget.addWidget(self.connectionScreen)
        self.stacked_widget.addWidget(self.operationScreen)

        self.initializeUI() 
        self.db_service = None


    def initializeUI(self):
        self.setGeometry(300, 200, 1200, 1000)
        self.setWindowTitle("App")
        self.setUpConnectionWindow()
        self.setUpOperationWindow()

        # настройка окна()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), Qt.GlobalColor.white)
        self.setPalette(palette)

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.stacked_widget)
        self.setLayout(windowLayout)
        self.stacked_widget.setCurrentIndex(0)
        self.show()


    def setUpConnectionWindow(self):

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
        self.field_port.setProperty("class", "QLineEdit")
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
        self.field_password.setEchoMode(QLineEdit.EchoMode.Password)
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

        mainLayout.addStretch()
        self.connectionScreen.setLayout(mainLayout)


    def setUpOperationWindow(self):
        self.loyuot1 = QVBoxLayout()

        self.new = QLabel("Новое окно")
        self.new.setProperty("class", "label5")

        self.loyuot1.addWidget(self.new)

        self.esc_button = QPushButton("назад")
        self.esc_button.setProperty("class", "QPushButton")
        self.esc_button.clicked.connect(self.go_to_screen1)

        self.loyuot1.addWidget(self.esc_button)
        self.operationScreen.setLayout(self.loyuot1)

    def connect_db(self):
        config ={
            "user": self.field_user.text(),
            "password": self.field_password.text(),
            "host": self.field_host.text(),
            "port": self.field_port.text(),
            "db_name": self.field_name_db.text()
        }
        self.db_service = DbService(config)
        
        if self.db_service.test_connection():
            self.stacked_widget.setCurrentIndex(1)
            QMessageBox.information(self, "Успех", "Подключение к БД прошло успешно")
        else:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
            self.db_service = None


    def go_to_screen1(self):
        self.stacked_widget.setCurrentIndex(0)


    @staticmethod
    def load_stylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""
    


