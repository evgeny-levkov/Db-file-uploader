from PyQt6.QtCore import pyqtSignal
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget, QComboBox, QFileDialog, QGridLayout
import pandas as pd

class OperationScreen(QWidget):

    escape = pyqtSignal()
    load = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.load_data = QWidget()
        self.form_report = QWidget()
        self.file = None

        self.stacked_widget.addWidget(self.load_data)
        self.stacked_widget.addWidget(self.form_report)

        self.initlUi()


    def initlUi(self):
        self.main_loyuot = QVBoxLayout()
        self.button_loyout = QHBoxLayout()

        self.load_data_button = QPushButton("Загрузка файлов операций\nЗагрузка XLSX-файлов, ETL-валидация, запись в БД")
        self.load_data_button.setProperty("class", "upload")
        self.form_report_button = QPushButton("Сформировать отчёт\nАналитика, прогнозы, экспорты PDF, CSV, PNG")
        self.form_report_button.setProperty("class", "upload")
        self.load_data_button.clicked.connect(self.show_load_data)
        self.form_report_button.clicked.connect(self.show_form_report)
        self.button_loyout.addWidget(self.load_data_button)
        self.button_loyout.addWidget(self.form_report_button)
        
        #Загрузка файлов и операций
        self.load_data_loyuot = QVBoxLayout()
        self.form_report_loyout = QVBoxLayout()

        self.label1 = QLabel("📎 Загрузка файлов операций")
        self.label1.setProperty("class", "label6")

        self.label2 = QLabel("Выберите тип продукта и приложите XLSX-файл (соответствует Приложению 2 – модель данных)")
        self.label2.setWordWrap(False)
        self.label2.setProperty("class", "label7")

        self.label3 = QLabel("Тип данных / продукт")
        self.label3.setProperty("class", "label7")

        self.list1 = QComboBox()
        self.list1.addItem("bill_bbk")
        self.list1.addItem("bill_maas_mgt")
        self.list1.addItem("bill_maas_mm")
        self.list1.addItem("bill_maas_ppk")
        self.list1.addItem("bill_vt")
        self.list1.addItem("prosmotr_prohodov_maas_mgt")
        self.list1.addItem("prosmotr_prohodov_maas_mm")
        self.list1.addItem("prosmotr_prohodov_maas_ppk")
        self.list1.addItem("prosmotr_prohodov_vt")
        self.list1.addItem("reestr_prodaj_maas")
        self.list1.addItem("reestr_prodaj_vt")
        self.list1.addItem("sessii_prodaj_maas")
        self.list1.addItem("sessii_prodaj_vt")
        self.list1.setProperty("class", "QComboBox")
        self.list1.setCurrentIndex(0)
        self.list1.update()

        self.label4 = QLabel("Выберите XLSX-файл")
        self.label4.setProperty("class", "label7")


        # self.open_file_loyuot = QHBoxLayout()
        self.open_file_button = QPushButton("Выбрать файл")
        self.open_file_button.clicked.connect(self.open_file)

        self.upload_button = QPushButton("Загрузить")
        self.upload_button.clicked.connect(self.upload_db)
        #self.upload_button.setMinimumWidth(10)

        self.file_name = QLabel("Файл не выбран")
        self.file_name.setProperty("class", "label7")

        # self.open_file_loyuot.addWidget(self.open_file_button)
        # self.open_file_loyuot.addWidget(self.file_name)
        self.open_file_loyuot = QGridLayout()
        self.open_file_loyuot.addWidget(self.open_file_button, 0, 0)
        self.open_file_loyuot.addWidget(self.file_name, 0, 1)
        self.open_file_loyuot.setColumnStretch(0, 2)
        self.open_file_loyuot.setColumnStretch(1, 6)
        self.null_widget = QLabel()
        self.null_widget.setMinimumHeight(10)
        self.open_file_loyuot.addWidget(self.null_widget, 1, 0)
        self.open_file_loyuot.setRowStretch(1, 10)
        
        self.upload_button_louout = QHBoxLayout()
        self.null_coll0 = QLabel()
        self.null_coll2 = QLabel()

        self.upload_button_louout.addWidget(self.upload_button, 2)
        self.upload_button_louout.addWidget(self.null_coll0, 3)
        self.upload_button_louout.addWidget(self.null_coll2, 3)

        # self.open_file_loyuot.addWidget(self.upload_button, 1, 2)
        self.open_file_loyuot.addLayout(self.upload_button_louout, 2, 0, 1, 2)


        self.load_data_loyuot.addWidget(self.label1)
        self.load_data_loyuot.addWidget(self.label2)
        self.load_data_loyuot.addWidget(self.label3) 
        self.load_data_loyuot.addWidget(self.list1)
        self.load_data_loyuot.addWidget(self.label4)
        self.load_data_loyuot.addLayout(self.open_file_loyuot)

        #self.load_data_loyuot.addWidget(self.upload_button)
        
        self.load_data_loyuot.addStretch(0)

        #Сформировать отчёт
        self.label5 = QLabel("📑 Параметры отчёта")
        self.label5.setProperty("class", "label7")
        self.form_report_loyout.addWidget(self.label5)


        self.load_data.setLayout(self.load_data_loyuot)
        self.form_report.setLayout(self.form_report_loyout)

        self.esc_button = QPushButton("Назад")
        self.esc_button.clicked.connect(self.go_to_screen1)

        self.main_loyuot.addLayout(self.button_loyout)
        self.main_loyuot.addWidget(self.stacked_widget)
        self.main_loyuot.addStretch()
        self.main_loyuot.addWidget(self.esc_button)
        self.setLayout(self.main_loyuot)

        
    def show_load_data(self):
        self.stacked_widget.setCurrentIndex(0)


    def show_form_report(self):
        self.stacked_widget.setCurrentIndex(1)


    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите XLSX файл", "", "Excel (*.xlsx)")

        if file_path:
            try:
                self.file = pd.read_excel(file_path)
                self.file_name.setText(file_path.split("/")[-1])

            except:
                self.file_name.setText("Ошибка при чтении файла")
                self.file = None
       

    def upload_db(self):
        if self.file is not None:
            self.load.emit((self.file, self.list1.currentText()))


    def go_to_screen1(self):
        self.escape.emit()