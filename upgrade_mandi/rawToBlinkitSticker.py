import pandas as pd
from datetime import date, datetime, timedelta
import numpy as np
from utils import console
from os.path import join

def rawToBlinkitSticker(file, sheetName, itemIdFileName, itemIdSheetName):
    # %%
    raw_df = pd.read_excel(
        file,
        sheet_name=sheetName,
    )
    
    item_id = pd.read_excel(
        itemIdFileName,
        sheet_name=itemIdSheetName,
    )[["Item ID", "UPC"]]


    raw_df["Item ID"]  =raw_df["Item ID"].apply(lambda x: 0 if str(x).lower().strip() == "nan" else int(x))

    newDf = raw_df.merge(item_id, how="inner", left_on="Item ID", right_on="Item ID")

    newDf["Date"] = date.today().strftime("%d-%m-%Y")
    newDf["Best Before Date"] = (datetime.now() + timedelta(days=6)).strftime("%d-%m-%Y")

    finalDf = newDf.loc[newDf.index.repeat(newDf["Final Indent (Qty) Dis"])][
        ["Item Name", "UOM", "Date", "Best Before Date", "UPC"]
    ].reset_index(drop=True)

    finalDf.to_excel(join(console.ConsolePath.output(), "blinkit sticker.xlsx"), index=False)