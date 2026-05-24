from Db.DbConnect import DbConnect
from docxtpl import DocxTemplate
from datetime import date, datetime
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
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'prosmotr_prohodov_maas_mm')
        elif user_table == 'Маас НГПТ':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'prosmotr_prohodov_maas_mgt')
        elif user_table == 'Маас ППК':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'prosmotr_prohodov_maas_ppk')
        elif user_table == 'Банковские карты':
            num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, 'bill_bbk')

        if num_from_db == None or num_from_db == False:
            return False

        doc = DocxTemplate("report_without_BBK.docx")
        try:
            pers = (round( (num_from_db[1]/num_from_db[0]) *100, 2))
        except:
            pers = 0

        res_grade = "Плохо" if pers < 35 else ("Нормально" if pers < 80 else "Хорошо")

        content = {
            "time_start": date_from,
            "time_end" : date_to,
            "time_today": date.today(),
            "product_name": user_table,
            "row_bill_count": num_from_db[0],
            "row_prosmotr_count": num_from_db[1],
            "persent": pers,
            "persent_grade": res_grade,
            "different_count": (num_from_db[0] - num_from_db[1]),
        }

        doc.render(content)
        doc_name = f"Отчёт{datetime.now()}.docx".replace(':', '_')
        doc.save(doc_name)

        return os.path.abspath(doc_name)