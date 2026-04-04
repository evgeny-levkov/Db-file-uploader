import pandas as pd

class Hander():
    def __init__(self):
        self.passanges_bbk_maas = pd.read_excel("data/passages_bbk_maas.xlsx")

    def hander_errors(self):
        self.passanges_bbk_maas.drop_duplicates(keep=False)
        return self.passanges_bbk_maas