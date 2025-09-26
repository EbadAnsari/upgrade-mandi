from typing import List, Self

import pandas as pd

from .Condition import Condition, ConditionMetaData, ConditionType
from .data_types import String
from .error import KeyNotFound, KeyOutOfBound


class Filter:
    filter_condition: List[Condition] = []
    view: pd.DataFrame

    def __init__(self, filter_condition: List[Condition] = []) -> None:
        self.filter_condition = filter_condition

    def delete(self, index: int) -> Condition:
        return self.filter_condition.pop(index)

    def clear(self) -> None:
        self.filter_condition.clear()

    def add(self, condition: Condition) -> Self:
        self.filter_condition.append(condition)
        return self

    def apply(self, df: pd.DataFrame) -> pd.DataFrame:
        # for condition in self.filter_condition:
        view = df.copy()
        for condition in self.filter_condition:
            if not condition.column:
                raise Exception("Column is required")

            key = condition.column.key
            if type(key) == str and key not in df.columns:
                raise KeyNotFound(
                    f"Column {key} not found in DataFrame",
                    key,
                )
            elif type(key) == int and len(df.columns) < key:
                raise KeyOutOfBound(
                    f"Column {key} not found in DataFrame",
                    key,
                )
            column_name = df.columns[key] if type(key) == int else key

            cb = condition.condition

            def function(cell):
                if not condition.column:
                    return True

                value = cb(
                    ConditionMetaData(
                        column=condition.column,
                        condition_type=ConditionType.match,
                        data=cell,
                    ),
                    *condition.paremeter_list,
                )

                return (
                    value
                    if condition.condition_type == ConditionType.match
                    else not value
                )

            view = view[view[column_name].apply(function)]
            # condition.condition
            # pass
        return view
