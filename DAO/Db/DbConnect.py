import sqlalchemy
from sqlalchemy import text
import pandas as pd
from DAO.Db.DbEngine import DbEngine
from settings import MAPPING
import traceback


class DbConnect():

    def __init__(self, db_engine : DbEngine):
        self.db_engine = db_engine


    def TestConnection(self):
        try:
            with self.db_engine.engine.connect() as connection:
                connection.execute(sqlalchemy.text("SELECT 1"))
                print('Соединение установлено')
                return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            traceback.print_exc()
            return False


    def LoadData(self, table, db_table):
        try:
            with self.db_engine.engine.connect() as conn:

                order_columns = conn.execute(sqlalchemy.text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{db_table}' AND table_schema = 'public' ORDER BY ordinal_position;")).fetchall()
                order_columns = [item[0] for item in order_columns]
                    
                if set(order_columns).issubset(table.columns):
                    table = table[order_columns]
                    table.to_sql(f'{db_table}', self.db_engine.engine, if_exists = 'append', index = False, chunksize = 500000)                            
                    return True
                    
                else:
                    missing_columns = set(order_columns) - set(table.columns)
                    print(missing_columns)
                    return False
                    

        except Exception as e:
            print(f'Ошибка при выполнении запроса: {e}, table = "{db_table}"')
            traceback.print_exc()
            return False
    
    
    def CreateReconciliationPassagesReport(self, qdate_from, qdate_to, db_table_prosmotr):
        try:
            with self.db_engine.engine.connect() as conn:
                db_column = conn.execute(sqlalchemy.text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{db_table_prosmotr}' AND table_schema = 'public' ORDER BY ordinal_position;")).fetchall()
                try:
                    if ('data_i_vremya_tranzaktsii',) in db_column:
                        if db_table_prosmotr == 'bill_bbk':
                            output = conn.execute(sqlalchemy.text(f"SELECT COUNT(*), COALESCE(SUM(CASE WHEN tekst_oshibki IS NOT NULL THEN 1 ELSE 0 END), 0) FROM {db_table_prosmotr} WHERE data_i_vremya_tranzaktsii BETWEEN '{qdate_from}' AND '{qdate_to}'")).fetchall()[0]
                        else:
                            output = conn.execute(sqlalchemy.text(f"SELECT COUNT(*), COALESCE(SUM(CASE WHEN (sverena_s_bankom != 'Да' OR sverena_s_bankom IS NULL) THEN 1 ELSE 0 END), 0) FROM {db_table_prosmotr} WHERE data_i_vremya_tranzaktsii BETWEEN '{qdate_from}' AND '{qdate_to}'")).fetchall()[0]
                    else:
                        output = None
                        print("Нет колонки data_i_vremya_tranzaktsii")

                except Exception as e:
                    print(f"Ошибка: {e}")
                    traceback.print_exc()
                    return False

                return output    
                             
        except Exception as e:
            print(f"Ошибка: {e}")
            traceback.print_exc()
            return False