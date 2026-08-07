from PyQt6.QtCore import QObject, pyqtSignal
from Service.DbService import DbService
from Core.DataLoadWorker import DataLoadWorker
from Core.CreateReportWorker import CreateReportWorker
from PyQt6.QtCore import QThread
import pandas as pd
import os


class OperationViewModel(QObject):
    load = pyqtSignal(tuple)
    do_report = pyqtSignal(dict)
    file_name = pyqtSignal(str)
    file_error = pyqtSignal(bool)
    load_error = pyqtSignal(str)
    load_info = pyqtSignal(str)
    report_success = pyqtSignal(str)
    report_error = pyqtSignal(str)
    report = pyqtSignal()

    def __init__(self, service=None):
        super().__init__()
        self.service: DbService | None = service
        self.data_load_worker = None
        self.load_thread = None
        self.create_report_worker = None
        self.report_thread = None
        self.file = None

    def open_file(self, file_path):
        if file_path:
            try:
                self.file = pd.read_excel(file_path)
                self.file_name.emit(os.path.basename(file_path))
            except Exception as e:
                self.file = None
                self.file_name.emit(f"Ошибка при чтении файла: {e}")

    def upload_db(self, list_tables):
        if self.file is not None:
            self.handle_load(list_tables)
        else:
            self.file_error.emit(True)

    def handle_load(self, data):
        if self.data_load_worker is None:
            self.load_thread = QThread()
            self.data_load_worker = DataLoadWorker(self.file, data, self.service)
            self.data_load_worker.moveToThread(self.load_thread)
            try:
                self.load_thread.started.connect(self.data_load_worker.do_work)
                self.load_thread.start()
                self.data_load_worker.finished.connect(self.finished_load)
            except Exception as e:
                self.load_error.emit(f"Ошибка при вставке: {e}")
        else:
            return False

    def finished_load(self, success):
        if success:
            self.load_info.emit("Вставка прошла успешно")
        else:
            self.load_error.emit("Ошибка при вставке")
        self.load_thread.quit()
        self.data_load_worker.deleteLater()
        self.load_thread.deleteLater()
        self.data_load_worker = None
        self.load_thread = None

    def do_report(self, date_from, date_to, list_bank_propucts, list_report_type):
        emit_dict = {
            "date_from": date_from,
            "date_to": date_to,
            "user_table": list_bank_propucts,
            "type_report": list_report_type,
        }

        self.form_report(emit_dict)

    def form_report(self, data):
        if self.create_report_worker is None and data is not None:
            self.report_thread = QThread()
            self.create_report_worker = CreateReportWorker(self.service, data)
            self.create_report_worker.moveToThread(self.report_thread)
            try:
                self.report_thread.started.connect(self.create_report_worker.do_work)
                self.report_thread.start()
                self.create_report_worker.finished.connect(self.finished_report)
            except Exception as e:
                self.report_error.emit(f"Ошибка: {e}")
        else:
            return False

    def finished_report(self, report):
        if report is not None and report is not False:
            self.report_success.emit(report)
        else:
            self.report_error.emit("Ошибка при генерации отчёта")
        self.report_thread.quit()
        self.create_report_worker.deleteLater()
        self.report_thread.deleteLater()
        self.create_report_worker = None
        self.report_thread = None