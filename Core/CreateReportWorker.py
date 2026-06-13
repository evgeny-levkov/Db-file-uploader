from Service.DbService import DbService
from PyQt6.QtCore import pyqtSignal, QObject



class CreateReportWorker(QObject):

    finished = pyqtSignal(str)

    def __init__(self, db_engine, data):
        super().__init__()
        self._service = DbService(db_engine)
        self.data = data


    def DoWork(self):
        self.report = self._service.GenerateReport(self.data)
        self.finished.emit(self.report)