# %%
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Tuple

import pandas as pd
from utils.read import readExcel
from utils.types import date


@dataclass
class Customer:
    customer_name: str
    location: str
    data: pd.DataFrame

    def __repr__(self):
        return f"{self.customer_name} - {self.location}"


def loadDateB2B(file_location: str, sheet_name: str):
    df = readExcel(file_location, sheetName=sheet_name)
    df.columns = [column.strip().title() for column in df.columns]

    # %%
    df = (
        df[
            [
                "Date",
                "Name",
                "Address",
                "Item Name",
                "Qty",
                "Rate",
            ]
        ]
        .dropna(
            subset=[
                "Item Name",
                "Qty",
                "Rate",
            ],
            how="all",
        )
        .reset_index(drop=True)
    )

    # %%
    def lower(row: pd.Series) -> pd.Series:
        for key in row.keys():
            row[key] = str(row[key]).title()
        return row

    df[["Address", "Name", "Item Name"]] = df[["Address", "Name", "Item Name"]].apply(
        lower
    )
    df[["Qty", "Rate"]] = df[["Qty", "Rate"]].astype(int)

    df["Date"] = pd.to_datetime(df["Date"]).apply(
        lambda date: date.strftime("%d-%m-%Y")
    )

    # %%

    groups = df.groupby(["Date", "Name", "Address"]).groups

    newDf = df.drop(labels=["Date", "Name", "Address"], axis=1).copy()

    # groups = { key: df.iloc[value] for key, value in groups.items() }

    by_dates: dict[str, List[Customer]] = {}

    for _key, value in groups.items():
        key: Tuple[str, str, str] = tuple(_key)  # type: ignore
        if key[0] not in by_dates:
            by_dates[key[0]] = []
        customer = Customer(key[1], key[2], newDf.iloc[value])
        by_dates[key[0]].append(customer)

    return by_dates
