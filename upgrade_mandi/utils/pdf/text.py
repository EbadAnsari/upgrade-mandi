from dataclasses import dataclass, field

from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph

from ._base import _BaseTextFormatting
from ._constants import WordWrap


@dataclass
class Indent:
    left: int = 0
    right: int = 0


@dataclass
class Space:
    before: int = 0
    after: int = 0


@dataclass
class Text(_BaseTextFormatting):

    _text: str = ""

    @property
    def text(self):
        style = ParagraphStyle(
            name="Text",
            alignment=self.align.value,
            fontName=f'{self.font.replace(" ", "-")}{self.bold and "-Bold" or ""}',
            fontSize=self.font_size,
            leading=self.leading,
            spaceBefore=self.space.before,
            spaceAfter=self.space.after,
            leftIndent=self.indent.left,
            rightIndent=self.indent.right,
            wordWrap=self.word_wrap.value,
            backColor=self.back_color,
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
    word_wrap: WordWrap = WordWrap.LTR
