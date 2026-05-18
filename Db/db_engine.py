import sqlalchemy

class Dbengine():

    def __init__(self, config):
        self.engine = sqlalchemy.create_engine(
        f"postgresql://{config['user']}:{config['password']}"
        f"@{config['host']}:{config['port']}/{config['db_name']}"
        )