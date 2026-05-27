from Db.DbConnect import DbConnect
from docxtpl import DocxTemplate
from datetime import date
from pathlib import Path
from tempfile import NamedTemporaryFile


class CreateReconciliationPassagesReport:

    def __init__(self, db_connect, date_from, date_to, user_table):
        self.db: DbConnect = db_connect
        self.date_from = date_from 
        self.date_to = date_to
        self.user_table = user_table

    def CreateReport(self):

        user_table_map = {
            'Маас ММ': 'prosmotr_prohodov_maas_mm',
            'Маас НГПТ': 'prosmotr_prohodov_maas_mgt',
            'Маас ППК': 'prosmotr_prohodov_maas_ppk',
            'Банковские карты': 'bill_bbk',
        }
        num_from_db = self.db.CreateReconciliationPassagesReport(self.date_from, self.date_to, user_table_map.get(self.user_table, 'bill_bbk'))
        if num_from_db == None or num_from_db == False:
            return False

        script_dir = Path(__file__).resolve().parent
        templates = script_dir.parent/'Report_templates'/'report_1.docx'

        try:
            doc = DocxTemplate(templates)
            try:
                pers = (round( ((num_from_db[0] - num_from_db[1]) / num_from_db[0]) *100, 2))
            except:
                pers = "Ошибка"

            res_grade = "Плохо" if pers < 35 else ("Нормально" if pers < 80 else "Хорошо")
            content = {
                "time_start": self.date_from,
                "time_end" : self.date_to,
                "time_today": date.today(),
                "product_name": self.user_table,
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
        
        except Exception as e:
            print(e)
            return False