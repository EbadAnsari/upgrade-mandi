from typing import Literal, Union

from pydantic import BaseModel, Field


class Date(BaseModel):
    date: int = Field(gt=0, lt=32)
    month: int = Field(gt=0, lt=13)
    year: int

    def __init__(cls, dateString: str):
        split = dateString.split("-")
        if len(split) != 3:
            raise ValueError(f"Invalid date string: {dateString}")

        date, month, year = map(int, [num.strip() for num in split])

        super().__init__(date=date, month=month, year=year)

    def toString(
        self,
        sep="-",
        order: Union[Literal["DMY"], Literal["MDY"], Literal["YMD"]] = "DMY",
    ):
        date = f"{'0' if self.date < 10 else ''}{self.date}"
        month = f"{'0' if self.month < 10 else ''}{self.month}"

        if order == "DMY":
            return f"{date}{sep}{month}{sep}{self.year}"
        elif order == "MDY":
            return f"{month}{sep}{date}{sep}{self.year}"
        elif order == "YMD":
            return f"{self.year}{sep}{month}{sep}{date}"
        else:
            raise ValueError(f"Invalid order: {order}")
