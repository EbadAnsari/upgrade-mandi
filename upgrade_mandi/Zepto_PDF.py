from datetime import datetime
from os.path import join
from typing import List

import pandas as pd
from pre import loadDataZepto
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle
from utils import config, types


class Zepto_PDF:

    __headingStyleCentered = ParagraphStyle(
        name="Centered",
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )
    __headingStyleLeft = ParagraphStyle(
        name="Centered",
        fontName="Helvetica-Bold",
    )
    __headingStyleRight = ParagraphStyle(
        name="Centered",
        alignment=TA_RIGHT,
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
    # 12 - 2 - 2 - 2 - 2 - 2 - 2
    __columnWithPercentage = [6, 26, 16, 14, 18, 8, 12]

    def __dateToStr(self, date: datetime, sep="-", monthFirst: bool = True) -> str:
        """Convert date string to datetime object."""
        if monthFirst:
            return date.strftime(f"%m{sep}%d{sep}%Y")
        else:
            return date.strftime(f"%d{sep}%m{sep}%Y")

    def __init__(
        self,
        domain: types.DomainSelection,
        data: dict[str, dict],
        date: types.Date,
        locationPo: dict[str, str] = {},
    ):

        self.domain = domain
        self.data = data
        self.date = date
        self.locatioPo = locationPo

        if sum(self.__columnWithPercentage) != 100:
            raise Exception("Sum of column percentage is not 100%")

    def __createDescriptionTable(
        self,
        location: types.Location,
    ) -> Table:
        data = [
            [
                Paragraph(
                    self.domain.vendor.name,
                    self.__headingStyleCentered,
                ),
                "",
            ],
            [
                Paragraph(
                    self.domain.vendor.dispatchedAddress,
                    self.__headingStyleCentered,
                ),
                "",
            ],
            [
                Paragraph(
                    f"Email: {self.domain.vendor.email}",
                    self.__headingStyleLeft,
                ),
                Paragraph(
                    f"Mob: {self.domain.vendor.mobile.e164}",
                    self.__headingStyleRight,
                ),
            ],
            [
                Paragraph(
                    "Cash/Credit Bill",
                    self.__headingStyleCentered,
                ),
                "",
            ],
            [
                Paragraph(
                    f"Invoice No: {location.invoiceNo(self.date, self.domain.vendor.code, self.domain.invoiceVersion)}",
                    self.__headingStyleLeft,
                ),
                Paragraph(
                    f"Date: {self.date.toString()}",
                    self.__headingStyleRight,
                ),
            ],
            [
                Paragraph(
                    f'PO No. {self.locatioPo[location.name] if location.name in self.locatioPo else ""}',
                    self.__headingStyleLeft,
                ),
                "",
            ],
            [Paragraph(location.shippingAddress, self.__headingStyleLeft)],
        ]
        span = TableStyle(
            [
                ("SPAN", (0, 0), (1, 0)),
                ("SPAN", (0, 1), (1, 1)),
                ("SPAN", (0, 3), (1, 3)),
                ("SPAN", (0, 5), (1, 5)),
                ("SPAN", (0, 6), (1, 6)),
                # ("SPAN", (0, 2), (0, 4)),
            ]
        )

        return Table(
            data,
            colWidths=[
                self.__pageWidth * sum(self.__columnWithPercentage[:3]) / 100,
                self.__pageWidth * sum(self.__columnWithPercentage[3:]) / 100,
            ],
            style=span,
        )

    def __createTable(self, df: pd.DataFrame) -> Table:
        style = TableStyle(
            [
                ("SPAN", (0, -1), (2, -1)),
            ]
        )
        return Table(
            self.__preprocessData(df),
            colWidths=[
                self.__pageWidth * (p / 100) for p in self.__columnWithPercentage
            ],
            style=style,
        )

    def __preprocessData(self, df: pd.DataFrame) -> List[List[Paragraph]]:
        summaryRow = [
            "Total",
            "",
            "",
            str(df["Invoice Qty."].apply(int).sum()),
            "",
            "",
            str(df["Amount"].apply(int).sum()),
        ]
        df = (
            [
                [
                    Paragraph(pdfColumn, self.__headingStyleCentered)
                    for pdfColumn in df.columns
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

    def __createFooter(self):
        footerStyle = ParagraphStyle(
            name="Centered",
            alignment=TA_LEFT,
            wordWrap="LTR",
        )
        data = [
            [Paragraph("No. of Crates: ", style=footerStyle), "", ""],
            [Paragraph("Dispatch Time: ", style=footerStyle), "", ""],
            [Paragraph("Recieved Time: ", style=footerStyle), "", "For"],
            [
                Paragraph(
                    "Kindly Note that complaints regarding goods you received must be within 24 Hr. after",
                    style=footerStyle,
                ),
                "Receiver Sign",
                "UPGRADE MANDI",
            ],
        ]
        span = TableStyle([("SPAN", (2, 0), (2, 1))])
        return Table(
            data,
            colWidths=[
                self.__pageWidth * sum(self.__columnWithPercentage[:4]) / 100,
                self.__pageWidth * self.__columnWithPercentage[4] / 100,
                self.__pageWidth * sum(self.__columnWithPercentage[5:]) / 100,
            ],
            style=span,
        )

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

            footer = self.__createFooter()
            footer.setStyle(self.__tableStyle)

            pdf = SimpleDocTemplate(
                filename=f"{folderPathForPdf}/{self.date.toString()} - {location.name}.pdf",
                pagesize=A4,
                topMargin=30,
                bottomMargin=30,
            )

            pdf.build([descriptionTable, table, footer])

            # print(
            # f'PDF generated at "{folderPathForPdf}/{self.__dateToStr(self.date)} - {location.locationName}.pdf"'
            # )
            totalPdfCreationCount.append(location.name)
        print(f"Total PDFs created: {len(totalPdfCreationCount)}")
        print(f"PDFs not created: {unCreatedPdfsCount}")


if __name__ == "__main__":
    data = loadDataZepto("./raw-sheets-dump/new.xlsx", types.Zepto, "Sheet1")
    pdf = Zepto_PDF(config.domainConfigClass["Zepto"], data, datetime.now(), 1)
    pdf.buildPDF("./output/Zepto/21-08-2025/pdfs")
