from .db_service import DbService
from PyQt6.QtCore import pyqtSignal, QObject



class dataLoadWorker(QObject):

    connect = pyqtSignal(object)
    finished = pyqtSignal(object)

    def __init__(self, table, db_table, db_engine):
        super().__init__()
        self._service = DbService(db_engine)
        self.table = table
        self.db_table = db_table


    def do_work(self):
        self._service.test_connection()
        self.success = self._service.load_data(self.table, self.db_table)
        self.finished.emit(self.success)