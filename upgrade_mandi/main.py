from os.path import join
from pathlib import Path

import pandas as pd
from utils.filter import Column, Condition, ConditionMetaData, ConditionType, Filter
from utils.filter.data_types import Date, Float, Int, String
from utils.read import readExcel

path = join(Path(__file__).parent, "utils", "heavy.xlsx")

df = readExcel(file=path, sheetName="Sheet1")

filter = Filter()


def func(cmd: ConditionMetaData[Int], string: int) -> bool:
    # return cpd.data.lower().startswith(string.lower())
    return cmd.data > string


condition = Condition(
    column=Column(column_name="Indents", data_type=Int()),
    condition_type=ConditionType.match,
    condition=func,
    paremeter_list=[20],
)

filter.add(condition)


df = filter.apply(df)

print(df)
