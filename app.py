from db_connect import Dbconnect
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout, QHBoxLayout, QLabel
import sys
import os


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.connectionScreen = QWidget()
        self.operationScreen = QWidget() 
        self.initializeUI()


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

        mainLayout = QVBoxLayout()
        layout = QHBoxLayout()

        self.label1 = QLabel("🚇 Финансовые сверки")
        self.label1.setProperty("class", "label1")

        self.label2 = QLabel("· Московский метрополитен")
        self.label2.setProperty("class", "label2")

        self.label3 = QLabel("Загрузка данных, ETL-обработка, формирование отчётов и аналитика")
        self.label3.setProperty("class", "label3")

        layout.setSpacing(5)
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.label3)
        mainLayout.addStretch()
        self.setLayout(mainLayout)

        # #кнопка подключения к БД
        # self.connect_to_db_button = QPushButton('Подключение к БД')
        # self.connect_to_db_button.clicked.connect(self.check_and_connect_db)
        # layout.addWidget(self.connect_to_db_button)

        # #кнопка вставки данных
        # self.insert_data_button = QPushButton('Вставка данных')
        # self.insert_data_button.clicked.connect(self.insert_data)
        # self.insert_data_button.setVisible(False)
        # layout.addWidget(self.insert_data_button)
        
        # layout.addStretch()
        # self.setLayout(layout)


    # def check_and_connect_db(self):
    #     self.db_connection = Dbconnect()
    #     if self.db_connection.test_connection() is True:
    #         QMessageBox.information(self, "Успех" ,"Подключение к БД успешно установлено!")
    #         self.connect_to_db_button.setEnabled(False)
    #         self.insert_data_button.setVisible(True)

    #     else:
    #         QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
    #         self.db_connection = None


    # def insert_data(self):
    #     if self.db_connection is None:
    #         QMessageBox.critical(self, "Ошибка",  "Нет подключения к БД")
    #         return

    #     try:
    #         succes = self.db_connection.alter_table()
    #         if succes is True:
    #             QMessageBox.information(self, "Успех", "Вставка прошла успешно")

    #         else:
    #             QMessageBox.critical(self, "Ошибка", "Ошибка при вставке данных!")

    #     except Exception as e:
    #         QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")         

    # def closeEvent(self, event):
    #     if self.db_connection:
    #         self.db_connection.close_connect()
    #     event.accept()

    @staticmethod
    def load_stylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""



if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Загружаем стили ПЕРЕД созданием окна
    stylesheet = MainWindow.load_stylesheet("style.css")
    if stylesheet:
        app.setStyleSheet(stylesheet)
        print("✅ Стили загружены")
    else:
        print("⚠️ Файл style.css не найден")
    
    window = MainWindow()
    sys.exit(app.exec())

sys.dont_write_bytecode = True