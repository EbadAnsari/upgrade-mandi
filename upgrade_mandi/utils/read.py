from collections.abc import Callable
from typing import List, Tuple

import pandas as __pd

from .reader.reader import read_excel as __read_excel


def getSheetNames(
    file: str, _filter_func: Callable[[str], bool] = lambda x: True
) -> List[str]:
    return list(
        filter(_filter_func, [str(name) for name in __pd.ExcelFile(file).sheet_names])
    )


def readExcel(file: str, sheetName: str) -> Tuple[__pd.DataFrame, __pd.DataFrame]:
    return __read_excel(file, sheet_name=sheetName)
