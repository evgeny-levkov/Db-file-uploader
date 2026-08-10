from abc import ABC, abstractmethod


class BaseStrategy(ABC):
    def __init__(self, table):
        self.excel_table = table

    @abstractmethod
    def transformation(self):
        pass