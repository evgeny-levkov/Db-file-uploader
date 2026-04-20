from Service.db_service import DbService
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QGridLayout, QSizePolicy

class ConnectionScreen(QWidget):

    success = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.initlUi()

    def initlUi(self):
        
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

        self.main_lower_box = QHBoxLayout()
        self.row = QGridLayout()

        self.host = QLabel("Хост / сервер")
        self.host.setProperty("class", "label4")
        self.field_host = QLineEdit()
        self.field_host.setProperty("class", "QLineEdit")

        self.port = QLabel("Порт")
        self.port.setProperty("class", "label4")
        self.field_port = QLineEdit()
        self.field_port.setProperty("class", "QLineEdit")

        self.name_db = QLabel("Имя базы днных")
        self.name_db.setProperty("class", "label4")
        self.field_name_db = QLineEdit()
        self.field_name_db.setProperty("class", "QLineEdit")

        self.user = QLabel("Пользователь")
        self.user.setProperty("class", "label4")
        self.field_user = QLineEdit()
        self.field_user.setProperty("class", "QLineEdit")

        self.password = QLabel("Пароль")
        self.password.setProperty("class", "label4")
        self.field_password = QLineEdit()
        self.field_password.setProperty("class", "QLineEdit")
        self.field_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.connect_button = QPushButton("Проверить подключение")
        self.connect_button.setProperty("class", "QPushButton")
        self.connect_button.clicked.connect(self.connect_db)


        self.row.addWidget(self.host, 0, 0)
        self.row.addWidget(self.field_host, 1, 0)

        self.row.addWidget(self.port, 0, 1)
        self.row.addWidget(self.field_port, 1, 1)

        self.row.addWidget(self.name_db, 2, 0)
        self.row.addWidget(self.field_name_db, 3, 0)

        self.row.addWidget(self.user, 2, 1)
        self.row.addWidget(self.field_user, 3, 1)

        self.row.addWidget(self.password, 4, 0)
        self.row.addWidget(self.field_password, 5, 0)    

        btn_container = QWidget()
        btn_layout = QHBoxLayout(btn_container)
        btn_layout.setContentsMargins(0, 0, 0, 0)
        self.connect_button.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Fixed
        )

        btn_layout.addStretch()
        btn_layout.addWidget(self.connect_button)
        btn_layout.addStretch()

        self.row.addWidget(btn_container, 6, 0, 2, 3)
        

        self.main_lower_box.addLayout(self.row) 

        mainLayout.addLayout(self.main_lower_box)
        mainLayout.addStretch()
        self.setLayout(mainLayout)
        

    def connect_db(self):
        if not self.field_user.text() or not self.field_password.text() or not self.field_host.text() or not self.field_port.text() or not self.field_name_db.text():
            self.success.emit(None)
            return
        
        config ={
            "user": self.field_user.text(),
            "password": self.field_password.text(),
            "host": self.field_host.text(),
            "port": self.field_port.text(),
            "db_name": self.field_name_db.text()
        }

        self.success.emit(config)
        