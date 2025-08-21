from dataclasses import dataclass, field
from typing import Any, List, Literal, Optional, Union, Unpack

import numpy as np
import pandas as pd
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
class Indent:
    left: int = 0
    right: int = 0


@dataclass
class Space:
    before: int = 0
    after: int = 0


@dataclass
class Padding:
    left: int = 3
    right: int = 3
    top: int = 3
    bottom: int = 3


@dataclass
class __BaseTextFormatting:

    __align: Literal["left", "center", "right", "justify"] = "left"

    backGround: colors = colors.transparent
    color: colors = colors.black
    font: str = "Times Roman"
    # how to specify the font
    bold: bool = False
    fontSize: int = 10
    leading: int = 12

    @property
    def align(self):
        return {"left": Left, "center": Center, "right": Right, "justify": Justify}[
            self.__align
        ]

    @align.setter
    def align(self, align: Literal["left", "center", "right", "justify"]):
        self.__align = align

    vAlign: Literal["TOP", "MIDDLE", "BOTTOM"] = "BOTTOM"


@dataclass
class Text(__BaseTextFormatting):

    _text: str = ""

    @property
    def text(self):
        style = ParagraphStyle(
            name="Text",
            alignment=self.align,
            fontName=f'{self.font.replace(" ", "-")}{self.bold and "-Bold" or ""}',
            fontSize=self.fontSize,
            leading=self.leading,
            spaceBefore=self.space.before,
            spaceAfter=self.space.after,
            leftIndent=self.indent.left,
            rightIndent=self.indent.right,
            wordWrap=self.wordWrap,
            backColor=self.backGround,
            textColor=self.color,
        )
        return Paragraph(str(self._text), style=style)

    @text.setter
    def text(self, value):
        self._text = value

    underline: bool = False
    strike: bool = False
    indent: Indent = field(default_factory=Indent)
    space: Space = field(default_factory=Space)
    wordWrap: Union[
        Literal["LTR"],
        Literal["RTL"],
        Literal["CJK"],
    ] = "LTR"


@dataclass
class Grid:
    rowStart: Optional[int] = None
    colStart: Optional[int] = None
    rowSpan: Optional[int] = None
    colSpan: Optional[int] = None


@dataclass
class Cell(Text, Grid):
    pass


@dataclass
class LineStyle:
    width: int = 0
    color: colors = colors.black


@dataclass
class Line:
    below: LineStyle = field(default_factory=None)
    above: LineStyle = field(default_factory=None)
    type: Literal["header", "body", "footer"] = "body"

    def getStyle(self):
        config = {
            "header": [(0, 0), (-1, 0)],
            "body": [(0, 1), (-1, -2)],
            "footer": [(0, -1), (-1, -1)],
        }
        style = []
        if self.above:
            style.append(
                (
                    "LINEABOVE",
                    config[self.type][0],
                    config[self.type][1],
                    self.above.width,
                    self.above.color,
                )
            )
        if self.below:
            style.append(
                (
                    "LINEBELOW",
                    config[self.type][0],
                    config[self.type][1],
                    self.below.width,
                    self.below.color,
                )
            )
        return style


@dataclass
class Grid(LineStyle):
    pass


@dataclass
class Table:
    headingStyle: Union[Cell, List[Cell]] = field(default_factory=list)
    footerStyle: Union[Cell, List[Cell]] = field(default_factory=list)
    bodyStyle: Union[Cell, List[Cell]] = field(default_factory=list)
    _headerRow: int = 0
    _footerRow: int = -1

    columnWidths: Union[int, List[int]] = field(default_factory=list)

    pageWidth: int = field(default_factory=None)

    headingLine: Line = field(default_factory=None)
    footerLine: Line = field(default_factory=None)

    grid: Grid = field(default_factory=None)

    tableData: pd.DataFrame = field(default_factory=None)
