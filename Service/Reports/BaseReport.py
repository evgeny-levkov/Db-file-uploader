from abc import ABC, abstractmethod


class BaseReport(ABC):
    def __init__(self, db, data_dict):
        self.db = db
        self.date_from = data_dict["date_from"]
        self.date_to = data_dict["date_to"]
        self.user_table = data_dict["user_table"]
        self.type_report = data_dict["type_report"]
        self.base_dir = data_dict['base_dir']
        self.mapping = data_dict['mapping']

    @abstractmethod
    def create_report(self):
        pass