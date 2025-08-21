from dataclasses import dataclass, field
from typing import Any, List, Literal, Optional, Union, Unpack

import numpy as np
import pandas as pd
import styles
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER as Center
from reportlab.lib.enums import TA_JUSTIFY as Justify
from reportlab.lib.enums import TA_LEFT as Left
from reportlab.lib.enums import TA_RIGHT as Right
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus import Table as _Table
from reportlab.platypus import TableStyle


@dataclass
class Table(styles.Table):

    def __init__(self):
        pass

    def build(self) -> _Table:
        headerRow = []
        if type(self.headingStyle) is not list:
            self.headingStyle = [self.headingStyle] * len(self.tableData.columns)
        for columnName, headerStyled in zip(self.tableData.columns, self.headingStyle):
            headerStyled.text = columnName
            headerRow.append(headerStyled.text)

        footerRow = []
        # if type(self.footerStyle) is not list:
        #     self.footerStyle = [self.footerStyle] * len(self.tableData.columns)

        # for columnName, footerStyled in zip(self.tableData.columns, self.footerStyle):
        #     footerStyled.text = columnName
        #     footerRow.append(footerStyled.text)

        tableStyle = []

        if self.headingLine:
            tableStyle.extend(self.headingLine.getStyle())
            # print(tableStyle)

        tableData = self.tableData.values.tolist()
        tableData.insert(0, headerRow)

        if type(self.columnWidths) is list:
            if len(self.columnWidths) != len(self.tableData.columns):
                raise Exception(
                    "Column widths must be equal to number of columns in table"
                )
            elif self.pageWidth is None:
                raise Exception("Page width must be set if using column widths")

        tbl = _Table(
            tableData,
            colWidths=(
                list(
                    map(
                        lambda widthPercentage: self.pageWidth
                        * (widthPercentage / 100),
                        self.columnWidths,
                    )
                )
                if type(self.columnWidths) is list
                else [self.columnWidths] * len(self.tableData.columns)
            ),
        )
        tbl.setStyle(tableStyle)
        return tbl


@dataclass
class experimental_PDF:

    lst: List[Any] = field(default_factory=list)

    def __init__(self):
        self.document = SimpleDocTemplate(
            filename="test.pdf",
            pagesize=A4,
            topMargin=30,
            bottomMargin=30,
        )
        self.lst = []

    def addComponent(self, components: Any):
        self.lst.append(components)

    def build(self):
        self.document.build(self.lst)
        pass


df = pd.DataFrame(
    {
        "A": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "B": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "C": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "D": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "E": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "F": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "G": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
        "H": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
    }
)


summary = [
    "",
    "",
    "",
    "",
    df["E"].sum(),
    "",
    df["G"].sum(),
    "",
]
df.loc[len(df) - 1] = summary

if __name__ == "__main__":
    a = experimental_PDF()

    table = Table()
    table.pageWidth = 550
    table.headingStyle = styles.Cell(
        font="Helvetica",
        bold=True,
    )
    table.tableData = df
    table.columnWidths = [6, 12, 22, 12, 12, 16, 8, 12]

    # temp = styles.Line(
    #     below=styles.LineStyle(1, colors.black),
    #     type="body",
    #     above=None,
    # )
    table.headingLine = styles.Line(
        below=styles.LineStyle(1), above=None, type="header"
    )

    a.addComponent(table.build())

    a.build()
