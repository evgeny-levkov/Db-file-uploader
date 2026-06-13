from .BaseStrategy import BaseStrategy
import pandas as pd


class StrategySessii(BaseStrategy):
    def __init__(self, table):
        super().__init__(table)


    def Transformation(self):
        self.excel_table['Дата и время транзакции'] = pd.to_datetime(self.excel_table['Дата и время транзакции'])
        self.excel_table['day_of_week_new'] = self.excel_table['Дата и время транзакции'].dt.dayofweek
        self.excel_table['hour_new'] = self.excel_table['Дата и время транзакции'].dt.hour

        return self.excel_table