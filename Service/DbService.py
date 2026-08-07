from DAO.Db.DbConnect import DbConnect
from .Reports.BaseReport import BaseReport
from .Reports.ReportFactory import ReportFactory
from settings import MAPPING
from .Strategy.DataTransform import DataTransform


class DbService:
    def __init__(self, db_connection: DbConnect):
        self.db = db_connection

    def test_connection(self):
        return self.db.test_connection()

    def load_data(self, table, db_table):
        try:
            dt_transform = DataTransform(table, db_table)
            table = dt_transform.transform()
            return self.db.load_data(table, db_table)
        except Exception as e:
            print(e)
            return False

    def generate_report(self, data):
        self.report_type = MAPPING["report_type"][data["type_report"]]
        factory: BaseReport = ReportFactory.create_object(
            self.report_type,
            self.db,
            data
        )
        return factory.create_report()