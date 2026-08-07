import pandas as pd
from settings import MAPPING
import traceback
from .BaseStrategy import BaseStrategy
from .StrategyPassages import StrategyPassages
from .StrategyReestry import StrategyReestry
from .StrategySessii import StrategySessii


class DataTransform:
    def __init__(self, table, db_table):
        self.excel_table = table
        self.db_table = db_table

    def transform(self):
        STRATEGIES = {
            "sessii_prodaj_vt": StrategySessii,
            "sessii_prodaj_maas": StrategySessii,
            "reestr_prodaj_vt": StrategyReestry,
            "reestr_prodaj_maas": StrategyReestry,
        }

        if isinstance(self.excel_table, pd.DataFrame):
            self.db_column = MAPPING[self.db_table]
            if len(self.db_column) == 0:
                print('Таблица не найдена')
                return False
            try:
                strategy = STRATEGIES.get(self.db_table, StrategyPassages)
                class_strategy: BaseStrategy = strategy(self.excel_table)
                self.excel_table = class_strategy.transformation()

            except Exception as e:
                print(f'Невозможно преобразовать исходные данные, ошибка: {e}')
                traceback.print_exc()
                return False

            self.excel_table = self.excel_table.rename(columns=self.db_column)

        return self.excel_table