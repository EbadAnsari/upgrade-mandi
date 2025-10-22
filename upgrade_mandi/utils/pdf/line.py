from dataclasses import dataclass, field
from typing import Optional

from reportlab.lib import colors

from ._cords import SelectArea


@dataclass
class LineStyle:
    width: float = 0
    color: colors.Color = colors.black


@dataclass
class Line(SelectArea):
    top: Optional[LineStyle] = field(default=None)
    bottom: Optional[LineStyle] = field(default=None)
    left: Optional[LineStyle] = field(default=None)
    right: Optional[LineStyle] = field(default=None)
