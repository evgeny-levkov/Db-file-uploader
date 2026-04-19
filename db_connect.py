import sqlalchemy
from hander import Hander

class Dbconnect():
    def __init__(self, user, password, host, port, db_name):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.db_name = db_name
        self.engine = sqlalchemy.create_engine(f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}")

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