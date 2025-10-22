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

from ._constants import Align, VAlign, WordWrap


@dataclass
class _BaseTextFormatting:

    _align: Align = Align.Left

    back_color: colors.Color = colors.transparent
    color: colors.Color = colors.black
    font: str = "Times Roman"
    # how to specify the font
    bold: bool = False
    font_size: int = 10
    leading: int = 12
    wordWrap: WordWrap = WordWrap.LTR

    @property
    def align(self):
        return self._align

    @align.setter
    def align(self, align: Align):
        self._align = align

    vAlign: VAlign = VAlign.Bottom
