# %%
from os import makedirs

import numpy as np
import pandas as pd
from utils.utils import nameExtracter

# %%
df = pd.read_excel(
    "./../data/raw/B2B/B2B Daily Update sheet.xlsx", sheet_name="ALL DATA"
)

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
df

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
df

# %%
df.to_excel("./../data/processed/B2B/Transaction List.xlsx", index=False)

# %%
grp = df.groupby(["Date"])

grp_names = list(grp.groups.keys())
ne = grp_names[4]
ne, df[df["Date"] == ne].sort_values("Item Name")[
    ["Date", "Item Name", "Rate"]
].groupby("Item Name")["Rate"].unique()
