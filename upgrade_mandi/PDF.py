from datetime import datetime
from os import makedirs
from os.path import join
from typing import List

import pandas as pd
import typer
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from utils.utils import domainConfig, generateInvoiceId, nameExtracter


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

    def __columnInitializer(self):
        self.pdfColumns = [
            element[0]
            for element in sorted(
                {
                    columnName: columnValue
                    for columnName, columnValue in self.config[self.domain][
                        "columns"
                    ].items()
                    if "invoice-pdf" in columnValue
                    and "index" in columnValue["invoice-pdf"]
                }.items(),
                key=lambda x: x[1]["invoice-pdf"]["index"],
            )
        ]

        self.filteredColumns = {
            columnName: columnValue
            for columnName, columnValue in self.config[self.domain]["columns"].items()
            if "raw-sheet-name" in columnValue
        }

        self.rawSheetColumns = [
            name["raw-sheet-name"]["name"] for name in self.filteredColumns.values()
        ]

    def __strToDate(self, date: str, sep="-", monthFirst: bool = True) -> datetime:
        """Convert date string to datetime object."""
        if monthFirst:
            return datetime.strptime(date, f"%m{sep}%d{sep}%Y")
        else:
            # If the date is in the format of "dd-mm-yyyy"
            # we need to change the order to "mm-dd-yyyy"
            return datetime.strptime(date, f"%d{sep}%m{sep}%Y")

    def __dateToStr(self, date: datetime, sep="-", monthFirst: bool = True) -> str:
        """Convert date string to datetime object."""
        if monthFirst:
            return date.strftime(f"%m{sep}%d{sep}%Y")
        else:
            return date.strftime(f"%d{sep}%m{sep}%Y")

    def __init__(
        self,
        fileName: str,
        sheetName: str,
        domain: str,
        config: dict,
        invoiceVersion: int,
    ):
        self.config = config
        self.domain = domain

        self.__columnInitializer()

        # self.columns = config[domain]["output-columns"]
        self.locations = config[domain]["locations"]
        self.data = None

        self.fileName = fileName
        self.sheetName = sheetName

        self.invoiceVersion = invoiceVersion

        self.__pdfDf = None

    def loadData(self):
        # self.df = pd.read_csv("./data/cleaned/Swiggy.csv")

        df = pd.read_excel(self.fileName, sheet_name=self.sheetName)
        df.dropna(inplace=True, how="all")

        extractPDFColumns = [
            columnName
            for columnName, columnValue in self.config[self.domain]["columns"].items()
            if "invoice-pdf" in columnValue and "raw-sheet-name" not in columnValue
        ]

        df = df[self.rawSheetColumns]
        df.columns = list(self.filteredColumns.keys())

        df["Location"] = df["Location"].apply(
            lambda location: nameExtracter(list(self.locations.keys()), location)
        )

        for i in extractPDFColumns:
            df[i] = range(1, len(df) + 1)

        self.__pdfDf = df.copy()
        df["Date"] = pd.to_datetime(
            df["Date"], format="%d-%m-%Y", errors="coerce", utc=True
        )
        # print(f"PDF Columns: {}")
        self.date = self.__strToDate(df["Date"][0].strftime("%m-%d-%Y"))
        # exit(0)

    def __filterByLoaction(self, location: str) -> pd.DataFrame:
        # print(self.__pdfDf.columns)
        return self.__pdfDf[self.__pdfDf["Location"] == location][
            self.pdfColumns
        ].copy()

    # def __filterData(self):
    #     self.df = self.df[self.df["Date"] == self.__dateToStr(self.date)].copy()
    # self.df["Sr"] = 0
    # self.df["Recieved Qty"] = ""

    def __createDescriptionTable(
        self,
        location: str,
    ) -> Table:
        retailer = self.locations[location]["retailer"]
        shippingAddress = self.locations[location]["shipping-address"]
        # vendorName = self.locations[location]["Vendor Name"]
        vendorName = "Upgrade Mandi"

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
                    f'Date: {self.__dateToStr(self.date, sep="/", monthFirst=False)}',
                    self.__headingStyle,
                ),
            ],
            [
                Paragraph(
                    f"Shipping Address: {shippingAddress}",
                    self.__headingStyle,
                ),
                Paragraph(
                    f"Invoice: {generateInvoiceId(self.date, self.domain, location, self.invoiceVersion)}",
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
            [
                [
                    Paragraph(pdfColumn, self.__headingStyle)
                    for pdfColumn in self.pdfColumns
                ]
            ]
            + df.values.tolist()
            + [summaryRow]
        )

        for index, row in enumerate(df[1:-1], start=1):
            row[0] = index
            for i in range(len(row)):
                row[i] = Paragraph(str(row[i]), self.__bodyStyle)
        return df

    def buildPDF(self):
        # self.__filterData()
        for location in self.locations.keys():
            descriptionTable = self.__createDescriptionTable(
                location
                # self.df["Invoice Version"].values[0],
            )
            descriptionTable.setStyle(self.__tableStyle)

            table = self.__createTable(self.__filterByLoaction(location))
            table.setStyle(self.__tableStyle)

            makedirs(f"./pdfs/{ self.__dateToStr(self.date)}", exist_ok=True)

            pdf = SimpleDocTemplate(
                filename=f"./pdfs/{self.__dateToStr(self.date)}/{self.__dateToStr(self.date)} - {location}.pdf",
                pagesize=A4,
                topMargin=30,
                bottomMargin=30,
            )

            pdf.build([descriptionTable, table])

            print(
                f'PDF generated at "./pdfs/{self.__dateToStr(self.date)}/{self.__dateToStr(self.date)} - {location}.pdf"'
            )


if __name__ == "__main__":

    def run(
        file: str = typer.Option(..., "--file", "-f", help="Excel file path"),
        domain: str = typer.Option("Swiggy", "--domain", "-d", help="Excel file path"),
        invoiceVersion: int = typer.Option(
            1, "--invoice-version", "-i", help="Excel file path"
        ),
        sheetName: str = typer.Option(
            "Sheet1", "--sheet-name", "-s", help="Excel file path"
        ),
    ):
        # print(file, domain, invoiceVersion, sheetName)
        pdf = PDF(file, sheetName, domain, domainConfig, invoiceVersion)
        pdf.loadData()
        pdf.buildPDF()

    typer.run(run)
