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


class Align(Enum):
    Left = TA_LEFT
    Center = TA_CENTER
    Right = TA_RIGHT
    Justify = TA_JUSTIFY


class VAlign(Enum):
    Top = "TOP"
    Middle = "MIDDLE"
    Bottom = "BOTTOM"


class WordWrap(Enum):
    LTR = "LTR"
    RTL = "RTL"
    CJK = "CJK"
