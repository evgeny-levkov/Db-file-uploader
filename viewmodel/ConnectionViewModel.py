from PyQt6.QtCore import QObject, pyqtSignal
from DAO.Db.DbEngine import DbEngine
from DAO.Db.DbConnect import DbConnect
from Service.DbService import DbService



class ConnectionViewModel(QObject):

    success = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        


    def ConnectDb(self, user, password, host, port, name_db):
        if not user or not password or not host or not port or not name_db:
            self.success.emit(None)
            return
        
        config ={
            "user": user,
            "password": password,
            "host": host,
            "port": port,
            "db_name": name_db
        }

        try:
            self.config = config
            self.db_engine = DbEngine(config)
            self.db_connection = DbConnect(self.db_engine)
            self.service = DbService(self.db_connection)
            if self.service.TestConnection():
                self.success.emit(self.service)
            else:
                self.success.emit("Ошибка подключения к БД")
        except:
            self.success.emit("Критическая ошибка")
