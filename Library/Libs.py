import numpy as np
import pandas as pd


def unpivot(frame):
    N, K = frame.shape
    data = {
        "value": frame.to_numpy().ravel("F"),
        "variable": np.asarray(frame.columns).repeat(N),
        "date": np.tile(np.asarray(frame.index), K),
    }
    return pd.DataFrame(data, columns=["date", "variable", "value"])


def exportToExcel(df, excelPath):
    df.to_excel(excelPath, index=False, sheet_name='First normal form')


def exportExcelToPd(excelPath):
    return pd.read_excel(excelPath, sheet_name='First normal form')
