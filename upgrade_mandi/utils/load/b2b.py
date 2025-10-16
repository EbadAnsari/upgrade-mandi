# %%
from dataclasses import dataclass
from datetime import datetime
from typing import Any, List, Tuple

import numpy as np
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


def filter_b2b(file_name: str, sheet_name="ALL DATA") -> pd.DataFrame:
    # %%
    df = pd.read_excel(file_name, sheet_name)

    df.columns = [i.strip().title() for i in df.columns]
    df = (
        df.dropna(how="all")
        .drop(
            labels=["Sr No", "Total Amount", "Overall"],
            axis=1,
        )
        .dropna(how="all")
    )

    # %%
    def formatDate(row: pd.Series) -> pd.Timestamp | float:
        try:
            return pd.to_datetime(row["Date"])
        except:
            return np.nan

    df["Date"] = df.apply(formatDate, axis=1).ffill()

    # %%
    df.dropna(subset=df.columns.difference(["Date"]), how="all", inplace=True)

    # %%
    df[["Name", "Address"]] = (
        df[["Name", "Address"]]
        .ffill()
        .apply(
            lambda srs: pd.Series(
                name=srs.name, data=[str(string).title() for string in srs]
            ),
            axis=1,
        )
    )

    df["Item Name"] = df["Item Name"].apply(lambda name: str(name).title())

    # %%
    lst = [
        "Red Onion Premium Wholesale",
        "Red Onion Premium Retail",
        "White onion Wholesale",
        "White onion Retail",
        "Agra potato Premium Wholesale",
        "Agra Potato Premium Retail",
        "Agra Potato Retail Big",
        "G4 potato Wholesale",
        "G4 Potato Retail",
        "Ginger Banglore",
        "Garlic Regular",
        "Garlic Bolder",
        "Onion B",
        "Potato B",
        "Ginger B",
        "White Onion B",
        "Potato Small",
    ]

    # %%
    df = df.dropna(
        subset=[
            "Item Name",
        ],
        how="all",
    )

    # %%
    return df


def loadDateB2B(file_location: str, sheet_name: str):
    df = filter_b2b(file_location, sheet_name)
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

    df[["Qty", "Rate"]] = df[["Qty", "Rate"]].astype(float)

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
