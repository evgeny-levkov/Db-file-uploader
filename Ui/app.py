from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QMessageBox, QDateEdit
from Ui.ConnectWindow import ConnectionScreen
from Ui.OperationWindow import OperationScreen
from Service.DbService import DbService
from Core.DataLoadWorker import DataLoadWorker
from Core.CreateReportWorker import CreateReportWorker 
from PyQt6.QtCore import QThread
from DAO.Db.DbEngine import DbEngine
import os
import shutil



class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.stacked_widget = QStackedWidget()
        self.connectionScreen = ConnectionScreen()
        self.operationScreen = OperationScreen()

        self.stacked_widget.addWidget(self.connectionScreen)
        self.stacked_widget.addWidget(self.operationScreen)

        self.connectionScreen.success.connect(self.HandleSuccess)
        self.operationScreen.escape.connect(self.HandleEscape)
        self.operationScreen.load.connect(self.HandleLoad)
        self.operationScreen.do_report.connect(self.FormReport)
        
        self.service = None
        self.data_load_worker = None
        self.create_report_worker = None
        self.config = None
        self.load_thread: QThread = None
        self.report_thread: QThread = None
        self.db_engine = None

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


    def HandleSuccess(self, config):
        if config is None:
            QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
            return
        
        try:
            self.config = config
            self.db_engine = DbEngine(config)
            self.service = DbService(self.db_engine)
            if self.service.TestConnection():
                self.stacked_widget.setCurrentIndex(1)
            else:
                QMessageBox.critical(self, "Ошибка", "Ошибка подключения к БД")
        except:
            QMessageBox.critical(self, "Ошибка", "Критическая ошибка")


    def HandleEscape(self):
        self.stacked_widget.setCurrentIndex(0)


    def HandleLoad(self, data):
        
        if self.data_load_worker is None:
            self.load_thread = QThread()
            self.data_load_worker = DataLoadWorker(data[0], data[1], self.db_engine)
            self.data_load_worker.moveToThread(self.load_thread)
            try:
                self.load_thread.started.connect(self.data_load_worker.DoWork)
                self.load_thread.start()
                self.data_load_worker.finished.connect(self.FinishedLoad)
            except:
                QMessageBox.critical(self, "Ошибка" ,"Ошибка при вставке")
        else:
            return False


    def FinishedLoad(self, success):
        if success:
            self.operationScreen.upload_button.setEnabled(True)
            self.operationScreen.load_progress.setVisible(False)
            QMessageBox.information(self, "Успех" ,"Вставка прошла успешно")
        else:
            QMessageBox.critical(self, "Ошибка" ,"Ошибка при вставке")
        self.load_thread.quit()
        self.data_load_worker.deleteLater()
        self.load_thread.deleteLater()
        self.data_load_worker = None
        self.load_thread = None


    def FormReport(self, data):

        date_from : QDateEdit = data[0]
        date_to : QDateEdit = data[1]
        date_from = date_from.date().toString("yyyy-MM-dd")
        date_to = date_to.date().toString("yyyy-MM-dd")
        str_date_from = f"{date_from} 00:00:00"
        str_date_to = f"{date_to} 23:59:59"


        if self.create_report_worker is None:
            self.report_thread = QThread()
            self.create_report_worker = CreateReportWorker(self.db_engine, str_date_from, str_date_to, data[2])
            self.create_report_worker.moveToThread(self.report_thread)
            try:
                self.report_thread.started.connect(self.create_report_worker.DoWork)
                self.report_thread.start()
                self.create_report_worker.finished.connect(self.FinishedReport)
            except:
                QMessageBox.critical(self, "Ошибка" ,"Ошибка при загрузке отчёта")
        else:
            return False


    def FinishedReport(self, report):
        if report is not None and report is not False:
            file_path, _ = QFileDialog.getSaveFileName(caption="Сохранить файл", directory="", filter=".docx")
            if file_path:
                _, extension = os.path.splitext(file_path)
                if extension != '.docx':
                    shutil.copy(report, file_path + '.docx')           
                    QMessageBox.information(self, "Успех", "Отчёт сохранён")
                else:
                    shutil.copy(report, file_path)
                    QMessageBox.information(self, "Успех", "Отчёт сохранён")
            os.remove(report)   
        else:
            QMessageBox.critical(self, "Ошибка" ,"Ошибка при загрузке отчёта")
        self.operationScreen.do_report_button.setEnabled(True)
        self.operationScreen.form_progress.setVisible(False)
        self.report_thread.quit()
        self.create_report_worker.deleteLater()
        self.report_thread.deleteLater()
        self.create_report_worker = None
        self.report_thread = None


    @staticmethod
    def LoadStylesheet(path):
        """Загрузка CSS из файла"""
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return file.read()
        return ""