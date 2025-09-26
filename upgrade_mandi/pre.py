from datetime import datetime
from typing import Any, List, Tuple

import pandas as pd
import typer
from utils import config, utils
from utils.read import readExcel
from utils.types import date
from utils.types import domain as d


def loadDataSwiggy(
    file: str, sheet_name: str, domain: d.Swiggy
) -> tuple[pd.DataFrame, list[Any], date.Date]:
    print(f"Reading file: {file}")
    df = readExcel(file, sheetName=sheet_name)

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


def pre_processing_zepto(
    file_name: str, sheet_name: str, domain: d.DomainSelection
) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    df = readExcel(
        file_name,
        sheetName=sheet_name,
    )
    # %%
    # al the columns are converted to lower case and stripped of leading/trailing spaces.
    df.columns = df.columns.str.lower().str.strip()

    zepto_nag_prefix_column_name = df.columns[
        [column.startswith("nag-") for column in df.columns]
    ]
    zepto_locations_name = [location.name for location in domain.locations]

    df["rate"] = df["rate"].astype(float)
    df["rate"] = df["rate"].fillna(0)

    df["grand total"] = df["grand total"].astype(float)
    df["grand total"] = df["grand total"].fillna(0)

    df[zepto_nag_prefix_column_name] = df[zepto_nag_prefix_column_name].fillna(0)
    df[zepto_nag_prefix_column_name] = df[zepto_nag_prefix_column_name].astype(float)

    df["uom"] = df["uom"].apply(lambda uom: "#N/A" if str(uom) == "nan" else uom)

    if not any([column.startswith("nag-") for column in df.columns]):
        print("❌ The specified columns does not exist in the file.")
        print("Try to change the domain.")
        exit(0)

    # the "nag-" prefix is removed from the location columns and the actual location name is extracted using the utils.nameExtracter function.
    df.columns = [
        (
            utils.nameExtracter(zepto_locations_name, column[4:])
            if column.startswith("nag-")
            else column
        )
        for column in df.columns
    ]

    zepto_product_info_df = df[["product name", "uom", "rate"]]
    zepto_nag_prefix_location_df = df[zepto_locations_name]

    zepto_nag_prefix_location_df = zepto_nag_prefix_location_df.astype(int)

    return (zepto_product_info_df, zepto_nag_prefix_location_df, zepto_locations_name)


def loadDataZepto(
    file: str, sheet: str, domain: d.DomainSelection
) -> dict[str, pd.DataFrame]:
    print(f"Reading file: {file}")

    zepto_product_info_df, zepto_nag_prefix_location_df, zepto_locations_name = (
        pre_processing_zepto(file, sheet, domain)
    )

    # %%
    # varibale holds invoice data of each location in dictonary format.
    # "Ayodhya Nagar": pd.DataFrame, "Besa": pd.DataFrame, ......
    location_seprated_df: dict[str, pd.DataFrame] = {}
    for location in zepto_locations_name:
        locationSeries = zepto_nag_prefix_location_df[location]
        locationSeries.name = "invoice qty."
        location_seprated_df[location] = pd.concat(
            [zepto_product_info_df, locationSeries], axis=1
        )

        # location_seprated_df[location]["rate"] = location_seprated_df[location]["rate"]

        location_seprated_df[location]["amount"] = location_seprated_df[location][
            "rate"
        ] * location_seprated_df[location]["invoice qty."].astype(float)

        location_seprated_df[location].columns = [
            "article name",
            "uom",
            "rate",
            "invoice qty.",
            "amount",
        ]

        location_seprated_df[location]["recieved qty."] = ""
        location_seprated_df[location]["no"] = range(
            1, len(location_seprated_df[location]) + 1
        )

        location_seprated_df[location] = location_seprated_df[location][
            [
                "no",
                "article name",
                "uom",
                "invoice qty.",
                "recieved qty.",
                "rate",
                "amount",
            ]
        ]

        location_seprated_df[location]["amount"] = location_seprated_df[location][
            "amount"
        ].round(3)

        location_seprated_df[location].columns = location_seprated_df[
            location
        ].columns.str.title()

    # %%
    return location_seprated_df


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
        data = loadDataSwiggy(file, sheetName, domain)  # type: ignore
        print(data)

    typer.run(run)
