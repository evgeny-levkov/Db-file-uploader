import psycopg2

class Dbconnect():
    def __init__(self):
        self.conn = psycopg2.connect("postgresql://admin:admin_password@localhost:5432/superset")
        self._cursor = None

    def query(self):
        self._cursor = self.conn.cursor()
        try:
            self._cursor.execute("select * from passages_bbk_maas")
            result = self._cursor.fetchone()
            print(result)
        except Exception as e:
            print(f"Ошибка при выполнении запроса: {e}")

    def close_connect(self):
        if self._cursor is not None:
            self._cursor.close()
        self.conn.close()

db = Dbconnect()
db.query()
db.close_connect()