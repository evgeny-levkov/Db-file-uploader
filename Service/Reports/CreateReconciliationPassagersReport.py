from docxtpl import DocxTemplate
from datetime import date
from tempfile import NamedTemporaryFile
from settings import BASE_DIR, MAPPING
from .ReportFactory import ReportFactory
from .BaseReport import BaseReport


@ReportFactory.register("CreateReconciliationPassagersReport")
class CreateReconciliationPassagersReport(BaseReport):
    def __init__(self, db, data_dict):
        super().__init__(db, data_dict)

    def create_report(self):
        user_table_map = {
            'Маас ММ': 'prosmotr_prohodov_maas_mm',
            'Маас НГПТ': 'prosmotr_prohodov_maas_mgt',
            'Маас ППК': 'prosmotr_prohodov_maas_ppk',
            'Банковские карты': 'bill_bbk',
        }
        self.date_from = f"{self.date_from} 00:00:00"
        self.date_to = f"{self.date_to} 23:59:59"

        num_from_db = self.db.create_reconciliation_passagers_report(
            self.date_from,
            self.date_to,
            user_table_map.get(
                self.user_table,
                'bill_bbk'
            )
        )
        if num_from_db is None or num_from_db is False:
            return False

        full_report_path = BASE_DIR / MAPPING['file_path']['path_report_1']

        try:
            doc = DocxTemplate(full_report_path)
            try:
                pers = round(((num_from_db[0] - num_from_db[1]) / num_from_db[0]) * 100, 2)
            except ZeroDivisionError:
                pers = "Ошибка"

            res_grade = "Плохо" if pers < 35 else ("Нормально" if pers < 80 else "Хорошо")
            content = {
                "time_start": self.date_from,
                "time_end": self.date_to,
                "time_today": date.today(),
                "product_name": self.user_table,
                "row_bill_count": num_from_db[0],
                "row_prosm_count": (num_from_db[0] - num_from_db[1]),
                "persent": pers,
                "persent_grade": res_grade,
                "different_count": num_from_db[1]
            }

            doc.render(content)
            tpm = NamedTemporaryFile(suffix='.docx', delete=False)
            tpm.close()
            doc.save(tpm.name)

            return tpm.name

        except Exception as e:
            print(e)
            return False