from os.path import join
from typing import List

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from utils.types import date
from utils.types import domain as d
from utils.types import location


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

    def __init__(
        self,
        domain: d.DomainSelection,
        data: dict[str, dict],
        date: date.Date,
    ):

        self.domain = domain
        self.data = data
        self.date = date

    def __createDescriptionTable(
        self,
        location: location.Location,
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
                    location.name,
                    self.__headingStyle,
                ),
                Paragraph(
                    f'Date: {self.date.toString(sep="/", order="MDY")}',
                    self.__headingStyle,
                ),
            ],
            [
                Paragraph(
                    f"Shipping Address: {location.shippingAddress}",
                    self.__headingStyle,
                ),
                Paragraph(
                    f"Invoice: {location.invoiceNo(self.date, self.domain.vendor.code, self.domain.invoiceVersion)}",
                    self.__headingStyle,
                ),
            ],
            ["", Paragraph("Email: ankushmisal7387@gmail.com", self.__headingStyle)],
            [
                "",
                Paragraph(
                    f"PO No: {location.poNo(self.date, location.storeId)}",
                    self.__headingStyle,
                ),
            ],
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
            # str(df["Rate"].apply(float).sum()),
            str(df["Total Amount"].apply(float).sum()),
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

        totalPdfCreationCount = []
        unCreatedPdfsCount = []
        for location in self.domain.locations:
            activeDf = self.data[location.name]

            if activeDf.empty:
                unCreatedPdfsCount.append(location.name)
                continue

            descriptionTable = self.__createDescriptionTable(location)
            descriptionTable.setStyle(self.__tableStyle)

            table = self.__createTable(activeDf)
            table.setStyle(self.__tableStyle)

            pdf = SimpleDocTemplate(
                filename=f"{folderPathForPdf}/{self.date.toString()} - {location.name}.pdf",
                pagesize=A4,
                topMargin=30,
                bottomMargin=30,
            )

            pdf.build([descriptionTable, table])

            # print(
            # f'PDF generated at "{folderPathForPdf}/{self.__dateToStr(self.date)} - {location.locationName}.pdf"'
            # )
            totalPdfCreationCount.append(location.name)
        print(f"Total PDFs created: {len(totalPdfCreationCount)}")
        print(f"PDFs not created: {unCreatedPdfsCount}")
