import sqlalchemy
from sqlalchemy import text
import pandas as pd
from Db.db_engine import Dbengine



class Dbconnect():

    def __init__(self, db_engine):
        self.db_engine: Dbengine = db_engine


    def test_connection(self):
        try:
            with self.db_engine.engine.connect() as connection:
                connection.execute(sqlalchemy.text("SELECT 1"))
                print('Соединение установлено')
                return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False


    def load_data(self, table, db_table):
        if isinstance(table, pd.DataFrame):
            try:
                with self.db_engine.engine.connect() as conn:
                    db_column = conn.execute(sqlalchemy.text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{db_table}' AND table_schema = 'public' ORDER BY ordinal_position;")).fetchall()
                    if len(db_column) == 0:
                        print('Таблица не найдена')
                        return False
                    if db_table in ['sessii_prodaj_vt', 'sessii_prodaj_maas']:
                        table['Дата и время транзакции'] = pd.to_datetime(table['Дата и время транзакции'])
                        table['day_of_week_new'] = table['Дата и время транзакции'].dt.dayofweek
                        table['hour_new'] = table['Дата и время транзакции'].dt.hour

                    elif db_table in ['reestr_prodaj_vt', 'reestr_prodaj_maas']:
                        table['transporttime'] = pd.to_datetime(table['Дата и время транзакции'])
                        table['day_of_week_new'] = table['transporttime'].dt.dayofweek
                        table['hour_new'] = table['Дата и время транзакции'].dt.hour

                    else:
                        table['Дата и время транзакции'] = pd.to_datetime(table['Дата и время транзакции'])
                        table['datetime_minus_4'] = table['Дата и время транзакции'] - pd.Timedelta(hours=4)
                        table['hour_new'] = table['datetime_minus_4'].dt.hour
                        table['day_of_week_new'] = table['datetime_minus_4'].dt.dayofweek

                    db_column_new = [item[0] for item in db_column]
                    if len(db_column_new) == len(table.columns):
                        try:
                            table.columns = db_column_new
                            table.to_sql(f'{db_table}', self.db_engine.engine, if_exists = 'append', index = False)
                            return True
                        
                        except Exception as e:
                            print(f'Ошибка при выполнении запроса: {e}, table = "{db_table}"')
                            return False
                    else:
                        print("Таблица не соответствует таблице в БД по количеству столбцов")
                        print(f"{table.columns}")
                        print(f"{db_column}")
                        return False
                
            except Exception as e:
                print(f'Ошибка при выполнении запроса: {e}, table = "{db_table}"')
                return False
        else:
            return False