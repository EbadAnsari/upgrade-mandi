from dataclasses import dataclass, field
from enum import Enum
from typing import IO, Any, List, Literal, Optional, Tuple, Union, Unpack

import numpy as np
import pandas as pd
from pydantic import BaseModel, field_validator, model_validator
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus import Table as _Table
from reportlab.platypus import TableStyle
from utils.pdf import Padding


@dataclass
class Grid:
    row_start: Optional[int] = None
    col_start: Optional[int] = None
    row_span: Optional[int] = None
    col_span: Optional[int] = None


@dataclass
class Cell(Text):
    padding: Padding = field(default_factory=Padding)
    line: Line = field(default_factory=Line)


@dataclass
class Header:
    row: Union[Cell, List[Cell]] = field(default_factory=Cell)


@dataclass
class Body:
    matrix: Union[Cell, List[Cell]] = field(default_factory=Cell)


@dataclass
class Footer:
    row: Union[Cell, List[Cell]] = field(default_factory=Cell)


@dataclass
class Table:
    heading: Header = field(default_factory=Header)
    body: Body = field(default_factory=Body)
    footer: Footer = field(default_factory=Footer)

    columnWidths: Union[int, List[int]] = field(default_factory=list)


class PDF(SimpleDocTemplate):
    __elements: List[Flowable] = []

    def __init__(self, filename: str | IO[bytes], **kw) -> None:
        super().__init__(filename, **kw)
        self.build

    pass


if __name__ == "__main__":
    cell = Cell()
    page = PDF(
        filename="test.pdf",
        pagesize=A4,
        topMargin=30,
        bottomMargin=30,
        leftMargin=30,
        rightMargin=30,
    )

    # page.append

    cell.text = "Hello"
    cell.above = LineStyle(1, colors.black)

    print(cell.text)
