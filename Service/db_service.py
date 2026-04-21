from Db.db_connect import Dbconnect


class DbService:
    def __init__(self, config):
        self.db = Dbconnect(config)

    def test_connection(self):
        return self.db.test_connection()