# %%
from datetime import datetime
from os import makedirs
from os.path import join

import pandas as pd
from utils.read import readExcel


def rawToReport(filePath: str):
    # %%
    df, dtype = readExcel(
        filePath,
        sheetName="Sheet1",
    )

    df.columns = [column.strip().lower() for column in df.columns]

    df["indents"] = df["indents"].apply(int)

    # %%
    groupByProductName = df.groupby("item_code")

    # %%
    columnOrder = ["Sr No", "Product Name", "Item Code", "Weight", "Indents", "Final"]

    final = groupByProductName.agg(
        {"product_name": "first", "weight": "first", "indents": "sum"}
    ).sort_values(by="product_name")

    final["Final"] = (
        final["weight"]
        .apply(
            lambda weight: "".join(
                [char for char in weight if 48 <= ord(char) and ord(char) <= 57]
            )
        )
        .astype(int)
        * final["indents"]
    )
    final = final.reset_index()
    final.index = final.index + 1
    final = final.reset_index()


    final["item_code"] = final["item_code"].astype(int)
    final = final.rename(
        {
            "index": "Sr No",
            "product_name": "Product Name",
            "weight": "Weight",
            "indents": "Indents",
            "item_code": "Item Code",
        },
        axis=1,
    )

    # %%
    summaryRow = pd.DataFrame(
        {
            "Sr No": [""],
            "Item Code": [""],
            "Product Name": [""],
            "Weight": [""],
            "Indents": [f'Total: {final["Indents"].sum().astype(int)}'],
            "Final": [""],
        }
    )
    print(final.head(1))
    print(summaryRow.head(1))

    final = pd.concat([final, summaryRow])

    # %%
    makedirs("./output/Report", exist_ok=True)
    # %%
    uniqueDates = df["date"].unique()
    if len(uniqueDates) > 1:
        raise ValueError("Multiple dates found in the data")

    date = datetime.strptime(uniqueDates[0], "%Y-%m-%d").strftime("%d-%m-%Y")

    # %%
    outputFilePath = join("./output/Report", f"Report - {date}.xlsx")
    with pd.ExcelWriter(outputFilePath, engine="xlsxwriter") as writer:
        final[columnOrder].to_excel(
            writer,
            sheet_name="Final Report",
            index=False,
            engine="openpyxl",
            freeze_panes=(1, 0),
            columns=columnOrder,
        )

        workbook = writer.book
        worksheet = writer.sheets["Final Report"]

        # 4. Set custom column widths (Syntax: first_col, last_col, width)
        # worksheet.set_column("A:A", 25)  # Set column A width to 25
        worksheet.set_column("B:B", 40)  # Set column B width to 10
        # worksheet.set_column("C:C", 30)  # Set column C width to 30
        print(f"Report generated successfully at {outputFilePath}")
