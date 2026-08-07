from Service.DbService import DbService
from PyQt6.QtCore import pyqtSignal, QObject


class CreateReportWorker(QObject):
    finished = pyqtSignal(object)

    def __init__(self, db_service: DbService, data):
        super().__init__()
        self._service = db_service
        self.data = data

    def do_work(self):
        self.report = self._service.generate_report(self.data)
        self.finished.emit(self.report)