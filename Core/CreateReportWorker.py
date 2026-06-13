from Service.DbService import DbService
from PyQt6.QtCore import pyqtSignal, QObject



class CreateReportWorker(QObject):

    finished = pyqtSignal(str)

    def __init__(self, db_service : DbService, data):
        super().__init__()
        self._service = db_service
        self.data = data


    def DoWork(self):
        self.report = self._service.GenerateReport(self.data)
        self.finished.emit(self.report)