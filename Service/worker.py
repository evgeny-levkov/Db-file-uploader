from .db_service import DbService
from PyQt6.QtCore import pyqtSignal, QObject


class Worker(QObject):

    finished = pyqtSignal(object)

    def __init__(self, table, db_table, config):
        super().__init__()
        self._service = DbService(config)
        self.table = table
        self.db_table = db_table

    def do_work(self):
        self.success = self._service.load_data(self.table, self.db_table)
        self.finished.emit(self.success)