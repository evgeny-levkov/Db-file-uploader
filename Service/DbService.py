from Db.DbConnect import DbConnect
from docxtpl import DocxTemplate
from datetime import date, datetime
from pathlib import Path
import os 
from tempfile import NamedTemporaryFile


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

        user_table_map = {
            'Маас ММ': 'prosmotr_prohodov_maas_mm',
            'Маас НГПТ': 'prosmotr_prohodov_maas_mgt',
            'Маас ППК': 'prosmotr_prohodov_maas_ppk',
            'Банковские карты': 'bill_bbk',
        }
        num_from_db = self.db.CreateReconciliationPassagesReport(date_from, date_to, user_table_map.get(user_table, 'bill_bbk'))
        if num_from_db == None or num_from_db == False:
            return False

        script_dir = Path(__file__).resolve().parent
        templates = script_dir.parent/'Report_templates'/'report_1.docx'

        doc = DocxTemplate(templates)
        try:
            pers = (round( ((num_from_db[0] - num_from_db[1]) / num_from_db[0]) *100, 2))
        except:
            pers = "Ошибка"

        res_grade = "Плохо" if pers < 35 else ("Нормально" if pers < 80 else "Хорошо")
        content = {
            "time_start": date_from,
            "time_end" : date_to,
            "time_today": date.today(),
            "product_name": user_table,
            "row_bill_count": num_from_db[0],
            "row_prosm_count": (num_from_db[0] - num_from_db[1]), 
            "persent": pers,
            "persent_grade": res_grade,
            "different_count": (num_from_db[1])
        }

        doc.render(content)
        tpm = NamedTemporaryFile(suffix = '.docx', delete = False)
        tpm.close()
        doc.save(tpm.name)

        return tpm.name