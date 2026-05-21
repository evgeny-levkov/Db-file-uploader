from Db.DbConnect import DbConnect
from docxtpl import DocxTemplate
from datetime import date
import os 



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
        
        
    def CreateReconciliationPassagesReport(self, date_from, date_to, user_table):
        if user_table == 'Маас ММ':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'bill_maas_mm', 'prosmotr_prohodov_maas_mm')
        elif user_table == 'Маас НГПТ':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'bill_maas_mgt', 'prosmotr_prohodov_maas_mgt')
        elif user_table == 'Маас ППК':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'bill_maas_ppk', 'prosmotr_prohodov_maas_ppk')
        elif user_table == 'Банковские карты':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'bill_bbk', None)

        doc = DocxTemplate("report_without_BBK.docx")
        if user_table != 'Банковские карты' and num_from_db:
            content = {
                "time_start": date_from,
                "time_end" : date_to,
                "time_today": date.today(),
                "product_name": user_table,
                "row_bill_count": num_from_db[0],
                "row_prosmotr_count": num_from_db[1],
                "persent": (round( (num_from_db[0]/num_from_db[1]), 1)),
                "different_count": (num_from_db[0] - num_from_db[1]),
                "sum": 10000000000000000,
            }

            doc.render(content)
            doc.save("Отчёт.docx")
            return os.path.abspath("Отчёт.docx")
        
        else:
            return None