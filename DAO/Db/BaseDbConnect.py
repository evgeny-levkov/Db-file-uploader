from abc import ABC, abstractmethod


class BaseDbConnect(ABC):
    def __init__(self, db_engine):
        self.db_engine = db_engine

    @abstractmethod
    def test_connection(self):
        pass

    @abstractmethod
    def load_data(self, table, db_table):
        pass

    @abstractmethod
    def create_reconciliation_passagers_report(self, qdate_from, qdate_to, db_table_prosmotr):
        pass