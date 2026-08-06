from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget, QComboBox, 
                             QFileDialog, QGridLayout, QDateEdit, QProgressBar, QMessageBox)
from PyQt6.QtCore import QDate
from Viewmodel.OperationViewModel import OperationViewModel
import os
import shutil



class OperationScreen(QWidget):

    escape = pyqtSignal()
    load = pyqtSignal(tuple)
    do_report = pyqtSignal(dict)

    def __init__(self, viewmodel: OperationViewModel):
        super().__init__()
        self.viewmodel: OperationViewModel = viewmodel
        self.stacked_widget = QStackedWidget()
        self.load_data = QWidget()
        self.form_report = QWidget()
        self.file = None

        self.stacked_widget.addWidget(self.load_data)
        self.stacked_widget.addWidget(self.form_report)

        self.InitlUi()

        self.viewmodel.file_name.connect(self.file_name.setText)
        self.viewmodel.load_error.connect(self.LoadError)
        self.viewmodel.load_info.connect(self.LoadInfo)
        self.viewmodel.report_error.connect(self.ReportError)
        self.viewmodel.file_error.connect(self.FileError)
        self.viewmodel.report_success.connect(self.ReportSuccess)


    def InitlUi(self):
        self.main_loyuot = QVBoxLayout()
        self.button_loyout = QHBoxLayout()

        self.load_data_button = QPushButton("Загрузка файлов операций\nЗагрузка XLSX-файлов, ETL-валидация, запись в БД")
        self.load_data_button.setProperty("class", "upload")
        self.form_report_button = QPushButton("Сформировать отчёт\nАналитика, прогнозы, экспорты PDF, CSV, PNG")
        self.form_report_button.setProperty("class", "upload")
        self.load_data_button.clicked.connect(self.ShowLoadData)
        self.form_report_button.clicked.connect(self.ShowFormReport)
        self.load_data_button.setCheckable(True)
        self.form_report_button.setCheckable(True)
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

        self.list_tables = QComboBox()
        self.list_tables.addItem("bill_bbk")
        self.list_tables.addItem("bill_maas_mgt")
        self.list_tables.addItem("bill_maas_mm")
        self.list_tables.addItem("bill_maas_ppk")
        self.list_tables.addItem("bill_vt")
        self.list_tables.addItem("prosmotr_prohodov_maas_mgt")
        self.list_tables.addItem("prosmotr_prohodov_maas_mm")
        self.list_tables.addItem("prosmotr_prohodov_maas_ppk")
        self.list_tables.addItem("prosmotr_prohodov_vt")
        self.list_tables.addItem("reestr_prodaj_maas")
        self.list_tables.addItem("reestr_prodaj_vt")
        self.list_tables.addItem("sessii_prodaj_maas")
        self.list_tables.addItem("sessii_prodaj_vt")
        self.list_tables.setProperty("class", "QComboBox")
        self.list_tables.setCurrentIndex(0)
        self.list_tables.update()

        self.label4 = QLabel("Выберите XLSX-файл")
        self.label4.setProperty("class", "label7")

        self.open_file_button = QPushButton("Выбрать файл")
        self.open_file_button.clicked.connect(self.OpenFile)

        self.upload_button = QPushButton("Загрузить")
        self.upload_button.clicked.connect(self.UploadDb)
        self.load_progress = QProgressBar(self)
        self.load_progress.setVisible(False)

        self.file_name = QLabel("Файл не выбран")
        self.file_name.setProperty("class", "label7")

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
        self.open_file_loyuot.addLayout(self.upload_button_louout, 2, 0, 1, 2)

        self.load_data_loyuot.addWidget(self.label1)
        self.load_data_loyuot.addWidget(self.label2)
        self.load_data_loyuot.addWidget(self.label3) 
        self.load_data_loyuot.addWidget(self.list_tables)
        self.load_data_loyuot.addWidget(self.label4)
        self.load_data_loyuot.addLayout(self.open_file_loyuot)
        self.load_data_loyuot.addWidget(self.load_progress)
        
        self.load_data_loyuot.addStretch(0)


        #Сформировать отчёт
        self.label5 = QLabel("📑 Параметры отчёта")
        self.label5.setProperty("class", "label6")

        self.label6 = QLabel("Продукт / раздел")
        self.label6.setProperty("class", "label7")

        self.list_bank_propucts = QComboBox()
        self.list_bank_propucts.setProperty("class", "QComboBox")
        self.list_bank_propucts.addItem("Банковские карты")
        self.list_bank_propucts.addItem("Маас ММ")
        self.list_bank_propucts.addItem("Маас НГПТ")
        self.list_bank_propucts.addItem("Маас ППК")

        self.label7 = QLabel("Период с")
        self.label7.setProperty("class", "label7")

        self.date_from = QDateEdit(QDate.currentDate())
        self.date_from.setCalendarPopup(True)
        self.date_from.setProperty("class", "QDateEdit")
                
        self.label8 = QLabel("Период по")
        self.label8.setProperty("class", "label7")

        self.date_to = QDateEdit(QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        self.date_to.setProperty("class", "QDateEdit")

        self.label9 = QLabel("Формат отчёта")
        self.label9.setProperty("class", "label7")

        self.list_formats = QComboBox()
        self.list_formats.setProperty("class", "QComboBox")
        self.list_formats.addItem("Word")

        self.report_type = QLabel("Тип отчёта")
        self.report_type.setProperty("class", "label7")

        self.list_report_type = QComboBox()
        self.list_report_type.setProperty("class", "QComboBox")
        self.list_report_type.addItem("Проходы")
        self.list_report_type.addItem("Продажи")

        self.do_report_button = QPushButton("Сформировать отчёт")
        self.do_report_button.clicked.connect(self.DoReport)
        self.form_progress = QProgressBar(self)
        self.form_progress.setVisible(False)

        self.form_report_grid = QGridLayout()

        self.form_report_grid.addWidget(self.label6, 0, 0)
        self.form_report_grid.addWidget(self.label7, 0, 1)

        self.form_report_grid.addWidget(self.list_bank_propucts, 1, 0)
        self.form_report_grid.addWidget(self.date_from, 1, 1)

        self.form_report_grid.addWidget(self.label8, 2, 0)
        self.form_report_grid.addWidget(self.label9, 2, 1)

        self.form_report_grid.addWidget(self.date_to, 3, 0)
        self.form_report_grid.addWidget(self.list_formats, 3, 1)

        self.form_report_grid.addWidget(self.report_type, 4, 0)
        self.form_report_grid.addWidget(self.list_report_type, 5, 0)

        self.do_report_loyout = QHBoxLayout()
        self.null_coll4 = QLabel()
        self.null_coll_6 = QLabel()
        self.null_widget_1 = QLabel()
        self.null_widget_1.setMinimumHeight(10)

        self.do_report_loyout.addWidget(self.do_report_button, 2)
        self.do_report_loyout.addWidget(self.null_coll4, 3)  
        self.do_report_loyout.addWidget(self.null_coll_6, 3)    
        
        self.form_report_grid.addWidget(self.null_widget_1, 6, 0)
        self.form_report_grid.addLayout(self.do_report_loyout, 6, 0, 1, 2)


        self.form_report_loyout.addWidget(self.label5)
        self.form_report_loyout.addLayout(self.form_report_grid)
        self.form_report_loyout.addWidget(self.form_progress)
        self.form_report_loyout.addStretch(0)


        self.load_data.setLayout(self.load_data_loyuot)
        self.form_report.setLayout(self.form_report_loyout)


        self.esc_button = QPushButton("Назад")
        self.esc_button.clicked.connect(self.GoToScreen1)

        self.main_loyuot.addLayout(self.button_loyout)
        self.main_loyuot.addWidget(self.stacked_widget)
        self.main_loyuot.addStretch()
        self.main_loyuot.addWidget(self.esc_button)
        self.setLayout(self.main_loyuot)

        
    def ShowLoadData(self):
        self.stacked_widget.setCurrentIndex(0)
        self.load_data_button.setChecked(True)
        self.form_report_button.setChecked(False)


    def ShowFormReport(self):
        self.stacked_widget.setCurrentIndex(1)
        self.load_data_button.setChecked(False)
        self.form_report_button.setChecked(True)


    def OpenFile(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Выберите XLSX файл", "", "Excel (*.xlsx)")
        self.viewmodel.OpenFile(file_path)
        

    def UploadDb(self):
        self.viewmodel.UploadDb(self.list_tables.currentText())
        self.upload_button.setEnabled(False)
        self.load_progress.setVisible(True)
        self.load_progress.setRange(0, 0)


    def GoToScreen1(self):
        self.escape.emit()


    def DoReport(self):
        self.viewmodel.DoReport(self.date_from.date().toString("yyyy-MM-dd"), self.date_to.date().toString("yyyy-MM-dd"), self.list_bank_propucts.currentText(), self.list_report_type.currentText())
        self.do_report_button.setEnabled(False)
        self.form_progress.setVisible(True)
        self.form_progress.setRange(0, 0)


    def LoadError(self, messege):
        self.upload_button.setEnabled(True)
        self.load_progress.setVisible(False)
        QMessageBox.critical(self, "Ошибка" ,f"{messege}")


    def FileError(self):
        self.upload_button.setEnabled(True)
        self.load_progress.setVisible(False)
        QMessageBox.critical(self, "Ошибка" ,"Файл не выбран")


    def LoadInfo(self):
        self.upload_button.setEnabled(True)
        self.load_progress.setVisible(False)
        QMessageBox.information(self, "Успех" ,"Вставка прошла успешно")


    def ReportError(self, messege):
        QMessageBox.critical(self, "Ошибка" ,f"{messege}")
        self.do_report_button.setEnabled(True)
        self.form_progress.setVisible(False)
            

    def ReportSuccess(self, report):
        file_path, _ = QFileDialog.getSaveFileName(caption="Сохранить файл", directory="", filter=".docx")
        if file_path:
            _, extension = os.path.splitext(file_path)
            if extension != '.docx':
                shutil.copy(report, file_path + '.docx')           
                QMessageBox.information(self, "Успех", "Отчёт сохранён")
            else:
                shutil.copy(report, file_path)
                QMessageBox.information(self, "Успех", "Отчёт сохранён")
        self.do_report_button.setEnabled(True)
        self.form_progress.setVisible(False)
        os.remove(report)  