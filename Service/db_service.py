from Db.db_connect import Dbconnect


class DbService:
    
    def __init__(self, config):
        self.db = Dbconnect(config)


    def test_connection(self):
        return self.db.test_connection()
    

    def load_data(self, table, db_table):
        try:
            return self.db.load_data(table, db_table)

        except Exception as e:
            print(e)
            return False
