from datetime import datetime
from os import makedirs
from os.path import join
from turtle import right
from typing import Any, List, Tuple

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from utils.load import Customer, loadDateB2B
from utils.types import date
from utils.types import domain as d
from utils.types import location


class B2B_PDF:

    __headingStyle = ParagraphStyle(
        name="Centered",
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=25,
        # backColor=colors.HexColor("#D3D3D3"),
    )

    __outer_border = TableStyle([("GRID", (0, 0), (-1, -1), 0.1, colors.black)])

    __sub_heading_style = ParagraphStyle(
        name="Centered", fontName="Helvetica-Bold", fontSize=14, leading=14
    )

    __body_style_14px_centered = ParagraphStyle(
        name="Centered", fontName="Helvetica", fontSize=14, alignment=TA_CENTER
    )
    __body_style_10px_centered = ParagraphStyle(
        name="Centered", fontName="Helvetica", fontSize=10, alignment=TA_CENTER
    )

    __body_style_14px = ParagraphStyle(
        name="Centered", fontName="Helvetica", fontSize=14
    )

    __body_style_10px = ParagraphStyle(
        name="Centered", fontName="Helvetica", fontSize=10
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

    __pageWidth = 540
    __table_column_percentage = [10, 42, 16, 16, 16]

    def __init__(self, customer_info: Customer, date: date.Date):
        self.customer_info = customer_info
        self.date = date

        if sum(self.__table_column_percentage) != 100:
            raise Exception("Sum of column percentage is not 100%")

    # address: str, state: str, phone: str, email: str, remain_width: int
    def __bill_from(
        self,
    ):
        bill = Paragraph("Bill from:", self.__body_style_10px)
        sub_heading = Paragraph("Upgrade Mandi", self.__sub_heading_style)

        style = TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                # ("GRID", (0, 0), (-1, -1), 0.1, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )

        data = [
            [
                Paragraph("Address:", self.__body_style_10px),
                Paragraph(
                    "Vijay Nagar, <br/>Near Laxminagar Masjid,<br/>Kalamna, Nagpur,<br/>Maharashtra, India<br/>440022",
                    self.__body_style_10px,
                ),
            ],
            [
                Paragraph("Phone:", self.__body_style_10px),
                Paragraph(
                    "7385994320",
                    self.__body_style_10px,
                ),
            ],
            [
                Paragraph("Email:", self.__body_style_10px),
                Paragraph(
                    "upgrademandi7@gmail.com",
                    self.__body_style_10px,
                ),
            ],
        ]
        table = Table(
            data,
            [(self.__pageWidth / 3 - 6) * 0.25, (self.__pageWidth / 3 - 6) * 0.73],
            style=style,
        )
        return [bill, Spacer(0, 10), sub_heading, Spacer(0, 10), table]

    def __bill_to(
        self,
    ):
        bill = Paragraph("Bill to:", self.__body_style_10px)
        sub_heading = Paragraph(
            self.customer_info.customer_name.title(), self.__sub_heading_style
        )

        style = TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                # ("GRID", (0, 0), (-1, -1), 0.1, colors.black),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )

        data = [
            [
                Paragraph("Address:", self.__body_style_10px),
                Paragraph(
                    f"{self.customer_info.location.title()}, Nagpur,<br/>Maharashtra, India",
                    self.__body_style_10px,
                ),
            ],
            [
                Paragraph("Date", self.__body_style_10px),
                Paragraph(
                    f"{self.date.toString(sep='/')}",
                    self.__body_style_10px,
                ),
            ],
        ]
        table = Table(
            data,
            [(self.__pageWidth / 3 - 6) * 0.25, (self.__pageWidth / 3 - 6) * 0.73],
            style=style,
        )
        return [bill, Spacer(0, 10), sub_heading, Spacer(0, 10), table]

    def __qr(self):
        image = Image("qr.jpg")
        image.drawWidth = 120
        image.drawHeight = 120
        return Table(
            data=[
                [
                    image,
                ],
                [Paragraph("Scan to Pay", self.__body_style_10px_centered)],
            ],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("LEFTPADDING", (0, 0), (-1, -1), 0),
                    ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
                    ("TOPPADDING", (0, 0), (-1, -1), 3),
                ]
            ),
        )

    def __create_data(self):
        left_style = ParagraphStyle(
            name="Centered",
            fontName="Helvetica-BOLD",
            fontSize=12,
            leading=16,
            # textColor=colors.HexColor("#464545"),
        )
        right_style = ParagraphStyle(
            name="Centered",
            fontName="Helvetica-BOLD",
            alignment=TA_RIGHT,
            fontSize=12,
            leading=16,
            # textColor=colors.HexColor("#464545"),
        )
        data = [
            [
                Paragraph(
                    "Sr no.",
                    right_style,
                ),
                Paragraph(
                    "Item Name",
                    left_style,
                ),
                Paragraph("Qty (per kg)", right_style),
                Paragraph("Rate", right_style),
                Paragraph("Amount", right_style),
            ],
        ]

        self.customer_info.data["Amount"] = self.customer_info.data["Qty"].astype(
            float
        ) * self.customer_info.data["Rate"].astype(float)
        total_amount = self.customer_info.data["Amount"].sum()

        for i, row in enumerate(self.customer_info.data.values.tolist()):
            left_style.fontName = right_style.fontName = "Helvetica"
            left_style.textColor = right_style.textColor = colors.black
            data.append(
                [
                    Paragraph(str(i + 1), right_style),
                    Paragraph(row[0], left_style),
                    Paragraph(str(row[1]), right_style),
                    Paragraph(str(row[2]), right_style),
                    Paragraph(str(row[3]), right_style),
                    # Paragraph(str(i[4]), right_style),
                ]
            )
        left_style.fontName = right_style.fontName = "Helvetica-BOLD"
        data.append(
            [
                Paragraph(""),
                Paragraph(""),
                Paragraph(""),
                Paragraph(""),
                Paragraph(str(total_amount), right_style),
            ]
        )

        return Table(
            data,
            colWidths=[
                self.__pageWidth * i / 100 for i in self.__table_column_percentage
            ],
            style=TableStyle(
                [
                    # ("LEFTPADDING", (0, 0), (0, -1), 10),
                    ("RIGHTPADDING", (-1, 0), (-1, -1), 10),
                    ("TOPPADDING", (0, 0), (-1, 0), 5),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 5),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#EFEFEF")),
                    ("GRID", (0, 0), (-1, -1), 0.1, colors.black),
                    ("VALIGN", (1, 1), (-1, -2), "TOP"),
                    ("VALIGN", (0, 1), (0, -1), "TOP"),
                ]
            ),
        )

    def buildPDF(self, folderPathForPdf: str):

        makedirs(folderPathForPdf, exist_ok=True)

        pdf = SimpleDocTemplate(
            filename=f"{folderPathForPdf}/{self.customer_info.customer_name} - {self.customer_info.location} - {self.date.toString()}.pdf",
            pagesize=A4,
            topMargin=30,
            bottomMargin=30,
        )

        page_title = Paragraph("Upgrade Mandi", self.__headingStyle)
        page_sub_title = Paragraph("Invoice", self.__body_style_10px_centered)

        spacer = Spacer(0, 30)

        description = Table(
            [[self.__bill_from(), self.__bill_to(), self.__qr()]],
            colWidths=[
                self.__pageWidth / 3 + 10,
                self.__pageWidth / 3 + 10,
                self.__pageWidth / 3 - 20,
            ],
            style=TableStyle(
                [
                    ("VALIGN", (0, 0), (-2, -1), "TOP"),
                    # ("ALIGN", (-1, -1), (-1, -1), "MIDDLE"),
                    ("VALIGN", (-1, -1), (-1, -1), "BOTTOM"),
                ]
            ),
        )
        description.setStyle(self.__outer_border)

        item_records = self.__create_data()

        # bill_to = self.__bill()

        # description = self.__create_invoice_description()

        pdf.build(
            [
                page_title,
                page_sub_title,
                spacer,
                description,
                Spacer(0, 20),
                item_records,
            ]
        )


if __name__ == "__main__":
    data = loadDateB2B("./raw-sheets-dump/b2b/Transaction List.xlsx", "Sheet1")
    key = list(data.keys())[0]
    cust = data[key][0]
    pdf = B2B_PDF(cust, date.Date(key))

    pdf.buildPDF("./raw-sheets-dump/b2b/pdfs")
