from .BaseStrategy import BaseStrategy
import pandas as pd


class StrategyReestry(BaseStrategy):
    def __init__(self, table):
        super().__init__(table)

    def transformation(self):
        self.excel_table['TransportTime'] = pd.to_datetime(self.excel_table['TransportTime'])
        self.excel_table['day_of_week_new'] = self.excel_table['TransportTime'].dt.dayofweek
        self.excel_table['hour_new'] = self.excel_table['TransportTime'].dt.hour

        return self.excel_table