from db_connect import Dbconnect
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_connection = None
        self.initializeUI()


    def initializeUI(self):
        self.setGeometry(300, 200, 500, 500)
        self.setWindowTitle("app")
        self.setUpMainWindow()
        self.show()


    def setUpMainWindow(self):

        layout = QVBoxLayout()

        #кнопка подключения к БД
        self.connect_to_db_button = QPushButton('Подключение к БД')
        self.connect_to_db_button.clicked.connect(self.check_and_connect_db)
        layout.addWidget(self.connect_to_db_button)

        #кнопка вставки данных
        self.insert_data_button = QPushButton('Вставка данных')
        self.insert_data_button.clicked.connect(self.insert_data)
        self.insert_data_button.setVisible(False)
        layout.addWidget(self.insert_data_button)
        
        layout.addStretch()
        self.setLayout(layout)


    def check_and_connect_db(self):
        self.db_connection = Dbconnect()
        if self.db_connection.test_connection() is True:
            QMessageBox.information(self, "Успех" ,"Подключение к БД успешно установлено!")
            self.connect_to_db_button.setEnabled(False)
            self.insert_data_button.setVisible(True)

        else:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
            self.db_connection = None


    def insert_data(self):
        if self.db_connection is None:
            QMessageBox.critical(self, "Ошибка",  "Нет подключения к БД")
            return

        try:
            succes = self.db_connection.alter_table()
            if succes is True:
                QMessageBox.information(self, "Успех", "Вставка прошла успешно")

            else:
                QMessageBox.critical(self, "Ошибка", "Ошибка при вставке данных!")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")         

    def closeEvent(self, event):
        if self.db_connection:
            self.db_connection.close_connect()
        event.accept()



app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec())
sys.dont_write_bytecode = True