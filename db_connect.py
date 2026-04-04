import sqlalchemy
from hander import Hander

class Dbconnect():
    def __init__(self):
        self.engine = sqlalchemy.create_engine("postgresql://admin:admin_password@localhost:5432/superset")

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            return True
        except Exception as e:
            print(f"Ошибка подключения: {e}")
            return False

    def alter_table(self):
        hander = Hander()
        self.data_passanges_bbk_maas = hander.hander_errors()
        try:
            self.data_passanges_bbk_maas.to_sql('passages_bbk_maas', self.engine, 
                                        if_exists='append', 
                                        index=False)
            return True
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")
            return False

    def close_connect(self):
        self.engine.dispose()