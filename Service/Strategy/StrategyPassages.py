from .BaseStrategy import BaseStrategy
import pandas as pd


class StrategyPassages(BaseStrategy):
    def __init__(self, table):
        super().__init__(table)


    def Transformation(self):
        self.excel_table['Дата и время транзакции'] = pd.to_datetime(self.excel_table['Дата и время транзакции'])
        self.excel_table['datetime_minus_4'] = self.excel_table['Дата и время транзакции'] - pd.Timedelta(hours=4)
        self.excel_table['hour_new'] = self.excel_table['datetime_minus_4'].dt.hour
        self.excel_table['day_of_week'] = self.excel_table['datetime_minus_4'].dt.dayofweek

        return self.excel_table