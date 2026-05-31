from datetime import datetime
from typing import Any

import pandas as pd
import utils.utils as utils
from utils.config import domainConfigClass
from utils.read import readExcel
from utils.types import date
from utils.types import domain as d


def loadDataSwiggy(
    file: str, sheet_name: str
) -> tuple[pd.DataFrame, list[Any], date.Date]:
    print(f"Reading file: {file}")
    domain = domainConfigClass["Swiggy"]
    df = readExcel(file, sheetName=sheet_name)

    print(df)

    try:
        df = df.dropna(how="all")[
            [
                column.rawSheet.columnName
                for column in domain.columns
                if column.rawSheet is not None
            ]
        ]
    except Exception as e:
        if "None of [Index([" in str(
            e
        ) and "dtype='object')] are in the [columns]" in str(e):
            print("❌ The specified columns does not exist in the file.")
            print("Try to change the domain.")
            exit(0)
        else:
            raise

    df.columns = [
        column.invoicePdf.columnName  # type: ignore
        for column in domain.columns
        if column.rawSheet is not None
    ]

    pdfColumns = list(
        map(
            lambda x: x.columnName,
            sorted(
                [
                    column.invoicePdf
                    for column in domain.columns
                    if column.invoicePdf is not None
                    and column.invoicePdf.index is not None
                ],
                key=lambda x: x.index,  # type: ignore
            ),  # type: ignore
        )
    )

    extra_columns = [
        column.invoicePdf.columnName
        for column in domain.columns
        if column.rawSheet is None and column.invoicePdf is not None
    ]

    pdf_df = df.copy()
    _date = date.Date(
        dateString=datetime.strptime(str(df["Date"][0]), "%Y-%m-%d").strftime(
            "%d-%m-%Y"
        )
    )

    for column in extra_columns:
        pdf_df[column] = ""

    pdf_df["Article Code"] = pdf_df["Article Code"].astype(int)

    pdf_df["Dispatched Qty"] = pdf_df["Dispatched Qty"].astype(int)
    pdf_df["Rate"] = pdf_df["Rate"].astype(float)

    pdf_df["Total Amount"] = pdf_df["Dispatched Qty"] * pdf_df["Rate"]

    pdf_df["Location"] = pdf_df["Location"].apply(
        lambda x: utils.nameExtracter(
            [location.name for location in domain.locations], x
        )
    )

    pdf_df["Total Amount"] = pdf_df["Total Amount"].round(3)

    # The table does contain "Sr", "Recieved Qty", "Total Amount" column(s).
    return (pdf_df, pdfColumns, _date)
