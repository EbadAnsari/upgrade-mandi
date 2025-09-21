import pandas as __pd

from .reader.reader import read_excel as __read_excel


def getSheetNames(file: str, _filter_func: callable = lambda x: True) -> list[str]:
    return list(filter(_filter_func, __pd.ExcelFile(file).sheet_names))


def readExcel(file: str, sheetName: str) -> __pd.DataFrame:
    return __read_excel(file, sheet_name=sheetName)
