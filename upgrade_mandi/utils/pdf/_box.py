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

from ._cords import SelectArea


@dataclass
class BoxModel:
    top: int = 0
    right: int = 0
    bottom: int = 0
    left: int = 0


class Padding(BoxModel, SelectArea, BaseModel):
    pass


@dataclass
class PageMargin(BoxModel):
    pass
