from settings import MAPPING
from DAO.Db.DbConnect import DbConnect

class BaseReport():
    def __init__(self, db, data_dict):
        self.db: DbConnect  = db
        self.date_from = data_dict["date_from"]
        self.date_to = data_dict["date_to"]
        self.list_blank = data_dict["list_blank"]
        self.type_report = data_dict["type_report"]
        self.report_type = MAPPING["report_type"][self.type_report]


    def CreateReport(self):
        pass