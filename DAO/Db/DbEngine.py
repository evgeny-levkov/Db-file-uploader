import sqlalchemy


class DbEngine:

    def __init__(self, config):
        self.engine = sqlalchemy.URL.create(
            drivername="postgresql",
            username=config['user'],
            password=config['password'],
            host=config['host'],
            port=config['port'],
            database=config['db_name'])

        try:
            self.engine = sqlalchemy.create_engine(self.engine)
        except Exception as e:
            print(f"Ошибка при создании DbEngine - {e}")