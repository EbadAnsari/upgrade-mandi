from datetime import datetime

import pandas as pd
import typer
from utils import config, types, utils


def loadDataSwiggy(file: str, domain: types.Swiggy, sheet: str):
    print(f"Reading file: {file}")
    df = pd.read_excel(file, sheet_name=sheet)

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
    date = types.Date(
        datetime.strptime(str(df["Date"][0]), "%Y-%m-%d 00:00:00").strftime("%d-%m-%Y")
    )

    for column in extraColumns:
        pdfDF[column] = ""

    pdfDF["Article Code"] = pdfDF["Article Code"].astype(int)

    pdfDF["Dispatched Qty"] = pdfDF["Dispatched Qty"].astype(int)
    pdfDF["Rate"] = pdfDF["Rate"].astype(int)

    pdfDF["Total Amount"] = pdfDF["Dispatched Qty"] * pdfDF["Rate"]

    pdfDF["Location"] = pdfDF["Location"].apply(
        lambda x: utils.nameExtracter(
            [location.locationName for location in domain.locations], x
        )
    )

    # The table does contain "Sr", "Recieved Qty", "Total Amount" column(s).
    return (pdfDF, pdfColumns, date)


def loadDataZepto(file: str, sheet: str):
    print(f"Reading file: {file}")
    df = pd.read_excel(
        file,
        sheet_name=sheet,
    )
    df.columns = df.columns.str.strip()
    if not any([column.startswith("NAG-") for column in df.columns]):
        print("❌ The specified columns does not exist in the file.")
        print("Try to change the domain.")
        exit(0)

    locations = [
        location.locationName
        for location in config.domainConfigClass["Zepto"].locations
    ]

    productDF = df[
        df.columns[[not column.startswith("NAG-") for column in df.columns]]
    ].drop(labels=["Product Code", "Grand Total", "Vendor Name"], axis=1)

    productDF["UoM"] = productDF["UoM"].apply(
        lambda uom: "#N/A" if str(uom) == "nan" else uom
    )

    locationDF = df[df.columns[[column.startswith("NAG-") for column in df.columns]]]
    locationDF.columns = [
        utils.nameExtracter(locations, column[4:]) for column in locationDF.columns
    ]

    locationSepratedDF: dict[str, pd.DataFrame] = {}
    for location in locations:
        locationSeries = locationDF[location]
        locationSeries.name = "Invoice Qty."
        locationSepratedDF[location] = pd.concat([productDF, locationSeries], axis=1)

        locationSepratedDF[location]["Amount"] = (
            locationSepratedDF[location]["Rate"]
            * locationSepratedDF[location]["Invoice Qty."]
        )

        locationSepratedDF[location].columns = [
            "Article Name",
            "UoM",
            "Rate",
            "Invoice Qty.",
            "Amount",
        ]

        locationSepratedDF[location]["Recieved Qty."] = ""
        locationSepratedDF[location]["No"] = range(
            1, len(locationSepratedDF[location]) + 1
        )

        locationSepratedDF[location] = locationSepratedDF[location][
            [
                "No",
                "Article Name",
                "UoM",
                "Invoice Qty.",
                "Recieved Qty.",
                "Rate",
                "Amount",
            ]
        ]
    return locationSepratedDF


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
