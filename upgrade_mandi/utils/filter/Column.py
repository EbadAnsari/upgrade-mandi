from typing import Generic, TypeAlias, TypeVar, Union

from .data_types import Date, Float, Int, String

DataType = TypeVar("DataType", "String", "Int", "Float", "Date")

ColumnNameType: TypeAlias = str | int


class Column(Generic[DataType]):
    data_type: DataType
    key: ColumnNameType

    def __init__(self, column_name: ColumnNameType, data_type: DataType) -> None:
        self.data_type = data_type
        self.key = column_name
