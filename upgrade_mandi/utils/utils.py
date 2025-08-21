import os
from collections import Counter
from glob import glob
from os.path import getmtime, join
from typing import List

from . import config, types


def generateInvoiceId(date: types.Date, code: str, invoiceVersion: int):
    return f'{date.toString(sep="")}U{code}{invoiceVersion}'


def generatePONo(date: types.Date, storeId: str, supplierId: str):
    return f'{date.toString(sep="", order="YMD")}-{storeId}-{supplierId}'


def nameExtracter(rightNamesList: List[str], wrongName: str) -> str:
    chances = [0] * len(rightNamesList)

    counterOriginal = Counter(wrongName.lower())
    for i, rightName in enumerate(rightNamesList):
        counterLocation = Counter(rightName.lower())
        chances[i] = (
            sum((counterOriginal & counterLocation).values())
            * 2
            / (sum(counterOriginal.values()) + sum(counterLocation.values()))
        )
    return rightNamesList[chances.index(max(chances))]


def fileInRawSheet() -> List[str]:
    return sorted(
        glob(join(config.PROJECT_SRC, "raw-sheets-dump", "*.xlsx")),
        key=getmtime,
        reverse=True,
    )
