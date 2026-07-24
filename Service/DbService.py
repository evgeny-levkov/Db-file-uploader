from DAO.Db.DbConnect import DbConnect
from .Reports.BaseReport import BaseReport
from .Reports.ReportFactory import ReportFactory
from settings import MAPPING
from .Strategy.DataTransform import DataTransform


class DbService:

    def __init__(self, db_connection : DbConnect):
        self.db = db_connection


    def TestConnection(self):
        return self.db.TestConnection()
    

    def LoadData(self, table, db_table):
        try:
            dt_transform = DataTransform(table, db_table)
            table = dt_transform.Transform()
            return self.db.LoadData(table, db_table)
        
        except Exception as e:
            print(e)
            return False
        
        
    def GenerateReport(self, data):
        self.report_type = MAPPING["report_type"][data["type_report"]]
        factory: BaseReport = ReportFactory.create_object(self.report_type, self.db, data)
        return factory.CreateReport()