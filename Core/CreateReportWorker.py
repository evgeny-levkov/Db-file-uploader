from Service.DbService import DbService
from PyQt6.QtCore import pyqtSignal, QObject



class CreateReportWorker(QObject):

    finished = pyqtSignal(str)

    def __init__(self, db_engine, date_from, date_to, user_table):
        super().__init__()
        self._service = DbService(db_engine)
        self.date_from = date_from
        self.date_to = date_to
        self.user_table = user_table


    def DoWork(self):
        self.report = self._service.CreateReconciliationPassagesReport(self.date_from, self.date_to, self.user_table)
        self.finished.emit(self.report)