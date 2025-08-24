from os.path import join

import pandas as pd
from utils import config, types


class Excel:
    def __init__(
        self,
        df: pd.DataFrame,
        domain: types.DomainSelection,
        date: types.Date,
        invoiceVersion: int = 1,
    ):
        self.df = df
        self.domain = domain
        self.date = date
        self.invoiceVersion = invoiceVersion


def toExcelSwiggy(
    df: pd.DataFrame,
    domain: types.DomainSelection,
    date: types.Date,
    baseFolerPath: str,
    invoiceVersion: int = 1,
):
    stringDate = date.toString()
    with pd.ExcelWriter(
        join(baseFolerPath, f"{stringDate}.xlsx"), engine="xlsxwriter"
    ) as xlW:
        for location in domain.locations:
            activeDF = df[location.name]
            if activeDF.empty:
                # print(
                #     f"No data found for the location: {location.locationName}.\nWhen creating excel file."
                # )
                continue

            activeDF["Sr"] = range(1, len(activeDF) + 1)

            sheetName = f'{stringDate} {location.name}{" " + invoiceVersion if invoiceVersion > 1 else ""}'

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
            workSheet.merge_range(0, 0, 0, 2, location.retailer, headerCellFormat)
            workSheet.merge_range(1, 0, 1, 2, location.name, headerCellFormat)
            workSheet.merge_range(
                2,
                0,
                4,
                2,
                f"Shipping Address: {location.shippingAddress}",
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
                f"Invoice: {location.invoiceNo(date, domain.vendor.code)}",
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
                f"PO No: {location.poNo(date, domain.vendor.supplierId)}",
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


def toExcelZepto(
    df: pd.DataFrame,
    date: types.Date,
    baseFolderPathExcel: str,
    invoiceVersion: int = 1,
    locationPo: dict[str, str] = {},
):
    stringDate = date.toString()

    with pd.ExcelWriter(
        join(baseFolderPathExcel, f"{stringDate}.xlsx"), engine="xlsxwriter"
    ) as xlW:
        for location in config.domainConfigClass["Zepto"].locations:
            activeDF = df[location.name]
            if activeDF.empty:
                continue

            sheetName = f'{stringDate} {location.name}{" " + invoiceVersion if invoiceVersion > 1 else ""}'

            activeDF.to_excel(
                xlW,
                sheet_name=sheetName,
                startrow=7,
                index=False,
                freeze_panes=(8, 0),
            )

            workBook = xlW.book
            workSheet = xlW.sheets[sheetName]

            title = workBook.add_format(
                {
                    "bold": True,
                    "align": "center",
                    "valign": "vcenter",
                    "text_wrap": True,
                    "font_size": 20,
                    "color": "#00af50",
                }
            )

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

            leftAlign = workBook.add_format(
                {"align": "left", "valign": "vcenter", "text_wrap": True, "bold": True}
            )

            rightAlign = workBook.add_format(
                {"align": "right", "valign": "vcenter", "text_wrap": True, "bold": True}
            )

            center = workBook.add_format({"align": "center"})

            workSheet.merge_range(
                0, 0, 0, 6, config.domainConfigClass["Zepto"].vendor.name, title
            )

            workSheet.merge_range(
                1,
                0,
                1,
                6,
                config.domainConfigClass["Zepto"].vendor.dispatchedAddress,
                headerCellFormat,
            )

            workSheet.merge_range(
                2,
                0,
                2,
                2,
                f'Email: {config.domainConfigClass["Zepto"].vendor.email}',
                leftAlign,
            )

            workSheet.merge_range(
                2,
                3,
                2,
                6,
                f'Mob: {config.domainConfigClass["Zepto"].vendor.mobile.e164}',
                rightAlign,
            )

            workSheet.merge_range(
                3,
                0,
                3,
                6,
                "Cash/Credit Bill",
                headerCellFormat,
            )

            workSheet.merge_range(
                4,
                0,
                4,
                2,
                f'Invoice No: {location.invoiceNo(date, config.domainConfigClass["Zepto"].vendor.code)}',
                leftAlign,
            )

            workSheet.merge_range(
                4,
                3,
                4,
                6,
                f"Date: {stringDate}",
                rightAlign,
            )

            workSheet.merge_range(
                5,
                0,
                5,
                6,
                f"PO No: {locationPo[location.name] if location.name in locationPo else ''}",
                leftAlign,
            )

            workSheet.merge_range(
                6,
                0,
                6,
                6,
                location.shippingAddress,
                leftAlign,
            )

            workSheet.set_column("A:A", 5)
            workSheet.set_column("B:G", 20)

            workSheet.write(
                7 + len(activeDF) + 1,
                3,
                activeDF["Invoice Qty."].sum(),
                borderedCellFormat,
            )
            workSheet.write(
                7 + len(activeDF) + 1, 6, activeDF["Amount"].sum(), borderedCellFormat
            )

            offset = 7 + len(activeDF) + 2
            workSheet.merge_range(
                offset,
                0,
                offset,
                3,
                "No. of Crates: ",
                leftAlign,
            )

            workSheet.merge_range(
                offset + 1,
                0,
                offset + 1,
                3,
                "Dispatch Time: ",
                leftAlign,
            )

            workSheet.merge_range(
                offset + 2,
                0,
                offset + 2,
                3,
                "Received Time: ",
                leftAlign,
            )

            workSheet.merge_range(
                offset + 3,
                0,
                offset + 3,
                3,
                "Kindly Note that complaints regarding goods you received must be within 24 Hr. after",
                leftAlign,
            )

            workSheet.write(
                offset + 3,
                4,
                "Reciever Sign",
                headerCellFormat,
            )

            workSheet.merge_range(offset, 5, offset + 1, 6, "")

            workSheet.merge_range(offset + 2, 5, offset + 2, 6, "For", center)
            workSheet.merge_range(
                offset + 3, 5, offset + 3, 6, "Upgrade Mandi", headerCellFormat
            )
