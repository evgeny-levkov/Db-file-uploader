from DAO.Db.DbConnect import DbConnect
from .Reports.CreateReconciliationPassagesReport import CreateReconciliationPassagesReport 


class DbService:

    def __init__(self, db_engine):
        self.db = DbConnect(db_engine)
        self.report = None


    def TestConnection(self):
        return self.db.TestConnection()
    

    def LoadData(self, table, db_table):
        try:
            return self.db.LoadData(table, db_table)
        
        except Exception as e:
            print(e)
            return False
        
        
    def CreateReconciliationPassagesReport(self, data):
        self.report = CreateReconciliationPassagesReport(self.db ,data["date_from"], data["date_to"], data["list_blank"])
        return self.report.CreateReport()