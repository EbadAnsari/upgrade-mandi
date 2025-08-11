from datetime import datetime

import pandas as pd
from utils.config import domainConfigClass


def toExcel(
    df: pd.DataFrame, date: datetime, baseFolerPath: str, invoiceVersion: int = 1
):
    stringDate = date.strftime("%d-%m-%Y")
    with pd.ExcelWriter(
        f"{baseFolerPath}/{stringDate}.xlsx", engine="xlsxwriter"
    ) as xlW:
        for loaction in domainConfigClass.locations:
            activeDF = df[loaction.locationName]["data-frame"]
            activeDF["Sr"] = range(1, len(activeDF) + 1)

            sheetName = f'{stringDate} {loaction.locationName}{" " + invoiceVersion if invoiceVersion > 1 else ""}'

            activeDF.to_excel(
                xlW,
                sheet_name=sheetName,
                startrow=5,
                index=False,
                freeze_panes=(6, 0),
            )

            workBook = xlW.book
            workSheet = xlW.sheets[sheetName]

            headerCellFormat = workBook.add_format(
                {
                    "bold": True,
                    "align": "center",
                    "valign": "vcenter",
                    "text_wrap": True,
                }
            )

            bodyCellFormat = workBook.add_format(
                {
                    "align": "center",
                    "valign": "vcenter",
                    "text_wrap": True,
                }
            )

            borderedCellFormat = workBook.add_format(
                {
                    "align": "center",
                    "valign": "vcenter",
                    "text_wrap": True,
                    "border": 1,
                }
            )

            # Merge cells for header information
            workSheet.merge_range(
                0, 0, 0, 2, df[loaction.locationName]["retailer"], headerCellFormat
            )
            workSheet.merge_range(1, 0, 1, 2, loaction.locationName, headerCellFormat)
            workSheet.merge_range(
                2,
                0,
                4,
                2,
                f'Shipping Address: {df[loaction.locationName]["shipping-address"]}',
                headerCellFormat,
            )

            workSheet.merge_range(
                0, 3, 0, 7, "Vendor Name: Upgrade Mandi", headerCellFormat
            )
            workSheet.merge_range(1, 3, 1, 7, f"Date: {stringDate}", headerCellFormat)
            workSheet.merge_range(
                2,
                3,
                2,
                7,
                f'Invoice: {df[loaction.locationName]["invoice-number"]}',
                headerCellFormat,
            )
            workSheet.merge_range(
                3, 3, 3, 7, "Email: ankushmisal7387@gmail.com", headerCellFormat
            )
            workSheet.merge_range(
                4,
                3,
                4,
                7,
                f'PO No: {df[loaction.locationName]["po-no"]}',
                headerCellFormat,
            )

            # Set column widths and formats
            workSheet.set_column("A:A", 5, bodyCellFormat)
            workSheet.set_column("B:F", 20, bodyCellFormat)
            workSheet.set_column("G:G", 10, bodyCellFormat)
            workSheet.set_column("H:H", 20, bodyCellFormat)

            workSheet.write(
                6 + len(activeDF),
                4,
                activeDF["Dispatched Qty"].sum(),
                borderedCellFormat,
            )
            workSheet.write(
                6 + len(activeDF),
                7,
                activeDF["Total Amount"].sum(),
                borderedCellFormat,
            )
