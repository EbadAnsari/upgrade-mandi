from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Generic, List, TypeAlias, TypeVar

import pandas as pd
from pydantic import BaseModel

from .Column import Column, DataType


class ConditionType(Enum):
    match = "match"
    remove = "remove"
    update = "update"


@dataclass
class ConditionMetaData(Generic[DataType]):
    column: Column[DataType] | None
    condition_type: ConditionType | None
    data: DataType


ConditionFunctionType: TypeAlias = Callable[[ConditionMetaData, Any], bool]
ConditionFunctionParameterListType: TypeAlias = List[Any]


@dataclass
class Condition(Generic[DataType]):
    column: Column[DataType] | None = field(default=None)
    condition_type: ConditionType | None = field(default=None)
    condition: ConditionFunctionType = field(default=lambda x, y: True)
    paremeter_list: List[Any] = field(default_factory=list)

    def add_condition(self, condition: ConditionFunctionType):
        self.condition = condition
