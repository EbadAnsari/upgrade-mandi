from typing import Any, Optional, Tuple

from pydantic import BaseModel


class SelectArea(BaseModel):
    row_start: Optional[int] = None
    col_start: Optional[int] = None
    row_span: Optional[int] = None
    col_span: Optional[int] = None

    def generate_value(
        self, type: str, *values: Tuple[Any, Optional[Any]]
    ) -> Tuple[str, Tuple[int, int], Tuple[int, int], Any, Optional[Any]]:
        if not (self.row_span and self.row_start and self.col_span and self.col_start):
            raise Exception(
                "SelectArea must have row_span and row_start and col_span and col_start"
            )
        row_end = self.row_start + self.row_span
        col_end = self.col_start + self.col_span
        return (
            type,
            (
                self.col_start,
                self.row_start,
            ),
            (
                col_end,
                row_end,
            ),
            values[0],
            values[1],
        )
