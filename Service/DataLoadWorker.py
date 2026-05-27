from .DbService import DbService
from PyQt6.QtCore import pyqtSignal, QObject



class DataLoadWorker(QObject):

    connect = pyqtSignal(object)
    finished = pyqtSignal(object)

    def __init__(self, table, db_table, db_engine):
        super().__init__()
        self._service = DbService(db_engine)
        self.table = table
        self.db_table = db_table


    def DoWork(self):
        self.success = self._service.LoadData(self.table, self.db_table)
        self.finished.emit(self.success)