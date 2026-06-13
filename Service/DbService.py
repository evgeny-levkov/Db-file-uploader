from DAO.Db.DbConnect import DbConnect
from Service.BaseReport import BaseReport
from Service.ReportFactory import ReportFactory
from settings import MAPPING


class DbService:

    def __init__(self, db_engine):
        self.db = DbConnect(db_engine)


    def TestConnection(self):
        return self.db.TestConnection()
    

    def LoadData(self, table, db_table):
        try:
            return self.db.LoadData(table, db_table)
        
        except Exception as e:
            print(e)
            return False
        
        
    def GenerateReport(self, data):
        self.report_type = MAPPING["report_type"][data["type_report"]]
        factory: BaseReport = ReportFactory.create_report(self.db, self.report_type, data)
        return factory.CreateReport()