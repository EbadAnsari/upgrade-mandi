from typing import Any

import numpy as __np
import pandas as __pd

from . import dll as __dll
from . import test


def read_excel(file_path: str, sheet_name: str) -> __pd.DataFrame:
    """Reads an Excel file and returns its contents as a pandas DataFrame.

    Args:
            file_path (str): Path to the Excel file.
            sheet_name (str): Name of the sheet to read.

    Returns:
            pd.DataFrame: DataFrame containing the sheet's data.
    """

    # Call Rust function
    table_ptr = __dll.read_excel(
        file_path.encode("utf-8"), sheet_name.encode("utf-8"), sheet_name
    )  # Excel file and sheet name
    if not table_ptr:
        raise RuntimeError("Failed to read Excel file or sheet")

    table = table_ptr.contents

    # print(table.data[90].kind)
    # print(table.data[90].value.decode("utf-8"))
    # print()
    # flat_list = []
    df = __pd.DataFrame()
    matrix = []
    for row in range(table.rows):
        _row = []
        for col in range(table.cols):
            cell = table.data[row * table.cols + col]
            value = cell.value.decode("utf-8")

            if cell.kind == 0:
                _row.append(__np.nan)
            elif cell.kind in [1, 5]:
                _row.append(str(value))
            elif cell.kind == 2:
                _row.append(int(value))
            elif cell.kind == 3:
                _row.append(float(value))
            elif cell.kind == 4:
                _row.append(value)
        if row == 0:
            for column_name in _row:
                df[column_name] = []
        else:
            matrix.append(_row)
    __dll.free_table(table_ptr)
    df = __pd.concat(
        [df, __pd.DataFrame(matrix, columns=df.columns)], axis=0, ignore_index=True
    )
    df.dropna(axis=0, how="all", inplace=True)
    return df
