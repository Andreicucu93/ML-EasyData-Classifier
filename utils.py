import pandas as pd

def load_excel(path, sheet=None):
    return pd.read_excel(path, sheet_name=sheet or 0)

def export_data(dataset, sheet=None):
    output = pd.DataFrame(dataset)
    print(output)
    return output