from typing import Optional

from pydantic import BaseModel

from .column import ColumnDefaultConfig


class InvoicePdfConfig(ColumnDefaultConfig, BaseModel):
    index: Optional[int] = None
    heading: Optional[bool] = None
