from datetime import datetime

import pandas as pd
import typer
from type.domain_types import Swiggy
from utils.utils import nameExtracter


def loadDataSwiggy(file: str, domain: Swiggy, sheet: str, invoiceVersion: int = 1):

    print("Loading Excel file...")
    df = pd.read_excel(file, sheet_name=sheet)

    df = df.dropna(how="all")[
        [
            column.rawSheet.columnName
            for column in domain.columns
            if column.rawSheet is not None
        ]
    ]

    df.columns = [
        column.invoicePdf.columnName
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
                key=lambda x: x.index,
            ),
        )
    )

    extraColumns = [
        column.invoicePdf.columnName
        for column in domain.columns
        if column.rawSheet is None and column.invoicePdf is not None
    ]

    pdfDF = df.copy()
    date = datetime.strptime(str(df["Date"][0]), "%Y-%m-%d 00:00:00")

    for column in extraColumns:
        pdfDF[column] = ""

    pdfDF["Article Code"] = pdfDF["Article Code"].astype(int)

    pdfDF["Dispatched Qty"] = pdfDF["Dispatched Qty"].astype(int)
    pdfDF["Rate"] = pdfDF["Rate"].astype(int)

    pdfDF["Total Amount"] = pdfDF["Dispatched Qty"] * pdfDF["Rate"]

    pdfDF["Location"] = pdfDF["Location"].apply(
        lambda x: nameExtracter(
            [location.locationName for location in domain.locations], x
        )
    )

    # The table does contain "Sr", "Recieved Qty", "Total Amount" column(s).
    return (pdfDF, pdfColumns, date)


if __name__ == "__main__":

    def run(
        file: str = typer.Option(..., "--file", "-f", help="Excel file path"),
        domain: str = typer.Option(
            "Swiggy", "--domain", "-d", help="Domain name ('Swiggy', 'Zomato', etc.)"
        ),
        invoiceVersion: int = typer.Option(
            1, "--invoice-version", "-i", help="Invoice Version"
        ),
        sheetName: str = typer.Option(
            "Sheet1",
            "--sheet-name",
            "-s",
            help="Sheet name of the Excel file (default: 'Sheet1')",
        ),
    ):
        data = loadDataSwiggy(file, sheetName, invoiceVersion)
        print(data)

    typer.run(run)
