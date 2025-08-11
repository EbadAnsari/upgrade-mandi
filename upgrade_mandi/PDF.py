from datetime import datetime
from os import makedirs
from os.path import join
from typing import List

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from utils.config import Location, domainConfigClass


class PDF:

    __headingStyle = ParagraphStyle(
        name="Centered",
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )

    __bodyStyle = ParagraphStyle(
        name="Centered", alignment=TA_CENTER, fontName="Helvetica"
    )

    __tableStyle = TableStyle(
        [
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, 0), 6),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 0.1, colors.black),
        ]
    )

    __pageWidth = 550
    __columnWithPercentage = [6, 12, 22, 12, 12, 16, 8, 12]

    __OUTPUT_Folder = join(".", "output")
    # __OUTPUT_REPORT_FOLDER = join(__OUTPUT_Folder, "reports")

    def __dateToStr(self, date: datetime, sep="-", monthFirst: bool = True) -> str:
        """Convert date string to datetime object."""
        if monthFirst:
            return date.strftime(f"%m{sep}%d{sep}%Y")
        else:
            return date.strftime(f"%d{sep}%m{sep}%Y")

    def __init__(
        self,
        data: dict[str, dict],
        date: datetime,
        invoiceVersion: int,
    ):

        self.data = data
        self.date = date
        self.invoiceVersion = invoiceVersion

    def __createDescriptionTable(
        self,
        location: Location,
    ) -> Table:
        vendorName = "Upgrade Mandi"

        data = [
            [
                Paragraph(
                    location.retailer,
                    self.__headingStyle,
                ),
                Paragraph(
                    f"Vendor Name: {vendorName}",
                    self.__headingStyle,
                ),
            ],
            [
                Paragraph(
                    location.locationName,
                    self.__headingStyle,
                ),
                Paragraph(
                    f'Date: {self.__dateToStr(self.date, sep="/", monthFirst=False)}',
                    self.__headingStyle,
                ),
            ],
            [
                Paragraph(
                    f"Shipping Address: {location.shippingAddress}",
                    self.__headingStyle,
                ),
                Paragraph(
                    f"Invoice: {self.data[location.locationName]['invoice-number']}",
                    self.__headingStyle,
                ),
            ],
            ["", Paragraph("Email: ankushmisal7387@gmail.com", self.__headingStyle)],
            ["", Paragraph("PO No", self.__headingStyle)],
        ]
        span = TableStyle([("SPAN", (0, 2), (0, 4))])

        return Table(
            data,
            colWidths=[
                self.__pageWidth * sum(self.__columnWithPercentage[:3]) / 100,
                self.__pageWidth * sum(self.__columnWithPercentage[3:]) / 100,
            ],
            style=span,
        )

    def __createTable(self, df: pd.DataFrame) -> Table:
        return Table(
            self.__preprocessData(df),
            colWidths=[
                self.__pageWidth * (p / 100) for p in self.__columnWithPercentage
            ],
        )

    def __preprocessData(self, df: pd.DataFrame) -> List[List[Paragraph]]:
        df["Sr"] = range(1, len(df) + 1)
        summaryRow = [
            "",
            "",
            "",
            "",
            str(df["Dispatched Qty"].apply(int).sum()),
            "",
            "",
            str(df["Total Amount"].apply(int).sum()),
        ]
        df = (
            [[Paragraph(pdfColumn, self.__headingStyle) for pdfColumn in df.columns]]
            + df.values.tolist()
            + [summaryRow]
        )

        for index, row in enumerate(df[1:-1], start=1):
            row[0] = index
            for i in range(len(row)):
                row[i] = Paragraph(str(row[i]), self.__bodyStyle)
        return df

    def buildPDF(self, folderPathForPdf: str):

        for location in domainConfigClass.locations:
            descriptionTable = self.__createDescriptionTable(location)
            descriptionTable.setStyle(self.__tableStyle)

            table = self.__createTable(self.data[location.locationName]["data-frame"])
            table.setStyle(self.__tableStyle)

            # makedirs(f"./output/pdfs/", exist_ok=True)

            pdf = SimpleDocTemplate(
                filename=f"{folderPathForPdf}/{self.__dateToStr(self.date)} - {location.locationName}.pdf",
                pagesize=A4,
                topMargin=30,
                bottomMargin=30,
            )

            pdf.build([descriptionTable, table])

            print(
                f'PDF generated at "{folderPathForPdf}/{self.__dateToStr(self.date)} - {location.locationName}.pdf"'
            )
