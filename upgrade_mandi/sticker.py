from datetime import datetime
from typing import final

import pandas as pd
from cv2 import merge
from pandas import to_datetime
from utils.read import readExcel


def rawToSticker(
    filepath: str,
    sheetName: str,
    shelfLifeFileName: str,
    shelfLifeSheetName: str,
    nxFileName: str,
    nxSheetName: str,
) -> None:
    # %%
    df = readExcel(
        filepath,
        sheetName=sheetName,
    )[0]

    shelfLife = readExcel(shelfLifeFileName, shelfLifeSheetName)[0]
    shelfLife.columns = shelfLife.iloc[0]
    shelfLife = shelfLife.iloc[1:]

    nx = readExcel(nxFileName, nxSheetName)[0]

    df.columns = df.columns.str.strip()
    shelfLife.columns = shelfLife.columns.str.strip()
    nx.columns = nx.columns.str.strip()

    # %%
    merged = df.merge(
        shelfLife, how="inner", left_on="ITEM_CODE", right_on="Article Code"
    )

    # %%
    finalDf = merged.copy()
    finalDf.columns = finalDf.columns.str.strip()
    finalDf = finalDf[
        ["PRODUCT_NAME", "WEIGHT", "Symbol", "Date", "ITEM_CODE", "Indents"]
    ]

    # %%
    finalDf["Date"] = pd.to_datetime(finalDf["Date"])
    finalDf["Date"] = finalDf["Date"] - pd.Timedelta(days=1)

    # %%
    day = finalDf["Date"].apply(lambda x: (x.isoweekday() % 7) + 1).unique()[0] - 1
    dayOfTheWeek = shelfLife.columns[8:15][day]

    # %%
    finalDf[dayOfTheWeek] = finalDf.merge(
        shelfLife, how="inner", left_on="ITEM_CODE", right_on="Article Code"
    )[dayOfTheWeek]

    # %%
    finalDf["ITEM_CODE"] = finalDf["ITEM_CODE"].astype(int)
    nx["ITEM_CODE"] = nx["ITEM_CODE"].astype(int)
    finalDf["Day"] = finalDf[dayOfTheWeek].astype(int)

    # %%
    finalDf["ID"] = finalDf.apply(
        lambda row: "b_"
        + str(row["ITEM_CODE"])
        + "_"
        + (row["Date"] + pd.Timedelta(days=1)).strftime("%d-%m-%Y"),
        axis=1,
    )

    finalDf["NX"] = ""
    for i in nx["ITEM_CODE"]:
        finalDf.loc[finalDf["ITEM_CODE"] == i, "NX"] = "NX"

    # %%
    finalDf = finalDf.loc[finalDf.index.repeat(finalDf["Indents"])]

    finalDf.to_excel("./output/sticker.xlsx", index=False)
