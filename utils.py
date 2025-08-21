import pandas as pd

def load_excel(path, sheet=None):
    return pd.read_excel(path, sheet_name=sheet or 0)