from datetime import datetime
from typing import List

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

from config.utils import config, generateInvoiceId


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

    def __init__(self, date: str, domain: str, config: dict):
        self.date = datetime.strptime(date, "%m-%d-%Y")
        self.domain = domain
        self.columns = config[domain]["output-columns"]
        self.locations = config[domain]["locations"]
        self.data = None

    def loadData(self):
        self.df = pd.read_csv("./data/cleaned/Swiggy.csv")

    def __filterData(self):
        self.df = self.df[self.df["Date"] == self.date.strftime("%m-%d-%Y")].copy()
        self.df["Sr"] = 0
        self.df["Recieved Qty"] = ""

    def __createDescriptionTable(
        self,
        location: str,
        retailer: str,
        shippingAddress: str,
        vendorName: str,
        invoiceVersion: int,
    ) -> Table:
        data = [
            [
                Paragraph(
                    retailer,
                    self.__headingStyle,
                ),
                Paragraph(
                    f"Vendor Name: {vendorName}",
                    self.__headingStyle,
                ),
            ],
            [
                Paragraph(
                    location,
                    self.__headingStyle,
                ),
                Paragraph(
                    f'Date: {self.date.strftime("%d/%m/%Y")}',
                    self.__headingStyle,
                ),
            ],
            [
                Paragraph(
                    f"Shipping Address: {shippingAddress}",
                    self.__headingStyle,
                ),
                Paragraph(
                    f"Invoice: {generateInvoiceId(self.date, self.domain, location, int(invoiceVersion))}",
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

    def __createTable(self):
        return Table(
            self.data,
            colWidths=[
                self.__pageWidth * (p / 100) for p in self.__columnWithPercentage
            ],
        )

    def __preprocessData(self, location: str) -> List[List[Paragraph]]:
        df = self.df[self.df["Location"] == location][self.columns]
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
        self.data = (
            [[Paragraph(column, self.__headingStyle) for column in self.columns]]
            + df.values.tolist()
            + [summaryRow]
        )

        for index, row in enumerate(self.data[1:-1], start=1):
            row[0] = index
            for i in range(len(row)):
                row[i] = Paragraph(str(row[i]), self.__bodyStyle)

    def buildPDF(self, location: str):
        self.__filterData()
        for location in self.locations:
            self.__preprocessData(location)

            descriptionTable = self.__createDescriptionTable(
                location,
                self.locations[location]["retailer"],
                self.locations[location]["shipping-address"],
                "Upgrade Mandi",
                self.df["Invoice Version"].values[0],
            )
            descriptionTable.setStyle(self.__tableStyle)

            table = self.__createTable()
            table.setStyle(self.__tableStyle)

            pdf = SimpleDocTemplate(
                filename=f'./{self.date.strftime("%m-%d-%Y")} - {location}.pdf',
                pagesize=A4,
                topMargin=30,
                bottomMargin=30,
            )

            pdf.build([descriptionTable, table])

            print(
                f'PDF generated at "./{self.date.strftime("%m-%d-%Y")} - {location}.pdf"'
            )


if __name__ == "__main__":
    pdf = PDF("04-16-2025", "Swiggy", config)
    pdf.loadData()
    pdf.buildPDF("Dharampeth")
