import sqlalchemy
from hander import Hander
import pandas as pd

class Dbconnect():
    def __init__(self, config):
        self.engine = sqlalchemy.create_engine(
        f"postgresql://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['db_name']}"
        )
        self.connection = None


    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
                self.connection = conn
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False


    def load_data(self, table, db_table):
        if isinstance(table, pd.DataFrame):
            try:
                table.columns = table.columns.str.lower()
                table.to_sql(f'{db_table}', self.engine, if_exists = 'append', index = False)
                return True
        
            except Exception as e:
                print(f'Ошибка при выполнении запроса: {e}')
                return False
        else:
            return False
        

    def close_connect(self):
        self.engine.dispose()