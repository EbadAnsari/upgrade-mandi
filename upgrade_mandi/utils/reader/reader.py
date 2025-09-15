import numpy as __np
import pandas as __pd

from . import __dll


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

    # Convert flat C array to Python list
    flat_list = [table.data[i].decode("utf-8") for i in range(table.rows * table.cols)]

    # Reshape into 2D NumPy array
    df = __pd.DataFrame(
        __np.array(flat_list, dtype=object).reshape(table.rows, table.cols)
    )

    # Free memory allocated in Rust
    __dll.free_table(table_ptr)

    return df
