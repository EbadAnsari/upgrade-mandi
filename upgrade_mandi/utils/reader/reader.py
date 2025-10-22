from typing import Any, Tuple

import numpy as __np
import pandas as __pd
from pyparsing import col

from . import dll as __dll
from . import test


def read_excel(
    file_path: str, sheet_name: str
) -> Tuple[__pd.DataFrame, __pd.DataFrame]:
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

    dtype = __pd.DataFrame()

    df = __pd.DataFrame()
    matrix = []

    cell_type_map_dict = [
        lambda x: __np.nan,
        __np.str_,
        __np.int64,
        __np.float64,
        __np.bool,
        __pd.to_datetime,
    ]

    for row in range(table.rows):
        _row = []
        for col_index in range(table.cols):
            cell = table.data[row * table.cols + col_index]
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
        matrix.append(_row)
    __dll.free_table(table_ptr)

    repeated_index_count: dict[str, int] = {}

    column_names = []

    for index, column_name in enumerate(matrix[0]):
        if column_name not in repeated_index_count:
            repeated_index_count[column_name] = -1
        repeated_index_count[column_name] += 1

        matrix[0][
            index
        ] = f"{column_name}{f' ({repeated_index_count[column_name]})' if repeated_index_count[column_name] > 0 else ''}"

    df = __pd.DataFrame(matrix[1:], columns=matrix[0])
    df.dropna(axis=0, how="all", inplace=True)

    return (df, dtype)
