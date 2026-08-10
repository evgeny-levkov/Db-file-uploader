from Service.DbService import DbService
from PyQt6.QtCore import pyqtSignal, QObject


class DataLoadWorker(QObject):
    connect = pyqtSignal(object)
    finished = pyqtSignal(object)

    def __init__(self, table, db_table, column_mapping, db_service: DbService):
        super().__init__()
        self._service = db_service
        self.table = table
        self.db_table = db_table
        self.column_mapping = column_mapping

    def do_work(self):
        self.success = self._service.load_data(self.table, self.db_table, self.column_mapping)
        self.finished.emit(self.success)