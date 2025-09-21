from typing import Optional

from pydantic import BaseModel

from .column import ColumnDefaultConfig


class DatabaseConfig(ColumnDefaultConfig, BaseModel):
    columnName: Optional[str]
